"""Plot every prospective comparison; no selected population or endpoint."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p=argparse.ArgumentParser();p.add_argument('--analysis',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    data=json.loads(a.analysis.read_text())
    if len(data['rows'])!=24:raise ValueError('Complete comparison required')
    names=['gaussian12','gaussian20','quartic20'];labels=['Gaussian σ = 12','Gaussian σ = 20','Quartic scale 20']
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(2,2,figsize=(11,6.5),sharex=True,sharey=True)
    for si,s in enumerate([0.,.25]):
        for ti,t in enumerate([10.,20.]):
            ax=axes[si,ti];ax.axvspan(-1,1,color='#e6edf2');ax.axvline(0,color='#64748b',lw=.8)
            for ni,name in enumerate(names):
                for cutoff,offset,color,marker in [(40,-.13,'#1d668d','o'),(64,.13,'#a65027','s')]:
                    r=next(v for v in data['rows'] if v['s']==s and v['tau']==t and v['population']==name+'-'+str(cutoff))
                    allowance=r['frozen_accuracy_allowance'];d=r['independent_minus_predicted'];lo,hi=np.array(d['ci95'])/allowance;m=d['mean']/allowance
                    ax.errorbar(m,ni+offset,xerr=[[m-lo],[hi-m]],fmt=marker,color=color,capsize=3,ms=5,mfc=color if r['prospective_prediction_qualified'] else 'white',label=f'Window cutoff {cutoff}' if ni==0 else None)
                    if not r['prospective_prediction_qualified']:ax.annotate('not qualified',(m,ni+offset),xytext=(5,7),textcoords='offset points',fontsize=8,color='#9b1c1c')
            ax.set_title(f"{'Stationary' if s==0 else 'Moving s = 0.25'} · T = {t:g}")
            ax.set_yticks(range(3),labels);ax.set_ylim(2.55,-.55);ax.grid(axis='x',alpha=.15)
    axes[0,0].legend(fontsize=9,loc='lower left')
    for ax in axes[-1]:ax.set_xlabel('(Independent − predicted response) / declared allowance')
    fig.suptitle('Can the recorded kernel predict new initial populations?',y=.985,fontsize=15)
    fig.tight_layout(rect=(0,.09,1,.95))
    fig.text(.04,.055,'Bars: pointwise 95% sampling intervals. Shaded band: the accuracy criterion frozen before new-shape evolution.',fontsize=9)
    fig.text(.04,.024,'Filled markers also pass numerical and window checks. This is a local external-model test, not a 3D halo prediction.',fontsize=9)
    a.out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(a.out,dpi=180);plt.close(fig)
    print(a.out)

if __name__=='__main__':main()
