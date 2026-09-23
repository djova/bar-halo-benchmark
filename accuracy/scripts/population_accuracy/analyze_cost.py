"""Separate measured component times, paired variances, and precision projections."""
from common import ROOT, sha
from analyze_refinement import read_matrix
from analyze_validation import interval
import argparse
import json
import time
from pathlib import Path
import numpy as np


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--matrix',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a = p.parse_args()
    start = time.process_time()
    records = read_matrix(a.matrix)
    if len(records)!=16 or any(not r['all_pass'] for r in records.values()):
        raise ValueError('Complete finite cost benchmark required')
    rows = []
    rng = np.random.default_rng(96203)
    resample = rng.integers(0,8,size=(20000,8))
    for s in (0.,.25):
        cases = sorted([(k,r) for k,r in records.items() if r['config']['s']==s],key=lambda x:x[1]['config']['seed'])
        if [r['config']['seed'] for _,r in cases] != list(range(96211,96219)):
            raise ValueError('Missing or replaced independent batch')
        cols = cases[0][1]['columns']
        arrays = []
        for key,r in cases:
            with np.load(a.matrix/key/'recorded.npz') as z:
                arrays.append((z['mean'].copy(),z['covariance'].copy()))
        means = np.stack([r[0] for r in arrays])
        cov = np.stack([r[1] for r in arrays])
        for tau in (10.,20.):
            for name in ('halo','exponential','gaussian8','stress1','stress0.125','stress0.015625'):
                def idx(method,level='fine'):
                    return cols.index(dict(tau=tau,level=level,population=name,method=method))
                ir,ic = idx('raw'),idx('remainder')
                vr,vc = cov[:,ir,ir],cov[:,ic,ic]
                cr,cc = [],[]
                for _,r in cases:
                    for method,target in [('raw',cr),('remainder',cc)]:
                        timing = next(v for v in r['timings'] if v['method']==method and v['population']==name)
                        target.append(timing['accounted_single_population_cpu_seconds'])
                cr,cc = np.array(cr),np.array(cc)
                # One kernel evolution records both endpoints. Costs are for the
                # full T20 workflow even when the target is its T10 measurement.
                ratio = (vr*cr).mean()/(vc*cc).mean()
                boot = (vr*cr)[resample].mean(axis=1)/(vc*cc)[resample].mean(axis=1)
                between_raw = means[:,ir].var(ddof=1)
                between_rem = means[:,ic].var(ddof=1)
                precision = []
                for method,values,cost,variance in [('raw',means[:,ir],cr,vr),('remainder',means[:,ic],cc,vc)]:
                    target_se = 1e-4
                    continuous = float(np.mean(cost*variance)/target_se**2)
                    batches = max(1,int(np.ceil(variance.mean()/target_se**2)))
                    precision.append(dict(method=method,measured_mean_accounted_batch_cpu_seconds=float(cost.mean()),
                        measured_batch_cpu_seconds=cost.tolist(),conditional_variance_per_batch=float(variance.mean()),
                        target_standard_error=target_se,continuous_cpu_seconds_projection=continuous,
                        integer_batch_cpu_seconds_projection=float(batches*cost.mean()),projected_batches=batches,
                        measured_eight_batch_response=interval(values),
                        between_batch_variance=float(values.var(ddof=1))))
                paired = interval(means[:,ir]-means[:,ic])
                rows.append(dict(s=s,tau=tau,population=name,paired_raw_minus_remainder=paired,
                    paired_interval_contains_zero=paired['ci95'][0]<=0<=paired['ci95'][1],
                    conditional_variance_ratio=float(vr.mean()/vc.mean()),
                    cost_times_variance_ratio=float(ratio),
                    paired_batch_bootstrap_cost_ratio_interval=np.quantile(boot,[.025,.975]).tolist(),
                    between_batch_cost_ratio=float(between_raw*cr.mean()/(between_rem*cc.mean())),
                    measured_accounted_batch_cost_ratio=float(cc.mean()/cr.mean()),
                    remainder_fine_minus_coarse=interval(means[:,ic]-means[:,idx('remainder','coarse')]),
                    precision=precision))
    result = dict(rows=rows,independent_batches_per_sweep=8,
        actual_total_job_cpu_seconds=sum(r['cpu_seconds'] for r in records.values()),
        worker_cpu_seconds=json.loads((a.matrix/'ledger.json').read_text())['completed_cpu_seconds'],
        maximum_path_budget=max(r['maximum_path_budget'] for r in records.values()),
        inputs={str(p):sha(p) for p in [a.matrix/'manifest.json',a.matrix/'ledger.json',*sorted(a.matrix.glob('*/result.json'))]},
        source_sha256=sha(__file__),cpu_seconds=time.process_time()-start,
        scope='Actual identical-path integration and separately measured method setup/evaluation costs. Cost-times-variance ratios are fixed-allocation precision-efficiency estimates, not directly timed executions at target precision. All costs cover T20 integration with both saved endpoints and paired numerical refinement. Twenty-thousand paired bootstrap resamples of eight independent batches retain method/timing covariance but do not certify tail variance. Narrow populations are stress tests; raw/remainder share the same expected quantity, not independent physical confirmations.')
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for r in rows:
        if r['s']==.25:
            print(r['tau'],r['population'],'cost-var ratio',r['cost_times_variance_ratio'],r['paired_batch_bootstrap_cost_ratio_interval'],'paired zero',r['paired_interval_contains_zero'])


if __name__ == '__main__':
    main()
