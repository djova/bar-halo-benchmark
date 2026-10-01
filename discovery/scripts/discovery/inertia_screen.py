"""Self-consistent discrete-frequency benchmarks for Milgrom 2022 Eq. (32).

This solves complete harmonic histories, not Newtonian trajectories with an
acceleration correction. Amplitudes are RMS amplitudes, as in that paper.
"""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
from pathlib import Path
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
import numpy as np
from scipy.optimize import brentq, least_squares

ROOT = Path(__file__).resolve().parents[2]


def theta(y, q):
    return 2 / (1 + np.abs(y) ** q)


def mu(x):
    """Explicit chosen interpolation; not an observationally fitted function."""
    return x / (1 + x)


def acceleration_measure(w, rms, q):
    return theta(w[None, :] / w[:, None], q) @ (w*w*rms)


def solve_harmonic(wn, rms, q, a0=1., guess=None):
    wn, rms = np.asarray(wn, float), np.asarray(rms, float)
    if np.any(wn <= 0) or np.any(rms <= 0):
        raise ValueError('Positive frequencies and RMS amplitudes required')
    def residual(logw):
        w = np.exp(logw)
        return np.log(w*w*mu(acceleration_measure(w, rms, q)/a0) / (wn*wn))
    start = wn if guess is None else guess
    answer = least_squares(residual, np.log(start), xtol=1e-13, ftol=1e-13,
                           gtol=1e-13, max_nfev=2000)
    w = np.exp(answer.x)
    return w, float(np.max(np.abs(residual(answer.x)))), answer.nfev


def single_frequency(wn, rms, a0):
    # y=omega^2, mu(y*r/a0)=y*r/(a0+y*r): quadratic.
    k = wn*wn
    return np.sqrt(.5*(k + np.sqrt(k*k + 4*k*a0/rms)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True)
    args = p.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    started, cpu = time.monotonic(), time.process_time()
    started_utc = datetime.now(timezone.utc).isoformat()
    rows, checks = [], {}
    qs = (2, 4, 8)
    # All values frozen in INERTIA_PROTOCOL.md before execution.
    for q in qs:
        y = np.logspace(-6, 6, 1025)
        checks[f'filter_{q}'] = dict(even_error=float(np.max(abs(theta(y, q)-theta(-y,q)))),
            normalization=float(theta(1,q)), low_frequency_limit=float(theta(0,q)),
            minimum=float(np.min(theta(y,q))), sampled_nondecreasing_violations=int(np.count_nonzero(np.diff(theta(y,q))>0)),
            analytic_derivative_negative_for_positive_y=bool(q>0),
            high_frequency_weight=float(theta(1e6,q)))
        for a0 in (1e-8, 1., 1e8):
            w, error, _ = solve_harmonic([.7], [.8], q, a0)
            exact = single_frequency(.7, .8, a0)
            rows.append(dict(kind='single_frequency', q=q, a0=a0, wn=[.7], rms=[.8],
                             w=w.tolist(), relative_analytic_error=float(abs(w[0]/exact-1)), residual=error))
        for amp_ratio in (.03, .1, .3, 1., 3., 10., 30.):
            for wn_ratio in (.25, .5, .9, 1.1, 2., 4.):
                wn=np.array([1.,wn_ratio]);rms=np.array([.15,.15*amp_ratio])
                solutions=[]
                for factor in (.3,1.,3.):
                    w,error,nfev=solve_harmonic(wn,rms,q,guess=wn*factor)
                    solutions.append(w)
                spread=float(np.max(np.ptp(np.asarray(solutions),axis=0)/solutions[1]))
                w=solutions[1];A=acceleration_measure(w,rms,q);m=mu(A)
                t=np.linspace(0,100,4097)
                x=np.sqrt(2)*rms[:,None]*np.cos(w[:,None]*t+.37)
                v=-np.sqrt(2)*rms[:,None]*w[:,None]*np.sin(w[:,None]*t+.37)
                force=-wn[:,None]**2*x
                # For orthogonal separable harmonic modes the nonlocal energy
                # reduces to this explicit positive expression on the solution.
                energy=.5*np.sum(m[:,None]*v*v+wn[:,None]**2*x*x,axis=0)
                momentum_derivative=-m[:,None]*w[:,None]**2*x
                rows.append(dict(kind='two_axis',q=q,a0=1.,wn=wn.tolist(),rms=rms.tolist(),w=w.tolist(),
                    acceleration_measure=A.tolist(),mu=m.tolist(),residual=error,guess_spread=spread,
                    force_relative_residual=float(np.max(abs(force-momentum_derivative))/np.max(abs(force))),
                    modified_energy_relative_drift=float(np.ptp(energy)/np.mean(energy))))
    # Model dependence survives a shared circular calibration. This is a
    # prediction of the chosen harmonic reference model, not a galaxy fit.
    comparisons=[]
    for amp_ratio in (.03,.1,.3,1.,3.,10.,30.):
        for wn_ratio in (.25,.5,.9,1.1,2.,4.):
            found=[r for r in rows if r['kind']=='two_axis' and r['rms'][1]==.15*amp_ratio and r['wn'][1]==wn_ratio]
            values=np.asarray([r['w'] for r in found])
            comparisons.append(dict(amplitude_ratio=amp_ratio,newtonian_frequency_ratio=wn_ratio,
                q=[r['q'] for r in found],w=values.tolist(),relative_range=((values.max(axis=0)-values.min(axis=0))/values[0]).tolist()))
    # Exact-frequency merger differs from the distinct-mode limiting expression.
    degenerate=[]
    for q in qs:
        w,error,_=solve_harmonic([1.,1.+1e-8],[.15,.15],q)
        merged=single_frequency(1.,np.sqrt(2)*.15,1.)
        degenerate.append(dict(q=q,distinct_frequency_limit=w.tolist(),merged_vector_rms=np.sqrt(2)*.15,
            exact_merged_frequency=float(merged),relative_discontinuity=float(w[0]/merged-1),residual=error))
    limits=[]
    # A hypothetical fast internal acceleration contaminates low-frequency
    # inertia by a_internal * Theta(omega_internal/omega_external).
    for q in qs:
        for ratio in (1e2,1e4,1e6):
            limits.append(dict(q=q,frequency_ratio=ratio,acceleration_ratio=1e12,
                               low_frequency_contamination_fraction=float(1e12*theta(ratio,q))))
    max_res=max(r['residual'] for r in rows)
    max_spread=max(r.get('guess_spread',0) for r in rows)
    gates=dict(frequency_equations=max_res<1e-10,multiple_guesses_agree=max_spread<1e-8,
               single_frequency_analytic=max(r.get('relative_analytic_error',0) for r in rows)<1e-10,
               harmonic_energy=max(r.get('modified_energy_relative_drift',0) for r in rows)<1e-10,
               filters=all(c['even_error']==0 and c['normalization']==1 and c['minimum']>0 and c['sampled_nondecreasing_violations']==0 and c['analytic_derivative_negative_for_positive_y'] for c in checks.values()))
    result=dict(model='Milgrom 2022 v3 Eq32 discrete distinct frequencies; mu=x/(1+x); Theta=2/(1+|y|^q)',
        benchmarks=rows,filter_checks=checks,model_comparisons=comparisons,degenerate_frequency_limit=degenerate,
        composite_decoupling=limits,gates=gates,all_benchmark_gates_pass=bool(all(gates.values())),
        pid=os.getpid(),state='complete',started_utc=started_utc,ended_utc=datetime.now(timezone.utc).isoformat(),
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-started,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        protocol_sha256=hashlib.sha256((ROOT/'research/discovery-20261001/INERTIA_PROTOCOL.md').read_bytes()).hexdigest(),
        scope='Exact finite distinct-frequency harmonic histories. No observational validation, uniqueness theorem, general galaxy evolution, relativistic or cosmological theory.')
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(gates=gates,max_residual=max_res,max_guess_spread=max_spread,
        largest_q_relative_range=max(max(r['relative_range']) for r in comparisons),degenerate=degenerate,cpu_seconds=result['cpu_seconds']),indent=2))


if __name__=='__main__':
    main()
