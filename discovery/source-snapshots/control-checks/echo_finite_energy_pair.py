"""T16-only finite-map numerical diagnosis; no late or collective calculation.

Scientific quadrature functions are statically copied from the frozen failed
preflight, not imported (which would install its 100-second process limit).
"""
import os
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import argparse,ast,copy,datetime,json,math,resource,signal,sys,time,traceback
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(257,259))
LAUNCH_WALL=time.monotonic()
class BudgetExhausted(RuntimeError):pass
def cpu_signal(signum,frame):raise BudgetExhausted('257-second soft CPU limit; 259-second child hard limit.')
signal.signal(signal.SIGXCPU,cpu_signal)
import numpy as np
from scipy.special import roots_legendre
from echo_halo import agama,coordinates,digest,potential_energy
from echo_monopole import Cohort,radial_parameters
from echo_multipole_pulse import IntegratedMultipolePulse
from echo_two_frequency import readout_radial
ROOT=Path(__file__).resolve().parents[2]
ARCHIVE=ROOT/'results/discovery-20261001/echoes/finite-map-preflight-01/measurement'
PROTOCOL=ROOT/'research/discovery-20261001/ECHO_FINITE_ENERGY_PAIR_PROTOCOL.md'
REFERENCE=ROOT/'results/discovery-20261001/echoes/two-frequency-ne512-L24-01/response.npz'
EXPECTED_ARCHIVE_CONFIG='25f1a061c4de3fff4581e0b42ef6667877ac1cc3410ec2b4e899923693008925'
EXPECTED_ARCHIVE_RESULT='9ec150abe878f86d15c7685953a5e2bcb640d933c0f747bf03f534062c505e05'
EXPECTED_ARCHIVE_SOURCE='d222c0ba4321678ce96a328714b8ef95c969f77fed6f3d6db862b97afeffd6b3'
EXPECTED_ARCHIVE_PROTOCOL='2139dcc9a5254d3ff48678a5db876949aa790160647b5e44d4dca261b2e8a67f'
EXPECTED_REFERENCE='2d26635a86096770e0187a812a1c99728fd13591f85e8531703df42ca99c777c'
PRIOR_DIAGNOSTIC=ROOT/'results/discovery-20261001/echoes/finite-map-diagnostic-completion02/measurement/result.json'
EXPECTED_PRIOR_DIAGNOSTIC='4b377941b087c71151ea732379b05e2aa2fd9659a1bdc618086a0b37eb9823e9'
BASE_CONFIG=json.loads((ARCHIVE/'config.json').read_text())
BASE_FROZEN=copy.deepcopy(BASE_CONFIG['frozen'])
FROZEN=copy.deepcopy(BASE_FROZEN)
ENERGY_SEGMENTS=None
OWNED_OUTPUT=None
SHAPE_SIGNS=((1,1),(1,-1),(-1,1),(-1,-1))
CONTRAST_SIGNS=np.array([1.,-1.,-1.,1.])/4
HELPERS=('echo_halo.py','echo_monopole.py','echo_multipole_pulse.py','echo_two_frequency.py')
UNCHANGED_FUNCTIONS=('json_ready','write','complex_json','pulse','loss_bound','cartesian_probe_checks','finite_row')
CHECKPOINT_CPU=255.
MATRIX_SAFETY_FACTOR=1.2
PLAN=[
 dict(label='energy_split352',energy=352,Lfraction=4,inclination=6,eccentric_anomaly=16,apsidal_angle=12,node=16,segments=[[.009,.02,32],[.02,.04,64],[.04,1.,256]],direction='Double only each final-energy partition count versus saved split176'),
 dict(label='energy_split704',energy=704,Lfraction=4,inclination=6,eccentric_anomaly=16,apsidal_angle=12,node=16,segments=[[.009,.02,64],[.02,.04,128],[.04,1.,512]],direction='Double only each final-energy partition count versus split352; four times saved split176')]

def budget(known=False):
    if time.process_time()>=CHECKPOINT_CPU:raise BudgetExhausted('255-second checkpoint reached.')

def energy_nodes():
    if ENERGY_SEGMENTS is None:
        x,w=roots_legendre(FROZEN['grid']['energy'])
        width=BASE_FROZEN['final_binding_upper']-BASE_FROZEN['final_binding_lower']
        return BASE_FROZEN['final_binding_lower']+.5*width*(x+1),w*.5*width
    E=[];W=[]
    for low,high,count in ENERGY_SEGMENTS:
        x,w=roots_legendre(count);E.append(low+.5*(high-low)*(x+1));W.append(.5*(high-low)*w)
    return np.concatenate(E),np.concatenate(W)

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

def complex_json(values):
    values = np.asarray(values)
    return dict(real=values.real.tolist(), imag=values.imag.tolist())

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
    energy, we = energy_nodes()
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


def select_grid(plan):
    global ENERGY_SEGMENTS
    FROZEN['grid'] = {key:plan[key] for key in BASE_FROZEN['grid']}
    ENERGY_SEGMENTS = plan['segments']


def scalar_mass_ladder(cohort):
    """Exactly integrate L/orientation analytically, isolating E/taper error."""
    global ENERGY_SEGMENTS
    rows = []
    for count in (16,32,64,128,256,512,1024,2048):
        budget(); FROZEN['grid']['energy'] = count; ENERGY_SEGMENTS = None
        E,w = energy_nodes(); Lmax = (1-E)/np.sqrt(2*E)
        mass = float((2*np.pi)**3*np.sum(w*cohort(E)*Lmax**2*(2*E)**-1.5))
        rows.append(dict(label='uniform'+str(count),energy_nodes=count,absolute_mass=mass,
                         difference_from_reference=mass-BASE_FROZEN['absolute_reference_cohort_mass']))
    for plan in PLAN:
        select_grid(plan); E,w = energy_nodes(); Lmax = (1-E)/np.sqrt(2*E)
        mass = float((2*np.pi)**3*np.sum(w*cohort(E)*Lmax**2*(2*E)**-1.5))
        rows.append(dict(label=plan['label'],energy_nodes=len(E),partitions=plan['segments'],
                         absolute_mass=mass,difference_from_reference=mass-BASE_FROZEN['absolute_reference_cohort_mass']))
    select_grid(PLAN[0])
    return rows


def scientific_function_audit():
    original=(ARCHIVE/'echo_finite_preflight.py').read_text()
    old = {n.name:n for n in ast.parse(original).body if isinstance(n,ast.FunctionDef)}
    new = {n.name:n for n in ast.parse(Path(__file__).read_text()).body if isinstance(n,ast.FunctionDef)}
    checks = {name:ast.dump(old[name],include_attributes=False)==ast.dump(new[name],include_attributes=False)
              for name in UNCHANGED_FUNCTIONS}
    grid=ast.get_source_segment(original,old['final_grid_chunk'])
    old_energy="x, we = roots_legendre(c['energy']); width = FROZEN['final_binding_upper']-FROZEN['final_binding_lower']\n    energy = FROZEN['final_binding_lower']+.5*width*(x+1); we *= .5*width"
    if old_energy not in grid:raise RuntimeError('Original energy-node expression changed.')
    expected_grid=ast.parse(grid.replace(old_energy,'energy, we = energy_nodes()')).body[0]
    checks['grid_changes_only_energy_node_provider']=ast.dump(expected_grid,include_attributes=False)==ast.dump(new['final_grid_chunk'],include_attributes=False)
    if not all(checks.values()):raise RuntimeError('Frozen scientific function changed: '+json.dumps(checks))
    return checks


def provenance(config,out):
    checks = dict(source=digest(__file__)==config['source_sha256'],
                  source_snapshot=digest(out/Path(__file__).name)==config['source_sha256'],
                  protocol=digest(PROTOCOL)==config['protocol_sha256'],
                  protocol_snapshot=digest(out/PROTOCOL.name)==config['protocol_sha256'],
                  archived_config=digest(ARCHIVE/'config.json')==EXPECTED_ARCHIVE_CONFIG,
                  archived_result=digest(ARCHIVE/'result.json')==EXPECTED_ARCHIVE_RESULT,
                  archived_source=digest(ARCHIVE/'echo_finite_preflight.py')==EXPECTED_ARCHIVE_SOURCE,
                  archived_protocol=digest(ARCHIVE/'ECHO_FINITE_PREFLIGHT_PROTOCOL.md')==EXPECTED_ARCHIVE_PROTOCOL,
                  prior_diagnostic=digest(PRIOR_DIAGNOSTIC)==EXPECTED_PRIOR_DIAGNOSTIC,
                  prior_diagnostic_snapshot=digest(out/'frozen_diagnostic_completion02.json')==EXPECTED_PRIOR_DIAGNOSTIC,
                  archived_config_snapshot=digest(out/'frozen_config.json')==EXPECTED_ARCHIVE_CONFIG,
                  archived_result_snapshot=digest(out/'frozen_failure_result.json')==EXPECTED_ARCHIVE_RESULT,
                  archived_source_snapshot=digest(out/'frozen_preflight.py')==EXPECTED_ARCHIVE_SOURCE,
                  archived_protocol_snapshot=digest(out/'frozen_preflight_protocol.md')==EXPECTED_ARCHIVE_PROTOCOL,
                  reference=digest(REFERENCE)==EXPECTED_REFERENCE,
                  AGAMA=digest(agama.__file__)==BASE_CONFIG['agama_binary_sha256'])
    for name in HELPERS:
        expected = BASE_CONFIG['source_hashes'][name]
        checks[name] = digest(Path(__file__).parent/name)==expected
        checks['snapshot:'+name] = digest(out/name)==expected
    if not all(checks.values()):raise RuntimeError('Input provenance changed: '+json.dumps(checks))
    return checks


def annotate_row(row,plan,peaks,scalar_mass):
    row['label']=plan['label'];row['refinement_direction']=plan['direction']
    row['grid']=FROZEN['grid'].copy();row['energy_partitions']=ENERGY_SEGMENTS
    magnitude=np.hypot(row['mixed']['real'],row['mixed']['imag'])
    row['zero_error_over_frozen_reference_peak']=(magnitude/peaks).tolist()
    row['unforced_6D_minus_analytic_angle_mass']=row['unforced_grid_mass']-scalar_mass
    row['gates']=dict(
        zero=bool(np.all(magnitude/peaks<=BASE_FROZEN['gates']['zero_relative_to_reference_peak'])),
        mass=bool(abs(row['unforced_grid_mass']/BASE_FROZEN['absolute_reference_cohort_mass']-1)<=BASE_FROZEN['gates']['initial_absolute_mass_relative_error']),
        mixed_mass=bool(abs(row['mixed_absolute_mass'])<=BASE_FROZEN['gates']['mixed_absolute_mass_error']),
        roundtrip=bool(row['inverse_mapper_roundtrip_error']<=BASE_FROZEN['gates']['canonical_roundtrip_absolute']))
    return row


def finish(out,config,rows,mass_ladder,cost,status):
    checks=provenance(config,out)
    result=dict(config=config,function_audit=scientific_function_audit(),terminal_provenance=checks,
                mass_ladder=mass_ladder,rows=rows,projected_cost_review=cost,status=status,
                process_cpu_seconds=time.process_time(),wall_seconds=time.monotonic()-LAUNCH_WALL,
                scope='T16 exact-zero quadrature diagnosis only. All directions retained; no late field or collective calculation.')
    write(out/'result.json',result);provenance(config,out)
    (out/'COMPLETE').write_text('Numerical diagnostic ended; COMPLETE is not an echo confirmation.\n')


def main():
    global OWNED_OUTPUT
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--expected-source-sha',required=True);p.add_argument('--expected-protocol-sha',required=True)
    a=p.parse_args()
    if digest(__file__)!=a.expected_source_sha or digest(PROTOCOL)!=a.expected_protocol_sha:
        raise RuntimeError('Approved source/protocol changed before output creation.')
    if digest(ARCHIVE/'config.json')!=EXPECTED_ARCHIVE_CONFIG or digest(ARCHIVE/'result.json')!=EXPECTED_ARCHIVE_RESULT or digest(ARCHIVE/'echo_finite_preflight.py')!=EXPECTED_ARCHIVE_SOURCE:
        raise RuntimeError('Frozen failed experiment changed.')
    if digest(ARCHIVE/'ECHO_FINITE_PREFLIGHT_PROTOCOL.md')!=EXPECTED_ARCHIVE_PROTOCOL or digest(PRIOR_DIAGNOSTIC)!=EXPECTED_PRIOR_DIAGNOSTIC:
        raise RuntimeError('Frozen protocol or reference diagnosis changed.')
    if os.getpriority(os.PRIO_PROCESS,0)<10:raise RuntimeError('Requires nice priority at least10.')
    a.out.mkdir(parents=True,exist_ok=False);OWNED_OUTPUT=a.out
    for source in [Path(__file__),PROTOCOL]+[Path(__file__).parent/name for name in HELPERS]:
        (a.out/source.name).write_bytes(source.read_bytes())
    for old_name,new_name in [('echo_finite_preflight.py','frozen_preflight.py'),('result.json','frozen_failure_result.json'),('config.json','frozen_config.json'),('ECHO_FINITE_PREFLIGHT_PROTOCOL.md','frozen_preflight_protocol.md')]:
        (a.out/new_name).write_bytes((ARCHIVE/old_name).read_bytes())
    (a.out/'frozen_diagnostic_completion02.json').write_bytes(PRIOR_DIAGNOSTIC.read_bytes())
    prior=json.loads(PRIOR_DIAGNOSTIC.read_text())
    profile=next(r for r in prior['rows'] if r['label']=='energy_split176')
    config=dict(pid=os.getpid(),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                source_sha256=digest(__file__),protocol_sha256=digest(PROTOCOL),
                original_source_sha256=EXPECTED_ARCHIVE_SOURCE,original_result_sha256=EXPECTED_ARCHIVE_RESULT,
                original_config_sha256=EXPECTED_ARCHIVE_CONFIG,original_protocol_sha256=EXPECTED_ARCHIVE_PROTOCOL,
                reference_sha256=EXPECTED_REFERENCE,prior_diagnostic_sha256=EXPECTED_PRIOR_DIAGNOSTIC,
                helper_hashes={n:BASE_CONFIG['source_hashes'][n] for n in HELPERS},
                actual_AGAMA=agama.__file__,AGAMA_sha256=digest(agama.__file__),
                physical_parameters=BASE_FROZEN,diagnostic_time=16.,fixed_amplitude=1.,
                plans=PLAN,seed=None,nice=os.getpriority(os.PRIO_PROCESS,0),
                child_hard_CPU_seconds=259,checkpoint_CPU_seconds=CHECKPOINT_CPU,
                projected_cost_safety_factor=MATRIX_SAFETY_FACTOR,
                profile_scope='Frozen preceding segmented176 row; no outcome-dependent profile selection.',
                inherited_known_control='Passed in immutable finite-map-preflight-01; preserved mathematical functions AST-matched, not a new known-limit measurement.')
    write(a.out/'config.json',config);provenance(config,a.out);scientific_function_audit()
    pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5)
    mapper,finder,cohort=agama.ActionMapper(pot),agama.ActionFinder(pot),Cohort(pot)
    masses=scalar_mass_ladder(cohort);write(a.out/'mass-ladder.json',masses)
    probes=cartesian_probe_checks(mapper,finder)
    for r in probes:
        if r['Cartesian_forward_inverse_error']>BASE_FROZEN['gates']['canonical_roundtrip_absolute'] or max(r['work_error_A'],r['work_error_B'])>BASE_FROZEN['gates']['impulse_work_absolute']:
            raise RuntimeError('Unchanged physical mapping/work control failed.')
        if r['minimum_postB_binding']<r['rigorous_minimum_binding']-1e-12:
            raise RuntimeError('Original physical support-bound probe failed.')
    write(a.out/'physical-probes.json',probes)
    original=next(r for r in json.loads((ARCHIVE/'result.json').read_text())['finite_rows'] if r['amplitude']==1.)
    peaks=np.array(original['reference_peak_scaled'])
    profile_count=int(np.prod(list(profile['grid'].values())))
    total_count=sum(int(np.prod([p[k] for k in BASE_FROZEN['grid']])) for p in PLAN)
    projected=profile['stage_cpu_seconds']*total_count/profile_count*MATRIX_SAFETY_FACTOR
    cost=dict(profile_CPU_seconds=profile['stage_cpu_seconds'],profile_points=profile_count,
              profile_label='Saved completion02 energy_split176',total_pair_points=total_count,
              projected_pair_CPU_seconds=projected,remaining_checkpoint_CPU_seconds=CHECKPOINT_CPU-time.process_time(),
              safety_factor=MATRIX_SAFETY_FACTOR)
    cost['advance_pair']=projected<=cost['remaining_checkpoint_CPU_seconds']
    write(a.out/'cost-review.json',cost)
    if not cost['advance_pair']:
        finish(a.out,config,[],masses,cost,'Projected pair cost exceeds frozen allocation; pair not launched.')
        return
    rows=[]
    for plan in PLAN:
        budget();select_grid(plan)
        E,w=energy_nodes();Lmax=(1-E)/np.sqrt(2*E)
        analytic_mass=float((2*np.pi)**3*np.sum(w*cohort(E)*Lmax**2*(2*E)**-1.5))
        row=annotate_row(finite_row(16.,1.,mapper,finder,cohort,a.out),plan,peaks,analytic_mass)
        z=lambda r:np.array(r['mixed']['real'])+1j*np.array(r['mixed']['imag'])
        row['change_from_saved_split176']=complex_json(z(row)-z(profile))
        row['change_from_saved_split176_over_reference_peak']=(abs(z(row)-z(profile))/peaks).tolist()
        if rows:
            row['change_from_split352']=complex_json(z(row)-z(rows[0]))
            row['change_from_split352_over_reference_peak']=(abs(z(row)-z(rows[0]))/peaks).tolist()
        rows.append(row);write(a.out/'progress.json',dict(rows=rows,process_cpu_seconds=time.process_time()))
    finish(a.out,config,rows,masses,cost,'Both fixed energy-only zero-field rows evaluated; no late calculation.')


if __name__=='__main__':
    try:main()
    except Exception as error:
        if OWNED_OUTPUT is not None:
            write(OWNED_OUTPUT/'FAILURE.json',dict(pid=os.getpid(),error=str(error),traceback=traceback.format_exc(),
                  cpu_seconds=time.process_time(),wall_seconds=time.monotonic()-LAUNCH_WALL,
                  budget_exhausted=isinstance(error,BudgetExhausted),partial_data='Completed progress rows and explicitly partial finite-chunk sums retained.'))
        raise
