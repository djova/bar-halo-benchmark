"""Regenerate unforced calibration and verify its connection to the frozen inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verify(actual, reference, forecast):
    assert actual['gates'] == reference['gates'] and actual['all_pass']
    assert [c['label'] for c in actual['cases']] == ['A', 'B']
    checks = []
    reordered_harmonics = []

    def compare(x, y, label):
        if isinstance(y, dict):
            assert set(x) == set(y), label
            for k in y:
                compare(x[k], y[k], label+'.'+k)
        elif isinstance(y, list):
            assert len(x) == len(y), label
            if label.endswith('.harmonics'):
                # Equal-amplitude harmonics can exchange sort rank after a
                # compiler rebuild. The wavevector, not the rank, is identity.
                xkeys = [tuple(row['k']) for row in x]
                ykeys = [tuple(row['k']) for row in y]
                assert len(set(xkeys)) == len(xkeys) and len(set(ykeys)) == len(ykeys)
                assert set(xkeys) == set(ykeys), label
                if xkeys != ykeys:
                    reordered_harmonics.append(label)
                x = sorted(x, key=lambda row: tuple(row['k']))
                y = sorted(y, key=lambda row: tuple(row['k']))
            for i, (a, b) in enumerate(zip(x, y)):
                compare(a, b, label+f'[{i}]')
        elif isinstance(y, (float, int)):
            assert math.isfinite(x) and math.isfinite(y), label
            error = abs(math.atan2(math.sin(x-y), math.cos(x-y))) if label.endswith('.phase') else abs(x-y)
            allowance = 1e-12 if label.endswith('.phase') else max(1e-13, 1e-10*abs(y))
            checks.append(dict(quantity=label, absolute_difference=error, allowance=allowance,
                               passes=error <= allowance))
        else:
            assert x == y, label

    compare(actual['cases'], reference['cases'], 'cases')
    links = []
    for c in actual['cases']:
        f = next(x for x in forecast['cases'] if x['label'] == c['label'])
        u, tu, ell, sigma = c['action_unit'], c['time_unit'], c['dimensionless_slope'], c['sigma']
        derived = dict(jr=c['actions'][0], jz=c['actions'][1], js0=c['actions'][2]/2,
                       width=sigma*u, mean=c['actions'][2]/2+ell*sigma*sigma*u,
                       amplitude=c['amplitude'], speed=c['physical_sweep_speed'],
                       D=c['physical_diffusion'], end=c['T']*tu, time_unit=tu, action_unit=u)
        begin = len(checks)
        compare(derived, f['orbit_config'], c['label']+'.frozen_orbit_config')
        links.append(dict(case=c['label'], frozen_input_agreement=all(r['passes'] for r in checks[begin:]),
                          forecast_prerequisite_qualified=f['qualified']))
    return dict(all_checks_pass=all(r['passes'] for r in checks), numerical_comparisons=len(checks),
                failed_comparisons=[r for r in checks if not r['passes']],
                maximum_fraction_of_allowance=max(r['absolute_difference']/r['allowance'] for r in checks),
                links=links, comparisons=checks, reordered_harmonic_lists=reordered_harmonics,
                scope='Unforced potential and Fourier quadratures only. Reproducing case A calibration '
                      'does not repair its failed response prerequisite or authorize its 3D run.')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--agama', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    manifest = json.loads((ROOT/'calibration/manifest.json').read_text())
    for name, digest in manifest.items():
        assert sha(ROOT/name) == digest, name
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    command = [sys.executable, str(ROOT/'scripts/noise_sweep/prepare_transfer.py'),
               '--agama-path', str(a.agama.resolve()), '--out', str(out/'unforced')]
    with (out/'run.log').open('x') as log:
        subprocess.run(['nice', '-n', '10', *command], cwd=ROOT, env=env,
                       stdout=log, stderr=subprocess.STDOUT, timeout=300, check=True)
    actual = json.loads((out/'unforced/result.json').read_text())
    reference = json.loads((ROOT/'calibration/reference.json').read_text())
    forecast = json.loads((ROOT/'forecast.json').read_text())
    frozen_reference_hash = forecast['source_sha256']['results/noise-sweep/transfer-preflight-01/unforced-coefficients/result.json']
    assert sha(ROOT/'calibration/reference.json') == frozen_reference_hash
    result = verify(actual, reference, forecast)
    result.update(source_manifest=manifest, helper_sha256=sha(Path(__file__)),
                  generated_result_sha256=sha(out/'unforced/result.json'),
                  agama_library_sha256=actual['agama_library_sha256'],
                  scientific_cpu_seconds=actual['cpu_seconds'])
    (out/'verification.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    marker = 'COMPLETE' if result['all_checks_pass'] else 'COMPARISON_FAILED'
    (out/marker).write_text('Unforced calibration readback finished; inspect every comparison.\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'comparisons'}, indent=2))
    if not result['all_checks_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
