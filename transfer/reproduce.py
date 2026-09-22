"""Offline seeded Cartesian transfer reproduction with an explicit AGAMA dependency."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys

ROOT=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--agama',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--workers',type=int,choices=[1,2,3,4],default=1)
    p.add_argument('--smoke',action='store_true')
    a=p.parse_args();out=a.out.resolve();library=a.agama.resolve()
    if not (library/'agama.so').exists():
        raise SystemExit('Build the specified patched AGAMA first; see transfer/README.md.')
    sources=json.loads((ROOT/'source-manifest.json').read_text())
    for name,digest in sources.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise SystemExit('Scientific source differs from the recorded release: '+name)
    out.mkdir(parents=True,exist_ok=False)
    build=ROOT/'build/noise-sweep';build.mkdir(parents=True,exist_ok=True)
    subprocess.run(['c++','-std=c++17','-O3','-fno-math-errno','-fPIC','-shared',str(ROOT/'benchmark/orbit_kernel.cpp'),'-o',str(build/'orbit-baseline.so')],check=True)
    env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    common=['--agama-path',str(library),'--forecast',str(ROOT/'forecast.json'),'--case','B','--seed','8302']
    variants=[('B-'+name,common+['--n',str(n)]+args) for name,args,n in [
        ('noisy',[],65536),('smooth',['--no-noise'],65536),
        ('unforced-noisy',['--no-bar'],65536),('unforced-smooth',['--no-bar','--no-noise'],65536),
        ('step-noisy',['--dt','.005'],16384),('step-smooth',['--dt','.005','--no-noise'],16384),
        ('cadence-noisy',['--noise-refine','2'],16384),('cadence-smooth',['--noise-refine','2','--no-noise'],16384)]]
    if a.smoke:
        variants=[('unforced-pilot',['--agama-path',str(library),'--pilot','--seed','8192','--n','4096','--no-bar'])]
    def run(item):
        name,args=item
        with (out/(name+'.log')).open('x') as log:
            subprocess.run(['nice','-n','10',sys.executable,str(ROOT/'scripts/noise_sweep/run_orbits.py'),'--out',str(out/name),*args],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=7200)
        d=json.loads((out/name/'result.json').read_text())
        return dict(case=name,local_pass=d['all_pass'],cpu_seconds=d['cpu_seconds'])
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        cases=list(pool.map(run,variants))
    if not a.smoke:
        subprocess.run([sys.executable,str(ROOT/'scripts/noise_sweep/analyze_transfer.py'),'--root',str(out),'--forecast',str(ROOT/'forecast.json'),'--case','B','--out',str(out/'analysis')],cwd=ROOT,env=env,check=True)
    (out/'reproduction.json').write_text(json.dumps(dict(cases=cases,smoke_only=a.smoke,source_sha256=sources),indent=2)+'\n')
    print(json.dumps(cases,indent=2))


if __name__=='__main__':main()
