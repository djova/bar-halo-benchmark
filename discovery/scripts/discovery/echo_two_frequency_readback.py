"""Inspect fixed-date harmonic refinements and the separate relaxation screen."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import argparse,datetime,json,time
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from echo_halo import digest,write

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--first',type=Path,required=True);p.add_argument('--first-comparison',type=Path,action='append',default=[])
    p.add_argument('runs',type=Path,nargs='+');a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False);(a.out/'source.py').write_bytes(Path(__file__).read_bytes())
    start,cpu=time.monotonic(),time.process_time();datasets=[]
    for path in a.runs:
        r=json.loads((path/'result.json').read_text());d=np.load(path/'response.npz');datasets.append((path,r,d))
    basepath,base,bd=datasets[-1];t=bd['t'];tau=base['config']['tau'];keep=(t>=1.5*tau)&(t<=2.5*tau)
    comparisons=[];fig,axes=plt.subplots(3,2,figsize=(11,11));refinement,refaxes=plt.subplots(3,1,figsize=(9,9));amplitudes={}
    firstdisplay=np.load(a.first/'response.npz');displaykeep=firstdisplay['t']<=2.5*tau;displaytime=firstdisplay['t'][displaykeep]
    for row,observable in enumerate(('potential','radial_force','tangential_force')):
        component='real' if observable=='tangential_force' else 'imag'
        selected=lambda z:z.real if component=='real' else z.imag
        for family in ('total','echo2_radial_only','echo2_apsidal_only','echo2_two_frequency','nonrefocusing'):
            key=observable+'_'+family;y=bd[key]
            axes[row,0].plot(t/tau,selected(y),'o-',ms=3,lw=.9,label=family.replace('echo2_',''))
            peak=float(np.max(abs(y[keep])));amplitudes[key]=dict(coefficient_peak=peak,
                maximum_physical_azimuthal_amplitude=2*peak,
                original_complex_values=[[float(z.real),float(z.imag)] for z in y])
        for path,r,d in datasets:
            assert np.array_equal(d['t'],t)
            label=f'E{r["config"]["ne"]} L{r["config"]["nL"]} n{r["config"]["nmax"]} {r["config"].get("formulation","ibp")}'
            key=observable+'_echo2_two_frequency';refaxes[row].plot(t/tau,selected(d[key]),'o-',ms=3,label=label,lw=.9)
            for family in ('total','echo2_two_frequency'):
                key=observable+'_'+family;scale=float(np.max(abs(bd[key][keep])))
                difference=float(np.max(abs(d[key][keep]-bd[key][keep])))
                comparisons.append(dict(reference=str(basepath),alternative=str(path),observable=observable,family=family,
                    frozen_interval=[1.5*tau,2.5*tau],maximum_complex_difference=difference,difference_over_reference_peak=difference/scale))
        for part in ('real','imag'):
            values=getattr(firstdisplay[observable+'_first_A'][displaykeep],part)
            axes[row,1].plot(displaytime/tau,values,'.',label='first A '+part+'; refined dates',ms=3)
        axes[row,0].set_ylabel(observable+' coefficient');refaxes[row].set_ylabel(observable+' two-frequency')
    for ax in axes.ravel():ax.set_xlabel('t / pulse separation');ax.axvline(1,color='black',ls=':',lw=.6);ax.axvline(2,color='black',ls=':',lw=.6);ax.legend(fontsize=7)
    for ax in refaxes:ax.set_xlabel('t / pulse separation');ax.legend(fontsize=7)
    fig.tight_layout();fig.savefig(a.out/'two-frequency-channels.png',dpi=160);fig.savefig(a.out/'two-frequency-channels.pdf')
    refinement.tight_layout();refinement.savefig(a.out/'two-frequency-refinement.png',dpi=160);refinement.savefig(a.out/'two-frequency-refinement.pdf')
    relaxation=[];first_refinements=[]
    for path in [a.first]+a.first_comparison:
        first=np.load(path/'response.npz');ft=first['t'];early=(ft>=0)&(ft<=8);rows=[]
        assert ft[early][0]==0 and ft[early][-1]==8
        for separation in (16,32,48,64):
            late=(ft>=.75*separation)&(ft<=separation)
            assert ft[late][0]==.75*separation and ft[late][-1]==separation
            entry=dict(separation=separation,early_interval=[0.,8.],late_interval=[.75*separation,separation],early_dates=ft[early].tolist(),late_dates=ft[late].tolist(),observables={})
            for observable in ('potential','radial_force','tangential_force'):
                v=first[observable+'_first_A'];re=float(np.sqrt(np.trapz(abs(v[early])**2,ft[early])/8))
                rl=float(np.sqrt(np.trapz(abs(v[late])**2,ft[late])/(.25*separation)))
                entry['observables'][observable]=dict(early_RMS=re,preB_RMS=rl,preB_over_early=rl/re)
            rows.append(entry)
        if path==a.first:relaxation=rows
        first_refinements.append(dict(run=str(path),raw_sha256=digest(path/'response.npz'),time_integrated_RMS=rows))
    vc2=1/(np.sqrt(1.25)*(.5+np.sqrt(1.25))**2)
    usefulness={obs:amplitudes[obs+'_total']['maximum_physical_azimuthal_amplitude']/vc2 for obs in ('radial_force','tangential_force')}
    result=dict(pid=os.getpid(),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_sha256=digest(__file__),
        source_runs=[dict(path=str(path),raw_sha256=digest(path/'response.npz'),config=r['config']) for path,r,d in datasets],
        first_pulse_run=str(a.first),first_raw_sha256=digest(a.first/'response.npz'),amplitudes=amplitudes,comparisons=comparisons,
        first_pulse_relaxation=relaxation,first_pulse_refinements=first_refinements,maximum_physical_force_over_reference_background=usefulness,
        phase_convention='Full signed complex coefficients retained. Potential/radial force are imaginary for Bphi=pi/8; tangential force real. Physical m2 field adds complex conjugate, giving twice the coefficient amplitude.',
        scope='Fixed-date leading mathematical predictions and convergence. Longer-separation A-only relaxation screen is not a later echo observation. No finite-amplitude/memory/stellar validation.',
        cpu_seconds=time.process_time()-cpu,process_cpu_seconds=time.process_time(),wall_seconds=time.monotonic()-start)
    write(a.out/'result.json',result);(a.out/'COMPLETE').write_text('Prediction readback complete; not finite-amplitude halo-echo confirmation.\n')
    compact=[dict(separation=row['separation'],ratios={key:value['preB_over_early'] for key,value in row['observables'].items()}) for row in relaxation]
    print(json.dumps(dict(comparison_count=len(comparisons),relaxation=compact,usefulness=usefulness),indent=2))

if __name__=='__main__':main()
