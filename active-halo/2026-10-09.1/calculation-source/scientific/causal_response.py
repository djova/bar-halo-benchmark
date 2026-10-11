"""Independent retarded kernel and physical source-overlap work.

Uses newly constructed orbit coefficients, never old orbit arrays/generators.
Backend arrays/functions are supplied by a metered caller. Causal convolution
is solved by direct Volterra quadrature. Source overlaps are spatial integrals
of the independent Poisson density basis against the external potential.
"""
import math
import time


def spatial_metric(nmax,np,eval_gegenbauer,order=128):
    x,w=np.polynomial.legendre.leggauss(order)
    theta=(x+1)*math.pi/4
    r=np.tan(theta); wr=w*math.pi/4*(1+r*r)
    z=(r*r-1)/(r*r+1)
    radial=np.stack([-r*r*(1+r*r)**(-2.5)*eval_gegenbauer(n,3,z) for n in range(nmax+1)],axis=1)
    density=np.stack([r*r*(1+r*r)**(-4.5)*eval_gegenbauer(n,3,z)*(n+2.5)*(n+3.5)/math.pi for n in range(nmax+1)],axis=1)
    gram=4*math.pi*density.T@((wr*r*r)[:,None]*radial)
    off=gram-np.diag(np.diag(gram))
    scale=np.sqrt(np.outer(-np.diag(gram),-np.diag(gram)))
    if np.max(np.abs(off)/scale)>1e-9 or np.any(np.diag(gram)>=0):
        raise ArithmeticError('Independent physical Poisson metric unresolved')
    return gram


def gradient_weights(library,strength,m,np,angular_coefficients):
    """Direct inclination quadrature, never old collapsed hbar/projection."""
    e=library['e'];L=library['L'];nu=library['nu']
    k=np.asarray(library['inplane_k'])[None,None,:]
    mu,mw=np.polynomial.legendre.leggauss(5)
    coeff=angular_coefficients(mu,m,np)
    if coeff.shape!=(len(mu),len(k[0,0])):raise ValueError('Angular coefficients [mu,k] required')
    constants=(3.795853269534006,-135.59804126193885,678.294264313138,-800.1997907110583,259.1199993421909,-136.73855372860442)
    powers=(5,6,7,8,10,12)
    h=np.zeros_like(e);he=np.zeros_like(e);hl2=np.zeros_like(e)
    for p,c in zip(powers,constants):
        a=16*p/((2*p+5)*(2*p+7));b=4/(p+1)
        h+=c*(-a*e**(p-1)+b*e**(p+1)+L*L*e**p)
        he+=c*(-a*(p-1)*e**(p-2)+b*(p+1)*e**p+p*L*L*e**(p-1))
        hl2+=c*e**p
    C=24*math.sqrt(2)/(7*math.pi**3)
    fe=C*.5*e**2.5*(7-11*(14/33)*e*e)
    even=-nu*fe[:,None,None]
    # In the hidden second term Lz=L*mu. Keep the nodal m*h separately.
    ans=np.zeros_like(nu)
    for j,u in enumerate(mu):
        derivative=even+strength*C*m*h[:,None,None]+strength*C*L[:,None,None]*u*(2*k*L[:,None,None]*hl2[:,None,None]-nu*he[:,None,None])
        ans+=mw[j]*coeff[j][None,None,:]**2*derivative
    return ans


def retarded_kernel(library,weighted_kappa,t,norms,np,guard=None):
    r=library['radial'].reshape(-1,library['radial'].shape[-1])
    freq=library['nu'].ravel()
    wk=(library['weight'][:,None,None]*weighted_kappa).ravel()
    K=np.zeros((len(t),r.shape[1],r.shape[1]),dtype=complex)
    # Bounded action/time blocks preserve every frequency and both signs.
    last=time.monotonic()
    for a in range(0,len(freq),4096):
        rr=r[a:a+4096];ww=wk[a:a+4096];ff=freq[a:a+4096]
        for j in range(0,len(t),128):
            phase=np.exp(-1j*t[j:j+128,None]*ff[None,:])
            K[j:j+128]+=1j*np.einsum('ta,ab,ac,a->tbc',phase,rr,rr,ww,optimize=True)/norms[None,:,None]
        if guard and time.monotonic()-last>10:guard.check();last=time.monotonic()
    return K


def response_matrix(library,weighted_kappa,z,norms,np):
    if z.imag<=0:raise ValueError('Analytic upper-half-plane resolvent only; real-axis resonance integration is separate')
    r=library['radial'].reshape(-1,library['radial'].shape[-1]);freq=library['nu'].ravel()
    wk=(library['weight'][:,None,None]*weighted_kappa).ravel()
    return (r.T@((wk/(freq-z))[:,None]*r))/norms[:,None]


def work_history(c,b,bdot,bshape,metric,t,np,m=2):
    """rho_basis times source potential integrated in space, then time."""
    overlap=lambda a:np.real(np.einsum('tb,bc,tc->t',c.conj(),metric,a))
    power=overlap(bdot);shape_power=overlap(bshape)
    torque=overlap(-1j*m*b)
    integrate=lambda f:np.concatenate(([0.],np.cumsum((f[1:]+f[:-1])*np.diff(t)/2)))
    return dict(power=power,shape_power=shape_power,torque=torque,work=integrate(power),shape_work=integrate(shape_power),impulse=integrate(torque))


def endpoint_budget(library,kappa,total,t,norms,np,guard=None,m=2):
    r=library['radial'].reshape(-1,library['radial'].shape[-1]);freq=library['nu'].ravel()
    wk=(library['weight'][:,None,None]*kappa).ravel()
    tw=np.empty(len(t));tw[0]=(t[1]-t[0])/2;tw[-1]=(t[-1]-t[-2])/2;tw[1:-1]=(t[2:]-t[:-2])/2
    Q=J=0.
    for a in range(0,len(freq),2048):
        if guard:guard.check()
        potential=total@r[a:a+2048].T
        phase=np.exp(-1j*(t[-1]-t[:,None])*freq[None,a:a+2048])
        g=np.sum(tw[:,None]*potential*phase,axis=0)
        square=np.abs(g)**2
        Q-=.5*float(np.sum(wk[a:a+2048]*freq[a:a+2048]*square))
        J-=.5*float(np.sum(wk[a:a+2048]*m*square))
    return Q,J
