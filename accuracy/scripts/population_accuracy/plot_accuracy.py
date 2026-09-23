"""Central prospective figure: every candidate, endpoint and physical window."""
from common import sha
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--analysis',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    result=json.loads(a.analysis.read_text())
    if len(result['rows'])!=24:
        raise ValueError('Complete family required')
    names=['exponential','gaussian8','gaussian32','gaussian128','gaussian512']
    labels=['Exponential','Gaussian 8','Gaussian 32','Gaussian 128','Gaussian 512']
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,2,figsize=(11,7.6),sharex=True,sharey=True)
    values=[]
    for ax,(tau,cut) in zip(axes.ravel(),[(10.,40),(20.,40),(10.,64),(20.,64)]):
        ax.axvspan(1e-5,1,color='#e4f0e6',zorder=0)
        ax.axvline(1,color='#4f7960',ls='--',lw=1)
        for i,name in enumerate(names):
            row=next(r for r in result['rows'] if (r['tau'],r['cutoff'],r['population'])==(tau,cut,name))
            f=row['forecast'];target=f['five_percent_absolute_target']
            if target<=0:
                raise ValueError('Percentage scale undefined; use absolute errors for this result')
            predicted=f['combined_response_allowance']/target
            actual=abs(row['forecast_minus_independent_halo'])/target
            numerical=row['independent_halo']['numerical_proxy']/target
            values.extend([predicted,actual+numerical])
            ax.plot(predicted,i-.13,'o',mfc='white',mec='#a06118',ms=7,
                label='Frozen full allowance' if i==0 else None)
            ax.errorbar(actual,i+.13,xerr=[[min(actual,numerical)],[numerical]],fmt='x',
                color='#23659a',capsize=3,ms=6,label='Independent discrepancy ± numerical proxy' if i==0 else None)
        ax.set_xscale('log');ax.set_title(f'T = {tau:g}, physical cutoff = {cut}')
        ax.set_yticks(range(len(names)),labels);ax.set_ylim(len(names)-.5,-.5);ax.grid(axis='x',alpha=.16)
        ax.set_xlabel('Absolute error / frozen 5% target')
    axes[0,0].set_xlim(1e-3,max(10,max(values)*1.3))
    fig.suptitle('Which population approximations fit a predeclared error budget?\nNew sweep s = 0.5, imposed noise η = 0.1',fontsize=15,y=.98)
    handles,legend=axes[0,0].get_legend_handles_labels()
    fig.legend(handles,legend,loc='lower center',bbox_to_anchor=(.5,.025),ncol=2,frameon=False)
    fig.text(.5,.008,'20 correlated candidate comparisons; one conditional action slice. Refinement changes are practical proxies, not rigorous error bounds.',ha='center',fontsize=8)
    fig.tight_layout(rect=(0,.085,1,.915))
    a.out.mkdir(parents=True,exist_ok=False)
    fig.savefig(a.out/'population-accuracy.png',dpi=180)
    fig.savefig(a.out/'population-accuracy.pdf')
    (a.out/'manifest.json').write_text(json.dumps(dict(analysis_sha256=sha(a.analysis),
        source_sha256=sha(__file__),all_candidates=20,scope='All frozen candidates, times and physical windows; halo self-references remain in the numeric table. Plotted discrepancy is the approximate-kernel forecast minus independently evolved halo, not the intrinsic population error.'),indent=2)+'\n')
    plt.close(fig)


if __name__=='__main__':
    main()
