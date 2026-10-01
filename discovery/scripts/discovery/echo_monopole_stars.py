"""Linear diagnostic of the isolated, annular mixed halo force.

This is a forced stable oscillator, not a stellar population simulation.
The external pulses would act directly on stars in a physical experiment.
"""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import argparse, datetime, json, time
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator, CubicSpline
from scipy.integrate import solve_ivp, quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from echo_monopole import digest, bound_cost, write

def circular(R):
    ss=np.sqrt(.25+R*R)
    vc2=R*R/(ss*(.5+ss)**2)
    kappa2=vc2/R**2*(4-R*R/ss**2-2*R*R/(ss*(.5+ss)))
    binding=1/(.5+ss)-.5*vc2
    return np.sqrt(vc2),np.sqrt(kappa2),binding

def measure(path):
    receipt=json.loads((path/'result.json').read_text());data=np.load(path/'traces.npz');c=receipt['config']
    mask=(data['t']>=1.5*c['tau'])&(data['t']<=2.5*c['tau'])
    t=data['t'][mask];g=data['eulerian_mixed'][mask,4]
    assert t[0]==1.5*c['tau'] and t[-1]==2.5*c['tau']
    vc,kappa,binding=circular(1.)
    interpolation=[];trajectories={}
    for label,field in [('PCHIP',PchipInterpolator(t,g)),('cubic',CubicSpline(t,g))]:
        impulse=quad(lambda u:abs(float(field(u))),t[0],t[-1],points=t,epsabs=1e-13,limit=300)[0]
        def rhs(u,y):return [y[1],float(field(u))-kappa*kappa*y[0]]
        evaltime=np.linspace(t[0],t[-1],1601)
        sol=solve_ivp(rhs,(t[0],t[-1]),[0.,0.],method='DOP853',rtol=2e-10,atol=2e-14,max_step=.05,t_eval=evaltime)
        assert sol.success
        reference_x=quad(lambda u:float(field(u))*np.sin(kappa*(t[-1]-u))/kappa,t[0],t[-1],points=t,epsabs=1e-14,limit=300)[0]
        reference_v=quad(lambda u:float(field(u))*np.cos(kappa*(t[-1]-u)),t[0],t[-1],points=t,epsabs=1e-14,limit=300)[0]
        final_free_velocity=np.hypot(sol.y[1,-1],kappa*sol.y[0,-1])
        interpolation.append(dict(kind=label,absolute_force_integral=impulse,
            absolute_force_integral_over_vc=impulse/vc,
            max_driven_radial_velocity=float(np.max(abs(sol.y[1]))),
            maximum_driven_or_subsequent_free_velocity=float(max(np.max(abs(sol.y[1])),final_free_velocity)),
            max_radial_displacement=float(np.max(abs(sol.y[0]))),
            final_free_velocity_amplitude=float(final_free_velocity),
            independent_Green_function_final_state_difference=float(max(abs(sol.y[0,-1]-reference_x),abs(sol.y[1,-1]-reference_v))),
            velocity_bound_if_vc_200kms=impulse/vc*200,
            actual_velocity_if_vc_200kms=float(max(np.max(abs(sol.y[1])),final_free_velocity)/vc*200)))
        trajectories[label]=dict(t=evaltime,x=sol.y[0],v=sol.y[1])
    amplitude=c['amplitude'];maximum_A_kick=2*amplitude/(3*np.sqrt(3)*.5**2)
    rmax=.5/np.sqrt(2);vcmax,_,_=circular(rmax)
    atR1=amplitude/(1+.25)**1.5
    field_peak=float(np.max(abs(g)))
    result=dict(run=str(path),source_raw_sha256=digest(path/'traces.npz'),amplitude=amplitude,tau=c['tau'],
        interval=[float(t[0]),float(t[-1])],background_vc_R1=float(vc),kappa_R1=float(kappa),
        kappa_vs_independent_isochrone_frequency_error=float(abs(kappa-(2*binding)**1.5)),
        maximum_sampled_mixed_force=field_peak,force_peak_over_background=field_peak/vc**2,
        A_maximum_velocity_impulse=maximum_A_kick,A_maximum_kick_over_local_vc=maximum_A_kick/vcmax,
        A_R1_impulse_over_local_vc=atR1/vc,
        two_pulse_global_binding_change_bound=bound_cost(amplitude,.5)+bound_cost(amplitude,1.5),
        possible_mass_fraction_for_duration_0p2=amplitude/.2,
        interpolants=interpolation,
        scope='Isolated annular-force linear epicycle and absolute-force integral bounds for specified interpolated fields. Direct stellar kicks, spatial frequency spread, disk self-gravity and actual gas/encounter histories are not simulated.')
    return result,trajectories

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('runs',nargs='+',type=Path);a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False);(a.out/'source.py').write_bytes(Path(__file__).read_bytes())
    start,cpu=time.monotonic(),time.process_time();rows=[];raw={};fig,axes=plt.subplots(2,1,figsize=(9,7))
    for index,path in enumerate(a.runs):
        row,traces=measure(path);rows.append(row)
        for label,trace in traces.items():
            for name,values in trace.items():raw[f'run{index}_{label}_{name}']=values
        trace=traces['PCHIP'];name=f'a={row["amplitude"]:g}, tau={row["tau"]:g}'
        axes[0].plot(trace['t']-2*row['tau'],trace['v']/row['background_vc_R1'],label=name)
        axes[1].plot(trace['t']-2*row['tau'],trace['x'],label=name)
    for ax in axes:ax.set_xlabel('t - 2 tau');ax.legend(fontsize=8);ax.grid(alpha=.15)
    axes[0].set_ylabel('Diagnostic radial velocity / circular speed');axes[1].set_ylabel('Diagnostic radial displacement / R')
    fig.tight_layout();fig.savefig(a.out/'linear-readout.png',dpi=160);fig.savefig(a.out/'linear-readout.pdf')
    np.savez_compressed(a.out/'oscillator.npz',**raw)
    result=dict(pid=os.getpid(),started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_sha256=digest(__file__),
        cpu_seconds=time.process_time()-cpu,process_cpu_seconds=time.process_time(),
        wall_seconds=time.monotonic()-start,rows=rows,raw_sha256=digest(a.out/'oscillator.npz'))
    write(a.out/'result.json',result);(a.out/'COMPLETE').write_text('Linear diagnostic complete; not stellar or live-galaxy validation.\n')
    print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
