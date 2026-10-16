"""Portable full four-state / sixteen-seed sign construction; no trajectories."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import zipfile

# Set before importing NumPy/SciPy in this standalone process. No installer.
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
os.environ['OMP_DYNAMIC'] = 'FALSE'
sys.dont_write_bytecode = True

SOURCE_HASHES = {'sign_constructor': 'cb830e55694e09dfaa472c80f807263712b325a5e318d950ccbad814a9b520bd', 'balanced_constructor': 'bccd4bfa65483890c17783386c54defd3bd30160142ab49ebb0dc648d3365a00', 'spatial_profiles': '43ca91fb25f94b91207ce254a01a9a0dc9651f3877c84379ef727534c0090b0e', 'nominal_history': 'af75ab82dc2e68059f83215d857d3a00c37efc9eff3757471a3524d1724d7a78', 'halfstep_history': 'd46e7db70e54389a89374d47c29fccfb13bf288731a3de935069d08653274415'}
MODULES = ('sign_science.py', 'balanced_science.py', 'profile_science.py')
LABELS = ('nominal__synchronous', 'nominal__lagged', 'halfstep__synchronous', 'halfstep__lagged')
PHYSICAL_PARAMETERS = {
    'units': 'G=M_host=b_host=1',
    'host': {'mass': 1., 'Plummer_scale': 1., 'count': 8192, 'seed': 76101401},
    'satellites': {'mass_each': .025, 'Plummer_scale_each': .1, 'count_each': 2048,
                   'seeds': [76101411, 76101412], 'host_monopole_apocentre': 3., 'host_monopole_pericentre': .5},
    'force': {'kernel': 'P1', 'epsilon': .0025, 'tree_theta': .0625},
    'history': {'endpoint': 40., 'both_satellites_present_at_t0': True,
                'lagged_second_satellite_initial_phase_advance': 4.,
                'velocity_frame': 'original initial whole-system barycentric inertial frame',
                'initial_sampling': 'unpaired; common original host and satellite clouds'},
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_write(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False); stream.write('\n')


def authenticate(path):
    manifest = json.loads(path.read_text())
    if (set(manifest) != {'schema', 'physical_parameters', 'scientific_source_sha256', 'states'}
            or manifest['schema'] != 'assembly-control-public-inputs-v1'
            or manifest['physical_parameters'] != PHYSICAL_PARAMETERS
            or manifest['scientific_source_sha256'] != SOURCE_HASHES
            or [row['label'] for row in manifest['states']] != list(LABELS)):
        raise RuntimeError('Exact public physical provenance and complete four-state manifest required')
    states = []; bindings = {path: sha(path)}; used = set()
    for index, row in enumerate(manifest['states']):
        if set(row) != {'label', 'arm', 'dt', 'time', 'file', 'sha256', 'bytes', 'arrays'}:
            raise RuntimeError('Unexpected public state metadata')
        expected_dt = .00125 if index < 2 else .000625
        if (row['arm'] != LABELS[index].split('__')[1] or row['dt'] != expected_dt or row['time'] != 40.
                or not isinstance(row['file'], str) or Path(row['file']).name != row['file']
                or not row['file'].endswith('.npz') or row['file'] in used):
            raise RuntimeError('Complete original endpoint identity required')
        used.add(row['file']); archive = path.parent/row['file']
        if (not archive.is_file() or archive.resolve() != archive
                or archive.stat().st_size != row['bytes'] or sha(archive) != row['sha256']):
            raise RuntimeError('Public particle archive hash/size mismatch')
        with zipfile.ZipFile(archive) as saved:
            if sorted(saved.namelist()) != ['cohort.npy', 'mass.npy', 'particle_id.npy', 'xv.npy']:
                raise RuntimeError('Only the four public particle arrays are allowed')
        if set(row['arrays']) != {'xv', 'mass', 'cohort', 'particle_id'}:
            raise RuntimeError('All four public array descriptions required')
        header = {}
        for name, description in row['arrays'].items():
            expected_shape = [12288, 6] if name == 'xv' else [12288]
            if (set(description) != {'shape', 'dtype'} or description['shape'] != expected_shape
                    or not isinstance(description['dtype'], str)):
                raise RuntimeError('Full all-particle array shape/dtype metadata required')
            header[name] = dict(npz=name, **description)
        states.append(dict(label=row['label'], arm=row['arm'], dt=row['dt'], arrays=archive, header=header))
        bindings[archive] = row['sha256']
    return manifest, states, bindings


def check_unchanged(bindings):
    if any(sha(path) != expected for path, expected in bindings.items()):
        raise RuntimeError('Read-only input changed during the run')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(); inputs = args.inputs.resolve(strict=True)
    output = args.output.absolute()
    if (output.exists() or output.resolve() != output or not output.parent.is_dir()
            or output.is_relative_to(inputs.parent)):
        raise RuntimeError('Use a new output directory outside the read-only input directory')
    here = Path(__file__).resolve().parent
    extraction = json.loads((here/'EXTRACTION.json').read_text())
    if (set(extraction['modules']) != set(MODULES)
            or extraction['public_scientific_source_sha256'] != SOURCE_HASHES
            or sha(here/'run.py') != extraction['runner_sha256']):
        raise RuntimeError('Portable source manifest mismatch')
    for name in MODULES:
        if sha(here/name) != extraction['modules'][name]['portable_sha256']:
            raise RuntimeError('Extracted scientific function module changed')
    provenance, states, bindings = authenticate(inputs)
    import numpy as np
    import scipy
    from scipy import linalg as la
    from scipy.optimize import minimize
    import sign_science as old
    import balanced_science as science
    import profile_science as body
    output.mkdir()  # Exclusive creation; never resume or overwrite another output.
    completed = []; summaries = []; labels = None
    def check():
        pass  # No host service, job cap, force evaluation or background monitoring.
    def save_arrays(name, arrays):
        with (output/name).open('xb') as stream: np.savez(stream, **arrays)
        return dict(file=name, sha256=sha(output/name))
    base = dict(schema='portable-balanced-sign-construction-v1', same_code_port=True,
        independent_physics_validation=False, input_manifest_sha256=bindings[inputs],
        public_input_provenance=provenance, extraction_manifest_sha256=sha(here/'EXTRACTION.json'),
        numerical_library_versions=dict(numpy=np.__version__, scipy=scipy.__version__),
        single_thread_environment=True, physical_pass=False, formation_control=False,
        finite_time_error_bound=False, trajectories_run=False)
    try:
        json_write(output/'fixture.json', science.fixtures(body, old, np, la, minimize, check))
        prepared, preparation_cost, labels = science.prepare(states, body, old, np, minimize, check)
        for row in prepared:
            values = dict(row['solution_arrays'], particle_id=row['raw']['particle_id'][:8192],
                seeds=np.asarray(old.SEEDS), independent_signs=row['independent_signs'])
            values.update({'independent__'+k: v for k, v in row['independent_arrays'].items()})
            row['refit_artifact'] = save_arrays(row['state']['label']+'-refit.npz', values)
            summaries.append(dict(label=row['state']['label'], solution=row['solved'],
                independent=row['independent_report'], even_identity=row['identity'], arrays=row['refit_artifact']))
        json_write(output/'refits.json', dict(complete=True, all_four_refits=summaries,
            feature_labels=labels, measured_preparation=preparation_cost))
        if any(row['solved']['status'] != 'finite_solver_candidate_only' for row in prepared):
            raise science.FlightFailure('At least one complete refit is inconclusive; no retry or state selection')
        for row in prepared:
            for index, seed in enumerate(old.SEEDS):
                signs, report, extra = science.flight(row['groups']['training'][0], row['mass'], row['h'],
                    row['A'], seed, np, la, check)
                row['balanced_signs'][index] = signs
                row['flights'].append(report); row['flight_arrays'].append(extra)
            identity = science.preserve(row['raw'], row['balanced_signs'], np, check)
            values, report = science.measure(row['groups'], row['mass'], row['h'],
                row['balanced_signs'], old, np, check, False)
            arrays = dict(particle_id=row['raw']['particle_id'][:8192], seeds=np.asarray(old.SEEDS),
                balanced_signs=row['balanced_signs'])
            arrays.update({'balanced__'+k: v for k, v in values.items()})
            for index, extra in enumerate(row['flight_arrays']):
                arrays.update({f'flight{index}__'+k: v for k, v in extra.items()})
            artifact = save_arrays(row['state']['label']+'-balanced-control.npz', arrays)
            summary = dict(label=row['state']['label'], time=40., original_dt=row['state']['dt'],
                solution=row['solved'], precondition=row['precondition'], independent=row['independent_report'],
                balanced=report, even_identity=identity, flights=row['flights'],
                refit_arrays=row['refit_artifact'], arrays=artifact)
            json_write(output/(row['state']['label']+'-summary.json'), summary); completed.append(summary)
        check_unchanged(bindings)
        json_write(output/'result.json', dict(base, complete=True, comparison_complete=True, states=completed,
            feature_labels=labels, original_training_rows=168, added_derivative_rows=35, total_training_rows=203,
            observer_definition='phi_scale(x)=phi_1(x/scale); gradient includes1/scale',
            observer_training_scale=1., heldout_observer_scales=[.8, 1.25], STF_names=list(science.STF_NAMES),
            seeds=list(old.SEEDS), rebase_every=science.REBASE_EVERY,
            limits=['Same extracted numerical code; this port is not independent physical validation.',
                'All four complete endpoints and all sixteen fixed seeds per method are retained.',
                'Selected currents are approximate; held-out currents remain a causal alternative.',
                'Even empirical measures and initial kinetic energy are preserved; central covariance depends on residual currents.',
                'Conditional landing variance excludes dependent flight covariance; seed scatter is descriptive.',
                'Cubic velocity changes and entropy are construction descriptors, not measurements of assembly memory.',
                'No force calculation, trajectory, equilibrium, stability or stellar qualification is performed.']))
    except BaseException as exc:
        # Preserve a visibly incomplete run without exporting host paths from exception text.
        if not (output/'result.json').exists():
            json_write(output/'result.json', dict(base, complete=False, comparison_complete=False,
                failure_type=type(exc).__name__, all_four_refits=summaries, completed_states=completed))
        raise


if __name__ == '__main__':
    main()
