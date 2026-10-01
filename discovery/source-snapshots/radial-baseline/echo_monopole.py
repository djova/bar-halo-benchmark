"""Spherical selected-halo memory screen: forward and Eulerian formulations."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[name]='1'
import argparse,datetime,json,time,hashlib
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre,expit,ndtr
from scipy.interpolate import RectBivariateSpline
from scipy.integrate import solve_ivp
from echo_halo import ROOT,agama,annulus_kernel,digest,write

B=.5

def radial_parameters(E,L):
    I=1/np.sqrt(2*E);Lmax=(1-E)/np.sqrt(2*E);L1=np.sqrt(L*L+2)
    Jr=I*(Lmax-L)/(I+.5*(L1-L))
    if np.min(Jr)<-1e-10:raise RuntimeError('Nonphysical radial action in background map.')
    Jr=np.maximum(Jr,0)
    eccentricity=np.sqrt(Jr*(Jr+L)*(Jr+L1)*(Jr+L+L1))/I**2
    return I,eccentricity

def radial_map(E,L,mean_anomaly):
    I,e=radial_parameters(E,L)
    M=np.remainder(mean_anomaly+np.pi,2*np.pi)-np.pi
    eta=M+.85*e*np.sign(np.sin(M))
    residual=1.
    for iteration in range(24):
        delta=(eta-e*np.sin(eta)-M)/(1-e*np.cos(eta))
        eta-=delta
        residual=float(np.max(abs(delta)))
        if residual<3e-14:break
    if residual>1e-11:raise RuntimeError('Kepler inversion failed.')
    s=I**2*(1-e*np.cos(eta))
    r=np.sqrt(np.maximum((s-B)*(s+B),0))
    if np.any(r<=0):raise RuntimeError('Zero radius in radial grid; use phases away from the turning boundary.')
    vr=I*e*np.sin(eta)/r
    return r,vr

def recover(r,vr,L):
    E=1/(B+np.sqrt(B*B+r*r))-.5*(vr*vr+(L/r)**2)
    if np.any(E<=0):raise RuntimeError('Unbound radial state; prescribed selected support should prevent this.')
    if np.any(E>1+2e-12):raise RuntimeError('Binding energy exceeds central-potential bound.')
    E=np.minimum(E,1.)
    I,e=radial_parameters(E,L)
    safe=np.maximum(e,1e-20)
    sin_eta=vr*r/(I*safe)
    cos_eta=(1-np.sqrt(B*B+r*r)/I**2)/safe
    eta=np.arctan2(sin_eta,cos_eta)
    M=eta-e*np.sin(eta)
    return E,np.remainder(M,2*np.pi)

def velocity_impulse(r,a,scale):return -a*r/(r*r+scale*scale)**1.5

def frequency(E):return (2*E)**1.5

def bound_cost(a,scale):
    kick=2*abs(a)/(3*np.sqrt(3)*scale**2)
    return np.sqrt(2)*kick+.5*kick*kick

class Cohort:
    def __init__(self,pot,low=.02,high=.04):
        self.df=agama.DistributionFunction(type='QuasiSpherical',density=pot,potential=pot)
        self.low,self.high=low,high

    def __call__(self,E):
        E=np.asarray(E);flat=E.ravel();out=np.zeros_like(flat)
        selected=(flat>self.low)&(flat<=1)
        energy=flat[selected]
        if len(energy):
            I=1/np.sqrt(2*energy);L=.5*(1-energy)/np.sqrt(2*energy)
            L1=np.sqrt(L*L+2)
            Jr=I*((1-energy)/np.sqrt(2*energy)-L)/(I+.5*(L1-L))
            actions=np.column_stack((Jr,L/2,L/2))
            f=self.df(actions)
            x=(energy-self.low)/(self.high-self.low)
            taper=np.ones_like(x);inside=x<1
            taper[inside]=expit(-1/x[inside]+1/(1-x[inside]))
            out[selected]=f*taper
        return out.reshape(E.shape)

def grid(ne,nL,nr,lower,radial_quadrature='mean_anomaly'):
    x,wE=roots_legendre(ne);energies=lower+(1-lower)*(x+1)/2;wE=wE*(1-lower)/2
    x,wL=roots_legendre(nL);lam=(x+1)/2;wL=wL/2
    phase=2*np.pi*(np.arange(nr)+.5)/nr
    E,la,M=np.meshgrid(energies,lam,phase,indexing='ij')
    Lmax=(1-E)/np.sqrt(2*E);L=la*Lmax
    weights=(2*np.pi)**3*(wE[:,None,None]*wL[None,:,None])/nr*2*L*Lmax*(2*E)**-1.5
    if radial_quadrature=='eccentric_anomaly':
        I,e=radial_parameters(E,L)
        weights=weights*(1-e*np.cos(M))
        M=M-e*np.sin(M)
    return E.ravel(),L.ravel(),M.ravel(),weights.ravel()

def observables(r,radii,width):
    values=[]
    for R in radii:
        z=-np.log(r/R)/width
        values.extend([-annulus_kernel(r,R,0,width),
            -R**-2*np.exp(2*width**2)*ndtr(z-2*width),ndtr(z)])
    return np.column_stack(values)

def independent_checks(E,L,M,a):
    indices=np.linspace(0,len(E)-1,12,dtype=int)
    r,vr=radial_map(E[indices],L[indices],M[indices])
    recE,recM=recover(r,vr,L[indices])
    checks=dict(energy_roundtrip=float(np.max(abs(recE-E[indices]))),
        radial_angle_roundtrip=float(np.max(abs(np.angle(np.exp(1j*(recM-M[indices])))))))
    errors=[]
    for er,ell,m,rr,vrr in zip(E[indices],L[indices],M[indices],r,vr):
        # Embed into a genuine inclined3D Cartesian orbit, then apply radial impulse.
        x=np.array([rr,0,0]);v=np.array([vrr,ell/rr*.5,ell/rr*np.sqrt(.75)])
        dv=-a*x/(np.dot(x,x)+.25)**1.5
        beforeL=np.cross(x,v);afterL=np.cross(x,v+dv)
        checks['max_L_vector_impulse_difference']=max(checks.get('max_L_vector_impulse_difference',0.),float(np.max(abs(afterL-beforeL))))
        initial=np.r_[x,v+dv]
        def rhs(t,y):
            xx=y[:3];u=np.sqrt(.25+np.dot(xx,xx))
            return np.r_[y[3:],-xx/(u*(.5+u)**2)]
        solution=solve_ivp(rhs,(0,32),initial,method='DOP853',rtol=2e-12,atol=2e-14)
        assert solution.success
        newE,newM=recover(np.array([rr]),np.array([vrr+velocity_impulse(np.array([rr]),a,.5)[0]]),np.array([ell]))
        predicted_r,predicted_v=radial_map(newE,np.array([ell]),newM+frequency(newE)*32)
        finalx,finalv=solution.y[:3,-1],solution.y[3:,-1]
        reference_r=np.linalg.norm(finalx);reference_v=np.dot(finalx,finalv)/reference_r
        errors.append(max(abs(predicted_r[0]-reference_r),abs(predicted_v[0]-reference_v)))
    checks['independent_Cartesian_DOP853_radial_difference']=float(max(errors))
    return checks

def harmonic_support():
    phase=2*np.pi*(np.arange(256)+.5)/256;rows=[]
    for binding in (.2,.5,.8):
        for fraction in (.3,.7):
            E=np.full(256,binding);L=np.full(256,fraction*(1-binding)/np.sqrt(2*binding))
            r,v=radial_map(E,L,phase);record=dict(binding=binding,L_fraction=fraction)
            for name,scale in [('A',.5),('B',1.5)]:
                potential=-1/np.sqrt(r*r+scale*scale)
                coeff=np.fft.fft(potential)/len(potential)
                coeff=coeff[:5]*np.exp(-1j*np.arange(5)*np.pi/256)
                record[name]=dict(radial_fourier_coefficients=[[float(z.real),float(z.imag)] for z in coeff],
                    n1_n2_n3_nonzero=bool(min(abs(coeff[1:4]))>1e-8))
            rows.append(record)
    return rows

def forward(E,L,M,phaseweights,cohort,times,a,tau,radii,width):
    weights=phaseweights*cohort(E)
    # Omit only identically zero initial DF nodes, with no post-kick selection.
    keep=weights>0
    E,L,M,weights=E[keep],L[keep],M[keep],weights[keep]
    initial_r,initial_v=radial_map(E,L,M)
    traces={};mass={};work={};maxLerror=0.
    for label,a1,a2 in [('AB',a,a),('A',a,0),('B',0,a),('0',0,0)]:
        vA=initial_v+velocity_impulse(initial_r,a1,.5)
        EA,MA=recover(initial_r,vA,L)
        rB,vB=radial_map(EA,L,MA+frequency(EA)*tau)
        vBplus=vB+velocity_impulse(rB,a2,1.5)
        EB,MB=recover(rB,vBplus,L)
        values=[]
        for t in times:
            if t<tau:r,v=radial_map(EA,L,MA+frequency(EA)*t)
            else:r,v=radial_map(EB,L,MB+frequency(EB)*(t-tau))
            values.append(np.sum(observables(r,radii,width)*weights[:,None],axis=0))
        traces[label]=np.array(values);mass[label]=float(np.sum(weights))
        work[label]=dict(total_external_work_A=float(np.sum(weights*(E-EA))),
            total_external_work_B=float(np.sum(weights*(EA-EB))),
            minimum_postkick_binding_energy=float(min(np.min(EA),np.min(EB))))
    return traces,mass,work

def memory_table(cohort,a,ne,nL,nr,lower,radial_quadrature='eccentric_anomaly'):
    # Tabulate the exact angle-averaged DF correction h=<f_afterA>-f0.
    # Dense energy coverage is explicit around the specified physical taper.
    energy=np.unique(np.r_[np.linspace(lower,.07,ne//2),np.linspace(.07,1-1e-8,ne//2)])
    lam=np.linspace(0,1,nL)
    phase=2*np.pi*(np.arange(nr)+.5)/nr
    E,la,M=np.meshgrid(energy,lam,phase,indexing='ij')
    L=la*(1-E)/np.sqrt(2*E)
    if radial_quadrature=='eccentric_anomaly':
        I,e=radial_parameters(E,L)
        jacobian=1-e*np.cos(M)
        ss=I**2*jacobian
        r=np.sqrt((ss-B)*(ss+B)).ravel()
        v=(I*e*np.sin(M)).ravel()/r
    else:
        jacobian=np.ones_like(M)
        r,v=radial_map(E.ravel(),L.ravel(),M.ravel())
    dv=velocity_impulse(r,a,.5)
    before_binding=E.ravel()+v*dv-.5*dv*dv
    correction=((cohort(before_binding)-cohort(E.ravel())).reshape(E.shape)*jacobian).mean(axis=2)
    h=RectBivariateSpline(energy,lam,correction,kx=3,ky=3,s=0)
    positivity=float(np.min(correction+cohort(energy)[:,None]))
    return h,dict(energy_nodes=len(energy),Lfraction_nodes=nL,radial_phase_nodes=nr,
                  radial_quadrature=radial_quadrature,
                  max_angle_measure_normalization_error=float(np.max(abs(jacobian.mean(axis=2)-1))),
                  min_averaged_DF=positivity,minimum_sampled_preA_binding=float(np.min(before_binding)))

def eulerian(E,L,M,weights,cohort,times,a,tau,radii,width,memory):
    rnow,vnow=radial_map(E,L,M)
    O=observables(rnow,radii,width)
    f0=cohort(E);baseline=np.sum(weights[:,None]*f0[:,None]*O,axis=0)
    traces={k:[] for k in ('AB','A','B','0')};mass={k:[] for k in traces};erased=[];erased_mass=[]
    maximum_inverse_energy=0.;minimum_inverse_energy=1.
    h,memory_info=memory
    lambda_now=L/((1-E)/np.sqrt(2*E))
    hnow=h.ev(E,lambda_now)
    for t in times:
        # A-only backward history: exact background to0, inverse A velocity kick.
        r0,v0=radial_map(E,L,M-frequency(E)*t)
        dvA=velocity_impulse(r0,a,.5)
        eAinit=E+v0*dvA-.5*dvA*dvA
        fA=cohort(eAinit)
        if t<tau:
            fAB=fA;fB=f0;memory_mixed=np.zeros_like(f0)
        else:
            # AB history: background backwards toB, inverse B, background toA,
            # inverse A. B-only needs only the first inverse velocity kick.
            rB,vB=radial_map(E,L,M-frequency(E)*(t-tau))
            vpreB=vB-velocity_impulse(rB,a,1.5)
            EpreB,MpreB=recover(rB,vpreB,L)
            fB=cohort(EpreB)
            rA,vA=radial_map(EpreB,L,MpreB-frequency(EpreB)*tau)
            dvA=velocity_impulse(rA,a,.5)
            eABinit=EpreB+vA*dvA-.5*dvA*dvA
            fAB=cohort(eABinit)
            lam_preB=L/((1-EpreB)/np.sqrt(2*EpreB))
            if np.any(lam_preB>1+1e-9):raise RuntimeError('L support exceeded during inverse kick.')
            memory_mixed=h.ev(EpreB,np.clip(lam_preB,0,1))-hnow
            maximum_inverse_energy=max(maximum_inverse_energy,float(np.max(eABinit)),float(np.max(EpreB)))
            minimum_inverse_energy=min(minimum_inverse_energy,float(np.min(eABinit)),float(np.min(EpreB)))
        for label,f in [('AB',fAB),('A',fA),('B',fB),('0',f0)]:
            traces[label].append(np.sum(weights[:,None]*f[:,None]*O,axis=0))
            mass[label].append(float(np.sum(weights*f)))
        erased.append(np.sum(weights[:,None]*memory_mixed[:,None]*O,axis=0))
        erased_mass.append(float(np.sum(weights*memory_mixed)))
    traces={k:np.array(v) for k,v in traces.items()};mass={k:np.array(v) for k,v in mass.items()}
    projection_mass=float(np.sum(weights*(f0+hnow)))
    audits=dict(maximum_inverse_initial_binding=maximum_inverse_energy,
        minimum_inverse_initial_binding=minimum_inverse_energy,
        initial_mass=float(np.sum(weights*f0)),projected_postA_mass=projection_mass,
        memory_projection_mass_difference=projection_mass-float(np.sum(weights*f0)),
        maximum_mixed_mass_residual=float(np.max(abs(mass['AB']-mass['A']-mass['B']+mass['0']))),
        maximum_memory_mixed_mass_residual=float(np.max(abs(np.asarray(erased_mass)))),
        memory_table=memory_info)
    return traces,mass,np.array(erased),audits

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--ne',type=int,default=128);p.add_argument('--nL',type=int,default=16);p.add_argument('--nr',type=int,default=128)
    p.add_argument('--tau',type=float,default=16.);p.add_argument('--amplitude',type=float,default=.002)
    p.add_argument('--support-amplitude',type=float,default=.004)
    p.add_argument('--cadence',type=float,default=1.);p.add_argument('--end-factor',type=float,default=3.5)
    p.add_argument('--taper-low',type=float,default=.02);p.add_argument('--taper-high',type=float,default=.04)
    p.add_argument('--memory-ne',type=int,default=512);p.add_argument('--memory-nL',type=int,default=65);p.add_argument('--memory-nr',type=int,default=128)
    p.add_argument('--radial-quadrature',choices=['mean_anomaly','eccentric_anomaly'],default='mean_anomaly')
    p.add_argument('--memory-quadrature',choices=['mean_anomaly','eccentric_anomaly'],default='eccentric_anomaly')
    p.add_argument('--times',type=float,nargs='*');p.add_argument('--method',choices=['both','forward','eulerian'],default='both')
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'source.py').write_bytes(Path(__file__).read_bytes());(args.out/'echo_halo_import.py').write_bytes((Path(__file__).parent/'echo_halo.py').read_bytes())
    start,cpu=time.monotonic(),time.process_time()
    largest_cost=bound_cost(args.amplitude,.5)+bound_cost(args.amplitude,1.5)
    assert args.amplitude<=args.support_amplitude
    grid_cost=bound_cost(args.support_amplitude,.5)+bound_cost(args.support_amplitude,1.5)
    lower=args.taper_low-grid_cost-1e-5
    assert lower>bound_cost(args.amplitude,1.5),'The Eulerian inverse-B grid must remain bound.'
    config=dict(pid=os.getpid(),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        ne=args.ne,nL=args.nL,nr=args.nr,nparticles=args.ne*args.nL*args.nr,tau=args.tau,amplitude=args.amplitude,
        taper_low=args.taper_low,taper_high=args.taper_high,current_energy_grid_lower=lower,
        maximum_two_pulse_binding_change_bound=largest_cost,guaranteed_selected_binding_after_both=args.taper_low-largest_cost,
        grid_covers_worst_case_binding=lower+1e-5,
        support_bound_amplitude=args.support_amplitude,
        radial_quadrature=args.radial_quadrature,memory_quadrature=args.memory_quadrature,
        cadence=args.cadence,end_factor=args.end_factor,method=args.method,read_radii=[.5,1.,2.],radial_log_width=.1,
        source_sha256=digest(__file__),halo_import_sha256=digest(Path(__file__).parent/'echo_halo.py'),
        agama_binary_sha256=digest(agama.__file__),agama_library=str(Path(agama.__file__).parent),
        nice=os.getpriority(os.PRIO_PROCESS,0),self_gravity=False,pulse_A_scale=.5,pulse_B_scale=1.5)
    write(args.out/'config.json',config);print('PID',os.getpid(),'N',config['nparticles'],flush=True)
    pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5);cohort=Cohort(pot,args.taper_low,args.taper_high)
    E,L,M,weights=grid(args.ne,args.nL,args.nr,lower,args.radial_quadrature)
    checks=independent_checks(E,L,M,args.amplitude)
    if max(checks.values())>1e-6:raise RuntimeError('Independent radial numerical gate failed.')
    cohort_mass=float(np.sum(weights*cohort(E)));config['absolute_initial_reference_halo_mass']=cohort_mass
    # Inclination/angular variables have been integrated exactly by symmetry.
    angular_info=dict(orientation_integrated_exactly=True,full_L_vector_preserved_by_central_forcing=True,
        radial_frequency_minimum_in_selected_support=frequency(args.taper_low),radial_frequency_maximum=frequency(1.))
    times=np.array(args.times) if args.times else np.arange(round(args.end_factor*args.tau/args.cadence)+1)*args.cadence
    raw=dict(t=times);results={}
    if args.method in ('both','forward'):
        traces,mass,work=forward(E,L,M,weights,cohort,times,args.amplitude,args.tau,config['read_radii'],.1)
        for label,value in traces.items():raw['forward_'+label]=value
        raw['forward_mixed']=traces['AB']-traces['A']-traces['B']+traces['0']
        results['forward']=dict(masses=mass,work=work)
        np.savez_compressed(args.out/'forward-partial.npz',**raw)
        print('Forward complete CPU',time.process_time()-cpu,flush=True)
    if args.method in ('both','eulerian'):
        memory=memory_table(cohort,args.amplitude,args.memory_ne,args.memory_nL,args.memory_nr,lower,args.memory_quadrature)
        print('Memory table complete CPU',time.process_time()-cpu,flush=True)
        traces,mass,erased,audits=eulerian(E,L,M,weights,cohort,times,args.amplitude,args.tau,config['read_radii'],.1,memory)
        for label,value in traces.items():raw['eulerian_'+label]=value;raw['eulerian_mass_'+label]=mass[label]
        raw['eulerian_mixed']=traces['AB']-traces['A']-traces['B']+traces['0'];raw['memory_erased_mixed']=erased
        results['eulerian']=audits
        print('Eulerian complete CPU',time.process_time()-cpu,flush=True)
    if args.method=='both':
        results['formulation_comparison']=dict(maximum_complex_readout_difference=float(np.max(abs(raw['forward_mixed']-raw['eulerian_mixed']))),
            maximum_forward_mixed=float(np.max(abs(raw['forward_mixed']))),maximum_eulerian_mixed=float(np.max(abs(raw['eulerian_mixed']))))
    np.savez_compressed(args.out/'traces.npz',**raw)
    result=dict(config=config,checks=checks,angular_info=angular_info,pulse_harmonic_support=harmonic_support(),results=results,
        raw_sha256=digest(args.out/'traces.npz'),cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        scope='Selected isotropic halo cohort radial-memory and absolute Newtonian gravitational-readout screen. Full halo, self-gravity, finite-duration mass changes and stellar response remain untested. Convergence/scaling/separation/memory controls required.')
    write(args.out/'result.json',result);(args.out/'COMPLETE').write_text('Spherical measurement complete; scientific controls required.\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['results','config','pulse_harmonic_support']},indent=2))
    if 'formulation_comparison' in results:print(json.dumps(results['formulation_comparison'],indent=2))

if __name__=='__main__':
    _started_wall,_started_cpu=time.monotonic(),time.process_time()
    try:main()
    except Exception as error:
        import sys,traceback
        if '--out' in sys.argv:
            _out=Path(sys.argv[sys.argv.index('--out')+1])
            if _out.exists():write(_out/'FAILURE.json',dict(pid=os.getpid(),error=repr(error),
                traceback=traceback.format_exc(),cpu_seconds=time.process_time()-_started_cpu,
                wall_seconds=time.monotonic()-_started_wall))
        raise
