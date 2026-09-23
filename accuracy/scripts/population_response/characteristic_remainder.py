"""Independent deterministic characteristic quadrature with a cumulative control."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
from pathlib import Path
import argparse,hashlib,json,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'benchmark'))
from characteristics import advance,identities,Y1,Y0
from cumulative import physical_populations
from profiles import load_table
from check_cumulative_identity import profile as known_weight,primitive as known_primitive


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def assembly_control():
    J=16.;nj=1024;nphi=128;dt=.025;end=2.;s=.25
    x=-J+(np.arange(nj)+.5)*2*J/nj
    psi,j=np.meshgrid((np.arange(nphi)+.5)*2*np.pi/nphi,x,indexing='ij')
    psi,j=psi.ravel(),j.ravel();initial=j.copy();B=np.zeros_like(j)
    for _ in range(round(end/dt)):advance(psi,j,B,s,dt)
    control=known_primitive(initial+B)-known_primitive(initial)
    raw=float(np.sum(known_weight(initial)*B)*2*J/nj/nphi)
    remainder=float(-np.sum(control-known_weight(initial)*B)*2*J/nj/nphi)
    return dict(raw=raw,remainder=remainder,difference=remainder-raw,
                moment_budget=float(abs(j+s*end-initial-B).max()))


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--table',type=Path,required=True);p.add_argument('--s',type=float,required=True)
    p.add_argument('--J',type=float,default=160.);p.add_argument('--nj',type=int,default=10240)
    p.add_argument('--nphi',type=int,default=256);p.add_argument('--dt',type=float,default=.025)
    p.add_argument('--chunk',type=int,default=8);p.add_argument('--controls-only',action='store_true')
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    start,cpu=time.monotonic(),time.process_time()
    control=assembly_control();identity=identities()
    bound=20*(2*abs(Y1)+abs(Y0))
    if a.J<=64+bound:raise ValueError('Initial quadrature must cover the full negative-substep support bound')
    if abs(control['difference'])>=1e-10 or control['moment_budget']>=1e-10 or identity>=1e-10:
        raise ValueError('Analytical/assembly controls failed')
    if a.controls_only:
        r=dict(control=control,analytical_identity_error=identity,bar_impulse_bound=bound,
               minimum_auxiliary_half_domain=64+bound,all_pass=True,
               source_sha256=sha(__file__),cpu_seconds=time.process_time()-cpu)
        (a.out/'result.json').write_text(json.dumps(r,indent=2)+'\n')
        (a.out/'COMPLETE').write_text('Analytical controls complete; no halo response run.\n')
        print(json.dumps(r,indent=2));return
    meta,table=load_table(a.table);populations=physical_populations(meta,table,spacing=1/8192)
    names=list(populations);dx=2*a.J/a.nj
    x=-a.J+(np.arange(a.nj)+.5)*dx
    steps=round(20/a.dt)
    if abs(steps*a.dt-20)>1e-12 or abs(round(10/a.dt)*a.dt-10)>1e-12:
        raise ValueError('Require exact T10 and T20')
    saves={round(10/a.dt):0,steps:1}
    raw=np.zeros((2,len(names)));rem=np.zeros_like(raw);control_sum=np.zeros_like(raw)
    physical=np.zeros_like(raw);mass=np.zeros(len(names));Hsquared=np.zeros_like(raw)
    budget=0.;Bmax=0.;chunks=[]
    for begin in range(0,a.nphi,a.chunk):
        stop=min(begin+a.chunk,a.nphi)
        psi,j=np.meshgrid((np.arange(begin,stop)+.5)*2*np.pi/a.nphi,x,indexing='ij')
        psi,j=psi.ravel(),j.ravel();initial=j.copy();B=np.zeros_like(j)
        K0=-j*j/2-np.cos(psi)+a.s*psi;weight=dx/a.nphi
        wF={key:pop.evaluate(initial) for key,pop in populations.items()}
        for pi,key in enumerate(names):mass[pi]+=float(wF[key][0].sum()*weight)
        for step in range(1,steps+1):
            advance(psi,j,B,a.s,a.dt)
            if step in saves:
                ti=saves[step];t=step*a.dt
                budget=max(budget,float(abs(j+a.s*t-initial-B).max()))
                Bmax=max(Bmax,float(abs(B).max()))
                deltaK=-j*j/2-np.cos(psi)+a.s*psi-K0
                for pi,key in enumerate(names):
                    pop=populations[key];w,F=wF[key]
                    shifted=pop.evaluate(initial+B)[1]
                    raw[ti,pi]+=float(np.sum(w*B)*weight)
                    rem[ti,pi]+=float(-np.sum(shifted-F-w*B)*weight)
                    control_sum[ti,pi]+=float(np.sum(shifted-F)*weight)
                    physical[ti,pi]+=float(np.sum(w*(j+a.s*t-initial))*weight)
                    Hsquared[ti,pi]+=float(np.sum(w*deltaK**2)*weight)
        chunks.append(dict(begin=begin,stop=stop))
    np.savez_compressed(a.out/'recorded.npz',times=np.array([10.,20.]),raw_bar_impulse=raw,
        remainder_bar_impulse=rem,control_integral=control_sum,physical_change=physical,
        initial_mass=mass,hamiltonian_rms=np.sqrt(Hsquared/mass))
    gates=dict(positive_density=True,full_auxiliary_support=a.J>64+bound,
        path_budget=budget<1e-8,force_bound=Bmax<=bound+1e-10,
        analytical_identities=identity<1e-10,short_identity=abs(control['difference'])<1e-10)
    r=dict(config={k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items() if k not in ['out','table']},
        populations=names,times=[10.,20.],raw_bar_impulse=raw.tolist(),
        remainder_bar_impulse=rem.tolist(),control_integral=control_sum.tolist(),
        initial_mass=mass.tolist(),maximum_path_budget=budget,maximum_bar_impulse=Bmax,
        guaranteed_bar_impulse_bound=bound,control=control,gates=gates,all_pass=all(gates.values()),
        chunks=chunks,raw_sha256=sha(a.out/'recorded.npz'),table_sha256=sha(a.table/'halo-table.npz'),
        source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'benchmark/characteristics.py',Path(__file__).with_name('cumulative.py'),Path(__file__).with_name('profiles.py'),Path(__file__).with_name('check_cumulative_identity.py')]},
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        scope='Positive unnormalized physical weights; fourth-order deterministic characteristic flow. A cumulative zero-integral control changes the quadrature estimator, not the dynamics or population. Auxiliary nodes outside the physical support have no added physical mass. Raw/remainder differences here are deterministic quadrature errors, not stochastic uncertainties. Numerical refinement remains separate.')
    (a.out/'result.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
    (a.out/'COMPLETE').write_text('Cumulative characteristic quadrature complete; inspect refinements.\n')
    print(json.dumps({k:v for k,v in r.items() if k!='chunks'},indent=2))


if __name__=='__main__':main()
