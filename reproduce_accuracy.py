"""Regenerate the new-condition kernel, frozen decisions and independent tests.

This is reproduction of a previously registered investigation, not a new
prospective experiment. Failed and inconclusive reference outcomes must remain.
"""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:
    os.environ[key]='1'
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
import math
import numpy as np

ROOT=Path(__file__).resolve().parent/'accuracy'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compare(actual,expected,path='',changes=None):
    if changes is None:
        changes=[]
    if isinstance(expected,dict):
        for key,value in expected.items():
            compare(actual[key],value,path+'/'+key,changes)
    elif isinstance(expected,list):
        if len(actual)!=len(expected):
            raise ValueError('Different list length '+path)
        for i,(a,b) in enumerate(zip(actual,expected)):
            compare(a,b,path+'/'+str(i),changes)
    elif isinstance(expected,bool) or expected is None or isinstance(expected,str):
        if actual!=expected:
            changes.append(dict(path=path,expected=expected,actual=actual))
    elif not math.isclose(actual,expected,rel_tol=1e-9,abs_tol=1e-11):
        changes.append(dict(path=path,expected=expected,actual=actual))
    return changes


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--workers',type=int,choices=[1,2,3],default=1)
    p.add_argument('--stop-utc')
    a=p.parse_args()
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((ROOT/'source-manifest.json').read_text())
    for path,expected in manifest.items():
        if sha(ROOT/path)!=expected:
            raise ValueError('Changed released file '+path)
    stop=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=24)
    if a.stop_utc:
        supplied=datetime.datetime.fromisoformat(a.stop_utc.replace('Z','+00:00'))
        if supplied.tzinfo is None:
            raise ValueError('UTC offset required')
        stop=min(stop,supplied)
    if stop<=datetime.datetime.now(datetime.timezone.utc):
        raise ValueError('Production stop has passed')
    def run(script,*arguments):
        subprocess.run([sys.executable,str(ROOT/'scripts/population_accuracy'/script),*map(str,arguments)],cwd=ROOT,check=True)
    run('check_diagnostic.py','--out',out/'diagnostic-controls')
    run('check_independent.py','--out',out/'independent-controls')
    def matrix(name,extra_inputs=None):
        recipe=json.loads((ROOT/'test'/(name+'-recipe.json')).read_text())
        if name=='independent':
            for case in recipe['cases']:
                args=case['arguments'];args[args.index('--forecast')+1]=str(out/'forecast/result.json')
        spec=dict(**recipe,workers=a.workers,stop_utc=stop.isoformat(),source_sha256=dict(manifest,**(extra_inputs or {})))
        spec_path=out/(name+'-spec.json');spec_path.write_text(json.dumps(spec,indent=2)+'\n')
        with (out/(name+'-supervisor.log')).open('x') as log:
            subprocess.run([sys.executable,str(ROOT/'scripts/noise_sweep/guarded_queue.py'),'--spec',str(spec_path),'--out',str(out/name)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    matrix('kernel')
    run('forecast.py','--batch',out/'kernel','--table',ROOT/'results/population-response/preflight-02','--out',out/'forecast','--s','.5')
    prediction=out/'forecast/result.json'
    current=json.loads(prediction.read_text());reference=json.loads((ROOT/'test/reference-forecast.json').read_text())
    forecast_changes=compare(current['rows'],reference['rows'])
    kernel_checks={}
    original_kernel=ROOT/'results/population-accuracy/forecast-01/kernel-batches.npz'
    with np.load(original_kernel) as original, np.load(out/'forecast/kernel-batches.npz') as generated:
        for key in ['edges','fine','coarse']:
            if original[key].shape!=generated[key].shape:
                raise ValueError('Reproduced kernel has a different shape: '+key)
            difference=float(np.max(abs(original[key]-generated[key])))
            passed=bool(np.allclose(original[key],generated[key],rtol=1e-9,atol=1e-11))
            kernel_checks[key]=dict(maximum_absolute_difference=difference,within_reproduction_tolerance=passed)
            if not passed:
                forecast_changes.append(dict(path='kernel/'+key,maximum_absolute_difference=difference))
    (out/'forecast-comparison.json').write_text(json.dumps(dict(all_decisions_and_values_reproduced=not forecast_changes,kernel_arrays=kernel_checks,changes=forecast_changes),indent=2)+'\n')
    if forecast_changes:
        raise SystemExit('Forecast reproduction differs; retained records require review')
    marker=out/'forecast/FROZEN_PREDICTIONS'
    marker.write_text(json.dumps(dict(forecast_sha256=sha(prediction),
        frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scope='Same-seed reproduction of a previously frozen forecast; not a new prospective test.'),indent=2)+'\n')
    paths=[prediction,marker,out/'forecast/kernel-batches.npz']
    matrix('independent',{str(p):sha(p) for p in paths})
    run('analyze_independent.py','--matrix',out/'independent','--forecast',prediction,'--out',out/'analysis')
    current=json.loads((out/'analysis/result.json').read_text());reference=json.loads((ROOT/'test/reference-analysis.json').read_text())
    changes=compare(current['rows'],reference['rows'])+compare(current['counts'],reference['counts'],'counts')
    result=dict(all_reference_decisions_and_values_reproduced=not changes,changes=changes,
        source_manifest_sha256=sha(ROOT/'source-manifest.json'),counts=current['counts'],kernel_arrays=kernel_checks,
        kernel_cpu_seconds=json.loads((out/'kernel/ledger.json').read_text())['completed_cpu_seconds'],
        independent_cpu_seconds=json.loads((out/'independent/ledger.json').read_text())['completed_cpu_seconds'],
        scope='Reproduction of all eight kernels and fourteen independent numerical cases. Operational decisions and numerical values are checked, including failures and inconclusive results. These are not new independent physical samples. Timing and file hashes are not numerical-equality targets.')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    if changes:
        raise SystemExit('Independent reproduction differs; retained records require review')
    run('plot_accuracy.py','--analysis',out/'analysis/result.json','--out',out/'figures')
    print('Complete accuracy experiment reproduced, including its original qualification outcomes.')


if __name__=='__main__':
    main()
