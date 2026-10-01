"""Replay saved-history contractions and uncertainty; no sampling or evolution.

Only NumPy and SciPy are required. Stored Fq values replace the original AGAMA
evaluation; all target DF values are rebuilt from the frozen 96-term series.
"""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def f0(e):
    coefficients = [Fraction(1)]
    for n in range(95):
        coefficients.append(coefficients[-1] * Fraction((n+2)*(n+5)**2,
            (n+1)*(n+4)*(2*n+7)))
    return (8/(5*np.sqrt(2)*np.pi**3) * e**2.5 *
            np.polynomial.polynomial.polyval(e, np.array([float(x) for x in coefficients])))


def weights(data, populations):
    e, angular, lz, q = (data[key] for key in ('e', 'L', 'Lz', 'sampling_DF_Fq'))
    assert np.all((e > 0) & (e < 1)) and np.all(q > 0) and np.all(np.isfinite(q))
    ratio = f0(e)/q
    assert np.max(abs(ratio-1)) < .001
    hs = []
    for pop in populations:
        p = pop['p']
        g0 = -4*p/((p+2.5)*(p+3.5))*e**(p-1) + 4/(p+3.5)*e**p
        h = pop['alpha'] * lz*(g0+angular*angular*e**p)/q
        assert np.max(abs(h/ratio)) <= .5+1e-10
        assert np.all(ratio+h > 0) and np.all(ratio-h > 0)
        hs.append(h)
    return ratio, np.array(hs)


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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    operands = ROOT/'operands/exact-twins'
    manifest = json.loads((operands/'manifest.json').read_text())
    frozen = json.loads((operands/'frozen-populations.json').read_text())
    published = json.loads((ROOT/'data/twins-exact.json').read_text())
    populations = frozen['populations']
    assert [x['p'] for x in populations] == [4, 6, 8]
    records, libraries = [], {}
    for entry in manifest['libraries']:
        rep = entry['library_id']; path = operands/entry['path']
        assert sha(path) == entry['sha256']
        data = np.load(path, allow_pickle=False)
        assert set(data.files) == set(entry['arrays'])
        assert np.all(data['masses'] > 0)
        ratio, hs = weights(data, populations)
        libraries[rep] = (data, ratio, hs)
        histories = {}
        for history in ('reference', 'frequency'):
            impulses = np.column_stack((data[history+'_Ipro'], data[history+'_Iretro']))
            histories[history] = dict(rows=contract(impulses, data['masses'], ratio, hs, populations))
        records.append(dict(library_id=rep, histories=histories))
    assert len(records) == 8
    values = np.array([[row['contrast'] for history in ('reference', 'frequency')
        for row in record['histories'][history]['rows']] for record in records])
    refs = np.array([[record['histories'][history]['rows'][0]['reference']
        for history in ('reference', 'frequency')] for record in records])
    means = values.mean(axis=0); se = values.std(axis=0, ddof=1)/np.sqrt(8)
    critical = float(t.ppf(.975, 7)); bonf = float(t.ppf(1-.05/(2*6), 7))
    summaries, reference_summaries = [], []
    for index, history in enumerate(('reference', 'frequency')):
        mean = float(refs[:, index].mean()); error = float(refs[:, index].std(ddof=1)/np.sqrt(8))
        reference_summaries.append(dict(history=history, transfer=mean, standard_error=error,
            nominal_pointwise_95_interval=[mean-critical*error, mean+critical*error]))
        for ii, pop in enumerate(populations):
            column = index*3+ii
            sample = [record['histories'][history]['rows'][ii] for record in records]
            plus = float(np.mean([row['plus'] for row in sample])); minus = float(np.mean([row['minus'] for row in sample]))
            plus_se = float(np.std([row['plus'] for row in sample], ddof=1)/np.sqrt(8))
            minus_se = float(np.std([row['minus'] for row in sample], ddof=1)/np.sqrt(8))
            summaries.append(dict(history=history, p=pop['p'], plus=plus, minus=minus,
                plus_standard_error=plus_se, minus_standard_error=minus_se,
                plus_nominal_pointwise_95_interval=[plus-critical*plus_se, plus+critical*plus_se],
                minus_nominal_pointwise_95_interval=[minus-critical*minus_se, minus+critical*minus_se],
                contrast=float(means[column]), standard_error=float(se[column]),
                nominal_95_interval=[float(means[column]-critical*se[column]), float(means[column]+critical*se[column])],
                supplementary_Bonferroni_six_interval=[float(means[column]-bonf*se[column]), float(means[column]+bonf*se[column])],
                nominal_pointwise_sign_resolved=bool(abs(means[column]) > critical*se[column]),
                supplementary_family_sign_resolved=bool(abs(means[column]) > bonf*se[column]),
                reference_transfer=mean, contrast_over_reference=float(means[column]/mean), plus_over_minus=plus/minus,
                paired_contrast_reference_covariance_of_mean=(np.cov(values[:, column], refs[:, index], ddof=1)/8).tolist()))
    refinements = []
    for name, history, rep, kind in [('phase-double-0','reference',0,'phase'),
        ('phase-double-1','reference',1,'phase'), ('halfstep-reference-0','reference',0,'timestep'),
        ('halfstep-frequency-0','frequency',0,'timestep')]:
        data, ratio, hs = libraries[rep]; key = name.replace('-', '_')
        delta = np.column_stack((data[key+'_Ipro']-data[history+'_Ipro'], data[key+'_Iretro']-data[history+'_Iretro']))
        rows = contract(delta, data['masses'], ratio, hs, populations)
        for row, h in zip(rows, hs):
            denominator = abs(next(x['contrast'] for x in summaries if x['history']==history and x['p']==row['p']))
            row['absolute_weighted_family_difference'] = float(data['masses'] @ (abs(h)*abs(delta[:,0]-delta[:,1])))
            row['paired_shift_over_ensemble_contrast'] = abs(row['contrast'])/denominator
            row['selected_material_error_screen_pass'] = abs(row['contrast']) < .1*denominator
        refinements.append(dict(id=name, history=history, library_id=rep, kind=kind, rows=rows))
    joint = np.column_stack((values, refs))
    result = dict(records=records, summaries=summaries, reference_summaries=reference_summaries,
        library_contrast_vectors=values.tolist(), covariance_of_mean=(np.cov(values,rowvar=False)/8).tolist(),
        joint_contrast_reference_vectors=joint.tolist(), joint_contrast_reference_covariance_of_mean=(np.cov(joint,rowvar=False)/8).tolist(),
        selected_refinements=refinements)
    differences = []
    def compare(actual, expected):
        if isinstance(actual, dict):
            for key, value in actual.items(): compare(value, expected[key])
        elif isinstance(actual, list):
            assert len(actual) == len(expected)
            for x, y in zip(actual, expected): compare(x, y)
        elif isinstance(actual, (float, int)) and not isinstance(actual, bool):
            difference = abs(actual-expected); differences.append(difference)
            assert difference <= 1e-17 + 1e-12*abs(expected), (actual, expected)
        else: assert actual == expected
    compare({key:value for key,value in result.items() if key!='selected_refinements'}, published)
    compare(refinements, published['numerical_checks']['selected_refinements'])
    result['receipt'] = dict(all_published_comparisons_pass=True, compared_numeric_values=len(differences),
        maximum_absolute_difference=max(differences), absolute_slack=1e-17, relative_slack=1e-12,
        source_sha256=sha(Path(__file__)), operand_manifest_sha256=sha(operands/'manifest.json'),
        published_export_sha256=sha(ROOT/'data/twins-exact.json'), frozen_populations_sha256=sha(operands/'frozen-populations.json'),
        environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
        scope='Software/arithmetic replay of fixed stored impulses, frozen populations and stored sampling densities. No new physical sample, AGAMA DF regeneration, orbit evolution or growth-history prediction.')
    (args.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result['receipt'],indent=2))


if __name__ == '__main__':
    main()
