"""Frozen exact-moment populations: importance contractions of saved impulses.

No new particle sampling, orbit integration or live-state modification.
"""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import sys
import time
import numpy as np
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/discovery'))
import twins_exact_moments as analytic


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')


def population_weights(actions, masses, populations, df, expected_mass):
    jr, jz, lz = actions.T
    angular = jz + np.abs(lz)
    action = jr+.5*(angular+np.sqrt(angular**2+2))
    e = .5/action**2
    assert np.all((e > 0) & (e < 1))
    assert np.all(masses > 0)
    assert abs(float(masses.sum())-expected_mass) < 1e-12
    assert np.max(np.abs(masses-expected_mass/len(masses))) < 1e-14
    q = df(actions)
    reverse = actions.copy()
    reverse[:, 2] *= -1
    qr = df(reverse)
    assert np.all(np.isfinite(q)) and np.all(q > 0)
    assert np.max(np.abs(qr/q-1)) < 1e-12
    exact = analytic.f0(e)
    ratio = exact/q
    assert np.max(np.abs(ratio-1)) < .001
    hs = []
    for row in populations:
        p = row['p']
        g0 = -4*p/((p+2.5)*(p+3.5))*e**(p-1) + 8*analytic.B/(p+3.5)*e**p
        h = row['alpha'] * np.abs(lz)*(g0+angular*angular*e**p)/q
        assert np.max(np.abs(h/ratio)) <= .5+1e-10
        assert np.all(ratio+h > 0) and np.all(ratio-h > 0)
        hs.append(h)
    return ratio, np.array(hs), dict(reference_sampling_mass=expected_mass,
        represented_exact_population_mass=float(masses @ ratio),
        target_population_mass=1., renormalized=False,
        energy_minimum=float(e.min()), energy_maximum=float(e.max()),
        exact_over_sampling_DF_minimum=float(ratio.min()), exact_over_sampling_DF_maximum=float(ratio.max()),
        maximum_sampled_analytic_multipliers=[float(np.max(np.abs(h/ratio))) for h in hs],
        sampling_DF_velocity_reversal_relative_error=float(np.max(np.abs(qr/q-1))))


def contract(impulses, mass, ratio, hs, populations):
    reference = float(mass @ (.5*ratio*impulses.sum(axis=1)))
    rows = []
    for h, pop in zip(hs, populations):
        plus = float(.5*mass @ ((ratio+h)*impulses[:, 0]+(ratio-h)*impulses[:, 1]))
        minus = float(.5*mass @ ((ratio-h)*impulses[:, 0]+(ratio+h)*impulses[:, 1]))
        contrast = float(mass @ (h*(impulses[:, 0]-impulses[:, 1])))
        assert abs((plus-minus)-contrast) < 1e-16
        rows.append(dict(p=pop['p'], alpha=pop['alpha'], plus=plus, minus=minus,
            contrast=contrast, reference=reference,
            contrast_over_reference=contrast/reference if reference else None))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, required=True)
    parser.add_argument('--frozen', type=Path, required=True)
    parser.add_argument('--protocol', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start_cpu = time.process_time()
    source = Path(__file__).read_bytes()
    (args.out/'source.py').write_bytes(source)
    (args.out/'protocol.md').write_bytes(args.protocol.read_bytes())
    (args.out/'frozen-populations.json').write_bytes(args.frozen.read_bytes())
    frozen = load(args.out/'frozen-populations.json')
    assert sha(analytic.__file__) == frozen['source_sha256']
    populations = frozen['populations']
    assert [row['p'] for row in populations] == [4, 6, 8]
    complete_at_start = (args.parent/'COMPLETE').is_file()
    config = load(args.parent/'config.json')
    assert config['replicas'] == 8 and config['families'] == 512
    assert config['phases'] == 256 and config['dt'] == .01 and config['duration'] == 300
    assert sha(analytic.agama.__file__) == config['snapshot_sha256']['agama']
    evidence_paths = [args.frozen, args.protocol, Path(__file__), Path(analytic.__file__), args.parent/'config.json']
    pot = analytic.agama.Potential(type='Isochrone', mass=1, scaleRadius=.5)
    df = analytic.agama.DistributionFunction(type='QuasiSpherical', potential=pot)
    sampling_mass = float(df.totalMass())
    records, libraries, checks = [], {}, []
    for rep in range(8):
        library_path = args.parent/f'library-{rep}.npz'
        evidence_paths.append(library_path)
        data = np.load(library_path)
        actions, mass = data['actions'], data['mass']
        with analytic.agama.setNumThreads(1):
            ratio, hs, check = population_weights(actions, mass, populations, df, sampling_mass)
        libraries[rep] = dict(actions=actions, mass=mass, ratio=ratio, hs=hs)
        check['library_id'] = rep
        checks.append(check)
        histories = {}
        for history in ('reference', 'frequency'):
            npz = args.parent/f'{history}-{rep}.npz'
            metadata_path = args.parent/f'{history}-{rep}.json'
            evidence_paths.extend((npz, metadata_path))
            response = np.load(npz)
            assert np.array_equal(actions, response['actions']) and np.array_equal(mass, response['mass'])
            metadata = load(metadata_path)
            assert metadata['sampler_method'] == 4
            assert abs(metadata['library_checks']['mass']-sampling_mass) < 1e-12
            check['sampler_returned_mass'] = metadata['library_checks']['sampler_returned_mass']
            histories[history] = dict(rows=contract(response['family_impulse'], mass, ratio, hs, populations),
                initial_invariant_checks=metadata['library_checks'])
        records.append(dict(library_id=rep, histories=histories))
    ordering = [(history, pop['p']) for history in ('reference', 'frequency') for pop in populations]
    values = np.array([[row['contrast'] for history in ('reference', 'frequency')
        for row in record['histories'][history]['rows']] for record in records])
    means = values.mean(axis=0)
    se = values.std(axis=0, ddof=1)/np.sqrt(8)
    critical = float(t.ppf(.975, 7))
    bonf = float(t.ppf(1-.05/(2*6), 7))
    reference_values = np.array([[record['histories'][history]['rows'][0]['reference']
        for history in ('reference', 'frequency')] for record in records])
    reference_summaries = []
    for i, history in enumerate(('reference', 'frequency')):
        mean_reference = float(reference_values[:, i].mean())
        reference_se = float(reference_values[:, i].std(ddof=1)/np.sqrt(8))
        reference_summaries.append(dict(history=history, transfer=mean_reference,
            standard_error=reference_se,
            nominal_pointwise_95_interval=[mean_reference-critical*reference_se,
                mean_reference+critical*reference_se],
            interval_scope='Supplementary pointwise reference uncertainty, not part of the six-contrast Bonferroni decisions'))
    summaries = []
    for column, (history, p) in enumerate(ordering):
        ii = list(analytic.P_VALUES).index(p)
        plus = float(np.mean([r['histories'][history]['rows'][ii]['plus'] for r in records]))
        minus = float(np.mean([r['histories'][history]['rows'][ii]['minus'] for r in records]))
        reference = float(np.mean([r['histories'][history]['rows'][ii]['reference'] for r in records]))
        plus_se = float(np.std([r['histories'][history]['rows'][ii]['plus'] for r in records], ddof=1)/np.sqrt(8))
        minus_se = float(np.std([r['histories'][history]['rows'][ii]['minus'] for r in records], ddof=1)/np.sqrt(8))
        reference_index = 0 if history == 'reference' else 1
        summaries.append(dict(history=history, p=p, plus=plus, minus=minus,
            plus_standard_error=plus_se, minus_standard_error=minus_se,
            plus_nominal_pointwise_95_interval=[plus-critical*plus_se, plus+critical*plus_se],
            minus_nominal_pointwise_95_interval=[minus-critical*minus_se, minus+critical*minus_se],
            contrast=float(means[column]), standard_error=float(se[column]),
            nominal_95_interval=[float(means[column]-critical*se[column]), float(means[column]+critical*se[column])],
            supplementary_Bonferroni_six_interval=[float(means[column]-bonf*se[column]), float(means[column]+bonf*se[column])],
            nominal_pointwise_sign_resolved=bool(abs(means[column]) > critical*se[column]),
            supplementary_family_sign_resolved=bool(abs(means[column]) > bonf*se[column]),
            reference_transfer=reference, contrast_over_reference=means[column]/reference if reference else None,
            plus_over_minus=plus/minus if minus else None,
            ratio_scope='Ratios of ensemble point means only; no qualified ratio interval or factor threshold claim',
            paired_contrast_reference_covariance_of_mean=(np.cov(values[:, column],
                reference_values[:, reference_index], ddof=1)/8).tolist()))
    refinements = []
    if complete_at_start:
        evidence_paths.extend((args.parent/'result.json', args.parent/'compute-ledger.json'))
        names = [('phase-double-0', 'reference', 0, 'phase'),
            ('phase-double-1', 'reference', 1, 'phase'),
            ('halfstep-reference-0', 'reference', 0, 'timestep'),
            ('halfstep-frequency-0', 'frequency', 0, 'timestep')]
        for name, history, rep, kind in names:
            fine_path = args.parent/(name+'.npz')
            fine_metadata = args.parent/(name+'.json')
            coarse_path = args.parent/f'{history}-{rep}.npz'
            evidence_paths.extend((fine_path, fine_metadata))
            fine, coarse = np.load(fine_path), np.load(coarse_path)
            lib = libraries[rep]
            assert np.array_equal(lib['actions'], fine['actions']) and np.array_equal(lib['mass'], fine['mass'])
            delta = fine['family_impulse']-coarse['family_impulse']
            rows = contract(delta, lib['mass'], lib['ratio'], lib['hs'], populations)
            for row, h in zip(rows, lib['hs']):
                denominator = abs(next(r['contrast'] for r in summaries if r['history']==history and r['p']==row['p']))
                row['absolute_weighted_family_difference'] = float(lib['mass'] @ (np.abs(h)*np.abs(delta[:, 0]-delta[:, 1])))
                row['paired_shift_over_ensemble_contrast'] = abs(row['contrast'])/denominator if denominator else None
                row['selected_material_error_screen_pass'] = bool(denominator and abs(row['contrast']) < .1*denominator)
            refinements.append(dict(id=name, history=history, library_id=rep, kind=kind, rows=rows))
    for summary in summaries:
        comparisons = [(entry['id'], entry['kind'], row) for entry in refinements
            if entry['history'] == summary['history'] for row in entry['rows'] if row['p'] == summary['p']]
        summary['selected_material_error_screen'] = dict(
            available_comparisons=len(comparisons),
            phase_comparisons=sum(kind == 'phase' for _, kind, _ in comparisons),
            timestep_comparisons=sum(kind == 'timestep' for _, kind, _ in comparisons),
            all_available_pass=bool(comparisons) and all(row['selected_material_error_screen_pass']
                for _, _, row in comparisons),
            both_phase_and_timestep_tested=bool(comparisons) and any(kind == 'phase' for _, kind, _ in comparisons)
                and any(kind == 'timestep' for _, kind, _ in comparisons),
            scope='Selected paired changes only; missing tests remain untested, not passed')
    hashes = {str(path): sha(path) for path in dict.fromkeys(evidence_paths)}
    result = dict(schema_version=1, started_utc=started,
        status='final_parent_complete_readback' if complete_at_start else 'preliminary_coarse_readback',
        no_new_orbits=True, no_response_optimization=True, new_history_prediction=False,
        parent_complete_at_start=complete_at_start,
        population_normalization='Exact analytic F0 plus/minus alpha deltaF divided by AGAMA sampling DF; common fixed sampling mass retained, no per-population or per-library renormalization',
        summaries=summaries, reference_summaries=reference_summaries, records=records, library_checks=checks,
        comparison_order=[dict(history=h, p=p) for h, p in ordering],
        library_contrast_vectors=values.tolist(), covariance_of_mean=(np.cov(values, rowvar=False)/8).tolist(),
        joint_contrast_reference_order=[dict(history=h, p=p, observable='contrast') for h, p in ordering]+
            [dict(history=h, observable='reference') for h in ('reference', 'frequency')],
        joint_contrast_reference_vectors=np.column_stack((values, reference_values)).tolist(),
        joint_contrast_reference_covariance_of_mean=(np.cov(np.column_stack((values, reference_values)), rowvar=False)/8).tolist(),
        uncertainty=dict(unit='Eight independent method-4 action libraries with independently randomized shared phase rules',
            pointwise='Nominal two-sided 95% Student-t with seven degrees of freedom',
            supplementary='Bonferroni nominal 95% family for these six contrasts, not the complete adaptive campaign',
            coverage='Uncalibrated; neither Student-t approximation nor general coverage is established',
            correlations='Populations and histories share each library; covariance retained'),
        selected_refinements=refinements,
        remaining_checks=['No doubled-phase frequency history in the parent matrix',
            'Selected refinements do not prove all-library discretization accuracy',
            'No live equilibrium, collective stability, formation-history or observational test'],
        source_sha256=hashlib.sha256(source).hexdigest(), evidence_sha256=hashes,
        cpu_seconds=time.process_time()-start_cpu,
        scope='Analytic-moment populations in prescribed recorded fields; no live-galaxy or dark-matter inference')
    write(args.out/'result.json', result)
    (args.out/'COMPLETE').write_text('Frozen analytic population contraction complete; no new orbits.\n')
    print(json.dumps(dict(status=result['status'], summaries=summaries, cpu_seconds=result['cpu_seconds']), indent=2))


if __name__ == '__main__':
    main()
