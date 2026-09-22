"""Positive quadrature of collisionless Liouville characteristics; fourth order."""
import os
os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import argparse,hashlib,json,time
import numpy as np

SLOPE=-0.016531804196572842
Y1=1/(2-2**(1/3));Y0=-2**(1/3)*Y1


def advance(psi,j,B,s,dt,bar=True):
    for q in (Y1,Y0,Y1):
        h=dt*q;psi-=j*h/2
        impulse=-np.sin(psi)*h if bar else np.zeros_like(j)
        j+=impulse-s*h;B+=impulse;psi-=j*h/2


def identities():
    worst=0.
    for s in (0.,.1,.4):
        psi=np.array([np.pi+np.arcsin(s)]);j=np.zeros(1);B=np.zeros(1)
        for _ in range(400):advance(psi,j,B,s,.025)
        worst=max(worst,abs(float(j[0])),abs(float(B[0]-s*10)),abs(float(psi[0]-np.pi-np.arcsin(s))))
    psi=np.array([.3,1.2]);j=np.array([-.4,2.]);B=np.zeros(2);oldpsi=psi.copy();oldj=j.copy();s=.4
    for _ in range(400):advance(psi,j,B,s,.025,False)
    worst=max(worst,float(np.max(abs(j-(oldj-s*10)))),float(np.max(abs(psi-(oldpsi-oldj*10+.5*s*100)))))
    return worst


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--s',required=True,type=float)
    p.add_argument('--nphi',type=int,default=128);p.add_argument('--nj',type=int,default=2048);p.add_argument('--J',type=float,default=64.)
    p.add_argument('--dt',type=float,default=.025);p.add_argument('--end',type=float);p.add_argument('--slope',type=float,default=SLOPE);p.add_argument('--sigma',type=float,default=8.);a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False);start,cpu=time.monotonic(),time.process_time();analytical=identities();assert analytical<1e-10
    end=a.end if a.end is not None else (min(8*np.pi,8/a.s) if a.s else 8*np.pi)
    steps=int(np.ceil(end/a.dt));dt=end/steps;dx=2*a.J/a.nj
    j0=-a.J+(np.arange(a.nj)+.5)*dx;phi0=(np.arange(a.nphi)+.5)*2*np.pi/a.nphi
    psi,j=np.meshgrid(phi0,j0,indexing='ij');psi=psi.ravel();j=j.ravel()
    weight=np.exp(-.5*((j-a.slope*a.sigma**2)/a.sigma)**2)*dx/(a.sigma*np.sqrt(2*np.pi)*a.nphi)
    initial_mass=float(weight.sum());weight/=initial_mass;initial=j.copy();B=np.zeros_like(j)
    K0=-j*j/2-np.cos(psi)+a.s*psi
    save=set(np.rint(np.linspace(0,steps,201)).astype(int));snap=set(np.rint(np.linspace(0,steps,21)).astype(int));rows=[];density=[];times=[]
    maxbudget=0.;maxH=0.
    for step in range(steps+1):
        tau=step*dt
        if step in save:
            residual=j+a.s*tau-initial-B;maxbudget=max(maxbudget,float(np.max(abs(residual))))
            K=-j*j/2-np.cos(psi)+a.s*psi;maxH=max(maxH,float(np.sqrt(weight@((K-K0)**2))))
            rows.append(dict(tau=tau,bar_impulse=float(weight@B),bar_torque=float(weight@(-np.sin(psi))),
                             physical_mean_change=float(weight@(j+a.s*tau-initial)),
                             budget_residual=float(weight@residual),weighted_hamiltonian_rms=float(np.sqrt(weight@((K-K0)**2))),
                             mass=float(weight.sum()),negative_mass=0.))
        if step in snap:
            h,_,_=np.histogram2d(np.mod(psi,2*np.pi),j,bins=[np.linspace(0,2*np.pi,65),np.linspace(-16,16,257)],weights=weight)
            density.append(h/((2*np.pi/64)*(32/256)));times.append(tau)
        if step==steps:break
        advance(psi,j,B,a.s,dt)
    np.savez_compressed(a.out/'recorded.npz',times=np.array(times),density=np.array(density),
                         phi=(np.arange(64)+.5)*2*np.pi/64,j=-16+(np.arange(256)+.5)*32/256)
    result=dict(config={k:v for k,v in vars(a).items() if k!='out'},history=rows,
                gates=dict(positive_mass=True,physical_moment=maxbudget<1e-8,analytical_identities=analytical<1e-10),
                maximum_budget_residual=maxbudget,maximum_weighted_hamiltonian_rms=maxH,analytical_identity_error=analytical,
                initial_truncated_mass=initial_mass,dt=dt,steps=steps,cpu_seconds=time.process_time()-cpu,
                wall_seconds=time.monotonic()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                raw_sha256=hashlib.sha256((a.out/'recorded.npz').read_bytes()).hexdigest(),
                scope='Positive collisionless Liouville quadrature. Gaussian weights retained; independent quadrature/domain/timestep checks are still required. Display density is a weighted histogram in the stated local window, without renormalizing omitted mass.')
    result['all_pass']=all(result['gates'].values())
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');(a.out/'COMPLETE').write_text('Finite characteristic quadrature; inspect refinements.\n')
    print(json.dumps({k:v for k,v in result.items() if k!='history'},indent=2))


if __name__=='__main__':main()
