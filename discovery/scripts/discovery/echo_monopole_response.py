"""Independent second-order canonical harmonic prediction for physical radial pulses.

At fixed L, f1_A=f0'(Jr)*d_theta U_A. The B pulse applies
-{f1_A,U_B}. Integrating its action derivative by parts gives the
observable response below. This isolates genuine refocusing channels before
comparison with exact positive-pulse inverse histories.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
import argparse, datetime, json, time
from pathlib import Path
import numpy as np
from scipy.special import roots_legendre,ndtr
from echo_monopole import Cohort, radial_map, frequency, agama, digest, write
from echo_halo import annulus_kernel

def phase_coefficients(E,L,nphase,nmax,observable):
    phase=2*np.pi*(np.arange(nphase)+.5)/nphase
    r,_=radial_map(E[:,None],L[:,None],phase[None,:])
    if observable=='potential':value=-annulus_kernel(r,1.,0,.1)
    elif observable=='radial_force':value=-np.exp(.02)*ndtr(-np.log(r)/.1-.2)
    elif observable=='potential_difference':value=-annulus_kernel(r,.5,0,.1)+annulus_kernel(r,1.,0,.1)
    else:raise ValueError(observable)
    fields=np.array([-1/np.sqrt(r*r+.5**2),-1/np.sqrt(r*r+1.5**2),value])
    coeff=np.fft.fft(fields,axis=2)/nphase
    harmonics=np.arange(-2*nmax,2*nmax+1)
    return coeff[:,:,harmonics % nphase]*np.exp(-1j*harmonics*np.pi/nphase)[None,None,:]

def one_angle_check():
    # The same integration-by-parts formula, with constant-frequency shear,
    # recovers the independently derived complex canonical-cylinder control.
    from scipy.integrate import quad
    n1,n2,tau,t,sigma,s=1,2,8.,15.,.7,1.
    k,n,m=-n1,n2,n2-n1;delta=m*t-n*tau
    factor=-1j*n*k*m*(t-tau)*s/4
    def integrand(p):
        f=np.exp(-p*p/(2*sigma*sigma))/(np.sqrt(2*np.pi)*sigma)
        return factor*(-p/sigma**2)*f*np.exp(-1j*delta*(1+s*p))
    val=quad(lambda p:integrand(p).real,-9*sigma,9*sigma,epsabs=1e-13)[0]+1j*quad(lambda p:integrand(p).imag,-9*sigma,9*sigma,epsabs=1e-13)[0]
    exact=-n1*n2*m*s*s*(t-tau)*delta/4*np.exp(-1j*delta-(sigma*s*delta)**2/2)
    return float(abs(val-exact))

def predict(ne,nL,nphase,nmax,times,tau,cohort,step_scale,observable):
    x,wE=roots_legendre(ne);E=.02+.98*(x+1)/2;wE=wE*.98/2
    x,wL=roots_legendre(nL);la=(x+1)/2;wL=wL/2
    E,la=np.meshgrid(E,la,indexing='ij')
    Lmax=(1-E)/np.sqrt(2*E);L=la*Lmax
    weights=(2*np.pi)**3*wE[:,None]*wL[None,:]*2*L*Lmax*(2*E)**-1.5
    E,L,weights=E.ravel(),L.ravel(),weights.ravel()
    I=1/np.sqrt(2*E);Jr=I-.5*(L+np.sqrt(L*L+2))
    step=np.minimum(step_scale*(1+Jr),.002*Jr)
    Ep=.5/(I+step)**2;Em=.5/(I-step)**2
    coefficients=phase_coefficients(E,L,nphase,nmax,observable)
    derivatives=(phase_coefficients(Ep,L,nphase,nmax,observable)-phase_coefficients(Em,L,nphase,nmax,observable))/(2*step[None,:,None])
    fprime=(cohort(Ep)-cohort(Em))/(2*step)
    om=frequency(E);omprime=-3*om*om/(2*E)
    total=np.zeros(len(times),complex);echo12=np.zeros_like(total);echo23=np.zeros_like(total)
    echo2tau=np.zeros_like(total);echo3tau=np.zeros_like(total)
    first=np.zeros_like(total);maximum_pair_imaginary=0.
    offset=2*nmax
    for k in range(-nmax,nmax+1):
        if k==0:continue
        ua=coefficients[0,:,k+offset]
        oo=coefficients[2,:,-k+offset]
        first+=np.sum((weights*fprime*1j*k*ua*oo)[None,:]*np.exp(-1j*k*times[:,None]*om[None,:]),axis=1)
        for n in range(-nmax,nmax+1):
            m=k+n
            ub=coefficients[1,:,n+offset];dub=derivatives[1,:,n+offset]
            oo=coefficients[2,:,-m+offset];doo=derivatives[2,:,-m+offset]
            stationary=(k*m*dub*oo+n*k*ub*doo)
            secular=-1j*n*k*m*omprime*ub*oo
            dt=np.maximum(times-tau,0.)
            phase=np.exp(-1j*(m*times[:,None]-n*tau)*om[None,:])
            pair=np.sum((weights*fprime*ua)[None,:]*(stationary[None,:]+dt[:,None]*secular[None,:])*phase,axis=1)
            pair[times<tau]=0
            total+=pair
            if (k,n) in [(-1,2),(1,-2)]:echo12+=pair
            if (k,n) in [(-2,3),(2,-3)]:echo23+=pair
            if m and 2*m==n:echo2tau+=pair
            if m and 3*m==n:echo3tau+=pair
            maximum_pair_imaginary=max(maximum_pair_imaginary,float(np.max(abs(pair.imag))))
    return dict(total=total,echo12=echo12,echo23=echo23,echo2tau=echo2tau,echo3tau=echo3tau,first=first),dict(
        phase_symmetry_imaginary_residual=float(max(np.max(abs(total.imag)),np.max(abs(first.imag)))),
        zero_time_first_response=float(abs(first[0])) if times[0]==0 else None,
        instantaneous_B_mixed_response=float(abs(total[np.flatnonzero(times==tau)[0]])) if tau in times else None,
        integrated_initial_cohort_mass=float(np.sum(weights*cohort(E))),
        minimum_action_difference_step=float(np.min(step)),
        maximum_action_difference_step=float(np.max(step)))

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--ne',type=int,default=256);p.add_argument('--nL',type=int,default=32)
    p.add_argument('--nphase',type=int,default=512);p.add_argument('--nmax',type=int,default=12)
    p.add_argument('--tau',type=float,default=16.);p.add_argument('--cadence',type=float,default=.5)
    p.add_argument('--end-factor',type=float,default=3.5)
    p.add_argument('--observable',choices=['potential','radial_force','potential_difference'],default='potential')
    p.add_argument('--times',nargs='*',type=float);p.add_argument('--step-scale',type=float,default=1e-5)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'source.py').write_bytes(Path(__file__).read_bytes());(a.out/'echo_monopole_import.py').write_bytes((Path(__file__).parent/'echo_monopole.py').read_bytes())
    start,cpu=time.monotonic(),time.process_time()
    config=dict(pid=os.getpid(),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                ne=a.ne,nL=a.nL,nphase=a.nphase,nmax=a.nmax,tau=a.tau,cadence=a.cadence,end_factor=a.end_factor,step_scale=a.step_scale,
                source_sha256=digest(__file__),actual_agama_module=agama.__file__,agama_binary_sha256=digest(agama.__file__),
                pulse_A_scale=.5,pulse_B_scale=1.5,primary_radius=1.,radial_log_width=.1,observable=a.observable,nice=os.getpriority(os.PRIO_PROCESS,0))
    write(a.out/'config.json',config)
    analytic_error=one_angle_check();assert analytic_error<1e-12
    times=np.array(a.times) if a.times else np.arange(round(a.end_factor*a.tau/a.cadence)+1)*a.cadence
    pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5);cohort=Cohort(pot)
    values,audits=predict(a.ne,a.nL,a.nphase,a.nmax,times,a.tau,cohort,a.step_scale,a.observable)
    np.savez_compressed(a.out/'response.npz',t=times,**values)
    result=dict(config=config,analytic_one_angle_error=analytic_error,audits=audits,
                cpu_seconds=time.process_time()-cpu,process_cpu_seconds=time.process_time(),
                wall_seconds=time.monotonic()-start,raw_sha256=digest(a.out/'response.npz'),
                scope='Independent leading-order gravitational readout by physical-pulse radial harmonic channels. Not an exact finite-amplitude or self-gravitating calculation.')
    write(a.out/'result.json',result);(a.out/'COMPLETE').write_text('Harmonic prediction complete; refinement and exact-response comparison required.\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
