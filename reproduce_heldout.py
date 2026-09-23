"""Regenerate frozen kernel forecasts, then independently evolve the held-out shapes."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,sys
import numpy as np
ROOT=Path(__file__).resolve().parent/'population'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--workers',type=int,choices=[1,2,3],default=1);p.add_argument('--check-forecasts-only',action='store_true');p.add_argument('--stop-utc',help='Optional earlier UTC stop for forced evolution')
    a=p.parse_args();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((ROOT/'source-manifest.json').read_text())
    for path,expected in manifest.items():
        if sha(ROOT/path)!=expected:raise ValueError('Changed released file '+path)
    forecast=ROOT/'heldout/forecast/result.json'
    subprocess.run([sys.executable,str(ROOT/'scripts/population_response/reweight_heldout.py'),
        '--kernel',str(ROOT/'reference/kernel-batches.npz'),'--analysis',str(ROOT/'reference/validation-analysis.json'),
        '--forecast',str(forecast),'--table',str(ROOT/'inputs/halo-table'),'--out',str(out/'regenerated-forecasts.json')],check=True)
    if a.check_forecasts_only:
        print('All prospective forecasts regenerated; no forced evolution requested.');return
    template=json.loads((ROOT/'heldout/reproduction.json').read_text())
    stop=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=48)
    if a.stop_utc:
        supplied=datetime.datetime.fromisoformat(a.stop_utc.replace('Z','+00:00'))
        if supplied.tzinfo is None:raise ValueError('UTC offset required')
        stop=min(stop,supplied)
    if stop<=datetime.datetime.now(datetime.timezone.utc):raise ValueError('Production deadline passed')
    spec=dict(protocol='research/population-response/HELDOUT_MATRIX_01.md',workers=a.workers,
        cpu_ceiling_seconds=14400,stop_utc=stop.isoformat(),
        source_sha256=manifest,cases=template['cases'])
    (out/'spec.json').write_text(json.dumps(spec,indent=2)+'\n')
    with (out/'supervisor.log').open('x') as log:
        subprocess.run([sys.executable,str(ROOT/'scripts/noise_sweep/guarded_queue.py'),'--spec',str(out/'spec.json'),'--out',str(out/'matrix')],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/population_response/analyze_heldout.py'),'--matrix',str(out/'matrix'),
        '--forecast',str(forecast),'--out',str(out/'analysis')],cwd=ROOT,check=True)
    actual=json.loads((out/'analysis/result.json').read_text());expected=json.loads((ROOT/'heldout/reference.json').read_text())
    differences=[]
    if len(actual['rows'])!=24 or len(expected['rows'])!=24:raise ValueError('Need all24comparisons')
    for row,ref in zip(actual['rows'],expected['rows']):
        if any(row[k]!=ref[k] for k in ['s','tau','population']):raise ValueError('Changed comparison definition')
        delta=abs(row['independent_integral_w_K_B']-ref['independent_integral_w_K_B'])
        delta=max(delta,max(abs(row['comparison_changes'][k]-v) for k,v in ref['comparison_changes'].items()))
        unchanged=all(row[k]==ref[k] for k in ['comparison_gates','all_local_gates_pass','numerical_window_qualified','forecast_qualified','accuracy_interval_contained','prospective_prediction_qualified'])
        differences.append(dict(s=row['s'],tau=row['tau'],population=row['population'],max_difference=delta,gates_unchanged=unchanged))
    passes=all(r['max_difference']<1e-9 and r['gates_unchanged'] for r in differences)
    result=dict(reference_values_reproduced=passes,rows=differences,source_manifest_sha256=sha(ROOT/'source-manifest.json'),
        scope='Regeneration of all frozen predictions and23independent held-out numerical cases. Historical prospective test reproduced, including failures; not a new prospective physical experiment or a3Dprediction.')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    if not passes:raise SystemExit('Reproduction differs; inspect retained complete output')
    subprocess.run([sys.executable,str(ROOT/'plot_heldout.py'),'--analysis',str(out/'analysis/result.json'),'--out',str(out/'heldout-predictions.png')],check=True)
    print('Held-out forecasts, measurements and decisions reproduced.')

if __name__=='__main__':main()
