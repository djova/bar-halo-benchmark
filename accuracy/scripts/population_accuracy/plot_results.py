"""Publication figures from completed records; never synthesize simulation frames."""
from common import ROOT, sha
import argparse
import json
import time
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cost',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    cpu=time.process_time()
    a.out.mkdir(parents=True,exist_ok=False)
    cost=json.loads(a.cost.read_text())
    original_path=ROOT/'results/population-response/validation-analysis-01/result.json'
    original=json.loads(original_path.read_text())
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    colors={'halo':'#176887','exponential':'#b97700','gaussian':'#a54667'}
    fig,axes=plt.subplots(1,2,figsize=(10.8,4.8),layout='constrained')
    names=['gaussian','halo','exponential']
    for ax,tau in zip(axes,[10.,20.]):
        rows=[next(r for r in original['rows'] if r['s']==.25 and r['tau']==tau and r['population']==name+'-40') for name in names]
        for i,(name,row) in enumerate(zip(names,rows)):
            r=row['integral_w_K_B'];mean=r['mean'];ci=r['ci95']
            ax.errorbar(i,mean*1000,yerr=np.array([[mean-ci[0]],[ci[1]-mean]])*1000,
                        fmt='o',ms=8,color=colors[name],capsize=4,label=name)
            ax.annotate(f'{mean*1000:+.3f}',(i,mean*1000),xytext=(0,11 if mean>=0 else -21),
                        textcoords='offset points',ha='center',fontsize=9,color=colors[name])
        ax.axhline(0,color='.55',lw=.8)
        ax.set_xticks(range(3),['Gaussian σ=8','Reference halo','Exponential'])
        ax.set_xlim(-.5,2.5);ax.margins(y=.35)
        ax.set_title(f'T = {tau:g} · '+('different signs' if tau==10 else 'different magnitudes'))
        ax.set_ylabel('Noise − smooth bar transfer  [×10⁻³]')
        ax.grid(axis='y',alpha=.18)
    fig.suptitle('The same central density and slope do not guarantee the same response',fontsize=13)
    fig.supxlabel('Reference-halo weighting in one fixed action slice · s=0.25, η=0.1 · pointwise 95% sampling intervals',fontsize=9)
    fig.savefig(a.out/'population-comparison.png',dpi=180,metadata={'Software':'Galaxy Bar scientific figure'})
    plt.close(fig)

    fig,axes=plt.subplots(1,2,figsize=(12,5.5),layout='constrained',gridspec_kw={'width_ratios':[1.15,1]})
    names=['halo','exponential','gaussian8','stress1','stress0.125','stress0.015625']
    labels=['Halo','Exp.','σ=8','σ=1','σ=⅛','σ=1/64']
    for s,style in [(0.,'--'),(.25,'-')]:
        for tau,color,offset in [(10.,'#176887',-.10),(20.,'#b97700',.10)]:
            rows=[next(r for r in cost['rows'] if r['s']==s and r['tau']==tau and r['population']==name) for name in names]
            y=np.array([r['cost_times_variance_ratio'] for r in rows]);ci=np.array([r['paired_batch_bootstrap_cost_ratio_interval'] for r in rows])
            x=np.arange(len(names))+offset+(s-.125)*.15
            axes[0].errorbar(x,y,yerr=np.maximum(0,np.stack([y-ci[:,0],ci[:,1]-y])),fmt='o',ms=4,
                             ls=style,lw=1.3,color=color,capsize=2,label=f's={s:g}, T={tau:g}')
    axes[0].set_yscale('log');axes[0].set_xticks(range(6),labels)
    axes[0].axhline(1,color='#a54667',lw=1)
    axes[0].axhspan(.5,1,color='#a54667',alpha=.07)
    axes[0].set_ylim(.7,1e5);axes[0].grid(axis='y',which='major',alpha=.2)
    axes[0].set_ylabel('(variance × CPU)raw / (variance × CPU)remainder')
    axes[0].set_title('The advantage vanishes for narrow weights')
    axes[0].legend(fontsize=9,ncol=2,loc='upper right')
    axes[0].text(.02,.04,'Above 1: remainder is more efficient\nBelow 1: raw is more efficient',transform=axes[0].transAxes,fontsize=9)
    for name,style,label in [('halo','-','Halo'),('stress0.125','--','Narrow σ=⅛')]:
        row=next(r for r in cost['rows'] if r['s']==.25 and r['tau']==20 and r['population']==name)
        for detail,color in zip(row['precision'],['#a54667','#176887']):
            unit=detail['measured_mean_accounted_batch_cpu_seconds']
            cpu_grid=np.geomspace(unit,unit*1e6,180)
            se=np.sqrt(detail['conditional_variance_per_batch']*unit/cpu_grid)
            axes[1].loglog(cpu_grid,se,ls=style,color=color,lw=1.4,label=label+' · '+detail['method'])
            axes[1].plot(sum(detail['measured_batch_cpu_seconds']),detail['measured_eight_batch_response']['se'],
                         marker='o',ms=5,color=color,mfc='white',mew=1.2)
    axes[1].set_xlabel('Accounted single-worker CPU [seconds]')
    axes[1].set_ylabel('Standard error of the transfer estimate')
    axes[1].set_title('Precision projections, not long timed runs')
    axes[1].grid(which='major',alpha=.2);axes[1].legend(fontsize=8.5)
    fig.suptitle('Identical paths and numerical weights: variance reduction has a measurable domain',fontsize=13)
    fig.supxlabel('Eight batches per sweep · intervals: paired batch bootstrap · right: lines assume independent fixed-allocation batches; circles are measured eight-batch estimates\nCosts include actual integration and each estimator’s setup/evaluation; both endpoints share the same T=20 integration workload.',fontsize=8.5)
    fig.savefig(a.out/'estimator-efficiency.png',dpi=180,metadata={'Software':'Galaxy Bar scientific figure'})
    plt.close(fig)
    result=dict(figures=['population-comparison.png','estimator-efficiency.png'],
        inputs={str(original_path.relative_to(ROOT)):sha(original_path),str(a.cost):sha(a.cost)},
        source_sha256=sha(__file__),cpu_seconds=time.process_time()-cpu,
        scope='Figures derived from complete archived population and matched-cost records. Precision curves are explicit independent-batch projections; they are not simulated or measured long-run histories.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
