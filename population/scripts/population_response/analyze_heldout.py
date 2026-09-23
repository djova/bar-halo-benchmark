"""Compare every prospective population forecast to independent forced evolution."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
from pathlib import Path
import argparse,json
import numpy as np
from analyze_refinement import read_matrix,noisy_B,sha
from analyze_validation import interval,equivalent
from heldout_profiles import NAMES


def main():
 p=argparse.ArgumentParser()
 for arg in ['matrix','forecast','out']:p.add_argument('--'+arg,type=Path,required=True)
 a=p.parse_args();records=read_matrix(a.matrix);forecast=json.loads(a.forecast.read_text())
 if len(records)!=23 or len(forecast['rows'])!=24:raise ValueError('Need complete frozen matrix and forecasts')
 if any(r['forecast_sha256']!=sha(a.forecast) for r in records.values()):raise ValueError('Changed forecast')
 rows=[]
 for s,label in [(0.,'stationary'),(.25,'moving')]:
  noisy={k:records[f'{label}-noisy-{k}'] for k in ['base','fine','halfstep','domain','wide','wide-fine','unforced-wide']}
  smooth={k:records[f'{label}-smooth-{k}'] for k in ['base','fine','halfstep','domain']}
  finest=records[label+'-smooth-finer'] if s else smooth['fine']
  comparison=smooth['fine'] if s else smooth['base']
  local=all(r['all_pass'] for r in [*noisy.values(),*smooth.values(),finest])
  for ti,t in enumerate([10.,20.]):
   for pi,name in enumerate(NAMES):
    c=lambda record,window:record['remainder_bar_impulse'][ti][record['populations'].index(name+'-'+str(window))]
    n=lambda key:float(noisy_B(noisy[key],t)[pi])
    window_change=(n('wide')-c(smooth['domain'],64))-(n('domain')-c(smooth['domain'],40))
    for window in [40,64]:
     prediction=next(r for r in forecast['rows'] if r['s']==s and r['tau']==t and r['population']==name+'-'+str(window))
     changes=dict(characteristic_quadrature=c(finest,window)-c(comparison,window),
      characteristic_timestep=c(smooth['halfstep'],window)-c(smooth['base'],window),
      characteristic_domain=c(smooth['domain'],window)-c(smooth['base'],window),
      noisy_mesh=n('fine')-n('base'),noisy_timestep=n('halfstep')-n('base'),
      noisy_domain=n('domain')-n('base'),noisy_wide_mesh=n('wide-fine')-n('wide'),physical_window=window_change)
     gates={key:abs(value)<2e-4 for key,value in changes.items()}
     independent=n('fine' if window==40 else 'wide-fine')-c(finest,window)
     discrepancy=interval(independent-np.array(prediction['batch_predictions']))
     allowance=prediction['frozen_independent_accuracy_allowance']
     numerical=bool(local and all(gates.values()));accuracy=equivalent(discrepancy,allowance)
     rows.append(dict(s=s,tau=t,population=name+'-'+str(window),independent_integral_w_K_B=independent,
      frozen_prediction=prediction['prediction'],independent_minus_predicted=discrepancy,
      frozen_accuracy_allowance=allowance,comparison_changes=changes,comparison_gates=gates,
      all_local_gates_pass=local,numerical_window_qualified=numerical,
      retained_characteristic_base_fine_change=c(smooth['fine'],window)-c(smooth['base'],window),
      forecast_qualified=prediction['forecast_qualified'],accuracy_interval_contained=accuracy,
      prospective_prediction_qualified=bool(numerical and prediction['forecast_qualified'] and accuracy)))
 a.out.mkdir(parents=True,exist_ok=False)
 result=dict(rows=rows,forecast_sha256=sha(a.forecast),source_sha256=sha(__file__),
  inputs={str(path):sha(path) for path in [a.matrix/'manifest.json',a.matrix/'ledger.json',*sorted(a.matrix.glob('*/result.json'))]},
  scope='All24prospective population/time/window/sweep comparisons. Original forecast intervals and allowances are unchanged. Independent noisy distribution and positive collisionless quadrature; no fitted forced outcome, selected endpoint or new3Dphysical validation. Numerical comparisons are operational diagnostics, not certified error bounds.')
 (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
 for r in rows:print(r['s'],r['tau'],r['population'],r['independent_integral_w_K_B'],r['prospective_prediction_qualified'])

if __name__=='__main__':main()
