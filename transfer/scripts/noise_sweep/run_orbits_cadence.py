"""Post-outcome nested-cadence diagnostic with unchanged canonical Js Brownian noise."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import argparse,hashlib,json,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'benchmark'));sys.path.insert(0,str(ROOT/'vendor/Agama'))
from orbit_fourth import Kernel
from brownian_leaves import increments as brownian_increments
from characteristics import advance as reduced_advance

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--agama-path',type=Path,default=Path('vendor/Agama'));p.add_argument('--pilot',action='store_true');p.add_argument('--pilot-end',type=float,choices=[40.,12720.],default=40.);p.add_argument('--forecast',type=Path);p.add_argument('--case',choices=['A','B'],default='A');p.add_argument('--seed',type=int,required=True);p.add_argument('--n',type=int,default=4096);p.add_argument('--start',type=int,default=0);p.add_argument('--dt',type=float,default=.01);p.add_argument('--noise-refine',type=int,choices=[1,2,4,8],default=1);p.add_argument('--no-noise',action='store_true');p.add_argument('--no-bar',action='store_true');a=p.parse_args()
 sys.path.insert(0,str((ROOT/a.agama_path).resolve()));import agama
 if a.pilot:
  assert a.seed==8192
  config=dict(jr=.03,jz=.02,js0=.25,width=.004,mean=.25,amplitude=.002,speed=0.,D=1e-8,end=a.pilot_end,time_unit=1.,action_unit=1.)
 else:
  if a.forecast is None:raise ValueError('A frozen magnitude forecast is required before new-condition 3D orbits')
  forecast=json.loads(a.forecast.read_text());selected=next(c for c in forecast['cases'] if c['label']==a.case);config=selected['orbit_config']
  assert forecast['frozen_before_3d'] and selected['qualified']
  assert a.seed=={'A':8301,'B':8302}[a.case]
 a.out.mkdir(parents=True,exist_ok=False);start,cpu=time.monotonic(),time.process_time();n=a.n
 pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5);am=agama.ActionMapper(pot);af=agama.ActionFinder(pot);kernel=Kernel(ROOT/'build/noise-sweep/orbit-fourth.so')
 js=np.random.default_rng(np.random.SeedSequence([a.seed,0])).normal(config['mean'],config['width'],a.start+n)[a.start:];angles=np.random.default_rng(np.random.SeedSequence([a.seed,1])).uniform(0,2*np.pi,(a.start+n,3))[a.start:];initial_actions=np.column_stack((np.full(n,config['jr']),np.full(n,config['jz']),2*js));initial_aa=np.column_stack((initial_actions,angles));z=np.ascontiguousarray(am(initial_aa));initial=z.copy();B=np.zeros(n);W=np.zeros(n);noiseL=np.zeros(n);noiseE=np.zeros(n);noiseJs=np.zeros(n)
 pvec=np.array([0. if a.no_bar else config['amplitude'],config['jr'],config['jz'],config['js0'],config['speed']]);D=0. if a.no_noise else config['D'];end=config['end'];blocks=int(np.ceil(end/2));h=end/blocks
 initialL=np.cross(z[:,:3],z[:,3:])[:,2];initialE=.5*np.sum(z[:,3:]**2,axis=1)+kernel.evaluate(z,0.,pvec)[:,0]
 maxround=maxfastkick=maxkickL=maxanglekick=0.;maxbudget=0.;rows=[];snap=[];times=[]
 redj=(js-config['js0'])/config['action_unit'];redinitial=redj.copy();redpsi=2*angles[:,2].copy();redB=np.zeros(n);rednoise=np.zeros(n);reds=config['speed']*config['time_unit']/config['action_unit'];maxredbudget=0.
 save=set(np.rint(np.linspace(0,blocks,min(201,blocks+1))).astype(int));maxwork=0.
 fast_times=[];fast_paths=[];fast_events=[]
 windows=[(0.,min(40.,end)),(max(0.,end/2-20),min(end,end/2+20)),(max(0.,end-40),end)]
 def in_window(t):return any(lo-1e-10<=t<=hi+1e-10 for lo,hi in windows)
 def capture(t,event):
  if in_window(t):
   ac,an,_=af(z[:64],angles=True,frequencies=True);fast_times.append(t);fast_events.append(event);fast_paths.append(np.column_stack((z[:64],ac,an,B[:64],noiseL[:64])))
 def drift(t0,steps,dt):
  if not any(t0<=hi and t0+steps*dt>=lo for lo,hi in windows):
   kernel.evolve(z,steps,t0,dt,pvec,B,W);return
  capture(t0,0);stride=max(1,int(round(.2/dt)))
  for begin in range(0,steps,stride):
   count=min(stride,steps-begin);kernel.evolve(z,count,t0+begin*dt,dt,pvec,B,W);capture(t0+(begin+count)*dt,0)
 def record(t):
  nonlocal maxbudget,maxwork,maxredbudget
  L=np.cross(z[:,:3],z[:,3:])[:,2];E=.5*np.sum(z[:,3:]**2,axis=1)+kernel.evaluate(z,t,pvec)[:,0];res=L-initialL-B-noiseL;er=E-initialE-W-noiseE;ac,an,fr=af(z,angles=True,frequencies=True)
  maxbudget=max(maxbudget,float(abs(res).max()));maxwork=max(maxwork,float(abs(er).max()))
  rows.append(dict(time=t,tau=t/config['time_unit'],bar_impulse=float(B.mean()),bar_impulse_se=float(B.std(ddof=1)/np.sqrt(n)),noise_Lz=float(noiseL.mean()),noise_Js=float(noiseJs.mean()),noise_Js_variance=float(noiseJs.var(ddof=1)),work_residual_mean=float(er.mean()),work_residual_rms=float(np.sqrt(np.mean(er*er))),max_torque_budget=float(abs(res).max()),fast_action_rms=np.sqrt(np.mean((ac[:,:2]-initial_actions[:,:2])**2,axis=0)).tolist(),fast_action_max=float(abs(ac[:,:2]-initial_actions[:,:2]).max()),retrograde_fraction=float(np.mean(ac[:,2]<0))))
  redres=redj+reds*t/config['time_unit']-redinitial-redB-rednoise;maxredbudget=max(maxredbudget,float(abs(redres).max()));rows[-1]['reduced_bar_Lz']=float(2*config['action_unit']*redB.mean());rows[-1]['paired_bar_discrepancy']=float(np.mean(B-2*config['action_unit']*redB));rows[-1]['reduced_budget']=float(abs(redres).max())
  snap.append(np.column_stack((z[:64],ac[:64],an[:64],B[:64],noiseL[:64])));times.append(t)
 for block in range(blocks+1):
  if block in save:record(block*h)
  if block==blocks:break
  increments=brownian_increments(a.seed,block,n,a.start,D,h,a.noise_refine)
  for k,increment in enumerate(increments):
   length=h/a.noise_refine;t0=block*h+k*length;steps=int(np.ceil(length/2/a.dt));dt=length/(2*steps)
   drift(t0,steps,dt)
   reduced_advance(redpsi,redj,redB,reds,length/(2*config['time_unit']),not a.no_bar)
   if D:
    tm=t0+length/2;ac,an,_=af(z,angles=True,frequencies=True)
    if not np.isfinite(ac).all():raise RuntimeError('Invalid or unbound action before stochastic kick')
    capture(tm,1)
    beforeL=np.cross(z[:,:3],z[:,3:])[:,2];beforeE=.5*np.sum(z[:,3:]**2,axis=1)+kernel.evaluate(z,tm,pvec)[:,0]
    # Gauge identity and fast-action preservation are checked on the actual mapped state.
    if block<2:maxround=max(maxround,float(abs(am(np.column_stack((ac,an)))-z).max()))
    target=ac.copy();target[:,2]+=2*increment
    if (target[:,2]<=0).any():raise RuntimeError('Action noise left declared prograde canonical chart')
    z[:]=am(np.column_stack((target,an)));afterL=np.cross(z[:,:3],z[:,3:])[:,2];afterE=.5*np.sum(z[:,3:]**2,axis=1)+kernel.evaluate(z,tm,pvec)[:,0]
    actual,afterangles,_=af(z,angles=True,frequencies=True);maxanglekick=max(maxanglekick,float(abs(np.angle(np.exp(1j*(afterangles-an)))).max()));maxfastkick=max(maxfastkick,float(abs(actual[:,:2]-ac[:,:2]).max()));maxkickL=max(maxkickL,float(abs(afterL-beforeL-2*increment).max()))
    noiseL+=afterL-beforeL;noiseE+=afterE-beforeE;noiseJs+=increment;capture(tm,2)
   redj+=increment/config['action_unit'];rednoise+=increment/config['action_unit']
   drift(t0+length/2,steps,dt)
   reduced_advance(redpsi,redj,redB,reds,length/(2*config['time_unit']),not a.no_bar)
 np.savez_compressed(a.out/'recorded.npz',fast_times=np.array(fast_times),fast_paths=np.array(fast_paths),fast_events=np.array(fast_events),particle_ids=np.arange(a.start,a.start+n),initial_actions_angles=initial_aa,final_reduced_bar_Lz=2*config['action_unit']*redB,initial_cartesian=initial,times=np.array(times),paths=np.array(snap),final_bar_Lz=B,final_noise_Lz=noiseL,final_noise_energy=noiseE,final_work=W,final_cartesian=z,final_noise_Js=noiseJs)
 gates=dict(reduced_budget=maxredbudget<1e-9,torque_budget=maxbudget<1e-9,noise_Lz=maxkickL<1e-10,noise_fast_actions=maxfastkick<1e-10,noise_angles=maxanglekick<1e-10,roundtrip=maxround<1e-10)
 if a.no_bar:
  expected=2*D*end;variance=float(noiseJs.var(ddof=1));se=expected*np.sqrt(2/(n-1))
  gates.update(unforced_bar=bool(np.max(abs(B))<1e-12),unforced_fast_actions=rows[-1]['fast_action_max']<5e-6,noise_variance=abs(variance-expected)<5*se if D else variance==0)
 result=dict(config=config,settings={k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items() if k!='out'},history=rows,gates=gates,all_pass=all(gates.values()),maximum_work_residual=maxwork,maximum_torque_residual=maxbudget,maximum_noise_Lz_error=maxkickL,maximum_kick_angle_error=maxanglekick,maximum_kick_fast_action_error=maxfastkick,maximum_roundtrip_error=maxround,cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,source_sha256={str(q):sha(ROOT/q) for q in ['scripts/noise_sweep/run_orbits_cadence.py','benchmark/brownian_leaves.py','benchmark/orbit_fourth.cpp','benchmark/orbit_fourth.py','benchmark/orbit_kernel.cpp','benchmark/orbit_kernel.py']},library_sha256=sha(ROOT/'build/noise-sweep/orbit-fourth.so'),agama_library_sha256=sha(agama.__file__),forecast_sha256=sha(a.forecast) if a.forecast else None,raw_sha256=sha(a.out/'recorded.npz'),fast_recording_windows=windows,fast_event_codes={'0':'deterministic integration state','1':'before canonical kick','2':'after canonical kick'},fast_recording_scope='Actual integrator states of fixed first64particleIDs at <=approximately0.2physical time in three40timeunit windows. Coarse whole-run positions are not an orbit-resolved movie.',random_stream_scheme='PCG64 SeedSequence [seed,0] for Js, [seed,1] for N-by-3 angles, [seed,2,base_block] for N-by-2 noise leaves; stable particle-ID prefixes and extensions. Finer bridges use [seed,3,base_block,level] with N-by-parentcount Gaussians; each parent splits as parent/2 plus or minus an independent bridge.',reduced_path_scope='Diagnostic integrator only for pilot; fixed independently calibrated slow Hamiltonian for a forecast case.',scope='Full 3D prescribed isochrone+bar; imposed canonical action noise changes position and velocity, external non-conserving bath; not physical scattering or a live halo.')
 gates={k:bool(v) for k,v in gates.items()};result['gates']=gates
 (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');(a.out/'COMPLETE').write_text('Finite 3D evolution complete; inspect scientific gates.\n');print(json.dumps({k:v for k,v in result.items() if k!='history'},indent=2))
if __name__=='__main__':main()
