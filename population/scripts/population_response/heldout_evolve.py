"""Independent new-population evolution, guarded by a saved prospective forecast."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1'
from pathlib import Path
import argparse,json,hashlib,sys,time
import numpy as np
from profiles import load_table
from heldout_profiles import density,populations,NAMES
from forward import evolve
from characteristic_remainder import assembly_control,advance,identities,Y1,Y0
ROOT=Path(__file__).resolve().parents[2]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def characteristics(meta,s,J,nj,nphi,dt,chunk):
    bound=20*(2*abs(Y1)+abs(Y0))
    if J<=64+bound:raise ValueError('Full negative-substep auxiliary support required')
    control=assembly_control();analytic=identities()
    if abs(control['difference'])>=1e-10 or analytic>=1e-10:raise ValueError('Analytical controls failed')
    pops=populations(meta);names=list(pops);dx=2*J/nj
    x=-J+(np.arange(nj)+.5)*dx
    steps=round(20/dt)
    if abs(steps*dt-20)>1e-12 or abs(round(10/dt)*dt-10)>1e-12:raise ValueError('Exact endpoints required')
    saves={round(10/dt):0,steps:1};raw=np.zeros((2,6));rem=np.zeros_like(raw)
    mass=np.zeros(6);budget=Bmax=0.
    for begin in range(0,nphi,chunk):
        stop=min(begin+chunk,nphi)
        psi,j=np.meshgrid((np.arange(begin,stop)+.5)*2*np.pi/nphi,x,indexing='ij')
        psi,j=psi.ravel(),j.ravel();initial=j.copy();B=np.zeros_like(j);weight=dx/nphi
        wF={key:pop.evaluate(initial) for key,pop in pops.items()}
        for pi,key in enumerate(names):mass[pi]+=float(wF[key][0].sum()*weight)
        for step in range(1,steps+1):
            advance(psi,j,B,s,dt)
            if step in saves:
                ti=saves[step];tau=step*dt
                budget=max(budget,float(abs(j+s*tau-initial-B).max()));Bmax=max(Bmax,float(abs(B).max()))
                for pi,key in enumerate(names):
                    w,F=wF[key];shifted=pops[key].evaluate(initial+B)[1]
                    raw[ti,pi]+=float(np.sum(w*B)*weight)
                    rem[ti,pi]+=float(-np.sum(shifted-F-w*B)*weight)
    gates=dict(path_budget=budget<1e-8,force_bound=Bmax<=bound+1e-10,
        full_auxiliary_support=J>64+bound,analytical_identities=analytic<1e-10,
        short_identity=abs(control['difference'])<1e-10)
    result=dict(populations=names,times=[10.,20.],raw_bar_impulse=raw.tolist(),
        remainder_bar_impulse=rem.tolist(),initial_mass=mass.tolist(),maximum_path_budget=budget,
        maximum_bar_impulse=Bmax,guaranteed_bar_impulse_bound=bound,control=control,
        gates=gates,all_pass=all(gates.values()))
    return result,dict(times=np.array([10.,20.]),raw_bar_impulse=raw,remainder_bar_impulse=rem,initial_mass=mass)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--forecast',type=Path,required=True);p.add_argument('--table',type=Path,required=True)
    p.add_argument('--method',choices=['distribution','characteristic'],required=True)
    p.add_argument('--s',type=float,choices=[0.,.25],required=True)
    p.add_argument('--J',type=float,required=True);p.add_argument('--nj',type=int,required=True)
    p.add_argument('--nphi',type=int,required=True);p.add_argument('--dt',type=float,default=.025)
    p.add_argument('--chunk',type=int,default=8);p.add_argument('--plateau',type=float,default=24.)
    p.add_argument('--cutoff',type=float,default=40.);p.add_argument('--no-bar',action='store_true')
    a=p.parse_args();forecast=json.loads(a.forecast.read_text())
    if not (a.forecast.parent/'FROZEN_PREDICTIONS').exists():raise ValueError('Saved prospective predictions required')
    if sha(a.forecast.parent/'predictions.npz')!=forecast['raw_sha256']:raise ValueError('Forecast arrays changed')
    expected={(s,t,f'{name}-{cutoff}') for s in [0.,.25] for t in [10.,20.] for name in NAMES for cutoff in [40,64]}
    if {(r['s'],r['tau'],r['population']) for r in forecast['rows']}!=expected:raise ValueError('Incomplete forecasts')
    if forecast['source_sha256']['heldout_profiles.py']!=sha(Path(__file__).with_name('heldout_profiles.py')):
        raise ValueError('Physical shapes changed after forecast')
    meta,table=load_table(a.table)
    if forecast['table_sha256']!=sha(a.table/'halo-table.npz'):raise ValueError('Unforced table changed')
    a.out.mkdir(parents=True,exist_ok=False);start,cpu=time.monotonic(),time.process_time()
    if a.method=='distribution':
        x=-a.J+(np.arange(a.nj)+.5)*2*a.J/a.nj
        w=np.stack([density(x,meta['g'],name,a.plateau,a.cutoff) for name in NAMES])
        result,raw=evolve(w,a.s,.1,a.J,a.nphi,a.dt,20.,not a.no_bar)
        result['profiles']=NAMES
    else:
        if a.no_bar:raise ValueError('Bar-free controls use the distribution solver')
        result,raw=characteristics(meta,a.s,a.J,a.nj,a.nphi,a.dt,a.chunk)
    np.savez_compressed(a.out/'recorded.npz',**raw)
    files=[Path(__file__),Path(__file__).with_name('heldout_profiles.py'),Path(__file__).with_name('forward.py'),Path(__file__).with_name('characteristic_remainder.py'),Path(__file__).with_name('cumulative.py'),Path(__file__).with_name('profiles.py'),Path(__file__).with_name('check_cumulative_identity.py'),ROOT/'benchmark/characteristics.py']
    result.update(config={k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items() if k not in ['out','table']},
        forecast_sha256=sha(a.forecast),source_sha256={str(f.relative_to(ROOT)):sha(f) for f in files},
        table_sha256=sha(a.table/'halo-table.npz'),raw_sha256=sha(a.out/'recorded.npz'),
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        scope='Independent held-out positive-population distribution/characteristic evolution. Same central absolute density, no window renormalization. Prospective response-kernel predictions must be committed before these outcomes. A local external-model test, not3D, live-halo or SIDM physics.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (a.out/'COMPLETE').write_text('Held-out evolution complete; inspect all comparisons.\n')
    print(json.dumps({k:v for k,v in result.items() if k!='history'},indent=2))


if __name__=='__main__':main()
