"""Analytical and numerical checks of the actual qualification algorithm."""
from common import ROOT, NAMES, WINDOWS, density, load_table, sha
from diagnostic import assess, bounded_contraction, envelope
import argparse
import json
import time
from pathlib import Path
import numpy as np


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    start = time.process_time()
    meta, table = load_table(ROOT/'results/population-response/preflight-02')
    edges = np.linspace(-64, 64, 4097)
    mid = (edges[:-1]+edges[1:])/2
    q0 = np.exp(-mid*mid/8)*(1+.2*mid)
    q = np.broadcast_to(q0, (8, 2, len(mid))).copy()
    exact = assess(edges, q, q, meta, table)
    checks = {}
    checks['all_fixed_comparisons_present'] = len(exact['rows']) == 24
    checks['identical_kernel_has_zero_sampling_step_error'] = all(
        r['approximate']['sampling_half'] == 0 and r['approximate']['step_half'] == 0
        for r in exact['rows'])
    checks['triangle_inequality_on_every_profile'] = all(
        abs(r['paired_error_mean']) <= r['plugin_mismatch']+1e-14 for r in exact['rows'])
    checks['identical_population_zero_mismatch'] = all(
        r['approximation_allowance'] == 0 for r in exact['rows'] if r['population']=='halo')
    zero = assess(edges, q*0, q*0, meta, table)
    checks['zero_response_does_not_qualify_sign_or_percentage'] = all(
        r['sign_qualification']=='unqualified' and not r['five_percent_qualified'] for r in zero['rows'])
    rng = np.random.default_rng(96202)
    perturbed = q+rng.normal(size=(8, 2, 1))*.5*np.exp(-mid*mid/12)
    uncertain = assess(edges, perturbed, q, meta, table)
    checks['uncertainty_expands_mismatch'] = all(
        r['expanded_mismatch'] >= r['plugin_mismatch']-1e-14 for r in uncertain['rows'])
    weights = density(edges, meta, table, 'halo')
    r = bounded_contraction(perturbed[:,0], q[:,0], weights, 3.)
    direct = -(perturbed[:,0] @ np.diff(weights))
    checks['scalar_contraction_preserves_batch_covariance'] = np.allclose(r['batches'], direct, rtol=0, atol=1e-15)
    # Arbitrary positive rescaling changes absolute transfer, not sign/relative gates.
    scaled_meta = dict(meta, f_ref=meta['f_ref']/3)
    # Test directly at contraction level: family central normalization is immutable.
    scaled = bounded_contraction(perturbed[:,0], q[:,0], weights*3, 3.)
    checks['no_hidden_unit_mass_normalization'] = abs(scaled['mean']-3*r['mean']) < 1e-12
    try:
        assess(edges, q[:7], q[:7], meta, table)
    except ValueError:
        checks['incomplete_batches_rejected'] = True
    else:
        checks['incomplete_batches_rejected'] = False
    try:
        assess(np.linspace(-16, 16, 4097), q, q, meta, table)
    except ValueError:
        checks['nonzero_boundary_rejected'] = True
    else:
        checks['nonzero_boundary_rejected'] = False
    # Dense direct quadrature checks the finite-cell population approximation.
    fine_edges = np.linspace(-64, 64, 65537)
    fine_mid = (fine_edges[:-1]+fine_edges[1:])/2
    fine_q = np.exp(-fine_mid*fine_mid/8)*(1+.2*fine_mid)
    errors = []
    for name in NAMES:
        w = density(edges, meta, table, name)
        wf = density(fine_edges, meta, table, name)
        errors.append(abs(-q0@np.diff(w)+fine_q@np.diff(wf)))
    checks['smooth_kernel_mesh_contractions'] = max(errors) < 2e-6
    result = dict(checks={k:bool(v) for k,v in checks.items()}, all_pass=all(checks.values()),
        maximum_smooth_mesh_change=max(errors), cpu_seconds=time.process_time()-start,
        source_sha256={n:sha(Path(__file__).with_name(n)) for n in ['check_diagnostic.py','common.py','diagnostic.py']},
        scope='Analytical synthetic kernels and numerical assembly checks, not new forced physical evidence or empirical proof of Student-t simultaneous coverage.')
    a.out.mkdir(parents=True, exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    if not result['all_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
