"""Exact scientific functions from the sealed forecast; NumPy only.

See function-provenance.json. No private launcher or field snapshot.
"""
AMPLITUDE,RAMP,DURATION=1e-4,10.,40.

def grid(np,ne,nl):
    en,ew=np.polynomial.legendre.leggauss(ne)
    ln,lw=np.polynomial.legendre.leggauss(nl)
    binding,ell=np.meshgrid((en+1)/2,(ln+1)/2,indexing='ij')
    binding,ell=binding.ravel(),ell.ravel()
    Lmax=(1-binding)/np.sqrt(2*binding)
    L=Lmax*ell
    return binding,ell,L,np.outer(ew/2,lw/2).ravel(),Lmax/(2*binding)**1.5

def stable_path(np,e,L,ell,eta):
    a=1/(2*e[:,None]);L=L[:,None]
    A=1-e[:,None]
    zeta=A*np.sqrt(1-ell[:,None]**2)
    eta=eta[None,:]
    measure=1-zeta*np.cos(eta)
    # u-b = a(A-zeta)+a*zeta*(1-cos eta). The first term
    # equals L²/(A+zeta); this avoids subtraction near radial pericenter.
    uminus=L*L/(A+zeta)+2*a*zeta*np.sin(eta/2)**2
    r2=uminus*(uminus+1.)
    assert np.all(r2>0) and np.all(np.isfinite(r2))
    r=np.sqrt(r2);M=eta-zeta*np.sin(eta)
    L1=np.sqrt(L*L+2.)
    phi1=np.arctan2((A+zeta)*np.sqrt(a)/L*np.sin(eta/2),np.cos(eta/2))
    phi2=np.arctan2((1+e[:,None]+zeta)*np.sqrt(a)/L1*np.sin(eta/2),np.cos(eta/2))
    q=.5*(1+L/L1)
    chi=phi1+L/L1*phi2-q*M
    vr=np.sqrt(a)*zeta*np.sin(eta)/r
    omega=a**-1.5
    return r,vr,M,chi,measure,L/r2/omega-q,omega

def coefficient_grid(np,ne,nl,order,limit):
    e,ell,L,weights,jacobian=grid(np,ne,nl)
    nodes,quadrature=np.polynomial.legendre.leggauss(order)
    eta=(nodes+1)*np.pi;quadrature=quadrature/2
    modes=np.arange(-limit,limit+1)
    R=np.empty((len(e),3,len(modes)),dtype=complex)
    Q=np.empty((len(e),3));V=np.empty_like(Q)
    radial_measure=np.empty(len(e))
    for first in range(0,len(e),32):
        last=min(first+32,len(e))
        r,vr,M,chi,measure,chi_prime,omega=stable_path(np,e[first:last],L[first:last],ell[first:last],eta)
        radial_measure[first:last]=measure @ quadrature
        value=-.5*.5**3*r*r/(.25+r*r)**2.5
        dr=-.5*.5**3*r*(.5-3*r*r)/(.25+r*r)**3.5
        w=measure*quadrature[None,:]
        fourier=np.exp(-1j*M[:,:,None]*modes[None,None,:])
        for ik,k in enumerate((-2,0,2)):
            v=value*np.exp(1j*k*chi)
            derivative=(dr*vr/omega+1j*k*value*chi_prime)*np.exp(1j*k*chi)
            R[first:last,ik]=np.einsum('bj,bjn->bn',v*w,fourier,optimize=False)
            V[first:last,ik]=np.sum(w*abs(v)**2,axis=1)
            Q[first:last,ik]=np.sum(w*abs(derivative)**2,axis=1)
    return dict(binding_energy=e,circularity=ell,L=L,quadrature_weights=weights,
                action_measure=jacobian,radial_modes=modes,inplane_modes=np.array([-2,0,2]),
                radial_coefficients=R,value_norm=V,derivative_norm=Q,
                radial_measure_integral=radial_measure)

def f0(np,e):
    # Exact positive-series DF from the unforced construction; no fitted data.
    coefficients=[1.]
    for n in range(95):
        coefficients.append(coefficients[-1]*(n+2)*(n+5)**2/((n+1)*(n+4)*(2*n+7)))
    return 8/(5*np.sqrt(2)*np.pi**3)*e**2.5*np.polynomial.polynomial.polyval(e,coefficients)

def contract(np,helper,arrays,populations,previous_quad=None):
    e,L=arrays['binding_energy'],arrays['L'];modes=arrays['radial_modes']
    omega_r=(2*e)**1.5
    q=.5*(1+L/np.sqrt(L*L+2.))
    omega_L=q*omega_r
    omega_p=float(helper.frequencies(np,.08,.05+2*.30)[1])
    k=np.array([-2,0,2])[None,:,None]
    omega=omega_r[:,None,None]*modes[None,None,:]+omega_L[:,None,None]*k
    delta=omega-2*omega_p
    history=helper.window(np,delta,AMPLITUDE,RAMP,DURATION)
    power=abs(arrays['radial_coefficients'])**2
    spectral_Q=np.sum(modes[None,None,:]**2*power,axis=2)
    Q=arrays['derivative_norm']
    Q_proxy=np.zeros(Q.shape)
    if previous_quad is not None:
        assert np.array_equal(e,previous_quad['binding_energy']) and np.array_equal(L,previous_quad['L'])
        assert np.array_equal(modes,previous_quad['radial_modes'])
        previous_spectral=np.sum(modes[None,None,:]**2*abs(previous_quad['radial_coefficients'])**2,axis=2)
        Q_proxy=2*(abs(Q-previous_quad['derivative_norm'])+abs(spectral_Q-previous_spectral))
    Q_full=Q+Q_proxy
    Q_tail=np.maximum(Q-spectral_Q,0)+Q_proxy
    N=int(np.max(abs(modes)))
    detuning_floor=(N+1)*omega_r[:,None]-abs(np.array([-2,0,2])[None,:]*omega_L[:,None]-2*omega_p)
    history_bound=np.full(Q.shape,AMPLITUDE*(DURATION-RAMP/2))
    np.minimum(history_bound,2*AMPLITUDE/np.maximum(detuning_floor,1e-300),out=history_bound,
               where=detuning_floor>0)
    action_weight=arrays['quadrature_weights']*arrays['action_measure']
    I_k=np.array([2/5,4/15,2/5])[None,:,None]
    M_k=np.array([-4/15,0.,4/15])[None,:,None]
    I=1/np.sqrt(2*e)
    hrr=-3/I**4;hrL=-3*q/I**4;hLL=1/(L*L+2.)**1.5/I**3-3*q*q/I**4
    curvature=hrr[:,None,None]*modes[None,None,:]**2+2*hrL[:,None,None]*modes[None,None,:]*k+hLL[:,None,None]*k*k
    libration_frequency=np.sqrt(2*AMPLITUDE*abs(arrays['radial_coefficients'])*abs(curvature))
    libration_phase=DURATION*libration_frequency
    near=np.abs(delta)<=2*np.pi/DURATION
    nonweak=np.any(near & (libration_phase>.3),axis=(1,2))
    mass_weights=(2*np.pi)**3*action_weight*2*L*f0(np,e)
    rows=[];mode_contributions=[]
    for pop in populations:
        p,alpha=pop['p'],pop['alpha']
        h,he=helper.h_and_derivative(np,e,L,p)
        gradient=2*alpha*L[:,None,None]*(2*h[:,None,None]*I_k+
                 L[:,None,None]*(2*k*L[:,None,None]*e[:,None,None]**p-he[:,None,None]*omega)*M_k)
        integrand=-2*(2*np.pi)**3*action_weight[:,None,None]*gradient*power*abs(history)**2
        assert np.all(np.isfinite(integrand))
        total=float(np.sum(integrand));absolute=float(np.sum(abs(integrand)))
        const=2*alpha*L[:,None]*(2*abs(h[:,None])*I_k[:,:,0]+L[:,None]*(
              2*abs(k[:,:,0])*L[:,None]*e[:,None]**p+abs(he[:,None])*abs(k[:,:,0])*omega_L[:,None])*abs(M_k[:,:,0]))
        slope=2*alpha*L[:,None]**2*abs(he[:,None])*omega_r[:,None]*abs(M_k[:,:,0])
        prefactor=2*(2*np.pi)**3*action_weight[:,None]*history_bound**2
        def tail(norm):return float(np.sum(prefactor*(const*norm/(N+1)**2+slope*norm/(N+1))))
        weaknesses=[]
        for threshold in (.3,.5,1.):
            mask=near & (libration_phase>threshold)
            weak_abs=float(np.sum(abs(integrand[mask])))
            weaknesses.append(dict(libration_phase_threshold=threshold,
                              near_condition='abs(detuning)<=2pi/T',absolute_contribution=weak_abs,
                              fraction_of_total_absolute=weak_abs/absolute if absolute else None,
                              over_absolute_net=weak_abs/abs(total) if total else None))
        rows.append(dict(p=p,alpha=alpha,forecast=total,absolute_mode_contribution=absolute,
                         absolute_over_net=absolute/abs(total) if total else None,
                         tail_proxy_full_norm=tail(Q_full),tail_proxy_residual_norm=tail(Q_tail),
                         norm_proxy_has_paired_quadrature=previous_quad is not None,
                         signed_inplane_contributions=np.sum(integrand,axis=(0,2)).tolist(),
                         near_resonance_weakness=weaknesses))
        mode_contributions.append(integrand)
    arrays['population_mode_contributions']=np.array(mode_contributions)
    arrays['libration_phase']=libration_phase
    arrays['detuning']=delta
    arrays['tail_norm_full_proxy']=Q_full;arrays['tail_norm_residual_proxy']=Q_tail
    arrays['tail_history_bound']=history_bound;arrays['reference_mass_action_weights']=mass_weights
    return dict(rows=rows,pattern_speed=omega_p,represented_reference_mass=float(np.sum(mass_weights)),
                reference_mass_with_any_recorded_near_mode_libration_phase_above_point3=float(np.sum(mass_weights[nonweak])),
                maximum_libration_phase=float(np.max(libration_phase)),
                maximum_radial_measure_error=float(np.max(abs(arrays['radial_measure_integral']-1))),
                observable='Accumulated Lz transfer to Fplus minus transfer to Fminus; second-order weak-field forecast',
                units='G=M=1 isochrone reference action units; common total population mass1',
                no_forced_outcomes_read=True)

def frequencies(np, jr, angular):
    root = np.sqrt(angular*angular+2.)
    I = jr+.5*(angular+root)
    radial = I**-3
    return radial, .5*(1+angular/root)*radial

def h_and_derivative(np, binding, angular, p):
    A = 4*p/((p+2.5)*(p+3.5))
    B = 4/(p+3.5)
    h = -A*binding**(p-1)+(B+angular*angular)*binding**p
    he = -A*(p-1)*binding**(p-2)+p*(B+angular*angular)*binding**(p-1)
    return h, he

def window(np, delta, amplitude, growth_time, duration):
    """Integral of clipped quintic growth times exp(i delta t).

    Integration by parts reduces the ramp to the characteristic function of
    a Beta(3,3) variate. Small arguments use its entire power series; larger
    arguments use polynomial-exponential recurrences. A separate series
    avoids subtraction of two nearly equal terms near delta=0.
    """
    delta = np.asarray(delta, dtype=float)
    flat = delta.ravel()
    answer = np.empty(flat.shape, dtype=complex)
    small = abs(flat*duration) < .01
    d = flat[small]
    result = np.zeros(d.shape, dtype=complex)
    coefficient = np.ones(d.shape, dtype=complex)
    moment = 1.
    for n in range(1, 34):
        moment *= (n+2)/(n+5)
        if n > 1:
            coefficient *= 1j*d/n
        result += coefficient*(duration**n-growth_time**n*moment)
    answer[small] = amplitude*result
    d = flat[~small]
    z = 1j*d*growth_time
    beta = np.empty(z.shape, dtype=complex)
    series = abs(z) < 2.
    zs = z[series]
    term = np.ones(zs.shape, dtype=complex)
    total = term.copy()
    for n in range(1, 64):
        term *= zs/n*(n+2)/(n+5)
        total += term
    beta[series] = total
    zr = z[~series]
    values = [np.expm1(zr)/zr]
    ez = np.exp(zr)
    for n in range(1, 5):
        values.append((ez-n*values[-1])/zr)
    beta[~series] = 30*(values[2]-2*values[3]+values[4])
    answer[~small] = amplitude*(np.exp(1j*d*duration)-beta)/(1j*d)
    return answer.reshape(delta.shape)
