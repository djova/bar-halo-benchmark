"""Record every frozen accuracy decision before independent population evolution."""
from common import ROOT, load_table, sha
from diagnostic import assess
import argparse
import json
import time
from pathlib import Path
import numpy as np


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--batch', type=Path, required=True)
    p.add_argument('--table', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--s', type=float, required=True)
    p.add_argument('--developmental', action='store_true')
    a = p.parse_args()
    start = time.process_time()
    ledger = json.loads((a.batch/'ledger.json').read_text())
    manifest = json.loads((a.batch/'manifest.json').read_text())
    if not (a.batch/'TERMINAL').exists() or any(r['state']!='complete' for r in ledger['cases'].values()):
        raise ValueError('Complete matrix required')
    meta, table = load_table(a.table)
    records, inputs = [], {}
    for key in sorted(ledger['cases']):
        folder = a.batch/key
        record = json.loads((folder/'result.json').read_text())
        if record['config']['s'] != a.s:
            continue
        if record['table_sha256'] != sha(a.table/'halo-table.npz'):
            raise ValueError('Changed halo table')
        if not record['all_performed_gates_pass'] or sha(folder/'recorded.npz') != record['raw_sha256']:
            raise ValueError('Unqualified or changed kernel')
        with np.load(folder/'recorded.npz') as z:
            records.append((record, z['kernel_edges'].copy(), z['kernel_primitive_cell_average'][:,:,1].copy()))
        inputs[str(folder/'result.json')] = sha(folder/'result.json')
    if len(records) != 8 or any(not np.array_equal(r[1],records[0][1]) for r in records):
        raise ValueError('Eight same-mesh independent batches required')
    if not a.developmental:
        seeds = [r[0]['config']['seed'] for r in records]
        if a.s != .5 or sorted(seeds) != list(range(96101,96109)):
            raise ValueError('Wrong prospective condition or samples')
        for name in ['common.py', 'diagnostic.py']:
            path = Path(__file__).with_name(name)
            if manifest['spec']['source_sha256'][str(path.relative_to(ROOT))] != sha(path):
                raise ValueError('Diagnostic changed after kernel launch')
    fine = np.stack([r[2][:,0] for r in records])
    coarse = np.stack([r[2][:,1] for r in records])
    edges = records[0][1]
    result = assess(edges, fine, coarse, meta, table)
    a.out.mkdir(parents=True, exist_ok=False)
    np.savez_compressed(a.out/'kernel-batches.npz', edges=edges, fine=fine, coarse=coarse)
    result.update(s=a.s, eta=.1, developmental=a.developmental, inputs=inputs,
        raw_sha256=sha(a.out/'kernel-batches.npz'), table_sha256=sha(a.table/'halo-table.npz'),
        protocol_sha256=sha(ROOT/'research/population-accuracy/PLAN.md'),
        source_sha256={n:sha(Path(__file__).with_name(n)) for n in ['common.py','diagnostic.py','forecast.py']},
        cpu_seconds=time.process_time()-start)
    (a.out/'result.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(dict(s=a.s, developmental=a.developmental,
        sign_qualified=sum(r['sign_qualification']!='unqualified' for r in result['rows']),
        five_percent_qualified=sum(r['five_percent_qualified'] for r in result['rows']),
        total_comparisons=len(result['rows']), cpu_seconds=result['cpu_seconds']), indent=2))


if __name__ == '__main__':
    main()
