"""Test the proposed identity on a known compact polynomial and fixed kick maps."""
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import argparse,hashlib,json,math,time
import numpy as np


def profile(x,c=5.):
    return np.maximum(1-(x/c)**2,0)**8


def primitive(x,c=5.):
    z=np.clip(x/c,-1.,1.)
    co=np.zeros(18)
    for k in range(9):
        co[2*k+1]=(-1)**k*math.comb(8,k)/(2*k+1)
    # The additive constant is immaterial to every difference.
    return c*np.polynomial.polynomial.polyval(z,co)


def probe(nj,nphi,noise):
    J=16.;dt=.025;steps=80;s=.25;dx=2*J/nj
    x=-J+(np.arange(nj)+.5)*dx
    psi,j=np.meshgrid((np.arange(nphi)+.5)*2*np.pi/nphi,x,indexing='ij')
    x0=j.copy();B=np.zeros_like(j);W=0.
    kicks=np.random.default_rng(94300).normal(size=steps)*.04 if noise else np.zeros(steps)
    for q in kicks:
        psi-=j*dt/2
        b=-np.sin(psi)*dt
        j+=b-s*dt+q;B+=b;W+=q
        psi-=j*dt/2
    w=profile(x0)
    control=primitive(x0+B)-primitive(x0)
    remainder=control-w*B
    factor=dx/nphi
    raw=float(np.sum(w*B)*factor)
    alternative=float(-np.sum(remainder)*factor)
    return dict(raw=raw,remainder=alternative,control_integral=float(control.sum()*factor),
        difference=alternative-raw,
        budget=float(abs(j+s*steps*dt-x0-B-W).max()),
        maximum_bar_impulse=float(abs(B).max()))


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    start,cpu=time.monotonic(),time.process_time()
    cases={}
    for noisy in [False,True]:
        for name,nj,nphi in [('coarse',512,64),('fine',1024,128)]:
            cases[f'{noisy}-{name}']=probe(nj,nphi,noisy)
    gates={key:abs(r['control_integral'])<1e-10 and r['budget']<1e-10 and r['maximum_bar_impulse']<=2+1e-12 for key,r in cases.items()}
    x=np.linspace(-4.9,4.9,201);h=1e-4
    numerical=(primitive(x-2*h)-8*primitive(x-h)+8*primitive(x+h)-primitive(x+2*h))/(12*h)
    derivative_error=float(abs(numerical-profile(x)).max())
    gates['known_primitive_derivative']=derivative_error<1e-9
    r=dict(cases=cases,gates=gates,all_pass=all(gates.values()),derivative_error=derivative_error,
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        scope='Two finite prescribed common kick histories and a known positive compact polynomial. Tests the derived integral identity, not halo torque or independent stochastic precision. No physical parameters or acceptance limits are fit to an outcome.')
    (a.out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
    return 0 if r['all_pass'] else 2


if __name__=='__main__':
    raise SystemExit(main())
