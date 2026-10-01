"""Export and replay saved cuspy-feedback arithmetic; never evolve trajectories."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import numpy as np


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def write(path,value):
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')


def stat(values):
    values=np.asarray(values,dtype=float)
    mean=float(values.mean());se=float(values.std(ddof=1)/np.sqrt(len(values)))
    square=float(np.sum(values*values))
    return dict(mean=mean,standard_error=se,
        effective_contributing_states=float(values.sum()**2/square) if square else 0.)


def scientific_step(row):
    keys=['dt','maximum_abs_energy_work_defect','maximum_all_L_vector_error',
        'maximum_all_L_vector_scaled_error','L_invariant_pass',
        'weighted_energy_work_signed','weighted_energy_work_mean_absolute',
        'ledger_forward_inverse_pair_ratios','weighted_ledger_gates',
        'inverse_composition_maximum_scaled_error','inverse_composition_pass']
    return {k:row[k] for k in keys}


def export(args):
    args.out.mkdir(parents=True,exist_ok=False)
    known=load(args.known/'result.json');pulse=load(args.pulse/'result.json')
    readback=load(args.readback/'result.json');pilot=load(args.pilot/'result.json')
    assert known['gate'] and pulse['status']=='COMPLETE'
    assert pulse['n']==8192 and pulse['seed']==201054
    assert sha(args.pulse/'result.json')==readback['input_sha256']['result.json']
    operands=args.out/'operands';operands.mkdir()
    input_rows=[]
    for name,folder in [('known-map',args.known),('physical-pulse',args.pulse),
                        ('pulse-analysis',args.readback),('failed-precision-pilot',args.pilot)]:
        input_rows.append(dict(selector=name+'/result.json',sha256=sha(folder/'result.json')))
    for name,digest in readback['input_sha256'].items():
        assert sha(args.pulse/name)==digest
        input_rows.append(dict(selector='physical-pulse/'+name,sha256=digest))
    initial=np.load(args.pulse/'initial.npz')
    np.savez_compressed(operands/'initial.npz',**{k:initial[k] for k in initial.files})
    for dt in (.00125,.000625):
        maps=np.load(args.pulse/f'maps-dt{dt:g}.npz')
        rem=np.load(args.pulse/f'remainder-dt{dt:g}.npz')
        replay=np.load(args.pulse/f'replay-dt{dt:g}.npz')
        payload={k:maps[k] for k in ['deltaE','delta_initial','delta_final','work',
            'energy_minus_work','L_vector_error','virtual_first_work']}
        payload.update({k:rem[k] for k in rem.files})
        payload['inverse_composition_scaled_norm']=np.linalg.norm(
            replay['endpoint']-initial['xv'][None,:,:],axis=-1)/(1+np.linalg.norm(initial['xv'],axis=-1))
        np.savez_compressed(operands/f'pulse-dt{dt:g}.npz',**payload)
    raw=np.load(args.known/'raw.npz')
    np.savez_compressed(operands/'known-map.npz',**{k:raw[k] for k in raw.files if k!='xv'})
    dop=np.load(args.pulse/'selected-dop.npz')
    np.savez_compressed(operands/'selected-reference.npz',**{k:dop[k] for k in dop.files})
    rows=[]
    for i,frequency in enumerate((5.,8.)):
        a=readback['actual_forward'][i+1];w=readback['regular_weak_forecast'][i]
        difference=readback['paired_forward_minus_regular_weak'][i]
        rows.append(dict(frequency=frequency,actual_forward_mean=a['mean'],standard_error=a['standard_error'],
            weak_mean=w['mean'],weak_standard_error=w['standard_error'],
            paired_actual_minus_weak_mean=difference['mean'],
            paired_actual_minus_weak_standard_error=difference['standard_error'],
            paired_fine_minus_coarse_mean=readback['paired_fine_minus_coarse'][i]['mean'],
            paired_fine_minus_coarse_standard_error=readback['paired_fine_minus_coarse'][i]['standard_error']))
    definition=dict(
        phase_space='Cartesian6D IID compact proposal; deterministic integration maps per IID state',
        energy='E=v²/2+Phi_static(r), Phi(infinity)=0; delta=E-Phi(0)',
        central_target='g(E)=f_piecewise(E)*[(Ec-E)/(Ec-Phi0)]²/Z for Phi0<E<Ec, zero otherwise',
        proposal='q=.5*delta^(-5/2)*[(Ec-E)/(Ec-Phi0)]²/U + .5/V inside E<Ec',
        forward_estimate='(R64+inverse_capture)/q, R=−[F(E_forward)−F(E)−g(E)*DeltaE_forward]',
        primitive='F(E)=−integral_E^Ec g(e)de, F=0 outside Ec; regular curvature plus downward seam atom',
        inverse_capture='−F(E)*indicator(E_inverse>=Ec); actual true inverse map, not negative pulse',
        standard_error='Empirical IID state standard deviation/sqrt(N), no self-normalization',
        axes=dict(initial=['IID_state','Cartesian_x_y_z_vx_vy_vz'],
            map=['forward_zero','forward_5','forward_8','inverse_zero','inverse_5','inverse_8'],
            forward_estimate=['zero','frequency5','frequency8'],weak=['frequency5','frequency8'],
            L_vector=['Lx','Ly','Lz'],translation_kicks=[0.,.05,.2,.8]),
        replay_scope='Recompute saved-array estimates/accounting/paired covariance; no resampling, force integration, DF inversion or self-consistent evolution')
    summary=dict(schema='feedback-cusp-v1',claim='Small finite central-halo energy response in the specified cuspy potential; coeval stellar finite-amplitude selectivity remains untested',
        model=dict(halo='Hernquist, G=M_h=a_h=1',gas_mass=.1,gas_scales=[.2,1.3],common_gas_cutoff=8.,
            gas_component_fractions='1/2+a(t),1/2−a(t)',
            pulse='a(t)=.003*sin²(pi*t/80)*cos(omega*t),0<t<80; zero outside',duration=80.,
            literal_frequencies=[5.,8.],amplitude=.003,
            DF_status=known['actual_DF_status'],tag_radius_parameter=2.,
            units=dict(length='Hernquist scale radius',mass='original halo mass',time='sqrt(a_h³/(G*M_h))',
                frequency='inverse code time',specific_energy='G*M_h/a_h',figure_energy_normalization='per unit normalized stationary central-tag mass')),
        normalization=pulse['normalization'],figure=dict(rows=rows,x_axis='Literal pulse frequency',
            y_axis='Specific energy gain per stationary tagged mass',
            error_bars='One empirical IID standard error; paired difference uses covariance of identical states',
            scope='Central halo only; weak stellar means are not combined with these finite halo means'),
        sampling=dict(n=pulse['n'],seed=pulse['seed'],IID=True,checks=pulse['sampling'],
            target_mass=readback['target_mass'],no_renormalization=True,
            failed_pilot=dict(n=pilot['n'],seed=pilot['seed'],
                sampling_precision_gate=pilot['refinement']['sampling_precision_gate'],
                retained_separately=True,pooled_with_8192=False)),
        numerical=dict(coarse=scientific_step(pulse['completed'][0]),fine=scientific_step(pulse['completed'][1]),
            refinement=pulse['refinement'],sampled_qualification=pulse['numerical_qualification'],
            qualification_scope=pulse['numerical_qualification_scope'],
            selected_reference=dict(selected_before_outcomes=pulse['selected_before_forced_outcomes'],
                maximum_abs_energy_work_defect=pulse['reference']['maximum_abs_energy_work_defect'],
                maximum_L_vector_error=pulse['reference']['maximum_all_L_vector_error'],
                scope='Selected endpoints only; not an omitted-state bound or volume-preserving population estimator')),
        physical_support=dict(coarse=pulse['completed'][0]['remainder']['raw'],
            fine=pulse['completed'][1]['remainder']['raw'],
            weak_seam_atom_upper=pulse['completed'][1]['remainder']['weak_seam_atom_absolute_upper'],
            statement='All inverse Ec capture terms and seam atoms retained; no sampled inverse capture is not a global absence theorem'),
        known_map={k:known[k] for k in ['scope','passivity','field_control','n','seed','kicks','normalization',
            'actual_DF_status','target_moment_checks','proposal_marginals','canonical_controls',
            'deterministic_endpoints','primitive_control','gate']},
        retained_analysis={k:readback[k] for k in ['actual_forward','paired_zero_contrast','raw_signed_forward',
            'raw_signed_zero_subtracted','regular_weak_forecast','paired_forward_minus_regular_weak',
            'paired_fine_minus_coarse','thresholds','energy_cohorts','top_contributions']},
        definitions=definition,input_selectors=input_rows,
        source_checksums=dict(physical_pulse=pulse['provenance']['source_sha256'],
            physical_protocol=pulse['provenance']['protocol_sha256'],
            known_map=known['provenance']['source_sha256'],known_protocol=known['provenance']['protocol_sha256'],
            analysis=readback['provenance']['source_sha256'],export=sha(__file__)),
        limitations=['Fixed analytic gravitational field, no self-gravity update or cusp-to-core transformation',
            'Stationary binding-energy tag is not all instantaneous mass enclosed at radius2',
            'No finite-amplitude warm stellar energy, random-motion or stellar/halo cost measurement',
            'No observational old-disk survival or vertical-survival bound',
            'Empirical IID errors and selected adaptive references do not certify unseen tails',
            'Fine numerical gates do not prove physical-flow accuracy at arbitrarily small radius',
            'Declared piecewise DF approximation; normalization/seam controls are not analytic Eddington exactness',
            'Actual-minus-weak paired differences are1.75/1.99 empirical SE; nonlinear ensemble correction unresolved',
            'Frequency8 needs a larger gas kinetic proxy; neither proxy is measured feedback work',
            'Literal frequency5 here differs from the earlier optimized cored-model waveform'])
    summary['arithmetic_package']='operands/feedback-cusp-v1'
    summary['arithmetic_replay']='scripts/discovery/replay_feedback_cusp_v1.py'
    summary['retained_files']=[dict(path=str(p.relative_to(args.out)),
        public_path='operands/feedback-cusp-v1/'+str(p.relative_to(args.out)),sha256=sha(p),bytes=p.stat().st_size)
        for p in sorted(operands.glob('*.npz'))]
    write(args.out/'feedback-cusp.json',summary)
    shutil.copyfile(__file__,args.out/'replay_feedback_cusp_v1.py')
    write(args.out/'receipt.json',dict(scope='Saved-array arithmetic export only',summary_sha256=sha(args.out/'feedback-cusp.json'),
        replay_sha256=sha(args.out/'replay_feedback_cusp_v1.py'),retained_files=summary['retained_files']))
    print(json.dumps(dict(scope='Arithmetic export only',file_count=len(summary['retained_files']),
        operand_bytes=sum(row['bytes'] for row in summary['retained_files']))))


def replay(args):
    data=load(args.source/'feedback-cusp.json')
    for row in data['retained_files']:
        assert sha(args.source/row['path'])==row['sha256'],row['path']
    initial=np.load(args.source/'operands/initial.npz');q=initial['q'];g=initial['g']
    steps=[];estimates=[];forecasts=[]
    for dt in (.00125,.000625):
        z=np.load(args.source/f'operands/pulse-dt{dt:g}.npz')
        positive=np.array([(z[f'R64_{i}']+z[f'support_{i}'])/q for i in range(3)])
        np.testing.assert_array_equal(positive,z['positive_estimates'])
        forecast=.5*initial['slope'][None,:]/q[None,:]*z['virtual_first_work'].T**2
        np.testing.assert_array_equal(forecast,z['weak_forecast'])
        ledger=np.mean(g[None,:]/q[None,:]*abs(z['deltaE']-z['work']),axis=1)
        contrast=positive[1:]-positive[0]
        ratio=np.array([[(ledger[i+1]+ledger[0])/contrast[i].mean(),
            (ledger[i+4]+ledger[3])/contrast[i].mean()] for i in range(2)])
        steps.append(dict(dt=dt,actual_forward=[stat(v) for v in positive],
            paired_zero_contrast=[stat(v) for v in contrast],
            raw_signed_forward=[stat(v) for v in g[None,:]/q[None,:]*z['deltaE'][:3]],
            regular_weak=[stat(v) for v in forecast],weighted_ledger_pair_ratios=ratio.tolist(),
            weighted_ledger_pass=(np.max(ratio,axis=1)<.05).tolist(),
            maximum_inverse_composition_scaled_norm=float(z['inverse_composition_scaled_norm'].max()),
            support_exit_counts=[int(np.sum(z['delta_final'][i+3]>=data['normalization']['Ec']-data['normalization']['Phi0'])) for i in range(3)]))
        estimates.append(positive);forecasts.append(forecast)
    paired=estimates[1][1:]-estimates[1][0]-estimates[0][1:]+estimates[0][0]
    actual_minus_weak=estimates[1][1:]-forecasts[1]
    for i,row in enumerate(data['figure']['rows']):
        np.testing.assert_allclose(stat(estimates[1][i+1])['mean'],row['actual_forward_mean'],rtol=1e-14,atol=0)
        np.testing.assert_allclose(stat(estimates[1][i+1])['standard_error'],row['standard_error'],rtol=1e-14,atol=0)
        np.testing.assert_allclose(stat(forecasts[1][i])['mean'],row['weak_mean'],rtol=1e-14,atol=0)
        np.testing.assert_allclose(stat(forecasts[1][i])['standard_error'],row['weak_standard_error'],rtol=1e-14,atol=0)
        np.testing.assert_allclose(stat(actual_minus_weak[i])['mean'],row['paired_actual_minus_weak_mean'],rtol=1e-14,atol=0)
        np.testing.assert_allclose(stat(actual_minus_weak[i])['standard_error'],row['paired_actual_minus_weak_standard_error'],rtol=1e-14,atol=0)
    known=np.load(args.source/'operands/known-map.npz');controls=[]
    for k in data['known_map']['kicks']:
        x=(known[f'R64_k{k}']+known[f'support_k{k}'])/known['q']
        controls.append(dict(k=k,known_mean=k*k/2,actual_forward=stat(x),
            inverse_capture_mean=float(np.mean(known[f'support_k{k}']/known['q'])),
            quadrature32_to64=stat((known[f'R64_k{k}']-known[f'R32_k{k}'])/known['q'])))
    result=dict(scope=data['definitions']['replay_scope'],hashes_checked=True,
        known_map=controls,pulse_steps=steps,paired_fine_minus_coarse=[stat(v) for v in paired],
        paired_actual_minus_regular_weak=[stat(v) for v in actual_minus_weak],
        limitations=data['limitations'])
    if args.out:
        args.out.mkdir(parents=True,exist_ok=False);write(args.out/'result.json',result)
    print(json.dumps(result,indent=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='mode',required=True)
    export_parser=sub.add_parser('export')
    for name in ('known','pulse','readback','pilot','out'):export_parser.add_argument('--'+name,type=Path,required=True)
    replay_parser=sub.add_parser('replay');replay_parser.add_argument('--source',type=Path,required=True)
    replay_parser.add_argument('--out',type=Path)
    args=parser.parse_args();(export if args.mode=='export' else replay)(args)


if __name__=='__main__':main()
