"""Independent full-support Plummer action coefficients for the active-halo study.

This module imports only the standard library.  Every numerical operation,
including backend construction, requires the campaign owner's admission.  No
old orbital generator, angular-coefficient table, projection, or field solve is
imported.  Numerical packages are injected through ``Backend``.

The independent numerical ingredients are physical-radius turning-point
brackets, a logarithmic radius anomaly, DOP853 initial-value integration,
physical-r Gegenbauer evaluation, and a rotated Cartesian harmonic quadrature.
See research/active-halo-20261009/INDEPENDENT_ORBIT_DESIGN.md for derivation and
the limits of the numerical error diagnostics.
"""
from dataclasses import dataclass
import math
import time


M_VALUES = (-2, -1, 0, 1, 2)
K_VALUES = (-2, 0, 2)
DF_C = 24 * math.sqrt(2) / (7 * math.pi**3)
FAMILY_POWERS = (5, 6, 7, 8, 10, 12)


@dataclass(frozen=True)
class Backend:
    """Injected numerical modules/functions; construction itself does no work."""

    np: object
    solve_ivp: object
    brentq: object
    eval_gegenbauer: object


@dataclass(frozen=True)
class OrbitConfig:
    ne: int = 8
    neta: int = 8
    nmax: int = 2
    radial_modes: int = 16
    orbit_tolerance: float = 3e-8
    initial_solver_rtol: float = 1e-8
    minimum_solver_rtol: float = 5e-14
    maximum_refinements: int = 5
    phase_step: float = 0.25
    phase_panels: int = 16
    phase_probe_order: int = 129

    def validate(self):
        integers = (self.ne, self.neta, self.nmax, self.radial_modes,
                    self.maximum_refinements, self.phase_panels,
                    self.phase_probe_order)
        if any(type(value) is not int for value in integers):
            raise ValueError("Explicit integer orbital resolutions required")
        if (min(self.ne, self.neta) < 2 or max(self.ne, self.neta) > 512
                or not 0 <= self.nmax <= 12
                or not 0 <= self.radial_modes <= 256
                or not 1 <= self.maximum_refinements <= 12
                or not 4 <= self.phase_panels <= 512
                or not 33 <= self.phase_probe_order <= 8193):
            raise ValueError("Bounded full-support orbital resolutions required")
        values = (self.orbit_tolerance, self.initial_solver_rtol,
                  self.minimum_solver_rtol, self.phase_step)
        if not all(math.isfinite(value) and value > 0 for value in values):
            raise ValueError("Finite positive integration controls required")
        if (not 1e-12 <= self.orbit_tolerance <= 1e-4
                or not 5e-14 <= self.minimum_solver_rtol
                <= self.initial_solver_rtol <= 1e-5
                or not 0.01 <= self.phase_step <= 0.5):
            raise ValueError("Resolved tolerance and phase-step controls required")


def _check(guard):
    if guard is not None:
        stop = getattr(guard, "stop", None)
        if stop is not None and stop[0]:
            raise InterruptedError("Interrupted independent orbital construction")
        guard.check()


def _finite_positive(value, name):
    if not math.isfinite(value) or value <= 0:
        raise ArithmeticError("Unresolved positive " + name)
    return value


def _circular_deficit(radius):
    """1-e_c(r), with no subtraction of the central value from one."""
    s = math.hypot(1.0, radius)
    u = 1 / s
    return (radius / s) * (radius / (s + 1)) * (1 + u / 2 + u*u / 2)


def circular_geometry(binding, backend):
    """Solve the circular energy equation in log physical radius.

    e_c=(1+r_c²/2)/(1+r_c²)^(3/2), L_c=r_c²/(1+r_c²)^(3/4).
    The central deficit form and the outer binding form use separate stable
    residuals.  No u-polynomial root routine is called.
    """
    e = float(binding)
    if not math.isfinite(e) or not 0 < e < 1:
        raise ValueError("Interior bound energy 0<e<1 required")
    estimate = math.sqrt(1-e) / e
    center = math.log(estimate)

    def residual(log_radius):
        radius = math.exp(log_radius)
        if e > 0.5:
            return _circular_deficit(radius) - (1-e)
        s = math.hypot(1.0, radius)
        return e - 0.5 * (1 + 1/(s*s)) / s

    left, right = center-2.0, center+2.0
    while residual(left) >= 0:
        left -= 2.0
        if left < -700:
            raise ArithmeticError("Circular physical-radius bracket underflow")
    while residual(right) <= 0:
        right += 2.0
        if right > 700:
            raise ArithmeticError("Circular physical-radius bracket overflow")
    log_radius = backend.brentq(residual, left, right, xtol=2e-14, rtol=1e-15)
    radius = math.exp(log_radius)
    s = math.hypot(1.0, radius)
    angular = radius * (radius/s) / math.sqrt(s)
    vc2 = (radius/s)**2 / s
    for value, name in ((radius, "circular radius"), (angular, "circular action"),
                        (vc2, "circular velocity squared")):
        _finite_positive(value, name)
    return dict(radius=radius, s=s, angular=angular, vc2=vc2)


def turning_geometry(binding, circularity, backend, tolerance=3e-8):
    """Independently bracket the two physical-r effective-energy roots.

    All retained nodes are strictly eccentric and nonradial.  Failure to
    resolve either turning point raises; there is no circularization, cutoff,
    replacement node, or omission.
    """
    e, eta = float(binding), float(circularity)
    if not math.isfinite(eta) or not 0 < eta < 1:
        raise ValueError("Interior circularity 0<eta<1 required")
    circle = circular_geometry(e, backend)
    rc, sc, vc2 = circle["radius"], circle["s"], circle["vc2"]
    L = eta * circle["angular"]
    logc = math.log(rc)

    def radial_energy(log_radius):
        r = math.exp(log_radius)
        if r == rc:
            return vc2 * (1-eta) * (1+eta)
        s = math.hypot(1.0, r)
        # Rationalized Psi(r)-Psi(rc), with the known circular kinetic term.
        potential_difference = -(r-rc) * ((r+rc)/(s+sc)) / (s*sc)
        return 2*potential_difference + vc2 - (L/r)**2

    step = math.log(2)
    left, right = logc-step, logc+step
    while radial_energy(left) >= 0:
        left -= step
        if left < -700:
            raise ArithmeticError("Pericentre physical-radius bracket underflow")
    while radial_energy(right) >= 0:
        right += step
        if right > 700:
            raise ArithmeticError("Apocentre physical-radius bracket overflow")
    logp = backend.brentq(radial_energy, left, logc, xtol=2e-14, rtol=1e-15)
    loga = backend.brentq(radial_energy, logc, right, xtol=2e-14, rtol=1e-15)
    rp, ra = math.exp(logp), math.exp(loga)
    sp, sa = math.hypot(1.0, rp), math.hypot(1.0, ra)
    if not 0 < rp < rc < ra or sp == sa:
        raise ArithmeticError("Unresolved ordered eccentric physical turning points")
    # In s=sqrt(1+r²), Q*r²*s is a cubic.  Its constant product gives the
    # negative root without subtracting two large physical turning roots.
    third = -1 / (e*sp*sa)
    d = loga-logp
    timescale = sa * math.sqrt(sa)
    root_error = max(abs(radial_energy(logp)), abs(radial_energy(loga))) / vc2
    if not math.isfinite(root_error) or root_error > min(tolerance/16, 1e-10):
        raise ArithmeticError("Unresolved effective-energy turning-point residual")
    _finite_positive(timescale, "orbital time scale")
    return dict(e=e, eta=eta, L=L, Lc=circle["angular"], circular_radius=rc,
                rp=rp, ra=ra, sp=sp, sa=sa, third_s=third, logp=logp,
                loga=loga, log_span=d, timescale=timescale,
                turning_point_residual=root_error)


def _log_exprel(value):
    """log[(exp(x)-1)/x], extended continuously through x=0."""
    if abs(value) < 1e-5:
        # log exprel(x)=x/2+x²/24-x⁴/2880+O(x⁶).
        square = value*value
        return value/2 + square/24 - square*square/2880
    if value > 50:
        return value + math.log1p(-math.exp(-value)) - math.log(value)
    if value < -50:
        return math.log1p(-math.exp(value)) - math.log(-value)
    return math.log(math.expm1(value)/value)


def chart_rates(anomaly, geometry):
    """Return physical r, Q=v_r², dt/dchi, dpsi/dchi, dr/dchi.

    r=rp*exp[d*sin²chi], 0<=chi<=pi/2.  The time rate cancels both
    endpoint square roots analytically through exprel.  This is a physical-r
    chart, not the old u=ua+(up-ua)*sin²z quadrature.
    """
    x = float(anomaly)
    if not 0 <= x <= math.pi/2:
        raise ValueError("Outbound half-orbit anomaly required")
    if x == 0:
        ss, cc = 0.0, 1.0
    elif x == math.pi/2:
        ss, cc = 1.0, 0.0
    else:
        ss, cc = math.sin(x)**2, math.cos(x)**2
    d = geometry["log_span"]
    logr = geometry["logp"] + d*ss
    r = math.exp(logr)
    s = math.hypot(1.0, r)
    sp, sa, s3 = geometry["sp"], geometry["sa"], geometry["third_s"]
    # Stable physical differences, including exact zero at either endpoint.
    dp = (-r*math.expm1(-d*ss)) * ((r+geometry["rp"])/(s+sp))
    da = (-geometry["ra"]*math.expm1(-d*cc)) * ((geometry["ra"]+r)/(sa+s))
    kinetic = 2*geometry["e"] * (dp/r) * (da/r) * ((s-s3)/s)
    log_time = (2*logr-geometry["logp"]-geometry["loga"]
                + 0.5*(math.log(s)+math.log(s+sp)+math.log(sa+s)
                       -math.log(2*geometry["e"])-math.log(s-s3)
                       -_log_exprel(2*d*ss)-_log_exprel(-2*d*cc)))
    time_rate = math.exp(log_time)
    angle_rate = geometry["L"] * (time_rate/r) / r
    radius_rate = 2*d*r*math.sqrt(ss*cc)
    if (not all(math.isfinite(value) for value in
                (r, kinetic, time_rate, angle_rate, radius_rate))
            or kinetic < 0 or time_rate <= 0 or angle_rate <= 0):
        raise ArithmeticError("Unresolved finite physical-radius anomaly rates")
    return r, kinetic, time_rate, angle_rate, radius_rate


def radial_basis(radius, nmax, backend):
    """Own physical-r CB l=2 potential and derivative; no old basis import."""
    np = backend.np
    r = np.asarray(radius, dtype=float)
    if not np.all(np.isfinite(r)) or np.any(r < 0):
        raise ValueError("Finite nonnegative physical radius required")
    s = np.hypot(1.0, r)
    ratio = r/s
    coordinate = 2*ratio*ratio-1
    values, derivatives = [], []
    for n in range(nmax+1):
        cn = backend.eval_gegenbauer(n, 3, coordinate)
        dc = 0.0 if n == 0 else 6*backend.eval_gegenbauer(n-1, 4, coordinate)
        values.append(-ratio*ratio/s**3 * cn)
        derivatives.append((r/s)/s**4 * ((3*ratio*ratio-2/s**2)*cn
                                             -4*ratio*ratio/s**2*dc))
    return np.stack(values, axis=-1), np.stack(derivatives, axis=-1)


def negative_basis_norm(n):
    """Independent CB l=2 signed physical norm, Y angular norm 4pi, r0=1.

    I_n2=-15*pi/2048 * binomial(n+5,5) * [4(n+3)^2-1]/(n+3).
    This follows from the Gegenbauer orthogonality integral; no old norm
    implementation is invoked.  The negative sign is part of Poisson gravity.
    """
    if type(n) is not int or n < 0:
        raise ValueError("Nonnegative radial basis index required")
    return -15*math.pi/2048 * math.comb(n+5, 5) * (4*(n+3)**2-1)/(n+3)


def _basis_scales(geometry, nmax, np):
    radius2 = min(max(2/3, geometry["rp"]**2), geometry["ra"]**2)
    base = radius2 / (1+radius2)**2.5
    result = np.asarray([base*math.comb(n+5, 5) for n in range(nmax+1)])
    if not np.all(np.isfinite(result)) or np.any(result <= 0):
        raise ArithmeticError("Unresolved nonzero potential scaling")
    return result


def _integrate_orbit(geometry, config, backend, rtol, guard):
    """Two DOP853 integrations with own normalized orbital moments."""
    np = backend.np
    basis_count = config.nmax+1
    scales = _basis_scales(geometry, config.nmax, np)
    ts, js = geometry["timescale"], geometry["Lc"]
    first_nfev = 0

    def first_rhs(x, unused_y):
        nonlocal first_nfev
        first_nfev += 1
        if first_nfev % 512 == 0:
            _check(guard)
        r, q, td, ad, unused_dr = chart_rates(x, geometry)
        values, unused_derivatives = radial_basis(r, config.nmax, backend)
        return np.concatenate(([td/ts, ad, q*td/(math.pi*js)],
                               (td/ts)*(values/scales)**2))

    # The first pass also measures RMS potential scales.  An absolute floor
    # one thousand times below rtol resolves small radial actions and moments.
    first = backend.solve_ivp(first_rhs, (0.0, math.pi/2),
                              np.zeros(3+basis_count), method="DOP853",
                              rtol=rtol, atol=rtol*1e-3, dense_output=True,
                              max_step=math.pi/(2*config.phase_panels))
    if not first.success or first.sol is None:
        raise ArithmeticError("Independent time/action DOP853 failed: " + first.message)
    half_time = float(first.y[0, -1])*ts
    half_angle = float(first.y[1, -1])
    jr = float(first.y[2, -1])*js
    for value, name in ((half_time, "radial half-period"),
                        (half_angle, "half-orbit azimuth"), (jr, "radial action")):
        _finite_positive(value, name)
    omega_r, omega_l = math.pi/half_time, half_angle/half_time
    first_value_norm = scales**2 * first.y[3:, -1]/first.y[0, -1]
    if not np.all(np.isfinite(first_value_norm)) or np.any(first_value_norm <= 0):
        raise ArithmeticError("Unresolved first-pass potential RMS moments")
    rms = np.sqrt(first_value_norm)
    n = np.arange(-config.radial_modes, config.radial_modes+1)
    k = np.asarray(K_VALUES)
    shape = (len(n), len(k), basis_count)
    coefficient_count = math.prod(shape)
    second_nfev = 0

    def second_rhs(x, unused_y):
        nonlocal second_nfev
        second_nfev += 1
        if second_nfev % 512 == 0:
            _check(guard)
        r, q, td, ad, unused_dr = chart_rates(x, geometry)
        t_scaled, azimuth = first.sol(x)[:2]
        theta = omega_r*ts*t_scaled
        periodic_angle = azimuth-omega_l*ts*t_scaled
        values, derivatives = radial_basis(r, config.nmax, backend)
        normalized = values/rms
        phase = k[None, :]*periodic_angle - n[:, None]*theta
        average_rate = td/half_time
        coefficient_rate = average_rate*np.cos(phase)[:, :, None]*normalized
        periodic_rate = (geometry["L"]/(r*r)-omega_l)/omega_r
        derivative_moment = (q/omega_r**2*(derivatives/rms)**2)[None, :]
        derivative_moment = derivative_moment + (k[:, None]*periodic_rate*normalized)**2
        return np.concatenate((coefficient_rate.ravel(),
                               average_rate*normalized**2,
                               (average_rate*derivative_moment).ravel()))

    second_size = coefficient_count+basis_count+len(k)*basis_count
    state = np.zeros(second_size)
    panel_limits = np.linspace(0.0, math.pi/2, config.phase_panels+1)
    minimum_step = math.inf
    # A positive sum of radial and azimuthal phase rates sets a local ceiling.
    # DOP853 still controls its own local quadrature error inside every panel.
    # The sampled phase-rate ceiling is an anti-aliasing precaution, not a
    # mathematical supremum or an error proof; independent refinement remains.
    for left, right in zip(panel_limits[:-1], panel_limits[1:]):
        _check(guard)
        rates = []
        for x in np.linspace(left, right, 9):
            unused_r, unused_q, td, ad, unused_dr = chart_rates(float(x), geometry)
            rates.append((config.radial_modes*omega_r+2*abs(omega_l))*td+2*ad)
        max_step = min(float(right-left), config.phase_step/(2*max(rates)))
        minimum_step = min(minimum_step, max_step)
        second = backend.solve_ivp(second_rhs, (float(left), float(right)), state,
                                   method="DOP853", rtol=rtol, atol=rtol*1e-3,
                                   max_step=max_step)
        if not second.success:
            raise ArithmeticError("Independent coefficient DOP853 failed: " + second.message)
        state = second.y[:, -1]
    radial = state[:coefficient_count].reshape(shape)*rms[None, None, :]
    value_norm = state[coefficient_count:coefficient_count+basis_count]*rms**2
    derivative_norm = state[coefficient_count+basis_count:].reshape(len(k), basis_count)*rms**2
    probe = np.linspace(0.0, math.pi/2, config.phase_probe_order)
    time_probe, angle_probe = first.sol(probe)[:2]
    phases = np.stack((omega_r*ts*time_probe,
                       angle_probe-omega_l*ts*time_probe), axis=-1)
    if (not all(np.all(np.isfinite(value)) for value in
                (radial, value_norm, derivative_norm, phases))
            or np.any(value_norm <= 0) or np.any(derivative_norm < 0)):
        raise ArithmeticError("Nonfinite independent orbital coefficient or norm")
    return dict(radial=radial, value_norm=value_norm,
                derivative_norm=derivative_norm, omega_r=omega_r,
                omega_l=omega_l, jr=jr, phase_probe=phases,
                first_pass_value_norm=first_value_norm,
                solver_rtol=rtol, first_nfev=first_nfev,
                second_nfev=second_nfev, minimum_coefficient_max_step=minimum_step,
                first_step_count=len(first.t)-1)


def _comparison(current, prior, np):
    frequency_action = max(abs(current[key]-prior[key])/abs(current[key])
                           for key in ("omega_r", "omega_l", "jr"))
    rms = np.sqrt(current["value_norm"])
    coefficient = float(np.max(np.abs(current["radial"]-prior["radial"])
                               /rms[None, None, :]))
    norms = max(float(np.max(np.abs(current["value_norm"]-prior["value_norm"])
                             /current["value_norm"])),
                float(np.max(np.abs(current["derivative_norm"]-prior["derivative_norm"])
                             /np.maximum(current["derivative_norm"], 1e-300))))
    phase = float(np.max(np.abs(current["phase_probe"]-prior["phase_probe"])))
    return frequency_action, coefficient, norms, phase


def resolve_orbit(binding, circularity, config, backend, guard=None):
    """Resolve one retained orbit; no numerical result is replaced on failure."""
    config.validate()
    _check(guard)
    started = time.process_time()
    geometry = turning_geometry(binding, circularity, backend, config.orbit_tolerance)
    rtol = config.initial_solver_rtol
    prior = _integrate_orbit(geometry, config, backend, rtol, guard)
    total_first, total_second = prior["first_nfev"], prior["second_nfev"]
    for refinement in range(1, config.maximum_refinements+1):
        tighter = max(config.minimum_solver_rtol, rtol/8)
        if tighter >= rtol:
            raise ArithmeticError("Independent orbital tolerance floor exhausted")
        current = _integrate_orbit(geometry, config, backend, tighter, guard)
        total_first += current["first_nfev"]
        total_second += current["second_nfev"]
        errors = _comparison(current, prior, backend.np)
        if math.isfinite(max(errors)) and max(errors) <= config.orbit_tolerance:
            del current["phase_probe"]
            current.update(geometry=geometry, quadrature_errors=errors,
                           refinements=refinement, total_first_nfev=total_first,
                           total_second_nfev=total_second,
                           construction_CPU_seconds=time.process_time()-started)
            return current
        prior, rtol = current, tighter
    raise ArithmeticError("Unresolved retained independent orbit: errors="+str(errors))


def make_action_nodes(config, backend):
    """Own GL tensor rule on the entire open (e,eta) unit square."""
    config.validate()
    np = backend.np
    en, ew = np.polynomial.legendre.leggauss(config.ne)
    ln, lw = np.polynomial.legendre.leggauss(config.neta)
    binding, circularity = np.meshgrid((en+1)/2, (ln+1)/2, indexing="ij")
    return dict(e=binding.ravel(), eta=circularity.ravel(),
                quadrature_weight=np.outer(ew/2, lw/2).ravel(),
                construction="independent tensor GL, full 0<e<1 and 0<eta<1")


def build_library(config, backend, guard=None, action_nodes=None):
    """Build independent coefficients at default or caller's interior nodes.

    Custom nodes require e, eta and positive ``quadrature_weight`` arrays.
    Those weights integrate de*deta; the physical action Jacobian is applied
    here exactly once.  This supports future resonance-split quadrature without
    interpreting a retained-node lattice as a continuum pole approximation.
    """
    config.validate()
    _check(guard)
    started = time.process_time()
    np = backend.np
    nodes = make_action_nodes(config, backend) if action_nodes is None else action_nodes
    e = np.array(nodes["e"], dtype=float, copy=True)
    eta = np.array(nodes["eta"], dtype=float, copy=True)
    proposal = np.array(nodes["quadrature_weight"], dtype=float, copy=True)
    if (e.ndim != 1 or not len(e) or eta.shape != e.shape or proposal.shape != e.shape
            or not all(np.all(np.isfinite(value)) for value in (e, eta, proposal))
            or np.any((e <= 0) | (e >= 1) | (eta <= 0) | (eta >= 1))
            or np.any(proposal <= 0)):
        raise ValueError("Positive original quadrature weights and every interior action node required")
    rows = []
    for index, (binding, circularity) in enumerate(zip(e, eta)):
        _check(guard)
        try:
            rows.append(resolve_orbit(float(binding), float(circularity), config, backend, guard))
        except (ValueError, ArithmeticError, FloatingPointError) as failure:
            raise ArithmeticError("Unresolved retained independent action node "
                                  +str(index)+": "+str(failure)) from failure
    radial = np.stack([row["radial"] for row in rows])
    omega_r = np.asarray([row["omega_r"] for row in rows])
    omega_l = np.asarray([row["omega_l"] for row in rows])
    Lc = np.asarray([row["geometry"]["Lc"] for row in rows])
    L = eta*Lc
    radial_n, inplane_k = np.arange(-config.radial_modes, config.radial_modes+1), np.asarray(K_VALUES)
    nu = omega_r[:, None, None]*radial_n[None, :, None] + omega_l[:, None, None]*inplane_k[None, None, :]
    # dJr*dL*dLz = (de/omega_r)*(Lc*deta)*(L*dmu).  Angle
    # integration is (2pi)^3; dmu remains explicitly unnormalized.
    weight = (2*math.pi)**3 * proposal * Lc*Lc*eta / omega_r
    value_norm = np.stack([row["value_norm"] for row in rows])
    derivative_norm = np.stack([row["derivative_norm"] for row in rows])
    value_gap = value_norm[:, None, :] - np.sum(radial*radial, axis=1)
    derivative_gap = derivative_norm - np.sum(radial_n[None, :, None, None]**2*radial*radial, axis=1)
    allowance = 20*config.orbit_tolerance
    if (np.any(value_gap < -allowance*value_norm[:, None, :])
            or np.any(derivative_gap < -allowance*np.maximum(derivative_norm, 1e-300))):
        raise ArithmeticError("Independent coefficients violate resolved Parseval moments")
    return dict(e=e, eta=eta, L=L, Lc=Lc, quadrature_weight=proposal,
                weight=weight, radial=radial, radial_n=radial_n, inplane_k=inplane_k,
                nu=nu, omega_r=omega_r, omega_l=omega_l,
                jr=np.asarray([row["jr"] for row in rows]),
                turning_radii=np.asarray([(row["geometry"]["rp"], row["geometry"]["ra"]) for row in rows]),
                turning_point_residual=np.asarray([row["geometry"]["turning_point_residual"] for row in rows]),
                quadrature_errors=np.asarray([row["quadrature_errors"] for row in rows]),
                value_norm=value_norm, derivative_norm=derivative_norm,
                value_tail_proxy=np.maximum(value_gap, 0)+allowance*value_norm[:, None, :],
                derivative_tail_proxy=np.maximum(derivative_gap, 0)+allowance*derivative_norm,
                solver_rtol=np.asarray([row["solver_rtol"] for row in rows]),
                refinements=np.asarray([row["refinements"] for row in rows]),
                first_nfev=np.asarray([row["total_first_nfev"] for row in rows]),
                second_nfev=np.asarray([row["total_second_nfev"] for row in rows]),
                per_node_CPU_seconds=np.asarray([row["construction_CPU_seconds"] for row in rows]),
                minimum_coefficient_max_step=np.asarray([row["minimum_coefficient_max_step"] for row in rows]),
                construction_CPU_seconds=time.process_time()-started,
                orbit_method="physical-r log anomaly, adaptive DOP853 IVP; independent angular polynomial quadrature",
                action_measure="(2pi)^3 de*deta*dmu * Lc(e)^2 eta / omega_r; mu unnormalized",
                full_domain="0<e<1,0<eta<1,-1<mu<1; no support cutoff or omitted retained node",
                continuum_response_qualified=False, stability_qualified=False,
                tail_proxy_scope="Numerical Parseval residual plus empirical orbital allowance at retained nodes; no rigorous continuum, resolvent, resonance, or action-tail bound")


def angular_moments(backend, inclination_order=8, azimuth_order=16):
    """Independently integrate rotated Cartesian complex Y2m polynomials.

    C_mk(mu)=mean_u Y2m(R_y(i)(cos u,sin u,0))*exp(-iku).
    A_mk=int_-1^1 |C_mk|² dmu and B_mk=int_-1^1 mu|C_mk|² dmu.
    Neither the old closed C table nor its GL3 contraction is used.
    """
    if type(inclination_order) is not int or inclination_order < 4:
        raise ValueError("Inclination rule exact through fifth-degree products required")
    if type(azimuth_order) is not int or azimuth_order < 9:
        raise ValueError("Azimuth rule without l=2 product aliasing required")
    np = backend.np
    mu, muw = np.polynomial.legendre.leggauss(inclination_order)
    u = 2*math.pi*np.arange(azimuth_order)/azimuth_order
    x = mu[:, None]*np.cos(u)[None, :]
    y = np.broadcast_to(np.sin(u)[None, :], x.shape)
    z = -np.sqrt((1-mu)*(1+mu))[:, None]*np.cos(u)[None, :]
    xy = x+1j*y
    plus2 = math.sqrt(15/8)*xy**2
    plus1 = -math.sqrt(15/2)*z*xy
    zero = math.sqrt(5)/2*(3*z*z-1)
    harmonics = np.stack((plus2.conj(), -plus1.conj(), zero, plus1, plus2), axis=2)
    fourier = np.exp(-1j*u[:, None]*np.asarray(K_VALUES)[None, :])/azimuth_order
    coefficients = np.einsum("uvm,vk->umk", harmonics, fourier, optimize=False)
    square = np.abs(coefficients)**2
    a = np.einsum("u,umk->mk", muw, square, optimize=False)
    b = np.einsum("u,u,umk->mk", muw, mu, square, optimize=False)
    reconstructed = np.einsum("umk,vk->uvm", coefficients,
                              np.exp(1j*u[:, None]*np.asarray(K_VALUES)[None, :]), optimize=False)
    expected_a = np.broadcast_to(np.asarray((0.75, 0.5, 0.75)), a.shape)
    expected_b = expected_a*np.asarray(M_VALUES)[:, None]*np.asarray(K_VALUES)[None, :]/6
    reconstruction_error = float(np.max(np.abs(reconstructed-harmonics)))
    moment_error = max(float(np.max(np.abs(a-expected_a))), float(np.max(np.abs(b-expected_b))))
    reality_error = float(np.max(np.abs(coefficients.imag)))
    if (not all(np.all(np.isfinite(value)) for value in (a, b, coefficients))
            or max(reconstruction_error, moment_error, reality_error) > 1e-12):
        raise ArithmeticError("Independent rotated-harmonic normalization failed")
    return dict(A=a, B=b, mu=mu, mu_weight=muw, coefficients=coefficients,
                m=np.asarray(M_VALUES), k=np.asarray(K_VALUES),
                normalization="complex Condon-Shortley Y, int |Y|² dOmega=4pi; int dmu=2",
                reconstruction_error=reconstruction_error, moment_error=moment_error,
                coefficient_reality_error=reality_error,
                inclination_order=inclination_order, azimuth_order=azimuth_order)


def df_derivatives(binding, angular_momentum, coefficients, backend):
    """g,g_e,h,h_e,h_L2 without C; exact shared physical DF, own code.

    F=C[g(e)+Lz*h(e,L²)], g=e^(7/2)(1-14e²/33), Mb=0.1.
    coefficients is the exact already-certified physical vector.  This helper
    does not load, fit, optimize, normalize, or certify it.
    """
    np = backend.np
    e, L = np.broadcast_arrays(np.asarray(binding, dtype=float),
                               np.asarray(angular_momentum, dtype=float))
    if (not all(np.all(np.isfinite(value)) for value in (e, L))
            or np.any((e <= 0) | (e >= 1)) or np.any(L <= 0)):
        raise ValueError("Interior energy and positive angular momentum required")
    h, he, hL2 = np.zeros_like(e), np.zeros_like(e), np.zeros_like(e)
    for power, coefficient in coefficients.items():
        if type(power) is not int or power not in FAMILY_POWERS or not math.isfinite(coefficient):
            raise ValueError("Certified six-power family coefficient map required")
        ap = 4*power/((power+2.5)*(power+3.5))
        bp = 4/(power+1)
        ep = e**power
        h += coefficient*((-ap/e+bp*e)*ep + L*L*ep)
        he += coefficient*((-ap*(power-1)/(e*e)+bp*(power+1))*ep
                           +power*L*L*ep/e)
        hL2 += coefficient*ep
    g = e**3.5*(1-14*e*e/33)
    ge = e**2.5*(7-11*(14/33)*e*e)/2
    return dict(g=g, g_e=ge, h=h, h_e=he, h_L2=hL2,
                normalization_C=DF_C, bar_mass=0.1)


def contracted_derivative(library, coefficients, m, backend, angular=None):
    """hbar[a,n,k]=int dmu |C_mk|² (n,k,m)·partial_J F.

    C is included here once.  Physical action weight and the signed basis
    norm are not included.  This is kappa, not minus kappa.
    """
    if m not in M_VALUES:
        raise ValueError("Complete l=2 azimuthal sector m=-2..2 required")
    np = backend.np
    moments = angular_moments(backend) if angular is None else angular
    mi = M_VALUES.index(m)
    e = library["e"][:, None, None]
    L = library["L"][:, None, None]
    derivatives = df_derivatives(e, L, coefficients, backend)
    nu = library["nu"]
    k = library["inplane_k"][None, None, :]
    a = moments["A"][mi][None, None, :]
    b = moments["B"][mi][None, None, :]
    result = DF_C*((-nu*derivatives["g_e"]+m*derivatives["h"])*a
                   +L*(2*k*L*derivatives["h_L2"]-nu*derivatives["h_e"])*b)
    if not np.all(np.isfinite(result)):
        raise ArithmeticError("Nonfinite full own-DF contracted derivative")
    return result


def physical_mass(library, backend):
    """Original full-action mass estimate; expected 0.9, never rescaled."""
    np = backend.np
    e = library["e"]
    return float(np.sum(library["weight"]*2*DF_C*e**3.5*(1-14*e*e/33)))
