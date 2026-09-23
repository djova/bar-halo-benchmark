"""Reassess archived precision and estimator variance without changing outcomes."""
from common import ROOT, sha
import argparse
import json
import time
from pathlib import Path
import numpy as np
from analyze_validation import interval


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    start = time.process_time()
    base = ROOT/'results/population-response'
    used = {}
    def read(path):
        used[str(path.relative_to(ROOT))] = sha(path)
        return json.loads(path.read_text())
    old = read(base/'heldout-analysis-01/result.json')
    predictions = read(base/'heldout-predictions-01/result.json')
    forecasts = {(r['s'], r['tau'], r['population']): r for r in predictions['rows']}
    forecast_rows = []
    for r in old['rows']:
        pred = forecasts[r['s'], r['tau'], r['population']]
        independent = sum(abs(v) for v in r['comparison_changes'].values())
        kernel_step = max(abs(v) for v in pred['fine_minus_coarse']['ci95'])
        kernel_mesh = 2*pred['maximum_kernel_coarsening_change']
        kernel_window = max(abs(v) for v in pred['wider_minus_narrower']['ci95'])
        numerical = independent+kernel_step+kernel_mesh+kernel_window
        lo, hi = r['independent_minus_predicted']['ci95']
        allowance = r['frozen_accuracy_allowance']
        forecast_rows.append(dict(s=r['s'], tau=r['tau'], population=r['population'],
            original_operational_pass=r['prospective_prediction_qualified'],
            original_allowance=allowance, original_discrepancy_interval=[lo, hi],
            independent_sum_absolute_changes=independent,
            paired_kernel_step_allowance=kernel_step, doubled_kernel_mesh_change=kernel_mesh,
            paired_kernel_window_allowance=kernel_window,
            summed_numerical_proxy=numerical, expanded_interval=[lo-numerical, hi+numerical],
            joint_proxy_qualification=bool(lo-numerical >= -allowance and hi+numerical <= allowance),
            numerical_proxy_is_rigorous_bound=False))
    deterministic = read(base/'deterministic-analysis-02/result.json')['rows']
    pop_rows, efficiency = [], []
    rng = np.random.default_rng(96201)
    bootstrap = rng.integers(0, 8, (20000, 8))
    for s, prefix in [(0., '0'), (.25, '.25')]:
        records = []
        for seed in range(94501, 94509):
            folder = base/'validation-01'/f's{prefix}-seed{seed}'
            r = read(folder/'result.json')
            if sha(folder/'recorded.npz') != r['raw_sha256']:
                raise ValueError('Changed historical arrays')
            with np.load(folder/'recorded.npz') as z:
                records.append((r, z['mean'].copy(), z['covariance'].copy()))
        columns = records[0][0]['columns']
        if any(r['columns'] != columns for r, _, _ in records):
            raise ValueError('Historical column mismatch')
        means = np.stack([v[1] for v in records])
        cov = np.stack([v[2] for v in records])
        def idx(tau, pop, method='remainder', level='fine', branch='antithetic'):
            return columns.index(dict(tau=tau, population=pop, method=method, level=level, branch=branch))
        for tau in (10., 20.):
            for cut in (40, 64):
                halo = means[:, idx(tau, f'halo-{cut}')]
                diff = means[:, idx(tau, f'exponential-{cut}')]-halo
                step = diff-(means[:, idx(tau, f'exponential-{cut}', level='coarse')]-means[:, idx(tau, f'halo-{cut}', level='coarse')])
                wide_diff = means[:, idx(tau, 'exponential-64')]-means[:, idx(tau, 'halo-64')]
                narrow_diff = means[:, idx(tau, 'exponential-40')]-means[:, idx(tau, 'halo-40')]
                h = next(r for r in deterministic if r['s']==s and r['tau']==tau and r['population']=='halo-40')
                e = next(r for r in deterministic if r['s']==s and r['tau']==tau and r['population']=='exponential-40')
                paired_changes = {k:e['comparison_changes'][k]-h['comparison_changes'][k]
                                  for k in h['comparison_changes']}
                proxy = sum(abs(v) for v in paired_changes.values())
                ds = interval(diff)
                step_allowance = max(abs(v) for v in interval(step)['ci95'])
                total_difference_upper = max(abs(v) for v in ds['ci95'])+proxy+step_allowance
                halo_sampling_lower = min(abs(v) for v in interval(halo)['ci95'])
                # This intentionally does not certify accuracy: the reference denominator
                # still has its own numerical uncertainty, and refinements are not bounds.
                pop_rows.append(dict(s=s, tau=tau, cutoff=cut, paired_difference=ds,
                    paired_timestep=interval(step), paired_window=interval(wide_diff-narrow_diff),
                    relative_point_difference=ds['mean']/float(halo.mean()),
                    independent_narrow_paired_changes=paired_changes,
                    independent_narrow_difference=e['integral_w_K_B']-h['integral_w_K_B'],
                    conservative_difference_proxy=total_difference_upper,
                    proxy_over_sampling_lower_halo=total_difference_upper/halo_sampling_lower,
                    certified_sub_one_tenth_percent=False))
                for name in ('gaussian', 'halo', 'exponential'):
                    pop = f'{name}-{cut}'
                    raw, rem = (idx(tau, pop, method=m) for m in ('raw', 'remainder'))
                    rv, cv = cov[:, raw, raw], cov[:, rem, rem]
                    ratios = rv[bootstrap].mean(axis=1)/cv[bootstrap].mean(axis=1)
                    efficiency.append(dict(s=s, tau=tau, population=pop,
                        conditional_raw_variance_per_batch=float(rv.mean()),
                        conditional_remainder_variance_per_batch=float(cv.mean()),
                        conditional_variance_ratio=float(rv.mean()/cv.mean()),
                        paired_batch_bootstrap_ratio_interval=np.quantile(ratios, [.025, .975]).tolist(),
                        between_batch_variance_ratio=float(means[:,raw].var(ddof=1)/means[:,rem].var(ddof=1)),
                        paired_raw_minus_remainder=interval(means[:,raw]-means[:,rem]),
                        eight_batch_total_recorded_cpu_seconds=sum(r['cpu_seconds'] for r,_,_ in records),
                        independent_paths_per_batch=records[0][0]['independent_initial_paths'],
                        actual_method_specific_cpu_measured=False))
    result = dict(historical_forecast_assessment=forecast_rows, exponential_halo=pop_rows,
        estimator_variance=efficiency, inputs=used, source_sha256=sha(__file__),
        cpu_seconds=time.process_time()-start,
        scope='Retrospective assessment, not a new physical sample. Numerical differences are operational proxies, not certified bounds. Historical operational outcomes are unchanged. Variance ratios compare identical allocation and paired paths, and are not CPU speedups. Bootstrap resamples whole independent batches and preserves estimator covariance; eight batches do not establish rare-event tail behavior.')
    a.out.mkdir(parents=True, exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(dict(historical_operational_passes=sum(r['original_operational_pass'] for r in forecast_rows),
        joint_proxy_qualifications=sum(r['joint_proxy_qualification'] for r in forecast_rows),
        conditional_variance_ratio_range=[min(r['conditional_variance_ratio'] for r in efficiency), max(r['conditional_variance_ratio'] for r in efficiency)],
        cpu_seconds=result['cpu_seconds']), indent=2))


if __name__ == '__main__':
    main()
