"""Unforced analytic iso-halo twins: exact streaming and positive populations.

No orbit history or forced-response array is read by this preflight.
"""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json
import math
import sys
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import beta, roots_jacobi
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'build/noise-sweep/Agama-stable-v2'))
import agama

B = .5
P_VALUES = (4, 6, 8)
A0 = 16 * B / (5 * np.sqrt(2) * np.pi**3)
F0_LEADING_TIMES_ROOT_TWO = 16 * B / (5 * np.pi**3)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def coefficients(count=96):
    values = [Fraction(1)]
    for n in range(count-1):
        values.append(values[-1] * Fraction((n+2)*(n+5)**2,
            (n+1)*(n+4)*(2*n+7)))
    return values


SERIES_EXACT = coefficients()
SERIES = np.array([float(x) for x in SERIES_EXACT])


def series_shape(e):
    return np.polynomial.polynomial.polyval(e, SERIES)


def f0(e):
    return A0 * np.asarray(e)**2.5 * series_shape(e)


def rho(psi):
    return B * (2-B*psi)*psi**4 / (4*np.pi*(1-B*psi)**3)


def rho_second(psi):
    x = B*psi
    h = (2-x)/(1-x)**3
    hp = (5-2*x)/(1-x)**4
    hpp = (18-6*x)/(1-x)**5
    return B/(4*np.pi) * (12*psi**2*h + 8*B*psi**3*hp + B*B*psi**4*hpp)


def eddington(e, order):
    nodes, weights = leggauss(order)
    u, weights = (nodes+1)/2, weights/2
    return 2*np.sqrt(e)/(np.sqrt(8)*np.pi**2) * (rho_second(e*(1-u*u)) @ weights)


def density_from_df(psi, order):
    nodes, weights = roots_jacobi(order, .5, 2.5)
    t = (nodes+1)/2
    return 4*np.pi*np.sqrt(2)*A0*psi**4 * (series_shape(psi*t) @ (weights/16))


def second_from_df(psi):
    nodes, weights = roots_jacobi(64, 1.5, 2.5)
    t = (nodes+1)/2
    return 8*np.sqrt(2)*np.pi/3 * A0 * psi**5 * (series_shape(psi*t) @ (weights/32))


def split1d(values):
    levels = [list(values)]
    while len(levels[-1]) > 1:
        last = levels[-1]
        levels.append([(last[i]+last[i+1])/2 for i in range(len(last)-1)])
    return [v[0] for v in levels], [v[-1] for v in reversed(levels)]


def split2d(values, axis):
    if axis == 0:
        cols = [split1d([row[j] for row in values]) for j in range(len(values[0]))]
        return tuple([[cols[j][side][i] for j in range(len(cols))]
            for i in range(len(values))] for side in (0, 1))
    rows = [split1d(row) for row in values]
    return tuple([row[side] for row in rows] for side in (0, 1))


def positivity_bound(p, depth=4):
    # The normalized numerator is H=e^(p-4)(1-e)t[-A+Bp e+.5(1-e)^2 t^2].
    # Denominator is the first 13 positive terms S_12 of f0/(a0 e^2.5).
    ap = Fraction(16*p, (2*p+5)*(2*p+7))
    bp = Fraction(8, 2*p+7)  # 8*b/(p+7/2), b=1/2
    power = {(p-4, 1): -ap, (p-3, 1): ap+bp, (p-2, 1): -bp,
        (p-4, 3): Fraction(1, 2), (p-3, 3): Fraction(-3, 2),
        (p-2, 3): Fraction(3, 2), (p-1, 3): Fraction(-1, 2)}
    num, den = [], []
    for i in range(13):
        num.append([sum((value * Fraction(math.comb(i, k), math.comb(12, k)) *
            Fraction(math.comb(j, ell), math.comb(3, ell)) for (k, ell), value in power.items()
            if k <= i and ell <= j), Fraction(0)) for j in range(4)])
        di = sum((SERIES_EXACT[k] * Fraction(math.comb(i, k), math.comb(12, k))
            for k in range(i+1)), Fraction(0))
        den.append([di]*4)
    boxes = [(num, den)]
    for _ in range(depth):
        refined = []
        for numerator, denominator in boxes:
            en = split2d(numerator, 0)
            ed = split2d(denominator, 0)
            for ns, ds in zip(en, ed):
                refined.extend(zip(split2d(ns, 1), split2d(ds, 1)))
        boxes = refined
    assert all(value > 0 for _, ds in boxes for row in ds for value in row)
    upper = max(abs(ns[i][j])/ds[i][j] for ns, ds in boxes
        for i in range(13) for j in range(4))
    maximum_ratio_bound = float(upper)/F0_LEADING_TIMES_ROOT_TWO
    alpha = .5/maximum_ratio_bound
    return dict(p=p, polynomial_ratio_upper_numerator=upper.numerator,
        polynomial_ratio_upper_denominator=upper.denominator,
        polynomial_ratio_upper_float=float(upper),
        maximum_deltaF_over_F0_bound=maximum_ratio_bound, alpha=alpha,
        alpha_exact_expression='4 / (5 pi^3 B_p), where B_p is the recorded exact rational bound',
        multiplier_bound=.5, positivity_minimum_Fplus_over_F0=.5,
        positivity_minimum_Fminus_over_F0=.5, denominator_series_terms=13,
        dyadic_subdivision_depth=depth, boxes=len(boxes),
        arithmetic='Exact Fraction coefficients and de Casteljau subdivisions; the reported alpha is a floating evaluation of the exact expression')


def ratio_at(e, p):
    ap = 4*p/((p+2.5)*(p+3.5))
    bp = 8*B/(p+3.5)
    t_values = [1.]
    if ap > bp*e and e < 1:
        t = np.sqrt(2*(ap-bp*e)/3)/(1-e)
        if t < 1:
            t_values.append(float(t))
    def value(t):
        h = e**(p-4)*(1-e)*t*(-ap+bp*e+.5*(1-e)**2*t*t)
        return abs(h)/(F0_LEADING_TIMES_ROOT_TWO*series_shape(e))
    values = [value(t) for t in t_values]
    i = int(np.argmax(values))
    return float(values[i]), t_values[i]


def numerical_maximum(p):
    grid = np.linspace(0, 1, 2001)
    values = np.array([ratio_at(e, p)[0] for e in grid])
    index = int(np.argmax(values))
    fit = minimize_scalar(lambda e: -ratio_at(e, p)[0],
        bounds=(grid[max(index-2, 0)], grid[min(index+2, len(grid)-1)]),
        method='bounded', options={'xatol': 1e-14})
    candidates = [(grid[index], values[index]), (float(fit.x), float(-fit.fun))]
    e, value = max(candidates, key=lambda pair: pair[1])
    _, t = ratio_at(e, p)
    return dict(maximum=value, binding_energy=e, L_over_Lmax=t,
        endpoint_is_escape_limit=bool(e == 0), scope='Numerical diagnostic; not the positivity certificate')


def local_moment(r, mu, order, population):
    psi = 1/(B+np.sqrt(B*B+r*r))
    nodes, weights = leggauss(order)
    speed = (nodes+1)*np.sqrt(2*psi)/2
    speed_weight = weights*np.sqrt(2*psi)/2*speed**2
    phi = np.arange(2*order)*np.pi/order
    v, cosine, azimuth = np.meshgrid(speed, nodes, phi, indexing='ij')
    vr = v*cosine
    vt = v*np.sqrt(1-cosine*cosine)*np.cos(azimuth)
    vp = v*np.sqrt(1-cosine*cosine)*np.sin(azimuth)
    velocity = np.column_stack((vr.ravel(), vt.ravel(), vp.ravel()))
    measure = (speed_weight[:, None, None]*weights[None, :, None]*
        np.full((1, 1, 2*order), np.pi/order)).ravel()
    e = psi-.5*v.ravel()**2
    L2 = r*r*(vt.ravel()**2+vp.ravel()**2)
    Lz = r*np.sqrt(1-mu*mu)*vp.ravel()
    p = population['p']
    g0 = -4*p/((p+2.5)*(p+3.5))*e**(p-1) + 8*B/(p+3.5)*e**p
    delta = population['alpha'] * Lz * (g0+L2*e**p)
    w = measure*delta
    density = rho(psi)
    second = second_from_df(psi)
    sigma = np.sqrt(second/density)
    first = np.sum(w[:, None]*velocity, axis=0)
    delta_second = np.einsum('i,ij,ik->jk', w, velocity, velocity)
    return dict(p=p, radius=r, mu=mu, velocity_order=order,
        density_difference_over_reference=float(2*w.sum()/density),
        first_difference_over_reference_RMS=(2*first/(density*sigma)).tolist(),
        second_tensor_difference_over_reference_diagonal=(2*delta_second/second).tolist(),
        third_azimuthal_difference_over_reference_sigma_cubed=float(2*(w @ (vp.ravel()**3))/(density*sigma**3)),
        velocity_nodes=len(w))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--protocol', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    started_cpu = time.process_time()
    started_wall = time.monotonic()
    source_bytes = Path(__file__).read_bytes()
    (args.out/'source.py').write_bytes(source_bytes)
    (args.out/'protocol.md').write_bytes(args.protocol.read_bytes())
    populations = [positivity_bound(p) for p in P_VALUES]
    energies = np.unique(np.r_[np.geomspace(1e-8, .5, 64), np.linspace(.51, 1-1e-8, 64)])
    edd_rows = []
    for e in energies:
        exact = float(f0(e))
        low, high = eddington(e, 64), eddington(e, 128)
        edd_rows.append(dict(binding_energy=float(e), series_df=exact,
            inversion_64=float(low), inversion_128=float(high),
            relative_inversion_difference=float(high/exact-1),
            relative_order_difference=float(high/low-1)))
    densities = []
    for psi in np.unique(np.r_[np.geomspace(1e-6, .5, 32), np.linspace(.51, 1, 32)]):
        low, high = density_from_df(psi, 32), density_from_df(psi, 64)
        densities.append(dict(relative_potential=float(psi), analytic_density=float(rho(psi)),
            recovered_32=float(low), recovered_64=float(high),
            relative_recovery_difference=float(high/rho(psi)-1),
            relative_order_difference=float(high/low-1)))
    pot = agama.Potential(type='Isochrone', mass=1, scaleRadius=B)
    df = agama.DistributionFunction(type='QuasiSpherical', potential=pot)
    agama_rows = []
    with agama.setNumThreads(1):
        for e in energies:
            I = 1/np.sqrt(2*e)
            Lmax = (1-e)/np.sqrt(2*e)
            L = Lmax*np.array([.15, .55, .9])
            Lz = L*np.array([.2, .5, .8])
            actions = np.column_stack((np.maximum(I-.5*(L+np.sqrt(L*L+2)), 0), L-Lz, Lz))
            measured = df(actions)
            agama_rows.append(dict(binding_energy=float(e), exact_df=float(f0(e)),
                relative_AGAMA_errors=(measured/f0(e)-1).tolist(),
                angular_momentum_fractions=[.15, .55, .9]))
    moment_rows = []
    for order in (12, 24):
        for r in (.01, .1, .3, 1., 3., 10., 30., 100.):
            for mu in (0., .5, .9, .999):
                for pop in populations:
                    moment_rows.append(local_moment(r, mu, order, pop))
    for pop in populations:
        pop['numerical_maximum_diagnostic'] = numerical_maximum(pop['p'])
        assert pop['numerical_maximum_diagnostic']['maximum'] <= pop['maximum_deltaF_over_F0_bound']*(1+1e-12)
        pop['maximum_diagnostic_normalized_multiplier'] = pop['alpha']*pop['numerical_maximum_diagnostic']['maximum']
    n = len(SERIES_EXACT)-1
    next_coef = SERIES_EXACT[-1] * Fraction((n+2)*(n+5)**2, (n+1)*(n+4)*(2*n+7))
    tail_bound = float(next_coef)/(1-.75)
    tails = dict(series_terms=len(SERIES), normalized_shape_tail_bound_for_all_e_at_most_1=tail_bound,
        coefficient_ratio_tail_bound=.75, coefficient_ratio_bound_starts_at_n=6,
        ratio_inequality_polynomial='2 n^3 + 3 n^2 - 51 n - 116 >= 0 for n>=6',
        leading_coefficient=A0, leading_coefficient_formula='16 b / (5 sqrt(2) pi^3)')
    summaries = dict(maximum_relative_eddington_error=max(abs(r['relative_inversion_difference']) for r in edd_rows),
        maximum_relative_eddington_order_change=max(abs(r['relative_order_difference']) for r in edd_rows),
        maximum_relative_density_recovery_error=max(abs(r['relative_recovery_difference']) for r in densities),
        maximum_relative_density_order_change=max(abs(r['relative_order_difference']) for r in densities),
        maximum_absolute_AGAMA_relative_error=max(abs(v) for r in agama_rows for v in r['relative_AGAMA_errors']),
        maximum_local_density_difference=max(abs(r['density_difference_over_reference']) for r in moment_rows),
        maximum_local_first_moment_difference=max(abs(v) for r in moment_rows for v in r['first_difference_over_reference_RMS']),
        maximum_local_second_tensor_difference=max(abs(v) for r in moment_rows for row in r['second_tensor_difference_over_reference_diagonal'] for v in row))
    assert summaries['maximum_relative_eddington_error'] < 1e-11
    assert summaries['maximum_relative_density_recovery_error'] < 1e-11
    assert summaries['maximum_local_first_moment_difference'] < 1e-11
    result = dict(schema_version=1, scope='Unforced analytic halo-population preflight; no orbit integration or bar response read',
        model=dict(G=1, mass=1, isochrone_scale=B, binding_energy_domain=[0, 1]),
        populations=populations, series=tails, summaries=summaries,
        eddington_rows=edd_rows, density_rows=densities, agama_comparison_rows=agama_rows,
        local_moment_rows=moment_rows,
        formal_identities=dict(C0='8 sqrt(2) pi / 3', C1='64 sqrt(2) pi / 15', C1_over_C0='8/5',
            local_streaming='Zero for every radius and inclination by two independent Beta-integral cancellations',
            density_and_even_moments='Identical by odd parity under complete velocity reversal',
            positive_populations='Fplus and Fminus are at least F0/2 by the exact rational Bernstein lower-denominator bound'),
        gates=dict(analytic_moment_identity_verified=True, all_domain_positivity_constructed=True,
            numerical_moment_checks_pass=True, forced_prediction=False, live_stability=False,
            observational_validation=False),
        source_sha256=hashlib.sha256(source_bytes).hexdigest(), protocol_sha256=sha(args.protocol),
        agama_sha256=sha(agama.__file__), cpu_seconds=time.process_time()-started_cpu,
        wall_seconds=time.monotonic()-started_wall,
        limitations=['The DF is stationary and self-consistent only for the unsoftened spherical reference potential',
            'Local first and even moments agree, but higher odd moments can differ',
            'This preflight does not establish collective stability or representability under a live disk/softened force',
            'AGAMA approximates the exact analytic DF; subsequent importance weighting must identify its sampling density',
            'No novelty or bar-evolution claim from a constructed equilibrium family'])
    (args.out/'frozen-populations.json').write_text(json.dumps(dict(populations=populations,
        formal_g0='-4p e^(p-1)/[(p+2.5)(p+3.5)] + 8b e^p/(p+3.5)',
        binding_energy_convention='e=-E, G=M=1, b=0.5', source_sha256=result['source_sha256'],
        protocol_sha256=result['protocol_sha256'], no_forced_response_used=True), indent=2, allow_nan=False)+'\n')
    (args.out/'result.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    (args.out/'COMPLETE').write_text('Unforced exact-moment and positivity preflight complete.\n')
    print(json.dumps(dict(populations=populations, summaries=summaries, cpu_seconds=result['cpu_seconds']), indent=2))


if __name__ == '__main__':
    main()
