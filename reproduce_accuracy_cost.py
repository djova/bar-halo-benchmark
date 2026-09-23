"""Run and verify every matched-cost case; remeasure rather than reproduce timings."""
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
import numpy as np

ROOT=Path(__file__).resolve().parent/'accuracy'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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
    subprocess.run([sys.executable,str(ROOT/'scripts/population_accuracy/check_cost_weights.py'),'--out',str(out/'weight-controls')],cwd=ROOT,check=True)
    template=json.loads((ROOT/'cost/reproduction.json').read_text())
    stop=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=24)
    if a.stop_utc:
        supplied=datetime.datetime.fromisoformat(a.stop_utc.replace('Z','+00:00'))
        if supplied.tzinfo is None:
            raise ValueError('UTC offset required')
        stop=min(stop,supplied)
    if stop<=datetime.datetime.now(datetime.timezone.utc):
        raise ValueError('Production deadline passed')
    spec=dict(protocol='research/population-accuracy/ESTIMATOR_COST_02.md',workers=a.workers,
        cpu_ceiling_seconds=3000,stop_utc=stop.isoformat(),source_sha256=manifest,cases=template['cases'])
    (out/'spec.json').write_text(json.dumps(spec,indent=2)+'\n')
    with (out/'supervisor.log').open('x') as log:
        subprocess.run([sys.executable,str(ROOT/'scripts/noise_sweep/guarded_queue.py'),'--spec',str(out/'spec.json'),'--out',str(out/'matrix')],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/population_accuracy/analyze_cost.py'),'--matrix',str(out/'matrix'),'--out',str(out/'analysis')],cwd=ROOT,check=True)
    reference=json.loads((ROOT/'cost/reference.json').read_text())
    checks=[]
    for name,ref in reference['cases'].items():
        record=json.loads((out/'matrix'/name/'result.json').read_text())
        with np.load(out/'matrix'/name/'recorded.npz') as z:
            differences={key:float(np.max(abs(z[key]-np.array(value)))) for key,value in ref['arrays'].items()}
        gates_same=record['gates']==ref['gates']
        checks.append(dict(case=name,maximum_differences=differences,gates_unchanged=gates_same,
            numerical_values_reproduced=bool(gates_same and max(differences.values())<1e-12)))
    passed=len(checks)==16 and all(r['numerical_values_reproduced'] for r in checks)
    result=dict(all_reference_numerical_values_reproduced=passed,cases=checks,
        timings_remeasured_not_required_to_match=True,source_manifest_sha256=sha(ROOT/'source-manifest.json'),
        scope='All16same-seed matched-cost cases regenerated from public inputs. Numerical means and full covariance are compared; CPU timings are new measurements on this host. This does not create new independent physical samples, certify asymptotic precision scaling or validate the separate new-sweep accuracy experiment.')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    if not passed:
        raise SystemExit('Numerical reproduction differs; retained outputs require review')
    subprocess.run([sys.executable,str(ROOT/'scripts/population_accuracy/plot_results.py'),'--cost',str(out/'analysis/result.json'),'--out',str(out/'figures')],cwd=ROOT,check=True)
    print('All16numerical statistics reproduced; CPU performance independently remeasured.')


if __name__=='__main__':
    main()
