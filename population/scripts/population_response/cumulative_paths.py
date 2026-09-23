"""Fresh expanded-support pilot/validation for raw and cumulative estimators."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
from pathlib import Path
import argparse,hashlib,json,time
import numpy as np
from profiles import load_table
from cumulative import physical_populations
from stratified_paths import integrate,combine_strata
from triangle_kernel import primitive_kernel,primitive_cell_average,contract_cells


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True);p.add_argument('--table',type=Path,required=True)
    p.add_argument('--s',type=float,required=True);p.add_argument('--seed',type=int,required=True)
    p.add_argument('--per-stratum',type=int,default=128);p.add_argument('--allocation',type=Path)
    p.add_argument('--dt',type=float,default=.025)
    p.add_argument('--verify-primitive',action='store_true')
    p.add_argument('--record-individual',action='store_true')
    p.add_argument('--record-kernel',action='store_true')
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    start,cpu=time.monotonic(),time.process_time();meta,table=load_table(a.table)
    if a.allocation:
        spec=json.loads(a.allocation.read_text());edges=np.array(spec['edges'],float);counts=np.array(spec['counts'],int)
    else:
        edges=np.arange(-88.,89.);counts=np.full(176,a.per_stratum,int)
    if len(edges)!=len(counts)+1 or np.any(counts<2) or np.any(np.diff(edges)<=0) or edges[0]>-84 or edges[-1]<84:
        raise ValueError('Need full expanded support and positive coverage in every stratum')
    rng=np.random.default_rng(a.seed)
    x=np.concatenate([rng.uniform(lo,hi,int(n)) for lo,hi,n in zip(edges[:-1],edges[1:],counts)])
    phase=rng.uniform(-np.pi,np.pi,len(x))
    B,budget,W=integrate(x,phase,a.s,.1,a.dt,20.,rng)
    populations=physical_populations(meta,table,spacing=1/8192)
    coarse=physical_populations(meta,table,spacing=1/4096) if a.verify_primitive else None
    # Process one stratum at a time, bounding memory even for a large allocation.
    definitions=[]
    for t in [10.,20.]:
        for level in ['fine','coarse']:
            for branch in ['single','antithetic']:
                for method in ['raw','remainder']:
                    for key in populations:
                        definitions.append(dict(tau=t,level=level,branch=branch,method=method,population=key))
    means=[];covariances=[];begin=0;primitive_change=0.
    for n in counts:
        stop=begin+n;xx=x[begin:stop];ys={}
        for key,pop in populations.items():
            w,_=pop.evaluate(xx)
            for ti,t in enumerate([10.,20.]):
                for level,i in [('fine',0),('coarse',3)]:
                    impulses=B[ti,i:i+3,begin:stop]
                    rem=np.stack([pop.remainder(xx,b) for b in impulses])
                    if coarse is not None:
                        low=np.stack([coarse[key].remainder(xx,b) for b in impulses])
                        primitive_change=max(primitive_change,float(abs(rem-low).max()))
                    raw=impulses*w
                    for branch in ['single','antithetic']:
                        for method,value in [('raw',raw),('remainder',-rem)]:
                            contrast=value[0]-value[2] if branch=='single' else (value[0]+value[1])/2-value[2]
                            ys[(t,level,branch,method,key)]=contrast
        y=np.stack([ys[(d['tau'],d['level'],d['branch'],d['method'],d['population'])] for d in definitions],axis=1)
        means.append(y.mean(axis=0));covariances.append(np.cov(y,rowvar=False,ddof=1));begin=stop
    means,covariances=np.array(means),np.array(covariances)
    estimate,covariance=combine_strata(means,covariances,edges,counts)
    raw=dict(edges=edges,counts=counts,stratum_mean=means,stratum_covariance=covariances,
             mean=estimate,covariance=covariance)
    kernel_error=None;kernel_change=None
    if a.record_kernel:
        grid=np.linspace(-64,64,32769)
        qweight=np.repeat(np.diff(edges)/counts,counts)
        Qcell=np.zeros((2,2,2,len(grid)-1));Qedge=np.zeros((2,2,2,len(grid)))
        raw_kernel=np.zeros((2,2,2,len(counts)));raw_kernel_variance=np.zeros_like(raw_kernel)
        kernel_error=0.;kernel_change=0.
        for ti,t in enumerate([10.,20.]):
            for li,(level,i) in enumerate([('fine',0),('coarse',3)]):
                point=[primitive_kernel(grid,x,B[ti,index],qweight) for index in range(i,i+3)]
                cell=[primitive_cell_average(grid,x,B[ti,index],qweight) for index in range(i,i+3)]
                for bi,branch in enumerate(['single','antithetic']):
                    coeff=np.array([1,0,-1]) if branch=='single' else np.array([.5,.5,-1])
                    Qcell[ti,li,bi]=sum(c*q for c,q in zip(coeff,cell))
                    Qedge[ti,li,bi]=sum(c*q for c,q in zip(coeff,point))
                    point_contrast=sum(c*B[ti,index] for c,index in zip(coeff,range(i,i+3)))
                    begin=0
                    for hi,n in enumerate(counts):
                        part=point_contrast[begin:begin+n];begin+=n
                        raw_kernel[ti,li,bi,hi]=part.mean()
                        raw_kernel_variance[ti,li,bi,hi]=part.var(ddof=1)/n
                    for key,pop in populations.items():
                        density=pop.evaluate(grid)[0]
                        prediction=float(contract_cells(grid,Qcell[ti,li,bi],density))
                        coarse_prediction=float(contract_cells(grid[::2],Qcell[ti,li,bi].reshape(-1,2).mean(axis=1),density[::2]))
                        column=definitions.index(dict(tau=t,level=level,branch=branch,method='remainder',population=key))
                        kernel_error=max(kernel_error,abs(prediction-estimate[column]))
                        kernel_change=max(kernel_change,abs(prediction-coarse_prediction))
        raw.update(kernel_edges=grid,kernel_primitive_cell_average=Qcell,
            kernel_primitive_at_edges=Qedge,raw_conditional_kernel=raw_kernel,
            raw_conditional_kernel_mean_variance=raw_kernel_variance)
    if a.record_individual:
        raw.update(initial_action=x,initial_phase=phase,bar_impulse=B,stochastic_impulse=W)
    np.savez_compressed(a.out/'recorded.npz',**raw)
    gates=dict(path_budget=budget<1e-9,bar_impulse_bound=bool(abs(B).max()<=20+1e-10),
               full_support=bool(edges[0]<=-84 and edges[-1]>=84),
               primitive_mesh=bool(primitive_change<1e-8) if coarse is not None else None,
               kernel_contraction=bool(kernel_error<1e-5 and kernel_change<1e-5) if a.record_kernel else None)
    result=dict(config={k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items() if k not in ['out','table']},
        columns=definitions,mean=estimate.tolist(),conditional_standard_error=np.sqrt(np.diag(covariance)).tolist(),
        independent_initial_paths=int(counts.sum()),maximum_path_budget=budget,
        maximum_primitive_remainder_change=primitive_change if coarse is not None else None,
        maximum_kernel_contraction_error=kernel_error,maximum_kernel_coarsening_change=kernel_change,
        gates=gates,all_performed_gates_pass=all(v for v in gates.values() if v is not None),
        source_sha256={name:sha(Path(__file__).with_name(name)) for name in ['cumulative_paths.py','cumulative.py','stratified_paths.py','profiles.py','triangle_kernel.py']},
        table_sha256=sha(a.table/'halo-table.npz'),raw_sha256=sha(a.out/'recorded.npz'),
        allocation_sha256=sha(a.allocation) if a.allocation else None,
        density_spacing=1/8192,cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        scope='Raw positive-density estimate versus an algebraically zero-integral control variate. Auxiliary quadrature paths include the full cutoff+T support, even where starting physical density is zero. All strata keep correct width weights. Brownian partners, numerical refinements, methods and populations are correlated; covariance is retained. Kernel array axes are time(T10,T20),level(fine,coarse),branch(single,antithetic),action. Cell-averaged primitives stably contract population gradients; their contributions are not individual initial-orbit cohorts. Raw conditional kernels retain the original starting-action meaning. This does not represent extra halo mass or a signed physical population.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (a.out/'COMPLETE').write_text('Cumulative paths complete; inspect independent comparisons.\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['columns','mean','conditional_standard_error']},indent=2))


if __name__=='__main__':main()
