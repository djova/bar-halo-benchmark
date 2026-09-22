"""Exercise the whole fixed-ID estimator with disposable mathematical fixtures."""
import argparse
import hashlib
import json
import os
import resource
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'scripts/noise_sweep'))
from analyze_physical_transfer import LOCAL_GATES, RECORDED_SOURCES
from reproduce_confirmation import design


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    started = time.monotonic()
    sources = json.loads((ROOT/'physical-analysis-manifest.json').read_text())
    assert all(sha(ROOT/name) == value for name, value in sources.items())
    env = os.environ.copy()
    env.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    def execute(script, arguments):
        return subprocess.run([sys.executable, str(ROOT/'scripts/noise_sweep'/script), *arguments],
                              env=env, capture_output=True, text=True, timeout=60)
    primitive = execute('check_physical_assembly.py', [])
    assert primitive.returncode == 0, primitive.stderr
    forecast = json.loads((ROOT/'forecast.json').read_text())
    case = next(c for c in forecast['cases'] if c['label'] == 'B')
    cfg = case['orbit_config']; band = case['adequacy_half_width']
    count = 524288; ids = np.arange(count)
    js = np.random.default_rng(np.random.SeedSequence([8302, 0])).normal(cfg['mean'], cfg['width'], count)
    angles = np.random.default_rng(np.random.SeedSequence([8302, 1])).uniform(0, 2*np.pi, (count, 3))
    initial = np.column_stack((np.full(count, cfg['jr']), np.full(count, cfg['jz']), 2*js, angles))
    disjoint = (ids < 65536) | (ids >= 196608)
    # Different known shifts make an incorrect primary/disjoint mask detectable.
    difference = np.where(disjoint, -.25*band, .5*band)
    y = 1e-4*np.sin(ids*.07); x = y+difference
    frozen = json.loads((ROOT/'confirmation-manifest.json').read_text())
    frozen.update({'build/noise-sweep/orbit-fourth.so': 'fixture-kernel',
                   'build/noise-sweep/Agama-stable-v2/agama.so': 'fixture-dependency'})
    with tempfile.TemporaryDirectory(prefix='physical-estimator-fixture-') as temp:
        base = Path(temp); prefix = base/'prefix'; confirmation = base/'confirmation'; physical = base/'physical'
        for root in [prefix, confirmation, physical]:
            root.mkdir()
            (root/'TERMINAL').write_text('Disposable fixture. NOT a simulation.\n')
        def write(root, name, start, n, smooth, step=.01, refine=4, unforced=False):
            folder = root/name; folder.mkdir()
            selected = slice(start, start+n)
            np.savez(folder/'recorded.npz', particle_ids=ids[selected], initial_actions_angles=initial[selected],
                     initial_cartesian=np.zeros((n, 6)), final_noise_Js=np.zeros(n),
                     final_bar_Lz=np.zeros(n) if smooth or unforced else x[selected],
                     final_reduced_bar_Lz=np.zeros(n) if smooth or unforced else y[selected])
            result = dict(config=cfg, forecast_sha256=sha(ROOT/'forecast.json'),
                          settings=dict(seed=8302, n=n, start=start, dt=step, noise_refine=refine,
                                        no_noise=smooth, no_bar=unforced, pilot=False, case='B'),
                          source_sha256={k: frozen[k] for k in RECORDED_SOURCES},
                          library_sha256='fixture-kernel', agama_library_sha256='fixture-dependency',
                          gates={k: True for k in LOCAL_GATES}, all_pass=True, cpu_seconds=0.,
                          maximum_work_residual=0., raw_sha256=sha(folder/'recorded.npz'),
                          fixture_notice='Artificial vectors and gate placeholders. Not physics or trajectory validation.')
            (folder/'result.json').write_text(json.dumps(result))
            (folder/'COMPLETE').write_text('Disposable fixture. NOT a simulation.\n')
        cases = design()
        for row in cases:
            a = row['arguments']; value = lambda key: a[a.index(key)+1]
            write(confirmation, row['id'], int(value('--start')), int(value('--n')),
                  '--no-noise' in a, float(value('--dt')), int(value('--noise-refine')), '--no-bar' in a)
        for start, n, root, label in [(0, 16384, prefix, 'candidate'), (16384, 49152, physical, 'candidate-16384')]+[
                (start, 65536, physical, f'candidate-{start}') for start in [196608, 262144, 327680, 393216, 458752]]:
            for smooth in [False, True]:
                write(root, label+('-smooth' if smooth else '-noisy'), start, n, smooth)
        for root in [confirmation, physical]:
            names = sorted(p.name for p in root.iterdir() if p.is_dir())
            (root/'ledger.json').write_text(json.dumps({'cases': {name: {'state': 'complete'} for name in names}}))
            (root/'manifest.json').write_text(json.dumps({'spec': {'cases': cases if root == confirmation else names,
                                                                   'source_sha256': frozen}}))
        numeric_args = ['--root', str(confirmation), '--forecast', str(ROOT/'forecast.json'), '--out', str(base/'numerical')]
        numerical = execute('analyze_cadence_confirmation.py', numeric_args)
        assert numerical.returncode == 0, numerical.stderr
        numerical_path = base/'numerical/result.json'; original_numeric = numerical_path.read_text()
        assert json.loads(original_numeric)['numerically_qualified']
        arguments = ['--prefix-root', str(prefix), '--confirmation-root', str(confirmation),
                     '--confirmation-analysis', str(numerical_path), '--physical-root', str(physical),
                     '--forecast', str(ROOT/'forecast.json')]
        full = execute('analyze_physical_transfer.py', arguments+['--out', str(base/'answer')])
        assert full.returncode == 0, full.stderr
        result = json.loads((base/'answer/result.json').read_text())
        assert result['primary']['n'] == count and result['disjoint_diagnostic']['n'] == 393216
        for key, expected in [('primary', -.0625*band), ('disjoint_diagnostic', -.25*band)]:
            assert abs(result[key]['discrepancy']['mean']-expected) < 1e-18
            assert result[key]['decision'].startswith('Qualified within')
        bad = json.loads(original_numeric); bad['numerically_qualified'] = False
        numerical_path.write_text(json.dumps(bad))
        rejected = execute('analyze_physical_transfer.py', arguments+['--out', str(base/'bad-numerical')])
        assert rejected.returncode != 0 and 'Independent numerical qualification failed' in rejected.stderr
        assert not (base/'bad-numerical').exists()
        numerical_path.write_text(original_numeric)
        manifest_path = physical/'manifest.json'; original_manifest = manifest_path.read_text()
        bad = json.loads(original_manifest); bad['spec']['source_sha256']['benchmark/orbit_fourth.cpp'] = 'changed-fixture'
        manifest_path.write_text(json.dumps(bad))
        rejected = execute('analyze_physical_transfer.py', arguments+['--out', str(base/'bad-source')])
        assert rejected.returncode != 0 and 'Physical queue differs' in rejected.stderr
        assert not (base/'bad-source').exists()
        manifest_path.write_text(original_manifest)
        # Corrupt both paired initial states, preserving their mutual identity and hashes.
        # The full seeded-population check must still refuse them.
        for kind in ['noisy', 'smooth']:
            folder = prefix/('candidate-'+kind)
            with np.load(folder/'recorded.npz') as loaded:
                arrays = {key: loaded[key].copy() for key in loaded.files}
            arrays['initial_actions_angles'][0, 0] += .001
            np.savez(folder/'recorded.npz', **arrays)
            record = json.loads((folder/'result.json').read_text()); record['raw_sha256'] = sha(folder/'recorded.npz')
            (folder/'result.json').write_text(json.dumps(record))
        rejected = execute('analyze_physical_transfer.py', arguments+['--out', str(base/'bad-seed')])
        assert rejected.returncode != 0 and 'Full population differs' in rejected.stderr
        assert not (base/'bad-seed').exists()
    receipt = dict(primitive_controls=json.loads(primitive.stdout), complete_fixed_id_assembly=True,
                   primary_and_disjoint_known_means=True, failed_numerical_confirmation_refused=True,
                   changed_queue_source_refused=True, mutually_matching_but_wrong_seeded_states_refused=True,
                   source_sha256=sources, wall_seconds=time.monotonic()-started,
                   cpu_seconds=sum(getattr(resource.getrusage(who), field)
                                   for who in [resource.RUSAGE_SELF, resource.RUSAGE_CHILDREN]
                                   for field in ['ru_utime', 'ru_stime']),
                   scope='Disposable mathematical fixtures only. No force solver, simulation, physical qualification, '
                         'full-population reproduction or actual reference comparison. Temporary arrays deleted.')
    if args.out:
        with args.out.open('x') as f:
            f.write(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
