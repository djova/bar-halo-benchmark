"""Disposable known-value controls, never simulation evidence or publication data."""
import contextlib
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import numpy as np

from reproduce_confirmation import ANALYZER, QUEUE, ROOT, design, run_queue


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_guard():
    with tempfile.TemporaryDirectory(prefix='.confirmation-fixture-', dir=ROOT/'scripts') as temp:
        folder = Path(temp)
        child = folder/'child.py'
        child.write_text("import argparse,time\nfrom pathlib import Path\np=argparse.ArgumentParser();p.add_argument('--out');p.add_argument('--busy',action='store_true');a=p.parse_args()\nd=Path(a.out);d.mkdir()\nif a.busy:\n while True: pass\n(d/'COMPLETE').write_text('Disposable fixture')\n")
        protocol = folder/'protocol.md'
        protocol.write_text('Disposable software fixture, no physics.\n')
        dependency = folder/'external-value.txt'
        dependency.write_text('Mapped dependency fixture.\n')
        source = str(child.relative_to(ROOT))
        base = dict(workers=1, protocol=str(protocol.relative_to(ROOT)),
                    stop_utc=(dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=2)).isoformat(),
                    source_sha256={source: sha(child), 'external/fixture': sha(dependency)},
                    external_sources={'external/fixture': str(dependency)})
        records = []
        for label, busy, cap, wall in [('complete', False, 100, 5),
                                      ('timeout', True, 100, 1), ('cpu', True, 16, 10)]:
            spec = dict(base, cpu_ceiling_seconds=cap, cases=[dict(id='first', script=source,
                        arguments=['--busy'] if busy else [], wall_seconds=wall)])
            if label == 'cpu':
                spec['cases'].append(dict(id='pending', script=source, arguments=[], wall_seconds=5))
            path = folder/(label+'.json')
            path.write_text(json.dumps(spec))
            out = folder/label
            done = subprocess.run([sys.executable, str(ROOT/QUEUE), '--spec', str(path), '--out', str(out)],
                                  capture_output=True, text=True, timeout=20)
            ledger = json.loads((out/'ledger.json').read_text())
            assert done.returncode == (0 if label == 'complete' else 1), done.stderr
            assert (out/'TERMINAL').exists()
            if label == 'cpu':
                assert ledger['stop_reason'] == 'aggregate CPU limit'
                assert ledger['cases']['pending']['state'] == 'not_started'
                assert 0 < ledger['completed_cpu_seconds'] < cap
            records.append(dict(check=label, passed=True, cpu_seconds=ledger['completed_cpu_seconds']))
        spec['source_sha256']['external/fixture'] = '0'*64
        path.write_text(json.dumps(spec))
        done = subprocess.run([sys.executable, str(ROOT/QUEUE), '--spec', str(path), '--out', str(folder/'bad')],
                              capture_output=True, timeout=10)
        assert done.returncode != 0 and not (folder/'bad').exists()
        records.append(dict(check='changed_external_input_refused', passed=True))
        return records


def check_cleanup():
    with tempfile.TemporaryDirectory(prefix='confirmation-cleanup-') as temp:
        folder = Path(temp)
        child = folder/'stubborn.py'
        child.write_text("import signal,time,os,sys\nfrom pathlib import Path\nsignal.signal(signal.SIGTERM,signal.SIG_IGN)\nPath(sys.argv[1]).write_text(str(os.getpid()))\nwhile True:time.sleep(.1)\n")
        parent = folder/'parent.py'
        parent.write_text("import subprocess,sys,time\nfrom pathlib import Path\nsubprocess.Popen([sys.executable,sys.argv[1],sys.argv[2]])\nwhile not Path(sys.argv[2]).exists():time.sleep(.01)\nraise SystemExit(7)\n")
        pidfile = folder/'pid'
        assert run_queue([sys.executable, str(parent), str(child), str(pidfile)], os.environ.copy()) == 7
        pid = int(pidfile.read_text())
        stat = Path(f'/proc/{pid}/stat')
        until = time.monotonic()+2
        while stat.exists() and stat.read_text().rsplit(')', 1)[1].split()[0] != 'Z' and time.monotonic() < until:
            time.sleep(.05)
        assert not stat.exists() or stat.read_text().rsplit(')', 1)[1].split()[0] == 'Z'
        return dict(failed_supervisor_descendant_stopped=True)


def check_known_analysis():
    """Raw shift is zero; a known reduced-only shift must fail discrepancy gates."""
    sys.path.insert(0, str(ROOT/'scripts/noise_sweep'))
    import analyze_cadence_confirmation as analyzer
    forecast = json.loads((ROOT/'forecast.json').read_text())
    case = next(c for c in forecast['cases'] if c['label'] == 'B')
    margin = .1*case['adequacy_half_width']
    with tempfile.TemporaryDirectory(prefix='confirmation-known-values-') as temp:
        root = Path(temp)
        frozen = json.loads((ROOT/'confirmation-manifest.json').read_text())
        frozen.update({'build/noise-sweep/orbit-fourth.so': 'fixture-kernel',
                       'build/noise-sweep/Agama-stable-v2/agama.so': 'fixture-library'})
        cases = design()
        assert len(cases) == 20
        (root/'manifest.json').write_text(json.dumps({'spec': {'cases': cases, 'source_sha256': frozen}}))
        (root/'ledger.json').write_text(json.dumps({'cases': {c['id']: {'state': 'complete'} for c in cases}}))
        (root/'TERMINAL').write_text('Disposable mathematical fixture. Not a simulation.\n')
        for row in cases:
            folder = root/row['id']; folder.mkdir()
            args = row['arguments']
            value = lambda key: args[args.index(key)+1]
            n, start = int(value('--n')), int(value('--start'))
            ids = np.arange(start, start+n)
            initial = np.zeros((n, 6)); initial[:, 0] = ids
            smooth = '--no-noise' in args
            unforced = '--no-bar' in args
            bar = np.zeros(n) if smooth or unforced else ids*1e-12
            reduced = bar.copy()
            if row['id'].startswith('halfcadence') and not smooth:
                reduced += 2*margin
            np.savez(folder/'recorded.npz', particle_ids=ids, initial_actions_angles=initial,
                     final_bar_Lz=bar, final_reduced_bar_Lz=reduced,
                     final_noise_Js=np.zeros(n) if smooth else ids*1e-15)
            result = dict(raw_sha256=sha(folder/'recorded.npz'), forecast_sha256=sha(ROOT/'forecast.json'),
                          config=case['orbit_config'], settings=dict(seed=8302, start=start, n=n,
                          dt=float(value('--dt')), noise_refine=int(value('--noise-refine')),
                          no_noise=smooth, no_bar=unforced, pilot=False, case='B'),
                          source_sha256={k: v for k, v in frozen.items() if k.startswith('benchmark/')},
                          library_sha256='fixture-kernel', agama_library_sha256='fixture-library',
                          all_pass=True, maximum_work_residual=0.,
                          fixture_notice='Artificial known values for analyzer verification, not scientific evidence.')
            (folder/'result.json').write_text(json.dumps(result))
            (folder/'COMPLETE').write_text('Disposable fixture.\n')
        argv = sys.argv
        try:
            sys.argv = ['analyze_cadence_confirmation', '--root', str(root), '--forecast', str(ROOT/'forecast.json'),
                        '--out', str(root/'analysis')]
            with contextlib.redirect_stdout(io.StringIO()):
                analyzer.main()
        finally:
            sys.argv = argv
        result = json.loads((root/'analysis/result.json').read_text())
        assert result['n'] == 131072 and result['first_id'] == 65536 and result['last_id'] == 196607
        assert len(result['chunks_and_controls']) == 10
        assert result['gates']['raw_points'] and result['gates']['raw_intervals']
        assert not result['gates']['discrepancy_points'] and not result['gates']['discrepancy_intervals']
        assert not result['numerically_qualified']
        row = next(r for r in result['refinements'] if r['setting'] == 'halfcadence')
        assert abs(row['discrepancy_shift']['mean']+2*margin) < 1e-20
        return dict(complete_design_readback=True, raw_pass_does_not_mask_discrepancy_failure=True,
                    numerical_failure_preserved=True)


if __name__ == '__main__':
    print(json.dumps(dict(supervisor=check_guard(), cleanup=check_cleanup(), analyzer=check_known_analysis(),
                         scope='Disposable mathematical and process controls. No simulated physical conclusion or full independent reproduction.'), indent=2))
