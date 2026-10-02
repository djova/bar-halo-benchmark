"""Recorded-operand scientific figures; no simulation or interpolation."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
data = json.loads((ROOT/'data/checks-v2.json').read_text())
out = ROOT/'figures'
out.mkdir(exist_ok=True)
plt.rcParams.update({'figure.facecolor':'#10202e','axes.facecolor':'#10202e',
                    'text.color':'#d8e4ed','axes.labelcolor':'#d8e4ed',
                    'xtick.color':'#d8e4ed','ytick.color':'#d8e4ed','axes.edgecolor':'#536477',
                    'font.size':10,'savefig.facecolor':'#10202e'})
colors = ['#80bfff','#ffd080','#7ad8bd']

w = data['warm_population']
fig, ax = plt.subplots(figsize=(7.5,3.7), constrained_layout=True)
values = [w['inner_guiding_mass']]+[r['paired']['inner_fraction'] for r in w['original_fine_dilution']]
errors = [0]+[r['paired']['fraction_delta_method_standard_error'] for r in w['original_fine_dilution']]
for i,(v,e) in enumerate(zip(values,errors)):
    ax.barh(2-i,100*v,height=.12,color=colors[i])
    ax.errorbar(100*v,2-i,xerr=100*e,color=colors[i],marker='o',capsize=4)
    digits=1 if i==1 else 2
    ax.text(1,2-i+.2,f'{100*v:.{digits}f}%'+(f' ± {100*e:.{digits}f} pp' if e else ''),fontsize=9)
ax.set(yticks=[2,1,0],yticklabels=['Target stellar mass','ω = 5 heating','ω = 8 heating'],
       xlim=(0,105),ylim=(-.4,2.55),xlabel='Mass fraction or signed sampled contribution ratio (%)',
       title='The inner guiding cohort carries nearly all sampled heating')
ax.grid(axis='x',alpha=.18)
fig.set_layout_engine(None);fig.subplots_adjust(left=.23,right=.98,bottom=.24,top=.85)
fig.text(.02,.04,'Rc < 0.25; N = 4096; empirical paired SE only. All-state numerical gate fails.',fontsize=8)
fig.savefig(out/'warm-cohort-v2.png',dpi=170);plt.close(fig)

e = data['echo_late']
labels=['L4 · phase16','L8 · phase16','L4 · phase32','L8 · phase32']
names=['coarse_E704_L4_eta16','cross_L8_eta16','cross_L4_eta32','fine_E704_L8_eta32']
rows=[next(r for r in e['rows'] if r['label']==name and r['time']==28) for name in names]
value=np.array([[r['mixed']['imag'][0],r['mixed']['imag'][1],r['mixed']['real'][2]] for r in rows])
q=np.array(e['local_scale_Q'])
lead=np.array([e['saved_signed_leading']['imag'][0][0],e['saved_signed_leading']['imag'][0][1],e['saved_signed_leading']['real'][0][2]])
fig,axes=plt.subplots(1,3,figsize=(9.5,3.7),sharey=True,constrained_layout=True)
for j,(ax,title) in enumerate(zip(axes,['Im potential','Im radial force','Re tangential force'])):
    ax.scatter(value[:,j]/q[j],np.arange(3,-1,-1),color=colors[j],zorder=3)
    ax.axvline(lead[j]/q[j],color=colors[j],linestyle='--',label='Leading prediction')
    ax.set(title=title,xlim=(-.3,1.15),xticks=[0,.5,1],ylim=(-.5,3.5),xlabel='Coefficient / fixed scale')
    ax.axvline(0,color='#afbdcc',alpha=.5,linewidth=1)
    ax.grid(axis='x',alpha=.18)
axes[0].set(yticks=[3,2,1,0],yticklabels=labels)
fig.suptitle('Time-28 spatial fields depend on angular-momentum quadrature',fontsize=12)
fig.set_layout_engine(None);fig.subplots_adjust(left=.17,right=.98,bottom=.24,top=.78,wspace=.16)
fig.text(.02,.04,'Recorded grids; dashed = leading model. All original 5% coarse/fine gates fail; no convergence beyond L8/phase32.',fontsize=8)
fig.savefig(out/'echo-cross-v2.png',dpi=170);plt.close(fig)

f=data['twin_forecast']
fig,ax=plt.subplots(figsize=(7.5,3.7),constrained_layout=True)
for i,r in enumerate(f['qualifications']):
    c=colors[i]
    ax.errorbar(r['forecast']/1e-10,2-i,xerr=r['combined_numerical_proxy']/1e-10,
                fmt='o',color=c,mfc=c if r['sign_numerically_qualified'] else '#10202e',capsize=4)
    ax.text(-.3,2-i+.22,'Small numerical proxy; driven test pending' if r['sign_numerically_qualified'] else 'Tail unresolved; numerical sign unqualified',fontsize=9)
ax.set(yticks=[2,1,0],yticklabels=['p = 4','p = 6','p = 8'],xlim=(-.4,3),ylim=(-.4,2.55),
       xlabel=r'Forecast $\Delta L_{z,+}-\Delta L_{z,-}$ ($10^{-10}$ reference action units)',title='A sealed weak-bar forecast; not a driven response')
ax.axvline(0,color='#536477');ax.grid(axis='x',alpha=.18)
fig.set_layout_engine(None);fig.subplots_adjust(left=.12,right=.98,bottom=.24,top=.85)
fig.text(.02,.04,'ε = 10⁻⁴, ramp = 10, T = 40 isochrone units, common mass 1. Bars show numerical proxies, not confidence.',fontsize=8)
fig.savefig(out/'twins-forecast-v2.png',dpi=170);plt.close(fig)
