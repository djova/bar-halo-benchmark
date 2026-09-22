"""Compare the original and public same-sample matrices after both terminate."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_confirmation_reference import CASES, verify, require


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare_array(xx, yy, label):
    require(xx.shape == yy.shape, 'Different array shape: '+label)
    require(xx.dtype == yy.dtype, 'Different array dtype: '+label)
    require(np.isfinite(xx).all() and np.isfinite(yy).all(), 'Nonfinite array: '+label)
    # array_equal regards +0 and -0 as equal; the published field promises bytes.
    return dict(bitwise_identical=xx.tobytes(order='C') == yy.tobytes(order='C'),
                maximum_absolute_difference=float(np.max(abs(xx-yy))) if xx.size else 0.)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--original', type=Path, required=True)
    p.add_argument('--reference-analysis', type=Path, required=True)
    p.add_argument('--isolated', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    actual = json.loads((a.isolated/'analysis/result.json').read_text())
    reference = json.loads(a.reference_analysis.read_text())
    scalar = verify(actual, reference)
    for folder in [a.original, a.isolated/'cases']:
        require((folder/'TERMINAL').exists(), 'Incomplete matrix')
        ledger = json.loads((folder/'ledger.json').read_text())
        require(set(ledger['cases']) == CASES and
                all(v['state'] == 'complete' for v in ledger['cases'].values()),
                'Missing or stopped case')
    rows = []
    for name in sorted(CASES):
        folders = [a.original/name, a.isolated/'cases'/name]
        records = [json.loads((folder/'result.json').read_text()) for folder in folders]
        for folder, record in zip(folders, records):
            require((folder/'COMPLETE').exists(), 'Incomplete case')
            require(sha(folder/'recorded.npz') == record['raw_sha256'], 'Changed recorded arrays')
            require(record['all_pass'] == all(record['gates'].values()), 'Inconsistent local gates')
        for key in ['gates', 'config', 'source_sha256', 'forecast_sha256']:
            require(records[0][key] == records[1][key], 'Different '+key+': '+name)
        for key, value in records[0]['settings'].items():
            if key not in ['agama_path', 'forecast']:
                require(records[1]['settings'][key] == value, 'Different setting: '+key)
        differences = {}
        with np.load(folders[0]/'recorded.npz') as x, np.load(folders[1]/'recorded.npz') as y:
            require(set(x.files) == set(y.files), 'Different array collection')
            for key in x.files:
                xx, yy = x[key], y[key]
                difference = compare_array(xx, yy, name+'/'+key)
                if key in ['particle_ids', 'initial_actions_angles', 'times', 'fast_times', 'fast_events']:
                    require(difference['bitwise_identical'],
                            'Changed initial state, ID or recording schedule: '+name+'/'+key)
                differences[key] = difference
        rows.append(dict(case=name, arrays=differences, local_gates_agree=True,
                         scientific_sources_identical=True,
                         original_raw_sha256=records[0]['raw_sha256'],
                         isolated_raw_sha256=records[1]['raw_sha256'],
                         original_agama_library_sha256=records[0]['agama_library_sha256'],
                         isolated_agama_library_sha256=records[1]['agama_library_sha256']))
    ledger = json.loads((a.isolated/'cases/ledger.json').read_text())
    result = dict(all_declared_checks_pass=True, scalar_verification=scalar, cases=rows,
                  isolated_scientific_core_hours=ledger['completed_cpu_seconds']/3600,
                  original_analysis_sha256=sha(a.reference_analysis),
                  isolated_analysis_sha256=sha(a.isolated/'analysis/result.json'),
                  comparison_source_sha256=sha(Path(__file__)),
                  scope='Fresh public source copy using the existing separate pinned environment '
                        'and independently built dependency. Same-seed reproducibility, not new '
                        'physical evidence or another statistical sample. Cartesian differences '
                        'are reported; no unmeasured bitwise equality or new build is claimed.')
    a.out.mkdir(parents=True, exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(dict(all_declared_checks_pass=True,
                         maximum_scalar_difference=scalar['maximum_scalar_difference'],
                         isolated_scientific_core_hours=result['isolated_scientific_core_hours']), indent=2))


if __name__ == '__main__':
    main()
