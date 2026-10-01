"""Recompute saved force/support diagnostics with NumPy and the standard library.

No force calls, quadrature-node generation, initial-condition generation, or orbit
evolution. Hashes identify the supplied records; arithmetic checks do not prove
their physical validity. Run from the clean discovery package with --out DIR.
"""
import os
for _key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[_key] = '1'
import argparse
from decimal import Decimal, localcontext
import hashlib
import json
from pathlib import Path
import platform
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    def numeric(item):
        if isinstance(item, np.generic):
            return item.item()
        raise TypeError('Unsupported JSON object: '+type(item).__name__)
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False, default=numeric)+'\n')


class Checks:
    def __init__(self):
        self.numeric_values = 0
        self.logical_values = 0
        self.maximum_absolute_difference = 0.

    def compare(self, actual, expected, name):
        if isinstance(actual, dict):
            for key, value in actual.items():
                assert key in expected, f'{name}/{key}: missing expected field'
                self.compare(value, expected[key], name+'/'+key)
        elif isinstance(actual, (list, tuple)):
            assert len(actual) == len(expected), name+': length mismatch'
            for index, (a, e) in enumerate(zip(actual, expected)):
                self.compare(a, e, name+'/'+str(index))
        elif isinstance(actual, (bool, np.bool_)) or actual is None or isinstance(actual, str):
            assert actual == expected, f'{name}: {actual!r} != {expected!r}'
            self.logical_values += 1
        else:
            a, e = float(actual), float(expected)
            assert np.isfinite(a) and np.isfinite(e), name+': nonfinite operand'
            delta = abs(a-e)
            assert delta <= 2e-15+1e-12*abs(e), f'{name}: {a!r} != {e!r}, difference {delta}'
            self.numeric_values += 1
            self.maximum_absolute_difference = max(self.maximum_absolute_difference, delta)


def stats(values):
    return dict(zip(('p50', 'p95', 'p99', 'maximum'),
        [float(x) for x in np.percentile(values, [50, 95, 99])]+[float(np.max(values))]))


def force_replay(z, published, checks):
    rows = []
    thresholds = published['configuration']['entrance_screen']
    for i, expected in enumerate(published['rows']):
        a, direct = z['native_acceleration'][i], z['direct_acceleration'][i]
        p, direct_p = z['native_potential'][i], z['direct_potential'][i]
        residual = a-direct
        assert np.array_equal(residual, z['force_residual'][i])
        assert np.array_equal(p-direct_p, z['potential_residual'][i])
        norm = np.linalg.norm(direct, axis=1)
        relative = np.linalg.norm(residual, axis=1)/np.maximum(norm, 1e-14)
        rounded = z['rounded_input_direct_acceleration'][i]
        row = dict(id=expected['id'], selected_force_relative64=stats(relative),
            selected_force_relative32inputs=stats(np.linalg.norm(a-rounded, axis=1)/np.maximum(np.linalg.norm(rounded, axis=1), 1e-14)),
            selected_potential_relative64=stats(abs(p-direct_p)/np.maximum(abs(direct_p), 1e-14)),
            selected_force_absolute=stats(np.linalg.norm(residual, axis=1)),
            force_floor_targets=int(np.count_nonzero(norm < 1e-14)),
            warmed_median_cpu_seconds=float(np.median(z['cpu_seconds'][i][~z['cold'][i]])),
            warmed_median_wall_seconds=float(np.median(z['wall_seconds'][i][~z['cold'][i]])))
        row['selected_force_entrance_screen'] = bool(row['selected_force_relative64']['p95'] < thresholds['selected_force_p95_relative']
            and row['selected_force_relative64']['p99'] < thresholds['selected_force_p99_relative'])
        checks.compare(row, expected, 'force/'+str(i))
        assert z['selected_particle_ids'][i].shape == (128,)
        rows.append(row)
    return dict(rows=rows, selected_cases=len(rows), selected_gates_pass=sum(r['selected_force_entrance_screen'] for r in rows),
        scope='Selected saved tree/direct vectors only; full-particle RMS source summaries not rederived')


def continuum_replay(z, published, diagnosis, checks):
    force_rows, central_rows, virials = [], [], []
    for i, expected in enumerate(published['forces']):
        gc = float(z[f'force-{i:02d}-coarse_du_weights'] @ z[f'force-{i:02d}-coarse_integrand'])
        gf = float(z[f'force-{i:02d}-fine_du_weights'] @ z[f'force-{i:02d}-fine_integrand'])
        ac, af = expected['adaptive_coarse'], expected['adaptive_fine']
        scale = abs(af)
        row = dict(epsilon=expected['epsilon'], r=expected['r'], gauss_coarse=gc, gauss_fine=gf,
            node_refinement_relative=abs(gf-gc)/scale,
            tolerance_refinement_relative=abs(af-ac)/scale,
            independent_formulation_relative=abs(gf-af)/scale,
            continuum_softening_force_relative=af/expected['unsoftened_force']-1)
        checks.compare(row, expected, 'continuum/forces/'+str(i))
        force_rows.append(row)
    for i, expected in enumerate(published['central']):
        gc, gf, ac, af = [expected[k] for k in ('gauss_coarse', 'gauss_fine', 'adaptive_coarse', 'adaptive_fine')]
        row = dict(epsilon=expected['epsilon'], node_refinement_relative=abs(gf-gc)/abs(af),
            tolerance_refinement_relative=abs(af-ac)/abs(af),
            independent_formulation_relative=abs(gf-af)/abs(af),
            continuum_softening_kappa_relative=af/expected['unsoftened_kappa']-1)
        checks.compare(row, expected, 'continuum/central/'+str(i))
        central_rows.append(row)
    for i, expected in enumerate(published['virials']):
        r, weights, rho = [z[f'virial-{i}-{k}'] for k in ('r', 'du_weights', 'rho')]
        W = float(weights @ (4*np.pi*r**3*rho*z[f'virial-{i}-force']))
        W0 = float(weights @ (4*np.pi*r**3*rho*z[f'virial-{i}-unsoftened_force']))
        row = dict(epsilon=expected['epsilon'], order=expected['order'], W=W, W_unsoftened=W0,
            mass=float(weights @ (4*np.pi*r*r*rho)), continuum_virial_relative=W/W0-1)
        checks.compare(row, expected, 'continuum/virials/'+str(i))
        virials.append(row)
    refinements = []
    for expected in published['global_refinements']:
        old, new = [r for r in virials if r['epsilon'] == expected['epsilon']]
        row = dict(epsilon=expected['epsilon'], virial_refinement_relative=abs(new['W']-old['W'])/abs(new['W']),
            mass_refinement_absolute=abs(new['mass']-old['mass']))
        checks.compare(row, expected, 'continuum/global/'+str(expected['epsilon']))
        refinements.append(row)
    formulas = []
    for i, expected in enumerate(published['formula_checks']):
        row = dict(potential_absolute_difference=abs(expected['potential']-expected['angular_potential']),
            derivative_absolute_difference=abs(expected['derivative']-expected['angular_derivative']),
            finite_difference_absolute_difference=abs(expected['finite_difference']-expected['derivative']))
        checks.compare(row, expected, 'continuum/formulas/'+str(i))
        formulas.append(row)
    limits = []
    for i, expected in enumerate(published['unsoftened_limit']):
        relative = expected['force']/expected['analytic_force']-1
        checks.compare(relative, expected['relative_difference'], 'continuum/unsoftened/'+str(i))
        limits.append(relative)
    far = []
    for i, expected in enumerate(published['far']):
        value = -expected['force']*expected['r']**2
        checks.compare(value, expected['monopole_fraction'], 'continuum/far/'+str(i))
        far.append(dict(r=expected['r'], monopole_fraction=value))
    thresholds = published['configuration']['gates']
    gates = dict(
        angular_potential=max(r['potential_absolute_difference'] for r in formulas) < thresholds['angular_potential_absolute'],
        angular_force=max(r['derivative_absolute_difference'] for r in formulas) < thresholds['angular_force_absolute'],
        finite_difference_force=max(r['finite_difference_absolute_difference'] for r in formulas) < thresholds['finite_difference_force_absolute'],
        force_node_doubling=max(r['node_refinement_relative'] for r in force_rows) < thresholds['refined_force_relative'],
        force_tolerance_halving=max(r['tolerance_refinement_relative'] for r in force_rows) < thresholds['refined_force_relative'],
        force_independent_formulation=max(r['independent_formulation_relative'] for r in force_rows) < thresholds['refined_force_relative'],
        central_checks=max(max(r[k] for k in ('node_refinement_relative', 'tolerance_refinement_relative', 'independent_formulation_relative')) for r in central_rows) < thresholds['refined_central_relative'],
        global_virial_doubling=max(r['virial_refinement_relative'] for r in refinements) < thresholds['refined_virial_relative'],
        mass=max(abs(r['mass']-1) for r in virials) < thresholds['mass_absolute'],
        mass_doubling=max(r['mass_refinement_absolute'] for r in refinements) < thresholds['mass_refinement_absolute'],
        unsoftened_limit=max(abs(value) for value, r in zip(limits, published['unsoftened_limit']) if r['epsilon'] == published['configuration']['unsoftened_limit']['epsilon'][-1]) < thresholds['unsoftened_limit_force_relative'],
        far_monopole=max(abs(r['monopole_fraction']-1) for r in far if r['r'] == published['configuration']['far_radii'][-1]) < thresholds['far_monopole_at_10000_relative'])
    checks.compare(gates, published['verification_gates'], 'continuum/gates')
    checks.compare(all(gates.values()), published['all_verification_gates_pass'], 'continuum/all_gates')
    # Decimal arithmetic checks the saved 80-digit operands, not the differentiation
    # that generated them. No mpmath, high-precision derivative or new FD evaluation.
    derivative_differences = []
    with localcontext() as ctx:
        ctx.prec = 90
        for i, row in enumerate(diagnosis['rows']):
            high = Decimal(row['independent_derivative_80digits'])
            # The original mpmath comparison converted the binary64 value itself,
            # not its shortest decimal display. Preserve that distinction here.
            low = Decimal.from_float(row['frozen_double_derivative'])
            difference = float(abs(high-low))
            checks.compare(difference, row['frozen_derivative_absolute_difference'], 'formula/saved_difference/'+str(i))
            derivative_differences.append(difference)
    maximum = max(derivative_differences)
    checks.compare(maximum, diagnosis['maximum_independent_derivative_difference'], 'formula/maximum')
    checks.compare(maximum < diagnosis['configuration']['direct_derivative_absolute_comparison'],
        diagnosis['independent_derivative_screen_pass'], 'formula/gate')
    assert not gates['finite_difference_force'] and diagnosis['original_finite_difference_screen_preserved'] is False
    return dict(force_rows=force_rows, central_rows=central_rows, virials=virials,
        reconstructed_gates=gates, all_original_gates_pass=all(gates.values()),
        saved_high_precision_difference_maximum=maximum,
        scope='Saved Gaussian-node contractions and scalar comparisons; central/adaptive/high-precision evaluations not rerun')


def live_replay(z, published, checks):
    thresholds = published['configuration']['terminal']
    fractions = published['configuration']['all_quantile_fractions']
    primary = [fractions.index(q) for q in published['configuration']['primary_quantile_fractions']]
    cases, arrays = [], []
    for i, expected in enumerate(published['cases']):
        get = lambda k:z[f'case-{i}-{k}']
        times = get('times')
        assert np.array_equal(times, np.arange(31)*.5)
        q, m, second, coverage = [get(k) for k in ('quantile_radii', 'shell_mass', 'second_diagonal', 'shell_coverage')]
        valid = get('shell_initial_pair_count') >= 256
        qdrift = float(np.max(abs(q[:, primary]/q[0, primary]-1)))
        md, sd, retained = [], [], True
        for t in range(31):
            for shell in range(4):
                if not valid[shell]:
                    continue
                if not coverage[t, shell] or np.any(second[0, shell] <= 0):
                    retained = False
                    continue
                md.append(abs(m[t, shell]/m[0, shell]-1))
                sd.append(float(np.max(abs(second[t, shell]/second[0, shell]-1))))
        E, P, L = [get(k) for k in ('E', 'P', 'L')]
        metrics = dict(maximum_primary_quantile_drift=qdrift,
            maximum_covered_shell_mass_drift=max(md) if md else None,
            maximum_covered_diagonal_second_drift=max(sd) if sd else None,
            coverage_retained=retained, maximum_energy_relative_error=float(np.max(abs((E-E[0])/abs(E[0])))),
            maximum_momentum_fixed_error=float(np.max(np.linalg.norm(P-P[0], axis=1)/np.sqrt(2))),
            maximum_angular_vector_fixed_error=float(np.max(np.linalg.norm(L-L[0], axis=1)/(1/np.sqrt(2)))))
        flags = dict(primary_quantile_adjustment=metrics['maximum_primary_quantile_drift'] >= thresholds['primary_quantile_or_covered_mass_second_drift'],
            covered_mass_adjustment=metrics['maximum_covered_shell_mass_drift'] is None or metrics['maximum_covered_shell_mass_drift'] >= thresholds['primary_quantile_or_covered_mass_second_drift'],
            covered_second_adjustment=metrics['maximum_covered_diagonal_second_drift'] is None or metrics['maximum_covered_diagonal_second_drift'] >= thresholds['primary_quantile_or_covered_mass_second_drift'],
            coverage_failure=not retained)
        direct, native = get('endpoint_direct_acceleration'), get('endpoint_returned_selected_acceleration')
        magnitude = np.linalg.norm(direct, axis=1)
        force = stats(np.linalg.norm(native-direct, axis=1)/np.maximum(magnitude, 1e-14))
        direct_p, native_p = get('endpoint_direct_potential'), get('endpoint_returned_selected_potential')
        endpoint = dict(force_relative=force, force_absolute=stats(np.linalg.norm(native-direct, axis=1)),
            potential_relative=stats(abs(native_p-direct_p)/np.maximum(abs(direct_p), 1e-14)),
            force_floor_targets=int(np.count_nonzero(magnitude < 1e-14)),
            selected_screen_pass=bool(force['p95'] < thresholds['selected_force_p95_relative'] and force['p99'] < thresholds['selected_force_p99_relative']))
        screens = dict(energy=metrics['maximum_energy_relative_error'] < thresholds['energy_relative_error'],
            momentum=metrics['maximum_momentum_fixed_error'] < thresholds['momentum_error_over_fixed_scale'],
            angular_vector=metrics['maximum_angular_vector_fixed_error'] < thresholds['angular_vector_error_over_fixed_scale'],
            endpoint_selected_force=endpoint['selected_screen_pass'])
        decision = dict(metrics=metrics, rapid_adjustment_flags=flags, numerical_screens=screens)
        checks.compare(decision, expected['decision'], 'live/'+expected['id']+'/decision')
        checks.compare(endpoint, expected['end_direct_check'], 'live/'+expected['id']+'/endpoint')
        cases.append(dict(id=expected['id'], decision=decision, end_direct_check=endpoint))
        arrays.append(dict(q=q, mass=m, second=second, coverage=coverage, modes=get('mode_amplitudes'), valid=valid, times=times))
    refinements = []
    for expected in published['timestep_refinements']:
        first_seed = published['configuration']['seeds'][0]
        indices = [i for i, r in enumerate(published['cases']) if r['population'] == expected['population'] and r['seed'] == first_seed]
        coarse, fine = [arrays[i] for i in indices]
        assert np.array_equal(coarse['times'], fine['times'])
        qdiff = float(np.max(abs(coarse['q'][:, primary]-fine['q'][:, primary])/coarse['q'][0, primary]))
        mdiff, sdiff, mode, coverage = 0., 0., 0., True
        for t in range(31):
            for shell in range(4):
                if not coarse['valid'][shell]:
                    continue
                if not coarse['coverage'][t, shell] or not fine['coverage'][t, shell]:
                    coverage = False
                    continue
                mdiff = max(mdiff, float(abs(coarse['mass'][t, shell]-fine['mass'][t, shell])/coarse['mass'][0, shell]))
                sdiff = max(sdiff, float(np.max(abs(coarse['second'][t, shell]-fine['second'][t, shell])/coarse['second'][0, shell])))
                mode = max(mode, float(np.max(abs(coarse['modes'][t, shell]-fine['modes'][t, shell]))))
        row = dict(population=expected['population'], maximum_primary_quantile_fractional_difference=qdiff,
            maximum_covered_mass_fractional_difference=mdiff, maximum_covered_second_fractional_difference=sdiff,
            maximum_absolute_mode_amplitude_difference=mode, coverage_retained=coverage,
            fractional_drift_step_screen_pass=coverage and max(qdiff, mdiff, sdiff) < thresholds['coarse_fine_fractional_drift_difference'])
        checks.compare(row, expected, 'live/refinement/'+expected['population'])
        refinements.append(row)
    qualification = all(all(r['decision']['numerical_screens'].values()) for r in cases) and all(r['fractional_drift_step_screen_pass'] for r in refinements)
    flags = any(any(r['decision']['rapid_adjustment_flags'].values()) for r in cases)
    checks.compare(qualification, published['numerical_qualification'], 'live/qualification')
    checks.compare(flags, published['rapid_adjustment_flags_present'], 'live/rapid_flags')
    assert qualification is False
    return dict(cases=cases, refinements=refinements, numerical_qualification=qualification,
        rapid_adjustment_flags_present=flags, scope='Recorded diagnostics replay; full self-gravitating evolution not rerun')


def energy_replay(z, published, checks):
    m = z['particle_mass']
    rows = []
    native_den = abs(float(z['native_E'][0]))
    for i, expected in enumerate(published['direct_records']):
        K = float(m @ z['specific_kinetic'][i])
        U = float(.5*m @ z['direct_potential'][i])
        row = dict(time=float(z['times'][i]), K=K, U_direct=U, E_direct=K+U,
            U_native=float(z['native_U'][i]), E_native=float(z['native_E'][i]),
            native_minus_direct_U=float(z['native_U'][i]-U))
        if i == 0:
            direct_initial = K+U
        row.update(direct_energy_change_over_live_E0=(row['E_direct']-direct_initial)/native_den,
            native_energy_change_over_live_E0=(row['E_native']-z['native_E'][0])/native_den)
        checks.compare(row, expected, 'energy/direct/'+str(i))
        rows.append(row)
    initial, toys, comparisons = z['toy_initial_family_E'], [], []
    for i, expected in enumerate(published['toy_records']):
        DE, DL = z['toy_family_DE'][i], z['toy_family_DL'][i]
        row = dict(dt=float(z['dt'][i]), absolute_total_energy_change=float(DE.sum()),
            energy_change_over_live_E0=float(DE.sum()/native_den),
            toy_relative_energy_change=float(DE.sum()/abs(initial.sum())),
            maximum_family_relative_energy_error=float(np.max(abs(DE)/abs(initial))),
            maximum_family_L_vector_error=float(np.max(np.linalg.norm(DL, axis=-1))))
        checks.compare(row, expected, 'energy/toy/'+str(i))
        toys.append(row)
        comparison = dict(dt=float(z['dt'][i]), max_selected_state_error=float(np.max(abs(z['selected_state_difference'][i]))))
        checks.compare(comparison, published['selected_reference']['comparisons'][i], 'energy/toy_reference/'+str(i))
        comparisons.append(comparison)
    pair = m.reshape(-1, 2)
    binding = float(-1.5/.025*np.sum(pair[:, 0]*pair[:, 1]))
    checks.compare(binding, published['initial_extra_pair_binding'], 'energy/binding')
    checks.compare(binding/native_den, published['initial_pair_binding_over_live_E0'], 'energy/binding_fraction')
    checks.compare(float(np.max(abs(z['selected_DOP_DE']))), published['selected_reference']['DOP_max_abs_family_energy_change'], 'energy/DOP_energy')
    checks.compare(float(np.max(np.linalg.norm(z['selected_DOP_DL'], axis=-1))), published['selected_reference']['DOP_max_family_L_vector_change'], 'energy/DOP_L')
    assert published['original_failed_energy_gate_unchanged'] is True
    return dict(direct_records=rows, toy_records=toys, selected_state_comparisons=comparisons,
        original_failed_energy_gate_unchanged=True,
        scope='Saved all-particle kinetic/potential and isolated-partner budget operands; toy trajectories and DOP853 not rerun')


def support_replay(z, published, checks):
    edges = dict(binding_energy=[0,.05,.1,.2,.4,.7,1], circularity=[0,.2,.4,.6,.8,1], inclination_cosine=[0,.2,.4,.6,.8,1])
    records, summaries = [], []
    expected_records = {(r['history'], r['library']):r for r in published['records']}
    expected_summaries = {(r['history'], r['partition']):r for r in published['summaries']}
    for history in ('fully-present', 'gradually-grown'):
        vectors = {key:[] for key in edges}
        whole, refs = [], []
        for library in range(8):
            get = lambda key:z[f'{history}-{library}-{key}']
            actions, mass, ratio, hs, impulse = [get(key) for key in ('actions', 'mass', 'F0_over_Fq', 'signed_deltaF_over_Fq', 'family_impulse')]
            contrast = mass[None, :]*hs*(impulse[:, 0]-impulse[:, 1])[None, :]
            reference = mass*.5*ratio*impulse.sum(axis=1)
            assert np.array_equal(contrast, get('contrast_contributions'))
            assert np.array_equal(reference, get('reference_contributions'))
            assert np.all(mass > 0) and np.all(ratio+hs > 0) and np.all(ratio-hs > 0)
            expected = expected_records[history, library]
            contractions = []
            for h, old in zip(hs, expected['contractions']):
                plus = float(.5*mass @ ((ratio+h)*impulse[:,0]+(ratio-h)*impulse[:,1]))
                minus = float(.5*mass @ ((ratio-h)*impulse[:,0]+(ratio+h)*impulse[:,1]))
                c = float(mass @ (h*(impulse[:,0]-impulse[:,1])))
                ref = float(mass @ (.5*ratio*impulse.sum(axis=1)))
                contractions.append(dict(p=old['p'], alpha=old['alpha'], plus=plus, minus=minus,
                    contrast=c, reference=ref, contrast_over_reference=c/ref))
            L = actions[:,1]+abs(actions[:,2])
            A = actions[:,0]+.5*(L+np.sqrt(L*L+2))
            e = .5/A**2
            maximum_L = (1-e)/np.sqrt(2*e)
            coordinates = dict(binding_energy=e, circularity=L/maximum_L, inclination_cosine=abs(actions[:,2])/L)
            bins = {}
            for name, coordinate in coordinates.items():
                assert np.all((coordinate >= 0) & (coordinate <= 1+1e-12))
                es = np.array(edges[name])
                index = np.searchsorted(es[1:-1], coordinate, side='right')
                rows = []
                for b, (lo, hi) in enumerate(zip(es[:-1], es[1:])):
                    pick = index == b
                    rows.append(dict(lower=float(lo), upper=float(hi), families=int(pick.sum()),
                        absolute_reference_mass=float(mass[pick] @ ratio[pick]),
                        reference_transfer=float(reference[pick].sum()), signed_contrast=contrast[:,pick].sum(axis=1).tolist(),
                        positive_contrast=np.maximum(contrast[:,pick],0).sum(axis=1).tolist(),
                        negative_contrast=np.minimum(contrast[:,pick],0).sum(axis=1).tolist()))
                vector = np.array([r['signed_contrast'] for r in rows]).T
                assert np.max(abs(vector.sum(axis=1)-contrast.sum(axis=1))) < 1e-16
                vectors[name].append(vector)
                bins[name] = rows
            concentration = []
            for values in contrast:
                absolute = np.sort(abs(values))[::-1]
                total = float(absolute.sum())
                concentration.append(dict(absolute_sum=total, signed_sum=float(values.sum()),
                    top_family_absolute_fraction={str(n):float(absolute[:n].sum()/total) if total else None for n in (1,5,20,64)},
                    positive_sum=float(np.maximum(values,0).sum()), negative_sum=float(np.minimum(values,0).sum())))
            row = dict(history=history, library=library, contractions=contractions, bins=bins, concentration=concentration)
            checks.compare(row, expected, 'support/'+history+'/'+str(library))
            records.append(row)
            whole.append(contrast.sum(axis=1))
            refs.append(reference.sum())
        checks.compare(np.array(whole).tolist(), z[history+'-whole-library-contrasts'].tolist(), 'support/'+history+'/whole')
        checks.compare(np.array(refs).tolist(), z[history+'-whole-library-reference'].tolist(), 'support/'+history+'/reference')
        for name, values in vectors.items():
            values = np.array(values)
            flat = values.reshape(8,-1)
            row = dict(history=history, partition=name, populations=[4,6,8], edges=edges[name],
                library_vectors=values.tolist(), mean=values.mean(axis=0).tolist(),
                standard_error=(values.std(axis=0,ddof=1)/np.sqrt(8)).tolist(),
                covariance_of_mean=(np.cov(flat,rowvar=False,ddof=1)/8).tolist(),
                covariance_order='Population-major, then bin; eight whole independent libraries')
            checks.compare(row, expected_summaries[history,name], 'support/'+history+'/summary/'+name)
            summaries.append(row)
    return dict(records=records, summaries=summaries, scope='Post hoc partitions and descriptive library covariance; no new bin sign qualification or trapping inference')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    cpu, wall = time.process_time(), time.monotonic()
    directory = ROOT/'operands/twins-force-support-v1'
    manifest_path = directory/'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    assert manifest['dataset_version'] == 'twins-force-support-v1'
    data_path = directory/manifest['data']['path']
    assert sha(data_path) == manifest['data']['sha256']
    published = json.loads(data_path.read_text())
    assert published['dataset_version'] == manifest['dataset_version']
    arrays = {}
    for entry in manifest['files']:
        path = directory/entry['path']
        assert path.stat().st_size == entry['bytes'] and sha(path) == entry['sha256']
        with np.load(path, allow_pickle=False) as archive:
            z = {key:archive[key].copy() for key in archive.files}
        assert set(z) == set(entry['arrays'])
        for key, value in z.items():
            description = entry['arrays'][key]
            assert list(value.shape) == description['shape'] and value.dtype.str == description['dtype']
            assert np.all(np.isfinite(value)) and not value.dtype.hasobject
        arrays[Path(entry['path']).stem] = z
    checks = Checks()
    reconstructed = dict(
        force=force_replay(arrays['selected-force'], published['force'], checks),
        continuum=continuum_replay(arrays['continuum-quadrature'], published['continuum'], published['formula_diagnosis'], checks),
        live=live_replay(arrays['paired-live-diagnostics'], published['live'], checks),
        early_energy=energy_replay(arrays['early-energy-operands'], published['early_energy'], checks),
        action_support=support_replay(arrays['action-support'], published['action_support'], checks))
    receipt = dict(status='complete_saved_arithmetic_replay', dataset_version=manifest['dataset_version'],
        scientific_evolution=False, native_force_or_AGAMA_required=False,
        manifest_sha256=sha(manifest_path), data_sha256=sha(data_path),
        numeric_values_compared=checks.numeric_values, logical_values_compared=checks.logical_values,
        maximum_absolute_numeric_difference=checks.maximum_absolute_difference,
        reconstructed=reconstructed, original_paired_live_numerical_qualification=False,
        coverage='Hashes, saved selected-vector errors, saved Gaussian contractions, scalar continuum gates, live diagnostics/gates, isolated-toy budgets and state errors, post hoc weighted support/covariance',
        exclusions=['Does not regenerate forces or quadrature integrands', 'Does not independently repeat high-precision differentiation',
            'Does not run trajectories or test collective stability', 'Does not prove confidence coverage or approximate live energy validity',
            'Does not certify the pending independent-sign sampler'],
        versions=dict(python=platform.python_version(), numpy=np.__version__),
        cpu_seconds=time.process_time()-cpu, wall_seconds=time.monotonic()-wall)
    write(args.out/'result.json', receipt)
    print(json.dumps({k:receipt[k] for k in ('status', 'numeric_values_compared', 'logical_values_compared',
        'maximum_absolute_numeric_difference', 'cpu_seconds', 'original_paired_live_numerical_qualification')}))


if __name__ == '__main__':
    main()
