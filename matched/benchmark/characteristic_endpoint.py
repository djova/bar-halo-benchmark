"""Same positive characteristic integral in cache-sized initial-angle blocks."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import argparse,hashlib,json,time
import numpy as np
from characteristics import advance,identities,SLOPE

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--s',required=True,type=float);p.add_argument('--slope',type=float,default=SLOPE);p.add_argument('--end',type=float,default=20);p.add_argument('--dt',type=float,default=.025);p.add_argument('--J',type=float,default=64);p.add_argument('--nphi',type=int,default=512);p.add_argument('--nj',type=int,default=8192);p.add_argument('--chunk',type=int,default=32);a=p.parse_args();a.out.mkdir(exist_ok=False,parents=True);start,cpu=time.monotonic(),time.process_time()
 error=identities();assert error<1e-10;steps=int(np.ceil(a.end/a.dt));dt=a.end/steps;dx=2*a.J/a.nj;j0=-a.J+(np.arange(a.nj)+.5)*dx;w=np.exp(-.5*((j0-a.slope*64)/8)**2)*dx/(8*np.sqrt(2*np.pi));mass=float(w.sum());w/=mass;rows=[]
 for begin in range(0,a.nphi,a.chunk):
  stop=min(begin+a.chunk,a.nphi);angles=(np.arange(begin,stop)+.5)*2*np.pi/a.nphi;psi,j=np.meshgrid(angles,j0,indexing='ij');psi=psi.ravel();j=j.ravel();weight=np.tile(w,stop-begin)/a.nphi;initial=j.copy();B=np.zeros_like(j);K0=-j*j/2-np.cos(psi)+a.s*psi
  for _ in range(steps):advance(psi,j,B,a.s,dt)
  residual=j+a.s*a.end-initial-B;K=-j*j/2-np.cos(psi)+a.s*psi
  rows.append(dict(begin=begin,stop=stop,mass=float(weight.sum()),bar_impulse=float(weight@B),physical_change=float(weight@(j+a.s*a.end-initial)),max_budget=float(abs(residual).max()),hamiltonian_mean_square=float(weight@((K-K0)**2))))
 B=sum(v['bar_impulse'] for v in rows);physical=sum(v['physical_change'] for v in rows);budget=max(v['max_budget'] for v in rows);gates=dict(positive_mass=bool(np.all(w>=0)),normalization=abs(sum(v['mass'] for v in rows)-1)<1e-12,physical_moment=budget<1e-8,analytical_identities=error<1e-10)
 result=dict(config={k:v for k,v in vars(a).items() if k!='out'},chunks=rows,history=[dict(tau=a.end,bar_impulse=B,physical_mean_change=physical,budget_residual=physical-B,weighted_hamiltonian_rms=float(np.sqrt(sum(v['hamiltonian_mean_square'] for v in rows))))],gates=gates,all_pass=all(gates.values()),maximum_budget_residual=budget,initial_truncated_mass=mass,dt=dt,steps=steps,cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('characteristics.py')]},scope='Endpoint only: same unmodified positive Gaussian quadrature and fourth-order flow, summed over disjoint initial-angle blocks; no intermediate frames computed.')
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'COMPLETE').write_text('Endpoint quadrature complete; inspect separate convergence.\n');print(json.dumps({k:v for k,v in result.items() if k!='chunks'},indent=2))
if __name__=='__main__':main()
