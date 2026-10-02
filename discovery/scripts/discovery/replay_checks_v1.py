"""Recompute recorded control arithmetic, without forces or orbit evolution."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
import argparse, hashlib, json, math, resource, time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(29,30))
if os.getpriority(os.PRIO_PROCESS,0)<10:os.nice(10-os.getpriority(os.PRIO_PROCESS,0))
start=time.process_time()
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
checks=[]
def same(value,expected,label):
    assert math.isclose(float(value),float(expected),rel_tol=2e-13,abs_tol=1e-20),(label,value,expected)
    checks.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stat(x):return dict(mean=float(x.mean()),standard_error=float(x.std(ddof=1)/np.sqrt(len(x))))
def run(out):
    out.mkdir(parents=True,exist_ok=False)
    operands=ROOT/'operands/checks-v1'
    data=json.loads((ROOT/'data/checks-v1.json').read_text())
    manifest=json.loads((operands/'manifest.json').read_text())
    for f in manifest['artifacts']:
        assert sha(operands/f['path'])==f['sha256'],f['path']
    profiles=json.loads((operands/'phase-profiles.json').read_text())
    for case in profiles['cases']:
        seed,pop=case['seed'],case['population']
        curve=next(r for r in data['phase']['curves'] if r['seed']==seed and r['population']==pop)
        row=next(r for r in data['phase']['rows'] if r['seed']==seed and r['population']==pop)
        component=['v_R_squared','v_phi_squared','v_z_squared'].index(curve['component'])
        baseline=case['analytic'][0]['shells'][curve['shell']]['second_diagonal'][component]
        for name in ('analytic','live'):
            max_change=0
            for index,record in enumerate(case[name]):
                same(record['time'],curve['times'][index],f'{seed}-{pop}-{name}-time-{index}')
                shell=record['shells'][curve['shell']]
                same(100*(shell['second_diagonal'][component]/baseline-1),curve[name+'_percent'][index],f'{seed}-{pop}-{name}-curve-{index}')
                for s in record['shells']:
                    assert s['coverage'] and s['particles']>=256
                    for c,v in enumerate(s['second_diagonal']):
                        initial=case['analytic'][0]['shells'][s['shell']]['second_diagonal'][c]
                        max_change=max(max_change,abs(v/initial-1))
            expected=abs(row['extrema'][name][name+'_change'])
            same(max_change,expected,f'{seed}-{pop}-{name}-all-shell-maximum')
            assert (max_change>.05)==row['descriptive_analytic_flags']['covered_second'] if name=='analytic' else max_change>.05
    with np.load(operands/'warm-initial.npz',allow_pickle=False) as a,np.load(operands/'warm-fine-response.npz',allow_pickle=False) as b:
        assert len(a['Rc'])==512
        for r in data['warm']['rows']:
            j=1 if r['frequency']==5 else 2
            mask=np.ones(512) if r['Rc_upper'] is None else (a['Rc']<r['Rc_upper'])/r['physical_mass']
            values=(b['positive_64'][j]-b['positive_64'][0])*mask
            actual=stat(values)
            for key,v in actual.items():same(v,r['paired'][key],f'warm-{r["Rc_upper"]}-{r["frequency"]}-{key}')
            same(actual['standard_error']/actual['mean'],r['relative_SE'],'warm-relative-SE')
            order=np.argsort(-abs(values));absolute=float(abs(values).sum())
            same(float(values.sum()**2/np.sum(values**2)),r['tails']['effective_sample_size'],'warm-heat-ESS')
            for point in r['tails']['top_absolute_contributions']:
                same(float(abs(values[order[:point['count']]]).sum()/absolute),point['absolute_share'],'warm-contribution-share')
            assert not (actual['mean']>0 and actual['standard_error']<=data['warm']['precision_allowance']*actual['mean'])
    weights=np.array(data['echo']['contrast_weights'])
    peaks=np.array(data['echo']['zero_reference_peaks'])
    for r in [*data['echo']['rows'],*data['echo']['energy_continuation']['rows']]:
        cases=np.array(r['case_values']['real'])+1j*np.array(r['case_values']['imag'])
        mixed=weights@cases
        # Direct integral and separate sign-case sums differ only by reduction order.
        recorded=np.array(r['mixed']['real'])+1j*np.array(r['mixed']['imag'])
        assert float(abs(mixed-recorded).max())<=1e-18
        ratios=abs(recorded)/peaks
        for v,e in zip(ratios,r['zero_error_over_frozen_reference_peak']):same(v,e,'echo-zero-error-over-peak')
        decision=bool(np.all(ratios<=data['echo']['zero_allowance_over_reference_peak']))
        assert decision==r['gates']['zero']
    result=dict(status='COMPLETE',saved_arithmetic_passed=True,comparisons=len(checks),
        original_physical_qualifications_unchanged=True,
        scope='Saved profile/response arithmetic only; no scientific evolution, confidence calibration or physical validity test.',
        cpu_seconds=time.process_time()-start,inputs_sha256={p.name:sha(p) for p in [ROOT/'data/checks-v1.json',operands/'manifest.json']},
        reader_sha256=sha(Path(__file__)))
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','saved_arithmetic_passed','comparisons','cpu_seconds')}))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);run(p.parse_args().out)
