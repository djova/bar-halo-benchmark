"""Frozen 100-CPU-second finite-map pilot, requiring coordinator launch approval.

This is a method/cost pilot, not a converged spatial echo experiment. All
numerical work, including startup, runs in one capped process. No live gravity.
"""
import os
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'

import argparse
import datetime
import json
import math
from pathlib import Path
import resource
import signal
import sys
import time
import traceback

# Install a process-wide ceiling before importing the scientific libraries.
resource.setrlimit(resource.RLIMIT_CPU, (98, 100))


class BudgetExhausted(RuntimeError):
    pass


def cpu_signal(signum, frame):
    raise BudgetExhausted('Process CPU soft limit reached; hard ceiling is 100 seconds.')


signal.signal(signal.SIGXCPU, cpu_signal)
LAUNCH_WALL = time.monotonic()

import numpy as np
from scipy.special import jv, roots_hermitenorm, roots_legendre
from echo_halo import agama, coordinates, digest, potential_energy
from echo_monopole import Cohort, radial_parameters
from echo_multipole_pulse import IntegratedMultipolePulse
from echo_two_frequency import readout_radial

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / 'results/discovery-20261001/echoes/two-frequency-ne512-L24-01'
PROTOCOL = ROOT / 'research/discovery-20261001/ECHO_FINITE_PREFLIGHT_PROTOCOL.md'
OWNED_OUTPUT = None
EXPECTED_AGAMA = 'f6c04e4941aff3538d3bb08f6446d731b788d85406af94092cf856fbd139d000'
EXPECTED_REFERENCE = '2d26635a86096770e0187a812a1c99728fd13591f85e8531703df42ca99c777c'
SOURCES = ('echo_finite_preflight.py', 'echo_halo.py', 'echo_monopole.py',
           'echo_multipole_pulse.py', 'echo_two_frequency.py')
SHAPE_SIGNS = ((1, 1), (1, -1), (-1, 1), (-1, -1))
CONTRAST_SIGNS = np.array([1., -1., -1., 1.]) / 4
FROZEN = dict(
    process_cpu_ceiling_seconds=100, checkpoint_cpu_seconds=96,
    known_limit_cpu_ceiling_seconds=20, known_limit_checkpoint_seconds=19,
    chunk_size=32768, self_gravity=False, tau=16., amplitudes=[1., .5],
    pulse_A=dict(ell=2, mass_integral=.006, scale=.8, epsilon=.5, orientation=0.),
    pulse_B=dict(ell=4, mass_integral=.010, scale=1.6, epsilon=.5, orientation=float(np.pi/8)),
    final_binding_lower=.009, final_binding_upper=1., cohort_taper=[.02, .04],
    grid=dict(energy=16, Lfraction=4, inclination=6, eccentric_anomaly=16,
              apsidal_angle=12, node=16),
    radial_phase_measure='Uniform eccentric anomaly with exact dtheta_r/deta = 1-e cos(eta)',
    timing_order=[16., 28., 32., 36.], readout_degree=2, readout_order=2,
    radius=1., annulus_log_width=.1, absolute_reference_cohort_mass=.952162896372471,
    known=dict(tau=3., times=[5.7, 6., 6.3], amplitudes=[.002, .001],
               omega0=[1., .8], Hessian=[[1., .15], [.15, .7]], covariance=[[.16, 0.], [0., .36]],
               first_vector=[1, 2], second_vectors=[[2, 4], [2, 3]],
               coarse=[32, 24], refine=[48, 32]),
    gates=dict(known_exact_peak_relative_error=1e-5, known_refinement_peak_relative_error=1e-5,
               known_pulse_product_peak_relative_error=.002,
               canonical_roundtrip_absolute=1e-8, impulse_work_absolute=1e-12,
               zero_relative_to_reference_peak=.1, initial_absolute_mass_relative_error=.001,
               mixed_absolute_mass_error=1e-6),
    limitations=['No angular/action quadrature convergence established by this pilot.',
                 'No memory erasure, changed separation, self-gravity or disk response.',
                 'Other degree-four/six output fields are not measured.'])


def json_ready(value, trail='$'):
    """Normalize numerical metadata explicitly; reject silent lossy encodings."""
    if isinstance(value, np.generic):
        return json_ready(value.item(), trail)
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist(), trail)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise TypeError(f'JSON object keys must be strings at {trail}.')
        return {key: json_ready(item, trail+'.'+key) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item, trail+f'[{index}]') for index, item in enumerate(value)]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f'Nonfinite JSON float at {trail}.')
        return value
    raise TypeError(f'Unsupported JSON type {type(value).__name__} at {trail}.')


def write(path, value):
    path.write_text(json.dumps(json_ready(value), indent=2, allow_nan=False)+'\n')


def verify_provenance(config, out):
    """Verify live inputs and their start snapshots immediately before COMPLETE."""
    checks = {}
    for name, expected in config['source_hashes'].items():
        checks['live_source:'+name] = digest(Path(__file__).parent/name) == expected
        checks['start_snapshot:'+name] = digest(out/name) == expected
    checks['live_protocol'] = digest(PROTOCOL) == config['protocol_sha256']
    checks['protocol_start_snapshot'] = digest(out/PROTOCOL.name) == config['protocol_sha256']
    checks['reference'] = digest(REFERENCE/'response.npz') == config['reference_raw_sha256']
    checks['loaded_AGAMA'] = digest(config['actual_agama_module']) == config['agama_binary_sha256']
    if not all(checks.values()):
        raise RuntimeError('Input provenance changed during run: '+json.dumps(checks))
    return dict(checks=checks, all_unchanged=True, checked_process_cpu_seconds=time.process_time())


def complete(out, config, result, message):
    result['terminal_provenance'] = verify_provenance(config, out)
    write(out/'result.json', result)
    # The last comparison follows the receipt write, on both execution paths.
    verify_provenance(config, out)
    (out/'COMPLETE').write_text(message+'\n')


def budget(known=False):
    deadline = FROZEN['known_limit_checkpoint_seconds'] if known else FROZEN['checkpoint_cpu_seconds']
    if time.process_time() >= deadline:
        raise BudgetExhausted(f'Checkpoint ceiling reached at {time.process_time():.6f} CPU seconds.')


def complex_json(values):
    values = np.asarray(values)
    return dict(real=values.real.tolist(), imag=values.imag.tolist())


def exact_gaussian_case(K, N, a, b, t, qmax=24):
    """Independent forward Jacobi-Anger series and Gaussian characteristic function.

    No inverse map or action quadrature is used here. Integer selection follows
    m + q N + p K = 0, for the observable exp(-i m.theta).
    """
    c = FROZEN['known']; D = np.array(c['Hessian']); S = np.array(c['covariance'])
    omega = np.array(c['omega0']); tau = c['tau']; m = N - K
    total = 0j
    for q in range(-qmax, qmax+1):
        numerator = -m-q*N
        if numerator[0] % K[0]:
            continue
        p = int(numerator[0] // K[0])
        if not np.array_equal(p*K+m+q*N, np.zeros(2, int)):
            continue
        d = t*m+q*tau*N
        zB = b*(t-tau)*(m @ D @ N)
        zA = a*(t*(m @ D @ K)+q*tau*(N @ D @ K))
        characteristic = np.exp(-1j*(d @ omega)-.5*(d @ D @ S @ D @ d))
        total += jv(q, zB)*jv(p, zA)*characteristic
    return total


def gaussian_leading(K, N, a, t):
    c = FROZEN['known']; D = np.array(c['Hessian']); S = np.array(c['covariance'])
    m = N-K; d = t*m-c['tau']*N
    return -(a*a/4)*(t-c['tau'])*(N @ D @ m)*(K @ D @ d)*np.exp(
        -1j*(np.array(c['omega0']) @ d)-.5*(d @ D @ S @ D @ d))


def gaussian_inverse(J, theta, K, N, a, b, t):
    c = FROZEN['known']; D = np.array(c['Hessian']); omega = np.array(c['omega0'])
    thetaB = theta-(omega+J @ D.T)*(t-c['tau'])
    JpreB = J-b*np.sin(thetaB @ N)[:, None]*N
    theta0 = thetaB-(omega+JpreB @ D.T)*c['tau']
    return JpreB-a*np.sin(theta0 @ K)[:, None]*K, theta0


def gaussian_forward(J, theta, K, N, a, b, t):
    c = FROZEN['known']; D = np.array(c['Hessian']); omega = np.array(c['omega0'])
    J1 = J+a*np.sin(theta @ K)[:, None]*K
    thetaB = theta+(omega+J1 @ D.T)*c['tau']
    J2 = J1+b*np.sin(thetaB @ N)[:, None]*N
    return J2, thetaB+(omega+J2 @ D.T)*(t-c['tau'])


def gaussian_quadrature(K, N, a, t, nj, nt):
    c = FROZEN['known']; sigma = np.sqrt(np.diag(c['covariance']))
    x, w = roots_hermitenorm(nj); w = w/np.sqrt(2*np.pi)
    theta_nodes = 2*np.pi*(np.arange(nt)+.5)/nt
    total_count = nj*nj*nt*nt
    case_values = np.zeros(4, complex); mass = np.zeros(4)
    mixed_value = 0j
    for lo in range(0, total_count, FROZEN['chunk_size']):
        budget(known=True)
        ix = np.unravel_index(np.arange(lo, min(lo+FROZEN['chunk_size'], total_count)), (nj, nj, nt, nt))
        J = np.column_stack((sigma[0]*x[ix[0]], sigma[1]*x[ix[1]]))
        theta = np.column_stack((theta_nodes[ix[2]], theta_nodes[ix[3]]))
        weights = w[ix[0]]*w[ix[1]]/(nt*nt)
        observable = np.exp(-1j*(theta @ (N-K)))
        exponent0 = np.sum(J*J/(sigma*sigma), axis=1)
        ratios = []
        for sa, sb in SHAPE_SIGNS:
            Ji, _ = gaussian_inverse(J, theta, K, N, sa*a, sb*a, t)
            ratios.append(np.exp(-.5*(np.sum(Ji*Ji/(sigma*sigma), axis=1)-exponent0)))
        ratios = np.asarray(ratios)
        mixed_ratio = np.sum(CONTRAST_SIGNS[:, None]*ratios, axis=0)
        mixed_value += np.sum(weights*mixed_ratio*observable)
        case_values += np.sum(ratios*(weights*observable)[None, :], axis=1)
        mass += np.sum(ratios*weights[None, :], axis=1)
    return mixed_value, case_values, mass


def known_limit(out):
    c = FROZEN['known']; K = np.array(c['first_vector']); rows = []
    J = np.array([[-.3, .4], [.2, -.1], [.6, .2], [-.2, -.5]])
    theta = np.array([[.2, .8], [1., 2.], [2.2, 3.1], [4.1, 5.3]])
    roundtrip = 0.; minimum_noncollinear_phase_variance = None
    for Nv in c['second_vectors']:
        N = np.array(Nv)
        for a in c['amplitudes']:
            Jf, tf = gaussian_forward(J, theta, K, N, a, -a, 6.3)
            Ji, ti = gaussian_inverse(Jf, tf, K, N, a, -a, 6.3)
            roundtrip = max(roundtrip, float(np.max(abs(Ji-J))), float(np.max(abs(ti-theta))))
        if K[0]*N[1]-K[1]*N[0] != 0:
            D = np.array(c['Hessian']); S = np.array(c['covariance']); C = D @ S @ D; m = N-K
            best_t = c['tau']*(m @ C @ N)/(m @ C @ m)
            d = best_t*m-c['tau']*N
            minimum_noncollinear_phase_variance = float(d @ C @ d)
            if not minimum_noncollinear_phase_variance > 0:
                raise RuntimeError('Noncollinear benchmark unexpectedly permits complete vector refocusing.')
        for a in c['amplitudes']:
            for t in c['times']:
                budget(known=True)
                start = time.process_time()
                exact_cases = np.array([exact_gaussian_case(K, N, sa*a, sb*a, t) for sa, sb in SHAPE_SIGNS])
                exact = CONTRAST_SIGNS @ exact_cases
                longer = CONTRAST_SIGNS @ np.array([exact_gaussian_case(K, N, sa*a, sb*a, t, 32) for sa, sb in SHAPE_SIGNS])
                if abs(exact-longer) > 1e-18:
                    raise RuntimeError('Jacobi-Anger series truncation check failed.')
                value, cases, mass = gaussian_quadrature(K, N, a, t, *c['coarse'])
                # Refine the smallest pulse, which is the stricter cancellation check.
                refined = None
                if a == min(c['amplitudes']):
                    refined, _, _ = gaussian_quadrature(K, N, a, t, *c['refine'])
                budget(known=True)
                rows.append(dict(second_vector=Nv, amplitude=a, time=t,
                                 exact=complex_json(exact), numerical=complex_json(value),
                                 refined=None if refined is None else complex_json(refined),
                                 leading=complex_json(gaussian_leading(K, N, a, t)),
                                 exact_error=float(abs(value-exact)),
                                 refined_error=None if refined is None else float(abs(refined-exact)),
                                 refinement_change=None if refined is None else float(abs(refined-value)),
                                 mass=mass.tolist(), case_values=complex_json(cases),
                                 stage_cpu_seconds=time.process_time()-start))
                write(out/'known-progress.json', dict(rows=rows, process_cpu_seconds=time.process_time()))
    gates = dict(roundtrip=roundtrip < 1e-12, noncollinear_residual=minimum_noncollinear_phase_variance > 0)
    for Nv in c['second_vectors']:
        for a in c['amplitudes']:
            subset = [r for r in rows if r['second_vector'] == Nv and r['amplitude'] == a]
            peak = max(np.hypot(r['exact']['real'], r['exact']['imag']) for r in subset)
            error = max(r['exact_error'] if r['refined_error'] is None else r['refined_error'] for r in subset)
            gates[f'exact_{Nv}_{a}'] = bool(error/peak < FROZEN['gates']['known_exact_peak_relative_error'])
            changes = [r['refinement_change'] for r in subset if r['refinement_change'] is not None]
            if changes:
                gates[f'refinement_{Nv}_{a}'] = bool(max(changes)/peak < FROZEN['gates']['known_refinement_peak_relative_error'])
            exact = np.array([complex(r['exact']['real'], r['exact']['imag']) for r in subset])
            leading = np.array([complex(r['leading']['real'], r['leading']['imag']) for r in subset])
            gates[f'weak_limit_{Nv}_{a}'] = bool(np.max(abs(exact-leading))/peak < FROZEN['gates']['known_pulse_product_peak_relative_error'])
    result = dict(rows=rows, gates=gates, all_pass=all(gates.values()),
                  canonical_forward_inverse_error=roundtrip,
                  minimum_noncollinear_phase_variance=minimum_noncollinear_phase_variance,
                  process_cpu_seconds=time.process_time(),
                  scope='Known constant-Hessian limit; collinear vectors reduce to one phase combination. No halo inference.')
    write(out/'known-result.json', result)
    return result


def pulse(which, amplitude, sign):
    c = FROZEN['pulse_'+which].copy()
    c['mass_integral'] *= amplitude; c['epsilon'] *= sign
    return IntegratedMultipolePulse(c['ell'], c['mass_integral'], c['scale'], c['epsilon'], c['orientation'])


def loss_bound(p):
    dv = p.gradient_bound()['total']
    return np.sqrt(2)*dv+.5*dv*dv


def cartesian_probe_checks(mapper, finder):
    E = np.array([.021, .04, .1, .3, .6, .9]); fraction = np.array([.1, .3, .6, .8, .5, .2])
    ci = np.array([-.8, -.4, .2, .6, .9, -.2]); L = fraction*(1-E)/np.sqrt(2*E)
    I = 1/np.sqrt(2*E); Jr = I-.5*(L+np.sqrt(L*L+2))
    actions = np.column_stack((Jr, L*(1-abs(ci)), L*ci))
    angles = np.column_stack(([.31, 1.2, 2.6, 3.7, 4.8, 5.9], [.22, 1.1, 2.2, 3.3, 4.4, 5.5], [.53, .7, 1.9, 2.9, 4.7, 5.1]))
    angles[:, 2] += np.sign(ci)*angles[:, 1]
    initial = mapper(np.column_stack((actions, angles)))
    rows = []
    for amplitude in FROZEN['amplitudes']:
        for sa, sb in SHAPE_SIGNS:
            budget(); A, B = pulse('A', amplitude, sa), pulse('B', amplitude, sb)
            xa = initial.copy(); dA = A.kick(xa[:, :3]); H0 = potential_energy(xa)
            wA = np.sum(xa[:, 3:]*dA, axis=1)+.5*np.sum(dA*dA, axis=1); xa[:, 3:] += dA
            Ja, aa, fa = finder(xa, angles=True, frequencies=True)
            xb = coordinates(mapper, Ja, aa, fa, FROZEN['tau']); HA = potential_energy(xb)
            dB = B.kick(xb[:, :3]); wB = np.sum(xb[:, 3:]*dB, axis=1)+.5*np.sum(dB*dB, axis=1); xb[:, 3:] += dB
            Jb, ab, fb = finder(xb, angles=True, frequencies=True)
            final = coordinates(mapper, Jb, ab, fb, 20.)
            Jf, af, ff = finder(final, angles=True, frequencies=True)
            backB = coordinates(mapper, Jf, af, ff, -20.); backB[:, 3:] -= B.kick(backB[:, :3])
            Ji, ai, fi = finder(backB, angles=True, frequencies=True)
            backA = coordinates(mapper, Ji, ai, fi, -FROZEN['tau']); backA[:, 3:] -= A.kick(backA[:, :3])
            min_binding = float(np.min(-potential_energy(final)))
            rows.append(dict(amplitude=amplitude, shape_signs=[sa, sb],
                             Cartesian_forward_inverse_error=float(np.max(abs(backA-initial))),
                             work_error_A=float(np.max(abs(potential_energy(xa)-H0-wA))),
                             work_error_B=float(np.max(abs(potential_energy(xb)-HA-wB))),
                             minimum_postB_binding=min_binding,
                             rigorous_minimum_binding=FROZEN['cohort_taper'][0]-loss_bound(A)-loss_bound(B)))
    return rows


def final_grid_chunk(lo, hi, mapper):
    c = FROZEN['grid']; sizes = tuple(c.values())
    ix = np.unravel_index(np.arange(lo, hi), sizes)
    x, we = roots_legendre(c['energy']); width = FROZEN['final_binding_upper']-FROZEN['final_binding_lower']
    energy = FROZEN['final_binding_lower']+.5*width*(x+1); we *= .5*width
    x, wl = roots_legendre(c['Lfraction']); lam = .5*(x+1); wl *= .5
    u, wu = roots_legendre(c['inclination'])
    E = energy[ix[0]]; Lmax = (1-E)/np.sqrt(2*E); L = Lmax*lam[ix[1]]; cosine = u[ix[2]]
    eta = 2*np.pi*(ix[3]+.5)/c['eccentric_anomaly']
    I, eccentricity = radial_parameters(E, L)
    jac = 1-eccentricity*np.cos(eta); Mr = eta-eccentricity*np.sin(eta)
    aps = 2*np.pi*(ix[4]+.5)/c['apsidal_angle']; node = 2*np.pi*(ix[5]+.5)/c['node']
    Jr = I-.5*(L+np.sqrt(L*L+2)); actions = np.column_stack((Jr, L*(1-abs(cosine)), L*cosine))
    angles = np.column_stack((Mr, aps, node+np.sign(cosine)*aps))
    omr = (2*E)**1.5; omL = .5*(1+L/np.sqrt(L*L+2))*omr
    frequencies = np.column_stack((omr, omL, np.sign(cosine)*omL))
    angular_count = c['eccentric_anomaly']*c['apsidal_angle']*c['node']
    weights = (2*np.pi)**3*we[ix[0]]*wl[ix[1]]*wu[ix[2]]*L*Lmax*(2*E)**-1.5*jac/angular_count
    now = mapper(np.column_stack((actions, angles)))
    r = np.linalg.norm(now[:, :3], axis=1)
    angular = np.conj((now[:, 0]+1j*now[:, 1])/r)**2
    O = np.column_stack([readout_radial(r, name)*angular for name in ('potential', 'radial_force', 'tangential_force')])
    return E, actions, angles, frequencies, now, weights, O


def finite_row(t, amplitude, mapper, finder, cohort, out):
    count = int(np.prod(list(FROZEN['grid'].values())))
    totals = np.zeros((4, 3), complex); masses = np.zeros(4); mixed = np.zeros(3, complex)
    initial_mass = 0.; mixed_mass = 0.; exclusions = np.zeros(2, int)
    minimum_preB = 1.; minimum_initial = 1.; largest_roundtrip = 0.
    start = time.process_time()
    for lo in range(0, count, FROZEN['chunk_size']):
        budget(); hi = min(lo+FROZEN['chunk_size'], count)
        E, actions, angles, freq, now, weights, O = final_grid_chunk(lo, hi, mapper)
        initial_mass += float(np.sum(weights*cohort(E)))
        backB = coordinates(mapper, actions, angles, freq, -(t-FROZEN['tau']))
        distributions = np.zeros((4, len(E)))
        for ib, sb in enumerate((1, -1)):
            B = pulse('B', amplitude, sb); beforeB = backB.copy(); beforeB[:, 3:] -= B.kick(beforeB[:, :3])
            binding = -potential_energy(beforeB); minimum_preB = min(minimum_preB, float(np.min(binding)))
            # This is a support proof, not removing particles after forcing:
            # a selected initial state cannot have post-A binding below this
            # floor under either shape sign. Excluded inverse histories have f=0.
            postA_floor = FROZEN['cohort_taper'][0]-loss_bound(pulse('A', amplitude, 1))
            supported = binding >= postA_floor-1e-12
            exclusions[ib] += int(np.count_nonzero(~supported))
            if not np.any(supported):
                continue
            if np.any(binding[supported] <= 0) or np.any(binding[supported] > 1+1e-12):
                raise RuntimeError('Inverse B violates proved bound-domain support.')
            J, a, f = finder(beforeB[supported], angles=True, frequencies=True)
            if not (np.isfinite(J).all() and np.isfinite(a).all() and np.isfinite(f).all()):
                raise RuntimeError('Nonfinite inverse-map output on admissible post-A support.')
            # Sparse internal roundtrip audit, separate from the initial probes.
            probe = np.linspace(0, len(J)-1, min(8, len(J)), dtype=int)
            reconstructed = mapper(np.column_stack((J[probe], a[probe])))
            largest_roundtrip = max(largest_roundtrip, float(np.max(abs(reconstructed-beforeB[supported][probe]))))
            beforeA = coordinates(mapper, J, a, f, -FROZEN['tau'])
            for ia, sa in enumerate((1, -1)):
                A = pulse('A', amplitude, sa); init = beforeA.copy(); init[:, 3:] -= A.kick(init[:, :3])
                Ei = -potential_energy(init); minimum_initial = min(minimum_initial, float(np.min(Ei)))
                distributions[2*ia+ib, supported] = cohort(Ei)
        delta = np.sum(CONTRAST_SIGNS[:, None]*distributions, axis=0)
        mixed += np.sum((weights*delta)[:, None]*O, axis=0)
        mixed_mass += float(np.sum(weights*delta))
        totals += np.einsum('cn,n,no->co', distributions, weights, O)
        masses += np.sum(distributions*weights[None, :], axis=1)
        if (lo//FROZEN['chunk_size']) % 4 == 0 or hi == count:
            write(out/'finite-chunk-progress.json', dict(time=t, amplitude=amplitude,
                  completed_grid_points=hi, total_grid_points=count, partial_quadrature=hi < count,
                  mixed_partial=complex_json(mixed), case_absolute_masses_partial=masses.tolist(),
                  unforced_grid_mass_partial=initial_mass, mixed_mass_partial=mixed_mass,
                  stage_cpu_seconds=time.process_time()-start, process_cpu_seconds=time.process_time(),
                  scope='Partial quadrature sums are not physical time-curve values.'))
    return dict(time=t, amplitude=amplitude, mixed=complex_json(mixed),
                case_values=complex_json(totals), case_absolute_masses=masses.tolist(),
                mixed_absolute_mass=mixed_mass, unforced_grid_mass=initial_mass,
                minimum_inverse_preB_binding=minimum_preB, minimum_inverse_initial_binding=minimum_initial,
                proven_zero_support_grid_count_per_B_sign=exclusions.tolist(),
                inverse_mapper_roundtrip_error=largest_roundtrip,
                direct_contrast_vs_case_sum_error=float(np.max(abs(mixed-CONTRAST_SIGNS @ totals))),
                stage_cpu_seconds=time.process_time()-start, process_cpu_seconds=time.process_time())


def main():
    global OWNED_OUTPUT
    p = argparse.ArgumentParser(); p.add_argument('--out', type=Path, required=True); p.add_argument('--known-only', action='store_true')
    p.add_argument('--expected-source-sha', required=True); p.add_argument('--expected-protocol-sha', required=True)
    args = p.parse_args()
    if digest(__file__) != args.expected_source_sha or digest(PROTOCOL) != args.expected_protocol_sha:
        raise RuntimeError('Coordinator-approved source/protocol hash mismatch before output creation.')
    args.out.mkdir(parents=True, exist_ok=False)
    OWNED_OUTPUT = args.out
    for name in SOURCES:
        (args.out/name).write_bytes((Path(__file__).parent/name).read_bytes())
    (args.out/PROTOCOL.name).write_bytes(PROTOCOL.read_bytes())
    config = dict(pid=os.getpid(), started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  source_sha256=digest(__file__), source_hashes={name:digest(Path(__file__).parent/name) for name in SOURCES},
                  actual_agama_module=agama.__file__, agama_binary_sha256=digest(agama.__file__),
                  protocol_sha256=digest(PROTOCOL), approved_source_sha256=args.expected_source_sha,
                  approved_protocol_sha256=args.expected_protocol_sha,
                  known_only=args.known_only, nice=os.getpriority(os.PRIO_PROCESS, 0),
                  reference_raw_sha256=digest(REFERENCE/'response.npz'), frozen=FROZEN,
                  seed=None, sampler='Deterministic phase-space quadrature; no IID uncertainty model')
    write(args.out/'config.json', config)
    if config['source_sha256'] != args.expected_source_sha or config['protocol_sha256'] != args.expected_protocol_sha:
        raise RuntimeError('Approved source/protocol changed during start snapshots.')
    verify_provenance(config, args.out)
    if config['nice'] < 10:
        raise RuntimeError('Launch requires nice priority at least 10.')
    if config['agama_binary_sha256'] != EXPECTED_AGAMA or config['reference_raw_sha256'] != EXPECTED_REFERENCE:
        raise RuntimeError('Frozen module/reference hash mismatch; review before launch.')
    known = known_limit(args.out)
    if not known['all_pass']:
        raise RuntimeError('Known-limit verification failed; physical pilot not advanced.')
    if args.known_only:
        complete(args.out, config, dict(config=config, known=known, finite_rows=[],
              process_cpu_seconds=time.process_time(), wall_seconds=time.monotonic()-LAUNCH_WALL,
              scope='Known-limit preflight only; no halo response.'),
              'Known-limit preflight ended; no physical inference.')
        return
    budget(); pot = agama.Potential(type='Isochrone', mass=1, scaleRadius=.5)
    mapper, finder, cohort = agama.ActionMapper(pot), agama.ActionFinder(pot), Cohort(pot)
    support = dict(global_binding_loss=loss_bound(pulse('A', 1, 1))+loss_bound(pulse('B', 1, 1)))
    support['guaranteed_postB_binding_floor'] = FROZEN['cohort_taper'][0]-support['global_binding_loss']
    if not 0 < FROZEN['final_binding_lower'] < support['guaranteed_postB_binding_floor']:
        raise RuntimeError('Fixed final-state grid does not contain all proved bound support.')
    probes = cartesian_probe_checks(mapper, finder)
    for r in probes:
        if r['Cartesian_forward_inverse_error'] > FROZEN['gates']['canonical_roundtrip_absolute']:
            raise RuntimeError('Physical Cartesian inverse map failed.')
        if max(r['work_error_A'], r['work_error_B']) > FROZEN['gates']['impulse_work_absolute']:
            raise RuntimeError('External-work accounting failed.')
        if r['minimum_postB_binding'] < r['rigorous_minimum_binding']-1e-12:
            raise RuntimeError('Forward support probe violates global impulse bound.')
    write(args.out/'physical-checks.json', dict(support=support, probes=probes))
    with np.load(REFERENCE/'response.npz') as raw:
        reference_t = raw['t'].copy()
        references = np.column_stack([raw[n+'_total'] for n in ('potential', 'radial_force', 'tangential_force')])
    peaks = np.max(abs(references[(reference_t >= 24)&(reference_t <= 40)]), axis=0)
    rows = []; zero_gates = {}
    for t in FROZEN['timing_order']:
        for amplitude in FROZEN['amplitudes']:
            budget(); row = finite_row(t, amplitude, mapper, finder, cohort, args.out)
            if t == FROZEN['tau']:
                row['exact_instantaneous_B_reference'] = complex_json(np.zeros(3, complex))
            else:
                row['leading_reference'] = complex_json(references[np.flatnonzero(reference_t == t)[0]]*amplitude**2)
            row['reference_peak_scaled'] = (peaks*amplitude**2).tolist()
            rows.append(row)
            write(args.out/'finite-progress.json', dict(rows=rows, process_cpu_seconds=time.process_time()))
            if t == FROZEN['tau']:
                magnitude = np.hypot(row['mixed']['real'], row['mixed']['imag'])
                zero_gates[str(amplitude)] = dict(
                    zero=bool(np.all(magnitude/(peaks*amplitude**2) <= FROZEN['gates']['zero_relative_to_reference_peak'])),
                    mass=bool(abs(row['unforced_grid_mass']/FROZEN['absolute_reference_cohort_mass']-1) <= FROZEN['gates']['initial_absolute_mass_relative_error']),
                    mixed_mass=bool(abs(row['mixed_absolute_mass']) <= FROZEN['gates']['mixed_absolute_mass_error']),
                    roundtrip=bool(row['inverse_mapper_roundtrip_error'] <= FROZEN['gates']['canonical_roundtrip_absolute']))
        if t == FROZEN['tau'] and not all(v for gates in zero_gates.values() for v in gates.values()):
            break
    result = dict(config=config, known=known, support=support, physical_probes=probes,
                  instantaneous_B_gates=zero_gates, finite_rows=rows,
                  process_cpu_seconds=time.process_time(), wall_seconds=time.monotonic()-LAUNCH_WALL,
                  physical_confirmation='Unresolved: this fixed grid has not received independent quadrature refinement.',
                  scope='Exact-kick method/support/cancellation and measured-cost pilot in l=2,m=2 only. No converged spatial echo, memory-erasure or collective result.')
    complete(args.out, config, result, 'Finite-map pilot ended; COMPLETE is not a scientific pass.')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        if OWNED_OUTPUT is not None:
            write(OWNED_OUTPUT/'FAILURE.json', dict(pid=os.getpid(), error=str(error), traceback=traceback.format_exc(),
                  cpu_seconds=time.process_time(), wall_seconds=time.monotonic()-LAUNCH_WALL,
                  budget_exhausted=isinstance(error, BudgetExhausted),
                  retained_partial_records=['known-progress.json', 'finite-progress.json', 'finite-chunk-progress.json', 'physical-checks.json']))
        raise
