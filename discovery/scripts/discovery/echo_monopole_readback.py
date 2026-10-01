"""Frozen-window amplitude, timing, memory and dynamical readout audit."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse, datetime, hashlib, json, time
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def window(t,y,tau,factor,parity):
    width=tau/4;center=factor*tau
    if t.min()>center-2*width or t.max()<center+2*width:return None
    dt=np.gradient(t);x=(t-center)/width
    weight=np.exp(-x*x/2)*dt*(abs(x)<=2)
    if parity=='odd':weight*=x
    denominator=np.sum(abs(weight))
    return float(np.sum(weight*y)/denominator)

def read(path):
    receipt=json.loads((path/'result.json').read_text());raw=np.load(path/'traces.npz')
    return path,receipt,raw

def values(raw,label):
    array=raw[label]
    return dict(potential=array[:,3],radial_force=array[:,4],enclosed_mass=array[:,5],
                potential_difference=array[:,0]-array[:,3])

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path)
    p.add_argument('--predictions',type=Path,nargs='*',default=[]);p.add_argument('runs',type=Path,nargs='+');a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False);(a.out/'source.py').write_bytes(Path(__file__).read_bytes())
    start,cpu=time.monotonic(),time.process_time();rows=[];datasets=[read(path) for path in a.runs]
    predictions=[]
    for path in a.predictions:
        receipt=json.loads((path/'result.json').read_text());raw=np.load(path/'response.npz')
        predictions.append((path,receipt,raw))
    fig,axes=plt.subplots(2,2,figsize=(11,8));separation,sepaxes=plt.subplots(2,1,figsize=(9,7))
    primary_stats={}
    for path,r,d in datasets:
        c=r['config'];t=d['t'];tau=c['tau'];amp=c['amplitude'];v=values(d,'eulerian_mixed');erased=values(d,'memory_erased_mixed')
        stats={};normalstats={}
        for observable,y in v.items():
            stats[observable]={};normalstats[observable]={}
            for factor in (2,3):
                for parity in ('even','odd'):
                    key=f'{factor}tau_{parity}';s=window(t,y,tau,factor,parity);e=window(t,erased[observable],tau,factor,parity)
                    stats[observable][key]=dict(original=s,memory_erased=e,
                                               erased_over_original=abs(e/s) if s not in (None,0) else None)
                    normalstats[observable][key]=s/amp**2 if s is not None else None
        single=d['eulerian_A']-d['eulerian_0'];relaxation={}
        for j,name in [(3,'potential'),(4,'radial_force'),(5,'enclosed_mass')]:
            early=(t>=1)&(t<=tau/3);late=(t>=.75*tau)&(t<=tau)
            rms_early=float(np.sqrt(np.mean(single[early,j]**2)));rms_late=float(np.sqrt(np.mean(single[late,j]**2)))
            relaxation[name]=dict(early_RMS=rms_early,preB_RMS=rms_late,preB_over_early=rms_late/rms_early)
        row=dict(run=str(path),config=c,raw_sha256=digest(path/'traces.npz'),
                 statistics=stats,normalized_statistics=normalstats,first_pulse_relaxation=relaxation,
                 absolute_initial_mass=r['results']['eulerian']['initial_mass'],
                 numerical_audits=r['results']['eulerian'])
        rows.append(row)
        xx=t-2*tau;name=f'tau={tau:g}, a={amp:g}'
        if tau==16:
            axes[0,0].plot(xx,v['potential']/amp**2,label=name,lw=1)
            axes[0,1].plot(xx,v['radial_force']/amp**2,label=name,lw=1)
            if amp==.002:
                axes[1,0].plot(xx,v['potential']/amp**2,label='Original')
                axes[1,0].plot(xx,erased['potential']/amp**2,label='Action-marginal memory erase')
                axes[1,1].plot(t,single[:,4],label='A-only radial force')
                axes[1,1].axvline(tau,color='black',ls=':',lw=.8)
        if amp==.002:
            sepaxes[0].plot(xx,v['potential']/amp**2,label=name)
            sepaxes[1].plot(xx,v['radial_force']/amp**2,label=name)
        if tau==16:primary_stats[amp]=normalstats
    prediction_comparisons=[]
    for path,r,d in predictions:
        c=r['config'];tau=c['tau'];observable=c.get('observable','potential')
        if observable not in ('potential','radial_force'):continue
        j=0 if observable=='potential' else 1
        if tau==16:axes[0,j].plot(d['t']-2*tau,d['total'].real,'k--',lw=.8,label='Independent harmonic prediction')
        sepaxes[j].plot(d['t']-2*tau,d['total'].real,'--',lw=.8,label=f'Prediction tau={tau:g}')
        for run,rr,dd in datasets:
            cc=rr['config']
            if cc['tau']!=tau:continue
            keep=(dd['t']>=1.5*tau)&(dd['t']<=2.5*tau)
            common=dd['t'][keep];indices=[np.flatnonzero(d['t']==t)[0] for t in common]
            exact=values(dd,'eulerian_mixed')[observable][keep];pred=d['total'][indices].real*cc['amplitude']**2
            scale=float(np.max(abs(exact)));difference=float(np.max(abs(exact-pred)))
            prediction_comparisons.append(dict(prediction=str(path),run=str(run),observable=observable,
                window=[1.5*tau,2.5*tau],maximum_exact_amplitude=scale,maximum_prediction_difference=difference,
                difference_over_peak=difference/scale if scale else None))
    scaling=[]
    if .002 in primary_stats:
        for amp,stats in sorted(primary_stats.items()):
            for observable in ('potential','radial_force'):
                for key in ('2tau_even','2tau_odd'):
                    base=primary_stats[.002][observable][key];value=stats[observable][key]
                    scaling.append(dict(amplitude=amp,observable=observable,statistic=key,
                                        normalized=value,reference_normalized=base,
                                        fractional_difference=abs(value/base-1) if base else None))
    for ax in axes.ravel():ax.legend(fontsize=8);ax.grid(alpha=.15)
    for ax in [axes[0,0],axes[0,1],axes[1,0]]:
        ax.axvline(0,color='black',ls=':',lw=.8);ax.set_xlim(-8,8);ax.set_xlabel('t - 2 tau')
    axes[0,0].set_ylabel('R=1 mixed potential / a^2');axes[0,1].set_ylabel('R=1 mixed radial force / a^2')
    axes[1,0].set_ylabel('Mixed potential / a^2');axes[1,1].set_xlabel('t');axes[1,1].set_ylabel('A-only force, absolute halo units')
    for ax in sepaxes:ax.axvline(0,color='black',ls=':',lw=.8);ax.set_xlim(-12,12);ax.set_xlabel('t - 2 tau');ax.legend(fontsize=8);ax.grid(alpha=.15)
    sepaxes[0].set_ylabel('Mixed potential / a^2');sepaxes[1].set_ylabel('Mixed radial force / a^2')
    fig.tight_layout();separation.tight_layout()
    for ext in ('png','pdf'):
        fig.savefig(a.out/f'radial-controls.{ext}',dpi=160);separation.savefig(a.out/f'radial-separation.{ext}',dpi=160)
    result=dict(pid=os.getpid(),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),rows=rows,
                amplitude_scaling=scaling,prediction_comparisons=prediction_comparisons,source_sha256=digest(__file__),
                cpu_seconds=time.process_time()-cpu,process_cpu_seconds=time.process_time(),wall_seconds=time.monotonic()-start,
                scope='Frozen first2tau controls of selected-halo gravitational readout. No full-halo, self-gravity, finite-duration pulse or stellar validation. Empty3tau statistics mean the full frozen window was not sampled.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'COMPLETE').write_text('Fixed control readback complete.\n')
    print(json.dumps(dict(amplitude_scaling=scaling,prediction_comparisons=prediction_comparisons),indent=2))

if __name__=='__main__':main()
