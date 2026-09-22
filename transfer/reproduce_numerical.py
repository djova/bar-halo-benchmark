"""Standalone six-case reproduction of the final fourth-order numerical matrix."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse,datetime,hashlib,json,os,subprocess,sys
from verify_numerical_reference import verify
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--agama',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--workers',type=int,choices=[1,2,3,4],default=1)
    p.add_argument('--smoke',action='store_true');p.add_argument('--resume',action='store_true')
    p.add_argument('--reference',type=Path,default=ROOT/'reference/final-numerical-analysis.json')
    a=p.parse_args();out=a.out.resolve();library=a.agama.resolve()
    if not (library/'agama.so').is_file():raise SystemExit('First build the pinned patched dependency; see README.md.')
    sources=json.loads((ROOT/'final-numerical-manifest.json').read_text())
    for name,digest in sources.items():assert sha(ROOT/name)==digest,name
    out.mkdir(parents=True,exist_ok=a.resume)
    build=ROOT/'build/noise-sweep';build.mkdir(parents=True,exist_ok=True)
    subprocess.run(['c++','-std=c++17','-O3','-fno-math-errno','-fPIC','-shared',str(ROOT/'benchmark/orbit_fourth.cpp'),'-o',str(build/'orbit-fourth.so')],check=True,timeout=120)
    library_sha=sha(library/'agama.so');kernel_sha=sha(build/'orbit-fourth.so')
    env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    variants=[]
    for label,dt,refine in [('candidate',.01,4),('halfstep',.005,4),('halfcadence',.01,8)]:
        for smooth in [False,True]:variants.append((label+('-smooth' if smooth else '-noisy'),dt,refine,smooth))
    if a.smoke:variants=[('smoke-noisy',.01,4,False),('smoke-smooth',.01,4,True)]
    def run(item):
        name,dt,refine,smooth=item;folder=out/name
        expected=dict(n=128 if a.smoke else 16384,seed=8192 if a.smoke else 8302,start=0,
                      dt=dt,noise_refine=refine,no_noise=smooth,no_bar=a.smoke,pilot=a.smoke,case='A' if a.smoke else 'B')
        def read():
            assert (folder/'COMPLETE').exists(),name
            d=json.loads((folder/'result.json').read_text())
            assert all(d['settings'][key]==value for key,value in expected.items())
            assert d['raw_sha256']==sha(folder/'recorded.npz')
            assert all(sources[key]==value for key,value in d['source_sha256'].items())
            assert d['library_sha256']==kernel_sha and d['agama_library_sha256']==library_sha
            assert d['forecast_sha256']==(None if a.smoke else sources['forecast.json'])
            return dict(case=name,local_pass=d['all_pass'],cpu_seconds=d['cpu_seconds'])
        if folder.exists():
            if not a.resume or not (folder/'COMPLETE').exists():raise RuntimeError('Preserve the incomplete attempt separately before resuming: '+name)
            return {**read(),'reused_complete_case':True}
        args=['--agama-path',str(library),'--n',str(expected['n']),'--seed',str(expected['seed']),
              '--dt',str(dt),'--noise-refine',str(refine)]
        if a.smoke:args+=['--pilot','--no-bar']
        else:args+=['--forecast',str(ROOT/'forecast.json'),'--case','B']
        if smooth:args+=['--no-noise']
        command=['nice','-n','10',sys.executable,str(ROOT/'scripts/noise_sweep/run_orbits_cadence.py'),'--out',str(folder),*args]
        with (out/(name+'.log')).open('x') as log:
            proc=subprocess.Popen(command,cwd=ROOT,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT)
            (out/(name+'-process.json')).write_text(json.dumps(dict(pid=proc.pid,command=command,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
            try:code=proc.wait(timeout=7200)
            except subprocess.TimeoutExpired:
                proc.terminate()
                try:proc.wait(timeout=10)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
                raise
            if code:raise RuntimeError(f'{name} exited with{code}; inspect its preserved log.')
        return read()
    with ThreadPoolExecutor(max_workers=a.workers) as pool:cases=list(pool.map(run,variants))
    reference=None
    if not a.smoke:
        (out/'TERMINAL').write_text('All six finite cases completed; numerical qualification remains separate.\n')
        if not (out/'analysis').exists():
            subprocess.run([sys.executable,str(ROOT/'scripts/noise_sweep/analyze_final_numerical.py'),'--root',str(out),
                            '--forecast',str(ROOT/'forecast.json'),'--out',str(out/'analysis')],cwd=ROOT,env=env,check=True,timeout=600)
        if a.reference.is_file():reference=verify(json.loads((out/'analysis/result.json').read_text()),json.loads(a.reference.read_text()))
    receipt=dict(cases=cases,scientific_cpu_seconds=sum(c['cpu_seconds'] for c in cases),smoke_only=a.smoke,
                 source_manifest=sources,reference_comparison=reference,
                 scope='Same-seed reproduction. A missing reference comparison is not a verified reproduction claim; '
                 'a failed numerical qualification remains failed. Smoke checks do not establish full-duration accuracy.')
    name='reproduction-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'.json'
    with (out/name).open('x') as f:f.write(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
