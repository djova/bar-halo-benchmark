"""Read the original unforced table and frozen population; no orbit integration."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ORIGINAL_TABLE = 'results/noise-sweep/transfer-preflight-01/unforced-coefficients/result.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def frequencies(jr, jz, js):
    angular = jz+2*np.asarray(js)
    root = np.sqrt(angular*angular+2)
    action = jr+(angular+root)/2
    radial = action**-3
    h = (1+angular/root)/2
    return radial, h*radial, 4*(radial/root**3-3*h*h/action**4)


def read_case(prepared, frozen):
    cfg = frozen['orbit_config']; reference = prepared['reference']
    assert prepared['label'] == frozen['label']
    assert cfg['action_unit'] == prepared['action_unit'] and cfg['time_unit'] == prepared['time_unit']
    assert cfg['width'] == prepared['sigma']*cfg['action_unit']
    assert cfg['end'] == frozen['T']*cfg['time_unit']
    assert cfg['speed'] == prepared['physical_sweep_speed']
    rows = sorted(prepared['scan'], key=lambda row: row['Js'])
    js = np.array([row['Js'] for row in rows])
    assert len(js) == 65 and np.all(np.diff(js) > 0)
    values = {key: np.array([row[key] for row in rows]) for key in ['a', 'b', 'dlogf_dJs', 'omega']}
    radial, omega, derivative = frequencies(cfg['jr'], cfg['jz'], js)
    complex_derivative = 2*np.imag(frequencies(cfg['jr'], cfg['jz'], js+1e-20j)[1])/1e-20
    errors = dict(archived_frequency=float(np.max(abs(omega-values['omega']))),
                  archived_a=float(np.max(abs(derivative-values['a']))),
                  complex_step_a=float(np.max(abs(complex_derivative-derivative))))
    assert max(errors.values()) < 1e-12
    u, tu, js0 = cfg['action_unit'], cfg['time_unit'], cfg['js0']
    sweep = [js0, js0+cfg['speed']*cfg['end']]
    population = [cfg['mean']-3*cfg['width'], cfg['mean']+3*cfg['width']]
    regions = {}
    for label, (lo, hi) in [('prescribed_resonance_path', sweep), ('initial_three_sigma', population)]:
        assert js[0] <= lo < hi <= js[-1]
        points = np.unique(np.r_[lo, js[(js >= lo) & (js <= hi)], hi])
        measured = {}
        for key in ['a', 'b', 'dlogf_dJs']:
            v = np.interp(points, js, values[key])
            ratio = v/reference[key]
            measured[key] = dict(minimum=float(v.min()), maximum=float(v.max()),
                                 relative_to_central_range=[float(ratio.min()), float(ratio.max())],
                                 max_abs_fractional_change=float(np.max(abs(ratio-1))))
        regions[label] = dict(Js_range=[lo, hi], local_action_range=[(lo-js0)/u, (hi-js0)/u],
                              tabulated_nodes_inside=int(np.sum((js >= lo) & (js <= hi))),
                              coefficients=measured)
    tau = np.linspace(0, frozen['T'], 201)
    resonance = js0+cfg['speed']*tu*tau
    gaussian_slope = -(resonance-cfg['mean'])/cfg['width']**2
    halo_slope = np.interp(resonance, js, values['dlogf_dJs'])
    assert abs(gaussian_slope[0]-reference['dlogf_dJs']) < 1e-10
    density_ratio = np.exp(-.5*((resonance-cfg['mean'])/cfg['width'])**2+
                          .5*((js0-cfg['mean'])/cfg['width'])**2)
    central = next(row for row in prepared['central'] if row['n'] == 32)
    harmonics = sorted(central['harmonics'], key=lambda row: tuple(row['k']))
    assert len(harmonics) == len({tuple(row['k']) for row in harmonics}) == 15
    assert sum(row['k'] == [0, 0, 2] for row in harmonics) == 1
    modes = [dict(k=row['k'], coupling=row['b'], coupling_over_reference=row['b']/reference['b'],
                  detuning=row['detuning'], detuning_over_libration_frequency=row['detuning']*tu)
             for row in harmonics]
    off = [row for row in modes if row['k'] != [0, 0, 2]]
    radial0, omega0, _ = frequencies(cfg['jr'], cfg['jz'], js0)
    omega_end = float(frequencies(cfg['jr'], cfg['jz'], sweep[1])[1])
    phase_error = max(abs(np.angle(np.exp(1j*(row['phase']-reference['phase'])))) for row in rows)
    return dict(label=prepared['label'], original_forecast_qualified=frozen['qualified'], config=cfg,
                reference=reference, regions=regions, reference_libration_period=2*np.pi*tu,
                azimuthal_angle_period=2*np.pi/float(omega0), radial_angle_period=2*np.pi/float(radial0),
                azimuthal_cycles_per_libration=float(omega0*tu), radial_cycles_per_libration=float(radial0*tu),
                duration_in_libration_periods=frozen['T']/(2*np.pi),
                pattern_frequency_range=[float(omega0), omega_end],
                pattern_frequency_fractional_change=omega_end/float(omega0)-1,
                sweep_in_reference_half_widths=(sweep[1]-sweep[0])/(2*u),
                initial_three_sigma_probability=math.erf(3/math.sqrt(2)),
                initial_gradient_along_sweep=dict(tau=tau.tolist(), Js=resonance.tolist(),
                    selected_gaussian_slope=gaussian_slope.tolist(), halo_df_slope=halo_slope.tolist(),
                    selected_slope_over_reference=(gaussian_slope/reference['dlogf_dJs']).tolist(),
                    halo_slope_over_reference=(halo_slope/reference['dlogf_dJs']).tolist(),
                    selected_initial_density_over_start=density_ratio.tolist()),
                retained_central_harmonics=modes,
                minimum_retained_nonresonant_frequency_ratio=min(abs(row['detuning_over_libration_frequency']) for row in off),
                maximum_archived_coupling_phase_offset=float(phase_error),
                analytic_frequency_checks=errors,
                scan=[dict(local_action=(row['Js']-js0)/u, **row) for row in rows])


def figures(case, out):
    plt.rcParams.update({'font.size': 12, 'figure.dpi': 180,
                         'axes.spines.top': False, 'axes.spines.right': False})
    reference = case['reference']; scan = case['scan']
    x = np.array([row['local_action'] for row in scan])
    fig, ax = plt.subplots(figsize=(5.8, 4.7))
    lo, hi = case['regions']['initial_three_sigma']['local_action_range']
    ax.axvspan(lo, hi, color='#c9d0d8', alpha=.28, label='Initial 99.73% population interval')
    lo, hi = case['regions']['prescribed_resonance_path']['local_action_range']
    ax.axvspan(lo, hi, color='#deac54', alpha=.34, label='Prescribed resonance sweep')
    ax.plot(x, [100*(row['a']/reference['a']-1) for row in scan], 'o-', ms=3,
            color='#28659a', label='Frequency gradient a')
    ax.plot(x, [100*(row['b']/reference['b']-1) for row in scan], 's-', ms=3,
            color='#a75237', label='Bar coupling b')
    ax.axhline(0, color='.5', lw=.8)
    ax.set(xlim=(-28, 28), xlabel='Initial action offset (Js − Js₀) / u',
           ylabel='Change from reference (%)')
    ax.set_title('Fixed coefficients across the population', fontsize=12, pad=12)
    visible=[v for row in scan if -28 <= row['local_action'] <= 28
             for v in [100*(row['a']/reference['a']-1),100*(row['b']/reference['b']-1)]]
    span=max(visible)-min(visible);ax.set_ylim(min(visible)-.1*span,max(visible)+.15*span)
    ax.legend(fontsize=11, loc='best');ax.grid(alpha=.12)
    fig.tight_layout(rect=(.02,.075,.98,.98))
    fig.text(.07,.035,'Markers: recorded unforced coefficients. Lines interpolate.',fontsize=9)
    for extension in ['png','pdf']:fig.savefig(out/f'coefficient-domain.{extension}')
    plt.close(fig)

    gradient=case['initial_gradient_along_sweep']
    fig,ax=plt.subplots(figsize=(5.8,4.7))
    ax.plot(gradient['tau'],gradient['selected_slope_over_reference'],color='#a75237',lw=2.5,
            label='Selected Gaussian population')
    ax.plot(gradient['tau'],gradient['halo_slope_over_reference'],color='#28659a',lw=2.5,
            label='Analytical halo DF (interpolated)')
    ax.set(xlim=(0,max(gradient['tau'])),ylim=(0,None),xlabel='Prescribed sweep time τ (local time units)',
           ylabel='Initial log-slope magnitude / starting value')
    ax.set_title('The initial gradient changes along the sweep', fontsize=12, pad=12)
    ax.annotate(f"{gradient['selected_slope_over_reference'][-1]:.2f}×",
                (gradient['tau'][-1],gradient['selected_slope_over_reference'][-1]),
                xytext=(-64,-30),textcoords='offset points',color='#a75237',fontsize=13,
                bbox=dict(facecolor='white',edgecolor='none',alpha=.92,pad=1.5))
    ax.legend(fontsize=10.5,loc='upper left');ax.grid(alpha=.15)
    fig.tight_layout(rect=(.02,.11,.98,.98))
    fig.text(.07,.057,'Both curves sample the initial distributions along Js,res(t).',fontsize=9)
    fig.text(.07,.022,'They are not evolved noisy or bar-forced density measurements.',fontsize=9)
    for extension in ['png','pdf']:fig.savefig(out/f'initial-gradient-sweep.{extension}')
    plt.close(fig)

    modes=case['retained_central_harmonics']
    fig,ax=plt.subplots(figsize=(5.8,4.7))
    for mode in modes:
        resonant=mode['k']==[0,0,2]
        ax.scatter(mode['detuning_over_libration_frequency'],mode['coupling_over_reference'],
                   s=65 if resonant else 34,color='#a75237' if resonant else '#28659a',
                   marker='s' if resonant else 'o')
        if resonant or mode['k']==[1,0,2]:
            ax.annotate(str(tuple(mode['k'])),(mode['detuning_over_libration_frequency'],mode['coupling_over_reference']),
                        xytext=(-5,-22) if resonant else (-55,10),textcoords='offset points',fontsize=11.5)
    ax.set_xscale('symlog',linthresh=1)
    ax.axvline(0,color='.5',lw=.8)
    ax.set(ylim=(-.03,1.27),xlabel='Signed detuning / reference libration frequency',
           ylabel='Coupling / retained resonance coupling')
    ax.set_title('A strong harmonic can still oscillate fast', fontsize=12, pad=12)
    ax.grid(alpha=.15);fig.tight_layout(rect=(.02,.11,.98,.98))
    fig.text(.07,.057,'Only the 15 archived largest harmonics at the starting action.',fontsize=9)
    fig.text(.07,.022,'This is not a complete resonance search or a torque-error bound.',fontsize=9)
    for extension in ['png','pdf']:fig.savefig(out/f'coupling-detuning.{extension}')
    plt.close(fig)


def main():
    p=argparse.ArgumentParser();p.add_argument('--coefficients',type=Path,required=True)
    p.add_argument('--forecast',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();cpu=time.process_time();wall=time.monotonic()
    prepared=json.loads(a.coefficients.read_text());forecast=json.loads(a.forecast.read_text())
    assert forecast['source_sha256'][ORIGINAL_TABLE]==sha(a.coefficients)
    assert prepared['all_pass'] and forecast['frozen_before_3d']
    assert {c['label'] for c in prepared['cases']}=={'A','B'}
    cases=[read_case(c,next(f for f in forecast['cases'] if f['label']==c['label'])) for c in prepared['cases']]
    a.out.mkdir(parents=True,exist_ok=False)
    figures(next(c for c in cases if c['label']=='B'),a.out)
    result=dict(cases=cases,coefficients_sha256=sha(a.coefficients),forecast_sha256=sha(a.forecast),
                source_sha256=sha(__file__),cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-wall,
                scope='Retrospective descriptive readback of the original unforced table and frozen initial populations. '
                'Initial-gradient curves are not evolved densities. Tabulated ranges and retained harmonics are not error bounds. '
                'No new trajectory, fitted parameter, physical qualification, changed forecast or altered numerical gate.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for c in cases:
        print(json.dumps(dict(label=c['label'],regions=c['regions'],
            selected_slope_ratio_at_end=c['initial_gradient_along_sweep']['selected_slope_over_reference'][-1],
            halo_slope_ratio_at_end=c['initial_gradient_along_sweep']['halo_slope_over_reference'][-1],
            azimuthal_cycles_per_libration=c['azimuthal_cycles_per_libration'],
            retained_nonresonant_frequency_ratio_min=c['minimum_retained_nonresonant_frequency_ratio'],
            analytic_checks=c['analytic_frequency_checks']),indent=2))


if __name__=='__main__':main()
