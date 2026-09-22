"""Unforced exact-isochrone coefficients and Fourier coupling; no forced orbits."""
import os
os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
import argparse,hashlib,json,sys,time
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'vendor/Agama'));import agama
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def exact(jr,jz,jphi,c=.5):
    L=jz+jphi;s=np.sqrt(L*L+4*c);I=jr+(L+s)/2
    h=(1+L/s)/2;hp=2*c/s**3
    return -1/(2*I*I),np.array([I**-3,h/I**3,h/I**3]),4*(hp/I**3-3*h*h/I**4)


def angles(n):
    v=(np.arange(n)+.5)*2*np.pi/n
    return np.stack(np.meshgrid(v,v,v,indexing='ij'),axis=-1).reshape(-1,3)


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    start,cpu=time.monotonic(),time.process_time()
    pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5);af=agama.ActionFinder(pot);am=agama.ActionMapper(pot)
    df=agama.DistributionFunction(type='QuasiSpherical',density=pot,potential=pot)
    rows=[];roundtrip=frequency=energy=0.
    for n in (16,32):
        phase=angles(n)
        for js in (np.linspace(.15,.35,41) if n==16 else [.25]):
            act=np.array([.05,.05,2*js]);aa=np.column_stack((np.tile(act,(len(phase),1)),phase));states=am(aa)
            ac,an,fr=af(states,angles=True,frequencies=True)
            E,freq,derivative=exact(*act)
            roundtrip=max(roundtrip,float(np.max(abs(ac-act))));frequency=max(frequency,float(np.max(abs(fr-freq))))
            r=np.linalg.norm(states[:,:3],axis=1)
            measuredE=.5*np.sum(states[:,3:]**2,axis=1)-1/(.5+np.sqrt(.25+r*r))
            energy=max(energy,float(np.max(abs(measuredE-E))))
            x,y=states[:,0],states[:,1]
            phi=-.42**2/(2*.34**2)*((1+.28)/(.28+r/.34))**5*(x*x-y*y)
            C=np.mean(phi*np.exp(-2j*phase[:,2]))
            plus,minus=act.copy(),act.copy();plus[2]+=2e-5;minus[2]-=2e-5
            f=float(df(act));slope=float((np.log(df(plus))-np.log(df(minus)))/(2e-5))
            rows.append(dict(n=n,Js=float(js),a=float(derivative),omega=float(freq[2]),
                             coupling_per_amplitude=float(2*abs(C)),phase=float(np.angle(C)),
                             df=f,dlogf_dJs=slope))
    ref=next(r for r in rows if r['n']==32);coarse=next(r for r in rows if r['n']==16 and abs(r['Js']-.25)<1e-8)
    scales=[]
    for amplitude in (.002,.0002):
        b=ref['coupling_per_amplitude']*amplitude;junit=np.sqrt(abs(b/ref['a']));tunit=1/np.sqrt(abs(b*ref['a']))
        scales.append(dict(amplitude=amplitude,b=b,action_unit=junit,separatrix_half_width=2*junit,
                           tlib=2*np.pi*tunit,dimensionless_log_slope=ref['dlogf_dJs']*junit,
                           domain_actions={str(j):[.25-j*junit,.25+j*junit] for j in (2,8,16)}))
    result=dict(background='Isochrone G=M=1,c=.5; differs from earlier Hernquist benchmark',
                actions=[.05,.05,.5],reference=ref,scan=rows,scales=scales,
                gates=dict(action_roundtrip=roundtrip<1e-10,frequency=frequency<1e-10,energy=energy<1e-10,
                           quadrature=abs(ref['coupling_per_amplitude']/coarse['coupling_per_amplitude']-1)<.01),
                maximum_errors=dict(action=roundtrip,frequency=frequency,energy=energy),
                quadrature_relative_difference=ref['coupling_per_amplitude']/coarse['coupling_per_amplitude']-1,
                cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
                source_sha256=sha(__file__),protocol_sha256=sha(ROOT/'research/noise-sweep/COEFFICIENT_PILOT.md'),
                scope='Unforced coefficient and coordinate pilot. No bar response or prediction measured.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='scan'},indent=2))


if __name__=='__main__':main()
