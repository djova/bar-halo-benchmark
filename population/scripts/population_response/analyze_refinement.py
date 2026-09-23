"""Population-specific finite-time comparisons with separate numerical/window gates."""
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_matrix(path):
    ledger=json.loads((path/'ledger.json').read_text())
    if not (path/'TERMINAL').exists() or any(c['state']!='complete' for c in ledger['cases'].values()):
        raise ValueError('Matrix is not successfully complete: '+str(path))
    results={}
    for name in ledger['cases']:
        folder=path/name
        r=json.loads((folder/'result.json').read_text())
        if not (folder/'COMPLETE').exists() or sha(folder/'recorded.npz')!=r['raw_sha256']:
            raise ValueError('Missing or altered record: '+str(folder))
        results[name]=r
    return results


def noisy_B(r,t):
    rows=[v for v in r['history'] if abs(v['tau']-t)<1e-12]
    if len(rows)!=1:
        raise ValueError('Missing prescribed time')
    return np.array(rows[0]['bar_impulse'])


def collisionless_B(r,t,window=0):
    indices=[i for i,v in enumerate(r['times']) if abs(v-t)<1e-12]
    if len(indices)!=1:
        raise ValueError('Missing prescribed time')
    return np.array(r['windows'][window]['bar_impulse'][indices[0]])


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--pilot',type=Path,required=True)
    p.add_argument('--reference',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    pilot,ref=read_matrix(a.pilot),read_matrix(a.reference)
    rows=[]
    margin=2e-4
    for s in ['0','.25']:
        p0=pilot[f'bar-s{s}-eta.1']
        noisy={name:ref[f'noisy-s{s}-{name}'] for name in ['fine','halfstep','domain','wide']}
        chars={name:ref[f'characteristic-s{s}-{name}'] for name in ['base','fine','halfstep','domain']}
        expected=p0['profiles']
        for r in noisy.values():
            if r['profiles']!=expected:
                raise ValueError('Profile ordering mismatch')
        for r in chars.values():
            if any(w['profiles']!=expected for w in r['windows']):
                raise ValueError('Profile ordering mismatch')
        local=all(r['all_pass'] for r in [p0,*noisy.values(),*chars.values(),
                  ref[f'noisy-s{s}-unforced-wide']])
        for t in [10.,20.]:
            N=noisy_B(p0,t)
            C=collisionless_B(chars['base'],t)
            base=N-C
            best=noisy_B(noisy['fine'],t)-collisionless_B(chars['fine'],t)
            domain=noisy_B(noisy['domain'],t)-collisionless_B(chars['domain'],t)
            wide=noisy_B(noisy['wide'],t)-collisionless_B(chars['domain'],t,1)
            changes=dict(
                characteristic_quadrature=collisionless_B(chars['fine'],t)-C,
                noisy_mesh=noisy_B(noisy['fine'],t)-N,
                timestep=noisy_B(noisy['halfstep'],t)-collisionless_B(chars['halfstep'],t)-base,
                numerical_domain=domain-base,
                physical_window=wide-domain)
            for i,name in enumerate(expected):
                delta={k:float(v[i]) for k,v in changes.items()}
                gates={k:abs(v)<margin for k,v in delta.items()}
                observed_sum=sum(abs(v) for v in delta.values())
                rows.append(dict(s=float(s),tau=t,profile=name,
                    primary_fine_integral_w_K_B=float(best[i]),base_integral_w_K_B=float(base[i]),
                    wider_window_integral_w_K_B=float(wide[i]),
                    Lz_per_fast_action_area=float(best[i]*p0['Lz_per_fast_action_area_factor']),
                    initial_mass=p0['initial_mass'][i],
                    auxiliary_per_tracer=float(best[i]/p0['initial_mass'][i]),
                    comparison_changes=delta,comparison_gates=gates,all_local_gates_pass=local,
                    numerical_window_checks_pass=local and all(gates.values()),
                    sum_absolute_observed_changes=observed_sum,
                    sign_survives_observed_changes=bool(abs(best[i])>observed_sum),
                    independent_stochastic_validation='not performed in this matrix'))
    result=dict(rows=rows,absolute_comparison_target=margin,
        scope='Positive characteristic reference plus noisy forward calculation. Numerical and window evidence is separate from independent stochastic validation. The sum of observed changes is a diagnostic, not a rigorous error bound or confidence interval. Fixed-fast-action differential contribution, not total halo torque.',
        inputs={str(p):sha(p) for batch in [a.pilot,a.reference] for p in
            [batch/'manifest.json',batch/'ledger.json',*sorted(batch.glob('*/result.json'))]},
        source_sha256=sha(__file__))
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for row in rows:
        print(row['s'],row['tau'],row['profile'],row['primary_fine_integral_w_K_B'],
              row['numerical_window_checks_pass'],row['comparison_changes'])


if __name__=='__main__':
    main()
