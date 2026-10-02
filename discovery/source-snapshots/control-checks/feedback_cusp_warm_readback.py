"""Saved-array arithmetic and descriptive tails; no sampling or evolution."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time

START = time.process_time()
resource.setrlimit(resource.RLIMIT_CPU, (20, 25))
import numpy as np

RESULT = 'e1a0e06d6f1937e3aab2b05281fed0810c2d04970e42820f3f448548fc5c7685'
ROOT = Path(__file__).resolve().parents[2]
CUTOFFS = [None, .25, .5, 1., 2.]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def stat(x):
    return dict(mean=float(np.mean(x)), standard_error=float(np.std(x, ddof=1)/np.sqrt(len(x))))


def mass(c):
    return 1. if c is None else float(-np.expm1(-c)-c*np.exp(-c))


def same(a, b):
    for key in ('mean', 'standard_error'):
        assert np.isclose(a[key], b[key], rtol=2e-12, atol=1e-25), (key, a, b)


def tail(x, z):
    order = np.argsort(-abs(x), kind='stable')
    total = float(np.sum(x))
    absolute = float(np.sum(abs(x)))
    return dict(mean=stat(x), effective_sample_size=float(total**2/np.sum(x*x)) if np.sum(x*x) else None,
        positive_count=int(np.sum(x>0)), negative_count=int(np.sum(x<0)), zero_count=int(np.sum(x==0)),
        negative_absolute_fraction=float(-np.sum(x[x<0])/absolute) if absolute else 0.,
        top_absolute_contributions=[dict(count=n, absolute_share=float(np.sum(abs(x[order[:n]]))/absolute) if absolute else 0.,
            signed_share=float(np.sum(x[order[:n]])/total) if total else None) for n in (1,5,32)],
        top_five=[dict(id=int(i), contribution=float(x[i]), Rc=float(z['Rc'][i]), L=float(z['L'][i]),
            radius=float(z['radius'][i]), Jr_over_Js=float(z['Jr'][i]/z['Js'][i]),
            guide_component=int(z['guide_component'][i]), radial_tail_component=bool(z['radial_component'][i]),
            initial_physical_weight=float(z['physical_weight'][i])) for i in order[:5]])


def run(args):
    args.out.mkdir(parents=True, exist_ok=False)
    assert sha(args.input/'result.json') == RESULT
    recorded=json.loads((args.input/'result.json').read_text())
    assert recorded['status']=='COMPLETE' and recorded['gate'] is False and recorded['closure_integrity']['gate']
    for relative, digest in recorded['source_sha256'].items():
        assert sha(ROOT/relative)==digest
        assert sha(args.input/'inputs'/Path(relative).name)==digest
    for path, digest in recorded['known_initial_sha256'].items():
        assert sha(path)==digest
    known=dict(json.loads((args.input/'inputs'/'input-hashes.json').read_text()))
    for path, digest in known.items(): assert sha(path)==digest
    z=np.load(args.input/'initial.npz'); n=len(z['Rc']);assert n==512
    rows=[]; response=[]; maps=[]
    for block in recorded['completed']:
        name=block['name']; m=np.load(args.input/f'{name}-maps.npz'); rr=np.load(args.input/f'{name}-response.npz')
        for count in ('32','64'):
            positive=z['guide_weight'][None,:]*(rr['R_'+count]+rr['support_'+count])/z['radial_q'][None,:]
            signed=z['physical_weight'][None,:]*m['deltaE'][[0,2,4]]
            assert np.array_equal(positive,rr['positive_'+count])
            assert np.array_equal(signed,rr['ordinary_signed_'+count])
            assert np.all(rr['R_'+count]>=0) and np.all(rr['support_'+count]>=0)
        replay=np.load(args.input/f'{name}-inverse-replay.npz')
        errors=np.maximum(abs(replay['radius']-z['radius'])/(1+z['radius']),abs(replay['pr']-z['pr'])/(1+abs(z['pr'])))
        assert np.array_equal(errors,replay['scaled_error'])
        assert float(errors.max())==block['inverse_scaled_error_maximum']
        assert block['capture_counts']==[int(np.sum(m['delta_final'][i]>=-z['energy_circular'])) for i in (1,3,5)]
        for old in block['rows']:
            c=old['Rc_upper']; j=1 if old['frequency']==5 else 2
            multiplier=np.ones(n) if c is None else (z['Rc']<c)/mass(c)
            paired=(rr['positive_64'][j]-rr['positive_64'][0])*multiplier
            values=dict(actual_forward=stat(rr['positive_64'][j]*multiplier),zero=stat(rr['positive_64'][0]*multiplier),
                paired=stat(paired),ordinary_signed=stat(rr['ordinary_signed_64'][j]*multiplier),
                absolute_energy_work=stat(z['physical_weight']*(abs(m['energy_minus_work'][2*j])+abs(m['energy_minus_work'][0]))*multiplier),
                curvature_difference=stat((rr['positive_64'][j]-rr['positive_32'][j])*multiplier))
            for key,value in values.items():same(value,old[key])
            rows.append(dict(name=name,Rc_upper=c,frequency=old['frequency'],physical_mass=mass(c),**values,
                relative_SE=values['paired']['standard_error']/values['paired']['mean'],
                work_fraction=values['absolute_energy_work']['mean']/values['paired']['mean'],
                tails=tail(paired,z)))
        response.append(rr); maps.append(m)
    refined=np.load(args.input/'fine-action256-response.npz')
    for old in recorded['paired_refinement']:
        c=old['Rc_upper']; j=1 if old['frequency']==5 else 2
        multiplier=np.ones(n) if c is None else (z['Rc']<c)/mass(c)
        fine=response[1]['positive_64'][j]-response[1]['positive_64'][0]
        coarse=response[0]['positive_64'][j]-response[0]['positive_64'][0]
        same(stat((fine-coarse)*multiplier),old['fine_minus_coarse'])
        same(stat((refined['positive'][j]-refined['positive'][0]-fine)*multiplier),old['action256_minus128'])
    ref=np.load(args.input/'selected-radial-reference.npz'); cart=np.load(args.input/'selected-cartesian-reference.npz')
    ids=np.array(recorded['selected_before_forced_outcomes']['ids']);reference=[]
    rerr=abs(ref['radius']-cart['radius'])/(1+ref['radius'])
    perr=abs(ref['pr']-cart['pr'])/(1+abs(ref['pr']))
    assert float(rerr.max())==recorded['reference']['radial_cartesian_scaled_r_error']
    assert float(perr.max())==recorded['reference']['radial_cartesian_scaled_pr_error']
    for k,i in enumerate(ids):
        reference.append(dict(id=int(i),Rc=float(z['Rc'][i]),L=float(z['L'][i]),radius=float(z['radius'][i]),
            initial_physical_weight=float(z['physical_weight'][i]),Jr_over_Js=float(z['Jr'][i]/z['Js'][i]),
            scaled_radius_errors=rerr[:,k].tolist(),scaled_momentum_errors=perr[:,k].tolist(),
            radial_cartesian_energy_difference=(ref['deltaE'][:,k]-cart['deltaE'][:,k]).tolist(),
            radial_energy_minus_work=(ref['deltaE'][:,k]-ref['work'][:,k]).tolist(),
            Cartesian_energy_minus_work=(cart['deltaE'][:,k]-cart['work'][:,k]).tolist(),
            KDK_coarse_scaled_radius_error=(abs(maps[0]['radius'][:,i]-ref['radius'][:,k])/(1+ref['radius'][:,k])).tolist(),
            KDK_fine_scaled_radius_error=(abs(maps[1]['radius'][:,i]-ref['radius'][:,k])/(1+ref['radius'][:,k])).tolist(),
            KDK_coarse_scaled_momentum_error=(abs(maps[0]['pr'][:,i]-ref['pr'][:,k])/(1+abs(ref['pr'][:,k]))).tolist(),
            KDK_fine_scaled_momentum_error=(abs(maps[1]['pr'][:,i]-ref['pr'][:,k])/(1+abs(ref['pr'][:,k]))).tolist(),
            KDK_coarse_energy_difference=(maps[0]['deltaE'][:,i]-ref['deltaE'][:,k]).tolist(),
            KDK_fine_energy_difference=(maps[1]['deltaE'][:,i]-ref['deltaE'][:,k]).tolist()))
    strata=[]
    for variable,cuts in [('Rc',[0.,.03,.1,.25,.5,1.,2.,8.,None]),('L',[0.,.001,.01,.1,1.,None]),
        ('Jr_over_Js',[0.,.1,1.,3.,10.,100.,None])]:
        v=z['Jr']/z['Js'] if variable=='Jr_over_Js' else z[variable]
        for low,high in zip(cuts[:-1],cuts[1:]):
            mask=(v>=low) & (np.ones(n,dtype=bool) if high is None else v<high)
            strata.append(dict(variable=variable,lower=low,upper=high,count=int(mask.sum()),physical_mass=stat(z['physical_weight']*mask),
                paired_heat={str(f):stat((response[1]['positive_64'][j]-response[1]['positive_64'][0])*mask) for j,f in [(1,5),(2,8)]},
                weighted_absolute_work_error={str(f):stat(z['physical_weight']*(abs(maps[1]['energy_minus_work'][2*j])+abs(maps[1]['energy_minus_work'][0]))*mask) for j,f in [(1,5),(2,8)]}))
    files=[p for p in args.input.iterdir() if p.suffix=='.npz']+[args.input/'result.json']
    result=dict(status='COMPLETE',gate=True,arithmetic_gate=True,original_scientific_gate=False,input_sha256={p.name:sha(p) for p in files},
        source_sha256=sha(__file__),scope='Saved arithmetic only; descriptive tails never exclude, clip, renormalize or alter qualification.',
        rows=rows,reference_by_path=reference,descriptive_strata=strata,
        target_underflow_count=int(np.sum(z['g']==0)),physical_mass=stat(z['physical_weight']),
        physical_mass_ESS=float(np.sum(z['physical_weight'])**2/np.sum(z['physical_weight']**2)),
        original_failed_gates=['Principal warm heating sampling precision exceeds30%.',
            'Selected radial/Cartesian DOP endpoint differences exceed1e-7.',
            'Coarse whole omega8 work accounting exceeds5%; fine passes.'],
        cpu_seconds=time.process_time()-START)
    (args.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(status=result['status'],arithmetic_gate=True,original_scientific_gate=False,cpu_seconds=result['cpu_seconds'])))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    run(p.parse_args())
