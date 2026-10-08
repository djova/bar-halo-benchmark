#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Portable full-support Plummer l2 collective response, with NumPy/SciPy.

The adjacent immutable bare_run.py supplies the existing orbital primitives
and actual DF constants. This port is not an independent response algorithm.
No saved response, host service or campaign path is needed at runtime.
"""
from dataclasses import asdict, dataclass, replace
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import signal
import stat
import sys
import tempfile
import time
import types

BARE_SHA = 'abc1d554e8a642e4b2d0007f664a9b372c8d62c331966d37da517d3f66fdd9b1'
SOURCE_FILES = ('run.py', 'bare_run.py', 'README.md', 'METHOD.md', 'requirements.txt')
POPS = ('F0', 'A_full_plus', 'A_full_minus', 'A_half_plus', 'A_nine_tenths_plus')
M_VALUES, K_VALUES = (-2, 2), (-2, 0, 2)
DF_C, BAR_MASS, Q = 24*math.sqrt(2)/(7*math.pi**3), .1, 14/33
ANCESTORS = {
    'robust_response.py': 'ae125e3d18708e2d1a27a0fdda5f29c70434038216d777f2b119148644c73f42',
    'compact_stationary_collective.py': '52b43b5e809ebab74362ea81f6e7d64a77762ffd6d831c835910a8eb4f1bd46c',
    'stationary_collective.py': 'f7c7e23b1d80d70b995fdd729df030be9e1df181c5a92af9e1720a1de7b0e485',
    'robust_orbits.py': '144eb392a8b0253b6fa59dccaca2f6225a247319bb5b6679351c86affb69df1b',
    'collective_basis.py': 'afe4d7ba393cc582f3ceb4ba598770c4084561c04f01d5244670d0b671dba426',
}


@dataclass(frozen=True)
class Config:
    ne: int = 8
    neta: int = 8
    nmax: int = 4
    radial_modes: int = 8
    orbit_order: int = 64
    maximum_orbit_order: int = 2048
    orbit_tolerance: float = 3e-8
    duration: float = 120.
    rise: float = 12.
    fall: float = 12.
    dt: float = .02
    omega: float = .12
    theta0: float = 0.
    shape: float = .8
    self_gravity: int = 1
    record_every: int = 50
    chunk_actions: int = 64
    checkpoint_seconds: float = 120.
    cpu_seconds: int = 3600
    wall_seconds: int = 7200
    memory_mib: int = 2048
    output_mib: int = 64

    @property
    def ramp(self):
        return self.rise

    @property
    def bar_mass(self):
        return BAR_MASS

    @property
    def populations(self):
        return POPS

    def validate(self):
        integer_names = ('ne', 'neta', 'nmax', 'radial_modes', 'orbit_order',
            'maximum_orbit_order', 'self_gravity', 'record_every', 'chunk_actions',
            'cpu_seconds', 'wall_seconds', 'memory_mib', 'output_mib')
        if any(type(getattr(self, name)) is not int for name in integer_names):
            raise ValueError('Explicit integer grid/basis/process controls required')
        if (not 2 <= self.ne <= 128 or not 2 <= self.neta <= 128 or not 0 <= self.nmax <= 6
                or not 1 <= self.radial_modes <= 128 or self.orbit_order not in (32, 64, 128, 256)
                or self.maximum_orbit_order not in (64, 128, 256, 512, 1024, 2048)
                or self.maximum_orbit_order < 2*self.orbit_order or self.self_gravity not in (0, 1)
                or self.record_every < 1 or not 1 <= self.chunk_actions <= 1024
                or not 60 <= self.cpu_seconds <= 86400 or not 60 <= self.wall_seconds <= 172800
                or not 512 <= self.memory_mib <= 8192 or not 8 <= self.output_mib <= 1024):
            raise ValueError('Grid/basis/process controls exceed declared bounds')
        values = (self.orbit_tolerance, self.duration, self.rise, self.fall, self.dt,
            self.omega, self.theta0, self.shape, self.checkpoint_seconds)
        if (not all(type(v) in (int, float) and math.isfinite(v) for v in values)
                or not 1e-12 <= self.orbit_tolerance <= 3e-8 or not 0 < self.duration <= 240
                or min(self.rise, self.fall, self.dt, self.checkpoint_seconds) <= 0
                or self.rise != self.fall or self.rise+self.fall > self.duration
                or not .001 <= self.dt <= .1 or not 0 <= self.omega <= 2 or not 0 <= self.shape <= 1):
            raise ValueError('Finite bounded complete symmetric cyclic profile required')
        if any(abs(t/self.dt-round(t/self.dt)) > 1e-9 for t in (self.duration, self.rise, self.fall)):
            raise ValueError('Cycle boundaries must be integer-step endpoints')
        if self.record_every > round(self.duration/self.dt):
            raise ValueError('At least initial/final recorded endpoints required')


def local_bytes(name):
    path = Path(__file__).resolve().parent/name
    if path.resolve(strict=True) != path:
        raise ValueError('Real adjacent source/document dependency required')
    with path.open('rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= 256*1024:
            raise ValueError('Small bounded local source/document required')
        raw = stream.read(256*1024+1); after = os.fstat(stream.fileno())
    identity = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if identity(before) != identity(after) or identity(after) != identity(path.stat()) or len(raw) != before.st_size:
        raise RuntimeError('Local operand changed during bounded read')
    return raw


def provenance():
    return {name: hashlib.sha256(local_bytes(name)).hexdigest() for name in SOURCE_FILES}


def load_bare():
    """Execute exactly the checked local bytes in a separate named namespace."""
    raw = local_bytes('bare_run.py')
    if hashlib.sha256(raw).hexdigest() != BARE_SHA:
        raise ValueError('Adjacent immutable public bare runner bytes differ')
    name = '_portable_collective_bare_dependency'
    module = types.ModuleType(name)
    module.__file__ = 'bare_run.py'
    sys.modules[name] = module  # Dataclass introspection needs its named module.
    exec(compile(raw, 'bare_run.py', 'exec'), module.__dict__)
    if module.M_VALUES != M_VALUES or module.K_VALUES != K_VALUES or module.Q != Q or module.BAR_MASS != BAR_MASS:
        raise ValueError('Immutable bare primitive model/API differs')
    return module


class Budget:
    def __init__(self, cfg):
        self.cfg = cfg
        self.cpu0, self.wall0 = time.process_time(), time.monotonic()
        self.limits = {'CPU': 'cooperative only', 'address_space': 'not available', 'wall': 'cooperative only'}
        try:
            import resource
        except ImportError:
            return
        for name, amount, label in (('RLIMIT_CPU', cfg.cpu_seconds, 'CPU'),
                ('RLIMIT_AS', cfg.memory_mib*1024**2, 'address_space')):
            if not hasattr(resource, name):
                continue
            key = getattr(resource, name); soft, hard = resource.getrlimit(key)
            limit = min([amount]+[v for v in (soft, hard) if v != resource.RLIM_INFINITY])
            new_hard = min(limit+5, hard) if name == 'RLIMIT_CPU' and hard != resource.RLIM_INFINITY else limit+5
            if name != 'RLIMIT_CPU':
                new_hard = limit
            try:
                resource.setrlimit(key, (limit, new_hard))
            except (ValueError, OSError) as failure:
                self.limits[label] = 'unavailable: '+type(failure).__name__
            else:
                self.limits[label] = dict(soft=limit, hard=new_hard)

    def check(self):
        if time.process_time()-self.cpu0 > self.cfg.cpu_seconds or time.monotonic()-self.wall0 > self.cfg.wall_seconds:
            raise TimeoutError('Process budget exhausted; no retained node/mode omitted')


class Outputs:
    """New output directory only; bounded atomic writes and held identity."""
    def __init__(self, supplied, cfg, budget):
        self.path = Path(supplied).absolute()
        if self.path.parent.resolve(strict=True) != self.path.parent:
            raise ValueError('Real existing output parent required')
        self.path.mkdir()  # Refuses every existing directory, file or link.
        self.fd = os.open(self.path, os.O_RDONLY|os.O_DIRECTORY) if hasattr(os, 'O_DIRECTORY') else None
        initial = self.path.stat(); self.identity = (initial.st_dev, initial.st_ino)
        self.limit, self.sizes, self.budget = cfg.output_mib*1024**2, {}, budget

    def check(self):
        self.budget.check()
        current = self.path.stat()
        held = os.fstat(self.fd) if self.fd is not None else current
        if (self.path.resolve(strict=True) != self.path or self.identity != (current.st_dev, current.st_ino)
                or (held.st_dev, held.st_ino) != (current.st_dev, current.st_ino)):
            raise RuntimeError('Held new output directory identity changed')

    def write(self, name, writer, replace_checkpoint=False):
        self.check()
        if '/' in name or name.startswith('.') or (replace_checkpoint and name != 'checkpoint.npz'):
            raise ValueError('Fixed local output name required')
        fd, temporary = tempfile.mkstemp(prefix='.'+name+'-', dir=self.path)
        allowance = self.limit-sum(self.sizes.values())
        class Capped:
            def __init__(self, stream): self.stream = stream
            def write(self, raw):
                self_outer.check()
                if self.stream.tell()+len(raw) > allowance:
                    raise ValueError('Aggregate output byte budget exhausted')
                return self.stream.write(raw)
            def __getattr__(self, key): return getattr(self.stream, key)
        self_outer = self
        try:
            with os.fdopen(fd, 'wb') as stream:
                writer(Capped(stream)); stream.flush(); os.fsync(stream.fileno())
                size = os.fstat(stream.fileno()).st_size
            self.check()
            if replace_checkpoint and name in self.sizes:
                os.replace(temporary, self.path/name)
            else:
                os.link(temporary, self.path/name)
            self.sizes[name] = size
            if self.fd is not None: os.fsync(self.fd)
        finally:
            try: os.unlink(temporary)
            except FileNotFoundError: pass

    def json(self, name, value):
        def writer(stream):
            encoder = json.JSONEncoder(indent=2, allow_nan=False)
            for piece in encoder.iterencode(value): stream.write(piece.encode('utf-8'))
            stream.write(b'\n')
        self.write(name, writer)

    def npz(self, name, np, **arrays):
        self.write(name, lambda stream: np.savez(stream, **arrays), name == 'checkpoint.npz')

    def close(self):
        if self.fd is not None: os.close(self.fd)


def negative_norm(n, ell=2):
    """Physical CB density-potential norm, angular norm4pi and r0=1."""
    lam = ell+1
    prefactor = -math.pi*16.**(-lam)*math.exp(math.lgamma(2*lam)-2*math.lgamma(lam))
    for j in range(1, n+1): prefactor *= (2*lam+j-1)/j
    return prefactor*(4*(n+lam)**2-1)/(n+lam)


def radial_values(u, one_minus_u, nmax, np):
    v, chi = one_minus_u*(1+u), 1-2*u*u
    def gegenbauer(lam, limit):
        values = [np.ones_like(u)]
        if limit: values.append(2*lam*chi)
        for n in range(1, limit):
            values.append((2*(n+lam)*chi*values[-1]-(n+2*lam-1)*values[-2])/(n+1))
        return values
    c = gegenbauer(3, nmax)
    cp = [np.zeros_like(u)]+[6*x for x in gegenbauer(4, max(nmax-1, 0))[:nmax]]
    f = np.stack([-v*u**3*cn for cn in c], axis=-1)
    fr = np.stack([-np.sqrt(v)*u**4*((2*u*u-3*v)*cn+4*v*u*u*dc) for cn, dc in zip(c, cp)], axis=-1)
    return f, fr


def phase_data(z, pole, ht, ha, omr, oml, cfg, np, budget, bare):
    """Existing adjacent-panel algorithm, retaining all frozen diagnostics."""
    bounds = np.concatenate(([0.], z, [math.pi/2])); indices = np.arange(len(bounds)-1)
    if not np.all(np.diff(bounds) > 0): raise ArithmeticError('Ordered complete half-orbit panels required')
    coarse = bare.panels(bounds, indices, 8, pole, np, budget)
    fine = bare.panels(bounds, indices, 16, pole, np, budget)
    orders = np.full(len(indices), 16); errors = np.abs(fine-coarse)
    allowance = cfg.orbit_tolerance/4
    local = (omr+abs(oml))*errors[:, 0]+errors[:, 1]
    if float(np.sum(local)) > allowance:
        selected = np.flatnonzero(local > allowance/len(indices))
        coarse[selected] = fine[selected]
        fine[selected] = bare.panels(bounds, selected, 32, pole, np, budget)
        errors[selected] = np.abs(fine[selected]-coarse[selected]); orders[selected] = 32
    suffix = np.cumsum(fine[::-1], axis=0)[::-1]
    difference = suffix[1:]-np.cumsum(coarse[::-1], axis=0)[::-1][1:]
    pole_angle = pole['prefactor']*np.arctan2(math.sqrt(1-pole['ua'])*np.cos(z), math.sqrt(pole['gap'])*np.sin(z))
    dt, da = float(suffix[0, 0]-ht), float(pole['prefactor']*math.pi/2+suffix[0, 1]-ha)
    cumulative = max(float(np.max(omr*np.abs(difference[:, 0]))), float(np.max(np.abs(difference[:, 1]-oml*difference[:, 0]))))
    summed = float((omr+abs(oml))*np.sum(errors[:, 0])+np.sum(errors[:, 1]))
    consistency = max(abs(omr*dt), abs(da-oml*dt))
    info = dict(error=max(cumulative, 4*summed, consistency), cumulative_difference=cumulative,
        summed_local_difference=summed, halfperiod_consistency=consistency, maximum_panel_order=int(np.max(orders)),
        maximum_local_dimensionless_difference=float(np.max((omr+abs(oml))*errors[:, 0]+errors[:, 1])),
        panels32=int(np.sum(orders == 32)), panel_count=len(indices))
    return suffix[1:, 0], pole_angle+suffix[1:, 1], info


def orbit_at_order(e, L, roots, order, cfg, np, budget, bare):
    pole = bare.pole_parameters(e, L, roots)
    nodes, weights = bare.rule(order, np); z, weights = (nodes+1)*math.pi/4, weights*math.pi/4
    u, one_minus, td, jd, remainder = bare.integrands(z, pole, np)
    ht, ha, jr = float(weights@td), pole['prefactor']*math.pi/2+float(weights@remainder), float(weights@jd)
    omr, oml = math.pi/ht, ha/ht
    pt, pa, info = phase_data(z, pole, ht, ha, omr, oml, cfg, np, budget, bare)
    n, k = np.arange(-cfg.radial_modes, cfg.radial_modes+1), np.asarray(K_VALUES)
    phase = (pa-oml*pt)[:, None, None]*k[None, None, :]-omr*pt[:, None, None]*n[None, :, None]
    f, fr = radial_values(u, one_minus, cfg.nmax, np)
    radial = np.einsum('q,qb,qnk->nkb', weights*td/ht, f, np.cos(phase), optimize=True)
    v = one_minus*(1+u)
    vr2 = 2*pole['delta']**2*np.sin(z)**2*np.cos(z)**2*(u-pole['third'])/v
    cp = (L*u*u/v-oml)/omr
    norm0 = np.einsum('q,qb->b', weights*td/ht, f*f)
    norm2 = np.einsum('q,qkb->kb', weights*td/ht, vr2[:, None, None]/omr**2*fr[:, None, :]**2+
        (k[None, :, None]*cp[:, None, None]*f[:, None, :])**2)
    ad = math.sqrt(2)*L/(v*np.sqrt(u-pole['third']))
    pole_error = float(np.max(np.abs(ad-(pole['fp']/one_minus+remainder))/np.maximum(np.abs(ad), 1e-300)))
    if (not all(math.isfinite(x) and x > 0 for x in (ht, ha, jr, omr, oml))
            or not all(np.all(np.isfinite(x)) for x in (radial, norm0, norm2)) or np.any(norm0 <= 0) or np.any(norm2 < 0)):
        raise ArithmeticError('Finite positive full orbit/Fourier diagnostics required')
    return dict(radial=radial, omega_r=omr, omega_l=oml, jr=jr, value_norm=norm0,
        derivative_norm=norm2, phase_diagnostics=info, pole_reconstruction_error=pole_error, order=order, up_gap=pole['gap'])


def resolve_orbit(e, L, roots, cfg, np, budget, bare):
    prior = orbit_at_order(e, L, roots, cfg.orbit_order, cfg, np, budget, bare)
    order = 2*cfg.orbit_order
    while True:
        budget.check(); current = orbit_at_order(e, L, roots, order, cfg, np, budget, bare)
        freq = max(abs(current[key]-prior[key])/abs(current[key]) for key in ('omega_r', 'omega_l', 'jr'))
        coefficient = float(np.max(np.abs(current['radial']-prior['radial'])/np.sqrt(current['value_norm'])[None, None, :]))
        norms = max(float(np.max(np.abs(current['value_norm']-prior['value_norm'])/current['value_norm'])),
            float(np.max(np.abs(current['derivative_norm']-prior['derivative_norm'])/np.maximum(current['derivative_norm'], 1e-300))))
        errors = (freq, coefficient, norms, current['phase_diagnostics']['error'])
        if max(errors) <= cfg.orbit_tolerance: return current, errors
        if order == cfg.maximum_orbit_order: raise ArithmeticError('Unresolved retained orbit: '+repr(errors))
        prior, order = current, 2*order


def build_library(cfg, np, brentq, budget, bare):
    started = time.process_time(); en, ew = bare.rule(cfg.ne, np); ln, lw = bare.rule(cfg.neta, np)
    e, eta = np.meshgrid((en+1)/2, (ln+1)/2, indexing='ij'); e, eta = e.ravel(), eta.ravel()
    probability = np.outer(ew/2, lw/2).ravel()
    uc = np.asarray([brentq(lambda u: u*(1+u*u)/2-x, 0., 1., xtol=5e-324, rtol=1e-14) for x in e])
    lc = (1-uc)*(1+uc)/np.sqrt(uc); L = eta*lc; rows, roots_list, errors = [], [], []
    for ai, (binding, angular) in enumerate(zip(e, L)):
        budget.check(); roots = bare.turning_points(float(binding), float(angular), brentq)
        try: row, error = resolve_orbit(float(binding), float(angular), roots, cfg, np, budget, bare)
        except ArithmeticError as failure: raise ArithmeticError('Retained action node '+str(ai)+': '+str(failure)) from failure
        rows.append(row); roots_list.append(roots); errors.append(error)
        if ai % 8 == 0:
            print(json.dumps(dict(stage='orbital-library', completed_nodes=ai+1, retained_nodes=len(e))), file=sys.stderr, flush=True)
    radial = np.stack([x['radial'] for x in rows]); omr = np.asarray([x['omega_r'] for x in rows]); oml = np.asarray([x['omega_l'] for x in rows])
    n, k = np.arange(-cfg.radial_modes, cfg.radial_modes+1), np.asarray(K_VALUES)
    weight = (2*math.pi)**3*probability*lc*lc*eta/omr
    nu = omr[:, None, None]*n[None, :, None]+oml[:, None, None]*k[None, None, :]
    vn = np.stack([x['value_norm'] for x in rows]); dn = np.stack([x['derivative_norm'] for x in rows])
    vg, dg = vn[:, None, :]-np.sum(radial*radial, axis=1), dn-np.sum(n[None, :, None, None]**2*radial*radial, axis=1)
    if np.any(vg < -20*cfg.orbit_tolerance*vn[:, None, :]) or np.any(dg < -20*cfg.orbit_tolerance*np.maximum(dn, 1e-300)):
        raise ArithmeticError('Retained Fourier coefficients violate Parseval norms')
    return dict(e=e, eta=eta, L=L, Lc=lc, weight=weight, radial=radial, nu=nu, radial_n=n, inplane_k=k,
        omega_r=omr, omega_l=oml, jr=np.asarray([x['jr'] for x in rows]), roots=np.asarray(roots_list),
        order=np.asarray([x['order'] for x in rows]), up_gap=np.asarray([x['up_gap'] for x in rows]),
        quadrature_errors=np.asarray(errors), value_norm=vn, derivative_norm=dn,
        value_tail_proxy=np.maximum(vg, 0)+20*cfg.orbit_tolerance*vn[:, None, :],
        derivative_tail_proxy=np.maximum(dg, 0)+20*cfg.orbit_tolerance*dn,
        phase_panel_order=np.asarray([x['phase_diagnostics']['maximum_panel_order'] for x in rows]),
        phase_panel_errors=np.asarray([[x['phase_diagnostics'][key] for key in ('cumulative_difference', 'summed_local_difference',
            'halfperiod_consistency', 'maximum_local_dimensionless_difference')] for x in rows]),
        pole_reconstruction_error=np.asarray([x['pole_reconstruction_error'] for x in rows]), construction_CPU_seconds=time.process_time()-started)


def chunks(cfg, library):
    width = len(library['radial_n'])*3
    for left in range(0, len(library['e']), cfg.chunk_actions):
        right = min(left+cfg.chunk_actions, len(library['e']))
        yield left, right, slice(left*width, right*width)


def build_operator(cfg, library, maps, np, budget, bare):
    started = time.process_time(); b = cfg.nmax+1
    expected = (cfg.ne*cfg.neta, 2*cfg.radial_modes+1, 3, b)
    if (tuple(maps) != POPS or maps != bare.population_maps() or library['radial'].shape != expected
            or library['nu'].shape != expected[:3] or tuple(library['inplane_k']) != K_VALUES
            or not np.array_equal(library['radial_n'], np.arange(-cfg.radial_modes, cfg.radial_modes+1))):
        raise ValueError('All five actual DFs and full signed n/k/radial lattice required')
    r, nu = library['radial'].reshape(-1, b), library['nu'].ravel()
    norms = np.asarray([negative_norm(n) for n in range(b)])
    kappa = np.empty((5, 2, len(nu))); kernel = np.zeros((5, 2, b, b), dtype=complex)
    force, drift = cfg.dt/(1+.5j*cfg.dt*nu), (1-.5j*cfg.dt*nu)/(1+.5j*cfg.dt*nu)
    ak, k = np.asarray((.75, .5, .75))[None, None, :], library['inplane_k'][None, None, :]
    for left, right, sl in chunks(cfg, library):
        budget.check(); e, L = library['e'][left:right, None, None], library['L'][left:right, None, None]
        frequency, weight = library['nu'][left:right], library['weight'][left:right, None, None]
        ge = .5*e**2.5*(7-11*Q*e*e)
        for pi, coefficients in enumerate(maps.values()):
            h, he, hs = bare.derivatives(e, L, coefficients)
            for mi, m in enumerate(M_VALUES):
                nodal = DF_C*ak*(-frequency*ge+m*h+(m*k/6)*L*(2*k*L*hs-frequency*he))
                kappa[pi, mi, sl] = (weight*nodal).ravel()
                kernel[pi, mi] += 1j*(r[sl].T@((kappa[pi, mi, sl]*force[sl])[:, None]*r[sl]))/norms[:, None]
    left_matrix = np.eye(b)[None, None, :, :]-.5*cfg.self_gravity*kernel
    condition = np.linalg.cond(left_matrix)
    if not all(np.all(np.isfinite(x)) for x in (r, nu, norms, kappa, kernel, condition)) or np.any(norms >= 0) or np.max(condition) > 1e12:
        raise ArithmeticError('Finite own-DF contraction and qualified midpoint conditioning required')
    mass = float(np.sum(library['weight']*2*DF_C*library['e']**3.5*(1-Q*library['e']**2)))
    return dict(r=r, nu=nu, norms=norms, weighted_kappa=kappa, force=force, drift=drift, kernel=kernel,
        inverse=np.linalg.inv(left_matrix), condition=condition, physical_mass_totals=[mass]*5, construction_CPU_seconds=time.process_time()-started)


def project(g, cfg, library, operator, np):
    c = np.zeros((5, 2, cfg.nmax+1), dtype=complex)
    for unused_left, unused_right, sl in chunks(cfg, library):
        c += 1j*np.matmul(operator['weighted_kappa'][:, :, sl]*g[:, :, sl], operator['r'][sl])/operator['norms'][None, None, :]
    return c


def envelope(t, cfg):
    if t <= 0 or t >= cfg.duration: return 0., 0.
    if t < cfg.rise: u, sign, scale = t/cfg.rise, 1., cfg.rise
    elif t > cfg.duration-cfg.fall: u, sign, scale = (cfg.duration-t)/cfg.fall, -1., cfg.fall
    else: return cfg.shape, 0.
    return cfg.shape*u**3*(10-15*u+6*u*u), sign*cfg.shape*30*u*u*(1-u)**2/scale


def external(t, cfg, np):
    amplitude, rate = envelope(t, cfg); unit = np.zeros((2, cfg.nmax+1), dtype=complex)
    scalar, angle = 3*BAR_MASS/(7*math.sqrt(30)), cfg.theta0+cfg.omega*t
    unit[0, 0], unit[1, 0] = scalar*np.exp(2j*angle), scalar*np.exp(-2j*angle)
    return amplitude*unit, rate*unit, unit


def full_coefficients(c, np):
    full = np.zeros((5, 5, c.shape[-1]), dtype=complex); full[:, 0, :], full[:, 4, :] = c[:, 0, :], c[:, 1, :]
    return full


def budget_values(g, c, cfg, library, operator, np):
    q, j = np.zeros(5), np.zeros(5); m = np.asarray(M_VALUES)[None, :, None]
    for unused_left, unused_right, sl in chunks(cfg, library):
        weighted = operator['weighted_kappa'][:, :, sl]*np.abs(g[:, :, sl])**2
        q -= .5*np.sum(weighted*operator['nu'][None, None, sl], axis=(1, 2)); j -= .5*np.sum(weighted*m, axis=(1, 2))
    field = .5*np.sum(operator['norms'][None, None, :]*np.abs(c)**2, axis=(1, 2))
    return q, j, field, cfg.self_gravity*field


def reality_errors(g, c, cfg, library, np):
    a, n, k, unused_b = library['radial'].shape; lattice = g.reshape(5, 2, a, n, k); modal = 0.
    for left in range(0, a, cfg.chunk_actions):
        block = lattice[:, :, left:left+cfg.chunk_actions]
        modal = max(modal, float(np.max(np.abs(block[:, ::-1, :, ::-1, ::-1]-block.conj()))))
    return modal, float(np.max(np.abs(c[:, ::-1]-c.conj())))


def step(g, c, t, cfg, library, operator, np, budget):
    bmid, rate, unused_unit = external(t+cfg.dt/2, cfg, np)
    new_g = operator['drift'][None, None, :]*g
    rhs = project(new_g, cfg, library, operator, np)
    rhs += np.einsum('pmbc,mc->pmb', operator['kernel'], bmid, optimize=True)
    rhs += .5*cfg.self_gravity*np.einsum('pmbc,pmc->pmb', operator['kernel'], c, optimize=True)
    solve = np.einsum('pmbc,pmc->pmb', operator['inverse'], rhs, optimize=True)
    total = bmid[None, :, :]+.5*cfg.self_gravity*(c+solve)
    for unused_left, unused_right, sl in chunks(cfg, library):
        budget.check(); new_g[:, :, sl] += operator['force'][None, None, sl]*np.matmul(total, operator['r'][sl].T)
        if not np.all(np.isfinite(new_g[:, :, sl])): raise FloatingPointError('Nonfinite retained generator; prior checkpoint preserved')
    fresh = project(new_g, cfg, library, operator, np); midpoint, norm = (c+fresh)/2, operator['norms'][None, None, :]
    ds = cfg.dt*np.real(np.sum(norm*midpoint.conj()*rate[None, :, :], axis=(1, 2)))
    torque = -1j*np.asarray(M_VALUES)[:, None]*bmid
    dj = cfg.dt*np.real(np.sum(norm*midpoint.conj()*torque[None, :, :], axis=(1, 2)))
    before, after = external(t, cfg, np)[0], external(t+cfg.dt, cfg, np)[0]
    dw = np.real(np.sum(norm*(midpoint.conj()*(after-before)[None, :, :]+
        (fresh-c).conj()*((before+after)/2-bmid)[None, :, :]), axis=(1, 2)))
    if not all(np.all(np.isfinite(x)) for x in (fresh, ds, dj, dw)): raise FloatingPointError('Nonfinite field or physical/discrete register')
    return new_g, fresh, ds, dj, dw, float(np.max(np.abs(fresh-solve)))


def measurements(g, c, t, cfg, library, operator, np, initial, shape, impulse, discrete):
    q, j, field, included = budget_values(g, c, cfg, library, operator, np)
    b = external(t, cfg, np)[0]
    interaction = np.real(np.sum(operator['norms'][None, None, :]*c.conj()*b[None, :, :], axis=(1, 2)))
    total, angular = q+included-initial[0]-initial[3], j-initial[1]
    full, reality = full_coefficients(c, np), reality_errors(g, c, cfg, library, np)
    if not all(np.all(np.isfinite(x)) for x in (q, j, field, included, interaction, shape, impulse, discrete, full, reality)):
        raise FloatingPointError('Nonfinite raw recorded canonical ledger')
    return dict(canonical_orbit_energy2=q.tolist(), canonical_impulse2=j.tolist(), projected_field_energy2=field.tolist(),
        included_field_energy2=included.tolist(), canonical_energy2_change=total.tolist(), canonical_impulse2_change=angular.tolist(),
        external_interaction_energy2=interaction.tolist(), shape_work2=shape.tolist(), angular_impulse2=impulse.tolist(),
        total_external_work2=(shape+cfg.omega*impulse).tolist(), discrete_external_flux2=discrete.tolist(),
        physical_energy_budget_residual=(total+interaction-shape-cfg.omega*impulse).tolist(),
        discrete_energy_budget_residual=(total+interaction-discrete).tolist(), impulse_budget_residual=(angular-impulse).tolist(),
        self_torque2=np.real(np.sum(operator['norms'][None, None, :]*c.conj()*
            (-1j*np.asarray(M_VALUES)[None, :, None])*cfg.self_gravity*c, axis=(1, 2))).tolist(),
        generator_reality_error=reality[0], coefficient_reality_error=reality[1],
        coefficients_real=full.real.tolist(), coefficients_imag=full.imag.tolist(),
        F0_l2_energy_bound_gap=float((q+included-3*q/8)[0]),
        F0_l2_energy_bound_scope='Continuum F_e-positive F0 benchmark only; no mixed-DF/discrete qualification')


def formula_fixture(cfg, np, quad, bare):
    old = bare.formula_fixture(cfg, np, quad)
    nodes, weights = bare.rule(128, np); t, wt = (nodes+1)*math.pi/2, weights*math.pi/2
    s = np.tan(t/2); w, chi = 1+s*s, (s*s-1)/(s*s+1)
    polys = [np.ones_like(s)]
    if cfg.nmax: polys.append(6*chi)
    for n in range(1, cfg.nmax): polys.append((2*(n+3)*chi*polys[-1]-(n+5)*polys[-2])/(n+1))
    phi = np.column_stack([-s*s*w**(-2.5)*p for p in polys])
    rho = np.column_stack([s*s*w**(-4.5)*p*(n+2.5)*(n+3.5)/math.pi for n, p in enumerate(polys)])
    volume = wt*s*s*(1+s*s)/2
    product = 4*math.pi*phi.T@(rho*volume[:, None]); norms = np.asarray([negative_norm(n) for n in range(cfg.nmax+1)])
    norm_error = float(np.max(np.abs(product-np.diag(norms))/np.sqrt(np.outer(-norms, -norms))))
    radii = np.asarray((.03, .3, 1.7, 9.)); h = 1e-5
    def values(r):
        u = 1/np.sqrt(1+r*r); return radial_values(u, r*r*u*u/(1+u), cfg.nmax, np)
    f, fr = values(radii); numerical = (values(radii+h)[0]-values(radii-h)[0])/(2*h)
    derivative_error = float(np.max(np.abs(fr-numerical)/np.maximum(1., np.abs(fr))))
    if not math.isfinite(norm_error) or not math.isfinite(derivative_error): raise FloatingPointError('Nonfinite formula control')
    return dict(passed=bool(old['passed'] and norm_error <= 3e-11 and derivative_error <= 2e-7),
        existing_bare_formula_controls=old, negative_physical_CB_norm_relative_error=norm_error, CB_norm_tolerance=3e-11,
        radial_derivative_scaled_error=derivative_error, radial_derivative_tolerance=2e-7,
        scope='Finite angular/window/bar/DF derivative/radial/Poisson norm controls; no response or positivity qualification')


def calculate(cfg, np, brentq, budget, bare, outputs, pins, versions, save_library=False, save_generator=False):
    library = build_library(cfg, np, brentq, budget, bare); maps = bare.population_maps()
    operator = build_operator(cfg, library, maps, np, budget, bare)
    if save_library: outputs.npz('orbit_library.npz', np, **{key: value for key, value in library.items() if key != 'construction_CPU_seconds'})
    g = np.zeros(operator['weighted_kappa'].shape, dtype=complex); c = project(g, cfg, library, operator, np)
    initial = budget_values(g, c, cfg, library, operator, np); initial_c = full_coefficients(c, np)
    zero_cfg = replace(cfg, shape=0.)
    zg, zc, zs, zj, zw, ze = step(g, c, 0., zero_cfg, library, operator, np, budget)
    zero_error = max(float(np.max(np.abs(x))) for x in (zg, zc, zs, zj, zw))
    if zero_error != 0 or ze != 0: raise ArithmeticError('Actual zero-drive/zero-seed operator control failed')
    del zg, zc
    shape, impulse, discrete = np.zeros(5), np.zeros(5), np.zeros(5)
    history, completed, max_solve = [], 0, 0.; evolution_started = time.process_time(); last_checkpoint = time.monotonic()
    def record():
        row = measurements(g, c, completed*cfg.dt, cfg, library, operator, np, initial, shape, impulse, discrete)
        row.update(step=completed, time=completed*cfg.dt, maximum_field_solve_residual=max_solve); history.append(row)
    def checkpoint():
        data = dict(density_coefficients=full_coefficients(c, np), initial_density_coefficients=initial_c,
            initial_budget=np.stack(initial), shape_work2=shape, angular_impulse2=impulse, discrete_external_flux2=discrete,
            metadata=np.asarray(json.dumps(dict(step=completed, time=completed*cfg.dt, history=history, config=asdict(cfg),
                populations=list(POPS), source_sha256=pins, method_ancestors_sha256=ANCESTORS,
                versions=versions,
                physical_coefficients={name: dict(zip(map(str, bare.POWERS), cs)) for name, cs in maps.items()},
                coefficient_order=dict(radial_n=list(range(cfg.nmax+1)), complex_m=[-2, -1, 0, 1, 2], l=2),
                completed_step_state=True, resume_supported=False), allow_nan=False)))
        if save_generator: data['generator'] = g
        outputs.npz('checkpoint.npz', np, **data)
    record(); checkpoint()
    for index in range(round(cfg.duration/cfg.dt)):
        budget.check(); g, c, ds, dj, dw, error = step(g, c, index*cfg.dt, cfg, library, operator, np, budget)
        completed = index+1; shape += ds; impulse += dj; discrete += dw; max_solve = max(max_solve, error)
        if completed % cfg.record_every == 0 or completed == round(cfg.duration/cfg.dt): record()
        if time.monotonic()-last_checkpoint >= cfg.checkpoint_seconds:
            if history[-1]['step'] != completed: record()
            checkpoint(); last_checkpoint = time.monotonic()
    if history[-1]['step'] != completed: record()
    checkpoint(); budget.check()
    return dict(physical_endpoint_complete=completed == round(cfg.duration/cfg.dt), response_calculated=True,
        step=completed, final_time=completed*cfg.dt, history=history, initial=history[0], final=history[-1],
        initial_absolute_budget=dict(canonical_orbit_energy2=initial[0].tolist(), canonical_impulse2=initial[1].tolist(),
            projected_field_energy2=initial[2].tolist(), included_field_energy2=initial[3].tolist()),
        initial_coefficients_real=initial_c.real.tolist(), initial_coefficients_imag=initial_c.imag.tolist(),
        forced_m=list(M_VALUES), implicit_zero_m=[-1, 0, 1],
        coefficient_order=dict(radial_n=list(range(cfg.nmax+1)), complex_m=[-2, -1, 0, 1, 2], l=2),
        physical_mass_totals=operator['physical_mass_totals'], expected_halo_mass=.9, midpoint_field_condition_numbers=operator['condition'].tolist(),
        zero_drive_zero_seed_max_absolute=zero_error, empirical_mass_normalization=False, independent_iid_families=0,
        orbital_quadrature=dict(retained_nodes=cfg.ne*cfg.neta, maximum_order=int(np.max(library['order'])),
            maximum_errors=np.max(library['quadrature_errors'], axis=0).tolist(),
            error_order=['frequency_and_action_relative', 'radial_coefficients_over_value_norm', 'Parseval_norm_relative', 'phase_radians'],
            maximum_phase_panel_order=int(np.max(library['phase_panel_order'])), maximum_phase_panel_errors=np.max(library['phase_panel_errors'], axis=0).tolist(),
            phase_panel_error_order=['cumulative_difference', 'summed_local_difference', 'halfperiod_consistency', 'maximum_local_dimensionless_difference'],
            maximum_pole_reconstruction_error=float(np.max(library['pole_reconstruction_error'])),
            minimum_binding=float(np.min(library['e'])), maximum_binding=float(np.max(library['e'])),
            minimum_circularity=float(np.min(library['eta'])), maximum_circularity=float(np.max(library['eta'])),
            full_domain='0<e<1,0<eta<1,-1<mu<1; no cutoff/rejected/deleted node',
            weighted_value_tail_proxy=np.einsum('a,akb->kb', library['weight'], library['value_tail_proxy']).tolist(),
            weighted_derivative_tail_proxy=np.einsum('a,akb->kb', library['weight'], library['derivative_tail_proxy']).tolist(),
            scope='Orbit/Parseval numerical proxies; no rigorous continuum response-error bound'),
        memory=dict(real_weighted_kappa_bytes=operator['weighted_kappa'].nbytes, generator_bytes=g.nbytes,
            transactional_step_extra_generator_bytes=g.nbytes, radial_bytes=operator['r'].nbytes, scope='Named arrays, not peak RSS'),
        pricing=dict(orbit_construction_CPU_seconds=library['construction_CPU_seconds'], operator_construction_CPU_seconds=operator['construction_CPU_seconds'],
            evolution_diagnostics_checkpoint_CPU_seconds=time.process_time()-evolution_started),
        saved_orbit_library=save_library, saved_generator=save_generator, resume_supported=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--preset', choices=('quick', 'reference'), default='quick')
    defaults = Config()
    for name, value in asdict(defaults).items(): parser.add_argument('--'+name.replace('_', '-'), type=type(value))
    parser.add_argument('--check-formulas', action='store_true')
    parser.add_argument('--save-library', action='store_true'); parser.add_argument('--save-generator', action='store_true')
    parser.add_argument('--output', required=True, help='Create a new directory; no existing output directory is overwritten')
    args = parser.parse_args(); values = {name: value for name, value in vars(args).items() if name in asdict(defaults) and value is not None}
    profile = Config(ne=64, neta=64, radial_modes=32, dt=.01) if args.preset == 'reference' else defaults
    cfg = Config(**(asdict(profile) | values)); cfg.validate()
    entries = cfg.ne*cfg.neta*(2*cfg.radial_modes+1)*3
    named_estimate = entries*(8*(cfg.nmax+1)+80+320+40)+512*1024**2
    if not args.check_formulas and named_estimate > .8*cfg.memory_mib*1024**2:
        parser.error('Named working arrays plus import allowance exceed memory envelope; select explicit smaller resolution or larger memory limit')
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        os.environ[name] = '1'
    started = time.process_time(); pins = provenance(); bare = load_bare(); budget = Budget(cfg)
    outputs = Outputs(args.output, cfg, budget)
    previous = {}; old_timer = None; timer_started = time.monotonic()
    def interrupted(unused_signal, unused_frame): raise InterruptedError('Process signal/timeout; prior checkpoint remains incomplete evidence')
    for name in ('SIGTERM', 'SIGINT', 'SIGXCPU', 'SIGALRM'):
        if hasattr(signal, name):
            value = getattr(signal, name); previous[value] = signal.signal(value, interrupted)
    if hasattr(signal, 'setitimer') and hasattr(signal, 'ITIMER_REAL'):
        old_timer = signal.getitimer(signal.ITIMER_REAL)
        interval = min(cfg.wall_seconds, old_timer[0]) if old_timer[0] > 0 else cfg.wall_seconds
        signal.setitimer(signal.ITIMER_REAL, interval); budget.limits['wall'] = dict(real_time_alarm_seconds=interval, cooperative_seconds=cfg.wall_seconds)
    result = dict(schema='collective-plummer-complete-cycle-public-v1', complete=False, physical_endpoint_complete=False,
        response_calculated=False, fixture_only=bool(args.check_formulas), config=asdict(cfg), preset=args.preset,
        save_orbit_library_requested=bool(args.save_library), save_generator_requested=bool(args.save_generator),
        source_sha256=pins, method_ancestors_sha256=ANCESTORS,
        dependency=dict(companion='bare_run.py', sha256=BARE_SHA, isolated_named_module=True, dependency_patched=False),
        populations=list(POPS), physical_coefficients={name: dict(zip(map(str, bare.POWERS), cs)) for name, cs in bare.population_maps().items()},
        physical_reference=dict(G=1, total_mass=1, radius=1, bar_mass='1/10', halo_Q='14/33', background='total Plummer with anchored physical bar monopole'),
        process_limits=budget.limits, action_measure='(2pi)^3 Lc² eta/omega_r de deta dmu; unnormalized mu in [-1,1]',
        units=dict(energy2='G M²/a; actual declared shape amplitude included', impulse2='M sqrt(G M a); actual declared shape amplitude included'),
        positivity_certificate=dict(verified_by_this_run=False, scope='Immutable original bare bundle supplies the separate background matching/positivity proof; no perturbed-DF proof'),
        continuum_response_qualified=False, stability_qualified=False, independent_algorithm=False,
        scope='Same central l2 canonical linear-response method port; own DF fields and prescribed cyclic rotor angle, no autonomous rotor or global stability claim')
    try:
        import numpy as np
        import scipy
        from scipy.optimize import brentq
        from scipy.integrate import quad
        result['versions'] = dict(python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__)
        result['formula_fixture'] = formula_fixture(cfg, np, quad, bare)
        if not result['formula_fixture']['passed']: raise ArithmeticError('Portable formula controls failed')
        if not args.check_formulas: result.update(calculate(cfg, np, brentq, budget, bare, outputs, pins, result['versions'], args.save_library, args.save_generator))
        budget.check()
        if provenance() != pins: raise RuntimeError('Local source/document operand changed during calculation')
        result['complete'] = bool(args.check_formulas or result['physical_endpoint_complete'])
        result['fixture_only'] = bool(args.check_formulas)
    except (Exception, KeyboardInterrupt) as failure:
        result['complete'] = False; result['physical_endpoint_complete'] = False
        result['error'] = type(failure).__name__+': '+str(failure)
    try:
        result['process_CPU_seconds'] = time.process_time()-started
        result['process_wall_seconds'] = time.monotonic()-budget.wall0
        outputs.json('result.json', result)
        print(json.dumps(dict(complete=result['complete'], physical_endpoint_complete=result['physical_endpoint_complete'],
            response_calculated=result['response_calculated'], stability_qualified=False)), flush=True)
    finally:
        if old_timer is not None: signal.setitimer(signal.ITIMER_REAL, 0.)
        for value, handler in previous.items(): signal.signal(value, handler)
        if old_timer is not None and old_timer[0] > 0:
            remaining = old_timer[0]-(time.monotonic()-timer_started)
            if remaining > 0: signal.setitimer(signal.ITIMER_REAL, remaining, old_timer[1])
        outputs.close()
    return 0 if result['complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
