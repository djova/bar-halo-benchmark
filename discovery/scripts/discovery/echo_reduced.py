"""Exact canonical two-kick echo control; replication, not a halo prediction."""
import os
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='1'
import argparse, hashlib, json, time
from pathlib import Path
import numpy as np
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OMEGA0=1.0
SHEAR=1.0
SIGMA=0.7

def grid(np_=512, nt=256):
    # Uniform momentum sampling resolves winding without Hermite alias revivals.
    spacing=18*SIGMA/np_
    p=-9*SIGMA+(np.arange(np_)+0.5)*spacing
    w=spacing*np.exp(-.5*(p/SIGMA)**2)/(np.sqrt(2*np.pi)*SIGMA)
    theta=2*np.pi*(np.arange(nt)+0.5)/nt
    return np.repeat(p,nt),np.tile(theta,np_),np.repeat(w/nt,nt)

def state_at_second(p,theta,a1,n1,tau):
    p=p+a1*n1*np.sin(n1*theta)
    return p,np.remainder(theta+(OMEGA0+SHEAR*p)*tau,2*np.pi)

def coefficients(p,theta,weights,times,a1,a2,n1,n2,tau):
    p,theta=state_at_second(p,theta,a1,n1,tau)
    p=p+a2*n2*np.sin(n2*theta)
    m=n2-n1
    return np.array([np.sum(weights*np.exp(-1j*m*(theta+(OMEGA0+SHEAR*p)*(t-tau)))) for t in times])

def mixed(p,theta,weights,times,a,n1,n2,tau):
    cases={label:coefficients(p,theta,weights,times,a1,a2,n1,n2,tau)
           for label,a1,a2 in [('AB',a,a),('A',a,0),('B',0,a),('0',0,0)]}
    return cases,cases['AB']-cases['A']-cases['B']+cases['0']

def prediction(times,a1,a2,n1,n2,tau):
    m=n2-n1
    delta=m*times-n2*tau
    characteristic=np.exp(-1j*OMEGA0*delta-0.5*(SIGMA*SHEAR*delta)**2)
    return -a1*a2*n1*n2*m*SHEAR**2*(times-tau)*delta*characteristic/4

def independent_df(t,a1,a2,n1,n2,tau):
    m=n2-n1
    delta=m*t-n2*tau
    def integrand(p):
        f=np.exp(-0.5*(p/SIGMA)**2)/(np.sqrt(2*np.pi)*SIGMA)
        fp=-p*f/SIGMA**2
        fpp=(p*p/SIGMA**4-1/SIGMA**2)*f
        coefficient=a1*a2*n1*n2*(fpp+1j*n1*SHEAR*tau*fp)/4
        return coefficient*np.exp(-1j*(OMEGA0+SHEAR*p)*delta)
    return quad(lambda p:integrand(p).real,-10*SIGMA,10*SIGMA,epsabs=1e-12)[0]+1j*quad(lambda p:integrand(p).imag,-10*SIGMA,10*SIGMA,epsabs=1e-12)[0]

def scrambled(p,theta,weights,times,a,n1,n2,tau):
    # Exact angle projection preserves the full discrete p marginal.
    fresh=2*np.pi*(np.arange(64)+0.5)/64
    values=[]
    for a1,a2 in [(a,a),(a,0),(0,a),(0,0)]:
        pp,_=state_at_second(p,theta,a1,n1,tau)
        pp=pp[:,None]+a2*n2*np.sin(n2*fresh)[None,:]
        ww=weights[:,None]/len(fresh)
        values.append(np.array([np.sum(ww*np.exp(-1j*(n2-n1)*(fresh[None,:]+(OMEGA0+SHEAR*pp)*(t-tau)))) for t in times]))
    return values[0]-values[1]-values[2]+values[3]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'source.py').write_bytes(Path(__file__).read_bytes())
    start,cpu=time.monotonic(),time.process_time()
    p,theta,weights=grid()
    rows=[]
    fig,axes=plt.subplots(2,2,figsize=(11,8))
    for n2 in (2,3):
        for tau in (8.,12.,16.):
            m=n2-1
            te=n2*tau/m
            times=np.linspace(tau,te+5/(m*SIGMA*SHEAR),241)
            for a in (0.0025,0.005,0.01):
                cases,cross=mixed(p,theta,weights,times,a,1,n2,tau)
                analytic=prediction(times,a,a,1,n2,tau)
                scale=np.max(abs(analytic))
                near=abs(times-te)<4/(m*SIGMA*SHEAR)
                lobe=int(np.argmax(abs(cross)))
                row=dict(n1=1,n2=n2,tau=tau,amplitude=a,refocusing_time=te,
                    peak_time=float(times[lobe]),peak_abs=float(abs(cross[lobe])),
                    relative_waveform_error=float(np.max(abs(cross[near]-analytic[near]))/scale),
                    mixed_at_refocusing=coefficients(p,theta,weights,[te],a,a,1,n2,tau)[0])
                # Complex values are saved in raw arrays; JSON uses a two-real representation.
                row['mixed_at_refocusing']=[float(cross[np.argmin(abs(times-te))].real),float(cross[np.argmin(abs(times-te))].imag)]
                name=f'n{n2}-tau{tau:g}-a{a:g}'
                np.savez_compressed(args.out/(name+'.npz'),t=times,mixed=cross,analytic=analytic,**cases)
                rows.append(row)
                if a==0.005:
                    axes[0,n2-2].plot(times-te,abs(cross)/a**2,label=f'tau={tau:g}')
                    axes[1,n2-2].plot(times-te,np.real(cross*np.exp(1j*OMEGA0*(m*times-n2*tau)))/a**2,label=f'tau={tau:g}')
    coarse_t=np.linspace(12,28,101)
    _,coarse=mixed(p,theta,weights,coarse_t,.0025,1,2,12.)
    p2,theta2,w2=grid(1024,384)
    _,fine=mixed(p2,theta2,w2,coarse_t,.0025,1,2,12.)
    selected=np.array([22.,23.,24.,25.,26.])
    # Symmetry makes the memory-erasure result independent of marginal resolution.
    sp,st,sw=grid(48,128)
    scr=scrambled(sp,st,sw,selected,.005,1,2,12.)
    checks={
        'quadrature_absolute_difference':float(np.max(abs(coarse-fine))),
        'independent_df_absolute_difference':float(max(abs(independent_df(t,.005,.005,1,2,12.)-prediction(t,.005,.005,1,2,12.)) for t in selected)),
        'scrambled_mixed_absolute_max':float(max(abs(scr))),
        'finest_amplitude_waveform_error_max':max(r['relative_waveform_error'] for r in rows if r['amplitude']==.0025),
    }
    gates=dict(quadrature=checks['quadrature_absolute_difference']<1e-10,
               independent_df=checks['independent_df_absolute_difference']<1e-10,
               memory_erasure=checks['scrambled_mixed_absolute_max']<1e-10,
               perturbative_convergence=checks['finest_amplitude_waveform_error_max']<.05)
    for j,n2 in enumerate((2,3)):
        axes[0,j].set_title(f'n1=1, n2={n2}: mixed density echo')
        axes[0,j].set_ylabel('|C_mixed| / a^2')
        axes[1,j].set_ylabel('Demodulated real C_mixed / a^2')
        for i in (0,1):
            axes[i,j].set_xlabel('t - analytic refocusing time')
            axes[i,j].axvline(0,color='black',lw=.7)
            axes[i,j].legend()
    fig.tight_layout();fig.savefig(args.out/'reduced-echo.png',dpi=160);fig.savefig(args.out/'reduced-echo.pdf')
    result=dict(scope='Known constant-shear collisionless echo replicated on a canonical cylinder; no halo or live gravity claim.',
        rows=rows,checks=checks,gates=gates,all_pass=all(gates.values()),
        parameters=dict(omega0=OMEGA0,shear=SHEAR,sigma=SIGMA,p_nodes=512,theta_nodes=256,momentum_sampler='midpoint uniform over +/-9 sigma'),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        nice=os.getpriority(os.PRIO_PROCESS,0))
    (args.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.out/'COMPLETE').write_text('Completed known-limit echo control. Inspect all_pass.\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))

if __name__=='__main__':main()
