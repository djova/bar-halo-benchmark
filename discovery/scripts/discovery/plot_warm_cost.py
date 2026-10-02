"""Plot recorded stellar specific-energy summaries; no physical computation."""
from pathlib import Path
import argparse
import json
import resource
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(data_path, output):
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    d = json.loads(data_path.read_text())
    bg, text = '#10202c', '#d8e4ed'
    plt.rcParams.update({'font.size': 13, 'text.color': text, 'axes.labelcolor': text,
                         'xtick.color': text, 'ytick.color': text, 'axes.edgecolor': '#657a89'})
    fig, ax = plt.subplots(figsize=(10.6, 6.2), facecolor=bg)
    ax.set_facecolor(bg)
    names = []
    for j, r in enumerate(d['figure']['rows']):
        for k, (name, source, color, marker) in enumerate([
                ('Whole stellar mass', r['whole'], '#80bfff', 'o'),
                (r'$R_c<0.25$ cohort', r['inner_guiding_Rc_lt_0_25'], '#ffd080', 'D')]):
            q = source['actual_forward'];y=3-2*j-k
            ax.errorbar(q['mean']*1e6,y,xerr=q['standard_error']*1e6,
                        fmt=marker,color=color,capsize=4,label=name if j==0 else None)
            ax.annotate(f"({q['mean']*1e6:.4g} ± {q['standard_error']*1e6:.3g}) × 10⁻⁶",
                        (q['mean']*1e6,y),xytext=((-10,12) if q['mean']*1e6>20 else (8,12)),ha=('right' if q['mean']*1e6>20 else 'left'),textcoords='offset points',fontsize=11)
            names.append(f"Carrier {int(r['frequency'])}\n{'Whole' if k==0 else 'Inner cohort'}")
    ax.set_yticks([3,2,1,0],names)
    ax.set_xlim(-.35,42.5);ax.set_ylim(-.45,3.65)
    ax.set_xticks([0,10,20,30,40]);ax.axvline(0,color='#93a8bc',lw=1)
    ax.grid(axis='x',ls=':',color='#405565')
    ax.set_xlabel(r'Specific-energy deposit per unit declared cohort mass ($10^{-6}GM_h/a_h$)',labelpad=12)
    ax.legend(loc='upper left',bbox_to_anchor=(0,1.16),ncol=2,facecolor=bg,labelcolor=text)
    fig.suptitle('A small inner cohort carries most stellar energy at a much larger specific cost',fontsize=15,y=.99)
    fig.text(.21,.04,'Actual forward estimates · empirical IID SE · same 4096 states, not replication\nGas amplitude 0.003 · pulse 80 Hernquist units · scalar energy, not measured velocity dispersion',fontsize=10)
    fig.subplots_adjust(left=.25,right=.96,top=.79,bottom=.22)
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=150,facecolor=bg,metadata={'Software':'Matplotlib'})
    plt.close(fig)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,default=Path(__file__).resolve().parents[2]/'data/warm-cost-v1.json')
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();main(a.data,a.out)
