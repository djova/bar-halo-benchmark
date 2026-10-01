"""Positive time-integrated Plummer density with a finite solid harmonic."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse, datetime, json, time
from pathlib import Path
import numpy as np
from echo_halo import agama,digest,write

class IntegratedMultipolePulse:
    def __init__(self,ell,mass_integral,scale,epsilon,orientation):
        assert ell in (2,4) and mass_integral>=0 and abs(epsilon)<1 and scale>0
        self.ell,self.mass,self.scale,self.epsilon,self.orientation=ell,mass_integral,scale,epsilon,orientation
        self.coefficient=-3*mass_integral*epsilon*2**ell/((2*ell+1)*(2*ell+3)*scale)

    def shape(self,position):
        y=np.asarray(position)/self.scale
        z=(y[...,0]+1j*y[...,1])*np.exp(-1j*self.orientation)
        q=(z**self.ell).real
        denominator=1+np.sum(y*y,axis=-1)
        return y,z,q,denominator

    def potential(self,position):
        _,_,q,d=self.shape(position)
        return -self.mass/self.scale/np.sqrt(d)+self.coefficient*q*d**(-self.ell-.5)

    def density(self,position):
        _,_,q,d=self.shape(position)
        baseline=3*self.mass/(4*np.pi*self.scale**3)*d**-2.5
        return baseline*(1+self.epsilon*2**self.ell*q/d**self.ell)

    def kick(self,position):
        y,z,q,d=self.shape(position);power=self.ell+.5
        dq=np.zeros_like(y)
        derivative=self.ell*z**(self.ell-1)*np.exp(-1j*self.orientation)/self.scale
        dq[...,0]=derivative.real;dq[...,1]=-derivative.imag
        gradient=(dq-2*power*q[...,None]*y/self.scale/d[...,None])*d[...,None]**-power
        return -self.mass*y/self.scale**2/d[...,None]**1.5-self.coefficient*gradient

    def gradient_bound(self):
        ell=self.ell;power=ell+.5
        x1=np.sqrt((ell-1)/(ell+2));x2=np.sqrt((ell+1)/(ell+2))
        first=x1**(ell-1)/(1+x1*x1)**power
        second=x2**(ell+1)/(1+x2*x2)**(power+1)
        multipole=abs(self.coefficient)/self.scale*(ell*first+2*power*second)
        monopole=2*self.mass/(3*np.sqrt(3)*self.scale**2)
        return dict(monopole=monopole,multipole_triangle=multipole,total=monopole+multipole)

def validate_source(pulse,rng):
    direction=rng.normal(size=(96,3));direction/=np.linalg.norm(direction,axis=1)[:,None]
    radius=pulse.scale*np.exp(rng.uniform(np.log(.1),np.log(5),len(direction)))
    position=radius[:,None]*direction
    h=1e-6*pulse.scale;grad=[];lap=[]
    for axis in np.eye(3):
        grad.append((pulse.potential(position+h*axis)-pulse.potential(position-h*axis))/(2*h))
        hh=2e-3*pulse.scale
        lap.append((-pulse.potential(position+2*hh*axis)+16*pulse.potential(position+hh*axis)
                    -30*pulse.potential(position)+16*pulse.potential(position-hh*axis)
                    -pulse.potential(position-2*hh*axis))/(12*hh*hh))
    actual=pulse.kick(position);reference=-np.array(grad).T
    rho=4*np.pi*pulse.density(position);lap=np.sum(lap,axis=0)
    difference=float(np.max(abs(actual-reference)))
    poisson_relative=float(np.max(abs(lap-rho)/rho))
    y,z,q,d=pulse.shape(position);ratio=1+pulse.epsilon*2**pulse.ell*q/d**pulse.ell
    result=dict(ell=pulse.ell,epsilon=pulse.epsilon,mass_integral=pulse.mass,scale=pulse.scale,
        orientation=pulse.orientation,Cartesian_gradient_max_difference=difference,
        independent_finite_difference_Poisson_max_relative_error=poisson_relative,
        minimum_sampled_density_over_Plummer=float(np.min(ratio)),
        rigorous_minimum_density_ratio=1-abs(pulse.epsilon),gradient_bound=pulse.gradient_bound())
    assert difference<1e-9 and poisson_relative<1e-5
    assert np.min(ratio)>=1-abs(pulse.epsilon)-1e-14
    assert np.max(np.linalg.norm(actual,axis=1))<=pulse.gradient_bound()['total']
    return result

def validate_canonical(ell,scale,epsilon,orientation,rng):
    pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5)
    mapper=agama.ActionMapper(pot);finder=agama.ActionFinder(pot)
    actions=np.array([[.05,.2,.3],[.2,.3,.2],[.5,.1,.4],[.07,.3,-.2],[.3,.2,-.5],[.8,.1,-.3]])
    angles=rng.uniform(.1,2*np.pi-.1,(len(actions),3));base=mapper(np.column_stack((actions,angles)))
    pulse=IntegratedMultipolePulse(ell,1.,scale,epsilon,orientation)
    grad_theta=[];grad_action=[];h=1e-5
    for axis in np.eye(3):
        plus=mapper(np.column_stack((actions,angles+h*axis)));minus=mapper(np.column_stack((actions,angles-h*axis)))
        grad_theta.append((pulse.potential(plus[:,:3])-pulse.potential(minus[:,:3]))/(2*h))
        plus=mapper(np.column_stack((actions+h*axis,angles)));minus=mapper(np.column_stack((actions-h*axis,angles)))
        grad_action.append((pulse.potential(plus[:,:3])-pulse.potential(minus[:,:3]))/(2*h))
    grad_theta=np.array(grad_theta).T;grad_action=np.array(grad_action).T
    rows=[]
    baseJ,baseTheta,_=finder(base,angles=True)
    for mass in (1e-5,1e-6,1e-7):
        final=base.copy();dv=pulse.kick(base[:,:3])*mass;final[:,3:]+=dv
        afterJ,afterTheta,_=finder(final,angles=True)
        dJ=(afterJ-baseJ)/mass;dTheta=np.angle(np.exp(1j*(afterTheta-baseTheta)))/mass
        actual_work=np.sum(base[:,3:]*dv,axis=1)+.5*np.sum(dv*dv,axis=1)
        kinetic_work=.5*np.sum(final[:,3:]**2-base[:,3:]**2,axis=1)
        rows.append(dict(mass_integral=mass,
            action_gradient_max_difference=float(np.max(abs(dJ+grad_theta))),
            angle_gradient_max_difference=float(np.max(abs(dTheta-grad_action))),
            exact_work_difference=float(np.max(abs(actual_work-kinetic_work)))))
    assert rows[-1]['action_gradient_max_difference']<1e-4
    assert rows[-1]['angle_gradient_max_difference']<1e-3
    return dict(ell=ell,rows=rows,
                scope='Canonical first-order kick and exact Cartesian external-work check; finite physical pulse is applied in Cartesian velocity.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False);(a.out/'source.py').write_bytes(Path(__file__).read_bytes())
    start,cpu=time.monotonic(),time.process_time();rng=np.random.default_rng(20261001)
    config=dict(pid=os.getpid(),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seed=20261001,
        source_sha256=digest(__file__),actual_agama_module=agama.__file__,agama_binary_sha256=digest(agama.__file__),nice=os.getpriority(os.PRIO_PROCESS,0),
        frozen_family=[dict(ell=2,mass_integral=.006,scale=.8,epsilon=.5,orientation=0.),
                       dict(ell=4,mass_integral=.010,scale=1.6,epsilon=.5,orientation=np.pi/8)],
        finite_amplitude_refinement='Both mass integrals divided by2; epsilon/spatial shapes fixed.',
        cohort_binding_floor=.02)
    write(a.out/'config.json',config);source=[];canonical=[];cost=0.
    for c in config['frozen_family']:
        for sign in (-1,1):
            pulse=IntegratedMultipolePulse(c['ell'],c['mass_integral'],c['scale'],c['epsilon']*sign,c['orientation'])
            source.append(validate_source(pulse,rng))
        bound=pulse.gradient_bound()['total'];cost+=np.sqrt(2)*bound+.5*bound*bound
        canonical.append(validate_canonical(c['ell'],c['scale'],c['epsilon'],c['orientation'],rng))
    assert cost<config['cohort_binding_floor']
    result=dict(config=config,source_checks=source,canonical_checks=canonical,
        global_two_pulse_binding_loss_bound=cost,guaranteed_minimum_binding_after_both=.02-cost,
        cpu_seconds=time.process_time()-cpu,process_cpu_seconds=time.process_time(),wall_seconds=time.monotonic()-start,
        scope='Positive integrated density and potential, Cartesian/canonical impulse and bound-support verification. No response measurement or physical encounter history.')
    write(a.out/'result.json',result);(a.out/'COMPLETE').write_text('Source/control preflight complete.\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
