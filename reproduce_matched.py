"""Reproduce both matched reduced-model signs from seeded inputs on one CPU."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent/'matched'

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True,type=Path)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    if hasattr(os,'nice'):os.nice(10)
    manifest=json.loads((ROOT/'source-manifest.json').read_text())
    for name,digest in manifest.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    reference=json.loads((ROOT/'reference.json').read_text())
    cpu=0.;start=time.monotonic();records=[]
    def run(name,module,args):
        nonlocal cpu
        with (a.out/(name+'.log')).open('w') as log:
            subprocess.run([sys.executable,str(ROOT/module),'--out',str(a.out/name),*args],
                           stdout=log,stderr=subprocess.STDOUT,check=True,timeout=7200)
        d=json.loads((a.out/name/'result.json').read_text())
        assert d['all_pass'],name
        cpu+=d['cpu_seconds'];return d
    common=['--slope','-0.004749321154862916','--end','20']
    impulse=lambda d:d['history'][-1]['bar_impulse']
    for name,s in [('stationary','0'),('moving','.25')]:
        params=common+['--s',s]
        noisy=run(name+'-noisy','benchmark/resonance.py',params+['--eta','.1','--nphi','256','--nj','4096'])
        if name=='stationary':
            smooth=run(name+'-smooth','benchmark/characteristics.py',params+['--nphi','512','--nj','8192'])
            batches=[run(f'paths-{seed}','scripts/noise_sweep/stationary_pairs.py',
                         ['--seed',str(seed),'--dt','.0125'])['mean'] for seed in range(8401,8409)]
        else:
            smooth=run(name+'-smooth','benchmark/characteristic_endpoint.py',
                       params+['--nphi','2048','--nj','32768','--chunk','8'])
            batches=[]
            for seed in range(8501,8509):
                args=params+['--method','trajectories','--n','524288','--dt','.0125','--seed',str(seed)]
                zero=run(f'paths-{seed}-eta0','benchmark/resonance.py',args+['--eta','0'])
                perturbed=run(f'paths-{seed}-eta01','benchmark/resonance.py',args+['--eta','.1'])
                batches.append(impulse(perturbed)-impulse(zero))
        contrast=impulse(noisy)-impulse(smooth)
        mean=float(np.mean(batches));se=float(np.std(batches,ddof=1)/np.sqrt(8))
        half=2.3646242515927844*se;ci=[mean-half,mean+half]
        ref=reference[name]
        errors=dict(distribution=abs(contrast-ref['distribution_contrast']),
                    batch=float(np.max(abs(np.array(batches)-ref['batches']))),
                    interval=float(np.max(abs(np.array(ci)-ref['ci95']))))
        assert max(errors.values())<1e-9,(name,errors)
        records.append(dict(name=name,s=float(s),eta=.1,T=20,distribution_contrast=contrast,
                            mean=mean,se=se,ci95=ci,batches=batches,reference_errors=errors))
    result=dict(records=records,scientific_cpu_seconds=cpu,wall_seconds=time.monotonic()-start,
                reference_values_reproduced=True,source_manifest=manifest,
                scope='Same-seed standalone reproduction, not an independent replication. '
                'Regenerates the matched positive-population estimates and independent sampling intervals; '
                'separate archived numerical refinements are not rerun by this command. '
                'No3D transfer, full-halo distribution or physical dark-matter claim.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
    for i,r in enumerate(records):
        color=['#b44f24','#126cb1'][i]
        ax.errorbar(r['mean'],i-.1,xerr=r['ci95'][1]-r['mean'],fmt='o',c=color,
                    capsize=4,label='Independent paths:95% interval' if i==0 else None)
        ax.plot(r['distribution_contrast'],i+.1,'*',color=color,ms=12,
                label='Distribution estimate' if i==0 else None)
    ax.axvline(0,color='grey',lw=1)
    ax.set(yticks=[0,1],yticklabels=['Stationary','Moving: s=.25'],ylim=(-.6,1.7),
           xlabel='Noise minus collisionless bar impulse, action units per tracer',
           title='Same population, noise strength and duration: T=20')
    ax.legend(fontsize=9);fig.savefig(a.out/'matched-response.png',dpi=160)
    print(json.dumps({k:v for k,v in result.items() if k!='source_manifest'},indent=2))

if __name__=='__main__':main()
