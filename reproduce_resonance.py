"""Regenerate two central response measurements and independent sampling checks."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import argparse,json,subprocess,sys,time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 if hasattr(os,'nice'):os.nice(10)
 reference=json.loads((ROOT/'reference-resonance.json').read_text());records=[];cpu=0.;start=time.monotonic()
 def run(name,module,args):
  nonlocal cpu
  target=a.out/name
  with (a.out/(name+'.log')).open('w') as log:subprocess.run([sys.executable,str(ROOT/module),'--out',str(target),*args],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=600)
  d=json.loads((target/'result.json').read_text());assert d['all_pass'];cpu+=d['cpu_seconds'];return d['history'][-1]['bar_impulse']
 for sweep in (0.,.4):
  common=['--s',str(sweep)];b=run(f's{sweep}-collisionless','characteristics.py',common+['--nphi','256','--nj','4096']);f=run(f's{sweep}-noisy','resonance.py',common+['--eta','.1']);batches=[]
  for seed in range(8201,8209):
   c=common+['--method','trajectories','--seed',str(seed)];zero=run(f's{sweep}-{seed}-eta0','resonance.py',c+['--eta','0']);noisy=run(f's{sweep}-{seed}-eta01','resonance.py',c+['--eta','.1']);batches.append(noisy-zero)
  mean=float(np.mean(batches));se=float(np.std(batches,ddof=1)/np.sqrt(8));ref=next(c for c in reference['independent_checks'] if c['s']==sweep)
  assert abs(f-b-ref['distribution_contrast'])<1e-9 and np.max(abs(np.array(batches)-ref['batch_contrasts']))<1e-9
  records.append(dict(s=sweep,eta=.1,distribution_contrast=f-b,batches=batches,mean=mean,se=se,ci95=[mean-2.364624251*se,mean+2.364624251*se],archived_strict_baseline_qualified=ref['strict_baseline_qualified']))
 result=dict(records=records,scientific_cpu_seconds=cpu,wall_seconds=time.monotonic()-start,reference_values_reproduced=True,scope='Finite Gaussian tracer population. This command reruns central measurements and independent stochastic paths; archived quadrature certification comes from separate refinements, not rerun here. The s=.4 collisionless reference missed its strict tolerance. No full-halo or SIDM claim.')
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');fig,ax=plt.subplots(figsize=(8,3.8),layout='constrained')
 for i,c in enumerate(records):
  ax.errorbar(c['mean'],i,xerr=c['ci95'][1]-c['mean'],fmt='o',c='#275b9b',label='Independent stochastic paths:95% sampling interval' if i==0 else None);ax.scatter(c['distribution_contrast'],i+.14,marker='s',color='#b34b25',label='Distribution estimate' if i==0 else None)
 ax.axvline(0,c='grey',lw=1);ax.set(yticks=range(2),yticklabels=['Stationary; T=25.13','Sweeping s=.4; T=20'],xlabel='Noise minus collisionless bar impulse, action units per tracer',title='Reproduced finite-time response at imposed diffusion η=.1');ax.legend(fontsize=8);fig.text(.1,-.06,'The moving collisionless reference misses its strict archived quadrature tolerance.\nDifferent rows have different elapsed times. These are selected tracer populations.',fontsize=9);fig.savefig(a.out/'response.png',dpi=160,bbox_inches='tight');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
