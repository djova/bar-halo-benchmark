"""Positive-population moving resonance: independent distribution and path solvers.

Dimensionless a=-1, b=1. Physical Js is u*(j+s*tau), Lz=2 Js.
This module needs only NumPy and can run outside the original project.
"""
import os
os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import argparse,hashlib,json,time
import numpy as np

SLOPE=-0.016531804196572842


def endpoint(s):return min(8*np.pi,8/s) if s else 8*np.pi


def distribution(s,eta,bar=True,nphi=128,nj=2048,J=64.,dtmax=.025,end=None,slope=SLOPE):
    end=endpoint(s) if end is None else end;steps=int(np.ceil(end/dtmax));dt=end/steps
    dx=2*J/nj;dp=2*np.pi/nphi
    j=-J+(np.arange(nj)+.5)*dx;phi=(np.arange(nphi)+.5)*dp
    f=np.broadcast_to(np.exp(-.5*((j-slope*64)/8)**2)/(8*np.sqrt(2*np.pi)*2*np.pi),(nphi,nj)).copy()
    initial_mass=f.sum()*dx*dp;f/=initial_mass
    kphi=np.fft.fftfreq(nphi,1/nphi)[:,None];kj=(2*np.pi*np.fft.fftfreq(nj,dx))[None,:]
    angle=np.exp(1j*kphi*j[None,:]*dt/2)
    force=-np.sin(phi)[:,None]*(1 if bar else 0);v=force-s;D=eta*2/np.pi
    q=-1j*v*kj-D*kj**2;action=np.exp(q*dt)
    integral=np.full_like(q,dt);np.divide(np.expm1(q*dt),q,out=integral,where=abs(q)>1e-14)
    # Left physical face is half a cell before the first stored cell centre.
    boundary_kernel=(v-1j*D*kj)*np.exp(-1j*kj*dx/2)*integral/nj
    B=0.;boundary=0.;initial_j=float((f*j).sum()*dx*dp)
    save=set(np.rint(np.linspace(0,steps,201)).astype(int));snap=set(np.rint(np.linspace(0,steps,21)).astype(int))
    rows=[];density=[];times=[];mass_error=negative=budget=0.
    for step in range(steps+1):
        t=step*dt
        if step in save:
            mass=float(f.sum()*dx*dp);mean=float((f*j).sum()*dx*dp);var=float((f*(j-mean)**2).sum()*dx*dp)
            torque=float((f*force).sum()*dx*dp);res=mean+s*t-initial_j-B-boundary
            mass_error=max(mass_error,abs(mass-1));negative=max(negative,float(-np.minimum(f,0).sum()*dx*dp));budget=max(budget,abs(res))
            rows.append(dict(tau=t,bar_impulse=B,bar_torque=torque,physical_mean_change=mean+s*t-initial_j,
                             boundary_moment=boundary,budget_residual=res,variance=var,mass=mass,negative_mass=negative))
        if step in snap:
            density.append(f[::max(1,nphi//64),::max(1,nj//512)].copy());times.append(t)
        if step==steps:break
        f=np.fft.ifft(np.fft.fft(f,axis=0)*angle,axis=0).real
        B+=dt*float((f*force).sum()*dx*dp)
        F=np.fft.fft(f,axis=1)
        boundary+=float(-2*J*dp*np.sum(F*boundary_kernel).real)
        f=np.fft.ifft(F*action,axis=1).real
        f=np.fft.ifft(np.fft.fft(f,axis=0)*angle,axis=0).real
    gates=dict(mass=mass_error<1e-10,positive_mass=negative<1e-10,moment_budget=budget<1e-7)
    if not bar:
        gates.update(unforced_mean=abs(rows[-1]['physical_mean_change'])<1e-7,
                     unforced_variance=abs(rows[-1]['variance']-(64+2*D*end))<1e-7)
    return dict(history=rows,gates=gates,all_pass=all(gates.values()),maximum_mass_error=mass_error,
                maximum_negative_mass=negative,maximum_budget_residual=budget,
                initial_truncated_mass=initial_mass,dt=dt,steps=steps),dict(
                times=np.array(times),phi=phi[::max(1,nphi//64)],j=j[::max(1,nj//512)],density=np.array(density))


def trajectories(s,eta,seed,n=32768,bar=True,dtmax=.025,end=None,slope=SLOPE):
    end=endpoint(s) if end is None else end;steps=int(np.ceil(end/dtmax));dt=end/steps
    rng=np.random.default_rng(seed);j=rng.normal(slope*64,8,n);psi=rng.uniform(-np.pi,np.pi,n);initial=j.copy()
    B=np.zeros(n);W=np.zeros(n);D=eta*2/np.pi
    save=set(np.rint(np.linspace(0,steps,201)).astype(int));rows=[];paths=[];times=[];maxbudget=0.
    for step in range(steps+1):
        t=step*dt
        if step in save:
            residual=j+s*t-initial-B-W;maxbudget=max(maxbudget,float(np.max(abs(residual))))
            rows.append(dict(tau=t,bar_impulse=float(B.mean()),bar_torque=float(np.mean(-np.sin(psi))) if bar else 0.,
                             stochastic_impulse=float(W.mean()),physical_mean_change=float(np.mean(j+s*t-initial)),
                             impulse_se=float(B.std(ddof=1)/np.sqrt(n)),variance=float(j.var()),budget_max=float(np.max(abs(residual)))))
            paths.append(np.stack((j[:64],psi[:64],B[:64],W[:64]),axis=1));times.append(t)
        if step==steps:break
        psi-=j*dt/2
        impulse=-np.sin(psi)*dt if bar else np.zeros(n)
        noise=np.sqrt(2*D*dt)*rng.normal(size=n) # Draw even for D=0: matched paths use the same stream.
        j+=impulse-s*dt+noise;B+=impulse;W+=noise
        psi-=j*dt/2
    return dict(history=rows,all_pass=maxbudget<1e-9,gates={'path_budget':maxbudget<1e-9},
                maximum_budget_residual=maxbudget,dt=dt,steps=steps),dict(
                times=np.array(times),paths=np.array(paths),final_impulse=B,final_j=j,initial_j=initial,final_stochastic=W)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--s',type=float,required=True);p.add_argument('--eta',type=float,required=True)
    p.add_argument('--method',choices=['distribution','trajectories'],default='distribution');p.add_argument('--no-bar',action='store_true')
    p.add_argument('--nphi',type=int,default=128);p.add_argument('--nj',type=int,default=2048);p.add_argument('--J',type=float,default=64.)
    p.add_argument('--dt',type=float,default=.025);p.add_argument('--end',type=float);p.add_argument('--seed',type=int,default=8201);p.add_argument('--n',type=int,default=32768);p.add_argument('--slope',type=float,default=SLOPE)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False);start,cpu=time.monotonic(),time.process_time()
    common=dict(s=a.s,eta=a.eta,bar=not a.no_bar,dtmax=a.dt,end=a.end,slope=a.slope)
    result,raw=distribution(**common,nphi=a.nphi,nj=a.nj,J=a.J) if a.method=='distribution' else trajectories(**common,seed=a.seed,n=a.n)
    np.savez_compressed(a.out/'recorded.npz',**raw)
    result.update(config={k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items() if k!='out'},
                  cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  raw_sha256=hashlib.sha256((a.out/'recorded.npz').read_bytes()).hexdigest(),
                  scope='Positive local tracer population; imposed white action noise and bar. Conditional finite-time torque, not physical SIDM or a self-gravitating halo.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (a.out/'COMPLETE').write_text('Finite evolution complete; inspect separate scientific gates.\n')
    print(json.dumps({k:v for k,v in result.items() if k!='history'},indent=2))


if __name__=='__main__':main()
