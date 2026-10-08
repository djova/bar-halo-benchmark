#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Generate full-support Plummer actions and contract finite-cycle bare work.

Only NumPy/SciPy are required. No saved trajectories, campaign paths, host
services or scalar-response inputs are used. A single quadrature is not a
continuum qualification. See README.md for the model and certificate scope.
"""
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import signal
import sys
import time

POWERS = (5, 6, 7, 8, 10, 12)
A_COEFFICIENTS = (3.795853269534006, -135.59804126193885, 678.294264313138,
                  -800.1997907110583, 259.1199993421909, -136.73855372860442)
NINE_TENTHS_COEFFICIENTS = (3.4162679425806055, -122.03823713574496,
    610.4648378818242, -720.1798116399525, 233.2079994079718, -123.06469835574397)
M_VALUES, K_VALUES = (-2, 2), (-2, 0, 2)
BAR_MASS, Q = .1, 14/33
DF_C = 24*math.sqrt(2)/(7*math.pi**3)
METHOD_ANCESTORS = {
    'robust_orbits.py': '144eb392a8b0253b6fa59dccaca2f6225a247319bb5b6679351c86affb69df1b',
    'compact_bare_window.py': '702cb3374757ae34ef58c95b53e37d1e738d555e19db7e261e1e2b66ebd86a5d',
    'stationary_bare_window.py': 'fca4483bad92b8756c2aa141ea564751f8097af644a25241d4641e702cadd985',
    'family.py': '7377e138eff9889d0a579cdbc329c0d94a0b2897446b643ef66543e2e4b665e6',
}


@dataclass(frozen=True)
class Config:
    ne: int = 32
    neta: int = 32
    radial_modes: int = 16
    orbit_order: int = 64
    maximum_orbit_order: int = 2048
    orbit_tolerance: float = 3e-8
    omega: float = .12
    duration: float = 120.
    ramp: float = 12.
    shape: float = .8
    cpu_seconds: int = 3600
    wall_seconds: int = 7200
    memory_mib: int = 2048

    def validate(self):
        if not (2 <= self.ne <= 128 and 2 <= self.neta <= 128
                and 1 <= self.radial_modes <= 128
                and self.orbit_order in (32, 64, 128, 256)
                and self.maximum_orbit_order in (64, 128, 256, 512, 1024, 2048)
                and self.maximum_orbit_order >= 2*self.orbit_order):
            raise ValueError('Action/Fourier/orbit orders exceed the declared bounds')
        values = (self.orbit_tolerance, self.omega, self.duration, self.ramp, self.shape)
        if (not all(math.isfinite(v) for v in values)
                or not 1e-12 <= self.orbit_tolerance <= 3e-8
                or not 0 <= self.omega <= 2 or not 1 <= self.duration <= 240
                or not 0 < self.ramp <= self.duration/2 or not 0 <= self.shape <= 1
                or not 60 <= self.cpu_seconds <= 14400
                or not 60 <= self.wall_seconds <= 86400
                or not 512 <= self.memory_mib <= 8192):
            raise ValueError('Finite bounded physical and process controls required')


class Budget:
    """Unix hard process limits where available; cooperative checks elsewhere."""
    def __init__(self, cfg):
        self.cfg, self.cpu0, self.wall0 = cfg, time.process_time(), time.monotonic()
        self.limits = {'cpu': 'cooperative', 'address_space': 'unavailable'}
        try:
            import resource
        except ImportError:
            return
        for name, amount, label in (('RLIMIT_CPU', cfg.cpu_seconds, 'cpu'),
                ('RLIMIT_AS', cfg.memory_mib*1024**2, 'address_space')):
            if not hasattr(resource, name):
                continue
            key = getattr(resource, name)
            soft, hard = resource.getrlimit(key)
            limit = min([amount]+[v for v in (soft, hard) if v != resource.RLIM_INFINITY])
            try:
                resource.setrlimit(key, (limit, hard))
            except (OSError, ValueError) as error:
                self.limits[label] = 'unavailable: '+type(error).__name__
            else:
                self.limits[label] = limit

    def check(self):
        if (time.process_time()-self.cpu0 > self.cfg.cpu_seconds
                or time.monotonic()-self.wall0 > self.cfg.wall_seconds):
            raise TimeoutError('Declared process budget exhausted; no node omitted')


def provenance():
    home = Path(__file__).resolve().parent
    return {name: hashlib.sha256((home/name).read_bytes()).hexdigest()
            for name in ('run.py', 'README.md', 'requirements.txt') if (home/name).is_file()}


@lru_cache(maxsize=24)
def rule(order, np):
    return np.polynomial.legendre.leggauss(order)


def turning_points(e, L, brentq):
    """Roots of 2(u-e)(1-u^2)-L^2 u^2; no tail circularization."""
    uc = brentq(lambda u: (1-u*u)**2-L*L*u, 0., 1., xtol=5e-324, rtol=1e-14)
    ec = .5*uc*(1+uc*uc)
    roundoff = 128*math.ulp(ec)+4e-14*abs(ec)
    if e >= ec-roundoff:
        raise ArithmeticError('Unresolved interior circular limit; node retained as failure')
    polynomial = lambda u: 2*(u-e)*(1-u*u)-L*L*u*u
    ua = brentq(polynomial, e, uc, xtol=5e-324, rtol=1e-14)
    up = brentq(polynomial, uc, 1., xtol=5e-324, rtol=1e-14)
    third = e-L*L/2-ua-up
    if not 0 < ua < up <= 1 or third >= 0:
        raise ArithmeticError('Physical turning-root ordering failed')
    return ua, up, third


def pole_parameters(e, L, roots):
    ua, up_root, third = roots
    gap = L*L*up_root*up_root/(2*(up_root-e)*(1+up_root))
    delta, up_eff = (1-ua)-gap, 1-gap
    rootp = math.sqrt(up_eff-third)
    dp = (1+up_eff)*rootp
    # The binary gap identity uses up_root; the stable chart ends at up_eff.
    prefactor = 2*math.sqrt((up_root-e)*(1+up_root))/(up_root*dp*math.sqrt(1-ua))
    if not 0 < ua < up_eff < 1 or not gap > 0 or not delta > 0:
        raise ArithmeticError('Unresolved positive turning-point chart')
    return dict(ua=ua, third=third, L=L, gap=gap, delta=delta,
                rootp=rootp, dp=dp, fp=math.sqrt(2)*L/dp, prefactor=prefactor)


def integrands(z, pole, np):
    ss, cc = np.sin(z)**2, np.cos(z)**2
    u = pole['ua']+pole['delta']*ss
    q = pole['gap']+pole['delta']*cc
    root, v = np.sqrt(u-pole['third']), q*(1+u)
    td = math.sqrt(2)/(u*u*root)
    jd = 2*math.sqrt(2)*pole['delta']**2*ss*cc*root/(u*u*v)/math.pi
    divided = pole['rootp']+(1+u)/(pole['rootp']+root)
    remainder = math.sqrt(2)*pole['L']*(pole['delta']*cc/q)*divided/((1+u)*root*pole['dp'])
    return u, q, td, jd, remainder


def panels(bounds, indices, order, pole, np, budget):
    nodes, weights = rule(order, np)
    result = np.empty((len(indices), 2))
    for offset in range(0, len(indices), 64):
        budget.check()
        selected = indices[offset:offset+64]
        half = (bounds[selected+1]-bounds[selected])/2
        z = bounds[selected, None]+half[:, None]*(1+nodes[None, :])
        unused_u, unused_q, td, unused_jd, remainder = integrands(z, pole, np)
        result[offset:offset+len(selected), 0] = half*(td@weights)
        result[offset:offset+len(selected), 1] = half*(remainder@weights)
    if not np.all(np.isfinite(result)) or np.any(result < 0):
        raise ArithmeticError('Finite positive phase panels required')
    return result


def partial_phases(z, pole, half_time, half_angle, omr, oml, cfg, np, budget):
    bounds = np.concatenate(([0.], z, [math.pi/2]))
    if not np.all(np.diff(bounds) > 0):
        raise ArithmeticError('Strict ordered complete half-orbit panels required')
    indices = np.arange(len(bounds)-1)
    coarse = panels(bounds, indices, 8, pole, np, budget)
    fine = panels(bounds, indices, 16, pole, np, budget)
    errors = np.abs(fine-coarse)
    allowance = cfg.orbit_tolerance/4
    local = (omr+abs(oml))*errors[:, 0]+errors[:, 1]
    refined = np.asarray([], dtype=int)
    if float(np.sum(local)) > allowance:
        refined = np.flatnonzero(local > allowance/len(indices))
        coarse[refined] = fine[refined]
        fine[refined] = panels(bounds, refined, 32, pole, np, budget)
        errors[refined] = np.abs(fine[refined]-coarse[refined])
    suffix = np.cumsum(fine[::-1], axis=0)[::-1]
    difference = suffix[1:]-np.cumsum(coarse[::-1], axis=0)[::-1][1:]
    pole_angle = pole['prefactor']*np.arctan2(math.sqrt(1-pole['ua'])*np.cos(z),
                                           math.sqrt(pole['gap'])*np.sin(z))
    dt = float(suffix[0, 0]-half_time)
    da = float(pole['prefactor']*math.pi/2+suffix[0, 1]-half_angle)
    summed = float((omr+abs(oml))*np.sum(errors[:, 0])+np.sum(errors[:, 1]))
    cumulative = max(float(np.max(omr*np.abs(difference[:, 0]))),
                     float(np.max(np.abs(difference[:, 1]-oml*difference[:, 0]))))
    consistency = max(abs(omr*dt), abs(da-oml*dt))
    return suffix[1:, 0], pole_angle+suffix[1:, 1], (
        max(cumulative, 4*summed, consistency), cumulative, summed, consistency, len(refined))


def orbit_at_order(e, L, roots, order, cfg, np, budget):
    pole = pole_parameters(e, L, roots)
    nodes, weights = rule(order, np)
    z, weights = (nodes+1)*math.pi/4, weights*math.pi/4
    u, q, td, jd, remainder = integrands(z, pole, np)
    ht = float(weights@td)
    ha = pole['prefactor']*math.pi/2+float(weights@remainder)
    jr, omr, oml = float(weights@jd), math.pi/ht, ha/ht
    pt, pa, phase_errors = partial_phases(z, pole, ht, ha, omr, oml, cfg, np, budget)
    n, k = np.arange(-cfg.radial_modes, cfg.radial_modes+1), np.asarray(K_VALUES)
    phase = (pa-oml*pt)[:, None, None]*k[None, None, :]-omr*pt[:, None, None]*n[None, :, None]
    v = q*(1+u)
    f = -v*u**3                       # phi_(nCB=0,l=2), r0=1
    fr = -np.sqrt(v)*u**4*(2*u*u-3*v)
    radial = np.einsum('q,q,qnk->nk', weights*td/ht, f, np.cos(phase), optimize=True)
    vr2 = 2*pole['delta']**2*np.sin(z)**2*np.cos(z)**2*(u-pole['third'])/v
    cp = (L*u*u/v-oml)/omr
    norm0 = float((weights*td/ht)@(f*f))
    norm2 = np.einsum('q,qk->k', weights*td/ht,
        vr2[:, None]/omr**2*fr[:, None]**2+(k[None, :]*cp[:, None]*f[:, None])**2)
    ad = math.sqrt(2)*L/(v*np.sqrt(u-pole['third']))
    pole_error = float(np.max(np.abs(ad-pole['fp']/q-remainder)/np.maximum(np.abs(ad), 1e-300)))
    if (not all(math.isfinite(a) and a > 0 for a in (ht, ha, jr, omr, oml, norm0))
            or not np.all(np.isfinite(radial)) or not np.all(np.isfinite(norm2)) or np.any(norm2 < 0)):
        raise ArithmeticError('Nonfinite full-orbit/Fourier diagnostic')
    return dict(radial=radial, omega_r=omr, omega_l=oml, jr=jr,
        norm0=norm0, norm2=norm2, phase_errors=phase_errors, pole_error=pole_error, order=order)


def resolve_orbit(e, L, roots, cfg, np, budget):
    prior = orbit_at_order(e, L, roots, cfg.orbit_order, cfg, np, budget)
    order = cfg.orbit_order*2
    while True:
        budget.check()
        current = orbit_at_order(e, L, roots, order, cfg, np, budget)
        freq = max(abs(current[key]-prior[key])/abs(current[key])
                   for key in ('omega_r', 'omega_l', 'jr'))
        coefficient = float(np.max(np.abs(current['radial']-prior['radial'])))/math.sqrt(current['norm0'])
        norms = max(abs(current['norm0']-prior['norm0'])/current['norm0'],
            float(np.max(np.abs(current['norm2']-prior['norm2'])/np.maximum(current['norm2'], 1e-300))))
        errors = (freq, coefficient, norms, current['phase_errors'][0])
        if max(errors) <= cfg.orbit_tolerance:
            return current, errors
        if order == cfg.maximum_orbit_order:
            raise ArithmeticError('Unresolved retained orbit; errors='+repr(errors))
        prior, order = current, order*2


def quintic_filter(x, np):
    x = np.asarray(x, dtype=float)
    value = np.empty_like(x)
    small = np.abs(x) <= 1
    xx, term = x[small]**2, np.ones_like(x[small])
    total = term.copy()
    for j in range(1, 17):
        term *= -xx/(2*j*(2*j+5))
        total += term
    value[small] = total
    y = x[~small]
    value[~small] = 15*((3-y*y)*np.sin(y)-3*y*np.cos(y))/y**5
    return value


def history(delta, cfg, np):
    length = cfg.duration-cfg.ramp
    return cfg.shape*length*np.sinc(delta*length/(2*math.pi))*quintic_filter(delta*cfg.ramp/2, np)


def history_envelope(dmin, cfg, np):
    envelope = np.full_like(dmin, cfg.shape*(cfg.duration-cfg.ramp))
    far = dmin > 2/(cfg.duration-cfg.ramp)
    envelope[far] = 2*cfg.shape/dmin[far]
    x = dmin*cfg.ramp/2
    large = x > 1
    inv = 1/x[large]
    envelope[large] *= np.minimum(1., 15*inv**3*(1+3*inv+3*inv**2))
    return envelope


def derivatives(e, L, coefficients):
    h = he = hs = 0.
    for p, c in zip(POWERS, coefficients):
        ap, bp = 4*p/((p+2.5)*(p+3.5)), 4/(p+1)
        h += c*(-ap*e**(p-1)+bp*e**(p+1)+L*L*e**p)
        he += c*(-ap*(p-1)*e**(p-2)+4*e**p+p*L*L*e**(p-1))
        hs += c*e**p
    return h, he, hs


def population_maps():
    return {'F0': (0.,)*6, 'A_full_plus': A_COEFFICIENTS,
        'A_full_minus': tuple(-v for v in A_COEFFICIENTS),
        'A_half_plus': tuple(v/2 for v in A_COEFFICIENTS),
        'A_nine_tenths_plus': NINE_TENTHS_COEFFICIENTS}


def angular_coefficients(mu, m, np):
    a, b = (1+mu)/2, (mu-1)/2
    plus = math.sqrt(15/8)*np.stack((b*b, 2*a*b, a*a), axis=-1)
    return plus if m == 2 else plus[:, ::-1]


def formula_fixture(cfg, np, quad):
    """Independent finite formula checks; no claim about action convergence."""
    mu, weights = rule(3, np)
    k = np.asarray(K_VALUES)
    angular_error = field_error = nodal_error = 0.
    e, L, nu = .4, .7, .31
    h, he, hs = derivatives(e, L, A_COEFFICIENTS)
    ge = .5*e**2.5*(7-11*Q*e*e)
    ak = np.asarray((.75, .5, .75))
    for m in M_VALUES:
        csq = angular_coefficients(mu, m, np)**2
        am = weights@csq
        bm = (weights*mu)@csq
        angular_error = max(angular_error, float(np.max(np.abs(am-ak))),
                           float(np.max(np.abs(bm-ak*m*k/6))))
        kappa = -nu*(ge+L*mu[:, None]*he)+2*k[None, :]*L*L*mu[:, None]*hs+m*h
        explicit = weights@(csq*kappa)
        analytic = ak*(-nu*ge+m*h)+ak*m*k/6*L*(2*k*L*hs-nu*he)
        nodal_error = max(nodal_error, float(np.max(np.abs(explicit-analytic))))
    for x, y, z, angle in ((.3, -.7, .2, .4), (-1.2, .2, .5, -.8)):
        r2 = x*x+y*y+z*z
        radial = -r2/(1+r2)**2.5
        y22 = math.sqrt(15/8)*(x+1j*y)**2/r2
        amplitude = 3*BAR_MASS/(7*math.sqrt(30))
        spectral = radial*amplitude*(y22*complex(math.cos(-2*angle), math.sin(-2*angle))
            +y22.conjugate()*complex(math.cos(2*angle), math.sin(2*angle)))
        qxy = math.cos(2*angle)*(x*x-y*y)+2*math.sin(2*angle)*x*y
        cartesian = -3*BAR_MASS/14*qxy/(1+r2)**2.5
        field_error = max(field_error, abs(spectral-cartesian))
    def shape(t):
        s = min(t/cfg.ramp, (cfg.duration-t)/cfg.ramp, 1.)
        return cfg.shape*s**3*(10-15*s+6*s*s)
    window_error = 0.
    for delta in (0., 1e-12, .001, .12, -.31, 2.):
        cuts = (0., cfg.ramp, cfg.duration-cfg.ramp, cfg.duration)
        real = sum(quad(lambda t: shape(t)*math.cos(delta*t), a, b, epsabs=2e-11,
                        epsrel=2e-12)[0] for a, b in zip(cuts[:-1], cuts[1:]))
        imag = sum(quad(lambda t: shape(t)*math.sin(delta*t), a, b, epsabs=2e-11,
                        epsrel=2e-12)[0] for a, b in zip(cuts[:-1], cuts[1:]))
        exact = float(history(np.asarray([delta]), cfg, np)[0])*complex(
            math.cos(delta*cfg.duration/2), math.sin(delta*cfg.duration/2))
        window_error = max(window_error, abs(complex(real, imag)-exact)/max(cfg.shape*(cfg.duration-cfg.ramp), 1.))
    passed = angular_error < 1e-12 and nodal_error < 1e-10 and field_error < 1e-14 and window_error < 3e-12
    return dict(passed=passed, angular_error=angular_error, nodal_error=nodal_error,
                physical_field_error=field_error, window_scaled_error=window_error,
                scope='Finite normalization/history checks, not continuum or positivity proof')


def calculate(cfg, np, brentq, budget):
    maps = population_maps()
    names = list(maps)
    work, impulse, tail = np.zeros((5, 2)), np.zeros((5, 2)), np.zeros((5, 2))
    maximum_errors = np.zeros(4)
    mass = max_reality = max_pole = min_factor = max_factor = 0.
    min_factor, max_order, max_panels32 = math.inf, 0, 0
    en, ew = rule(cfg.ne, np)
    etan, etaw = rule(cfg.neta, np)
    n, k = np.arange(-cfg.radial_modes, cfg.radial_modes+1), np.asarray(K_VALUES)
    ak, amplitude = np.asarray((.75, .5, .75)), 3*BAR_MASS/(7*math.sqrt(30))
    for ie, (enode, eweight) in enumerate(zip((en+1)/2, ew/2)):
        e = float(enode)
        uc = brentq(lambda u: u*(1+u*u)/2-e, 0., 1., xtol=5e-324, rtol=1e-14)
        lc = (1-uc)*(1+uc)/math.sqrt(uc)
        g0, ge = e**3.5*(1-Q*e*e), .5*e**2.5*(7-11*Q*e*e)
        for il, (eta, etaweight) in enumerate(zip((etan+1)/2, etaw/2)):
            budget.check()
            L = float(eta)*lc
            try:
                row, errors = resolve_orbit(e, L, turning_points(e, L, brentq), cfg, np, budget)
            except ArithmeticError as failure:
                raise ArithmeticError(f'Retained action node ({ie},{il}), e={e!r}, eta={float(eta)!r}, L={L!r}: {failure}') from failure
            maximum_errors = np.maximum(maximum_errors, errors)
            max_order = max(max_order, row['order'])
            max_panels32 = max(max_panels32, row['phase_errors'][4])
            max_pole = max(max_pole, row['pole_error'])
            r = row['radial']
            max_reality = max(max_reality, float(np.max(np.abs(r-r[::-1, ::-1])))/math.sqrt(row['norm0']))
            omr, oml = row['omega_r'], row['omega_l']
            nu = omr*n[:, None]+oml*k[None, :]
            weight = (2*math.pi)**3*float(eweight)*float(etaweight)*lc*lc*float(eta)/omr
            mass += 2*DF_C*g0*weight
            gap0, gap2 = row['norm0']-np.sum(r*r, axis=0), row['norm2']-np.sum(n[:, None]**2*r*r, axis=0)
            if (np.any(gap0 < -20*cfg.orbit_tolerance*row['norm0'])
                    or np.any(gap2 < -20*cfg.orbit_tolerance*np.maximum(row['norm2'], 1e-300))):
                raise ArithmeticError('Resolved Fourier coefficients violate Parseval norms')
            p0 = np.maximum(gap0, 0)+20*cfg.orbit_tolerance*row['norm0']
            p2 = np.maximum(gap2, 0)+20*cfg.orbit_tolerance*row['norm2']
            nu2 = (omr*np.sqrt(p2)+np.abs(k*oml)*np.sqrt(p0))**2
            nu1 = np.sqrt(p0*nu2)
            for pi, coefficients in enumerate(maps.values()):
                h, he, hs = derivatives(e, L, coefficients)
                factors = (1-L*h/g0, 1+L*h/g0)  # sampled diagnostic, never a certificate
                min_factor, max_factor = min(min_factor, *factors), max(max_factor, *factors)
                for mi, m in enumerate(M_VALUES):
                    hbar = DF_C*ak*((-nu*ge+m*h)+m*k/6*L*(2*k*L*hs-nu*he))
                    square = (r*amplitude*history(nu-m*cfg.omega, cfg, np))**2
                    work[pi, mi] += -.5*weight*float(np.sum(hbar*nu*square))
                    impulse[pi, mi] += -.5*m*weight*float(np.sum(hbar*square))
                    a, b = ge+m*k*L*he/6, m*h+m*k*k*L*L*hs/3
                    dmin = np.maximum(0., omr*(cfg.radial_modes+1)-np.abs(k*oml-m*cfg.omega))
                    prefactor = .5*DF_C*ak*weight*amplitude**2*history_envelope(dmin, cfg, np)**2
                    tail[pi, 0] += float(np.sum(prefactor*(np.abs(a)*nu2+np.abs(b)*nu1)))
                    tail[pi, 1] += abs(m)*float(np.sum(prefactor*(np.abs(a)*nu1+np.abs(b)*p0)))
            if (ie*cfg.neta+il+1) % 32 == 0:
                print(json.dumps({'stage': 'actions', 'completed': ie*cfg.neta+il+1,
                    'total': cfg.ne*cfg.neta, 'orbit_order': row['order']}), file=sys.stderr, flush=True)
    values = np.stack((np.sum(work, axis=1), np.sum(impulse, axis=1)), axis=-1)
    if (not np.all(np.isfinite(values)) or not np.all(np.isfinite(tail)) or mass <= 0
            or max_reality > 1e-10 or values[0, 0] < 0 or min_factor < .5-1e-10 or max_factor > 1.5+1e-10):
        raise ArithmeticError('Nonfinite response, reality/passivity failure or sampled DF margin failure')
    return dict(populations={name: {'W2': float(values[i, 0]), 'J2': float(values[i, 1]),
        'rotation_W2': cfg.omega*float(values[i, 1]),
        'switching_W2': float(values[i, 0])-cfg.omega*float(values[i, 1]),
        'by_m_W2': work[i].tolist(), 'by_m_J2': impulse[i].tolist(),
        'omitted_radial_Fourier_response_proxies': tail[i].tolist()} for i, name in enumerate(names)},
        physical_mass_quadrature=[mass]*len(names), exact_halo_mass=.9, mass_renormalization=False,
        maximum_orbit_errors=maximum_errors.tolist(), maximum_orbit_order=max_order,
        maximum_panels_refined_to_GL32=max_panels32, pole_reconstruction_error=max_pole,
        relative_Fourier_reality_error=max_reality, sampled_DF_factor_range=[min_factor, max_factor],
        bare_affine_sum_residual=(values[1]+values[2]-2*values[0]).tolist(),
        tail_scope='Numerical Parseval/frequency/DF/history-weighted proxies at retained action nodes; not rigorous action-tail or total response-error bounds')


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--preset', choices=('quick', 'reference'), default='quick')
    for name in ('ne', 'neta', 'radial_modes', 'orbit_order', 'maximum_orbit_order',
                 'cpu_seconds', 'wall_seconds', 'memory_mib'):
        parser.add_argument('--'+name.replace('_', '-'), type=int)
    for name in ('orbit_tolerance', 'omega', 'duration', 'ramp', 'shape'):
        parser.add_argument('--'+name.replace('_', '-'), type=float)
    parser.add_argument('--check-formulas', action='store_true', help='Run formula fixtures only; not a response calculation')
    parser.add_argument('--output', help='Create a new JSON file; existing files are never overwritten')
    arguments = parser.parse_args()
    values = {key: value for key, value in vars(arguments).items() if value is not None
              and key not in ('preset', 'check_formulas', 'output')}
    defaults = asdict(Config(ne=128, neta=128, radial_modes=64) if arguments.preset == 'reference' else Config())
    cfg = Config(**(defaults | values))
    cfg.validate()
    if arguments.output and Path(arguments.output).exists():
        parser.error('Output exists; select a new filename')
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        os.environ[name] = '1'
    pins = provenance()
    started = time.process_time()
    budget = Budget(cfg)
    def interrupted(unused_signal, unused_frame):
        raise InterruptedError('Interrupted process; no partial physical response claim')
    for name in ('SIGTERM', 'SIGINT', 'SIGXCPU'):
        if hasattr(signal, name):
            signal.signal(getattr(signal, name), interrupted)
    result = {'schema': 'bare-plummer-complete-cycle-public-v1', 'complete': False,
        'config': asdict(cfg), 'preset': arguments.preset, 'source_sha256': pins,
        'method_ancestors_sha256': METHOD_ANCESTORS, 'physical_reference': {
            'G': 1, 'total_mass': 1, 'radius': 1, 'bar_mass': '1/10', 'halo_Q': '14/33'},
        'physical_coefficients': {name: dict(zip(map(str, POWERS), cs)) for name, cs in population_maps().items()},
        'scope': 'Bare prescribed field, initially stationary full-support populations; no self-gravity, stability, autonomous rotor or observational result',
        'positivity_certificate': {'companion': 'certificate.json', 'theorem': 'MATCHING_AND_POSITIVITY.md',
            'verified_by_this_run': False, 'publication_binding': 'Companions must be supplied and hash-bound by publisher before release'},
        'action_measure': '(2pi)^3 Lc^2 eta/omega_r de deta dmu, mu in [-1,1] without normalization',
        'units': {'W2': 'G M^2/a per contrast squared', 'J2': 'M sqrt(G M a) per contrast squared'},
        'process_limits': budget.limits, 'continuum_qualification': 'Not established by a single deterministic quadrature'}
    try:
        import numpy as np
        import scipy
        from scipy.optimize import brentq
        result['versions'] = {'python': sys.version.split()[0], 'numpy': np.__version__, 'scipy': scipy.__version__}
        if arguments.check_formulas:
            from scipy.integrate import quad
            result['formula_fixture'] = formula_fixture(cfg, np, quad)
            result['complete'] = result['formula_fixture']['passed']
            result['response_calculated'] = False
        else:
            result.update(calculate(cfg, np, brentq, budget))
            result['complete'], result['response_calculated'] = True, True
        budget.check()
        if provenance() != pins:
            raise RuntimeError('Local source/document operand changed while running')
    except (Exception, KeyboardInterrupt) as failure:
        result['complete'] = False
        result['error'] = type(failure).__name__+': '+str(failure)
    result['process_CPU_seconds'] = time.process_time()-started
    payload = json.dumps(result, indent=2, allow_nan=False)
    if arguments.output:
        with Path(arguments.output).open('x', encoding='utf-8') as output:
            output.write(payload+'\n')
    print(payload, flush=True)
    return 0 if result['complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
