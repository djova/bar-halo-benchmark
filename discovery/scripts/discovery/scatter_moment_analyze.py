"""Frozen conditional-moment law controls and signed response endpoints."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse
import json
import numpy as np
import scatter_analyze as old

BASE=old.BASE


def save(label,result):
    out=BASE/label;out.mkdir(exist_ok=False)
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))


def controls():
    seeds=range(260511,260515);laws=('A','B');eq=[];all_runs=[]
    for law in laws:
        rr=[old.read(f'moment-controls-equilibrium-{law}-{s}') for s in seeds];all_runs+=rr
        n=rr[0]['config']['n'];ns=len(rr)
        speed2=np.mean([r['history'][-1]['speed_second'] for r in rr]);speed4=np.mean([r['history'][-1]['speed_fourth'] for r in rr])
        means=np.mean([r['history'][-1]['mean'] for r in rr],axis=0);second=np.mean([r['history'][-1]['second'] for r in rr],axis=0)
        rates=[r['event_rate'] for r in rr];relative=np.mean(rates)/rr[0]['maxwell_rate_reference']-1
        gates=dict(rate=bool(abs(relative)<.05),maxwell_speed_second=bool(abs(speed2-3)<5*np.sqrt(6/(n*ns))),
            maxwell_speed_fourth=bool(abs(speed4-15)<5*np.sqrt(720/(n*ns))),maxwell_means=bool(np.max(abs(means))<5/np.sqrt(n*ns)),
            maxwell_components=bool(np.max(abs(second-1))<5*np.sqrt(2/(n*ns))))
        eq.append(dict(law=law,relative_rate_error=float(relative),speed_second=float(speed2),speed_fourth=float(speed4),gates=gates))
    stress={l:[old.read(f'moment-controls-stress-{l}-{s}') for s in seeds] for l in laws}
    all_runs +=[r for rr in stress.values() for r in rr]
    hh={l:np.array([[h['stress']/r['initial']['stress'] for h in r['history']] for r in rr]) for l,rr in stress.items()}
    ci=old.interval(hh['B']-hh['A'])
    maxend=float(max(np.max(abs(np.array(ci['low']))),np.max(abs(np.array(ci['high'])))))
    numerics=dict(max_probability=max(r['ledger']['max_probability'] for r in all_runs),
        max_energy_residual=max(r['max_energy_work_residual'] for r in all_runs),max_momentum_residual=max(r['max_momentum_impulse_residual'] for r in all_runs),
        max_collision_energy_per_particle=max(abs(r['ledger']['collision_energy_change'])/r['config']['n'] for r in all_runs),
        max_collision_momentum_per_particle=max(max(abs(v) for v in r['ledger']['collision_momentum_change'])/r['config']['n'] for r in all_runs))
    numerical_pass=numerics['max_probability']<.1 and max(v for k,v in numerics.items() if k!='max_probability')<1e-10
    save('moment-control-analysis-01',dict(equilibrium=eq,stress_difference=ci,stress_maximum_abs_interval_endpoint=maxend,stress_equivalence_pass=maxend<.05,
        numerics=numerics,numerical_pass=numerical_pass,all_control_gates_pass=bool(all(all(r['gates'].values()) for r in eq) and maxend<.05 and numerical_pass),
        uncertainty_unit='Four initial-state seeds; nominal95% pointwise Student-t stress intervals, not simultaneous bands.'))


def responses(condition):
    seeds=range(260521,260537) if condition=='original' else range(260541,260557)
    groups={l:[old.read(f'moment-{condition}-{l}-{s}') for s in seeds] for l in ('A','B')}
    vals={l:np.array([r['history'][-1]['impulse'] for r in rr]) for l,rr in groups.items()}
    ci=old.interval(vals['B']-vals['A'])
    rows={l:dict(impulse=old.interval(vals[l]),q=[r['q_exchange_invariant_over_resonance_halfwidth'] for r in rr],ncoll=[r['ncoll_per_libration'] for r in rr],
        max_energy_residual=max(r['max_energy_work_residual'] for r in rr),max_momentum_residual=max(r['max_momentum_impulse_residual'] for r in rr)) for l,rr in groups.items()}
    snap=old.interval([b['history'][-1]['instantaneous_libration_fraction']-a['history'][-1]['instantaneous_libration_fraction'] for a,b in zip(groups['A'],groups['B'])])
    result=dict(condition=condition,seeds=list(seeds),groups=rows,primary_B_minus_A=ci,primary_excludes_zero=bool(ci['low']>0 or ci['high']<0),
        paired_seed_output_correlation=float(np.corrcoef(vals['A'],vals['B'])[0,1]),secondary_snapshot_difference=snap,
        controls_all_pass=json.loads((BASE/'moment-control-analysis-01/result.json').read_text())['all_control_gates_pass'],
        uncertainty_unit='16 independent initial-state seeds; nominal95% Student-t interval, shared initial states but no common stochastic trajectories.',
        scope='Either-signed finite-time impulse comparison under matched conditional linear-vx drift/raw second moments. Two exploratory waveform endpoints; no SIDM prediction or general magnitude convergence.')
    save(f'moment-{condition}-analysis-01',result)


def refinement(condition):
    seeds=range(260521,260537) if condition=='original' else range(260541,260557)
    orig=json.loads((BASE/f'moment-{condition}-analysis-01/result.json').read_text());sgn=np.sign(orig['primary_B_minus_A']['mean'])
    baseline=[]
    for s in seeds:
        aa=old.read(f'moment-{condition}-A-{s}');bb=old.read(f'moment-{condition}-B-{s}');baseline.append(bb['history'][-1]['impulse']-aa['history'][-1]['impulse'])
    rows=[]
    for variant in ('halfdt','cells64'):
        contrast=[];all_runs=[]
        for s in seeds:
            aa=old.read(f'moment-{condition}-{variant}-A-{s}');bb=old.read(f'moment-{condition}-{variant}-B-{s}');all_runs +=[aa,bb]
            contrast.append(bb['history'][-1]['impulse']-aa['history'][-1]['impulse'])
        ci=old.interval(contrast);change=old.interval(np.array(contrast)-baseline)
        rows.append(dict(variant=variant,contrast=ci,change=change,same_signed_interval=bool(ci['low']>0 if sgn>0 else ci['high']<0),
            max_energy_residual=max(r['max_energy_work_residual'] for r in all_runs),max_momentum_residual=max(r['max_momentum_impulse_residual'] for r in all_runs)))
    save(f'moment-{condition}-refinement-analysis-01',dict(rows=rows,signed_signal_at_all_selected_discretizations=all(r['same_signed_interval'] for r in rows),
        scope='Frozen either-sign endpoint; selected refinements do not certify continuum magnitude.'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=('controls','original','second','refinement-original','refinement-second'),required=True)
    a=p.parse_args()
    if a.phase=='controls':controls()
    elif a.phase.startswith('refinement'):refinement(a.phase.replace('refinement-',''))
    else:responses(a.phase)
