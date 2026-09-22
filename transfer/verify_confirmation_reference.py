"""Compare a same-sample public reproduction without reopening qualification."""
import argparse
import json
import math
from pathlib import Path

PAIRS = {f'{label}-{start}': (start, 32768)
         for label in ['candidate', 'halfcadence']
         for start in [65536, 98304, 131072, 163840]}
PAIRS.update(halfstep=(65536, 16384), unforced=(65536, 4096))
CASES = {label+'-'+kind for label in PAIRS for kind in ['noisy', 'smooth']}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(actual, reference):
    for key, expected in [('n', 131072), ('first_id', 65536), ('last_id', 196607),
                          ('numerical_margin', 1.8126730139721574e-7)]:
        require(actual[key] == reference[key] == expected, 'Changed '+key)
    for key in ['forecast_sha256', 'analysis_sha256', 'gates', 'numerically_qualified']:
        require(actual[key] == reference[key], 'Changed '+key)
    for data in [actual, reference]:
        require(data['numerically_qualified'] == all(data['gates'].values()),
                'Inconsistent numerical qualification')
        require(set(data['source_sha256']) == CASES, 'Missing or additional source case')
        require(len(data['refinements']) == 2 and
                {r['setting'] for r in data['refinements']} == {'halfstep', 'halfcadence'},
                'Missing numerical intervention')
        require(math.isfinite(data['brownian_endpoint_difference']) and
                0 <= data['brownian_endpoint_difference'] < 1e-12,
                'Changed Brownian endpoint identity')
        require(len(data['chunks_and_controls']) == len(PAIRS) and
                {r['label'] for r in data['chunks_and_controls']} == set(PAIRS),
                'Missing or repeated paired chunk/control')
    records = []
    descriptive = []

    def compare(label, x, y, n):
        require(x['n'] == y['n'] == n, 'Changed estimator sample size: '+label)
        for row in [x, y]:
            require(len(row['ci95']) == 2, 'Invalid interval: '+label)
            values = [row['mean'], row['se'], row['half_width'], *row['ci95']]
            require(all(math.isfinite(v) for v in values), 'Nonfinite estimator: '+label)
            require(row['se'] >= 0 and row['half_width'] >= 0 and
                    row['ci95'][0] <= row['mean'] <= row['ci95'][1], 'Invalid estimator: '+label)
        for key in ['mean', 'se', 'half_width']:
            error = abs(x[key]-y[key])
            require(error < 1e-9, 'Scalar reproduction tolerance exceeded: '+label+'.'+key)
            records.append(dict(quantity=label+'.'+key, absolute_difference=error))
        error = max(abs(a-b) for a, b in zip(x['ci95'], y['ci95']))
        require(error < 1e-9, 'Interval reproduction tolerance exceeded: '+label)
        records.append(dict(quantity=label+'.ci95', absolute_difference=error))

    for key in ['candidate_raw_3D', 'candidate_reduced', 'candidate_discrepancy']:
        compare(key, actual[key], reference[key], 131072)
    for row in actual['refinements']:
        label = row['setting']
        ref = next(r for r in reference['refinements'] if r['setting'] == label)
        n = 16384 if label == 'halfstep' else 131072
        for key in ['raw_3D_shift', 'discrepancy_shift', 'reduced_shift']:
            x, y = row[key], ref[key]
            compare(label+'.'+key, x, y, n)
            if key == 'reduced_shift':
                continue
            margin = actual['numerical_margin']
            for data in [x, y]:
                require(data['point_pass'] == (abs(data['mean']) < margin) and
                        data['interval_pass'] == (max(abs(v) for v in data['ci95']) < margin),
                        'Inconsistent numerical decision: '+label+'.'+key)
                require(len(data['largest20_ids']) == 20 and len(set(data['largest20_ids'])) == 20,
                        'Invalid descriptive rank list')
                require(all(65536 <= i < 65536+n for i in data['largest20_ids']),
                        'Ranked ID outside declared sample')
                require(math.isfinite(data['largest20_variance_fraction']) and
                        0 <= data['largest20_variance_fraction'] <= 1 and
                        math.isfinite(data['maximum_absolute_individual_change']),
                        'Invalid descriptive concentration')
            for flag in ['point_pass', 'interval_pass']:
                require(x[flag] == y[flag], 'Changed numerical decision: '+label+'.'+key)
            descriptive.append(dict(quantity=label+'.'+key,
                rank_order_identical=x['largest20_ids'] == y['largest20_ids'],
                variance_fraction_difference=abs(x['largest20_variance_fraction']-y['largest20_variance_fraction']),
                maximum_individual_difference=abs(x['maximum_absolute_individual_change']-y['maximum_absolute_individual_change'])))
    for row in actual['chunks_and_controls']:
        label = row['label']
        ref = next(r for r in reference['chunks_and_controls'] if r['label'] == label)
        start, n = PAIRS[label]
        require(row['start'] == ref['start'] == start and row['n'] == ref['n'] == n,
                'Changed paired sample coverage: '+label)
        for key in ['raw', 'reduced', 'discrepancy']:
            compare(label+'.'+key, row[key], ref[key], n)
    return dict(all_pass=True, absolute_tolerance=1e-9, measurements=records,
                maximum_scalar_difference=max(r['absolute_difference'] for r in records),
                descriptive_tail_comparison=descriptive, gates_agree=True,
                numerical_qualification=actual['numerically_qualified'],
                scope='Same-seed reproducibility, not another independent statistical sample. '
                      'The original numerical criterion and failed qualification are unchanged. '
                      'Full individual-array differences require the separate archive comparison.')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--result', type=Path, required=True)
    p.add_argument('--reference', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    result = verify(json.loads(a.result.read_text()), json.loads(a.reference.read_text()))
    with a.out.open('x') as stream:
        stream.write(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
