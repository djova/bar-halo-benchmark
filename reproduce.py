"""Regenerate numerical controls and a published initial-Maxwell moment result.

All inputs are generated here. Run from any directory; no project imports.
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('MPLBACKEND', 'Agg')
import argparse
import hashlib
import json
from pathlib import Path
import platform
import time
import numpy as np

LAGS = (1., 2., 4.)
WINDOWS = ((0., 10.), (10., 20.), (20., 32.))


def pooled_rows(x, t):
    """Same ddof=0 pooling and window convention as the historical screen."""
    rows = []
    for lo, hi in WINDOWS:
        for lag in LAGS:
            start = np.flatnonzero((t >= lo-1e-9) & (t < hi-1e-9)
                                   & (t+lag <= t[-1]+1e-9))
            inc = x[start+round(lag/(t[1]-t[0]))]-x[start]
            mean = float(inc.mean())
            rate = float(np.mean((inc-mean)**2)/(2*lag))
            rows.append(dict(window=[lo, hi], lag=lag, mean_increment=mean,
                             variance_rate=rate, starts=len(start),
                             exact=expected_rate(lo, hi, lag, t)))
    return rows


def expected_rate(lo, hi, lag, t):
    gamma, mu, sigma = .25, .1, .3
    starts = t[(t >= lo-1e-9) & (t < hi-1e-9) & (t+lag <= t[-1]+1e-9)]
    m = np.exp(mu*starts)*np.expm1(mu*lag)
    r2 = np.exp((2*mu+sigma*sigma)*starts)*(np.expm1((2*mu+sigma*sigma)*lag)
                                                        -2*np.expm1(mu*lag))
    return {'brownian': 1., 'ou': float(-np.expm1(-gamma*lag)/(gamma*lag)),
            'geometric': float((r2.mean()-m.mean()**2)/(2*lag))}


def spread(values):
    v = np.asarray(values)
    return float(np.ptp(v)/np.mean(v))


def controls():
    dt, n = .05, 4096
    t = np.arange(801)*dt
    batches = []
    for seed in range(8101, 8105):
        for index, model in enumerate(('brownian', 'ou', 'geometric')):
            rng = np.random.default_rng(np.random.SeedSequence([seed, index]))
            x = np.empty((len(t), n))
            x[0] = rng.normal(0, 2, n) if model == 'ou' else (1 if model == 'geometric' else 0)
            for i in range(1, len(t)):
                z = rng.normal(size=n)
                if model == 'brownian': x[i] = x[i-1]+np.sqrt(2*dt)*z
                elif model == 'ou':
                    x[i] = np.exp(-.25*dt)*x[i-1]+np.sqrt(-np.expm1(-.5*dt)/.25)*z
                else: x[i] = x[i-1]*np.exp((.1-.3**2/2)*dt+.3*np.sqrt(dt)*z)
            rows = pooled_rows(x, t)
            record = dict(seed=seed, model=model, rows=rows,
                          flatness_spread=spread([r['variance_rate'] for r in rows]),
                          true_diffusion='0.045 J^2' if model == 'geometric' else 1.)
            record['flatness_pass'] = record['flatness_spread'] < .2
            if model == 'ou':
                # Fit only starts in first window at lag one; no future fitting.
                a, b = x[:200].ravel(), x[20:220].ravel()
                rho = float(a@b/(a@a))
                gamma = float(-np.log(rho))
                residual = b-rho*a
                D = float(np.mean(residual**2)*gamma/(1-rho*rho))
                record['first_window_fit'] = dict(gamma=gamma, D=D, rho=rho,
                    future_stationary_variance_rate=[D*(-np.expm1(-gamma*lag))/(gamma*lag) for lag in LAGS])
            batches.append(record)
    summaries = []
    for model in ('brownian', 'ou', 'geometric'):
        chosen = [b for b in batches if b['model'] == model]
        values = np.array([[r['variance_rate'] for r in b['rows']] for b in chosen])
        truth = np.array([r['exact'][model] for r in chosen[0]['rows']])
        summaries.append(dict(model=model, mean=values.mean(0).tolist(),
            batch_se=(values.std(0, ddof=1)/2).tolist(), exact=truth.tolist(),
            exact_flatness_spread=spread(truth),
            max_relative_mean_error=float(np.max(abs(values.mean(0)/truth-1)))))
    # Independent one-step geometric-transition test avoids long-path tail growth.
    rng = np.random.default_rng(8105)
    z = rng.normal(size=1048576)
    y = np.exp((.1-.3**2/2)*2+.3*np.sqrt(2)*z)-1
    truth = np.array([np.expm1(.2), np.exp((.2+.09)*2)-2*np.exp(.2)+1])
    vals = np.column_stack((y, y*y))
    mean, se = vals.mean(0), vals.std(0, ddof=1)/np.sqrt(len(y))
    # Exact total-variance decomposition, checked on a deterministic finite sample.
    v = np.array([[1., 2., 3.], [4., 5., 6.]])
    total_variance_error = abs(float(v.var()-np.mean(v.var(axis=1))-np.var(v.mean(axis=1))))
    gates = dict(total_variance_identity=total_variance_error < 1e-12,
                 brownian_accuracy=summaries[0]['max_relative_mean_error'] < .05,
                 ou_accuracy=summaries[1]['max_relative_mean_error'] < .05,
                 brownian_flatness=all(b['flatness_pass'] for b in batches if b['model']=='brownian'),
                 constant_diffusion_ou_fails_flatness=all(not b['flatness_pass'] for b in batches if b['model']=='ou'),
                 geometric_transition_five_se=bool(np.all(abs(mean-truth) < 5*se)))
    return dict(config=dict(paths_per_batch=n, dt=dt, end=40., seeds=list(range(8101,8105)),
                            lags=LAGS, windows=WINDOWS, gamma=.25, D=1., mu=.1, sigma=.3),
                batches=batches, summaries=summaries, gates=gates, all_pass=all(gates.values()),
                geometric_transition=dict(mean=mean.tolist(), se=se.tolist(), exact=truth.tolist()),
                scope='Known Markov controls. OU has constant diffusion despite non-flat finite-lag variance rate. No model is inferred for the halo from this counterexample.')


def maxwell():
    """Same seeds and exact moment definitions as the archived Maxwell check."""
    blocks, algebra, arrays = [], [], []
    for seed in range(7141, 7145):
        rng = np.random.default_rng(seed)
        v, bath = rng.normal(size=(262144, 3)), rng.normal(size=(262144, 3))
        u, V = v-bath, (v+bath)/2
        v2, u2, V2 = [(a*a).sum(1) for a in (v,u,V)]
        vu = (v*u).sum(1)
        rate = .2*np.sqrt(u2)
        A = -rate[:,None]*u/2
        B = rate[:,None,None]*(u2[:,None,None]*np.eye(3)/3+u[:,:,None]*u[:,None,:])/4
        hessian = 8*v[:,:,None]*v[:,None,:]+4*v2[:,None,None]*np.eye(3)
        gaussian = (A*(4*v2[:,None]*v)).sum(1)+.5*np.einsum('nij,nij->n',B,hessian)
        simple = rate*(-2*v2*vu+4*v2*u2/3+vu*vu)
        second = 2*(A*v).sum(1)+np.trace(B,axis1=1,axis2=2)
        exact = rate*((V2+u2/4)**2+u2*V2/3-v2*v2)
        angular, angular2 = np.zeros(len(v)), np.zeros(len(v))
        for axis in range(3):
            for sign in (-1,1):
                after = V.copy(); after[:,axis] += sign*np.sqrt(u2)/2
                r2 = (after*after).sum(1)
                angular += (r2*r2-v2*v2)/6
                angular2 += (r2-v2)/6
        angular *= rate; angular2 *= rate
        relative = lambda x,y: float(np.linalg.norm(x-y)/max(np.linalg.norm(y),1e-15))
        algebra.append(dict(gaussian=relative(gaussian,simple), jump=relative(angular,exact), second=relative(second,angular2)))
        values = np.column_stack((rate,gaussian,exact,second,angular2))
        blocks.append(dict(seed=seed, mean=values.mean(0).tolist(), se=(values.std(0,ddof=1)/np.sqrt(len(values))).tolist()))
        arrays.append(values)
    values = np.concatenate(arrays)
    mean, se = values.mean(0), values.std(0,ddof=1)/np.sqrt(len(values))
    expected = np.array([.8/np.sqrt(np.pi),25.6/np.sqrt(np.pi),0,0,0])
    reference = json.loads(Path(__file__).with_name('reference-maxwell.json').read_text())
    reproduction_error = float(np.max(abs(mean-np.asarray(reference['pooled_mean']))))
    gates = dict(algebra=max(v for row in algebra for v in row.values()) < 1e-12,
                 analytical_five_se=bool(np.all(abs(mean-expected)<5*se)),
                 precision=bool(np.all(se<.02*expected[1])),
                 reproduces_archived_mean=reproduction_error<1e-10)
    return dict(columns=reference['columns'], pooled_mean=mean.tolist(), pooled_se=se.tolist(),
                analytical=expected.tolist(), blocks=blocks, algebra=algebra, gates=gates,
                all_pass=all(gates.values()), reproduction_error=reproduction_error,
                n_total=len(values), rho=1., cross_section_per_mass=.2, sigma_1d=1.,
                scope='Verification of a known finite-jump limitation at initial Maxwell equilibrium, not a time-evolved halo or a novel SIDM prediction.')


def figures(result, out):
    import matplotlib
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':11, 'axes.spines.top':False,'axes.spines.right':False})
    fig, ax = plt.subplots(1,2,figsize=(10,4.4),layout='constrained')
    for s,c in zip(result['finite_lag']['summaries'][:2],('#306d98','#b65b28')):
        ax[0].plot(LAGS,s['exact'][:3],color=c,label=s['model'].upper()+' exact')
        ax[0].errorbar(LAGS,s['mean'][:3],yerr=np.array(s['batch_se'][:3])*3.182446,fmt='o',color=c,capsize=4)
    ax[0].set(xlabel='Increment duration',ylabel='Pooled variance / (2 duration)',ylim=(.45,1.12),
              title='Both processes have constant D = 1')
    ax[0].legend(fontsize=9)
    models=result['finite_lag']['summaries'][:2]
    ax[1].bar(['Brownian','Restoring drift'],[100*s['exact_flatness_spread'] for s in models],color=['#306d98','#b65b28'])
    ax[1].axhline(20,color='#555',ls='--',label='Old flatness cutoff: 20%')
    ax[1].set(ylabel='Exact relative spread (%)',ylim=(0,40),title='Flatness is not a constant-D test')
    ax[1].legend(fontsize=9)
    fig.suptitle('Known-limit verification · points: four independent batches · bars: nominal 95% t₃ intervals')
    fig.savefig(out/'finite-lag-controls.png',dpi=170);plt.close(fig)
    m=result['maxwell'];fig,ax=plt.subplots(figsize=(7,4.4),layout='constrained')
    ax.errorbar([0,1],m['pooled_mean'][1:3],yerr=np.array(m['pooled_se'][1:3])*1.96,fmt='o',capsize=5,label='Regenerated Monte Carlo, 95% intervals')
    ax.scatter([0,1],m['analytical'][1:3],marker='_',s=400,color='#b65b28',label='Analytical derivative')
    ax.set(xticks=[0,1],xticklabels=['Gaussian truncation','Exact elastic jumps'],ylabel='Initial derivative of ⟨|v|⁴⟩',title='The same first two jump moments do not fix the fourth')
    ax.legend(fontsize=9);fig.savefig(out/'maxwell-generators.png',dpi=170);plt.close(fig)
    return matplotlib.__version__


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    start,cpu=time.monotonic(),time.process_time()
    result=dict(finite_lag=controls(),maxwell=maxwell())
    version=figures(result,a.out)
    result.update(all_pass=result['finite_lag']['all_pass'] and result['maxwell']['all_pass'],
        versions=dict(python=platform.python_version(),numpy=np.__version__,matplotlib=version),
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.iterdir() if p.is_file()})
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(all_pass=result['all_pass'],cpu_seconds=result['cpu_seconds'],
        control_gates=result['finite_lag']['gates'],maxwell_gates=result['maxwell']['gates']),indent=2))
    if not result['all_pass']:raise SystemExit(1)


if __name__=='__main__':main()
