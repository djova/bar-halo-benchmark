"""Replay growing-bar population contractions from compact saved operands.

NumPy/SciPy only: no AGAMA, initial-condition generation, trajectory evolution,
credentials, or remote service. This verifies saved-array arithmetic, not the
underlying force law, uncertainty coverage, or a live-halo prediction.
"""
import os
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
import argparse
import hashlib
import json
from pathlib import Path
import platform
import time
import numpy as np
import scipy
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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


def ensemble(records):
    critical = float(t.ppf(.975, 7))
    bonf = float(t.ppf(1-.05/(2*3), 7))
    values = np.array([[[row['contrast'] for row in h['transfer_rows']]
        for h in record['histories']] for record in records])
    refs = np.array([[h['transfer_rows'][0]['reference'] for h in record['histories']] for record in records])
    means = values.mean(axis=0)
    errors = values.std(axis=0, ddof=1)/np.sqrt(8)
    histories = []
    for time_id in range(25):
        rows = []
        for col, p in enumerate((4, 6, 8)):
            plus = np.array([r['histories'][time_id]['transfer_rows'][col]['plus'] for r in records])
            minus = np.array([r['histories'][time_id]['transfer_rows'][col]['minus'] for r in records])
            mean, error = float(means[time_id, col]), float(errors[time_id, col])
            ref = float(refs[:, time_id].mean())
            rows.append(dict(p=p, plus=float(plus.mean()), minus=float(minus.mean()),
                contrast=mean, standard_error=error,
                nominal_pointwise_95_interval=[mean-critical*error, mean+critical*error],
                supplementary_three_population_Bonferroni_interval=[mean-bonf*error, mean+bonf*error],
                nominal_pointwise_sign_resolved=bool(abs(mean)>critical*error),
                supplementary_three_population_sign_resolved=bool(abs(mean)>bonf*error),
                reference=ref, contrast_over_reference=mean/ref if ref else None,
                plus_over_minus=float(plus.mean()/minus.mean()) if minus.mean() else None,
                plus_standard_error=float(plus.std(ddof=1)/np.sqrt(8)),
                minus_standard_error=float(minus.std(ddof=1)/np.sqrt(8))))
        joint = np.column_stack((values[:, time_id], refs[:, time_id]))
        histories.append(dict(time=12.5*time_id, rows=rows,
            contrast_reference_mean_covariance=(np.cov(joint, rowvar=False)/8).tolist()))
    reference_mean = float(refs[:, -1].mean())
    reference_error = float(refs[:, -1].std(ddof=1)/np.sqrt(8))
    joint = np.column_stack((values[:, -1], refs[:, -1]))
    return dict(endpoint_rows=histories[-1]['rows'], histories=histories,
        critical_pointwise=critical, critical_Bonferroni_three=bonf,
        contrast_order=[4, 6, 8], library_contrast_history=values.tolist(), library_reference_history=refs.tolist(),
        endpoint_reference=dict(mean=reference_mean, standard_error=reference_error,
            nominal_pointwise_95_interval=[reference_mean-critical*reference_error, reference_mean+critical*reference_error]),
        joint_endpoint_order=['contrast_p4', 'contrast_p6', 'contrast_p8', 'reference'],
        joint_endpoint_vectors=joint.tolist(),
        joint_endpoint_covariance_of_mean=(np.cov(joint, rowvar=False)/8).tolist())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    cpu, wall = time.process_time(), time.monotonic()
    operands = ROOT/'operands/twins-growth-v1'
    manifest = json.loads((operands/'manifest.json').read_text())
    published = json.loads((ROOT/'data/twins-growth-v1.json').read_text())
    populations = published['frozen_populations']
    assert [r['p'] for r in populations] == [4, 6, 8]
    libraries, records = {}, []
    for entry in manifest['libraries']:
        path = operands/entry['path']
        assert sha(path) == entry['sha256']
        with np.load(path, allow_pickle=False) as archive:
            data = {key:archive[key].copy() for key in archive.files}
        assert set(data) == set(entry['arrays'])
        for key, description in entry['arrays'].items():
            assert list(data[key].shape) == description['shape'] and data[key].dtype.str == description['dtype']
            assert np.all(np.isfinite(data[key]))
        assert np.array_equal(data['times'], np.arange(25)*12.5)
        assert np.all(data['mass'] > 0) and np.all(data['F0_over_Fq'] > 0)
        assert np.all(data['F0_over_Fq']+data['signed_deltaF_over_Fq'] > 0)
        assert np.all(data['F0_over_Fq']-data['signed_deltaF_over_Fq'] > 0)
        histories = []
        for index, when in enumerate(data['times']):
            histories.append(dict(time=float(when),
                transfer_rows=contract(data['family_impulses'][index], data['mass'], data['F0_over_Fq'],
                    data['signed_deltaF_over_Fq'], populations),
                external_work_rows=contract(data['family_external_work'][index], data['mass'], data['F0_over_Fq'],
                    data['signed_deltaF_over_Fq'], populations)))
        records.append(dict(id=entry['id'], histories=histories))
        libraries[entry['library_id']] = data
    assert len(records) == 8 and list(libraries) == list(range(8))
    summary = ensemble(records)
    base = libraries[0]
    refinements = []
    for ident in ('azimuth-double-0', 'radial-vertical-double-0', 'halfstep-0'):
        prefix = ident.replace('-', '_')
        delta = base[prefix+'_family_impulses']-base['family_impulses']
        history = []
        for time_id in range(25):
            rows = contract(delta[time_id], base['mass'], base['F0_over_Fq'], base['signed_deltaF_over_Fq'], populations)
            for row, h in zip(rows, base['signed_deltaF_over_Fq']):
                row['absolute_weighted_family_difference'] = float(base['mass'] @ (abs(h)*abs(delta[time_id, :, 0]-delta[time_id, :, 1])))
            history.append(dict(time=12.5*time_id, rows=rows))
        for row, endpoint in zip(history[-1]['rows'], summary['endpoint_rows']):
            denominator = abs(endpoint['contrast'])
            row['signed_refinement_shift'] = row['contrast']
            row['absolute_shift_over_ensemble_contrast'] = abs(row['contrast'])/denominator if denominator else None
            row['selected_material_error_screen_pass'] = bool(denominator and abs(row['contrast']) < .1*denominator)
        refinements.append(dict(id=ident, history=history, endpoint_rows=history[-1]['rows']))
    for row in summary['endpoint_rows']:
        candidates = [r for refinement in refinements for r in refinement['endpoint_rows'] if r['p']==row['p']]
        row['selected_refinement_qualification'] = dict(all_pass=all(r['selected_material_error_screen_pass'] for r in candidates))
    result = dict(coarse_contractions=records, ensemble=summary, selected_refinements=refinements)
    differences = []
    def compare(actual, expected, pointer=''):
        if isinstance(actual, dict):
            for key, value in actual.items(): compare(value, expected[key], pointer+'/'+key)
        elif isinstance(actual, list):
            assert len(actual) == len(expected), pointer
            for index, (x, y) in enumerate(zip(actual, expected)): compare(x, y, pointer+'/'+str(index))
        elif isinstance(actual, (int, float)) and not isinstance(actual, bool):
            difference = abs(actual-expected)
            differences.append(difference)
            assert difference <= 1e-17+1e-12*abs(expected), (pointer, actual, expected)
        else:
            assert actual == expected, (pointer, actual, expected)
    compare(result, published['replay_targets'])
    result['receipt'] = dict(all_selected_saved_arithmetic_comparisons_pass=True,
        compared_numeric_values=len(differences), maximum_absolute_difference=max(differences),
        absolute_slack=1e-17, relative_slack=1e-12, cpu_seconds=time.process_time()-cpu,
        wall_seconds=time.monotonic()-wall, source_sha256=sha(Path(__file__)),
        operand_manifest_sha256=sha(operands/'manifest.json'), published_export_sha256=sha(ROOT/'data/twins-growth-v1.json'),
        environment=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__),
        scope='Arithmetic replay of frozen weights and saved family impulse/work histories; no new orbital evolution, physical sample or confidence-coverage validation')
    (args.out/'result.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(result['receipt'], indent=2))


if __name__ == '__main__':
    main()
