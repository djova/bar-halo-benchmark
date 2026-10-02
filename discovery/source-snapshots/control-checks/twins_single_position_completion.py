"""Resource-only completion of the archived single-position screen; no new draws."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
from pathlib import Path
import argparse
import datetime
import hashlib
import importlib.util
import json
import resource
import shutil
import signal
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
CPU_START,WALL_START=time.process_time(),time.monotonic()
OWNED=None
ACTIVE=None
COUNT=16384
SEEDS=(50511,50512)
POPS=('F0','plus','minus')
EPSILON,THETA,KERNEL=.025,.125,1
END,DT,FINE_DT,PREFIX=15.,.01,.005,.5
CPU_SOFT,CPU_HARD,WALL_CAP=7800,8000,9000
QUANTILES=(.01,.05,.1,.25,.5,.75,.9,.95,.99)
PRIMARY_QUANTILES=(.1,.25,.5,.75,.9)
MOMENT_ALLOWANCE=2e-13
SIGN_PROBABILITY_ROUNDOFF=1e-12
P_SCALE=2**.5
L_SCALE=.5**.5


def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(Path(path).read_text())


def tied_quantile(np,values,weights,fractions):
    """Interpolate a weighted CDF after aggregating exactly tied coordinates.

    Splitting a co-located mass into unequal partners must not change a spatial
    quantile merely through the arbitrary order of equal coordinates.
    """
    order=np.argsort(values,kind='stable');v=values[order];w=weights[order]
    starts=np.r_[0,np.flatnonzero(v[1:]!=v[:-1])+1]
    grouped=np.add.reduceat(w,starts);cdf=np.cumsum(grouped);cdf/=cdf[-1]
    return np.interp(fractions,cdf,v[starts])


def write(path,value):
    path=Path(path)
    def numeric(item):
        if hasattr(item,'item'):return item.item()
        raise TypeError('Unsupported JSON value:'+type(item).__name__)
    temporary=path.with_name(path.name+'.tmp')
    temporary.write_text(json.dumps(value,indent=2,allow_nan=False,default=numeric)+'\n')
    temporary.replace(path)


def configuration():
    return dict(scope='Rapid-adjustment veto screen at finite N/eps; no collective-stability proof',
        model='Live self-gravitating spherical p8 twins, G=M0=1,b=.5; no disc/bar/collisions',
        family_count=COUNT,particle_count=COUNT,seeds=list(SEEDS),sampling_method=4,common_uniform_seeds=[s+20000 for s in SEEDS],
        sign_probabilities='F0:1/2; F±:(1±h/ratio)/2; same PCG64 U across populations',
        sign_probability_certificate=dict(interval=[.25,.75],roundoff_allowance=SIGN_PROBABILITY_ROUNDOFF,
            treatment='Validate without clipping or changing any sampled threshold'),
        populations=list(POPS),epsilon=EPSILON,theta=THETA,kernel=KERNEL,
        duration=END,coarse_dt=DT,first_seed_refined_dt=FINE_DT,
        cases=[dict(seed=s,population=p,dt=DT) for s in SEEDS for p in POPS]+
              [dict(seed=SEEDS[0],population=p,dt=FINE_DT) for p in POPS],
        integrator='Cached kick-drift-kick; full velocities at every recorded state',
        diagnostic_interval=.5,full_snapshot_interval=.5,tracked_interval=.05,
        tracked_particles=128,tracked_rule='Same particles as fixed direct targets; no outcome selection',
        all_quantile_fractions=list(QUANTILES),primary_quantile_fractions=list(PRIMARY_QUANTILES),
        quantile_rule='Weighted CDF interpolation after aggregation of exactly tied coordinate values',
        shell_rule='Four initial mass-quartile radial shells about unchanged origin; last unbounded',
        covered_initial_families_minimum=256,current_coverage_particles_minimum=256,
        second_moments='Raw diagonal cylindrical vR,vphi,vz moments; full tensors retained',
        modes=dict(ell=[1,2,3,4],origin='Original inertial origin, no recenter',
            coefficient='C_lm=sum(m_i Y_lm)/shell_mass',amplitude='sqrt(4pi sum_m abs(C_lm)^2)',
            use='Absolute recorded modes and F0/draw context; no relative change from near-zero mode gate'),
        entrance=dict(positive_finite_masses=True,same_position_even_identity_allowance=MOMENT_ALLOWANCE,
            streaming_coverage='All twelve frozen shell/latitude bins; positive finite mass and component RMS',
            maximum_local_paired_stream_difference_over_RMS=.05,maximum_raw_virial_imbalance=.05,
            selected_force_p95_relative=.005,selected_force_p99_relative=.01),
        terminal=dict(primary_quantile_or_covered_mass_second_drift=.05,
            coarse_fine_fractional_drift_difference=.01,energy_relative_error=1e-4,
            momentum_error_over_fixed_scale=1e-6,angular_vector_error_over_fixed_scale=1e-4,
            selected_force_p95_relative=.005,selected_force_p99_relative=.01),
        normalization=dict(momentum_scale=P_SCALE,angular_momentum_scale=L_SCALE,
            energy='Each case actual E0; U=.5 sum physical mass times native self-excluded potential'),
        direct_targets=dict(unique_initial_positions=128,particle_ids=128,
            selection='Eight radial-rank strata, sixteen particles each; seed60511/60512',
            endpoints='Same IDs at initial/end; direct sum over all16384 current particles'),
        profile=dict(prefix=PREFIX,case='seed50511 F0 dt.01',overhead_fraction=.25,
            rule='Whole prefix CPU per completed step times remaining fixed steps, plus elapsed setup CPU',
            stop_if_projected_CPU_above=CPU_SOFT),
        cpu_soft=CPU_SOFT,cpu_hard=CPU_HARD,wall_cap=WALL_CAP,
        no_renormalization=True,no_recentering=True,no_velocity_correction=True,no_resampling=True,
        limits=['Two draws do not establish reliable ensemble coverage','No particle-number or softening refinement',
            'Rapid-adjustment flags are not independently sufficient to infer instability',
            'No live bar or transfer of prescribed-field response forecast','No observational validation'])


class BudgetReached(RuntimeError):pass
class EntranceVeto(RuntimeError):pass


def finite_limits():
    old=resource.getrlimit(resource.RLIMIT_CPU)[1]
    hard=CPU_HARD if old==resource.RLIM_INFINITY else min(CPU_HARD,old)
    resource.setrlimit(resource.RLIMIT_CPU,(min(CPU_SOFT,hard-1),hard))
    def stop(*_):raise BudgetReached('Finite unforced-screen allowance reached')
    for sig in (signal.SIGXCPU,signal.SIGTERM,signal.SIGALRM):signal.signal(sig,stop)
    signal.alarm(WALL_CAP)
    priority=os.getpriority(os.PRIO_PROCESS,0)
    if priority<10:os.nice(10-priority)


def freeze(args):
    global OWNED
    args.out.mkdir(parents=True,exist_ok=False);OWNED=args.out.resolve()
    finite_limits()
    inputs=args.out/'inputs';inputs.mkdir()
    baseline=load(args.force_baseline/'result.json')
    if baseline['status']!='complete' or not baseline['frozen_inputs_unchanged']:
        raise RuntimeError('Complete immutable initial-force baseline required')
    files=[(Path(__file__).resolve(),'scripts/discovery/twins_single_position_completion.py',None),
        (args.protocol,'protocol.md',None),(args.resource_review,'resource-review.md',None),
        (ROOT/'research/discovery-20261001/TWINS_SINGLE_POSITION_COMPLETION_SOURCE_REVIEW.json','completion-source-review.json',None),
        (ROOT/'research/discovery-20261001/TWINS_RESOURCE_REVIEW_03.md','resource-review-prior-twelve-hours.md',None),
        (args.force_baseline/'result.json','initial-force-result.json',None),
        (args.opening/'result.json','opening-result.json',None),
        (args.continuum/'result.json','continuum-result.json',None),
        (args.continuum_formula/'result.json','formula-diagnosis.json',None)]
    for row in load(args.force_baseline/'START.json')['snapshots']:
        files.append((args.force_baseline/'inputs'/row['path'],'base/'+row['path'],row['sha256']))
    original_start=load(args.parent/'START.json')
    if sha(args.parent/'launch-config.json')!=original_start['launch_config_sha256']:
        raise RuntimeError('Original launch configuration no longer matches its START receipt')
    original_config=load(args.parent/'launch-config.json')
    original_terminal=load(args.parent/'TERMINAL.json')
    original_entrance=load(args.parent/'ENTRANCE.json')
    original_profile=load(args.parent/'PROFILE.json')
    current=configuration()
    for key in ('cpu_soft','cpu_hard','wall_cap'):
        original_config.pop(key);current.pop(key)
    original_config['profile'].pop('stop_if_projected_CPU_above')
    current['profile'].pop('stop_if_projected_CPU_above')
    if original_config!=current:raise RuntimeError('Archived physical settings/criteria differ')
    if original_terminal['status']!='failed' or original_terminal['error_type']!='BudgetReached':
        raise RuntimeError('Expected preserved finite-cost failed attempt')
    if not original_entrance['all_entrance_pass'] or original_profile['proceed'] or original_profile['prefix_time']!=PREFIX:
        raise RuntimeError('Original entrance and cost-stop records do not match')
    prefix_receipt=load(args.parent/'run-50511-F0-dt0.01.receipt.json')
    if prefix_receipt['last_complete_time']!=PREFIX or original_terminal['last_complete_checkpoint']!=PREFIX:
        raise RuntimeError('Original stopped checkpoint time differs')
    for key in ('snapshot','diagnostics'):
        row=prefix_receipt[key]
        if sha(args.parent/row['path'])!=row['sha256']:
            raise RuntimeError('Original prefix no longer matches its per-case receipt:'+key)
    archived_names=['START.json','launch-config.json','ENTRANCE.json','PROFILE.json','TERMINAL.json','FAILED',
        'run-50511-F0-dt0.01.npz','run-50511-F0-dt0.01.json','run-50511-F0-dt0.01.receipt.json','interrupted-checkpoint.npz']
    for row in original_start['snapshots']:
        files.append((args.parent/'inputs'/row['path'],'original-attempt/inputs/'+row['path'],row['sha256']))
    for sample in original_entrance['samples']:
        seed=sample['seed']
        files.append((args.parent/sample['data'],'original-attempt/'+sample['data'],sample['data_sha256']))
        archived_names.append(f'sample-{seed}.json')
    for seed in SEEDS:
        for pop in POPS:
            archived_names.extend((f'entrance-{seed}-{pop}.json',f'initial-field-{seed}-{pop}.npz'))
    for name in archived_names:files.append((args.parent/name,'original-attempt/'+name,None))
    records=[]
    for source,name,expected in files:
        digest=sha(source)
        if expected is not None and digest!=expected:raise RuntimeError('Prior source hash mismatch:'+name)
        target=inputs/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        if sha(target)!=digest:raise RuntimeError('Source changed while freezing:'+name)
        records.append(dict(path=name,sha256=digest,bytes=target.stat().st_size))
    write(args.out/'launch-config.json',configuration())
    start=dict(started_utc=utc(),snapshots=records,launch_config_sha256=sha(args.out/'launch-config.json'),
        sampling_status='No scientific imports or evolution before snapshots; exact original arrays, no new sampling')
    write(args.out/'START.json',start)
    original_hashes={row['path']:row['sha256'] for row in original_start['snapshots']}
    for row in records:
        if row['path'].startswith('base/') and row['sha256']!=original_hashes.get(row['path']):
            raise RuntimeError('Original executed helper/native/proof differs:'+row['path'])
    review=load(inputs/'completion-source-review.json')
    if review['completion_source_sha256']!=sha(inputs/'scripts/discovery/twins_single_position_completion.py'):
        raise RuntimeError('Completion source-comparison receipt refers to another source')
    if review['original_executed_source_sha256']!=sha(inputs/'original-attempt/inputs/scripts/discovery/twins_single_position.py'):
        raise RuntimeError('Source-comparison original differs from the executed archived source')
    return inputs,start


def run(args):
    global ACTIVE
    inputs,start=freeze(args)
    import numpy as np
    import scipy
    from scipy.special import sph_harm_y
    sys.path.insert(0,str(inputs/'base/build/native'))
    sys.path.insert(0,str(inputs/'base/scripts/discovery'))
    import pyfalcon
    import twins_exact_response as exact
    agama=exact.analytic.agama
    if Path(pyfalcon.__file__).resolve().parent!=(inputs/'base/build/native').resolve():
        raise RuntimeError('Wrong native force extension')
    if Path(agama.__file__).resolve()!=(inputs/'base/build/noise-sweep/Agama-stable-v2/agama.so').resolve():
        raise RuntimeError('Wrong action/sampling extension')
    spec=importlib.util.spec_from_file_location('frozen_force_helpers',inputs/'base/scripts/discovery/twins_force_preflight.py')
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    frozen=load(inputs/'base/evidence/frozen-populations.json')
    if sha(inputs/'base/scripts/discovery/twins_exact_moments.py')!=frozen['source_sha256']:
        raise RuntimeError('Frozen analytic population source mismatch')
    population=next(row for row in frozen['populations'] if row['p']==8)
    opening=load(inputs/'opening-result.json')
    selected=[x for x in opening['measurements'] if x['epsilon']==EPSILON and x['theta']==THETA]
    if len(selected)!=9 or not all(x['selected_force_entrance_screen'] for x in selected):
        raise RuntimeError('Specified prior selected-force setting was not qualified')
    write(args.out/'versions.json',dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,
        native_storage='falcON_SINGLE; float64 output containers'))

    def force(position,mass):
        a,p=pyfalcon.gravity(np.ascontiguousarray(position),mass,EPSILON,theta=THETA,kernel=KERNEL)
        if not np.all(np.isfinite(a)) or not np.all(np.isfinite(p)):raise RuntimeError('Nonfinite force/potential')
        return a,p

    def budgets(x,v,m,a,phi):
        K=float(.5*m@np.sum(v*v,axis=1));U=float(.5*m@phi)
        return dict(K=K,U=U,E=K+U,P=np.sum(m[:,None]*v,axis=0).tolist(),
            L=np.sum(m[:,None]*np.cross(x,v),axis=0).tolist(),W=float(m@np.sum(x*a,axis=1)))

    def direct_check(x,m,a,phi,ids,out_name):
        ar,pr=helper.direct(np,x,m,ids,EPSILON)
        pr=pr+m[ids]*1.5/EPSILON
        rounded_x=x.astype('f4').astype(float);rounded_m=m.astype('f4').astype(float)
        aa,pp=helper.direct(np,rounded_x,rounded_m,ids,float(np.float32(EPSILON)))
        pp=pp+rounded_m[ids]*1.5/float(np.float32(EPSILON))
        den=np.linalg.norm(ar,axis=1);err=np.linalg.norm(a[ids]-ar,axis=1)/np.maximum(den,1e-14)
        st=helper.stats(np,err)
        filename=out_name+'.npz'
        np.savez(args.out/filename,selected_particle_ids=ids,direct_acceleration=ar,direct_potential=pr,
            rounded_input_direct_acceleration=aa,rounded_input_direct_potential=pp,
            returned_selected_acceleration=a[ids],returned_selected_potential=phi[ids],
            selected_relative_force_error=err,selected_direct_force_magnitude=den,
            selected_absolute_force_error=np.linalg.norm(a[ids]-ar,axis=1),selected_positions=x[ids])
        return dict(force_relative=st,force_absolute=helper.stats(np,np.linalg.norm(a[ids]-ar,axis=1)),
            potential_relative=helper.stats(np,abs(phi[ids]-pr)/np.maximum(abs(pr),1e-14)),
            force_floor_targets=int(np.sum(den<1e-14)),data=filename,data_sha256=sha(args.out/filename),
            selected_screen_pass=bool(st['p95']<.005 and st['p99']<.01))

    pot=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5)
    df=agama.DistributionFunction(type='QuasiSpherical',potential=pot)
    with agama.setNumThreads(1):Mq=float(df.totalMass())
    samples={};sample_records=[];entrance=[];initial_fields={}
    # Reuse both original complete signed samples; no RNG/sampler/ActionFinder.
    archived_records={row['seed']:row for row in load(inputs/'original-attempt/ENTRANCE.json')['samples']}
    for seed in SEEDS:
        archived=archived_records[seed]
        with np.load(inputs/'original-attempt'/archived['data']) as z:
            raw=z['raw_sample'].copy();returned_mass=z['returned_mass'].copy()
            folded=z['folded_sample'].copy();actions=z['actions'].copy()
            proposal=z['proposal_mass'].copy();ratio=z['F0_over_Fq'].copy();h=z['p8_deltaF_over_Fq'].copy()
            negative=z['negative_Lz_mask'].copy();uniform=z['common_uniform'].copy()
            probabilities={pop:z[pop+'_threshold'].copy() for pop in POPS}
            signs={pop:z[pop+'_sign'].copy() for pop in POPS}
            initials={pop:z[pop+'_initial'].copy() for pop in POPS}
            physical_mass=z['common_particle_mass'].copy()
            ids=z['selected_particle_ids'].copy();tracked_ids=z['tracked_particle_ids'].copy()
            bounds=z['fixed_shell_boundaries'].copy();saved_counts=z['initial_shell_family_counts'].copy()
        weight_check=archived['population_checks']
        if raw.shape!=(COUNT,6) or returned_mass.shape!=(COUNT,) or not np.all(np.isfinite(raw)) or not np.all(np.isfinite(returned_mass)):
            raise RuntimeError('Unexpected or nonfinite archived sampler arrays')
        expected_folded=raw.copy();expected_negative=np.cross(raw[:,:3],raw[:,3:])[:,2]<0
        expected_folded[expected_negative,3:]*=-1
        if not np.array_equal(negative,expected_negative) or not np.array_equal(folded,expected_folded):
            raise RuntimeError('Archived complete velocity folding differs')
        if not np.array_equal(proposal,np.full(COUNT,Mq/COUNT)) or not np.array_equal(physical_mass,proposal*ratio):
            raise RuntimeError('Archived proposal or physical masses differ')
        expected_probabilities={'F0':np.full(COUNT,.5),'plus':.5*(1+h/ratio),'minus':.5*(1-h/ratio)}
        for pop in POPS:
            if not np.array_equal(probabilities[pop],expected_probabilities[pop]) or not np.array_equal(signs[pop],np.where(uniform<probabilities[pop],1.,-1.)):
                raise RuntimeError('Archived sign thresholds/choices differ:'+pop)
            expected=folded.copy();expected[:,3:]*=signs[pop][:,None]
            if not np.array_equal(initials[pop],expected):raise RuntimeError('Archived actual signed state differs:'+pop)
        weights={pop:physical_mass.copy() for pop in POPS}
        positions=folded[:,:3];radii=np.linalg.norm(positions,axis=1)
        if not np.array_equal(ids,tracked_ids):raise RuntimeError('Archived tracked IDs differ from direct targets')
        quartiles=bounds[1:-1]
        if not np.array_equal(quartiles,helper.quantile(np,radii,physical_mass,[.25,.5,.75])):
            raise RuntimeError('Archived shell boundaries differ')
        initial_family_counts=[int(np.sum((radii>=lo)&(radii<hi))) for lo,hi in zip(bounds[:-1],bounds[1:])]
        if initial_family_counts!=saved_counts.tolist():raise RuntimeError('Archived initial shell counts differ')
        even=np.array([np.einsum('i,ij,ik->jk',weights[pop],initials[pop][:,3:],initials[pop][:,3:]) for pop in POPS])
        kinetic=np.array([.5*weights[pop]@np.sum(initials[pop][:,3:]**2,axis=1) for pop in POPS])
        matching=dict(positions_bitwise_identical=all(np.array_equal(initials[pop][:,:3],positions) for pop in POPS),
            masses_bitwise_identical=all(np.array_equal(weights[pop],physical_mass) for pop in POPS),
            absolute_velocities_bitwise_identical=all(np.array_equal(abs(initials[pop][:,3:]),abs(folded[:,3:])) for pop in POPS),
            maximum_second_tensor_difference=float(np.max(abs(even-even[0]))),
            maximum_K_difference=float(kinetic.max()-kinetic.min()),
            unique_position_count=int(len(np.unique(positions,axis=0))),
            selected_unique_ID_count=int(len(np.unique(ids))),
            selected_IDs_in_range=bool(np.all((ids>=0)&(ids<COUNT))),explicit_partner_copies=0)
        matching_pass=bool(matching['positions_bitwise_identical'] and matching['masses_bitwise_identical']
            and matching['absolute_velocities_bitwise_identical'] and matching['maximum_second_tensor_difference']<MOMENT_ALLOWANCE
            and matching['maximum_K_difference']<MOMENT_ALLOWANCE
            and matching['unique_position_count']==COUNT and matching['selected_unique_ID_count']==128 and len(ids)==128
            and matching['selected_IDs_in_range'])
        diag=helper.initial_diagnostics(np,positions,folded[:,3:],proposal,ratio,h)
        diag['family_effective_count']=diag.pop('independent_pair_effective_count')
        # Old helper means Rao-Blackwellize the sign. They are NOT actual streams.
        expected_bins=diag.pop('streaming_bins');diag['conditional_fractional_streaming_bins']=expected_bins
        for row in expected_bins:
            row['families']=row.pop('pairs')
            row['interpretation']='Conditional sign expectation before drawing U; separate context, NOT actual sample stream or entrance statistic'
        for row in diag['center_history']:row['families']=row.pop('pairs')
        R=np.hypot(positions[:,0],positions[:,1]);safe=np.maximum(R,1e-30)
        components=np.column_stack(((positions[:,0]*folded[:,3]+positions[:,1]*folded[:,4])/safe,
            (positions[:,0]*folded[:,4]-positions[:,1]*folded[:,3])/safe,folded[:,5]))
        latitude=abs(positions[:,2])/np.maximum(radii,1e-30);actual_bins=[];stream_coverage_failures=[]
        expected_keys={(shell,latitude_id) for shell in range(4) for latitude_id in range(3)}
        present_keys={(row['shell_id'],row['latitude_id']) for row in expected_bins}
        for shell,latitude_id in sorted(expected_keys-present_keys):
            stream_coverage_failures.append(dict(shell_id=shell,latitude_id=latitude_id,reason='Missing sampled streaming bin'))
        for row in expected_bins:
            lo,hi=row['radius_low'],row['radius_high'];mu0,mu1=row['absolute_z_over_r']
            pick=(radii>=lo)&((radii<hi) if row['shell_id']<3 else (radii<=hi))&(latitude>=mu0)&(latitude<mu1)
            denominator=float(physical_mass[pick].sum())
            if not np.any(pick) or not np.isfinite(denominator) or denominator<=0:
                stream_coverage_failures.append(dict(shell_id=row['shell_id'],latitude_id=row['latitude_id'],
                    reason='No positive finite sampled mass in streaming bin'))
                continue
            means={pop:(physical_mass[pick]@(components[pick]*signs[pop][pick,None])/denominator) for pop in POPS}
            second=physical_mass[pick]@(components[pick]**2)/denominator
            if not np.all(np.isfinite(second)) or np.any(second<=0) or not all(np.all(np.isfinite(mean)) for mean in means.values()):
                stream_coverage_failures.append(dict(shell_id=row['shell_id'],latitude_id=row['latitude_id'],
                    reason='Nonpositive or nonfinite component RMS or sampled mean'))
                continue
            difference=means['plus']-means['minus']
            actual_bins.append(dict(shell_id=row['shell_id'],latitude_id=row['latitude_id'],radius_low=lo,radius_high=hi,
                absolute_z_over_r=[mu0,mu1],families=int(pick.sum()),physical_mass=denominator,
                F0_mean_R_phi_z=means['F0'].tolist(),plus_mean_R_phi_z=means['plus'].tolist(),minus_mean_R_phi_z=means['minus'].tolist(),
                plus_minus_mean_difference=difference.tolist(),common_second_R_phi_z=second.tolist(),
                difference_over_RMS=(difference/np.sqrt(second)).tolist(),
                interpretation='ACTUAL common-uniform finite signed sample; no Rao-Blackwell replacement or velocity correction'))
        diag['streaming_bins']=actual_bins
        diag['streaming_bin_coverage_failures']=stream_coverage_failures
        diag['streaming_bin_coverage_pass']=bool(not stream_coverage_failures and len(actual_bins)==12 and present_keys==expected_keys)
        for pop,key in [('F0','reference_momentum'),('plus','raw_plus_momentum'),('minus','raw_minus_momentum')]:
            diag[key]=np.sum(physical_mass[:,None]*initials[pop][:,3:],axis=0).tolist()
        stream=float(np.max(np.abs([z['difference_over_RMS'] for z in actual_bins]))) if actual_bins else None
        sign_certificate=bool(all(np.all(np.isfinite(p)) and np.all((p>=.25-SIGN_PROBABILITY_ROUNDOFF)&(p<=.75+SIGN_PROBABILITY_ROUNDOFF))
            for p in probabilities.values()))
        positive=bool(np.all(np.isfinite(physical_mass)) and np.all(physical_mass>0)
            and np.all(np.isfinite(uniform)) and np.all((uniform>=0)&(uniform<1))
            and all(np.all(np.isfinite(z)) for z in initials.values())
            and all(np.all(np.isfinite(p)) and np.all((p>=0)&(p<=1)) for p in probabilities.values()) and sign_certificate)
        data=f'sample-{seed}.npz'
        shutil.copyfile(inputs/'original-attempt'/archived['data'],args.out/data)
        if sha(args.out/data)!=archived['data_sha256']:raise RuntimeError('Copied sample bytes differ')
        record=dict(seed=seed,method=4,common_uniform_seed=seed+20000,common_uniform_generator='NumPy PCG64',
            data=data,data_sha256=sha(args.out/data),represented_mass=diag['represented_mass'],
            sampler_returned_mass=float(returned_mass.sum()),expected_proposal_mass=Mq,population_checks=weight_check,
            sign_threshold_ranges={pop:[float(p.min()),float(p.max())] for pop,p in probabilities.items()},
            realized_sign_differences=int(np.sum(signs['plus']!=signs['minus'])),
            matching=matching,matching_pass=matching_pass,positive_finite_pass=positive,sign_probability_certificate_pass=sign_certificate,
            initial_diagnostics=diag,maximum_local_stream_difference_over_RMS=stream,
            local_stream_pass=bool(diag['streaming_bin_coverage_pass'] and stream is not None and stream<=.05),
            fixed_shell_boundaries=[0.,*[float(z) for z in quartiles],None],unbounded_boundary_semantics='None means +infinity',
            initial_shell_family_counts=initial_family_counts,covered_shells=[n>=256 for n in initial_family_counts])
        if record!=archived:raise RuntimeError('Recomputed original sample diagnostics differ')
        sample_records.append(record);write(args.out/f'sample-{seed}.json',record)
        samples[seed]=dict(initials=initials,weights=weights,ids=ids,bounds=bounds,family_counts=initial_family_counts,record=record)

    for seed in SEEDS:
        bundle=samples[seed]
        for pop in POPS:
            x=bundle['initials'][pop][:,:3];v=bundle['initials'][pop][:,3:];m=bundle['weights'][pop]
            a,phi=force(x,m);initial_fields[(seed,pop)]=(a,phi)
            with np.load(inputs/'original-attempt'/f'initial-field-{seed}-{pop}.npz') as old:
                if not np.array_equal(a,old['acceleration']) or not np.array_equal(phi,old['potential']):
                    raise RuntimeError('Initial native field differs from original execution')
            if pop!='F0':
                af,pf=initial_fields[(seed,'F0')]
                if not np.array_equal(a,af) or not np.array_equal(phi,pf):raise RuntimeError('Initial native field differs despite identical physical inputs')
            check=direct_check(x,m,a,phi,bundle['ids'],f'initial-direct-{seed}-{pop}')
            b=budgets(x,v,m,a,phi);virial=(2*b['K']+b['W'])/abs(b['W'])
            row=dict(seed=seed,population=pop,budget=b,raw_virial_imbalance=virial,
                virial_pass=bool(abs(virial)<=.05),direct_check=check,
                matching_pass=bundle['record']['matching_pass'],positive_pass=bundle['record']['positive_finite_pass'],
                local_stream_pass=bundle['record']['local_stream_pass'])
            row['all_entrance_pass']=bool(row['virial_pass'] and check['selected_screen_pass'] and row['matching_pass']
                and row['positive_pass'] and row['local_stream_pass'])
            entrance.append(row);write(args.out/f'entrance-{seed}-{pop}.json',row)
            np.savez(args.out/f'initial-field-{seed}-{pop}.npz',acceleration=a,potential=phi)
    write(args.out/'ENTRANCE.json',dict(samples=sample_records,checks=entrance,
        all_entrance_pass=all(x['all_entrance_pass'] for x in entrance),cpu_seconds=time.process_time()-CPU_START))
    if not all(x['all_entrance_pass'] for x in entrance):
        write(args.out/'result.json',dict(status='entrance_veto',scope=configuration()['scope'],configuration=configuration(),
            samples=sample_records,entrance=entrance,no_trajectory_evolved=True,started_utc=start['started_utc'],completed_utc=utc()))
        raise EntranceVeto('Frozen entrance screen failed; both draws retained and no trajectory launched')

    def diagnostic(t,x,v,m,a,phi,bundle,initial_budget):
        r=np.linalg.norm(x,axis=1);q=tied_quantile(np,r,m,QUANTILES)
        R=np.hypot(x[:,0],x[:,1]);safe=np.maximum(R,1e-30)
        components=np.column_stack(((x[:,0]*v[:,0]+x[:,1]*v[:,1])/safe,
            (x[:,0]*v[:,1]-x[:,1]*v[:,0])/safe,v[:,2]))
        angle=np.arccos(np.clip(x[:,2]/np.maximum(r,1e-30),-1,1));azimuth=np.arctan2(x[:,1],x[:,0])
        ys={(ell,order):sph_harm_y(ell,order,angle,azimuth) for ell in range(1,5) for order in range(-ell,ell+1)}
        shell_rows=[]
        for shell,(lo,hi) in enumerate(zip(bundle['bounds'][:-1],bundle['bounds'][1:])):
            pick=(r>=lo)&(r<hi);shell_mass=float(m[pick].sum());count=int(pick.sum())
            coverage=bool(bundle['family_counts'][shell]>=256 and count>=256 and shell_mass>0)
            row=dict(shell=shell,initial_family_count=bundle['family_counts'][shell],particles=count,mass=shell_mass,coverage=coverage)
            if shell_mass>0:
                second=np.einsum('i,ij,ik->jk',m[pick],components[pick],components[pick])/shell_mass
                row.update(mean=(m[pick]@components[pick]/shell_mass).tolist(),second_tensor=second.tolist(),
                    second_diagonal=np.diag(second).tolist(),effective_particles=float(shell_mass**2/np.sum(m[pick]**2)))
                coefficients=[];amplitudes=[]
                for ell in range(1,5):
                    power=0.
                    for order in range(-ell,ell+1):
                        z=m[pick]@ys[(ell,order)][pick]/shell_mass
                        coefficients.append(dict(ell=ell,m=order,real=float(z.real),imag=float(z.imag)));power+=abs(z)**2
                    amplitudes.append(float(np.sqrt(4*np.pi*power)))
                row['mode_coefficients']=coefficients;row['mode_amplitudes']=amplitudes
            else:row.update(mean=None,second_tensor=None,second_diagonal=None,effective_particles=0.,mode_coefficients=[],mode_amplitudes=None)
            shell_rows.append(row)
        center=np.array([tied_quantile(np,x[:,axis],m,[.5])[0] for axis in range(3)])
        radius=float(q[QUANTILES.index(.5)]);history=[]
        for _ in range(12):
            pick=np.linalg.norm(x-center,axis=1)<radius
            if int(pick.sum())<256:break
            center=np.average(x[pick],axis=0,weights=m[pick]);history.append(dict(radius=radius,particles=int(pick.sum()),center=center.tolist()));radius*=.7
        b=budgets(x,v,m,a,phi)
        b.update(energy_relative_error=(b['E']-initial_budget['E'])/abs(initial_budget['E']),
            momentum_error_over_fixed_scale=float(np.linalg.norm(np.array(b['P'])-initial_budget['P'])/P_SCALE),
            angular_vector_error_over_fixed_scale=float(np.linalg.norm(np.array(b['L'])-initial_budget['L'])/L_SCALE))
        return dict(time=t,mass=float(m.sum()),quantile_radii=q.tolist(),shells=shell_rows,
            budget=b,inner_center=center.tolist(),center_history=history)

    def flush_case(case):
        temporary=args.out/(case['id']+'.tmp.npz');target=args.out/(case['id']+'.npz')
        np.savez(temporary,times=np.array([x['time'] for x in case['records']]),
            states=np.array(case['states']),tracked_times=np.array(case['tracked_times']),tracked_states=np.array(case['tracked_states']),
            tracked_particle_ids=case['bundle']['ids'],particle_mass=case['mass'],initial=case['initial'],
            snapshot_particle_ids=np.arange(COUNT),quantile_fractions=np.array(QUANTILES),
            time_unit=np.array('Isochrone code time: G=M0=1,b=.5; not Gyr'),
            position_unit=np.array('Isochrone code length, b=.5'),
            velocity_unit=np.array('Isochrone code length/code time'),
            fixed_shell_boundaries=case['bundle']['bounds'],
            last_complete_x=case['checkpoint']['x'],last_complete_v=case['checkpoint']['v'],
            last_complete_acceleration=case['checkpoint']['a'],last_complete_potential=case['checkpoint']['phi'],
            last_complete_time=case['checkpoint']['time'])
        temporary.replace(target)
        write(args.out/(case['id']+'.json'),dict(id=case['id'],seed=case['seed'],population=case['pop'],dt=case['dt'],
            records=case['records'],data=target.name,last_complete_time=case['checkpoint']['time'],
            coordinate_frame='Original inertial Cartesian frame, no recenter or renormalization'))
        metadata=args.out/(case['id']+'.json')
        write(args.out/(case['id']+'.receipt.json'),dict(id=case['id'],last_complete_time=case['checkpoint']['time'],
            snapshot=dict(path=target.name,sha256=sha(target)),
            diagnostics=dict(path=metadata.name,sha256=sha(metadata)),
            interpretation='Use this pair only if both hashes and recorded times agree; files replace separately'))

    def record(case,t):
        x,v,a,phi=case['x'],case['v'],case['a'],case['phi']
        case['records'].append(diagnostic(t,x,v,case['mass'],a,phi,case['bundle'],case['initial_budget']))
        case['states'].append(np.column_stack((x,v)).copy())
        case['checkpoint']=dict(time=t,x=x.copy(),v=v.copy(),a=a.copy(),phi=phi.copy())
        flush_case(case)
        write(args.out/'status.json',dict(stage='evolving',case=case['id'],time=t,
            cpu_seconds=time.process_time()-CPU_START,wall_seconds=time.monotonic()-WALL_START))

    def case_screen(case,end_check):
        first=case['records'][0];qd=[];md=[];sd=[];coverage=True
        primary=[QUANTILES.index(q) for q in PRIMARY_QUANTILES]
        for row in case['records']:
            qd.append(float(np.max(abs(np.array(row['quantile_radii'])[primary]/np.array(first['quantile_radii'])[primary]-1))))
            for old,new in zip(first['shells'],row['shells']):
                if old['initial_family_count']<256:continue
                if not new['coverage']:coverage=False;continue
                md.append(abs(new['mass']/old['mass']-1))
                initial_second=np.array(old['second_diagonal']);current_second=np.array(new['second_diagonal'])
                if np.any(initial_second<=0):coverage=False;continue
                sd.append(float(np.max(abs(current_second/initial_second-1))))
        metrics=dict(maximum_primary_quantile_drift=max(qd),maximum_covered_shell_mass_drift=max(md) if md else None,
            maximum_covered_diagonal_second_drift=max(sd) if sd else None,coverage_retained=coverage,
            maximum_energy_relative_error=max(abs(r['budget']['energy_relative_error']) for r in case['records']),
            maximum_momentum_fixed_error=max(r['budget']['momentum_error_over_fixed_scale'] for r in case['records']),
            maximum_angular_vector_fixed_error=max(r['budget']['angular_vector_error_over_fixed_scale'] for r in case['records']))
        flags=dict(primary_quantile_adjustment=bool(metrics['maximum_primary_quantile_drift']>=.05),
            covered_mass_adjustment=bool(metrics['maximum_covered_shell_mass_drift'] is None or metrics['maximum_covered_shell_mass_drift']>=.05),
            covered_second_adjustment=bool(metrics['maximum_covered_diagonal_second_drift'] is None or metrics['maximum_covered_diagonal_second_drift']>=.05),
            coverage_failure=not coverage)
        numerical=dict(energy=bool(metrics['maximum_energy_relative_error']<1e-4),
            momentum=bool(metrics['maximum_momentum_fixed_error']<1e-6),
            angular_vector=bool(metrics['maximum_angular_vector_fixed_error']<1e-4),
            endpoint_selected_force=bool(end_check['selected_screen_pass']))
        return dict(metrics=metrics,rapid_adjustment_flags=flags,numerical_screens=numerical,
            interpretation='Flags require matched F0 and independent-draw context; none alone establishes instability')

    completed=[];profile=None;all_steps=6*int(round(END/DT))+3*int(round(END/FINE_DT))
    cases=configuration()['cases']
    for index,setting in enumerate(cases):
        seed,pop,dt=setting['seed'],setting['population'],setting['dt'];bundle=samples[seed]
        mass=bundle['weights'][pop].copy();a0,p0=initial_fields[(seed,pop)];initial=bundle['initials'][pop]
        initial_budget=budgets(initial[:,:3],initial[:,3:],mass,a0,p0)
        case=dict(id=f'run-{seed}-{pop}-dt{dt:g}',seed=seed,pop=pop,dt=dt,bundle=bundle,mass=mass,initial=initial,
            x=initial[:,:3].copy(),v=initial[:,3:].copy(),a=a0.copy(),phi=p0.copy(),
            initial_budget=initial_budget,records=[],states=[],tracked_times=[0.],
            tracked_states=[initial[bundle['ids']].copy()],checkpoint=None)
        ACTIVE=case;case_cpu=time.process_time();record(case,0.)
        steps=int(round(END/dt));diag_stride=int(round(.5/dt));track_stride=int(round(.05/dt))
        for step in range(1,steps+1):
            case['v']+=.5*dt*case['a']
            case['x']+=dt*case['v']
            case['a'],case['phi']=force(case['x'],mass)
            case['v']+=.5*dt*case['a']
            if not np.all(np.isfinite(case['x'])) or not np.all(np.isfinite(case['v'])):raise RuntimeError('Nonfinite complete KDK state')
            t=step*dt
            if step%track_stride==0:
                case['tracked_times'].append(t);case['tracked_states'].append(np.column_stack((case['x'],case['v']))[bundle['ids']].copy())
            if step%diag_stride==0:record(case,t)
            if index==0 and step==int(round(PREFIX/dt)):
                with np.load(inputs/'original-attempt'/(case['id']+'.npz')) as original_prefix:
                    if not np.array_equal(np.array(case['states']),original_prefix['states']) or not np.array_equal(np.array(case['tracked_states']),original_prefix['tracked_states']):
                        raise RuntimeError('Repeated complete prefix states/tracks differ from original')
                    if not np.array_equal(np.array(case['tracked_times']),original_prefix['tracked_times']):
                        raise RuntimeError('Repeated recorded prefix times differ from original')
                if case['records']!=load(inputs/'original-attempt'/(case['id']+'.json'))['records']:
                    raise RuntimeError('Repeated prefix diagnostics differ from original')
                write(args.out/'PREFIX_REPLAY.json',dict(bitwise_states_and_tracks=True,diagnostics_identical=True,time=t,
                    interpretation='Duplicate archived prefix, not a new sample'))
                prefix_cpu=time.process_time()-case_cpu
                projected=time.process_time()-CPU_START+1.25*(all_steps-step)*prefix_cpu/step
                profile=dict(case=case['id'],prefix_time=t,prefix_steps=step,prefix_cpu_seconds=prefix_cpu,
                    elapsed_setup_and_prefix_cpu=time.process_time()-CPU_START,projected_total_cpu_seconds=projected,
                    cutoff=CPU_SOFT,proceed=bool(projected<CPU_SOFT),overhead_fraction=.25)
                write(args.out/'PROFILE.json',profile)
                if not profile['proceed']:raise BudgetReached('Whole-prefix projection does not fit the frozen allocation')
        if not np.array_equal(mass,bundle['weights'][pop]):raise RuntimeError('Fixed physical masses changed')
        end_check=direct_check(case['x'],mass,case['a'],case['phi'],bundle['ids'],'end-direct-'+case['id'])
        summary=dict(id=case['id'],seed=seed,population=pop,dt=dt,duration=END,
            sample_data_sha256=bundle['record']['data_sha256'],data=case['id']+'.npz',data_sha256=sha(args.out/(case['id']+'.npz')),
            records=case['records'],initial_budget=initial_budget,end_direct_check=end_check,
            decision=case_screen(case,end_check),cpu_seconds=time.process_time()-case_cpu)
        completed.append(summary);write(args.out/'partial.json',dict(status='partial',completed=completed,
            samples=sample_records,entrance=entrance,profile=profile,cpu_seconds=time.process_time()-CPU_START))
        print(json.dumps(dict(stage='case_complete',id=case['id'],cpu_seconds=time.process_time()-CPU_START,
            rapid_adjustment_flags=summary['decision']['rapid_adjustment_flags'],numerical_screens=summary['decision']['numerical_screens'])),flush=True)
        ACTIVE=None

    refinements=[]
    primary=[QUANTILES.index(q) for q in PRIMARY_QUANTILES]
    for pop in POPS:
        coarse=next(r for r in completed if r['seed']==SEEDS[0] and r['population']==pop and r['dt']==DT)
        fine=next(r for r in completed if r['seed']==SEEDS[0] and r['population']==pop and r['dt']==FINE_DT)
        if coarse['sample_data_sha256']!=fine['sample_data_sha256']:raise RuntimeError('Coarse/fine initial sample differs')
        expected_records=int(round(END/.5))+1
        if len(coarse['records'])!=expected_records or len(fine['records'])!=expected_records:
            raise RuntimeError('Coarse/fine comparison requires every frozen diagnostic epoch')
        quantile=massdiff=second=mode=0.;coverage=True
        q0=np.array(coarse['records'][0]['quantile_radii'])[primary]
        for c,f in zip(coarse['records'],fine['records']):
            if c['time']!=f['time']:raise RuntimeError('Coarse/fine recorded clock differs')
            quantile=max(quantile,float(np.max(abs(np.array(c['quantile_radii'])[primary]-np.array(f['quantile_radii'])[primary])/q0)))
            for c0,cs,fs in zip(coarse['records'][0]['shells'],c['shells'],f['shells']):
                if c0['initial_family_count']<256:continue
                if not cs['coverage'] or not fs['coverage']:coverage=False;continue
                massdiff=max(massdiff,abs(cs['mass']-fs['mass'])/c0['mass'])
                second=max(second,float(np.max(abs(np.array(cs['second_diagonal'])-np.array(fs['second_diagonal']))/np.array(c0['second_diagonal']))))
                mode=max(mode,float(np.max(abs(np.array(cs['mode_amplitudes'])-np.array(fs['mode_amplitudes'])))))
        refinements.append(dict(population=pop,maximum_primary_quantile_fractional_difference=quantile,
            maximum_covered_mass_fractional_difference=massdiff,maximum_covered_second_fractional_difference=second,
            maximum_absolute_mode_amplitude_difference=mode,coverage_retained=coverage,
            fractional_drift_step_screen_pass=bool(coverage and max(quantile,massdiff,second)<.01),
            mode_status='Recorded absolute difference; no relative small-mode criterion'))
    unchanged=all(sha(inputs/r['path'])==r['sha256'] for r in start['snapshots']);assert unchanged
    result=dict(status='complete',scope=configuration()['scope'],configuration=configuration(),
        started_utc=start['started_utc'],completed_utc=utc(),samples=sample_records,entrance=entrance,
        completed=completed,timestep_refinements=refinements,profile=profile,frozen_inputs_unchanged=unchanged,
        source_snapshots=start['snapshots'],cpu_seconds=time.process_time()-CPU_START,wall_seconds=time.monotonic()-WALL_START,
        numerical_qualification=bool(all(all(r['decision']['numerical_screens'].values()) for r in completed)
            and all(r['fractional_drift_step_screen_pass'] for r in refinements)),
        rapid_adjustment_flags_present=bool(any(any(r['decision']['rapid_adjustment_flags'].values()) for r in completed)),
        interpretation='Completion and numerical checks do not prove stability; inspect F0/draw context and all flags',
        limitations=configuration()['limits'])
    write(args.out/'result.json',result);write(args.out/'TERMINAL.json',dict(status='complete',
        cpu_seconds=result['cpu_seconds'],wall_seconds=result['wall_seconds'],completed_utc=result['completed_utc']))
    (args.out/'COMPLETE').write_text('Nine-case short screen complete; flags/numerical qualification separate, no stability proof.\n')
    print(json.dumps(dict(stage='complete',cases=len(completed),cpu_seconds=result['cpu_seconds'],
        numerical_qualification=result['numerical_qualification'],rapid_adjustment_flags_present=result['rapid_adjustment_flags_present']),indent=2),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--protocol',type=Path,default=ROOT/'research/discovery-20261001/TWINS_SINGLE_POSITION_COMPLETION_PROTOCOL.md')
    parser.add_argument('--resource-review',type=Path,default=ROOT/'research/discovery-20261001/TWINS_RESOURCE_REVIEW_04.md')
    parser.add_argument('--parent',type=Path,default=ROOT/'results/discovery-20261001/twins/single-position-01')
    parser.add_argument('--force-baseline',type=Path,default=ROOT/'results/discovery-20261001/twins/live-force-preflight-02')
    parser.add_argument('--opening',type=Path,default=ROOT/'results/discovery-20261001/twins/force-opening-refinement-02')
    parser.add_argument('--continuum',type=Path,default=ROOT/'results/discovery-20261001/twins/continuum-p1-02')
    parser.add_argument('--continuum-formula',type=Path,default=ROOT/'results/discovery-20261001/twins/continuum-formula-01')
    args=parser.parse_args()
    try:run(args)
    except BaseException as error:
        if OWNED==args.out.resolve() and not (OWNED/'TERMINAL.json').exists():
            # Only completed diagnostic checkpoints are publishable. A interrupted
            # half kick/drift never masquerades as a full synchronized state.
            if ACTIVE is not None and ACTIVE.get('checkpoint') is not None:
                checkpoint=ACTIVE['checkpoint']
                np_module=sys.modules.get('numpy')
                if np_module is not None:
                    np_module.savez(OWNED/'interrupted-checkpoint.npz',
                        time=checkpoint['time'],x=checkpoint['x'],v=checkpoint['v'],
                        acceleration=checkpoint['a'],potential=checkpoint['phi'],mass=ACTIVE['mass'])
            status='vetoed' if isinstance(error,EntranceVeto) else 'failed'
            write(OWNED/'TERMINAL.json',dict(status=status,error_type=type(error).__name__,error=str(error),
                completed_utc=utc(),cpu_seconds=time.process_time()-CPU_START,wall_seconds=time.monotonic()-WALL_START,
                last_complete_checkpoint=ACTIVE['checkpoint']['time'] if ACTIVE is not None and ACTIVE.get('checkpoint') is not None else None))
            (OWNED/'FAILED').write_text(type(error).__name__+': '+str(error)+'\n')
        raise


if __name__=='__main__':main()
