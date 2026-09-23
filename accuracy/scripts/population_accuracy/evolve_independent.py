"""Independent six-population evolution after committed numerical forecasts."""
from common import ROOT, NAMES, WINDOWS, density, populations, load_table, sha
from forward import evolve
from characteristic_remainder import assembly_control, advance, identities, Y1, Y0
import argparse
import json
import time
from pathlib import Path
import numpy as np


def characteristics(meta, table, J, nj, nphi, dt, chunk):
    bound = 20*(2*abs(Y1)+abs(Y0))
    if J <= 64+bound:
        raise ValueError('Missing auxiliary support for negative substeps')
    control, identity = assembly_control(), identities()
    if abs(control['difference']) >= 1e-10 or identity >= 1e-10:
        raise ValueError('Independent analytical controls failed')
    pops = populations(meta, table)
    names = list(pops)
    dx = 2*J/nj
    x = -J+(np.arange(nj)+.5)*dx
    steps = round(20/dt)
    if abs(steps*dt-20)>1e-12 or abs(round(10/dt)*dt-10)>1e-12:
        raise ValueError('Exact endpoints required')
    saves = {round(10/dt):0, steps:1}
    raw = np.zeros((2,len(names)))
    remainder = np.zeros_like(raw)
    mass = np.zeros(len(names))
    budget = bmax = 0.
    for begin in range(0,nphi,chunk):
        stop = min(begin+chunk,nphi)
        psi,j = np.meshgrid((np.arange(begin,stop)+.5)*2*np.pi/nphi,x,indexing='ij')
        psi,j = psi.ravel(),j.ravel()
        initial = j.copy()
        B = np.zeros_like(j)
        weight = dx/nphi
        wF = {name:pop.evaluate(initial) for name,pop in pops.items()}
        for pi,name in enumerate(names):
            mass[pi] += float(wF[name][0].sum()*weight)
        for step in range(1,steps+1):
            advance(psi,j,B,.5,dt)
            if step in saves:
                ti,tau = saves[step],step*dt
                budget = max(budget,float(abs(j+.5*tau-initial-B).max()))
                bmax = max(bmax,float(abs(B).max()))
                for pi,name in enumerate(names):
                    w,F = wF[name]
                    shifted = pops[name].evaluate(initial+B)[1]
                    raw[ti,pi] += float(np.sum(w*B)*weight)
                    remainder[ti,pi] -= float(np.sum(shifted-F-w*B)*weight)
    gates = dict(path_budget=budget<1e-8,force_bound=bmax<=bound+1e-10,
                 full_auxiliary_support=J>64+bound,analytical_identities=identity<1e-10,
                 short_identity=abs(control['difference'])<1e-10)
    result = dict(populations=names,times=[10.,20.],raw_bar_impulse=raw.tolist(),
        remainder_bar_impulse=remainder.tolist(),initial_mass=mass.tolist(),
        maximum_path_budget=budget,maximum_bar_impulse=bmax,
        guaranteed_bar_impulse_bound=bound,control=control,gates=gates,all_pass=all(gates.values()))
    arrays = dict(times=np.array([10.,20.]),raw_bar_impulse=raw,remainder_bar_impulse=remainder,initial_mass=mass)
    return result,arrays


def main():
    p = argparse.ArgumentParser()
    for name in ('out','table','forecast'):
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--method',choices=['distribution','characteristic'],required=True)
    p.add_argument('--J',type=float,required=True)
    p.add_argument('--nj',type=int,required=True)
    p.add_argument('--nphi',type=int,required=True)
    p.add_argument('--dt',type=float,default=.025)
    p.add_argument('--chunk',type=int,default=8)
    p.add_argument('--wide',action='store_true')
    p.add_argument('--no-bar',action='store_true')
    a = p.parse_args()
    forecast = json.loads(a.forecast.read_text())
    if not (a.forecast.parent/'FROZEN_PREDICTIONS').exists():
        raise ValueError('Committed prospective predictions are required')
    if forecast['developmental'] or forecast['s'] != .5 or forecast['eta'] != .1:
        raise ValueError('Not the preselected new condition')
    if sha(a.forecast.parent/'kernel-batches.npz') != forecast['raw_sha256']:
        raise ValueError('Forecast kernel changed')
    expected = {(t,n,int(c)) for t in (10.,20.) for n in NAMES for _,c in WINDOWS}
    if {(r['tau'],r['population'],r['cutoff']) for r in forecast['rows']} != expected:
        raise ValueError('Incomplete prospective family')
    if forecast['source_sha256']['common.py'] != sha(Path(__file__).with_name('common.py')):
        raise ValueError('Physical population source changed')
    if forecast['table_sha256'] != sha(a.table/'halo-table.npz'):
        raise ValueError('Unforced halo table changed')
    a.out.mkdir(parents=True,exist_ok=False)
    start,cpu = time.monotonic(),time.process_time()
    meta,table = load_table(a.table)
    if a.method == 'distribution':
        x = -a.J+(np.arange(a.nj)+.5)*2*a.J/a.nj
        plateau,cutoff = WINDOWS[int(a.wide)]
        w = np.stack([density(x,meta,table,name,plateau,cutoff) for name in NAMES])
        result,arrays = evolve(w,.5,.1,a.J,a.nphi,a.dt,20.,not a.no_bar)
        result['profiles'] = list(NAMES)
    else:
        if a.no_bar or a.wide:
            raise ValueError('Characteristics cover both windows; unforced control uses forward solver')
        result,arrays = characteristics(meta,table,a.J,a.nj,a.nphi,a.dt,a.chunk)
    np.savez_compressed(a.out/'recorded.npz',**arrays)
    sources = [Path(__file__),Path(__file__).with_name('common.py')]
    sources += [ROOT/'scripts/population_response'/n for n in ['forward.py','characteristic_remainder.py','cumulative.py','profiles.py','check_cumulative_identity.py']]
    sources += [ROOT/'benchmark/characteristics.py']
    result.update(config={k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items() if k not in ('out','table')},
        forecast_sha256=sha(a.forecast),source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sources},
        table_sha256=sha(a.table/'halo-table.npz'),raw_sha256=sha(a.out/'recorded.npz'),
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        scope='Independent evolution under the preselected s0.5 local operator. Positive absolute populations; no refitting, unit-mass normalization or new 3D/live-halo/SIDM interpretation. Prospective numerical forecasts were frozen first.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (a.out/'COMPLETE').write_text('Independent population evolution complete; inspect all comparisons.\n')
    print(json.dumps({k:v for k,v in result.items() if k!='history'},indent=2))
    if not result['all_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
