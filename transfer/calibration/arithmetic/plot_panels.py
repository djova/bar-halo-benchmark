"""Readable individual panels from the unchanged arithmetic comparison."""
import argparse
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    p.add_argument('--analysis',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    paths=[a.root/name/'result.json' for name in ['original','rebuilt']]
    original,rebuilt=[json.loads(p.read_text()) for p in paths];data=json.loads(a.analysis.read_text())
    assert {p.parent.name:sha(p) for p in paths}==data['input_sha256']
    a.out.mkdir(parents=True,exist_ok=False)
    plt.rcParams.update({'font.size':13,'axes.labelsize':13,'xtick.labelsize':13,'ytick.labelsize':13})
    fig,ax=plt.subplots(figsize=(4.1,3.8),layout='constrained')
    for label,color in [('A','#135c91'),('B','#bf4d28')]:
        pairs=[(x,y) for x,y in zip(original['rows'],rebuilt['rows']) if x['case']==label and x['group']=='scan' and x['h']==1e-5]
        xs=[x['Js'] for x,y in pairs]
        ax.plot(xs,[(y['ordinary_slope']-x['ordinary_slope'])*1e9 for x,y in pairs],color=color,label=label,lw=1.6)
        ax.scatter(xs,[(y['high_precision_same_inputs']-x['high_precision_same_inputs'])*1e9 for x,y in pairs],color=color,marker='x',s=12)
    ax.set(xlabel='Original slow action Js',ylabel='Slope difference (×10⁻⁹)',xticks=[.22,.25,.28])
    ax.axhline(0,color='.6',lw=.7);ax.legend(title='Orbit',fontsize=13,title_fontsize=13)
    fig.savefig(a.out/'calibration-action-scan.png',dpi=180);plt.close(fig)
    fig,ax=plt.subplots(figsize=(4.1,3.8),layout='constrained')
    rows=data['rows'];hs=[r['h'] for r in rows]
    ax.loglog(hs,[r['maximum_cross_build_slope_difference'] for r in rows],'o-',label='Total')
    ax.loglog(hs,[r['maximum_cross_build_precise_log_difference'] for r in rows],'x--',label='50-digit logs')
    ax.loglog(hs,[r['maximum_differential_log_arithmetic_error'] for r in rows],'s-',label='Log arithmetic')
    ax.set_xticks(hs,['1','2','4','8']);ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set(xlabel='Offset h in Js (×10⁻⁵)',ylabel='Maximum difference (log scale)')
    ax.grid(alpha=.2);ax.legend(fontsize=12,loc='center right')
    fig.savefig(a.out/'calibration-offset-check.png',dpi=180);plt.close(fig)
    result=dict(input_sha256={p.parent.name:sha(p) for p in paths},analysis_sha256=sha(a.analysis),
                source_sha256=sha(Path(__file__)),files={p.name:sha(p) for p in a.out.glob('*.png')},
                scope='Individual mobile-readable panels of the unchanged recorded comparison; no new evaluation or inference.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
