"""Test frozen 3D forecasts, with paired precision and numerical uncertainty apart."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[2]


def estimate(values):
    n = len(values)
    mean = float(np.mean(values))
    se = float(np.std(values, ddof=1)/np.sqrt(n))
    half = float(t.ppf(.975, n-1)*se)
    return dict(n=n, mean=mean, se=se, ci95=[mean-half, mean+half], half_width=half)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--forecast', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--case', choices=['A','B'])
    args = parser.parse_args()
    forecast = json.loads(args.forecast.read_text())
    sources = {}

    def read(case):
        folder = args.root/case
        d = json.loads((folder/'result.json').read_text())
        digest = hashlib.sha256((folder/'recorded.npz').read_bytes()).hexdigest()
        assert digest == d['raw_sha256']
        assert d['forecast_sha256'] == hashlib.sha256(args.forecast.read_bytes()).hexdigest()
        sources[str(folder)] = dict(result_sha256=hashlib.sha256((folder/'result.json').read_bytes()).hexdigest(), raw_sha256=digest)
        with np.load(folder/'recorded.npz') as raw:
            arrays = {key:raw[key] for key in ['particle_ids','initial_actions_angles','final_bar_Lz','final_reduced_bar_Lz','final_noise_Js']}
        return d, arrays

    def pair(label, suffix):
        dn, n = read(label+'-'+suffix+'noisy')
        ds, s = read(label+'-'+suffix+'smooth')
        assert np.array_equal(n['initial_actions_angles'], s['initial_actions_angles'])
        assert np.array_equal(n['particle_ids'], s['particle_ids'])
        x = n['final_bar_Lz']-s['final_bar_Lz']
        y = n['final_reduced_bar_Lz']-s['final_reduced_bar_Lz']
        return x, y, n, dn['all_pass'] and ds['all_pass']

    cases = []
    for c in forecast['cases']:
        if args.case and c['label'] != args.case:
            continue
        label = c['label']
        x, y, initial, local = pair(label, '')
        residual = x-y
        raw, reduced, discrepancy = estimate(x), estimate(y), estimate(residual)
        refinements = []
        for suffix in ['step-', 'cadence-']:
            xx, yy, start, passed = pair(label, suffix)
            n = len(xx)
            assert np.array_equal(start['particle_ids'], initial['particle_ids'][:n])
            assert np.array_equal(start['initial_actions_angles'], initial['initial_actions_angles'][:n])
            brownian_difference = float(np.max(abs(start['final_noise_Js']-initial['final_noise_Js'][:n])))
            assert brownian_difference < 1e-12
            refinements.append(dict(setting=suffix.rstrip('-'), discrepancy_shift=estimate((xx-yy)-residual[:n]),
                                    raw_3D_shift=estimate(xx-x[:n]), brownian_endpoint_difference=brownian_difference, local_pass=passed))
            local &= passed
        unforced = {}
        for suffix in ['unforced-noisy', 'unforced-smooth']:
            d, arrays = read(label+'-'+suffix)
            assert np.array_equal(arrays['initial_actions_angles'], initial['initial_actions_angles'])
            unforced[suffix] = dict(gates=d['gates'], final=d['history'][-1], maximum_work_residual=d['maximum_work_residual'])
            local &= d['all_pass']
        band = c['adequacy_half_width']
        shifts = [r['discrepancy_shift'] for r in refinements]
        numeric = c['numerical_envelope_Lz'] + sum(abs(r['mean']) for r in shifts)
        conservative_numeric = c['numerical_envelope_Lz'] + sum(max(abs(v) for v in r['ci95']) for r in shifts)
        point_numerics = all(abs(r['mean']) < .1*band for r in shifts)
        precise_numerics = all(max(abs(v) for v in r['ci95']) < .1*band for r in shifts)
        interval = [discrepancy['ci95'][0]-conservative_numeric, discrepancy['ci95'][1]+conservative_numeric]
        if not local or not point_numerics or not precise_numerics:
            decision = 'Numerical qualification unresolved or failed; inspect separate gates and intervals.'
        elif interval[0] >= -band and interval[1] <= band:
            decision = 'Qualified within the frozen operational approximation band.'
        elif interval[1] < -band or interval[0] > band:
            decision = 'Resolved failure of the frozen constant-coefficient prediction.'
        else:
            decision = 'Unresolved model adequacy: enlarged interval overlaps a band boundary.'
        cases.append(dict(label=label, forecast_Lz=c['physical_Lz_contrast'], adequacy_half_width=band,
                          raw_3D=raw, paired_reduced=reduced, discrepancy=discrepancy,
                          covariance_xy=float(np.cov(x,y,ddof=1)[0,1]), correlation_xy=float(np.corrcoef(x,y)[0,1]),
                          variance_reduced_3D_estimate=c['physical_Lz_contrast']+discrepancy['mean'],
                          variance_reduced_scope='Forecast plus mean(X-Y), with fixed coefficient1. Not the raw3D sample mean.',
                          refinements=refinements, unforced=unforced, local_pass=local,
                          numerical_point_changes_pass=point_numerics, numerical_sampling_intervals_pass=precise_numerics,
                          point_numerical_envelope=numeric, conservative_numerical_envelope=conservative_numeric,
                          enlarged_discrepancy_interval=interval,
                          extension_trigger=discrepancy['half_width']>.1*abs(c['physical_Lz_contrast']), decision=decision))
    args.out.mkdir(parents=True, exist_ok=False)
    result = dict(cases=cases, source_sha256=sources,
                  forecast_sha256=hashlib.sha256(args.forecast.read_bytes()).hexdigest(),
                  interval_scope='Pointwise Student-t iid particle intervals. Numerical refinement intervals are reported separately and conservatively added; not a simultaneous confidence guarantee.',
                  inference='Conditional prescribed-bar response under imposed canonical white action noise. No physical SIDM or live-halo claim.')
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(cases, indent=2))


if __name__ == '__main__':
    main()
