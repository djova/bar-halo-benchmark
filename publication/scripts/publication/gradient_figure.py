#!/usr/bin/env python3
"""Render a fixed recorded-kernel comparison. No dynamical calculation is run."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser=argparse.ArgumentParser()
parser.add_argument('--source',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
payload=args.source.read_bytes(); d=json.loads(payload)
x=np.asarray(d['action']); edge=np.asarray(d['cumulative_action']); dx=np.diff(edge)
assert len(x)==512 and len(edge)==513 and np.allclose(dx,dx[0])
rows={v['profile']:v for v in d['records'] if v['s']==.25 and v['tau']==10.}
k=next(v for v in d['kernels'] if v['s']==.25 and v['tau']==10.)
assert set(rows)=={'halo','gaussian','exponential'}
checks={}
for key,r in rows.items():
    signed=np.asarray(r['contribution']['mean'])*dx
    cumulative=np.asarray(r['cumulative']['mean'])
    assert np.max(np.abs(np.r_[0,np.cumsum(signed)]-cumulative))<1e-12
    assert abs(cumulative[-1]-r['estimate']['mean'])<1e-9
    checks[key]={'recorded_response':r['estimate']['mean'],'full_gradient_sum':float(signed.sum()),'inside_radius_4':float(signed[abs(x)<4].sum()),'outside_radius_4':float(signed[abs(x)>=4].sum()),'maximum_cumulative_residual':float(np.max(np.abs(np.r_[0,np.cumsum(signed)]-cumulative))),'pointwise_95_interval':r['estimate']['ci95']}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.labelsize':9,'axes.titlesize':9.2,'axes.titleweight':'normal','legend.fontsize':8.5,'xtick.labelsize':8,'ytick.labelsize':8,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42})
fig,axs=plt.subplots(2,2,figsize=(7.25,5.75),gridspec_kw={'hspace':.48,'wspace':.28})
colors={'halo':'#0072B2','gaussian':'#D55E00','exponential':'#009E73'}
labels={'halo':'Isochrone halo slice','gaussian':r'Gaussian $\sigma=8$','exponential':'Slope-matched exponential'}
styles={'halo':'-','gaussian':'-','exponential':(0,(2,2))}
widths={'halo':2.4,'gaussian':1.6,'exponential':1.6}
for ax in axs.ravel():
    ax.axhline(0,color='.65',lw=.55,zorder=0)
    ax.grid(axis='y',alpha=.16,lw=.5)
    ax.tick_params(direction='out',width=.6,length=3)
    for spine in ax.spines.values():spine.set_linewidth(.6)
for ax in (axs[0,0],axs[0,1],axs[1,0]):
    ax.set_xlim(-16,16);ax.set_xticks([-16,-8,0,8,16])
    ax.axvspan(-4,4,color='.88',alpha=.5,zorder=-1)
    ax.set_xlabel(r'Gradient coordinate $x$')
for key in ['halo','gaussian','exponential']:
    r=rows[key]; opts=dict(color=colors[key],lw=widths[key],ls=styles[key],label=labels[key])
    axs[0,0].plot(x,r['gradient'],**opts)
    c=np.asarray(r['contribution']['mean']); ci=np.asarray(r['contribution']['ci95'])
    axs[1,0].plot(x,c,**opts)
    axs[1,0].fill_between(x,ci[:,0],ci[:,1],color=colors[key],alpha=.10,lw=0)
    cum=np.asarray(r['cumulative']['mean']); ci=np.asarray(r['cumulative']['ci95'])
    axs[1,1].plot(edge,cum,**opts)
    axs[1,1].fill_between(edge,ci[:,0],ci[:,1],color=colors[key],alpha=.10,lw=0)
    axs[1,1].plot([40],[cum[-1]],marker='o' if key=='gaussian' else ('s' if key=='halo' else 'x'),markersize=4,color=colors[key],mew=1)
ci=np.asarray(k['ci95'])
axs[0,1].plot(x,k['mean'],color='#333333',lw=1.6)
axs[0,1].fill_between(x,ci[:,0],ci[:,1],color='#555555',alpha=.18,lw=0)
axs[0,0].set_title('(a) Population gradients',loc='left',pad=7)
axs[0,0].set_ylabel(r'Population gradient $w^{\prime}(x)$')
axs[0,0].set_ylim(-.085,.085)
axs[0,0].text(.03,.09,'Halo and exponential nearly coincide',transform=axs[0,0].transAxes,fontsize=7.3,color='#345c66')
axs[0,1].set_title('(b) Primitive response kernel',loc='left',pad=7)
axs[0,1].set_ylabel(r'Primitive response $Q_{\rm p}(x)$')
axs[1,0].set_title('(c) Signed contributions',loc='left',pad=7)
axs[1,0].set_ylabel(r'Signed integrand $-w^{\prime}(x)Q_{\rm p}(x)$')
axs[1,0].ticklabel_format(axis='y',style='sci',scilimits=(-2,-2),useMathText=True)
axs[1,1].set_title('(d) Cumulative response',loc='left',pad=7)
axs[1,1].set_ylabel(r'Cumulative gradient integral')
axs[1,1].set_xlim(-40,40);axs[1,1].set_xticks([-40,-20,0,20,40])
axs[1,1].set_xlabel(r'Gradient coordinate $x$ (full tapered window)')
axs[1,1].set_ylim(-.034,.0055)
axs[1,1].ticklabel_format(axis='y',style='sci',scilimits=(-2,-2),useMathText=True)
axs[1,1].annotate(r'Gaussian: $+0.001508$',xy=(40,checks['gaussian']['full_gradient_sum']),xytext=(7,.0032),textcoords='data',fontsize=7.5,color=colors['gaussian'])
axs[1,1].annotate(r'Halo: $-0.003901$',xy=(40,checks['halo']['full_gradient_sum']),xytext=(8,-.0102),textcoords='data',arrowprops={'arrowstyle':'-','color':colors['halo'],'lw':.6},fontsize=7.5,color=colors['halo'])
handles,legend_labels=axs[0,0].get_legend_handles_labels()
fig.legend(handles,legend_labels,loc='upper center',bbox_to_anchor=(.5,.995),ncol=3,frameon=False,handlelength=3,columnspacing=1.8)
fig.subplots_adjust(top=.885,bottom=.085,left=.10,right=.985)
fig.savefig(args.out/'population-gradient-explanation.png',dpi=220,facecolor='white')
fig.savefig(args.out/'population-gradient-explanation.svg',facecolor='white',metadata={'Date':None})
plt.close(fig)
caption='''Population curvature changes the balance of the response. The three initial populations have the same central density and slope and evolve with the same imposed bar and diffusion (s = 0.25, eta = 0.1, T = 10). (a) Recorded population gradients in the central action interval. (b) The common primitive kernel. (c) Signed gradient contributions, evaluated on the original fine cells and summed into the displayed cells. The shaded action strip marks |x| < 4. (d) Cumulative contributions across the complete population window, which tapers to zero at |x| = 40. The Gaussian's inner and outer contributions are -0.011058 and +0.012565, yielding a positive response; the halo gives -0.004835 and +0.000934, yielding a negative response. The exponential nearly coincides with the halo. These are contributions to the gradient integral, not literal cohorts of initial orbits. All quantities are dimensionless and conditional on the same fixed fast-action slice. Shaded curve bands are pointwise 95 per cent Student-t intervals across eight independent batches, without numerical-error expansion. Lines join recorded display cells; no trajectories or additional times are interpolated. The three central panels show |x| <= 16; panel (d) retains the complete physical window.'''
(args.out/'gradient-figure-caption.txt').write_text(caption+'\n')
receipt={'source':'web/data/population-response/publication.json','source_sha256':hashlib.sha256(payload).hexdigest(),'condition':{'s':.25,'eta':.1,'T':10.,'plateau':24,'cutoff':40},'data_origin':'Previously released coarsened primitive-kernel cells, population gradients and exact sums of fine-cell contributions; no simulation, fitting, smoothing or new numerical experiment.','checks':checks,'scope':d['display_scope'],'figure_sha256':{name:hashlib.sha256((args.out/name).read_bytes()).hexdigest() for name in ['population-gradient-explanation.png','population-gradient-explanation.svg']}}
(args.out/'gradient-figure-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'checks':checks,'source_sha256':receipt['source_sha256']},indent=2))
