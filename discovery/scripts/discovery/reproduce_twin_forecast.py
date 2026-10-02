"""Regenerate an unforced coefficient forecast, not a driven-orbit experiment."""
from pathlib import Path
import argparse
import ast
import hashlib
import importlib.util
import json
import resource
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case', choices=list('abcdefg')+['all'], default='a')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--cpu-cap', type=int, default=5)
    a = p.parse_args()
    resource.setrlimit(resource.RLIMIT_CPU, (a.cpu_cap, a.cpu_cap+1))
    start = time.process_time()
    source = ROOT/'source-snapshots/twin-forecast/operator.py'
    provenance = json.loads(source.with_name('function-provenance.json').read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==provenance['operator_sha256']
    tree = ast.parse(source.read_text())
    for r in provenance['functions']:
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name==r['name'])
        assert hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()==r['function_ast_sha256']
    spec = importlib.util.spec_from_file_location('operator', source)
    operator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(operator)
    populations = json.loads((ROOT/'operands/twin-forecast/populations.json').read_text())['populations']
    stages = json.loads((ROOT/'data/checks-v2.json').read_text())['twin_forecast']['stages']
    a.output.mkdir(parents=True, exist_ok=False)
    outputs, previous = [], None
    for r in stages:
        if a.case!='all' and r['id']!=a.case:
            continue
        arrays = operator.coefficient_grid(np, *r['grid'], r['anomaly_order'], r['radial_mode_limit'])
        same = previous is not None and np.array_equal(previous['binding_energy'], arrays['binding_energy']) and np.array_equal(previous['radial_modes'], arrays['radial_modes'])
        computed = operator.contract(np, operator, arrays, populations, previous if same else None)
        # Single even-anomaly cases omit the paired norm proxy by design.
        # All-case execution retains pairing exactly as in the original matrix.
        for actual, saved in zip(computed['rows'], r['rows']):
            assert actual['p']==saved['p']
            for name in ['forecast','absolute_mode_contribution','absolute_over_net','signed_inplane_contributions']:
                if not np.allclose(actual[name], saved[name], rtol=2e-11, atol=0):
                    raise AssertionError(f"{r['id']} {actual['p']} {name}")
            if r['id'] in 'adf' or same:
                for name in ['tail_proxy_full_norm','tail_proxy_residual_norm']:
                    assert np.isclose(actual[name], saved[name], rtol=2e-11, atol=0)
        record = dict(id=r['id'], grid=r['grid'], anomaly_order=r['anomaly_order'], radial_mode_limit=r['radial_mode_limit'], **computed)
        (a.output/f"forecast-{r['id']}.json").write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
        np.savez_compressed(a.output/f"forecast-{r['id']}.npz", **arrays)
        outputs.append(r['id'])
        previous = arrays
    receipt = dict(status='PASS', cases=outputs, cpu_seconds=time.process_time()-start,
                   numpy_version=np.__version__, operator_sha256=provenance['operator_sha256'],
                   scope='Unforced coefficients and second-order contraction only. No independent forced dynamics or physical validation.')
    (a.output/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__=='__main__':
    main()
