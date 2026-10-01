"""Readback of seed-level equivalence and response comparisons.

Four independent realization seeds are the uncertainty unit. No particles or
history samples are counted as independent replicate runs.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from scipy.stats import t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/discovery-20261001/scattering'
SEEDS=list(range(260101,260105))
LAWS=['iso','angle02','angle01']


def read(name):
    p=BASE/name/'result.json'
    r=json.loads(p.read_text())
    assert hashlib.sha256((p.parent/'states.npz').read_bytes()).hexdigest()==r['raw_sha256']
    return r


def interval(a):
    a=np.asarray(a)
    mean=np.mean(a,axis=0)
    se=np.std(a,axis=0,ddof=1)/np.sqrt(len(a))
    margin=t.ppf(.975,len(a)-1)*se
    return dict(mean=np.asarray(mean).tolist(),se=np.asarray(se).tolist(),low=np.asarray(mean-margin).tolist(),high=np.asarray(mean+margin).tolist())


def controls(prefix='controls'):
    label='control-analysis-01' if prefix=='controls' else 'limit-control-analysis-01' if prefix.startswith('limit') else 'transport-control-analysis-01'
    out=BASE/label;out.mkdir(exist_ok=False)
    groups=[];checks={};all_runs=[]
    laws=['iso','angle01','angle005'] if prefix.startswith('limit') else LAWS
    for law in laws:
        seeds=SEEDS if prefix=='controls' else list(range(260301,260305)) if prefix.startswith('limit') else list(range(260201,260205))
        runs=[read(f'{prefix}-equilibrium-{law}-{seed}') for seed in seeds]
        all_runs+=runs
        rates=np.array([r['event_rate'] for r in runs]);reference=runs[0]['maxwell_rate_reference']
        speed2=np.array([r['history'][-1]['speed_second'] for r in runs]);speed4=np.array([r['history'][-1]['speed_fourth'] for r in runs])
        n=runs[0]['config']['n'];nseeds=len(runs)
        second_reference=3.;fourth_reference=15.
        second_se=np.sqrt(6/(n*nseeds));fourth_se=np.sqrt(720/(n*nseeds))
        means=np.array([r['history'][-1]['mean'] for r in runs]).mean(axis=0)
        variances=np.array([r['history'][-1]['second'] for r in runs]).mean(axis=0)
        check=dict(rate=bool(abs(rates.mean()/reference-1)<.05),
            maxwell_speed_second=bool(abs(speed2.mean()-3)<5*second_se),
            maxwell_speed_fourth=bool(abs(speed4.mean()-15)<5*fourth_se),
            maxwell_means=bool(np.max(abs(means))<5/np.sqrt(n*nseeds)),
            maxwell_components=bool(np.max(abs(variances-1))<5*np.sqrt(2/(n*nseeds))))
        checks[law]=check
        groups.append(dict(law=law,rate=interval(rates),reference=reference,
            relative_rate_error=float(rates.mean()/reference-1),final_speed_second=interval(speed2),final_speed_fourth=interval(speed4),
            analytic_second_se=second_se,analytic_fourth_se=fourth_se,gates=check))
    stress={law:[read(f'{prefix}-stress-{law}-{seed}') for seed in seeds] for law in laws}
    all_runs+=[r for row in stress.values() for r in row]
    histories={law:np.array([[h['stress']/r['initial']['stress'] for h in r['history']] for r in runs]) for law,runs in stress.items()}
    eq=[]
    for law in [l for l in laws if l!='iso']:
        diff=histories[law]-histories['iso'];ci=interval(diff)
        passed=bool(np.min(ci['low'])>-.05 and np.max(ci['high'])<.05)
        eq.append(dict(law=law,vs='iso',paired_history_difference=ci,
            maximum_abs_interval_endpoint=float(max(abs(np.asarray(ci['low'])).max(),abs(np.asarray(ci['high'])).max())),
            final_difference_relative_to_iso_decay=interval(diff[:,-1]/(1-histories['iso'][:,-1])),equivalence_pass=passed))
    numerics=dict(max_candidate_probability=max(r['ledger']['max_probability'] for r in all_runs),
        max_energy_residual=max(r['max_energy_work_residual'] for r in all_runs),
        max_momentum_residual=max(r['max_momentum_impulse_residual'] for r in all_runs),
        max_collision_energy_per_particle=max(abs(r['ledger']['collision_energy_change'])/r['config']['n'] for r in all_runs),
        max_collision_momentum_per_particle=max(max(abs(x) for x in r['ledger']['collision_momentum_change'])/r['config']['n'] for r in all_runs))
    ng=dict(probability=numerics['max_candidate_probability']<.1,energy=numerics['max_energy_residual']<1e-10,
        momentum=numerics['max_momentum_residual']<1e-10,collision_energy=numerics['max_collision_energy_per_particle']<1e-10,
        collision_momentum=numerics['max_collision_momentum_per_particle']<1e-10)
    result=dict(equilibrium=groups,stress_equivalence=eq,numerics=numerics,numerical_gates=ng,
        all_control_gates_pass=bool(all(all(c.values()) for c in checks.values()) and all(e['equivalence_pass'] for e in eq) and all(ng.values())),
        scope='Maxwell equilibrium, exact conservation and tensor stress matching of this gas operator; no halo equivalence or arbitrary transport equivalence.')
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained')
    for law in laws:
        tt=[h['time'] for h in stress[law][0]['history']]
        ci=interval(histories[law]);ax.plot(tt,ci['mean'],label=law)
        ax.fill_between(tt,ci['low'],ci['high'],alpha=.15)
    ax.set(xlabel='Reference time',ylabel='Tensor stress / initial stress',title='Measured ordinary relaxation: viscosity-matched elastic laws')
    ax.legend();fig.savefig(out/'stress-controls.png',dpi=170);plt.close(fig)
    print(json.dumps(dict(all_control_gates_pass=result['all_control_gates_pass'],equilibrium=[{k:v for k,v in g.items() if k in ('law','relative_rate_error','gates')} for g in groups],stress_equivalence=[{k:v for k,v in e.items() if k!='paired_history_difference'} for e in eq],numerics=numerics),indent=2))


def responses(phase):
    out=BASE/(phase+'-analysis-01');out.mkdir(exist_ok=False)
    laws=['collisionless']+(['iso','angle01','angle005'] if phase=='limit' else LAWS)
    seeds=SEEDS if phase=='resonance' else list(range(260301,260305)) if phase=='limit' else list(range(260201,260205)) if phase=='transport' else list(range(260211,260215))
    runs={law:[read(f'{phase}-{law}-{seed}') for seed in seeds] for law in laws}
    groups=[];comparisons=[]
    for law in laws:
        groups.append(dict(law=law,impulse=interval([r['history'][-1]['impulse'] for r in runs[law]]),
            libration_fraction=interval([r['history'][-1]['instantaneous_libration_fraction'] for r in runs[law]]),
            q_labelled=[r['q_kick_over_resonance_halfwidth'] for r in runs[law]],
            q_exchange_invariant=[r['q_exchange_invariant_over_resonance_halfwidth'] for r in runs[law]],
            ncoll=[r['ncoll_per_libration'] for r in runs[law]],
            max_energy_residual=max(r['max_energy_work_residual'] for r in runs[law])))
    pairs=[('angle005','iso'),('angle01','iso'),('angle005','angle01'),('iso','collisionless'),('angle01','collisionless')] if phase=='limit' else [('angle02','iso'),('angle01','iso'),('angle01','angle02'),('iso','collisionless'),('angle02','collisionless')]
    for law1,law2 in pairs:
        for metric in ('impulse','instantaneous_libration_fraction'):
            diff=[a['history'][-1][metric]-b['history'][-1][metric] for a,b in zip(runs[law1],runs[law2])]
            ci=interval(diff)
            comparisons.append(dict(first=law1,second=law2,metric=metric,paired=ci,excludes_zero=bool(ci['low']>0 or ci['high']<0)))
    ctr=json.loads((BASE/('limit-control-analysis-01' if phase=='limit' else 'transport-control-analysis-01' if phase=='transport' else 'control-analysis-01')/'result.json').read_text())
    result=dict(phase=phase,groups=groups,comparisons=comparisons,
        controls_all_pass=ctr['all_control_gates_pass'],
        stress_qualified_laws=[e['law'] for e in ctr['stress_equivalence'] if e['equivalence_pass']],
        uncertainty_unit='Four independent matched realization seeds, Student t nominal95%; exploratory multiple observables.',
        scope='Finite-time forced gas response; no SIDM halo, self-gravity or observational validation.')
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for law in laws:
        tt=[h['time'] for h in runs[law][0]['history']]
        for ax,metric in zip(axes,('impulse','instantaneous_libration_fraction')):
            vals=[[h[metric] for h in r['history']] for r in runs[law]]
            ci=interval(vals);ax.plot(tt,ci['mean'],label=law);ax.fill_between(tt,ci['low'],ci['high'],alpha=.1)
    axes[0].set(xlabel='Reference time',ylabel='Mean external impulse',title='Signed resonant response')
    axes[1].set(xlabel='Reference time',ylabel='Instantaneous libration-region fraction',title='Population near the moving resonance')
    axes[1].legend(fontsize=8);fig.savefig(out/'response.png',dpi=170);plt.close(fig)
    print(json.dumps(result,indent=2))


def refinements(phase='refinement'):
    out=BASE/(phase+'-analysis-01');out.mkdir(exist_ok=False)
    seeds=SEEDS if phase=='refinement' else list(range(260201,260205))
    original_phase='resonance' if phase=='refinement' else 'transport'
    rows=[]
    for variant in ('halfdt','cells64'):
        for law in ('iso','angle01'):
            for metric in ('impulse','instantaneous_libration_fraction'):
                original=[read(f'{original_phase}-{law}-{seed}') for seed in seeds]
                refined=[read(f'{phase}-{variant}-{law}-{seed}') for seed in seeds]
                diff=[a['history'][-1][metric]-b['history'][-1][metric] for a,b in zip(refined,original)]
                rows.append(dict(variant=variant,law=law,metric=metric,paired=interval(diff)))
        # The interpreted law contrast itself must survive the change.
        for metric in ('impulse','instantaneous_libration_fraction'):
            refined_contrast=[];contrast_change=[]
            for seed in seeds:
                ai=read(f'{phase}-{variant}-iso-{seed}')['history'][-1][metric]
                aa=read(f'{phase}-{variant}-angle01-{seed}')['history'][-1][metric]
                oi=read(f'{original_phase}-iso-{seed}')['history'][-1][metric]
                oa=read(f'{original_phase}-angle01-{seed}')['history'][-1][metric]
                refined_contrast.append(aa-ai);contrast_change.append((aa-ai)-(oa-oi))
            rows.append(dict(variant=variant,law='angle01-minus-iso',metric=metric,refined_contrast=interval(refined_contrast),change=interval(contrast_change)))
    (out/'result.json').write_text(json.dumps(dict(rows=rows,scope='Selected finite timestep and cell refinements, nominal95% intervals; no continuum proof.'),indent=2)+'\n')
    print(json.dumps(rows,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=('controls','resonance','refinement','heldout','transport-controls','transport','transport-refinement','limit-controls','limit'),required=True)
    a=p.parse_args()
    if a.phase in ('controls','transport-controls','limit-controls'):controls(a.phase)
    elif a.phase in ('refinement','transport-refinement'):refinements(a.phase)
    else:responses(a.phase)
