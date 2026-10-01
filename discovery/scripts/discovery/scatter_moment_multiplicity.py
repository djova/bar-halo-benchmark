"""Supplementary two-waveform intervals; frozen operational gates unchanged."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import json
from pathlib import Path
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/discovery-20261001/scattering'
rows=[]
for condition in ('original','second'):
    r=json.loads((BASE/f'moment-{condition}-analysis-01/result.json').read_text())
    ci=r['primary_B_minus_A'];df=len(r['seeds'])-1
    margin=float(t.ppf(1-.05/(2*2),df)*ci['se'])
    family=dict(mean=ci['mean'],low=ci['mean']-margin,high=ci['mean']+margin)
    rows.append(dict(condition=condition,nominal95_per_condition=ci,original_operational_refinement_trigger=r['primary_excludes_zero'],
        supplementary_Bonferroni95_two_waveform_family=family,supplementary_interval_excludes_zero=bool(family['low']>0 or family['high']<0)))
out=BASE/'moment-multiplicity-analysis-01';out.mkdir(exist_ok=False)
result=dict(rows=rows,scope='Supplementary nominal95% simultaneous coverage for the frozen two A/B waveform primary endpoints using Bonferroni. Not a correction over the entire adaptive campaign or every secondary/refinement screen; does not alter original gates. No campaign-wide discovery inference.')
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
