"""Audit all existing map backgrounds against their exact bar-free moments."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')

import argparse
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.stats import chi2, norm

SWEEPS = (0., .1, .4, 1.2)
NOISE = (0., .01, .1, 1.)
PATH_CONDITIONS = ((0., .1), (.4, .1), (1.2, 1.))
LEGACY_SOLVER_SHA256 = 'bc1359a145b4ecaeb8dcf026a7c62bfdbbbb28ccbff4b3de6c8524117b6d6db5'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--solver-source', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists(), 'Preserve existing reviews'
    cpu = time.process_time()
    # This recorded version hardcodes sigma=8; it predates the --sigma option.
    assert sha(args.solver_source) == LEGACY_SOLVER_SHA256, 'Wrong archived solver'
    source_hashes = {}
    for name in ['map-01', 'positive-01']:
        directory = args.root/name
        assert (directory/'TERMINAL').exists(), 'Matrix has not terminated'
        ledger = json.loads((directory/'ledger.json').read_text())
        assert all(row['state'] == 'complete' for row in ledger.values())

    def read(name, s, eta, method):
        directory = args.root/name
        assert (directory/'COMPLETE').exists(), 'Missing completed control: '+name
        data = json.loads((directory/'result.json').read_text())
        config = data['config']
        assert config['no_bar'] and config['method'] == method
        assert config['s'] == s and config['eta'] == eta
        assert data['source_sha256'] == LEGACY_SOLVER_SHA256
        assert 'sigma' not in config and config['slope'] == -.016531804196572842
        assert config['dt'] == .025
        end = data['history'][-1]['tau']
        expected_end = min(8*math.pi, 8/s) if s else 8*math.pi
        assert math.isclose(end, expected_end, rel_tol=0., abs_tol=1e-12)
        assert data['all_pass'] == all(data['gates'].values())
        digest = sha(directory/'recorded.npz')
        assert digest == data['raw_sha256'], 'Changed raw arrays: '+name
        source_hashes[name] = dict(result_sha256=sha(directory/'result.json'),
                                  raw_sha256=digest, solver_sha256=data['source_sha256'])
        return directory, data, end, 2*eta/math.pi

    distributions = []
    for s in SWEEPS:
        for eta in NOISE:
            name = f'map-01/unforced-s{s:g}-eta{eta:g}'
            if (s, eta) == (.4, .1):
                name = 'map-pilot-01/unforced'
            variants = [(name, 'original')]
            if eta == 1:
                variants.append((f'positive-01/unforced-domain-s{s:g}', 'double_domain'))
            for name, variant in variants:
                _, data, end, delta = read(name, s, eta, 'distribution')
                config = data['config']
                expected_J = 64. if variant == 'original' else 128.
                assert config['J'] == expected_J and config['nj'] == int(expected_J*32)
                final = data['history'][-1]
                variance_expected = 8.**2 + 2*delta*end
                mean_error = final['physical_mean_change']
                variance_error = final['variance'] - variance_expected
                assert (abs(mean_error) < 1e-7) == data['gates']['unforced_mean']
                assert (abs(variance_error) < 1e-7) == data['gates']['unforced_variance']
                assert all(row['bar_impulse'] == 0. for row in data['history'])
                distributions.append(dict(source=name, variant=variant, s=s, eta=eta,
                    T=end, J=expected_J, expected_variance=variance_expected,
                    measured_variance=final['variance'], mean_error=mean_error,
                    variance_error=variance_error, original_gates=data['gates'],
                    original_all_pass=data['all_pass'], bar_impulse_zero=True,
                    maximum_saved_negative_mass=data['maximum_negative_mass'],
                    maximum_saved_moment_residual=data['maximum_budget_residual'],
                    scope='Recorded full-grid summary moments; decimated density is not '
                          'used to reconstruct the full-grid moments. Raw checksum verified.'))

    batches = []
    groups = []
    for s, eta in PATH_CONDITIONS:
        endpoints = []
        for seed in range(8201, 8209):
            name = f'map-01/paths-unforced-{seed}-s{s:g}-eta{eta:g}'
            directory, data, end, delta = read(name, s, eta, 'trajectories')
            assert data['config']['seed'] == seed and data['config']['n'] == 32768
            with np.load(directory/'recorded.npz') as raw:
                initial, final, bar, noise = [raw[key].copy() for key in
                    ['initial_j', 'final_j', 'final_impulse', 'final_stochastic']]
            assert all(x.shape == (32768,) and np.isfinite(x).all()
                       for x in [initial, final, bar, noise])
            assert np.count_nonzero(bar) == 0
            residual = final+s*end-initial-bar-noise
            final_budget = float(np.max(abs(residual)))
            assert final_budget < 1e-9, 'Original endpoint budget target failed'
            row = data['history'][-1]
            assert float(bar.mean()) == row['bar_impulse']
            assert float(noise.mean()) == row['stochastic_impulse']
            assert float(final.var()) == row['variance']
            assert float(np.mean(final+s*end-initial)) == row['physical_mean_change']
            expected = 2*delta*end
            batches.append(dict(source=name, seed=seed, s=s, eta=eta, T=end,
                n=len(noise), expected_noise_variance=expected, noise_mean=float(noise.mean()),
                noise_variance=float(noise.var(ddof=1)),
                mean_standardized=float(noise.mean()/math.sqrt(expected/len(noise))),
                final_budget_max=final_budget, bar_impulse_zero=True,
                original_gates=data['gates'], original_all_pass=data['all_pass']))
            endpoints.append(noise)
        # Eight independent seeds at one condition; NEVER pool different conditions.
        values = np.concatenate(endpoints)
        n = len(values)
        mean = float(values.mean())
        variance = float(values.var(ddof=1))
        mean_half = float(norm.ppf(.975)*math.sqrt(expected/n))
        variance_ci = ((n-1)*variance/chi2.ppf([.975, .025], n-1)).tolist()
        groups.append(dict(s=s, eta=eta, T=end, seeds=list(range(8201, 8209)), n=n,
            expected_mean=0., expected_noise_variance=expected, noise_mean=mean,
            mean_ci95_known_variance=[mean-mean_half, mean+mean_half],
            mean_standardized=mean/math.sqrt(expected/n), noise_variance=variance,
            variance_ci95=variance_ci, variance_ratio=variance/expected,
            scope='Pointwise descriptive intervals at this condition. Conditions share '
                  'seeds and are not treated as independent. No new qualification gate.'))

    result = dict(distribution_controls=distributions, stochastic_batches=batches,
        stochastic_groups=groups, source_sha256=source_hashes,
        coverage=dict(original_distributions=16, domain_replacements=4,
                      stochastic_batches=24, groups=3),
        readback_checks_pass=True,
        retained_original_failures=[r['source'] for r in distributions
                                    if r['variant']=='original' and not r['original_all_pass']],
        replacement_failures=[r['source'] for r in distributions
                              if r['variant']=='double_domain' and not r['original_all_pass']],
        review_source_sha256=sha(Path(__file__)), cpu_seconds=time.process_time()-cpu,
        population_width_provenance=dict(sigma=8., solver_sha256=LEGACY_SOLVER_SHA256,
            scope='Width is hardcoded in this exact archived solver, not supplied '
                  'from current defaults. Slope is explicit in every case config.'),
        scope='Retrospective readback of completed bar-free map controls. Analytic '
              'moments and exact recorded budgets do not qualify a forced contrast, '
              'the 3D forecast, a gravitational noise model or a physical SIDM law.')
    args.out.mkdir(parents=True)
    (args.out/'result.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({key:result[key] for key in ['coverage', 'readback_checks_pass',
                      'retained_original_failures', 'replacement_failures', 'cpu_seconds']}))


if __name__ == '__main__':
    main()
