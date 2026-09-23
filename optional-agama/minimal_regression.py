"""Four fixed turning-phase probes with independent 80-digit coordinates.

AGAMA: Eugene Vasiliev and contributors. This diagnostic does not redistribute
AGAMA or its binary. Invoke separately for original and patched library paths.
"""
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import argparse,hashlib,json,platform,subprocess,sys,time
import numpy as np
import mpmath as mp

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
 p=argparse.ArgumentParser();p.add_argument('--library',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 a.out.mkdir(parents=True,exist_ok=False);start=time.process_time();sys.path.insert(0,str(a.library.resolve()));import agama
 pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5)
 mapper=agama.ActionMapper(pot);finder=agama.ActionFinder(pot)
 phases=np.array([[0.,.93,1.37],[1e-8,.93,1.37],[np.pi-1e-8,.93,1.37],[np.pi+1e-8,.93,1.37]])
 actions=np.tile([.03,.02,.5],(len(phases),1));states=mapper(np.column_stack((actions,phases)))
 got_actions,got_angles,got_freq=finder(states,angles=True,frequencies=True)
 back=mapper(np.column_stack((got_actions,got_angles)))
 reference=np.array([high_precision(act,phase) for act,phase in zip(actions,phases)])
 angle_error=abs(np.angle(np.exp(1j*(got_angles-phases))))
 results=[]
 for i in range(len(phases)):
  results.append(dict(actions=actions[i].tolist(),angles=phases[i].tolist(),state=states[i].tolist(),reference_state=reference[i].tolist(),recovered_angles=got_angles[i].tolist(),angle_error=angle_error[i].tolist(),coordinate_error=float(abs(states[i]-reference[i]).max()),roundtrip_error=float(abs(states[i]-back[i]).max()),action_error=float(abs(actions[i]-got_actions[i]).max())))
 gates=dict(angles=bool(angle_error.max()<1e-10),coordinates=bool(abs(states-reference).max()<1e-10),roundtrip=bool(abs(states-back).max()<1e-10),actions=bool(abs(actions-got_actions).max()<1e-10))
 def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
 r=dict(cases=results,gates=gates,all_pass=all(gates.values()),library_sha256=sha(agama.__file__),source_sha256=sha(__file__),source_revision=subprocess.check_output(['git','-C',str(a.library),'rev-parse','HEAD'],text=True).strip(),python=platform.python_version(),numpy=np.__version__,mpmath=mp.__version__,cpu_seconds=time.process_time()-start,scope='Four deliberately difficult nondegenerate isochrone turning phases. These probes establish a numerical issue at these inputs, not its frequency in a galaxy or a universal action-mapper error bound. Completion with failed gates is retained for the unchanged library.')
 (a.out/'result.json').write_text(json.dumps(r,indent=2)+'\n');(a.out/'COMPLETE').write_text('Coordinate probes complete; inspect gates.\n');print(json.dumps(r,indent=2))

if __name__=='__main__':main()
