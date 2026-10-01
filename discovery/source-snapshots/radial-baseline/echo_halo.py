"""Exact-background 3D tracer screen with spatial gravitational impulses."""
import os
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
from pathlib import Path
import argparse, datetime, hashlib, json, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import sph_harm_y, ndtr
ROOT=Path(__file__).resolve().parents[2]
DEFAULT_AGAMA=ROOT/'build/noise-sweep/Agama-stable-v2'
AGAMA_LIBRARY=Path(os.environ.get('ECHO_AGAMA_LIBRARY',str(DEFAULT_AGAMA if DEFAULT_AGAMA.exists() else ROOT/'vendor/Agama')))
sys.path.insert(0,str(AGAMA_LIBRARY))
import agama

def sph_harm(m,ell,phi,theta):return sph_harm_y(ell,m,theta,phi)

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(path,value):path.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')

def potential_energy(xv):
    r2=np.sum(xv[:,:3]**2,axis=1)
    return .5*np.sum(xv[:,3:]**2,axis=1)-1/(.5+np.sqrt(.25+r2))

def pulse(x,amplitude,scale,phi):
    c,s=np.cos(2*phi),np.sin(2*phi)
    q=(x[:,0]**2-x[:,1]**2)*c+2*x[:,0]*x[:,1]*s
    gradq=np.column_stack((2*x[:,0]*c+2*x[:,1]*s,2*x[:,0]*s-2*x[:,1]*c,np.zeros(len(x))))
    u=1+np.sum(x*x,axis=1)/scale**2
    f=u**-2.5/scale**2
    potential=amplitude*q*f
    grad=amplitude*(f[:,None]*gradq-5*(q*f/u/scale**2)[:,None]*x)
    return potential,-grad

def coordinates(am,actions,angles,frequencies,elapsed):
    return am(np.column_stack((actions,np.remainder(angles+frequencies*elapsed,2*np.pi))))

def symmetry_sample(pot,nbase,seed):
    agama.setRandomSeed(seed)
    df=agama.DistributionFunction(type='QuasiSpherical',density=pot,potential=pot)
    base,mass=agama.GalaxyModel(pot,df).sample(nbase)
    # Each independent sampled particle gets eight azimuthal rotations. Error bars
    # must use nbase independent units, never count rotations as new samples.
    xv=np.repeat(base,8,axis=0)
    angle=np.tile(np.arange(8)*2*np.pi/8,nbase)
    for offset in (0,3):
        x,y=xv[:,offset].copy(),xv[:,offset+1].copy()
        xv[:,offset]=np.cos(angle)*x-np.sin(angle)*y
        xv[:,offset+1]=np.sin(angle)*x+np.cos(angle)*y
    return xv,np.repeat(mass/8,8),base

def annulus_kernel(r,radius,ell,width):
    if width==0:return np.minimum(r,radius)**ell/np.maximum(r,radius)**(ell+1)
    # Exact Newtonian radial kernel averaged over log R'~N(log R,width^2).
    # E[R'^a 1(R'<r)] has the elementary truncated-lognormal moment below.
    rr=np.maximum(r,1e-30);ratio=np.log(rr/radius)
    inner=rr**(-ell-1)*radius**ell*np.exp(.5*ell**2*width**2)*ndtr((ratio-ell*width**2)/width)
    outer=rr**ell*radius**(-ell-1)*np.exp(.5*(ell+1)**2*width**2)*ndtr((-ratio-(ell+1)*width**2)/width)
    return inner+outer

def observable_particles(x,read_radii,width=0):
    r=np.linalg.norm(x,axis=1)
    safe=np.maximum(r,1e-30)
    u=(x[:,0]+1j*x[:,1])/safe
    y22=np.sqrt(15/(32*np.pi))*u**2
    y20=np.sqrt(5/(16*np.pi))*(3*(x[:,2]/safe)**2-1)
    y44=3/16*np.sqrt(35/(2*np.pi))*u**4
    harmonics=[(0,0,None),(2,0,y20),(2,2,y22),(4,4,y44)]
    values=[]
    for radius in read_radii:
        for ell,m,y in harmonics:
            if ell==0:
                coefficient=-annulus_kernel(r,radius,0,width)
            else:
                kernel=annulus_kernel(r,radius,ell,width)
                eq=sph_harm(m,ell,0,np.pi/2)
                coefficient=-4*np.pi/(2*ell+1)*kernel*np.conj(y)*eq
            values.append(coefficient)
    return np.column_stack(values)

def moments(x,weights,read_radii,nbase,width):
    values=observable_particles(x,read_radii,width)
    normalized=weights/np.sum(weights)
    mean=np.sum(values*normalized[:,None],axis=0)
    # GalaxyModel equal-weight sampling is required for these independent blocks.
    assert np.ptp(normalized)<1e-12
    original_units=values.reshape(nbase,8,-1).mean(axis=1)
    blocks=original_units.reshape(8,nbase//8,-1).mean(axis=1)
    return mean,blocks

def validate(pot,am,af,xv):
    actions,angles,freq=af(xv,angles=True,frequencies=True)
    reconstructed=am(np.column_stack((actions,angles)))
    checks={'initial_cartesian_roundtrip':float(np.max(abs(reconstructed-xv)))}
    selected=np.array([0,8,16,24,32,40,48,56])
    reference=[]
    for z in xv[selected]:
        def rhs(t,y):
            x=y[:3];u=np.sqrt(.25+np.dot(x,x))
            force=-x/(u*(.5+u)**2)
            return np.r_[y[3:],force]
        sol=solve_ivp(rhs,(0,32),z,method='DOP853',rtol=2e-12,atol=2e-14)
        assert sol.success
        reference.append(sol.y[:,-1])
    propagated=coordinates(am,actions[selected],angles[selected],freq[selected],32)
    checks['independent_DOP853_state_difference']=float(np.max(abs(propagated-reference)))
    checks['background_energy_drift']=float(np.max(abs(potential_energy(propagated)-potential_energy(xv[selected]))))
    points=xv[:128,:3]
    _,analytic=pulse(points,.01,.8,.21)
    differences=[]
    for dim in range(3):
        h=2e-6*np.maximum(1,np.linalg.norm(points,axis=1))
        plus=points.copy();minus=points.copy()
        plus[:,dim]+=h;minus[:,dim]-=h
        finite=-(pulse(plus,.01,.8,.21)[0]-pulse(minus,.01,.8,.21)[0])/(2*h)
        differences.append(abs(finite-analytic[:,dim]))
    checks['impulse_gradient_absolute_difference']=float(np.max(differences))
    x=points;radius=np.linalg.norm(x,axis=1);phi=np.arctan2(x[:,1],x[:,0]);theta=np.arccos(x[:,2]/radius)
    checks['Y22_algebra_difference']=float(np.max(abs(sph_harm(2,2,phi,theta)-np.sqrt(15/(32*np.pi))*((x[:,0]+1j*x[:,1])/radius)**2)))
    checks['Y44_algebra_difference']=float(np.max(abs(sph_harm(4,4,phi,theta)-3/16*np.sqrt(35/(2*np.pi))*((x[:,0]+1j*x[:,1])/radius)**4)))
    return checks,actions,angles,freq

def channels(actions,frequencies,tau):
    # Spherical nondegenerate frequencies are radial and apsidal/plane frequency.
    omega=np.column_stack((frequencies[:,0],frequencies[:,1]))
    pairs=[((1,0),(2,0)),((0,2),(1,2)),((1,2),(2,2)),((1,0),(1,2))]
    rows=[]
    for k1,k2 in pairs:
        k1,k2=np.array(k1),np.array(k2);kd=k2-k1
        a=omega@kd;b=omega@k2
        va=np.var(a)
        ratio=float(np.mean((a-np.mean(a))*(b-np.mean(b)))/va) if va>0 else 1.
        ratio=max(ratio,1.)
        residual=a*ratio-b
        rows.append(dict(k1=k1.tolist(),k2=k2.tolist(),difference=kd.tolist(),
            minimum_dispersion_time_over_tau=ratio,
            residual_frequency_standard_deviation=float(np.std(residual)),
            unweighted_phase_coherence=float(abs(np.mean(np.exp(-1j*tau*residual)))),
            warning='Frequency-only screen. Actual impulse Fourier weights and DF derivatives are not included.'))
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--nbase',type=int,default=1024);p.add_argument('--seed',type=int,default=81320)
    p.add_argument('--tau',type=float,default=16.);p.add_argument('--amplitude',type=float,default=.01)
    p.add_argument('--cadence',type=float,default=.5);p.add_argument('--end-factor',type=float,default=4.)
    p.add_argument('--radial-width',type=float,default=.1)
    p.add_argument('--validate-only',action='store_true');args=p.parse_args()
    assert args.nbase%8==0
    args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'source.py').write_bytes(Path(__file__).read_bytes())
    start,cpu=time.monotonic(),time.process_time()
    config=dict(pid=os.getpid(),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        nbase=args.nbase,nparticles=8*args.nbase,seed=args.seed,tau=args.tau,
        amplitude=args.amplitude,cadence=args.cadence,end_factor=args.end_factor,
        radial_log_width=args.radial_width,
        read_radii=[.5,1.,2.],source_sha256=digest(__file__),agama_binary_sha256=digest(agama.__file__),
        agama_library=str(Path(agama.__file__).parent),
        nice=os.getpriority(os.PRIO_PROCESS,0),self_gravity=False,
        pulse_A=dict(scale=.8,phi=0),pulse_B=dict(scale=1.6,phi=float(np.pi/4)))
    write(args.out/'config.json',config)
    print('PID',os.getpid(),'CONFIG',args.out,flush=True)
    pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5)
    am,af=agama.ActionMapper(pot),agama.ActionFinder(pot)
    xv,weights,base=symmetry_sample(pot,args.nbase,args.seed)
    np.savez_compressed(args.out/'initial.npz',xv=xv,weights=weights,independent_base=base)
    checks,J0,angles0,freq0=validate(pot,am,af,xv)
    gates={name:value<(2e-7 if name=='independent_DOP853_state_difference' else 1e-8) for name,value in checks.items()}
    channel_rows=channels(J0,freq0,args.tau)
    if args.validate_only:
        result=dict(config=config,checks=checks,gates=gates,all_pass=all(gates.values()),channels=channel_rows,
            cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start)
        write(args.out/'result.json',result);(args.out/'COMPLETE').write_text('Independent validation only.\n')
        print(json.dumps(result,indent=2));return
    if not all(gates.values()):
        write(args.out/'result.json',dict(config=config,checks=checks,gates=gates,all_pass=False,
            cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start))
        raise RuntimeError('Independent numerical gate failed; preserving failure.')
    times=np.arange(round(args.end_factor*args.tau/args.cadence)+1)*args.cadence
    cases={};scrambled={};case_blocks={};scrambled_blocks={};work={}
    rng=np.random.default_rng(args.seed+1)
    uniform=np.repeat(rng.uniform(0,2*np.pi,(args.nbase,2)),8,axis=0)
    max_energy_drift=0.;max_L_preservation_error=0.;max_postkick_roundtrip=0.
    for label,a1,a2 in [('AB',args.amplitude,args.amplitude),('A',args.amplitude,0),('B',0,args.amplitude),('0',0,0)]:
        state=xv.copy();initialE=potential_energy(state)
        dv=pulse(state[:,:3],a1,.8,0)[1]
        externalA=np.sum(state[:,3:]*dv,axis=1)+.5*np.sum(dv*dv,axis=1)
        state[:,3:]+=dv;J,angles,freq=af(state,angles=True,frequencies=True)
        firstE=potential_energy(state)
        second=coordinates(am,J,angles,freq,args.tau)
        dv=pulse(second[:,:3],a2,1.6,np.pi/4)[1]
        externalB=np.sum(second[:,3:]*dv,axis=1)+.5*np.sum(dv*dv,axis=1)
        second[:,3:]+=dv
        Js,ans,fs=af(second,angles=True,frequencies=True)
        if not np.isfinite(Js).all():raise RuntimeError('Unbound particle after physical impulse.')
        max_postkick_roundtrip=max(max_postkick_roundtrip,float(np.max(abs(am(np.column_stack((Js,ans)))-second))))
        secondE=potential_energy(second)
        memory_angles=angles.copy()
        memory_angles[:,0]=uniform[:,0]
        node=angles[:,2]-np.sign(J[:,2])*angles[:,1]
        memory_angles[:,1]=uniform[:,1]
        memory_angles[:,2]=node+np.sign(J[:,2])*uniform[:,1]
        erased=coordinates(am,J,memory_angles,freq,0)
        beforeL=np.cross(state[:,:3],state[:,3:]);afterL=np.cross(erased[:,:3],erased[:,3:])
        max_L_preservation_error=max(max_L_preservation_error,float(np.max(abs(afterL-beforeL))))
        # The intervention happens immediately before B. The new angle is independent
        # and uniform, so advancing it by tau is distributionally identical.
        erased[:,3:]+=pulse(erased[:,:3],a2,1.6,np.pi/4)[1]
        Je,ae,fe=af(erased,angles=True,frequencies=True)
        trace=[];blocks=[];etrace=[];eblocks=[]
        for t in times:
            if t<args.tau:
                frame=coordinates(am,J,angles,freq,t)
                E=firstE
            else:
                frame=coordinates(am,Js,ans,fs,t-args.tau)
                E=secondE
            max_energy_drift=max(max_energy_drift,float(np.max(abs(potential_energy(frame)-E))))
            mean,block=moments(frame[:,:3],weights,config['read_radii'],args.nbase,args.radial_width)
            trace.append(mean);blocks.append(block)
            if t>=args.tau:
                frame=coordinates(am,Je,ae,fe,t-args.tau)
                mean,block=moments(frame[:,:3],weights,config['read_radii'],args.nbase,args.radial_width)
                etrace.append(mean);eblocks.append(block)
        cases[label]=np.asarray(trace);case_blocks[label]=np.asarray(blocks)
        scrambled[label]=np.asarray(etrace);scrambled_blocks[label]=np.asarray(eblocks)
        work[label]=dict(mean_impulse_A=float(np.average(externalA,weights=weights)),
            mean_impulse_B=float(np.average(externalB,weights=weights)),
            impulse_energy_accounting_residual=float(max(np.max(abs(firstE-initialE-externalA)),np.max(abs(secondE-firstE-externalB)))))
        print('Completed',label,'CPU',time.process_time()-cpu,flush=True)
    combine=lambda d:d['AB']-d['A']-d['B']+d['0']
    raw=dict(t=times,mixed=combine(cases),mixed_blocks=combine(case_blocks),
        scrambled_t=times[times>=args.tau],scrambled_mixed=combine(scrambled),
        scrambled_mixed_blocks=combine(scrambled_blocks),
        **{f'case_{k}':v for k,v in cases.items()},**{f'block_{k}':v for k,v in case_blocks.items()})
    np.savez_compressed(args.out/'traces.npz',**raw)
    checks.update(max_background_energy_drift=max_energy_drift,
        memory_erasure_L_vector_difference=max_L_preservation_error,
        postkick_cartesian_roundtrip=max_postkick_roundtrip,
        external_work_residual=max(v['impulse_energy_accounting_residual'] for v in work.values()))
    result=dict(config=config,checks=checks,numerical_gates=gates,channels=channel_rows,work=work,
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        raw_sha256=digest(args.out/'traces.npz'),
        scope='3D fixed-background collisionless tracer with spatial quadrupole impulses and gravitational multipole readout. No echo interpretation automatic; timing, scaling, sampling and memory controls remain required.')
    write(args.out/'result.json',result);(args.out/'COMPLETE').write_text('Tracer measurement complete; interpretation requires controls.\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['channels','work']},indent=2))

if __name__=='__main__':main()
