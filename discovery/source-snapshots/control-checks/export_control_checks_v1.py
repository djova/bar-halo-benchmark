"""Export selected terminal control records and actual saved operands; no evolution."""
from pathlib import Path
import argparse, json, hashlib, math, re, resource
resource.setrlimit(resource.RLIMIT_CPU,(29,30))
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
args=p.parse_args();args.out.mkdir(parents=True,exist_ok=False)
root=Path(__file__).resolve().parents[2];base=root/'results/discovery-20261001';pub=args.out
release='discovery-2026-10-01.4'
def load(p):return json.loads((base/p).read_text())
def anchor(p):
 f=base/p
 return dict(record_id=p,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
def write(path,data):
 s=json.dumps(data,indent=2,allow_nan=False)+'\n'
 # Preserve parsed numbers while avoiding numeric literals resembling telephone numbers.
 s=re.sub(r'(?<![\w".])(-?\d+\.\d{10,}(?:[eE][+-]?\d+)?)(?![\w".])',lambda m:format(float(m[1]),'.17e'),s)
 assert json.loads(s)==data
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(s)
phase=load('twins/analytic-phase-control-01/result.json'); readback=load('twins/analytic-phase-control-readback-01/result.json')
compact=[]; curves=[]
for row in readback['rows']:
 seed,pop=row['seed'],row['population']; analytic=load(f'twins/analytic-phase-control-01/seed-{seed}.json')['records'][pop];live=load(f'twins/analytic-phase-control-01/inputs/run-{seed}-{pop}-dt0.01.json')['records']
 def record(r):return dict(time=r['time'],shells=[{k:s[k] for k in ['shell','particles','mass','coverage','second_diagonal']} for s in r['shells']])
 compact.append(dict(seed=seed,population=pop,analytic=[record(r) for r in analytic],live=[record(r) for r in live]))
 ext=row['extrema']['live'];shell=ext['shell'];component=['v_R_squared','v_phi_squared','v_z_squared'].index(ext['component']);initial=analytic[0]['shells'][shell]['second_diagonal'][component]
 assert initial==live[0]['shells'][shell]['second_diagonal'][component]
 curves.append(dict(seed=seed,population=pop,shell=shell,component=ext['component'],initial_moment=initial,times=[r['time'] for r in analytic],analytic_percent=[100*(r['shells'][shell]['second_diagonal'][component]/initial-1) for r in analytic],live_percent=[100*(r['shells'][shell]['second_diagonal'][component]/initial-1) for r in live]))
phase_data=dict(model='fixed-unsoftened-isochrone versus live-softened-halo',status='numerical_controls_passed_original_shell_flags_retained',clock=dict(unit='isochrone reference time',end=15,cadence=.5),seeds=[50511,50512],population_size=16384,old_threshold_fraction=.05,observable='Mass-normalized shell diagonal second moment, divided by its common initial value',formula='100*(moment(t)/moment(0)-1)',curves=curves,rows=readback['rows'],checks={k:phase[k] for k in ['initial_checks','all_31_epochs_complete','original_live_numerical_qualification','original_flags_unchanged','frozen_inputs_unchanged','module_hashes_unchanged']},selected_Cartesian=[{k:r[k] for k in ['seed','particle_ids','maximum_state_scaled','maximum_DOP_energy_scaled','maximum_DOP_L_vector_scaled','pass_all']} for r in phase['selected_checks']],limits=phase['limitations'],anchors=[anchor('twins/analytic-phase-control-01/result.json'),anchor('twins/analytic-phase-control-readback-01/result.json'),anchor('twins/single-position-completion-01/result.json')])
warm=load('feedback/cusp-warm-pilot-01/result.json');wr=load('feedback/cusp-warm-readback-01/result.json');ref=load('feedback/cusp-warm-reference-01/result.json')
principal=[r for r in wr['rows'] if r['name']=='fine' and r['Rc_upper'] in [None,.25]]
assert len(principal)==4
warm_data=dict(model='fixed-Hernquist halo plus prescribed positive gas cycle, analytic warm stellar target',status='finite_heating_unresolved',clock=dict(unit='Hernquist reference time',duration=80),count=512,seed=warm['seed'],selection_seed=warm['selection_seed'],frequencies=[5,8],fine_dt=.000625,precision_allowance=.3,observable='Paired finite-pulse minus unforced specific stellar energy gain',energy_units='G=M_h=a_h=1; per exact declared cohort mass',whole_target_mass=1,inner_guiding_mass=0.026499021160743902,rows=principal,original_scientific_gate=warm['gate'],original_reference={k:warm['reference'][k] for k in ['radial_cartesian_scaled_r_error','radial_cartesian_scaled_pr_error','Cartesian_all_L_scaled_error']},tighter_reference={k:ref[k] for k in ['ids','rtol','position_momentum_atol','work_atol','max_step','maximum_scaled_radius_error','maximum_scaled_momentum_error','maximum_energy_disagreement','maximum_all_L_scaled_error','maximum_radial_energy_work_error','maximum_Cartesian_energy_work_error','per_path','gate']},limits=warm['limitations'],anchors=[anchor('feedback/cusp-warm-pilot-01/result.json'),anchor('feedback/cusp-warm-readback-01/result.json'),anchor('feedback/cusp-warm-reference-01/result.json')])
echo=load('echoes/finite-map-diagnostic-completion02/measurement/result.json');phys=echo['config']['physical_parameters']
echo_data=dict(model='positive-source prescribed spatial pulses; no self-gravity',status='instantaneous_exact_zero_test_failed',clock=dict(unit='isochrone reference time',time=16,meaning='Immediately after the second impulse; positions have not yet responded'),readout=dict(degree=2,order=2,radius=1,annulus_log_width=.1,components=['complex potential','complex radial force','complex tangential force']),case_order=[[1,1],[1,-1],[-1,1],[-1,-1]],contrast_weights=[.25,-.25,-.25,.25],cohort_mass=phys['absolute_reference_cohort_mass'],zero_allowance_over_reference_peak=.1,zero_reference_peaks=[abs(v)/r for v,r in zip([complex(a,b) for a,b in zip(echo['rows'][0]['mixed']['real'],echo['rows'][0]['mixed']['imag'])],echo['rows'][0]['zero_error_over_frozen_reference_peak'])],rows=echo['rows'],mass_ladder=echo['mass_ladder'],pulse_A=phys['pulse_A'],pulse_B=phys['pulse_B'],taper=phys['cohort_taper'],limits=['All nine combined complex zero gates failed; no late spatial echo calculated.','Energy/taper refinement repaired the unforced mass gate, not the field zero gate.','The readout measures only degree/order (2,2); no total angular field claim.','No self-gravity, stellar response or observational validation.'],anchors=[anchor('echoes/finite-map-diagnostic-completion02/measurement/result.json'),anchor('echoes/finite-map-diagnostic-completion02/result.json')])
data=dict(schema_version=1,release=release,status='completed_checks_with_unresolved_physical_extensions',article='discovery-controls.html',phase=phase_data,warm=warm_data,echo=echo_data,reproduction_scope='Compact saved-profile and response arithmetic. No new orbit evolution, force solve, physical sample or complete live-galaxy reproduction.')
energy_path='echoes/finite-energy-pair-01/measurement/result.json'
energy=load(energy_path);outer=load('echoes/finite-energy-pair-01/result.json')
assert outer['child_COMPLETE'] and outer['child_receipt']['exit_code']==0
assert len(energy['rows'])==2 and all(r['gates']['zero'] for r in energy['rows'])
data['echo']['status']='energy_only_continuation_passes_instantaneous_gate_late_response_untested'
data['echo']['energy_continuation']=dict(rows=energy['rows'],scope=energy['scope'],anchor=anchor(energy_path))
data['echo']['limits'][0]='The original nine combined zero gates failed. A separate predeclared energy-only pair passes that instantaneous prerequisite; no late spatial echo has been calculated.'
write(pub/'checks-v1.json',data)
write(pub/'phase-profiles.json',dict(schema_version=1,cases=compact))
for name in ['initial.npz','fine-response.npz']:
 src=base/'feedback/cusp-warm-pilot-01'/name;(pub/('warm-'+name)).write_bytes(src.read_bytes())
print('Exported six phase curves, four warm readouts, nine original and two later echo rows.')
