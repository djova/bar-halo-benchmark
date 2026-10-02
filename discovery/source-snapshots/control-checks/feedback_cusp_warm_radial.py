"""PREPARATION: variable-L canonical target, no automatic job or sampling."""
import numpy as np
from scipy.special import ndtr,ndtri,gammaincinv
from feedback_cusp_radial import fields,legendre,PHI0


def cdf(R):return -np.expm1(-R)-R*np.exp(-R)


class Population:
    """One fixed L per family; energy delta means E-E_circular(L)."""
    def __init__(self,Rc):
        self.Rc=np.atleast_1d(np.asarray(Rc,dtype=float))
        if np.any(self.Rc<=0) or np.any(~np.isfinite(self.Rc)):raise RuntimeError('Invalid guiding radius; no replacement.')
        phi,f,s=fields(self.Rc);self.vc=np.sqrt(self.Rc*f);self.L=self.Rc*self.vc
        self.kappa=np.sqrt(s+3*f/self.Rc);self.Js=(.1*self.vc)**2/self.kappa
        self.Ec=phi+.5*self.vc**2;self.D=-self.Ec
        lo=self.L/(2*np.sqrt(-2*PHI0));hi=self.Rc.copy()
        if np.any(fields(lo)[0]+.5*self.L**2/lo**2<=0) or np.any(self.Ec>=0):raise RuntimeError('Parabolic root bracket failure.')
        for _ in range(64):
            mid=(lo+hi)/2;left=fields(mid)[0]+.5*self.L**2/mid**2>0
            lo=np.where(left,mid,lo);hi=np.where(left,hi,mid)
        self.rmin=(lo+hi)/2

    def subset(self,ids):return Population(self.Rc[ids])

    def difference(self,r,ids=None):
        r=np.asarray(r);c=self.Rc if ids is None else self.Rc[ids]
        c=c.reshape((len(c),)+(1,)*(r.ndim-1));d=r-c
        result=d*d*((2+c)*r+c)/(2*r*r*(1+r)*(1+c)**2)
        for s in (.2,1.3):
            uc=np.sqrt(c*c+s*s);ur=np.sqrt(r*r+s*s);norm=8**3/(64+s*s)**1.5
            inside=.05/norm*d*d*(r+c)**2*(c*c+2*s*s-c*c*uc/(ur+uc))/(2*r*r*ur*uc**3*(ur+uc))
            outside=.05*d*d/(2*c*r*r)
            phi_r=np.where(r<8,-.05*(1/ur-s*s/(64+s*s)**1.5)/norm,-.05/r)
            phi_c=np.where(c<8,-.05*(1/uc-s*s/(64+s*s)**1.5)/norm,-.05/c)
            Lc2=np.where(c<8,.05*c**4/uc**3/norm,.05*c)
            crossing=phi_r-phi_c-.5*Lc2*d*(r+c)/(r*r*c*c)
            result+=np.where((r<8)&(c<8),inside,np.where((r>=8)&(c>=8),outside,crossing))
        return result

    def action_period(self,delta,count=128):
        delta=np.asarray(delta,dtype=float)
        if delta.shape[0]!=len(self.Rc) or np.any(delta<0):raise RuntimeError('Invalid conditional energy; no clipping.')
        shape=delta.shape;values=delta.ravel();family=np.repeat(np.arange(len(self.Rc)),delta.size//len(self.Rc))
        depth=self.D[family];J=np.full(len(values),np.inf);om=np.zeros(len(values))
        zero=values==0;J[zero]=0;om[zero]=self.kappa[family[zero]]
        ids=np.flatnonzero((values>0)&(values<depth));t,w=legendre(count)
        for offset in range(0,len(ids),1024):
            chosen=ids[offset:offset+1024];owners=family[chosen];e=values[chosen]
            lo=self.rmin[owners].copy();hi=self.Rc[owners].copy()
            if np.any(self.difference(lo,owners)<e):raise RuntimeError('Inner action bracket failure.')
            for _ in range(64):
                mid=(lo+hi)/2;left=self.difference(mid,owners)>e
                lo=np.where(left,mid,lo);hi=np.where(left,hi,mid)
            rp=(lo+hi)/2;lo=self.Rc[owners].copy();hi=2.2/(depth[chosen]-e)
            if np.any(self.difference(hi,owners)<e):raise RuntimeError('Outer action bracket failure.')
            for _ in range(64):
                mid=(lo+hi)/2;left=self.difference(mid,owners)<e
                lo=np.where(left,mid,lo);hi=np.where(left,hi,mid)
            ra=(lo+hi)/2;cut=np.full(len(e),np.pi/2);cross=(rp<8)&(ra>8)
            cut[cross]=np.arcsin(np.sqrt((8-rp[cross])/(ra[cross]-rp[cross])))
            action=np.zeros(len(e));period=np.zeros(len(e))
            for begin,end in ((np.zeros(len(e)),cut),(cut,np.full(len(e),np.pi/2))):
                use=end>begin
                if not np.any(use):continue
                angle=begin[use,None]+(end-begin)[use,None]*t
                r=rp[use,None]+(ra-rp)[use,None]*np.sin(angle)**2
                dr=(ra-rp)[use,None]*np.sin(2*angle)*(end-begin)[use,None]
                Q=2*(e[use,None]-self.difference(r,owners[use]))
                if np.any(Q<=0):raise RuntimeError('Nonpositive action quadrature radicand; no repair.')
                p=np.sqrt(Q);action[use]+=np.sum(w*p*dr,axis=1)/np.pi
                period[use]+=np.sum(w*dr/p,axis=1)
            J[chosen]=action;om[chosen]=np.pi/period
        return J.reshape(shape),om.reshape(shape)

    def target(self,delta,count=128):
        delta=np.asarray(delta);J,om=self.action_period(delta,count)
        Js=self.Js.reshape((len(self.Js),)+(1,)*(delta.ndim-1));D=self.D.reshape(Js.shape)
        inside=delta<D;g=np.zeros_like(J);slope=np.zeros_like(J)
        values=np.exp(-J/Js)/(2*np.pi*Js);g[inside]=values[inside]
        denom=Js*om;slope[inside]=g[inside]/denom[inside]
        if np.any(~np.isfinite(g)) or np.any(~np.isfinite(slope)) or np.any(slope<0):raise RuntimeError('Passive target failure.')
        return J,om,g,slope

    def curvature(self,initial,final,count=64,action_count=128):
        t,w=legendre(count);change=final-initial
        points=initial[:,None]+change[:,None]*t
        slope=self.target(points,action_count)[3]
        return change**2*np.sum(w*(1-t)*slope,axis=1)

    def primitive(self,delta,count=64,action_count=128):
        t,w=legendre(count);distance=self.D-delta
        if np.any(distance<=0):raise RuntimeError('Primitive called outside initial bound support.')
        points=delta[:,None]+distance[:,None]*t*t
        g=self.target(points,action_count)[2]
        return np.sum(w*2*distance[:,None]*t*g,axis=1)


def sample_guiding(rng,n,centers):
    label=rng.random(n);u=rng.random(n);width=np.array([.03,.015]);center=np.array(centers)
    Rc=gammaincinv(2,u);component=np.where(label<.5,0,np.where(label<.75,1,2))
    for j in range(2):
        ids=component==j+1;low=ndtr(-center[j]/width[j])
        Rc[ids]=center[j]+width[j]*ndtri(low+(1-low)*u[ids])
    p=Rc*np.exp(-Rc);q=.5*p
    for mu,s in zip(center,width):
        q+=.25*np.exp(-.5*((Rc-mu)/s)**2)/(s*np.sqrt(2*np.pi)*ndtr(mu/s))
    if np.any(Rc<=0) or np.any(q<=0):raise RuntimeError('Invalid guiding state; no replacement.')
    recovered=cdf(Rc)
    for j in range(2):
        ids=component==j+1;low=ndtr(-center[j]/width[j])
        recovered[ids]=(ndtr((Rc[ids]-center[j])/width[j])-low)/(1-low)
    return dict(Rc=Rc,guide_q=q,guide_p=p,guide_weight=p/q,guide_component=component,
        guide_u=u,guide_recovered_u=recovered)


def sample_radial(model,rng):
    n=len(model.Rc);label=rng.random(n)<.5;u=rng.random(n);v=rng.random(n);R=1+model.Rc
    lower=ndtr(np.log(model.rmin/model.Rc)/.2)
    near=model.Rc*np.exp(.2*ndtri(lower+(1-lower)*u))
    r=np.where(label,model.rmin+R*u/(1-u),near)
    vmax2=2*(model.D-model.difference(r))
    if np.any(vmax2<=0):raise RuntimeError('Radial sampling support failure; no repair.')
    vmax=np.sqrt(vmax2);sigma=.1*model.vc;plow=ndtr(-vmax/sigma);pwidth=ndtr(vmax/sigma)-plow
    p=np.where(label,vmax*(2*v-1),sigma*ndtri(plow+pwidth*v))
    tail=R/((r-model.rmin+R)**2*2*vmax)
    qr=np.exp(-.5*(np.log(r/model.Rc)/.2)**2)/(r*.2*np.sqrt(2*np.pi)*(1-lower))
    qp=np.exp(-.5*(p/sigma)**2)/(sigma*np.sqrt(2*np.pi)*pwidth)
    q=.5*(tail+qr*qp);delta=model.difference(r)+.5*p*p
    if np.any(delta>=model.D) or np.any(~np.isfinite(q)) or np.any(q<=0):raise RuntimeError('Conditional proposal endpoint failure.')
    recovered_u=np.where(label,(r-model.rmin)/(r-model.rmin+R),(ndtr(np.log(r/model.Rc)/.2)-lower)/(1-lower))
    recovered_v=np.where(label,.5*(p/vmax+1),(ndtr(p/sigma)-plow)/pwidth)
    return dict(radius=r,pr=p,delta=delta,radial_q=q,radial_component=label,
        radial_u=u,radial_v=v,radial_recovered_u=recovered_u,radial_recovered_v=recovered_v)


def force(r):
    """Static radial derivative, centered unit-fraction gas basis, derivative."""
    static=1/(1+r)**2;centered=[];grad=[]
    for s in (.2,1.3):
        norm=8**3/(64+s*s)**1.5;u=np.sqrt(r*r+s*s);inside=r<8
        d=np.where(inside,r*r/(s*u*(u+s))/norm,
            (1/s-s*s/(64+s*s)**1.5)/norm-1/r)
        f=np.where(inside,r/u**3/norm,1/r**2)
        static+=.05*f;centered.append(d);grad.append(f)
    return static,.1*(centered[0]-centered[1]),.1*(grad[0]-grad[1])


def pulse(t,frequency):
    valid=(t>0)&(t<80)&(frequency!=0)
    a=.003*np.sin(np.pi*t/80)**2*np.cos(frequency*t)
    da=.003*(np.pi/80*np.sin(2*np.pi*t/80)*np.cos(frequency*t)-frequency*np.sin(np.pi*t/80)**2*np.sin(frequency*t))
    return np.where(valid,a,0.),np.where(valid,da,0.)


FREQUENCY=np.array([0.,0.,5.,5.,8.,8.]);DIRECTION=np.array([1.,-1.,1.,-1.,1.,-1.])


def kdk(model,r0,p0,dt,directions=DIRECTION):
    r=np.broadcast_to(r0,(6,len(model.Rc))).copy();p=np.broadcast_to(p0,r.shape).copy()
    clock=np.arange(round(80/dt)+1)*dt;times=np.where(directions[:,None]>0,clock,clock[::-1])
    a,da=pulse(times,FREQUENCY[:,None]);h=dt*directions[:,None];L=model.L[None,:]
    initial=model.difference(r.T).T+.5*p*p;work=np.zeros_like(r)
    f,psi,basis=force(r)
    for i in range(len(clock)-1):
        p-=.5*h*(f+a[:,i,None]*basis)
        newr=np.sqrt((r+h*p)**2+(h*L/r)**2)
        p=(r*p+h*(p*p+L*L/r**2))/newr;r=newr
        f,newpsi,basis=force(r);p-=.5*h*(f+a[:,i+1,None]*basis)
        work+=.5*h*(psi*da[:,i,None]+newpsi*da[:,i+1,None]);psi=newpsi
    final=model.difference(r.T).T+.5*p*p
    return dict(radius=r,pr=p,delta_initial=initial,delta_final=final,deltaE=final-initial,
        work=work,energy_minus_work=final-initial-work)
