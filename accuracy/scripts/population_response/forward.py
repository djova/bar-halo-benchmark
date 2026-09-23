"""Finite-time forward equation with absolute population weights and budgets.

Same spectral split operator as the archived normalized benchmark, generalized
to several unnormalized positive populations. No coefficient is fit to a torque.
"""
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
from profiles import load_table, weights


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def evolve(initial_weights, s, eta, J, nphi=128, dtmax=.025, end=20., bar=True,
           return_final=False):
    w = np.asarray(initial_weights, dtype=float)
    if w.ndim != 2 or np.any(w < 0) or not np.all(np.isfinite(w)):
        raise ValueError('Expected nonnegative finite population-by-action weights')
    if J <= 0 or nphi < 4 or eta < 0 or end < 0 or dtmax <= 0:
        raise ValueError('Invalid solver geometry or time/noise parameter')
    populations, nj = w.shape
    steps = int(np.ceil(end/dtmax))
    dt = end/steps if steps else 0.
    dx, dp = 2*J/nj, 2*np.pi/nphi
    j = -J + (np.arange(nj)+.5)*dx
    psi = (np.arange(nphi)+.5)*dp
    f = np.broadcast_to(w[:, None, :]/(2*np.pi), (populations,nphi,nj)).copy()
    mass0 = w.sum(axis=1)*dx
    if np.any(mass0 <= 0):
        raise ValueError('Each population must have positive mass')
    moment0 = (w*j).sum(axis=1)*dx
    mean0 = moment0/mass0
    variance0 = (w*(j[None,:]-mean0[:,None])**2).sum(axis=1)*dx/mass0
    kpsi = np.fft.fftfreq(nphi, 1/nphi)[:, None]
    kj = (2*np.pi*np.fft.fftfreq(nj,dx))[None,:]
    angle = np.exp(1j*kpsi*j[None,:]*dt/2)
    force = -np.sin(psi)[:,None] if bar else np.zeros((nphi,1))
    velocity = force-s
    D = 2*eta/np.pi
    q = -1j*velocity*kj-D*kj**2
    action = np.exp(q*dt)
    integral = np.full_like(q,dt)
    np.divide(np.expm1(q*dt),q,out=integral,where=abs(q)>1e-14)
    face_kernel = (velocity-1j*D*kj)*np.exp(-1j*kj*dx/2)*integral/nj
    impulse = np.zeros(populations)
    boundary = np.zeros(populations)
    mass_error = np.zeros(populations)
    negative = np.zeros(populations)
    budget_error = np.zeros(populations)
    edge_fraction = np.zeros(populations)
    save = set(np.rint(np.linspace(0,steps,201)).astype(int))
    snapshots = set(np.rint(np.linspace(0,steps,5)).astype(int))
    if end >= 10:
        save.add(int(round(10/dt)))
    rows, densities, times = [], [], []
    ps, js = max(1,nphi//64), max(1,nj//768)
    edge = abs(j) > J-min(8., J/4)
    for step in range(steps+1):
        tau = step*dt
        if step in save:
            mass = f.sum(axis=(1,2))*dx*dp
            moment = (f*j).sum(axis=(1,2))*dx*dp
            mean = moment/mass
            variance = (f*(j[None,None,:]-mean[:,None,None])**2).sum(axis=(1,2))*dx*dp/mass
            torque = (f*force).sum(axis=(1,2))*dx*dp
            change = moment+s*tau*mass0-moment0
            residual = change-impulse-boundary
            mass_error = np.maximum(mass_error, abs(mass/mass0-1))
            negative = np.maximum(negative, -np.minimum(f,0).sum(axis=(1,2))*dx*dp/mass0)
            budget_error = np.maximum(budget_error, abs(residual)/mass0)
            edge_fraction = np.maximum(edge_fraction, abs(f[:,:,edge]).sum(axis=(1,2))*dx*dp/mass0)
            rows.append(dict(tau=tau,mass=mass.tolist(),bar_impulse=impulse.tolist(),
                             bar_torque=torque.tolist(),physical_first_moment_change=change.tolist(),
                             boundary_moment=boundary.tolist(),budget_residual=residual.tolist(),
                             physical_mean_change=(change/mass0).tolist(),variance=variance.tolist()))
        if step in snapshots:
            densities.append(f[:,::ps,::js].copy()); times.append(tau)
        if step == steps:
            break
        f = np.fft.ifft(np.fft.fft(f,axis=1)*angle,axis=1).real
        impulse += dt*(f*force).sum(axis=(1,2))*dx*dp
        spectrum = np.fft.fft(f,axis=2)
        boundary += -2*J*dp*np.sum(spectrum*face_kernel,axis=(1,2)).real
        f = np.fft.ifft(spectrum*action,axis=2).real
        f = np.fft.ifft(np.fft.fft(f,axis=1)*angle,axis=1).real
    gates = dict(mass=bool(np.max(mass_error)<1e-10),
                 positive_mass=bool(np.max(negative)<1e-10),
                 first_moment_budget=bool(np.max(budget_error)<1e-7))
    if not bar:
        gates.update(unforced_mean=bool(np.max(abs(np.array(rows[-1]['physical_mean_change'])))<1e-7),
                     unforced_variance=bool(np.max(abs(np.array(rows[-1]['variance'])-variance0-2*D*end))<1e-7),
                     unforced_bar_impulse=bool(np.max(abs(impulse))==0))
    result = dict(history=rows,initial_mass=mass0.tolist(),initial_mean=mean0.tolist(),
                  initial_variance=variance0.tolist(),maximum_mass_relative_error=mass_error.tolist(),
                  maximum_negative_mass_fraction=negative.tolist(),
                  maximum_budget_per_initial_mass=budget_error.tolist(),
                  maximum_edge_absolute_mass_fraction=edge_fraction.tolist(),gates=gates,
                  all_pass=all(gates.values()),dt=dt,steps=steps,
                  normalization='Absolute central-density weights; initial mass is never rescaled.')
    raw = dict(times=np.array(times),psi=psi[::ps],j=j[::js],density=np.array(densities),
               initial_j=j,initial_weights=w)
    if return_final:
        raw['final_density'] = f
    return result, raw


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--table',required=True,type=Path)
    p.add_argument('--s',required=True,type=float)
    p.add_argument('--eta',required=True,type=float)
    p.add_argument('--J',type=float,default=96.)
    p.add_argument('--nj',type=int,default=3072)
    p.add_argument('--nphi',type=int,default=128)
    p.add_argument('--dt',type=float,default=.025)
    p.add_argument('--end',type=float,default=20.)
    p.add_argument('--plateau',type=float,default=24.)
    p.add_argument('--cutoff',type=float,default=40.)
    p.add_argument('--no-bar',action='store_true')
    p.add_argument('--profiles',default='gaussian,halo,exponential,gaussian_untapered')
    a = p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    start,cpu = time.monotonic(),time.process_time()
    meta,table = load_table(a.table)
    names = a.profiles.split(',')
    j = -a.J+(np.arange(a.nj)+.5)*2*a.J/a.nj
    w = weights(j,names,meta,table,a.plateau,a.cutoff)
    result,raw = evolve(w,a.s,a.eta,a.J,a.nphi,a.dt,a.end,not a.no_bar)
    np.savez_compressed(a.out/'recorded.npz',**raw)
    result.update(profiles=names,config={k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items() if k not in ['out','table']},
                  mass_per_fast_action_area_factor=meta['mass_per_fast_action_area_factor'],
                  Lz_per_fast_action_area_factor=meta['Lz_per_fast_action_area_factor'],
                  table_sha256=sha(a.table/'halo-table.npz'),table_metadata_sha256=sha(a.table/'result.json'),
                  source_sha256={name:sha(Path(__file__).parent/name) for name in ['forward.py','profiles.py']},
                  raw_sha256=sha(a.out/'recorded.npz'),cpu_seconds=time.process_time()-cpu,
                  wall_seconds=time.monotonic()-start,
                  scope='Finite positive populations at fixed fast actions; prescribed local bar and noise. Numerical completion does not qualify the domain, taper or physical inference.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (a.out/'COMPLETE').write_text('Evolution complete; inspect local and comparison gates.\n')
    print(json.dumps({k:v for k,v in result.items() if k!='history'},indent=2))


if __name__ == '__main__':
    main()
