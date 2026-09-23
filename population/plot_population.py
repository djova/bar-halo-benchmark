"""Figure from actual regenerated or explicitly archived population measurements."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
from pathlib import Path
import argparse,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p=argparse.ArgumentParser();p.add_argument('--analysis',type=Path,required=True)
    p.add_argument('--distribution',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();r=json.loads(a.analysis.read_text());d=json.loads(a.distribution.read_text())
    fig,axes=plt.subplots(1,2,figsize=(10,5.2),layout='constrained')
    colors={'gaussian':'#a96523','halo':'#1670a4','exponential':'#377858'}
    for ax,t in zip(axes,[10.,20.]):
        for si,s in enumerate([0.,.25]):
            for pi,(name,color) in enumerate(colors.items()):
                row=next(v for v in r['rows'] if v['s']==s and v['tau']==t and v['population']==name+'-40')
                estimate=row['integral_w_K_B'];y=si*4+pi
                ax.errorbar(estimate['mean'],y,xerr=[[estimate['mean']-estimate['ci95'][0]],[estimate['ci95'][1]-estimate['mean']]],fmt='o',capsize=3,color=color)
                independent=next(v for v in d['central'] if v['s']==s and v['tau']==t and v['population']==name+'-40')
                ax.plot(independent['distribution'],y+.23,'*',color=color,ms=9)
                if not independent.get('archived_distribution_refinement_qualification',False):ax.plot(independent['distribution'],y+.23,'x',color='red',ms=11)
                if not row['numerical_window_qualified']:ax.plot(estimate['mean'],y,'x',color='red',ms=10)
        ax.axvline(0,color='gray',lw=.8)
        ax.set(title=f'Saved duration T = {t:g}',xlabel='Noise-induced weighted bar transfer',yticks=[0,1,2,4,5,6],yticklabels=['Stationary · Gaussian','Stationary · Halo','Stationary · Exponential','Moving · Gaussian','Moving · Halo','Moving · Exponential'],ylim=(-.7,7.2))
    fig.suptitle('Changing the population at fixed central halo density',fontsize=13)
    fig.get_layout_engine().set(rect=(0,.12,1,.75))
    fig.text(.05,.025,'Dots: independent trajectory95%intervals. Stars: distribution/characteristic estimates.\nRed crosses: failed associated numerical/window checks. Fixed fast-action slice; not total halo torque.\nOther distribution refinements have separate qualification records; reproduction is not new physical evidence.',fontsize=8.5)
    fig.savefig(a.out,dpi=170)


if __name__=='__main__':main()
