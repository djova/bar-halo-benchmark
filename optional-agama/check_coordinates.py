"""Original versus isolated half-angle algebra, with 80-digit mapping reference."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import argparse,hashlib,json,sys,time
import numpy as np
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]

def high_precision(actions,angles):
 mp.mp.dps=80;jr,jz,jp=map(lambda x:mp.mpf(float(x)),actions);tr,tz,tp=map(lambda x:mp.mpf(float(x)),angles)
 L=jz+abs(jp);L1=mp.sqrt(L*L+2);I=jr+(L+L1)/2;e=mp.sqrt(jr*(jr+L)*(jr+L1)*(jr+L+L1))/I**2
 eta=mp.findroot(lambda x:x-e*mp.sin(x)-tr,tr);sn,cs=mp.sin(eta),mp.cos(eta)
 f1=(1+e-mp.mpf('.5')/I**2)*I/L;f2=(1+e+mp.mpf('.5')/I**2)*I/L1
 radial=tr-(2*mp.pi if eta>mp.pi else 0);psi=tz-(1+L/L1)*radial/2+mp.atan(f1*mp.tan(eta/2))+(L/L1)*mp.atan(f2*mp.tan(eta/2))
 chi=mp.atan2(abs(jp)*mp.sin(psi),L*mp.cos(psi));ct=mp.sqrt(1-(jp/L)**2)*mp.sin(psi);st=mp.sqrt(1-ct*ct);r=mp.sqrt(((1-e*cs)*I**2)**2-mp.mpf('.25'))
 vr=I*e*sn/r;vt=-L*mp.sqrt(1-(jp/L)**2)*mp.cos(psi)/(r*st);R=r*st;z=r*ct;phi=tp+(chi-tz)*mp.sign(jp);vR=vr*st+vt*ct;vz=vr*ct-vt*st;vp=jp/R
 return np.array(list(map(float,[R*mp.cos(phi),R*mp.sin(phi),z,vR*mp.cos(phi)-vp*mp.sin(phi),vR*mp.sin(phi)+vp*mp.cos(phi),vz])))

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--library',required=True,type=Path);a=p.parse_args();a.out.mkdir(exist_ok=False,parents=True);start,cpu=time.monotonic(),time.process_time();sys.path.insert(0,str(a.library.resolve()));import agama
 pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5);am=agama.ActionMapper(pot);af=agama.ActionFinder(pot);rng=np.random.default_rng(8193);random=rng.uniform(0,2*np.pi,(4096,3));critical=[]
 for centre in (0.,np.pi,2*np.pi):
  for d in [0.,*sum(([10.**-k,-10.**-k] for k in range(2,13)),[])]:critical.append([np.mod(centre+d,2*np.pi),.93,1.37])
 phase=np.vstack((random,critical));actions=np.tile([.03,.02,.5],(len(phase),1));z=am(np.column_stack((actions,phase)));ac,an,freq=af(z,angles=True,frequencies=True);back=am(np.column_stack((ac,an)));angle=abs(np.angle(np.exp(1j*(an-phase))));high=np.array([high_precision(act,ang) for act,ang in zip(actions[4096:],phase[4096:])]);err=abs(z[4096:]-high)
 I=.03+(.52+np.sqrt(.52**2+2))/2;f=np.array([1,(1+.52/np.sqrt(.52**2+2))/2,(1+.52/np.sqrt(.52**2+2))/2])/I**3
 result=dict(max_action_error=float(abs(ac-actions).max()),max_frequency_error=float(abs(freq-f).max()),max_angle_error=float(angle.max()),max_cartesian_roundtrip=float(abs(z-back).max()),max_high_precision_error=float(err.max()),uniform_max_angle_error=float(angle[:4096].max()),critical=[dict(radial_angle=float(phase[4096+i,0]),angle_error=angle[4096+i].tolist(),state_error=float(err[i].max())) for i in range(len(critical))],cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,library_sha256=hashlib.sha256(Path(agama.__file__).read_bytes()).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Exact analytic coordinate test. Critical phases are numerical probes, not a physical orbit ensemble.')
 result['gates']=dict(actions=result['max_action_error']<1e-10,frequency=result['max_frequency_error']<1e-10,angles=result['max_angle_error']<1e-10,cartesian=result['max_cartesian_roundtrip']<1e-10,high_precision=result['max_high_precision_error']<1e-10);result['all_pass']=all(result['gates'].values());np.savez_compressed(a.out/'recorded.npz',states=z,phases=phase,angles=an,actions=ac,frequencies=freq,high_precision=high)
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'COMPLETE').write_text('Coordinate diagnostic complete.\n');print(json.dumps({k:v for k,v in result.items() if k!='critical'},indent=2))
if __name__=='__main__':main()
