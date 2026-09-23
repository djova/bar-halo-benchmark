"""Independent weighted paths with explicit action strata and paired refinements.

Each stratum samples the full uniform resonant phase and Brownian law. Optional
antithetic branches are one correlated observation, never two independent paths.
"""
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
from profiles import load_table,weights


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def combine_strata(means,covariances,edges,counts):
    widths=np.diff(edges)
    estimate=widths@means
    covariance=np.einsum('h,hij->ij',widths**2/counts,covariances)
    return estimate,covariance


def integrate(initial, phase, s, eta, dt, end, rng, bar=True):
    """dt is the coarse step; fine paths use dt/2 and the same Brownian leaves."""
    if abs(round(end/dt)*dt-end)>1e-12 or abs(round(10/dt)*dt-10)>1e-12:
        raise ValueError('Endpoints must be exact steps')
    steps=int(round(end/dt))
    n=len(initial)
    j=np.broadcast_to(initial,(6,n)).copy()
    psi=np.broadcast_to(phase,(6,n)).copy()
    B=np.zeros_like(j)
    W=np.zeros_like(j)
    saves={int(round(10/dt)):0,steps:1}
    records=np.zeros((2,6,n))
    worst=0.
    def step(indices,h,kicks):
        # Basic slices retain views, unlike integer-array fancy indexing.
        z=j[indices];p=psi[indices];b=B[indices];w=W[indices]
        p-=z*h/2
        impulse=-np.sin(p)*h if bar else np.zeros_like(p)
        z+=impulse-s*h+kicks
        b+=impulse;w+=kicks
        p-=z*h/2
    for k in range(1,steps+1):
        leaf1=np.sqrt(eta*2/np.pi*dt)*rng.normal(size=n)
        leaf2=np.sqrt(eta*2/np.pi*dt)*rng.normal(size=n)
        kicks=np.stack((leaf1,-leaf1,np.zeros(n)))
        step(slice(0,3),dt/2,kicks)
        kicks=np.stack((leaf2,-leaf2,np.zeros(n)))
        step(slice(0,3),dt/2,kicks)
        full=leaf1+leaf2
        step(slice(3,6),dt,np.stack((full,-full,np.zeros(n))))
        if k in saves:
            records[saves[k]]=B
            worst=max(worst,float(abs(j+s*k*dt-initial-B-W).max()))
    return records,worst,W


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--table',type=Path,required=True)
    p.add_argument('--s',type=float,required=True)
    p.add_argument('--eta',type=float,default=.1)
    p.add_argument('--seed',type=int,required=True)
    p.add_argument('--per-stratum',type=int,default=128)
    p.add_argument('--allocation',type=Path)
    p.add_argument('--dt',type=float,default=.025)
    p.add_argument('--end',type=float,default=20.)
    p.add_argument('--record-individual',action='store_true')
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    start,cpu=time.monotonic(),time.process_time()
    meta,table=load_table(a.table)
    if a.end!=20.:
        raise ValueError('This protocol has exactly T10 and T20 endpoints')
    if a.allocation:
        allocation=json.loads(a.allocation.read_text())
        edges=np.array(allocation['edges'],dtype=float)
        counts=np.array(allocation['counts'],dtype=int)
    else:
        edges=np.linspace(-64,64,129)
        counts=np.full(128,a.per_stratum,dtype=int)
    if len(counts)!=len(edges)-1 or np.any(counts<2) or np.any(np.diff(edges)<=0):
        raise ValueError('Need positive coverage and variance in every stratum')
    if edges[0]>-64 or edges[-1]<64:
        raise ValueError('Proposal must cover every physical taper')
    rng=np.random.default_rng(a.seed)
    initial=np.concatenate([rng.uniform(lo,hi,int(n)) for lo,hi,n in zip(edges[:-1],edges[1:],counts)])
    phase=rng.uniform(-np.pi,np.pi,len(initial))
    B,budget,W=integrate(initial,phase,a.s,a.eta,a.dt,a.end,rng)
    # Columns are all paired: times, numerical levels, estimator, physical DF.
    population=[];ws=[]
    for plateau,cutoff in [(24.,40.),(48.,64.)]:
        names=['gaussian','halo','exponential']
        ws.extend(weights(initial,names,meta,table,plateau,cutoff))
        population.extend([dict(name=name,plateau=plateau,cutoff=cutoff) for name in names])
    columns=[];contrasts=[]
    for ti,t in enumerate([10.,20.]):
        for level,start_index in [('fine',0),('coarse',3)]:
            plus=B[ti,start_index]-B[ti,start_index+2]
            antithetic=(B[ti,start_index]+B[ti,start_index+1])/2-B[ti,start_index+2]
            for estimator,contrast in [('single',plus),('antithetic',antithetic)]:
                for pop,w in zip(population,ws):
                    columns.append(dict(tau=t,level=level,estimator=estimator,**pop))
                    contrasts.append((w,contrast))
    means=[];covariances=[]
    begin=0
    for n in counts:
        stop=begin+n
        y=np.stack([w[begin:stop]*c[begin:stop] for w,c in contrasts],axis=1)
        means.append(y.mean(axis=0))
        covariances.append(np.cov(y,rowvar=False,ddof=1))
        begin=stop
    means=np.array(means);covariances=np.array(covariances)
    estimate,covariance=combine_strata(means,covariances,edges,counts)
    raw=dict(edges=edges,counts=counts,stratum_mean=means,stratum_covariance=covariances,
             mean=estimate,covariance=covariance)
    if a.record_individual:
        raw.update(initial_action=initial,initial_phase=phase,bar_impulse=B,stochastic_impulse=W)
    np.savez_compressed(a.out/'recorded.npz',**raw)
    gates=dict(path_budget=budget<1e-9,all_strata_present=bool(np.all(counts>=2)),
        physical_support_covered=bool(edges[0]<=-64 and edges[-1]>=64),
        positive_finite_weights=bool(np.all(np.isfinite(ws)) and np.all(np.array(ws)>=0)))
    result=dict(config={k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items() if k not in ['out','table']},
        columns=columns,mean=estimate.tolist(),conditional_standard_error=np.sqrt(np.diag(covariance)).tolist(),
        independent_initial_paths=int(counts.sum()),antithetic_branches_per_path=2,
        gates=gates,all_pass=all(gates.values()),maximum_path_budget=budget,
        source_sha256={name:sha(Path(__file__).with_name(name)) for name in ['stratified_paths.py','profiles.py']},
        raw_sha256=sha(a.out/'recorded.npz'),table_sha256=sha(a.table/'halo-table.npz'),
        allocation_sha256=sha(a.allocation) if a.allocation else None,
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        scope='Integral sum_h width_h mean_h(w times paired bar contrast); no unit-mass renormalization. Every action stratum contributes with its full weight. Fine/coarse paths share Brownian leaves. Antithetic branches and reweighted populations are correlated, not independent replicas. Pilot samples cannot qualify their own subsequently chosen allocation.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (a.out/'COMPLETE').write_text('Weighted paths complete; inspect independent precision and refinement.\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['columns','mean','conditional_standard_error']},indent=2))


if __name__=='__main__':
    main()
