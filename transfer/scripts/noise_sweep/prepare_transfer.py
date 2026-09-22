"""Unforced coefficients, competing Fourier harmonics and domain for fixed tests."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import argparse,json,sys,hashlib,time
import numpy as np
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'vendor/Agama'))


def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--agama-path',type=Path,default=Path('vendor/Agama'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False);start,cpu=time.monotonic(),time.process_time()
 sys.path.insert(0,str((ROOT/a.agama_path).resolve()));import agama
 from coefficients import exact,angles
 pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5);am=agama.ActionMapper(pot);af=agama.ActionFinder(pot);df=agama.DistributionFunction(type='QuasiSpherical',density=pot,potential=pot);cases=[];maxmap=maxfreq=0.
 for label,jr in [('A',.05),('B',.08)]:
  def measure(js,n,spectrum=False):
   nonlocal maxmap,maxfreq
   act=np.array([jr,.05,2*js]);phase=angles(n);z=am(np.column_stack((np.tile(act,(len(phase),1)),phase)));found,aa,fr=af(z,angles=True,frequencies=True);E,freq,aa=exact(*act)
   maxmap=max(maxmap,float(np.max(abs(found-act))));maxfreq=max(maxfreq,float(np.max(abs(fr-freq))))
   x,y=z[:,0],z[:,1];r=np.linalg.norm(z[:,:3],axis=1);phi=-.0002*.42**2/(2*.34**2)*(1.28/(.28+r/.34))**5*(x*x-y*y);C=np.mean(phi*np.exp(-2j*phase[:,2]))
   plus,minus=act.copy(),act.copy();plus[2]+=2e-5;minus[2]-=2e-5;slope=float((np.log(df(plus))-np.log(df(minus)))/(2e-5))
   row=dict(Js=float(js),n=n,a=float(aa),b=float(2*abs(C)),phase=float(np.angle(C)),omega=float(freq[2]),df=float(df(act)),dlogf_dJs=slope)
   if spectrum:
    harmonics=[]
    for nr in range(-4,5):
     for nz in range(-4,5):
      k=np.array([nr,nz,2]);c=np.mean(phi*np.exp(-1j*(phase@k)));harmonics.append(dict(k=k.tolist(),b=float(2*abs(c)),detuning=float(k@freq-2*freq[2])))
    row['harmonics']=sorted(harmonics,key=lambda h:-h['b'])[:15]
   return row
  central=[measure(.25,n,n==32) for n in (16,32,64)];ref=central[-1];u=np.sqrt(abs(ref['b']/ref['a']));tu=1/np.sqrt(abs(ref['a']*ref['b']));scan=[measure(.25+j*u,32) for j in np.arange(-64,65,2)]
  cases.append(dict(label=label,actions=[jr,.05,.5],amplitude=.0002,s=.25,eta=.1,T=20,sigma=8,reference=ref,central=central,scan=scan,action_unit=float(u),time_unit=float(tu),dimensionless_slope=float(u*ref['dlogf_dJs']),physical_sweep_speed=float(.25*ref['b']),physical_diffusion=float((2*.1/np.pi)*u*u/tu),coupling_quadrature_relative_change=float(central[1]['b']/ref['b']-1)))
 gates=dict(map=maxmap<1e-10,frequency=maxfreq<1e-10,coupling=all(abs(c['coupling_quadrature_relative_change'])<.001 for c in cases))
 result=dict(cases=cases,gates=gates,all_pass=all(gates.values()),max_map_error=maxmap,max_frequency_error=maxfreq,cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),agama_library_sha256=hashlib.sha256(Path(agama.__file__).read_bytes()).hexdigest(),scope='Unforced preparation only; no held-out 3D response observed.')
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'COMPLETE').write_text('Unforced preparation complete.\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
