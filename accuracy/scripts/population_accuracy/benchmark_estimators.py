"""Actual matched component CPU and paired estimator variance on the same paths."""
from common import ROOT, Population, density, load_table, sha, taper
from stratified_paths import integrate, combine_strata
import argparse
import json
import time
from pathlib import Path
import numpy as np

NAMES = ('halo', 'exponential', 'gaussian8', 'stress1', 'stress0.125', 'stress0.015625')


def weight(x, name, meta, table):
    if name.startswith('stress'):
        sigma = float(name.removeprefix('stress'))
        return np.exp(meta['g']*x-x*x/(2*sigma*sigma))*taper(x, 24., 40.)
    return density(x, meta, table, name)


def numerical_weight(x, name, meta, table):
    """Same piecewise-linear population as the primitive, without unused nodes."""
    q = np.clip((np.asarray(x)+96)*8192,0,192*8192)
    index = np.minimum(q.astype(np.int64),192*8192-1)
    z = q-index
    left = weight(-96+index/8192, name, meta, table)
    right = weight(-96+(index+1)/8192, name, meta, table)
    return left+(right-left)*z


def postprocess(method, name, initial, B, meta, table):
    if method == 'raw':
        w = numerical_weight(initial, name, meta, table)
        value = B*w
    else:
        grid = np.linspace(-96, 96, 192*8192+1)
        pop = Population(grid, weight(grid, name, meta, table))
        value = -pop.remainder(initial, B)
    # Endpoints, {fine, coarse}; each Brownian pair is one observation.
    return np.stack([(value[:,i]+value[:,i+1])/2-value[:,i+2] for i in (0,3)], axis=1)


def main():
    p = argparse.ArgumentParser()
    for name in ('out', 'table'):
        p.add_argument('--'+name, type=Path, required=True)
    p.add_argument('--s', type=float, choices=[0., .25], required=True)
    p.add_argument('--seed', type=int, required=True)
    p.add_argument('--per-stratum', type=int, default=512)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    cpu, wall = time.process_time(), time.monotonic()
    meta, table = load_table(a.table)
    edges = np.arange(-88., 89.)
    counts = np.full(176, a.per_stratum, int)
    rng = np.random.default_rng(a.seed)
    initial = np.concatenate([rng.uniform(lo, hi, n) for lo,hi,n in zip(edges[:-1],edges[1:],counts)])
    phase = rng.uniform(-np.pi, np.pi, len(initial))
    before = time.process_time()
    B, budget, W = integrate(initial, phase, a.s, .1, .025, 20., rng)
    integration_cpu = time.process_time()-before
    outputs, timing = {}, {}
    for name in NAMES:
        for repeat in range(3):
            methods = ('raw', 'remainder') if (repeat+a.seed)%2 else ('remainder', 'raw')
            for method in methods:
                before = time.process_time()
                values = postprocess(method, name, initial, B, meta, table)
                elapsed = time.process_time()-before
                timing.setdefault((name,method), []).append(elapsed)
                if (name,method) in outputs and not np.array_equal(values,outputs[name,method]):
                    raise ValueError('Repeated deterministic postprocessing changed')
                outputs[name,method] = values
    columns = [dict(tau=t, level=level, population=name, method=method)
               for t in (10.,20.) for level in ('fine','coarse') for name in NAMES for method in ('raw','remainder')]
    means, covariances, offset = [], [], 0
    for n in counts:
        stop = offset+n
        values = np.stack([outputs[c['population'],c['method']][int(c['tau']/10-1),int(c['level']=='coarse'),offset:stop]
                           for c in columns], axis=1)
        means.append(values.mean(axis=0)); covariances.append(np.cov(values,rowvar=False,ddof=1))
        offset = stop
    means, covariances = np.array(means), np.array(covariances)
    estimate, covariance = combine_strata(means,covariances,edges,counts)
    np.savez_compressed(a.out/'recorded.npz', edges=edges,counts=counts,
                        stratum_mean=means,stratum_covariance=covariances,mean=estimate,covariance=covariance)
    timings = [dict(population=name,method=method,postprocessing_cpu_seconds=values,
                    accounted_single_population_cpu_seconds=integration_cpu+float(np.median(values)))
               for (name,method),values in timing.items()]
    gates = dict(path_budget=budget<1e-9, impulse_bound=bool(abs(B).max()<=20+1e-10),
                 full_auxiliary_support=bool(edges[0]<=-60 and edges[-1]>=60),
                 finite_statistics=bool(np.all(np.isfinite(estimate)) and np.all(np.isfinite(covariance))))
    result = dict(config=dict(s=a.s,seed=a.seed,eta=.1,coarse_dt=.025,paths=int(counts.sum())),
        columns=columns,mean=estimate.tolist(),integration_cpu_seconds=integration_cpu,timings=timings,
        maximum_path_budget=budget,gates=gates,all_pass=all(gates.values()),
        raw_sha256=sha(a.out/'recorded.npz'),table_sha256=sha(a.table/'halo-table.npz'),
        source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),Path(__file__).with_name('common.py'),ROOT/'scripts/population_response/stratified_paths.py',ROOT/'scripts/population_response/cumulative.py',ROOT/'scripts/population_response/profiles.py']},
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-wall,
        scope='Measured shared integration plus separately timed per-population setup and estimator evaluation on identical paths. Both accounted workflows include paired fine/coarse integration. Postprocessing timed three times in alternating order; all timings retained. Covariance assembly and writing are excluded from both method-specific costs but included in job CPU. No forecast of actual galactic torque or claimed precision speedup before variance analysis.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (a.out/'COMPLETE').write_text('All cost and covariance measurements recorded.\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('columns','mean','source_sha256')},indent=2))
    if not result['all_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
