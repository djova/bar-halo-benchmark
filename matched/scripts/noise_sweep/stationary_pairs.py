"""Independent positive-weight reflected-pair estimate, stationary resonance only."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import argparse, hashlib, json, sys, time
import numpy as np
ROOT=Path(__file__).resolve().parents[2]


def paired_paths(seed,dt,n=32768):
    assert dt in (.025,.0125)
    rng=np.random.default_rng(seed);initial=rng.normal(0,8,n);phase=rng.uniform(-np.pi,np.pi,n)
    j=np.stack((initial,initial));psi=np.stack((phase,phase));B=np.zeros_like(j);W=np.zeros(n)
    D=.2/np.pi;h=.025;refine=1 if dt==h else 2
    for _ in range(800):
        leaves=rng.normal(size=(n,2));increments=[np.sqrt(D*h)*leaves.sum(1)] if refine==1 else [np.sqrt(D*h)*leaves[:,k] for k in range(2)]
        for noise in increments:
            psi-=j*dt/2;impulse=-np.sin(psi)*dt
            j+=impulse;j[1]+=noise;B+=impulse;W+=noise;psi-=j*dt/2
    residual=j-initial-B;residual[1]-=W
    return initial,B,W,float(abs(residual).max())


def reflection_check(dt):
    rng=np.random.default_rng(8399);j=rng.normal(0,8,256);psi=rng.uniform(-np.pi,np.pi,256)
    jj=-j.copy();pp=-psi.copy();B=np.zeros(256);BB=np.zeros(256)
    steps=int(np.ceil(20/dt));dt=20/steps
    for _ in range(steps):
        psi-=j*dt/2;pp-=jj*dt/2
        noise=np.sqrt(2*(.2/np.pi)*dt)*rng.normal(size=256)
        b=-np.sin(psi)*dt;bb=-np.sin(pp)*dt
        j+=b+noise;jj+=bb-noise;B+=b;BB+=bb
        psi-=j*dt/2;pp-=jj*dt/2
    return float(max(np.max(abs(j+jj)),np.max(abs(psi+pp)),np.max(abs(B+BB))))


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--seed',required=True,type=int);p.add_argument('--dt',default=.025,type=float);a=p.parse_args();a.out.mkdir(exist_ok=False,parents=True)
    start,cpu=time.monotonic(),time.process_time();reflection=reflection_check(a.dt);assert reflection<1e-10
    ell=-0.004749321154862916;sigma=8;n=32768
    j,B,W,budget=paired_paths(a.seed,a.dt,n)
    c=.5*(ell*sigma)**2;plus=np.exp(ell*j-c);minus=np.exp(-ell*j-c)
    factor=.5*(plus-minus);mass=.5*(plus+minus);contrast=(B[1]-B[0])*factor
    mass_se=float(mass.std(ddof=1)/np.sqrt(n));expected=2*(.2/np.pi)*20
    gates=dict(reflection=reflection<1e-10,positive_weights=bool(np.all(plus>0)&np.all(minus>0)),normalization=abs(float(mass.mean())-1)<5*mass_se,path_budgets=budget<1e-9,noise_variance=abs(float(W.var(ddof=1))-expected)<5*expected*np.sqrt(2/(n-1)))
    np.savez_compressed(a.out/'recorded.npz',initial_j=j,positive_weights=plus,reflected_positive_weights=minus,pair_contrast=contrast,noise_impulse=W)
    result=dict(seed=a.seed,dt=a.dt,n_independent_pairs=n,mean=float(contrast.mean()),se=float(contrast.std(ddof=1)/np.sqrt(n)),mass_estimate=float(mass.mean()),mass_se=mass_se,reflection_error=reflection,maximum_budget_residual=budget,noisy_impulse=float(np.mean(B[1]*factor)),smooth_impulse=float(np.mean(B[0]*factor)),gates={k:bool(v) for k,v in gates.items()},all_pass=bool(all(gates.values())),cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),ROOT/'benchmark/resonance.py']},scope='Exact stationary reflection with two positive importance weights per independent pair. Same declared Gaussian target, no fitted coefficient. Counts pairs as independent samples. Fine/coarse use nested Brownian increments.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'COMPLETE').write_text('Finite reflected-pair estimate complete.\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
