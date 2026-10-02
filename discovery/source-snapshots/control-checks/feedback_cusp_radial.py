"""Conditional canonical warm radial known-map preflight; no gas-pulse evolution."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
from functools import lru_cache
import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr,ndtri,roots_legendre,roots_laguerre

ROOT=Path(__file__).resolve().parents[2]
PROTOCOL=ROOT/'research/discovery-20261001/FEEDBACK_CUSP_RADIAL_PREFLIGHT_PROTOCOL.md'
EXPECTED='1041bce973f4129cf5b6e38592cbafa8627485f448b94a982ece2c94120d1705'
N=512
SELECT=np.array([0,17,63,127,255,511])
PHI0=-1.2900604555052089


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,value):
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False,
        default=lambda x:x.item() if isinstance(x,np.generic) else (_ for _ in ()).throw(TypeError(type(x).__name__)))+'\n')
def stat(x):return dict(mean=float(x.mean()),standard_error=float(x.std(ddof=1)/np.sqrt(len(x))))


@lru_cache(None)
def legendre(count):
    x,w=roots_legendre(count);return (x+1)/2,w/2


def fields(r):
    r=np.asarray(r);phi=-1/(1+r);first=1/(1+r)**2;second=-2/(1+r)**3
    for s in (.2,1.3):
        norm=8**3/(64+s*s)**1.5;root=np.sqrt(r*r+s*s);inside=r<8
        phi=phi+np.where(inside,-.05*(1/root-s*s/(64+s*s)**1.5)/norm,-.05/r)
        first=first+np.where(inside,.05*r/root**3/norm,.05/r**2)
        second=second+np.where(inside,.05*(s*s-2*r*r)/root**5/norm,-.1/r**3)
    return phi,first,second


class Radial:
    def __init__(self,Rc):
        self.Rc=float(Rc);p,f,s=fields(np.array([Rc]));self.vc=float(np.sqrt(Rc*f[0]));self.L=Rc*self.vc
        self.kappa=float(np.sqrt(s[0]+3*f[0]/Rc));self.Js=(.1*self.vc)**2/self.kappa
        self.Ec=float(p[0]+.5*self.vc**2);self.D=-self.Ec
        lower=self.L/(2*np.sqrt(-2*PHI0))
        self.rmin=float(brentq(lambda r:float(fields(np.array([r]))[0][0]+.5*self.L**2/r**2),lower,Rc,
            xtol=np.nextafter(0.,1.),rtol=8*np.finfo(float).eps))

    def difference(self,r):
        """Rationalized Veff(r)-Veff(Rc); Rc is always below the cutoff."""
        r=np.asarray(r);c=self.Rc;d=r-c
        result=d*d*((2+c)*r+c)/(2*r*r*(1+r)*(1+c)**2)
        for s in (.2,1.3):
            uc=np.sqrt(c*c+s*s);ur=np.sqrt(r*r+s*s);norm=8**3/(64+s*s)**1.5
            stable=.05/norm*d*d*(r+c)**2*(c*c+2*s*s-c*c*uc/(ur+uc))/(2*r*r*ur*uc**3*(ur+uc))
            phi_r=np.where(r<8,-.05*(1/ur-s*s/(64+s*s)**1.5)/norm,-.05/r)
            phi_c=-.05*(1/uc-s*s/(64+s*s)**1.5)/norm
            Lc2=.05*c**4/uc**3/norm
            exterior=phi_r-phi_c+.5*Lc2*(1/r**2-1/c**2)
            result+=np.where(r<8,stable,exterior)
        return result

    def action_period(self,delta,count=128):
        delta=np.asarray(delta,dtype=float);shape=delta.shape;values=delta.ravel()
        if np.any(values<0):raise RuntimeError('Energy below circular minimum; no clipping.')
        J=np.full(len(values),np.inf);Omega=np.zeros(len(values));J[values==0]=0;Omega[values==0]=self.kappa
        ids=np.flatnonzero((values>0)&(values<self.D));t,w=legendre(count)
        for offset in range(0,len(ids),1024):
            chosen=ids[offset:offset+1024];e=values[chosen]
            lo=np.full(len(e),self.rmin);hi=np.full(len(e),self.Rc)
            if np.any(self.difference(lo)<e):raise RuntimeError('Inner bracket failure.')
            for _ in range(64):
                middle=(lo+hi)/2;left=self.difference(middle)>e
                lo=np.where(left,middle,lo);hi=np.where(left,hi,middle)
            rp=(lo+hi)/2;lo=np.full(len(e),self.Rc);hi=2.2/(self.D-e)
            if np.any(self.difference(hi)<e):raise RuntimeError('Outer bracket failure.')
            for _ in range(64):
                middle=(lo+hi)/2;left=self.difference(middle)<e
                lo=np.where(left,middle,lo);hi=np.where(left,hi,middle)
            ra=(lo+hi)/2;cut=np.full(len(e),np.pi/2);cross=ra>8
            cut[cross]=np.arcsin(np.sqrt((8-rp[cross])/(ra[cross]-rp[cross])))
            action=np.zeros(len(e));period=np.zeros(len(e))
            for begin,end in ((np.zeros(len(e)),cut),(cut,np.full(len(e),np.pi/2))):
                active=end>begin
                if not np.any(active):continue
                angle=begin[active,None]+(end-begin)[active,None]*t
                radius=rp[active,None]+(ra-rp)[active,None]*np.sin(angle)**2
                dr=(ra-rp)[active,None]*np.sin(2*angle)*(end-begin)[active,None]
                Q=2*(e[active,None]-self.difference(radius))
                if np.any(Q<=0):raise RuntimeError('Nonpositive interior radial quadrature; retain failure, no clipping.')
                p=np.sqrt(Q);action[active]+=np.sum(w*p*dr,axis=1)/np.pi
                period[active]+=np.sum(w*dr/p,axis=1)
            J[chosen]=action;Omega[chosen]=np.pi/period
        return J.reshape(shape),Omega.reshape(shape)

    def target(self,delta,count=128):
        J,om=self.action_period(delta,count);inside=(np.asarray(delta)>=0)&(np.asarray(delta)<self.D)
        g=np.zeros_like(J);slope=np.zeros_like(J)
        g[inside]=np.exp(-J[inside]/self.Js)/(2*np.pi*self.Js)
        slope[inside]=g[inside]/(self.Js*om[inside])
        if np.any(~np.isfinite(g)) or np.any(~np.isfinite(slope)) or np.any(slope<0):raise RuntimeError('Passive conditional target failure.')
        return J,om,g,slope

    def energy_from_action(self,J,count):
        lo=np.zeros_like(J);hi=np.full_like(J,self.D)
        for _ in range(52):
            middle=(lo+hi)/2;value,_=self.action_period(middle,count)
            left=value<J;lo=np.where(left,middle,lo);hi=np.where(left,hi,middle)
        return (lo+hi)/2

    def reference(self,countJ,countR):
        y,wy=roots_laguerre(countJ);J=self.Js*y;d=self.energy_from_action(J,countR)
        # Independent time averages on each energy surface.
        t,w=legendre(countR);lo=np.full(len(d),self.rmin);hi=np.full(len(d),self.Rc)
        for _ in range(64):
            mid=(lo+hi)/2;left=self.difference(mid)>d;lo=np.where(left,mid,lo);hi=np.where(left,hi,mid)
        rp=(lo+hi)/2;lo=np.full(len(d),self.Rc);hi=2.2/(self.D-d)
        for _ in range(64):
            mid=(lo+hi)/2;left=self.difference(mid)<d;lo=np.where(left,mid,lo);hi=np.where(left,hi,mid)
        ra=(lo+hi)/2;cut=np.full(len(d),np.pi/2);cross=ra>8
        cut[cross]=np.arcsin(np.sqrt((8-rp[cross])/(ra[cross]-rp[cross])))
        integrals={k:np.zeros(len(d)) for k in ('time','radius','p2','known_energy')}
        for begin,end in ((np.zeros(len(d)),cut),(cut,np.full(len(d),np.pi/2))):
            use=end>begin;angle=begin[use,None]+(end-begin)[use,None]*t
            radius=rp[use,None]+(ra-rp)[use,None]*np.sin(angle)**2
            dr=(ra-rp)[use,None]*np.sin(2*angle)*(end-begin)[use,None]
            Q=2*(d[use,None]-self.difference(radius))
            if np.any(Q<=0):raise RuntimeError('Independent reference nonpositive radicand.')
            factor=w*dr/np.sqrt(Q)
            for key,value in [('time',np.ones_like(radius)),('radius',radius),('p2',Q),
                              ('known_energy',.5*(.2*radius*np.exp(-radius))**2)]:
                integrals[key][use]+=np.sum(factor*value,axis=1)
        return {k:float(wy@(v/integrals['time'])) for k,v in integrals.items() if k!='time'}


def sample(model,rng):
    label=rng.random(N)<.5;u=rng.random(N);v=rng.random(N);R=1+model.Rc
    lower=ndtr(np.log(model.rmin/model.Rc)/.2)
    near=model.Rc*np.exp(.2*ndtri(lower+(1-lower)*u))
    radius=np.where(label,model.rmin+R*u/(1-u),near)
    vmax2=2*(model.D-model.difference(radius))
    if np.any(vmax2<=0):raise RuntimeError('Invalid bound sampling domain; no rejection repair.')
    vmax=np.sqrt(vmax2);sigma=.1*model.vc;plow=ndtr(-vmax/sigma);pwidth=ndtr(vmax/sigma)-plow
    pr=np.where(label,vmax*(2*v-1),sigma*ndtri(plow+pwidth*v))
    tail=R/((radius-model.rmin+R)**2*2*vmax)
    near_r=np.exp(-.5*(np.log(radius/model.Rc)/.2)**2)/(radius*.2*np.sqrt(2*np.pi)*(1-lower))
    near_p=np.exp(-.5*(pr/sigma)**2)/(sigma*np.sqrt(2*np.pi)*pwidth)
    q=.5*(tail+near_r*near_p);delta=model.difference(radius)+.5*pr*pr
    if np.any(delta>=model.D) or np.any(~np.isfinite(q)) or np.any(q<=0):raise RuntimeError('Sampling endpoint/density failure.')
    recovered_u=np.where(label,(radius-model.rmin)/(radius-model.rmin+R),
        (ndtr(np.log(radius/model.Rc)/.2)-lower)/(1-lower))
    recovered_v=np.where(label,.5*(pr/vmax+1),(ndtr(pr/sigma)-plow)/pwidth)
    cdf=[]
    for name,values in [('radius',recovered_u),('momentum',recovered_v)]:
        for cutoff in (.1,.25,.5,.75,.9):
            observed=float(np.mean(values<cutoff));se=np.sqrt(cutoff*(1-cutoff)/N)
            cdf.append(dict(variable=name,cutoff=cutoff,observed=observed,standard_error=float(se),pass_gate=abs(observed-cutoff)<5*se))
    return dict(radius=radius,pr=pr,delta=delta,q=q,component=label,u=u,v=v),dict(cdf=cdf,
        maximum_CDF_recovery_error=float(max(abs(recovered_u-u).max(),abs(recovered_v-v).max())),
        pass_gate=all(z['pass_gate'] for z in cdf) and max(abs(recovered_u-u).max(),abs(recovered_v-v).max())<1e-12)


def curvature(model,initial,final,count,action_count=128):
    t,w=legendre(count);change=final-initial
    points=initial[:,None]+change[:,None]*t
    _,_,_,slope=model.target(points.ravel(),action_count);slope=slope.reshape(points.shape)
    return change**2*np.sum(w*(1-t)*slope,axis=1)


def primitive(model,delta,count):
    t,w=legendre(count);distance=model.D-delta
    points=delta[:,None]+distance[:,None]*t*t
    _,_,g,_=model.target(points.ravel());g=g.reshape(points.shape)
    return np.sum(w*2*distance[:,None]*t*g,axis=1)


def free(model,r,p,h):
    R=np.sqrt((r+h*p)**2+(h*model.L/r)**2)
    P=(r*p+h*(p*p+model.L**2/r**2))/R
    return R,P


def free_control(model,z):
    r=z['radius'][SELECT];p=z['pr'][SELECT];h=.1/model.kappa;R,P=free(model,r,p,h);r0,p0=free(model,R,P,-h)
    cartx=np.column_stack((r+h*p,h*model.L/r,np.zeros(len(r))))
    cartv=np.column_stack((p,model.L/r,np.zeros(len(r))))
    reference_r=np.linalg.norm(cartx,axis=1);reference_p=np.sum(cartx*cartv,axis=1)/reference_r
    epsr=1e-5*r;epsp=1e-5*np.maximum(abs(p),.1*model.vc)
    Ra,Pa=free(model,r+epsr,p,h);Rb,Pb=free(model,r-epsr,p,h)
    Rc,Pc=free(model,r,p+epsp,h);Rd,Pd=free(model,r,p-epsp,h)
    determinant=(Ra-Rb)*(Pc-Pd)/(4*epsr*epsp)-(Rc-Rd)*(Pa-Pb)/(4*epsr*epsp)
    error=float(max((abs(R-reference_r)/(1+r)).max(),(abs(P-reference_p)/(1+abs(p))).max(),
        (abs(r0-r)/(1+r)).max(),(abs(p0-p)/(1+abs(p))).max()))
    return dict(selected_indices=SELECT.tolist(),step=h,scaled_cartesian_inverse_error=error,
        determinant=determinant.tolist(),maximum_determinant_error=float(abs(determinant-1).max()),
        pass_gate=error<1e-10 and abs(determinant-1).max()<1e-5)


def difference_control(radii):
    """Independent direct potential subtraction away from cancellation."""
    rows=[]
    for Rc in radii:
        model=Radial(Rc)
        radius=np.concatenate((Rc*np.array([.2,.5,.9,1.1,2.,4.]),np.array([7.9,8.,8.1,100.])))
        direct=fields(radius)[0]+.5*model.L**2/radius**2-model.Ec
        stable=model.difference(radius)
        scaled=abs(stable-direct)/np.maximum(abs(direct),1e-14)
        steps=np.array([1e-3,1e-4,1e-5]);near=Rc*(1+np.concatenate((-steps,steps)))
        quadratic=.5*model.kappa**2*(near-Rc)**2
        ratio=model.difference(near)/quadratic
        local_error=abs(ratio-1)
        rows.append(dict(Rc=Rc,radius=radius.tolist(),direct=direct.tolist(),rationalized=stable.tolist(),
            relative_errors=scaled.tolist(),near_radius=near.tolist(),local_quadratic_ratios=ratio.tolist(),
            maximum_direct_relative_error=float(scaled.max()),
            smallest_offset_local_relative_error=float(max(local_error[2],local_error[5])),
            pass_gate=bool(scaled.max()<1e-10 and local_error.max()<.01
                and max(local_error[2],local_error[5])<1e-4)))
    return dict(rows=rows,pass_gate=all(row['pass_gate'] for row in rows),
        interpretation='Direct subtraction away from cancellation and independent local epicycle limit; no orbit response.')


def block(model,rng,out,index):
    started=time.process_time();z,sampling=sample(model,rng)
    np.savez_compressed(out/f'proposal-{index}.npz',**z)
    J,om,g,slope=model.target(z['delta']);z.update(Jr=J,Omega=om,g=g,slope=slope)
    Jfine,ofine,gfine,_=model.target(z['delta'],256)
    np.savez_compressed(out/f'initial-{index}.npz',**z,Jr256=Jfine,Omega256=ofine,g256=gfine)
    first=model.reference(24,64);second=model.reference(48,128)
    weight=g/z['q'];moments=[]
    for name,values,truth,old in [('mass',weight,1.,1.),('radius',weight*z['radius'],second['radius'],first['radius']),
        ('p2',weight*z['pr']**2,second['p2'],first['p2'])]:
        observed=stat(values);moments.append(dict(moment=name,sample=observed,predicted=truth,reference_old=old,
            pass_gate=abs(observed['mean']-truth)<5*observed['standard_error']+abs(truth-old)))
    kick=.2*z['radius']*np.exp(-z['radius']);forward=model.difference(z['radius'])+.5*(z['pr']+kick)**2
    inverse=model.difference(z['radius'])+.5*(z['pr']-kick)**2
    raw={};means=[]
    exits=inverse>=model.D
    for count in (32,64):
        R=curvature(model,z['delta'],forward,count);support=np.zeros(N)
        support[exits]=primitive(model,z['delta'][exits],count)
        estimate=(R+support)/z['q'];raw['R'+str(count)]=R;raw['support'+str(count)]=support
        raw['positive'+str(count)]=estimate;means.append(stat(estimate))
    ordinary=weight*(z['pr']*kick+.5*kick*kick);quadrature=stat(raw['positive64']-raw['positive32'])
    zero=curvature(model,z['delta'],z['delta'],32)
    assert np.all(zero==0),'Known zero map remainder is not exactly zero.'
    selected_R256=curvature(model,z['delta'][SELECT],forward[SELECT],64,256)
    selected_remainder_difference=(selected_R256-raw['R64'][SELECT])/z['q'][SELECT]/N
    known=second['known_energy'];reference_change=abs(known-first['known_energy']);value=means[1]
    fixed=z['delta'][SELECT];distance=np.minimum(fixed,model.D-fixed);h=.0001*distance
    jp,_=model.action_period(fixed+h,256);jm,_=model.action_period(fixed-h,256)
    derivative=(jp-jm)/(2*h);jerror=abs(derivative*ofine[SELECT]-1)
    freecheck=free_control(model,z)
    # Direct forward/inverse signed energies and capture operands remain separate.
    np.savez_compressed(out/f'known-map-{index}.npz',**raw,forward_delta=forward,inverse_delta=inverse,
        ordinary_signed=ordinary,kick=kick,capture_mask=exits,known_mean=np.array(known),
        zero_remainder=zero,zero_support=np.zeros(N),selected_R256=selected_R256)
    gates=dict(sampling=sampling['pass_gate'],moments=all(x['pass_gate'] for x in moments),
        known_mean=abs(value['mean']-known)<4*value['standard_error']+reference_change+abs(quadrature['mean']),
        precision=value['standard_error']<.25*known,quadrature=abs(quadrature['mean'])<.005*known,
        derivative=float(jerror.max())<1e-4,canonical_free=freecheck['pass_gate'])
    return dict(Rc=model.Rc,L=model.L,Js=model.Js,kappa=model.kappa,rmin=model.rmin,energy_circular=model.Ec,
        n=N,sampling=sampling,moments=moments,independent_reference_old=first,independent_reference=second,
        target_g128_to256=stat((gfine-g)/z['q']),passive_slope_minimum=float(slope.min()),
        numerical_underflow_count=int(np.sum(g==0)),ordinary_signed=stat(ordinary),positive32=means[0],positive64=means[1],
        quadrature_difference=quadrature,forward_unbound_count=int(np.sum(forward>=model.D)),
        inverse_unbound_count=int(exits.sum()),inverse_support_mean=float(np.mean(raw['support64']/z['q'])),
        selected_remainder128_to256_partial_difference=selected_remainder_difference.tolist(),
        selected_refinement_scope='Fixed selected paths only; no omitted-state error bound.',
        selected_action_derivative_relative_errors=jerror.tolist(),canonical_free=freecheck,gates=gates,
        gate=all(gates.values()),cpu_seconds=time.process_time()-started)


def run(args):
    resource.setrlimit(resource.RLIMIT_CPU,(240,245));started=time.process_time()
    assert sha(args.preflight/'result.json')==EXPECTED,'Frozen actual-potential preflight mismatch.'
    source=sha(__file__);protocol=sha(PROTOCOL);args.out.mkdir(parents=True,exist_ok=False)
    radius=lambda f:brentq(lambda r:float(np.sqrt(fields(np.array([r]))[2][0]+3*fields(np.array([r]))[1][0]/r))-f,1e-6,1.)
    radii=[.01,radius(8.),radius(5.),.25,.5,1.,2.,6.]
    result=dict(scope='Conditional canonical warm-star normalization/Jr/known-map gate only, no gas-pulse or population estimate',
        status='RUNNING',seed=201062,radii=radii,n_per_radius=N,proposal='50/50 exact full-support tail and truncated near-circular proposal',
        source_sha256=source,protocol_sha256=protocol,input_sha256=dict(actual_potential_preflight=EXPECTED),blocks=[])
    import feedback_cusp as previous
    radius_control=np.array([1e-10,.001,.01,.1,1.,2.,7.9,8.,8.1,100.])
    original=previous.fields(radius_control);current=fields(radius_control)
    field_error=[float(np.max(abs(a-b))) for a,b in zip(current,original[:3])]
    assert max(field_error)<1e-12,'New analytic field differs from the existing actual potential.'
    result['actual_potential_control']=dict(radius=radius_control.tolist(),maximum_absolute_errors=field_error,
        original_source_sha256=sha(previous.__file__))
    result['effective_potential_control']=difference_control(radii)
    write(args.out/'partial.json',result)
    if not result['effective_potential_control']['pass_gate']:
        result['status']='ACTUAL_POTENTIAL_FAILED';result['gate']=False
        write(args.out/'result.json',result)
        raise RuntimeError('Frozen direct effective-potential/local-quadratic controls failed.')
    write(args.out/'partial.json',result);rng=np.random.default_rng(201062)
    try:
        for index,Rc in enumerate(radii):
            row=block(Radial(Rc),rng,args.out,index);result['blocks'].append(row)
            write(args.out/'partial.json',result)
            if index==0:
                forecast=time.process_time()-started+7*row['cpu_seconds']+60
                result['timing_gate']=dict(projected_cpu_seconds=forecast,cutoff=230,proceed=forecast<230)
                write(args.out/'partial.json',result)
                if forecast>=230:
                    result['status']='COST_PARTIAL';break
        else:result['status']='COMPLETE'
    except Exception as error:
        result['status']='NUMERICAL_FAILED';result['error']=dict(type=type(error).__name__,message=str(error))
        write(args.out/'result.json',result);raise
    assert sha(__file__)==source and sha(PROTOCOL)==protocol
    result['gate']=len(result['blocks'])==8 and all(x['gate'] for x in result['blocks'])
    result['cpu_seconds']=time.process_time()-started
    write(args.out/'result.json',result);print((args.out/'result.json').read_text())


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--preflight',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    run(parser.parse_args())


if __name__=='__main__':main()
