"""Leading physical l2 x l4 halo readout with exact orientation integration.

This is a second-order prediction, not a finite-amplitude echo confirmation.
The four positive-source sign cases share monopoles; their angular bilinear
contrast is represented below. Direct first-order monopoles are also saved.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
import argparse, datetime, json, math, time, sys, traceback
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre, ndtr
from scipy.integrate import quad
from echo_monopole import Cohort,radial_parameters,frequency,agama,digest,write
from echo_halo import annulus_kernel
from echo_multipole_pulse import IntegratedMultipolePulse

def orbit_shape(E,L,M):
    I,e=radial_parameters(E[:,None],L[:,None])
    wrapped=np.remainder(M+np.pi,2*np.pi)-np.pi
    eta=wrapped+.85*e*np.sign(np.sin(wrapped))
    for _ in range(24):
        delta=(eta-e*np.sin(eta)-wrapped)/(1-e*np.cos(eta));eta-=delta
        if np.max(abs(delta))<3e-14:break
    assert np.max(abs(delta))<1e-11
    ss=I**2*(1-e*np.cos(eta));r=np.sqrt((ss-.5)*(ss+.5))
    aminus=1-.5/I**2;aplus=1+.5/I**2;L1=np.sqrt(L[:,None]**2+2)
    sine=np.sin(eta/2);cosine=np.cos(eta/2)
    phi1=np.arctan2(np.sqrt(np.maximum(aminus+e,0))*sine,np.sqrt(np.maximum(aminus-e,0))*cosine)
    phi2=np.arctan2(np.sqrt(aplus+e)*sine,np.sqrt(aplus-e)*cosine)
    F=.5*(1+L[:,None]/L1)
    chi=phi1+L[:,None]/L1*phi2-F*wrapped
    return r,chi

def inclination(ell,harmonic,c):
    h=(ell-harmonic)//2
    if (ell-harmonic)%2 or not 0<=h<=ell:return np.zeros_like(c),np.zeros_like(c)
    A=(1+c)/2;B=(1-c)/2;binomial=math.comb(ell,h)
    p=ell-h
    value=binomial*A**p*B**h
    derivative=binomial*(p/2*A**(p-1)*B**h if p else 0)-binomial*(h/2*A**p*B**(h-1) if h else 0)
    return value,derivative

def angular_integrals(ellA,ellB):
    # A carries node -2, B +4, O -2. A's coefficient is C2,-ellA.
    c,w=roots_legendre(5);ellout=ellA+ellB
    ca,_=inclination(2,-ellA,c);cb,dcb=inclination(4,ellB,c)
    co,dco=inclination(2,ellout,c)
    return (float(np.sum(w*ca*cb*co)),
            float(np.sum(w*ca*dcb*co*(2-ellout*c))),
            float(np.sum(w*ca*cb*dco*(4-ellB*c))))

def direct_angular_integrals(ellA,ellB):
    c,w=roots_legendre(5);mell=ellA+ellB
    ca,dca=inclination(2,-ellA,c);cb,dcb=inclination(4,ellB,c);co,_=inclination(2,mell,c)
    return (float(np.sum(w*ca*cb*co)),
            float(np.sum(w*ca*dcb*co*(-2-ellA*c))),
            float(np.sum(w*dca*cb*co*(4-ellB*c))))

def readout_radial(r,observable,ell=2,R=1.,width=.1):
    coefficient=math.comb(2*ell,ell)/4**ell
    if observable=='potential':return -coefficient*annulus_kernel(r,R,ell,width)
    d=np.log(r/R)
    inner=r**(-ell-1)*R**(ell-1)*np.exp(.5*(ell-1)**2*width**2)*ndtr((d-(ell-1)*width**2)/width)
    outer=r**ell*R**(-ell-2)*np.exp(.5*(ell+2)**2*width**2)*ndtr((-d-(ell+2)*width**2)/width)
    if observable=='radial_force':return coefficient*(ell*inner-(ell+1)*outer)
    if observable=='tangential_force':return 1j*ell*coefficient*(inner+outer)
    raise ValueError(observable)

def harmonics(E,L,nphase,nmax):
    M=2*np.pi*(np.arange(nphase)+.5)/nphase
    r,chi=orbit_shape(E,L,M[None,:]);fields=[];labels=[]
    for name,ell,mass,scale,eps,phi in [('A',2,.006,.8,.5,0.),('B',4,.010,1.6,.5,np.pi/8)]:
        coefficient=-3*mass*eps*2**ell/((2*ell+1)*(2*ell+3)*scale)
        radial=coefficient*(r/scale)**ell/(1+(r/scale)**2)**(ell+.5)/2
        node=-ell if name=='A' else ell
        phase=np.exp(-1j*node*phi)
        for angular in range(-ell,ell+1,2):
            fields.append(radial*phase*np.exp(1j*angular*chi));labels.append((name,angular))
        fields.append(-mass/np.sqrt(r*r+scale*scale));labels.append((name+'_monopole',0))
    for observable in ('potential','radial_force','tangential_force'):
        radial=readout_radial(r,observable)
        for angular in (-2,0,2):
            fields.append(radial*np.exp(1j*angular*chi));labels.append((observable,angular))
    fields.append(-annulus_kernel(r,1.,0,.1));labels.append(('monopole_potential',0))
    fields.append(-np.exp(.02)*ndtr(-np.log(r)/.1-.2));labels.append(('monopole_radial_force',0))
    coeff=np.fft.fft(np.array(fields),axis=2)/nphase
    modes=np.arange(-2*nmax,2*nmax+1)
    coeff=coeff[:,:,modes%nphase]*np.exp(-1j*modes*np.pi/nphase)[None,None,:]
    return {label:coeff[index] for index,label in enumerate(labels)}

def checks():
    # Check inclined spherical geometry against the independent Cartesian mapper.
    pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5);mapper=agama.ActionMapper(pot)
    E=np.array([.1,.3,.6]);frac=np.array([.2,.5,.8]);Lmax=(1-E)/np.sqrt(2*E);L=Lmax*frac
    I=1/np.sqrt(2*E);Jr=I-.5*(L+np.sqrt(L*L+2));M=np.array([.2,2.3,4.2])
    r,chi=orbit_shape(E,L,M[None,:]);r=r.diagonal();chi=chi.diagonal()
    errors=[]
    for c in (-.6,.5):
        actions=np.column_stack((Jr,L*(1-abs(c)),L*c));thetaL=.4;node=.3
        angles=np.column_stack((M,np.full(3,thetaL),np.full(3,node+np.sign(c)*thetaL)))
        xyz=mapper(np.column_stack((actions,angles)))[:,:3]
        psi=thetaL+chi
        x=r*(np.cos(node)*np.cos(psi)-np.sin(node)*c*np.sin(psi))
        y=r*(np.sin(node)*np.cos(psi)+np.cos(node)*c*np.sin(psi))
        z=r*np.sqrt(1-c*c)*np.sin(psi)
        errors.append(float(np.max(abs(xyz-np.column_stack((x,y,z))))))
    # Independent radial-force averaging of the unsmoothed Newtonian kernel.
    force_errors=[]
    for rr in (.2,.8,1.,1.7,4.):
        def integrand(u):
            R=np.exp(.1*u);g=3/8*(2*R/rr**3 if R<rr else -3*rr**2/R**4)
            return g*np.exp(-u*u/2)/np.sqrt(2*np.pi)
        cut=np.log(rr)/.1
        reference=quad(integrand,-9,9,points=[cut] if -9<cut<9 else [],epsabs=2e-13)[0]
        force_errors.append(abs(reference-readout_radial(np.array(rr),'radial_force')))
    # 2D constant-Hessian Gaussian: integrate the canonical IBP expression
    # independently of its closed characteristic-function expression.
    K=np.array([1.,2.]);N=2*K;m=N-K;S=np.array([[1.,.15],[.15,.7]])
    Sigma=np.diag([.4**2,.6**2]);omega0=np.array([1.,.8]);tau=5.;t=9.7;d=m*t-N*tau
    x,w=roots_legendre(80);p1=3.6*x;p2=5.4*x
    pp=np.stack(np.meshgrid(p1,p2,indexing='ij'),axis=-1).reshape(-1,2)
    weight=np.outer(w*3.6,w*5.4).ravel()
    f=np.exp(-.5*np.sum(pp**2/np.diag(Sigma),axis=1))/(2*np.pi*np.sqrt(np.linalg.det(Sigma)))
    # Echo channel has k=-K, n=N, m=N-K, so k.grad f is positive here.
    kgradf=f*((pp/np.diag(Sigma))@K)
    omega=omega0+pp@S.T
    numerical=np.sum(weight*kgradf*(-1j*(t-tau)*(N@S@m)/4)*np.exp(-1j*(omega@d)))
    exact=-(t-tau)*(N@S@m)*(K@S@d)/4*np.exp(-1j*(omega0@d)-.5*d@S@Sigma@S@d)
    result=dict(inclined_Cartesian_map_max_difference=max(errors),
                annular_radial_force_independent_integral_max_difference=float(max(force_errors)),
                two_frequency_Gaussian_canonical_formula_difference=float(abs(numerical-exact)))
    if not(max(errors)<1e-10 and max(force_errors)<1e-11 and abs(numerical-exact)<1e-12):
        raise RuntimeError('Independent check failed: '+json.dumps(result))
    return result

def predict(ne,nL,nphase,nmax,times,tau,step_scale,formulation='ibp',first_only=False,df_step=1e-4):
    x,we=roots_legendre(ne);E=.02+.98*(x+1)/2;we*=.98/2
    x,wl=roots_legendre(nL);frac=(x+1)/2;wl/=2
    E,frac=np.meshgrid(E,frac,indexing='ij');Lmax=(1-E)/np.sqrt(2*E);L=frac*Lmax
    weights=(2*np.pi)**3*we[:,None]*wl[None,:]*L*Lmax*(2*E)**-1.5
    E,L,weights=E.ravel(),L.ravel(),weights.ravel()
    I=1/np.sqrt(2*E);L1=np.sqrt(L*L+2);Jr=I-.5*(L+L1);F=.5*(1+L/L1)
    dJ=np.minimum(step_scale*(1+Jr),.002*Jr);dL=np.minimum(step_scale*(1+L),.002*L)
    fields=harmonics(E,L,nphase,nmax)
    derivativeJ={};derivativeL={}
    if not first_only:
        plus=harmonics(.5/(I+dJ)**2,L,nphase,nmax);minus=harmonics(.5/(I-dJ)**2,L,nphase,nmax)
        derivativeJ={k:(plus[k]-minus[k])/(2*dJ[:,None]) for k in fields}
        plus=harmonics(.5/(Jr+.5*(L+dL+np.sqrt((L+dL)**2+2)))**2,L+dL,nphase,nmax)
        minus=harmonics(.5/(Jr+.5*(L-dL+np.sqrt((L-dL)**2+2)))**2,L-dL,nphase,nmax)
        derivativeL={k:(plus[k]-minus[k])/(2*dL[:,None]) for k in fields}
    pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5);cohort=Cohort(pot)
    dE=df_step*np.minimum(E,1-E);f0=cohort(E)
    fplus=cohort(E+dE);fminus=cohort(E-dE)
    fE=(fplus-fminus)/(2*dE);fEE=(fplus-2*f0+fminus)/dE**2
    omr=frequency(E);omL=F*omr
    Hrr=-3/I**4;HrL=F*Hrr;HLL=F*F*Hrr+omr/(L*L+2)**1.5
    dt=np.maximum(times-tau,0.);offset=2*nmax
    result={}
    for observable in ('potential','radial_force','tangential_force'):
        arrays={k:np.zeros(len(times),complex) for k in ('total','echo2_radial_only','echo2_apsidal_only','echo2_two_frequency','declared_pair','nonrefocusing','first_A')}
        for aell in (() if first_only else (-2,0,2)):
            for bell in (-4,-2,0,2,4):
                mell=aell+bell
                if mell not in (-2,0,2):continue
                i0,ib,io=angular_integrals(aell,bell)
                _,direct_ib,direct_ia=direct_angular_integrals(aell,bell)
                for k in range(-nmax,nmax+1):
                    UA=fields['A',aell][:,k+offset]
                    AJ=derivativeJ['A',aell][:,k+offset];AL=derivativeL['A',aell][:,k+offset]
                    kf=-fE*(k*omr+aell*omL)
                    for n in range(-nmax,nmax+1):
                        m=k+n;B=fields['B',bell][:,n+offset];O=fields[observable,-mell][:,-m+offset]
                        BJ=derivativeJ['B',bell][:,n+offset];BL=derivativeL['B',bell][:,n+offset]
                        OJ=derivativeJ[observable,-mell][:,-m+offset];OL=derivativeL[observable,-mell][:,-m+offset]
                        stationary=i0*((m*BJ+mell*BL)*O+B*(n*OJ+bell*OL))+(ib+io)*B*O/L
                        contraction=n*(m*Hrr+mell*HrL)+bell*(m*HrL+mell*HLL)
                        secular=-1j*contraction*i0*B*O
                        phase=np.exp(-1j*((m*omr+mell*omL)[None,:]*times[:,None]-(n*omr+bell*omL)[None,:]*tau))
                        if formulation=='ibp':
                            integrand=(kf*UA)[None,:]*(stationary[None,:]+dt[:,None]*secular[None,:])
                        else:
                            Hnk=n*(k*Hrr+aell*HrL)+bell*(k*HrL+aell*HLL)
                            nkf=fEE*(k*omr+aell*omL)*(n*omr+bell*omL)-fE*Hnk
                            direct=i0*O*(kf*UA*(k*BJ+aell*BL)-B*(nkf*UA+kf*(n*AJ+bell*AL)))
                            direct+=(direct_ib-direct_ia)*kf*UA*B*O/L+1j*tau*Hnk*i0*kf*UA*B*O
                            integrand=direct[None,:]
                        pair=np.sum(weights[None,:]*integrand*phase,axis=1)
                        pair[times<tau]=0;arrays['total']+=pair
                        if n==2*m and bell==2*mell:
                            key='echo2_two_frequency' if m and mell else 'echo2_radial_only' if m else 'echo2_apsidal_only'
                            arrays[key]+=pair
                        else:arrays['nonrefocusing']+=pair
                        if (k,aell,n,bell)==(-1,-2,2,4):arrays['declared_pair']+=pair
        c,w=roots_legendre(5)
        for angular in (-2,0,2):
            incl,_=inclination(2,angular,c);orientation=np.sum(w*incl*incl)
            for k in range(-nmax,nmax+1):
                # Positive-node source coefficient from the real pulse.
                UA=np.conj(fields['A',-angular][:,-k+offset])
                O=fields[observable,-angular][:,-k+offset]
                kf=-fE*(k*omr+angular*omL)
                arrays['first_A']+=np.sum((1j*weights*kf*UA*O*orientation)[None,:]*np.exp(-1j*(k*omr+angular*omL)[None,:]*times[:,None]),axis=1)
        result.update({observable+'_'+key:value for key,value in arrays.items()})
    for pulse in ('A','B'):
        for observable in ('potential','radial_force'):
            array=np.zeros(len(times),complex)
            for k in range(-nmax,nmax+1):
                U=fields[pulse+'_monopole',0][:,k+offset];O=fields['monopole_'+observable,0][:,-k+offset]
                array+=np.sum((2j*weights*(-fE*k*omr)*U*O)[None,:]*np.exp(-1j*k*omr[None,:]*times[:,None]),axis=1)
            result['direct_'+pulse+'_monopole_'+observable]=array
    mass=float(np.sum(2*weights*cohort(E)))
    return result,dict(initial_absolute_cohort_mass=mass,phase_grid=nphase,radial_harmonic_cutoff=nmax,
        orientation_integrated_exactly_polynomial_nodes=5,
        maximum_negative_Hessian_determinant_error=float(np.max(abs(Hrr*HLL-HrL**2+3*I**-7/(L*L+2)**1.5))),
        positive_common_monopoles='Retained in direct first-order readouts; their higher-order effect on angular bilinear contrast is not included in this prediction.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--ne',type=int,default=64);p.add_argument('--nL',type=int,default=8)
    p.add_argument('--nphase',type=int,default=128);p.add_argument('--nmax',type=int,default=8)
    p.add_argument('--tau',type=float,default=16.);p.add_argument('--step-scale',type=float,default=1e-5)
    p.add_argument('--df-step',type=float,default=1e-4);p.add_argument('--first-only',action='store_true')
    p.add_argument('--relaxation-cadence',type=float)
    p.add_argument('--times',type=float,nargs='*');p.add_argument('--formulation',choices=['ibp','direct'],default='ibp');a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    for filename in ('echo_two_frequency.py','echo_monopole.py','echo_halo.py','echo_multipole_pulse.py'):
        (a.out/filename).write_bytes((Path(__file__).parent/filename).read_bytes())
    start,cpu=time.monotonic(),time.process_time()
    config=dict(pid=os.getpid(),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ne=a.ne,nL=a.nL,nphase=a.nphase,nmax=a.nmax,
        tau=a.tau,step_scale=a.step_scale,source_sha256=digest(__file__),actual_agama_module=agama.__file__,agama_binary_sha256=digest(agama.__file__),
        pulse_A=dict(ell=2,mass_integral=.006,scale=.8,epsilon=.5,orientation=0.),pulse_B=dict(ell=4,mass_integral=.010,scale=1.6,epsilon=.5,orientation=float(np.pi/8)),
        nice=os.getpriority(os.PRIO_PROCESS,0),self_gravity=False,formulation=a.formulation,first_only=a.first_only,relaxation_cadence=a.relaxation_cadence,df_fractional_step=a.df_step,method='Leading canonical bilinear response; exact polynomial inclinations and nodes')
    write(a.out/'config.json',config);print('PID',os.getpid(),a.out,flush=True)
    audit=checks();times=np.array(a.times) if a.times else np.arange(97. if a.first_only else 41.)
    if a.relaxation_cadence:
        assert a.first_only and a.relaxation_cadence>0
        intervals=[(0.,8.)]+[(.75*t,t) for t in (16.,32.,48.,64.)]
        times=np.unique(np.concatenate([np.linspace(lo,hi,round((hi-lo)/a.relaxation_cadence)+1) for lo,hi in intervals]))
    arrays,numerics=predict(a.ne,a.nL,a.nphase,a.nmax,times,a.tau,a.step_scale,a.formulation,a.first_only,a.df_step)
    np.savez_compressed(a.out/'response.npz',t=times,**arrays)
    result=dict(config=config,checks=audit,audits=numerics,cpu_seconds=time.process_time()-cpu,process_cpu_seconds=time.process_time(),wall_seconds=time.monotonic()-start,
        raw_sha256=digest(a.out/'response.npz'),scope='Mathematical second-order prediction for specified positive physical pulse shapes and gravitational readouts. Finite-amplitude, memory erasure, self-gravity and induced stellar signal remain unvalidated.')
    write(a.out/'result.json',result);(a.out/'COMPLETE').write_text('Leading two-frequency prediction completed; independent physical confirmation still required.\n');print(json.dumps(result,indent=2))

if __name__=='__main__':
    launch=time.monotonic()
    try:main()
    except Exception as error:
        if '--out' in sys.argv:
            path=Path(sys.argv[sys.argv.index('--out')+1])
            if path.is_dir():write(path/'FAILURE.json',dict(pid=os.getpid(),error=str(error),traceback=traceback.format_exc(),cpu_seconds=time.process_time(),wall_seconds=time.monotonic()-launch))
        raise
