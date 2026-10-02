"""Frozen same-sample analytic isochrone phase control.

--prepare copies immutable inputs and selects validation IDs without importing
NumPy/SciPy/AGAMA or mapping/integrating an orbit. --run requires a separately
reviewed launch and the original live matrix's terminal closure. No tree force,
resampling, phase randomization, mass correction or live-halo claim is added.
"""
import os
for _name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import argparse
import ast
import copy
import datetime
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import shutil
import signal
import struct
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT/'results/discovery-20261001/twins/single-position-completion-01'
SEEDS, POPS = (50511,50512), ('F0','plus','minus')
COUNT, END, EPOCHS = 16384, 15., tuple(.5*i for i in range(31))
QUANTILES = (.01,.05,.1,.25,.5,.75,.9,.95,.99)
PRIMARY = (.1,.25,.5,.75,.9)
CPU_SOFT, CPU_HARD, INTERNAL_WALL = 90, 100, 170
EXPECTED = {
    'sample-50511.npz':'4d46b37f8d88d829e5a4a8a14e75ac5f19633b093cb6434345e27618b80a88b4',
    'sample-50512.npz':'6dc37b3314056da29e5ff63984985aba67818a2b91b604c1349fef79ae30d723',
    'source.py':'6bdbc827f17c98f785558debec26047a69238f4fd9b2fc2f57a36ab21fe4e5f6',
    'agama.so':'f6c04e4941aff3538d3bb08f6446d731b788d85406af94092cf856fbd139d000',
    'live-launch-config.json':'f1c26a918ea9bffb3feb17341e0dd93b71d464a4fa71209dbd46c411732c7aee',
}
ALLOWANCES = dict(action_scaled=1e-10, frequency_relative=1e-10,
    roundtrip_position_scaled=1e-10, roundtrip_velocity_scaled=1e-10,
    initial_profile_scaled=1e-8, all_path_energy_scaled=1e-10,
    all_path_L_vector_scaled=1e-10, selected_DOP_state_scaled=1e-8,
    selected_DOP_energy_scaled=1e-9, selected_DOP_L_vector_scaled=1e-9)
RUN_CPU, RUN_WALL, OWNED = None, None, None


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    def numeric(item):
        if hasattr(item, 'item'):
            return item.item()
        raise TypeError('Unsupported JSON type: '+type(item).__name__)
    temporary = path.with_name(path.name+'.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False, default=numeric)+'\n')
    temporary.replace(path)


def read_numeric_npy(archive, key):
    """Read selected archived numeric inputs with the standard library only."""
    with zipfile.ZipFile(archive) as z:
        raw = z.read(key+'.npy')
    assert raw[:6] == b'\x93NUMPY'
    major = raw[6]
    length_bytes = 2 if major == 1 else 4
    assert major in (1,2)
    header_length = int.from_bytes(raw[8:8+length_bytes], 'little')
    offset = 8+length_bytes
    metadata = ast.literal_eval(raw[offset:offset+header_length].decode('latin1'))
    assert not metadata['fortran_order'] and metadata['descr'] in ('<i8','<f8')
    count = math.prod(metadata['shape'])
    values = struct.unpack('<'+('q' if metadata['descr'] == '<i8' else 'd')*count, raw[offset+header_length:])
    return metadata['shape'], values


def selection(archive):
    shape, ids = read_numeric_npy(archive, 'selected_particle_ids')
    assert shape == (128,) and len(set(ids)) == 128
    fshape, folded = read_numeric_npy(archive, 'folded_sample')
    ashape, actions = read_numeric_npy(archive, 'actions')
    assert fshape == (COUNT,6) and ashape == (COUNT,3)
    selected = {}
    def add(index, reason):
        selected.setdefault(int(index), []).append(reason)
    for stratum, index in enumerate(ids[::16]):
        add(index, f'first retained direct target in original radial-rank stratum {stratum}')
    scores = {name:[] for name in ('binding','radius','circularity','turning','near_circular')}
    for i in range(COUNT):
        x,y,z,vx,vy,vz = folded[6*i:6*i+6]
        jr,jz,lz = actions[3*i:3*i+3]
        radius = math.sqrt(x*x+y*y+z*z)
        speed = math.sqrt(vx*vx+vy*vy+vz*vz)
        L = jz+abs(lz)
        I = jr+.5*(L+math.sqrt(L*L+2))
        binding = .5/(I*I)
        maximum_L = (1-binding)/math.sqrt(2*binding)
        scores['binding'].append(binding)
        scores['radius'].append(radius)
        scores['circularity'].append(L/maximum_L)
        scores['turning'].append(abs(x*vx+y*vy+z*vz)/(radius*speed) if radius*speed else 0.)
        scores['near_circular'].append(jr/(math.sqrt(.5)+jr+L))
    add(min(range(COUNT),key=scores['binding'].__getitem__), 'weakest bound archived action')
    add(max(range(COUNT),key=scores['radius'].__getitem__), 'largest initial radius')
    add(min(range(COUNT),key=scores['circularity'].__getitem__), 'smallest action circularity')
    add(min(range(COUNT),key=scores['turning'].__getitem__), 'smallest initial absolute radial-velocity fraction')
    add(min(range(COUNT),key=scores['near_circular'].__getitem__), 'smallest radial-action fraction')
    return [dict(particle_id=index, reasons=reasons) for index,reasons in selected.items()]


def pure_diagnostic_nodes(source):
    tree = ast.parse(source)
    candidates = [node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef)]
    tied = copy.deepcopy(next(node for node in candidates if node.name == 'tied_quantile'))
    original = next(node for node in candidates if node.name == 'diagnostic')
    prefix = []
    for statement in original.body:
        if (isinstance(statement,ast.Assign) and isinstance(statement.value,ast.Call)
            and isinstance(statement.value.func,ast.Name) and statement.value.func.id == 'budgets'):
            break
        prefix.append(copy.deepcopy(statement))
    returned = copy.deepcopy(original.body[-1])
    assert isinstance(returned,ast.Return) and isinstance(returned.value,ast.Call)
    returned.value.keywords = [kw for kw in returned.value.keywords if kw.arg != 'budget']
    diagnostic = copy.deepcopy(original)
    diagnostic.name = 'profile'
    diagnostic.args.args = [copy.deepcopy(arg) for arg in original.args.args if arg.arg not in ('a','phi','initial_budget')]
    diagnostic.body = prefix+[returned]
    assert ast.dump(ast.Module(body=prefix,type_ignores=[]),include_attributes=False) == ast.dump(
        ast.Module(body=diagnostic.body[:-1],type_ignores=[]),include_attributes=False)
    module = ast.fix_missing_locations(ast.Module(body=[tied,diagnostic],type_ignores=[]))
    prefix_ast = ast.dump(ast.Module(body=prefix,type_ignores=[]),include_attributes=False)
    receipt = dict(original_pure_prefix_AST_sha256=hashlib.sha256(prefix_ast.encode()).hexdigest(),
        pure_prefix_AST_identical=True, original_return_fields_retained_except=['budget'],
        no_live_self_energy_or_momentum_gate_imported=True)
    return module, receipt


def configuration(selected):
    return dict(schema_version=1, scope='Same-sample finite phase/cohort control; different analytic fixed Hamiltonian',
        model='External unsoftened spherical isochrone G=M0=1,b=.5; no self-gravity/bar/softening/collisions',
        seeds=list(SEEDS), populations=list(POPS), particle_count=COUNT, times=list(EPOCHS),
        samples='Exact archived masses, positions, folded velocities, actions, stored signs/uniforms and fixed bins; no resampling',
        propagation='Archived actions plus recovered canonical angles; analytic frequencies; mapper at positive/negative time and exact velocity reversal',
        initial_record='Original saved Cartesian state; mapped T0 is independently checked and recorded separately',
        diagnostic='AST-identical original profile arithmetic before the live budget; same shells, quantiles, modes, origin and coverage',
        selected_paths=selected, selected_path_senses=['folded_positive_Lz','complete_velocity_reversal'],
        selected_path_rule='Eight original radial-rank targets plus deterministic initial weak/radial/turning/circular extremes; all ties choose first index',
        independent_integrator=dict(method='DOP853',rtol=2e-11,atol=2e-12,max_step=.1,t_eval=list(EPOCHS)),
        allowances=ALLOWANCES, all_outliers_retained=True,
        analytic_budget='E=sum m(v²/2+Phi0); each orbit conserves vector L; finite-sample P is not an invariant',
        old_adjustment_threshold=.05, old_flags_preserved=True,
        cpu_soft=CPU_SOFT,cpu_hard=CPU_HARD,internal_wall=INTERNAL_WALL,
        external_wall=dict(timeout=175,kill_after=5), force_threads=1,nice=10,
        profile=dict(epochs=[0.,.5],seed=SEEDS[0],all_three_populations=True,
            remaining_seed_epoch_records=60,safety=1.25,selected_check_reservation=10.,stop_above=CPU_SOFT),
        exclusions=['Not a matched softened continuum control','Not a live collective stability or bar-torque test',
            'Similar excursions do not calibrate false-positive rates','No old numerical or adjustment criterion is changed'])


def installed_module_snapshot():
    """Freeze selected environment files by path, without scientific imports."""
    site = ROOT/'.venv/lib/python3.11/site-packages'
    paths = [('python-executable',Path(sys.executable).resolve()),
        ('numpy',site/'numpy/__init__.py'),
        ('numpy.core',site/'numpy/core/_multiarray_umath.cpython-311-x86_64-linux-gnu.so'),
        ('scipy',site/'scipy/__init__.py'),
        ('scipy.special.native',site/'scipy/special/_special_ufuncs.cpython-311-x86_64-linux-gnu.so'),
        ('scipy.special.gufuncs',site/'scipy/special/_gufuncs.cpython-311-x86_64-linux-gnu.so'),
        ('scipy.special.sph_harm_y',site/'scipy/special/_multiufuncs.py'),
        ('scipy.special.input-validation',site/'scipy/special/_input_validation.py'),
        ('scipy.integrate.solve_ivp',site/'scipy/integrate/_ivp/ivp.py'),
        ('scipy.integrate.rk',site/'scipy/integrate/_ivp/rk.py'),
        ('scipy.integrate.base',site/'scipy/integrate/_ivp/base.py'),
        ('scipy.integrate.common',site/'scipy/integrate/_ivp/common.py')]
    assert sys.version.split()[0] == '3.11.14', 'Prepare with the original pinned project interpreter'
    return dict(scope='Selected interpreter, mapping/profile and DOP853 environment files; not a full dependency closure',
        python=sys.version.split()[0], scientific_imports=False,
        modules=[dict(name=name,path=str(path.resolve()),sha256=sha(path),bytes=path.stat().st_size) for name,path in paths])


def prepare(out, protocol):
    out.mkdir(parents=True,exist_ok=False)
    inputs = out/'inputs'
    inputs.mkdir()
    cpu,wall = time.process_time(),time.monotonic()
    live_start = load(LIVE/'START.json')
    artifacts = {
        'phase_control.py':Path(__file__), 'protocol.md':protocol,
        'assessment.md':ROOT/'research/discovery-20261001/TWINS_NEXT_STAGE_ASSESSMENT_01.md',
        'resource-review-04.md':ROOT/'research/discovery-20261001/TWINS_RESOURCE_REVIEW_04.md',
        'mixed-ledger-04.json':ROOT/'results/discovery-20261001/twins/compute-review-04/result.json',
        'live-START.json':LIVE/'START.json','live-launch-config.json':LIVE/'launch-config.json',
        'live-versions.json':LIVE/'versions.json',
        'source.py':LIVE/'inputs/scripts/discovery/twins_single_position_completion.py',
        'agama.so':LIVE/'inputs/base/build/noise-sweep/Agama-stable-v2/agama.so',
        'AGAMA-LICENSE':LIVE/'inputs/base/build/noise-sweep/Agama-stable-v2/LICENSE',
        'frozen-populations.json':LIVE/'inputs/base/evidence/frozen-populations.json',
        'exact-moments-derivation.md':LIVE/'inputs/base/evidence/exact-moments-derivation.md',
    }
    for seed in SEEDS:
        artifacts[f'sample-{seed}.npz'] = LIVE/f'sample-{seed}.npz'
        for pop in POPS:
            ident = f'run-{seed}-{pop}-dt0.01'
            artifacts[ident+'.json'] = LIVE/(ident+'.json')
            artifacts[ident+'.receipt.json'] = LIVE/(ident+'.receipt.json')
    snapshots = []
    for name,original in artifacts.items():
        if name in EXPECTED:
            assert sha(original) == EXPECTED[name], 'Unexpected input hash: '+name
        target = inputs/name
        shutil.copyfile(original,target)
        assert sha(target) == sha(original), 'Source changed while freezing: '+name
        snapshots.append(dict(path=name,sha256=sha(target),bytes=target.stat().st_size))
    for seed in SEEDS:
        for pop in POPS:
            ident = f'run-{seed}-{pop}-dt0.01'
            receipt = load(inputs/(ident+'.receipt.json'))
            assert receipt['last_complete_time'] == END
            assert receipt['diagnostics']['sha256'] == sha(inputs/(ident+'.json'))
            assert load(inputs/(ident+'.json'))['last_complete_time'] == END
    copied_agama = next(r for r in live_start['snapshots'] if r['path'] == 'base/build/noise-sweep/Agama-stable-v2/agama.so')
    assert sha(inputs/'agama.so') == copied_agama['sha256']
    selected = {str(seed):selection(inputs/f'sample-{seed}.npz') for seed in SEEDS}
    write(out/'launch-config.json',configuration(selected))
    module,methods = pure_diagnostic_nodes((inputs/'source.py').read_text())
    helper = ast.unparse(module)+'\n'
    (inputs/'pure_profiles.py').write_text(helper)
    snapshots.append(dict(path='pure_profiles.py',sha256=sha(inputs/'pure_profiles.py'),bytes=(inputs/'pure_profiles.py').stat().st_size))
    write(out/'METHOD-RECEIPT.json',methods)
    write(out/'PREPARED-MODULES.json',installed_module_snapshot())
    frozen = dict(prepared_utc=utc(),status='prepared_not_executed',scientific_imports_or_evolution=False,
        snapshots=snapshots, launch_config_sha256=sha(out/'launch-config.json'),
        methods_sha256=sha(out/'METHOD-RECEIPT.json'), original_live_parent='single-position-completion-01',
        prepared_modules_sha256=sha(out/'PREPARED-MODULES.json'),
        live_matrix_terminal_required_before_execution=True,
        prepare_cpu_seconds=time.process_time()-cpu,prepare_wall_seconds=time.monotonic()-wall)
    write(out/'FROZEN.json',frozen)
    (out/'PREPARED').write_text('Inputs frozen; scientific execution requires root source review.\n')
    print(json.dumps(dict(status='prepared_not_executed',frozen_sha256=sha(out/'FROZEN.json'),
        prepare_cpu_seconds=frozen['prepare_cpu_seconds'],selection_sizes={k:len(v) for k,v in selected.items()})))


class BudgetReached(RuntimeError):
    pass


def limits():
    hard = resource.getrlimit(resource.RLIMIT_CPU)[1]
    hard = CPU_HARD if hard == resource.RLIM_INFINITY else min(hard,CPU_HARD)
    resource.setrlimit(resource.RLIMIT_CPU,(min(CPU_SOFT,hard-1),hard))
    def stop(*_):
        raise BudgetReached('Finite analytic phase-control allowance reached')
    for sig in (signal.SIGXCPU,signal.SIGTERM,signal.SIGALRM):
        signal.signal(sig,stop)
    signal.alarm(INTERNAL_WALL)
    if os.getpriority(os.PRIO_PROCESS,0) < 10:
        os.nice(10-os.getpriority(os.PRIO_PROCESS,0))


def strip_budget(row):
    return {key:value for key,value in row.items() if key != 'budget'}


def profile_difference(actual,expected):
    """Compare numeric profile values; structural/count differences are failures."""
    worst = 0.
    def visit(a,b):
        nonlocal worst
        if isinstance(a,dict):
            assert set(a) == set(b)
            for k in a:
                visit(a[k],b[k])
        elif isinstance(a,list):
            assert len(a) == len(b)
            for aa,bb in zip(a,b):
                visit(aa,bb)
        elif a is None or isinstance(a,(str,bool,int)):
            assert a == b, 'Profile structure/count mismatch'
        else:
            assert math.isfinite(float(a)) and math.isfinite(float(b))
            worst = max(worst,abs(float(a)-float(b))/(1+abs(float(b))))
    visit(actual,expected)
    return worst


def run(out):
    global RUN_CPU,RUN_WALL,OWNED
    assert (out/'PREPARED').exists() and not (out/'EXECUTION-START.json').exists()
    assert not (out/'TERMINAL.json').exists()
    OWNED = out
    RUN_CPU,RUN_WALL = time.process_time(),time.monotonic()
    limits()
    inputs = out/'inputs'
    frozen = load(out/'FROZEN.json')
    assert all(sha(inputs/r['path']) == r['sha256'] for r in frozen['snapshots'])
    assert sha(Path(__file__)) == sha(inputs/'phase_control.py'), 'Executed source differs from frozen source'
    assert sha(out/'launch-config.json') == frozen['launch_config_sha256']
    assert sha(out/'METHOD-RECEIPT.json') == frozen['methods_sha256']
    assert sha(out/'PREPARED-MODULES.json') == frozen['prepared_modules_sha256']
    prepared_modules = load(out/'PREPARED-MODULES.json')
    assert prepared_modules['python'] == sys.version.split()[0]
    assert all(sha(row['path']) == row['sha256'] for row in prepared_modules['modules'])
    config = load(out/'launch-config.json')
    assert config == configuration(config['selected_paths'])
    # The live matrix may close after preparation. Capture its terminal record
    # before importing scientific modules, retaining the earlier FROZEN unchanged.
    assert (LIVE/'COMPLETE').exists() and (LIVE/'TERMINAL.json').exists()
    live_result = load(LIVE/'result.json')
    assert live_result['status'] == 'complete' and len(live_result['completed']) == 9
    assert live_result['frozen_inputs_unchanged'] is True
    closure = out/'live-closure'
    closure.mkdir()
    closure_rows = []
    for name in ('result.json','TERMINAL.json','COMPLETE'):
        shutil.copyfile(LIVE/name,closure/name)
        assert sha(closure/name) == sha(LIVE/name)
        closure_rows.append(dict(path=name,sha256=sha(closure/name),bytes=(closure/name).stat().st_size))
    write(out/'LIVE-CLOSURE-FROZEN.json',dict(utc=utc(),files=closure_rows,
        original_numerical_qualification=live_result['numerical_qualification'],
        qualification_not_required_for_diagnostic=True))
    write(out/'EXECUTION-START.json',dict(utc=utc(),prepared_frozen_sha256=sha(out/'FROZEN.json'),
        source_sha256=sha(inputs/'phase_control.py'),protocol_sha256=sha(inputs/'protocol.md'),
        closure_frozen_sha256=sha(out/'LIVE-CLOSURE-FROZEN.json')))
    import numpy as np
    import scipy
    import scipy.special._special_ufuncs as special_native
    from scipy.special import sph_harm_y
    from scipy.integrate import solve_ivp
    spec = importlib.util.spec_from_file_location('agama',inputs/'agama.so')
    agama = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agama)
    assert Path(agama.__file__).resolve() == (inputs/'agama.so').resolve()
    original_versions = load(inputs/'live-versions.json')
    assert np.__version__ == original_versions['numpy'] and scipy.__version__ == original_versions['scipy']
    module_records = []
    for name,path in [('numpy',np.__file__),('numpy.core',np.core._multiarray_umath.__file__),
        ('scipy',scipy.__file__),('scipy.special.native',special_native.__file__),('agama',agama.__file__),
        ('scipy.special.sph_harm_y',sys.modules[sph_harm_y.__module__].__file__),
        ('scipy.integrate.solve_ivp',sys.modules[solve_ivp.__module__].__file__)]:
        module_records.append(dict(name=name,path=str(path),sha256=sha(path)))
    write(out/'MODULES.json',dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,modules=module_records))
    prepared_by_name = {r['name']:r for r in prepared_modules['modules']}
    assert all((r['name'] == 'agama' or r['sha256'] == prepared_by_name[r['name']]['sha256']) for r in module_records)
    namespace = dict(np=np,sph_harm_y=sph_harm_y,QUANTILES=QUANTILES)
    helper_tree,_ = pure_diagnostic_nodes((inputs/'source.py').read_text())
    assert ast.unparse(helper_tree)+'\n' == (inputs/'pure_profiles.py').read_text()
    exec(compile(helper_tree,str(inputs/'pure_profiles.py'),'exec'),namespace)
    profile = namespace['profile']
    potential = agama.Potential(type='Isochrone',mass=1,scaleRadius=.5)
    finder,mapper = agama.ActionFinder(potential),agama.ActionMapper(potential)
    bundles,checks = {},[]

    def invariants(states):
        x,v = states[:,:3],states[:,3:]
        E = .5*np.sum(v*v,axis=1)-1/(.5+np.sqrt(.25+np.sum(x*x,axis=1)))
        return E,np.cross(x,v)

    def state_error(a,b):
        return dict(position=float(np.max(abs(a[:,:3]-b[:,:3])/(.5+abs(b[:,:3])))),
            velocity=float(np.max(abs(a[:,3:]-b[:,3:])/(math.sqrt(2)+abs(b[:,3:])))))

    def mapped(bundle,t,sense,ids=None):
        actions = bundle['actions'] if ids is None else bundle['actions'][ids]
        initial_angles = bundle['angles'] if ids is None else bundle['angles'][ids]
        frequencies = bundle['frequencies'] if ids is None else bundle['frequencies'][ids]
        angles = np.mod(initial_angles+sense*t*frequencies,2*np.pi)
        with agama.setNumThreads(1):
            state = mapper(np.column_stack((actions,angles)))
        if state.shape != (len(actions),6) or not np.all(np.isfinite(state)):
            np.savez_compressed(out/f'failed-mapping-{bundle["seed"]}-{t:g}-{sense}.npz',
                particle_ids=np.arange(COUNT) if ids is None else ids,states=state,
                actions=actions,angles=angles)
            raise AssertionError('Failed mapping operands retained; no particles removed')
        if sense < 0:
            state[:,3:] *= -1
        return state

    for seed in SEEDS:
        setup_start = time.process_time()
        with np.load(inputs/f'sample-{seed}.npz',allow_pickle=False) as z:
            data = {key:z[key].copy() for key in z.files}
        actions,folded,mass = data['actions'],data['folded_sample'],data['common_particle_mass']
        assert actions.shape == (COUNT,3) and folded.shape == (COUNT,6)
        assert np.all(np.isfinite(actions)) and np.all(actions >= 0)
        assert np.all(np.isfinite(folded)) and np.all(np.isfinite(mass)) and np.all(mass > 0)
        assert len(np.unique(folded[:,:3],axis=0)) == COUNT
        L = actions[:,1]+actions[:,2]
        I = actions[:,0]+.5*(L+np.sqrt(L*L+2))
        radial = I**-3
        angular = .5*(1+L/np.sqrt(L*L+2))*radial
        frequencies = np.column_stack((radial,angular,angular))
        with agama.setNumThreads(1):
            recovered,angles,finder_frequency = finder(folded,angles=True)
            roundtrip,mapper_frequency = mapper(np.column_stack((actions,angles)),frequencies=True)
        np.savez_compressed(out/f'seed-{seed}-mapping.npz',archived_actions=actions,
            recovered_actions=recovered,initial_angles=angles,analytic_frequencies=frequencies,
            finder_frequencies=finder_frequency,mapper_frequencies=mapper_frequency,
            roundtrip_state_difference=roundtrip-folded)
        finite = (np.all(np.isfinite(recovered),axis=1)&np.all(np.isfinite(angles),axis=1)
            &np.all(np.isfinite(finder_frequency),axis=1)&np.all(np.isfinite(roundtrip),axis=1)
            &np.all(np.isfinite(mapper_frequency),axis=1))
        write(out/f'seed-{seed}-mapping-finite.json',dict(seed=seed,all_finite=bool(np.all(finite)),
            nonfinite_particle_ids=np.flatnonzero(~finite).tolist(),all_outliers_retained=True))
        assert np.all(finite), 'Nonfinite mapping retained in saved diagnostic operands'
        action_error = float(np.max(abs(recovered-actions)/(math.sqrt(.5)+abs(actions))))
        finder_error = float(np.max(abs(finder_frequency-frequencies)/np.maximum(abs(frequencies),1e-30)))
        mapper_error = float(np.max(abs(mapper_frequency-frequencies)/np.maximum(abs(frequencies),1e-30)))
        roundtrip_error = state_error(roundtrip,folded)
        bad = (np.max(abs(recovered-actions)/(math.sqrt(.5)+abs(actions)),axis=1) > ALLOWANCES['action_scaled'])
        bad |= (np.max(abs(finder_frequency-frequencies)/np.maximum(abs(frequencies),1e-30),axis=1) > ALLOWANCES['frequency_relative'])
        bad |= (np.max(abs(mapper_frequency-frequencies)/np.maximum(abs(frequencies),1e-30),axis=1) > ALLOWANCES['frequency_relative'])
        bad |= (np.max(abs(roundtrip[:,:3]-folded[:,:3])/(.5+abs(folded[:,:3])),axis=1) > ALLOWANCES['roundtrip_position_scaled'])
        bad |= (np.max(abs(roundtrip[:,3:]-folded[:,3:])/(math.sqrt(2)+abs(folded[:,3:])),axis=1) > ALLOWANCES['roundtrip_velocity_scaled'])
        write(out/f'seed-{seed}-mapping-check.json',dict(seed=seed,action_scaled=action_error,
            finder_frequency_relative=finder_error,mapper_frequency_relative=mapper_error,
            roundtrip_scaled=roundtrip_error,failed_particle_ids=np.flatnonzero(bad).tolist(),
            all_outliers_retained=True,mapping_data=f'seed-{seed}-mapping.npz'))
        assert action_error <= ALLOWANCES['action_scaled']
        assert max(finder_error,mapper_error) <= ALLOWANCES['frequency_relative']
        assert roundtrip_error['position'] <= ALLOWANCES['roundtrip_position_scaled']
        assert roundtrip_error['velocity'] <= ALLOWANCES['roundtrip_velocity_scaled']
        bundle = dict(seed=seed,data=data,actions=actions,angles=angles,frequencies=frequencies,mass=mass,
            bounds=data['fixed_shell_boundaries'],family_counts=data['initial_shell_family_counts'].tolist(),
            ids=data['tracked_particle_ids'], records={pop:[] for pop in POPS},traces={pop:[] for pop in POPS},
            maximum_energy=0.,maximum_L=0.,setup_cpu_seconds=0.,initial_profiles={})
        for pop in POPS:
            initial = data[pop+'_initial']
            sign = data[pop+'_sign']
            assert sign.shape == (COUNT,) and np.all((sign == 1)|(sign == -1))
            assert np.array_equal(initial[:,:3],folded[:,:3])
            assert np.array_equal(initial[:,3:],folded[:,3:]*sign[:,None])
            # Confirm saved common sign decisions without producing a new uniform.
            expected_sign = np.where(data['common_uniform'] < data[pop+'_threshold'],1,-1)
            assert np.array_equal(sign,expected_sign)
            saved_profile = profile(0.,initial[:,:3],initial[:,3:],mass,bundle)
            old = strip_budget(load(inputs/f'run-{seed}-{pop}-dt0.01.json')['records'][0])
            assert saved_profile == old, 'Original initial pure diagnostic mismatch'
            mapped_initial = roundtrip.copy()
            mapped_initial[:,3:] *= sign[:,None]
            diff = profile_difference(profile(0.,mapped_initial[:,:3],mapped_initial[:,3:],mass,bundle),old)
            assert diff <= ALLOWANCES['initial_profile_scaled']
            bundle['initial_profiles'][pop] = saved_profile
            checks.append(dict(seed=seed,population=pop,action_scaled=action_error,
                finder_frequency_relative=finder_error,mapper_frequency_relative=mapper_error,
                roundtrip_scaled=roundtrip_error,mapped_initial_profile_scaled=diff,
                original_initial_profile_exact=True,no_changed_state_mass_sign_or_bin=True))
        bundle['initial_E'],bundle['initial_L'] = invariants(folded)
        bundle['setup_cpu_seconds'] = time.process_time()-setup_start
        bundles[seed] = bundle
    write(out/'INITIAL-CHECKS.json',dict(rows=checks,all_checks_pass=True,
        no_resampling=True,all_particles_retained=True,cpu_seconds=time.process_time()-RUN_CPU))

    def flush(seed,bundle):
        times = np.array([row['time'] for row in bundle['records']['F0']])
        assert all([row['time'] for row in bundle['records'][pop]] == times.tolist() for pop in POPS)
        arrays = dict(times=times,tracked_particle_ids=bundle['ids'],
            **{pop+'_tracked_states':np.array(bundle['traces'][pop]) for pop in POPS})
        target = out/f'seed-{seed}.npz'
        temporary = out/f'seed-{seed}.tmp.npz'
        np.savez_compressed(temporary,**arrays)
        temporary.replace(target)
        meta = out/f'seed-{seed}.json'
        write(meta,dict(seed=seed,records=bundle['records'],last_complete_time=float(times[-1]),
            analytic_invariants=dict(maximum_energy_scaled=bundle['maximum_energy'],maximum_L_vector_scaled=bundle['maximum_L']),
            coordinate_frame='Original inertial frame; original fixed shells; no recentering',data=target.name))
        write(out/f'seed-{seed}.receipt.json',dict(last_complete_time=float(times[-1]),
            snapshots=dict(path=target.name,sha256=sha(target)),diagnostics=dict(path=meta.name,sha256=sha(meta))))

    for seed in SEEDS:
        bundle = bundles[seed]
        prefix_cpu = time.process_time()
        for epoch_id,t in enumerate(EPOCHS):
            if time.monotonic()-RUN_WALL > INTERNAL_WALL:
                raise BudgetReached('Wall allowance reached between analytic epochs')
            if t == 0:
                positive = bundle['data']['folded_sample']
                negative = positive.copy()
                negative[:,3:] *= -1
            else:
                positive,negative = mapped(bundle,t,1),mapped(bundle,t,-1)
            for state,sense in ((positive,1),(negative,-1)):
                E,L = invariants(state)
                energy_error = float(np.max(abs(E-bundle['initial_E'])/(1+abs(bundle['initial_E']))))
                L_error = float(np.max(np.linalg.norm(L-sense*bundle['initial_L'],axis=1)/(math.sqrt(.5)+np.linalg.norm(bundle['initial_L'],axis=1))))
                bundle['maximum_energy'] = max(bundle['maximum_energy'],energy_error)
                bundle['maximum_L'] = max(bundle['maximum_L'],L_error)
                if energy_error > ALLOWANCES['all_path_energy_scaled'] or L_error > ALLOWANCES['all_path_L_vector_scaled']:
                    np.savez_compressed(out/f'failed-invariant-{seed}-{t:g}-{sense}.npz',states=state,
                        energy=E,angular_momentum=L,initial_energy=bundle['initial_E'],initial_angular_momentum=bundle['initial_L'])
                assert energy_error <= ALLOWANCES['all_path_energy_scaled']
                assert L_error <= ALLOWANCES['all_path_L_vector_scaled']
            epoch_records,epoch_traces = {},{}
            for pop in POPS:
                signs = bundle['data'][pop+'_sign']
                state = np.where((signs > 0)[:,None],positive,negative)
                row = profile(t,state[:,:3],state[:,3:],bundle['mass'],bundle)
                if t == 0:
                    assert row == bundle['initial_profiles'][pop]
                epoch_records[pop] = row
                epoch_traces[pop] = state[bundle['ids']].copy()
            # Commit only a whole, synchronized seed/epoch's three populations.
            for pop in POPS:
                bundle['records'][pop].append(epoch_records[pop])
                bundle['traces'][pop].append(epoch_traces[pop])
            flush(seed,bundle)
            write(out/'STATUS.json',dict(seed=seed,time=t,stage='analytic_phase_profiles',
                cpu_seconds=time.process_time()-RUN_CPU,wall_seconds=time.monotonic()-RUN_WALL))
            if seed == SEEDS[0] and epoch_id == 1:
                measured = time.process_time()-prefix_cpu
                setup_reserved = bundles[SEEDS[1]]['setup_cpu_seconds']
                # Both seeds have already been prepared/measured. Count second
                # setup once in elapsed CPU; list it explicitly, not a duplicate.
                projected = time.process_time()-RUN_CPU+1.25*60*measured/2+10.
                cost = dict(prefix_seed=seed,prefix_epochs=[0.,.5],prefix_seed_epoch_records=2,
                    all_three_population_diagnostics=True,prefix_cpu_seconds=measured,
                    already_measured_second_seed_setup_cpu_seconds=setup_reserved,
                    remaining_seed_epoch_records=60,safety_factor=1.25,selected_check_reservation=10.,
                    projected_total_cpu_seconds=projected,soft_cutoff=CPU_SOFT,proceed=projected < CPU_SOFT)
                write(out/'PROFILE.json',cost)
                if not cost['proceed']:
                    raise BudgetReached('Complete analytic-control projection exceeds frozen soft allowance')

    selected_results = []
    for seed in SEEDS:
        bundle = bundles[seed]
        ids = np.array([r['particle_id'] for r in config['selected_paths'][str(seed)]],dtype=int)
        folded = bundle['data']['folded_sample'][ids]
        reverse = folded.copy()
        reverse[:,3:] *= -1
        initial = np.concatenate((folded,reverse))
        def rhs(t,flat):
            state = flat.reshape(-1,6)
            x = state[:,:3]
            u = np.sqrt(.25+np.sum(x*x,axis=1))
            a = -x/(u*(.5+u)**2)[:,None]
            return np.column_stack((state[:,3:],a)).ravel()
        independent_start = time.process_time()
        solution = solve_ivp(rhs,(0.,END),initial.ravel(),method='DOP853',rtol=2e-11,atol=2e-12,max_step=.1,t_eval=np.array(EPOCHS))
        assert solution.success and np.array_equal(solution.t,np.array(EPOCHS))
        states = solution.y.T.reshape(len(EPOCHS),len(initial),6)
        initial_E,initial_L = invariants(initial)
        rows,mapped_states = [],[]
        for when,reference in zip(EPOCHS,states):
            mapped_plus = mapped(bundle,when,1,ids) if when else folded
            mapped_minus = mapped(bundle,when,-1,ids) if when else reverse
            actual = np.concatenate((mapped_plus,mapped_minus))
            mapped_states.append(actual.copy())
            error = state_error(actual,reference)
            E,L = invariants(reference)
            budget = dict(energy=float(np.max(abs(E-initial_E)/(1+abs(initial_E)))),
                L_vector=float(np.max(np.linalg.norm(L-initial_L,axis=1)/(math.sqrt(.5)+np.linalg.norm(initial_L,axis=1)))))
            rows.append(dict(time=when,state_scaled=error,independent_budget_scaled=budget))
        maximum_state = max(max(r['state_scaled'].values()) for r in rows)
        maximum_E = max(r['independent_budget_scaled']['energy'] for r in rows)
        maximum_L = max(r['independent_budget_scaled']['L_vector'] for r in rows)
        selected_data = out/f'seed-{seed}-selected-Cartesian.npz'
        np.savez_compressed(selected_data,times=np.array(EPOCHS),particle_ids=ids,
            independent_states=states,mapped_states=np.array(mapped_states))
        selected = dict(seed=seed,particle_ids=ids.tolist(),both_senses=True,rows=rows,
            maximum_state_scaled=maximum_state,maximum_DOP_energy_scaled=maximum_E,maximum_DOP_L_vector_scaled=maximum_L,
            DOP_function_evaluations=int(solution.nfev),cpu_seconds=time.process_time()-independent_start,
            data=selected_data.name,data_sha256=sha(selected_data),
            pass_all=bool(maximum_state <= ALLOWANCES['selected_DOP_state_scaled'] and maximum_E <= ALLOWANCES['selected_DOP_energy_scaled'] and maximum_L <= ALLOWANCES['selected_DOP_L_vector_scaled']))
        selected_results.append(selected)
        write(out/'SELECTED-CARTESIAN.json',dict(records=selected_results))
        assert selected['pass_all'], 'Independent selected Cartesian screen failed'
    comparisons = []
    for seed in SEEDS:
        bundle = bundles[seed]
        primary = [QUANTILES.index(q) for q in PRIMARY]
        for pop in POPS:
            analytic = bundle['records'][pop]
            live = load(inputs/f'run-{seed}-{pop}-dt0.01.json')['records']
            assert [r['time'] for r in analytic] == [r['time'] for r in live] == list(EPOCHS)
            init = analytic[0]
            rows = []
            qflag=mflag=sflag=False
            for a,b in zip(analytic,live):
                q = float(np.max(abs(np.array(a['quantile_radii'])[primary]/np.array(init['quantile_radii'])[primary]-1)))
                md,sd,coverage = 0.,0.,True
                mass_residual,second_residual = [],[]
                for old,aa,bb in zip(init['shells'],a['shells'],b['shells']):
                    if old['initial_family_count'] < 256:
                        continue
                    if not aa['coverage'] or not bb['coverage']:
                        coverage=False
                        continue
                    md=max(md,abs(aa['mass']/old['mass']-1))
                    sd=max(sd,float(np.max(abs(np.array(aa['second_diagonal'])/np.array(old['second_diagonal'])-1))))
                    mass_residual.append((bb['mass']-aa['mass'])/old['mass'])
                    second_residual.append(((np.array(bb['second_diagonal'])-np.array(aa['second_diagonal']))/np.array(old['second_diagonal'])).tolist())
                qflag |= q >= .05
                mflag |= md >= .05
                sflag |= sd >= .05
                rows.append(dict(time=a['time'],analytic_maximum_primary_quantile_drift=q,
                    analytic_maximum_covered_mass_drift=md,analytic_maximum_covered_second_drift=sd,coverage=coverage,
                    live_minus_analytic_primary_quantile_over_initial=((np.array(b['quantile_radii'])[primary]-np.array(a['quantile_radii'])[primary])/np.array(init['quantile_radii'])[primary]).tolist(),
                    live_minus_analytic_shell_mass_over_initial=mass_residual,
                    live_minus_analytic_shell_second_over_initial=second_residual))
            original = next(r for r in live_result['completed'] if r['seed']==seed and r['population']==pop and r['dt']==.01)
            comparisons.append(dict(seed=seed,population=pop,rows=rows,
                analytic_descriptive_adjustment_flags=dict(primary_quantile=qflag,covered_mass=mflag,covered_second=sflag),
                original_live_decision_retained=original['decision'],
                scope='Live-minus-analytic combines softening, discreteness, tree and collective effects; no unique instability inference'))
    unchanged = all(sha(inputs/r['path']) == r['sha256'] for r in frozen['snapshots'])
    unchanged &= all(sha(closure/r['path']) == r['sha256'] for r in closure_rows)
    unchanged &= all(sha(r['path']) == r['sha256'] for r in module_records)
    unchanged &= all(sha(r['path']) == r['sha256'] for r in prepared_modules['modules'])
    assert unchanged
    result = dict(status='complete',scope=config['scope'],configuration=config,initial_checks=checks,
        selected_checks=selected_results,comparisons=comparisons,all_31_epochs_complete=True,
        original_live_numerical_qualification=live_result['numerical_qualification'],original_flags_unchanged=True,
        frozen_inputs_unchanged=True,module_hashes_unchanged=True,
        prepared_frozen_sha256=sha(out/'FROZEN.json'),protocol_sha256=sha(inputs/'protocol.md'),
        cpu_seconds=time.process_time()-RUN_CPU,wall_seconds=time.monotonic()-RUN_WALL,
        limitations=config['exclusions'])
    write(out/'result.json',result)
    write(out/'TERMINAL.json',dict(status='complete',completed_utc=utc(),cpu_seconds=result['cpu_seconds'],wall_seconds=result['wall_seconds'],scientific_scope=config['scope']))
    (out/'COMPLETE').write_text('Same-sample analytic phase control complete; original live flags unchanged.\n')
    print(json.dumps(dict(status='complete',cpu_seconds=result['cpu_seconds'],original_live_numerical_qualification=live_result['numerical_qualification'])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--protocol',type=Path,default=ROOT/'research/discovery-20261001/TWINS_ANALYTIC_PHASE_CONTROL_PROTOCOL.md')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare',action='store_true')
    mode.add_argument('--run',action='store_true')
    args = parser.parse_args()
    if args.prepare:
        prepare(args.out,args.protocol)
        return
    try:
        run(args.out)
    except BaseException as error:
        if OWNED == args.out and not (OWNED/'TERMINAL.json').exists():
            write(OWNED/'TERMINAL.json',dict(status='failed',completed_utc=utc(),error_type=type(error).__name__,error=str(error),
                cpu_seconds=time.process_time()-RUN_CPU,wall_seconds=time.monotonic()-RUN_WALL,
                original_live_flags_unchanged=True))
            (OWNED/'FAILED').write_text(type(error).__name__+': '+str(error)+'\n')
        raise


if __name__ == '__main__':
    main()
