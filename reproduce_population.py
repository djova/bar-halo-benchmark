"""Regenerate the full fixed population sample and independent central estimates."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,sys,time
import numpy as np

ROOT=Path(__file__).resolve().parent/'population'


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--workers',type=int,choices=[1,2,3],default=1)
    p.add_argument('--stop-utc',help='Optional earlier UTC stop; never overrides the finite48h run bound.')
    a=p.parse_args();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((ROOT/'source-manifest.json').read_text())
    for path,expected in manifest.items():
        if sha(ROOT/path)!=expected:raise ValueError('Changed released source/input: '+path)
    template=json.loads((ROOT/'reproduction.json').read_text())
    reference=json.loads((ROOT/'reference/result.json').read_text())
    now=datetime.datetime.now(datetime.timezone.utc);stop=now+datetime.timedelta(hours=48)
    if a.stop_utc:
        supplied=datetime.datetime.fromisoformat(a.stop_utc.replace('Z','+00:00'))
        if supplied.tzinfo is None:raise ValueError('Timezone required')
        stop=min(stop,supplied)
    if stop<=now:raise ValueError('Production stop has passed')
    cpu=0.;start=time.monotonic();records={};comparisons=[]
    for block in ['validation','distribution']:
        spec=dict(protocol='research/population-response/VALIDATION_01.md',workers=a.workers,
            cpu_ceiling_seconds=21600-cpu,stop_utc=stop.isoformat(),source_sha256=manifest,cases=template[block])
        if spec['cpu_ceiling_seconds']<60:raise RuntimeError('No remaining reproduction CPU allowance')
        specfile=out/(block+'-spec.json');specfile.write_text(json.dumps(spec,indent=2)+'\n')
        with (out/(block+'-supervisor.log')).open('w') as log:
            subprocess.run([sys.executable,str(ROOT/'scripts/noise_sweep/guarded_queue.py'),
                '--spec',str(specfile),'--out',str(out/block)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,
                check=True,timeout=172850)
        ledger=json.loads((out/block/'ledger.json').read_text());cpu+=ledger['completed_cpu_seconds']
        if not (out/block/'TERMINAL').exists() or any(v['state']!='complete' for v in ledger['cases'].values()):
            raise RuntimeError('Reproduction incomplete; retained ledger: '+block)
        for key in ledger['cases']:
            folder=out/block/key;r=json.loads((folder/'result.json').read_text())
            if sha(folder/'recorded.npz')!=r['raw_sha256']:raise ValueError('Changed recorded output')
            expected=reference['cases'][key]
            if block=='validation':
                if r['columns']!=expected['columns'] or r['gates']!=expected['gates']:
                    raise ValueError('Changed measurement definitions/gates: '+key)
                delta=float(np.max(abs(np.array(r['mean'])-expected['mean'])))
            elif key.startswith('noisy'):
                actual=[v['bar_impulse'] for v in r['history'] if v['tau'] in [10.,20.]]
                delta=float(np.max(abs(np.array(actual)-expected['bar_impulse'])))
            else:delta=float(np.max(abs(np.array(r['remainder_bar_impulse'])-expected['bar_impulse'])))
            if delta>=1e-9:raise ValueError(f'Reference value mismatch {key}: {delta}')
            if block!='validation' and r['gates']!=expected['gates']:raise ValueError('Changed local gates')
            comparisons.append(dict(case=key,max_absolute_error=delta,pass_=delta<1e-9));records[key]=r
    with (out/'analysis.log').open('w') as log:
        subprocess.run([sys.executable,str(ROOT/'scripts/population_response/analyze_validation.py'),
            '--batch',str(out/'validation'),'--table',str(ROOT/'inputs/halo-table'),
            '--out',str(out/'analysis')],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=120)
    analysis=json.loads((out/'analysis/result.json').read_text())
    failures=[]
    for row,expected in zip(analysis['rows'],reference['analysis_rows']):
        if (row['s'],row['tau'],row['population'])!=(expected['s'],expected['tau'],expected['population']):raise ValueError('Analysis ordering changed')
        for field in ['integral_w_K_B','fine_minus_coarse','wider_minus_narrower']:
            error=max(abs(row[field]['mean']-expected[field]['mean']),float(np.max(abs(np.array(row[field]['ci95'])-expected[field]['ci95']))))
            if error>=1e-9:failures.append((row['s'],row['tau'],row['population'],field,error))
        for field in ['numerical_window_qualified','qualified_sign']:
            if row[field]!=expected[field]:failures.append((row['s'],row['tau'],row['population'],field))
    if len(analysis['rows'])!=len(reference['analysis_rows']) or failures:raise ValueError('Analysis comparison failed: '+str(failures))
    with np.load(out/'analysis/kernel-batches.npz') as actual,np.load(ROOT/'reference/kernel-batches.npz') as expected:
        kernel_errors={key:float(np.max(abs(actual[key]-expected[key]))) for key in expected.files}
    if max(kernel_errors.values())>=1e-8:raise ValueError('Recorded response-kernel mismatch')
    central=[]
    for s,label in [('0','stationary'),('.25','moving')]:
        noisy=records['noisy-s'+s];smooth=records[label+'-characteristic']
        for ti,t in enumerate([10.,20.]):
            N=next(v['bar_impulse'] for v in noisy['history'] if v['tau']==t)
            for pi,name in enumerate(['gaussian','halo','exponential']):
                ci=smooth['populations'].index(name+'-40');value=N[pi]-smooth['remainder_bar_impulse'][ti][ci]
                central.append(dict(s=float(s),tau=t,population=name+'-40',distribution=float(value)))
    refcentral=reference['central']
    if len(central)!=len(refcentral):raise ValueError('Incomplete central comparison')
    for row,expected in zip(central,refcentral):row['archived_distribution_refinement_qualification']=expected['archived_distribution_refinement_qualification']
    for row,expected in zip(central,refcentral):
        if (row['s'],row['tau'],row['population'])!=(expected['s'],expected['tau'],expected['population']) or abs(row['distribution']-expected['distribution'])>=1e-9:raise ValueError('Central distribution comparison failed')
    result=dict(reference_values_reproduced=True,cases=comparisons,kernel_errors=kernel_errors,
        central=central,scientific_cpu_seconds=cpu,wall_seconds=time.monotonic()-start,
        python=sys.version,numpy=np.__version__,source_manifest_sha256=sha(ROOT/'source-manifest.json'),
        scope='Same-seed regeneration of16trajectory cases, four central independent distribution/characteristic calculations, and their numerical readback. This is not a new independent sample. Separate archived distribution refinement matrices and held-out population/3Dtests are not rerun by this command. Reproduced failures remain failures.')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    subprocess.run([sys.executable,str(ROOT/'plot_population.py'),'--analysis',str(out/'analysis/result.json'),
        '--distribution',str(out/'result.json'),'--out',str(out/'population-response.png')],check=True,timeout=120)
    print(json.dumps({k:v for k,v in result.items() if k not in ['cases','kernel_errors']},indent=2))


if __name__=='__main__':main()
