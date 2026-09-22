"""Reproduce the fixed independent numerical sample; no physical extension."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
RUNNER = 'scripts/noise_sweep/run_orbits_cadence.py'
ANALYZER = 'scripts/noise_sweep/analyze_cadence_confirmation.py'
QUEUE = 'scripts/noise_sweep/guarded_queue.py'
DEPENDENCY = 'build/noise-sweep/Agama-stable-v2/agama.so'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def design(smoke=False):
    """Exact order, IDs and settings of the original twenty-case amendment."""
    variants = []
    for start in [65536, 98304, 131072, 163840]:
        for label, refine in [('candidate', 4), ('halfcadence', 8)]:
            variants.append((f'{label}-{start}', start, 32768, .01, refine, False))
    variants.extend([('halfstep', 65536, 16384, .005, 4, False),
                     ('unforced', 65536, 4096, .01, 4, True)])
    if smoke:
        variants = [('smoke', 0, 128, .01, 4, True)]
    cases = []
    for label, start, n, step, refine, unforced in variants:
        for smooth in [False, True]:
            arguments = ['--seed', '8192' if smoke else '8302', '--n', str(n),
                         '--start', str(start), '--dt', str(step),
                         '--noise-refine', str(refine)]
            arguments += ['--pilot'] if smoke else ['--forecast', 'forecast.json', '--case', 'B']
            if unforced:
                arguments.append('--no-bar')
            if smooth:
                arguments.append('--no-noise')
            cases.append(dict(id=label+('-smooth' if smooth else '-noisy'),
                              script=RUNNER, arguments=arguments, wall_seconds=7200))
    return cases


def run_queue(command, env):
    # A failed supervisor must not leave scientific children running elsewhere.
    proc = subprocess.Popen(command, cwd=ROOT, env=env, start_new_session=True)
    try:
        return proc.wait()
    finally:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        until = time.monotonic()+3
        while time.monotonic() < until:
            try:
                os.killpg(proc.pid, 0)
            except ProcessLookupError:
                break
            time.sleep(.05)
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agama', type=Path)
    p.add_argument('--out', type=Path)
    p.add_argument('--workers', type=int, choices=[1, 2, 3], default=1)
    p.add_argument('--smoke', action='store_true')
    p.add_argument('--show-design', action='store_true')
    p.add_argument('--stop-utc', help='Optional timezone-aware ISO deadline; may only shorten the default stop')
    a = p.parse_args()
    if a.show_design:
        print(json.dumps(design(a.smoke), indent=2))
        return
    if not sys.platform.startswith('linux'):
        p.error('This guarded command requires Linux /proc CPU accounting.')
    if a.agama is None or a.out is None:
        p.error('--agama and --out are required for execution')
    library = a.agama.resolve()
    if not (library/'agama.so').is_file():
        p.error('Build the pinned, fully patched dependency first; see transfer/README.md')
    now = dt.datetime.now(dt.timezone.utc)
    stop = now+dt.timedelta(hours=2 if a.smoke else 41)
    if a.stop_utc:
        try:
            requested = dt.datetime.fromisoformat(a.stop_utc.replace('Z', '+00:00'))
            if requested.tzinfo is None or requested <= now:
                raise ValueError('Deadline must have a timezone and be in the future')
            stop = min(stop, requested)
        except ValueError as error:
            p.error(str(error))
    source_manifest = json.loads((ROOT/'confirmation-manifest.json').read_text())
    for name, expected in source_manifest.items():
        if sha(ROOT/name) != expected:
            raise RuntimeError('Changed packaged source: '+name)
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    build = ROOT/'build/noise-sweep'
    build.mkdir(parents=True, exist_ok=True)
    subprocess.run(['nice', '-n', '10', 'c++', '-std=c++17', '-O3', '-fno-math-errno',
                    '-fPIC', '-shared', str(ROOT/'benchmark/orbit_fourth.cpp'),
                    '-o', str(build/'orbit-fourth.so')], check=True, timeout=120)
    sources = {**source_manifest, 'build/noise-sweep/orbit-fourth.so': sha(build/'orbit-fourth.so'),
               DEPENDENCY: sha(library/'agama.so')}
    cases = design(a.smoke)
    for case in cases:
        case['arguments'] += ['--agama-path', str(library)]
    spec = dict(protocol='INDEPENDENT_CADENCE_CONFIRMATION.md', workers=a.workers,
                cpu_ceiling_seconds=300 if a.smoke else 14*3600,
                stop_utc=stop.isoformat(),
                source_sha256=sources, external_sources={DEPENDENCY: str(library/'agama.so')},
                cases=cases)
    spec_path = out/'execution-spec.json'
    spec_path.write_text(json.dumps(spec, indent=2)+'\n')
    env = os.environ.copy()
    env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    code = run_queue([sys.executable, str(ROOT/QUEUE), '--spec', str(spec_path),
                      '--out', str(out/'cases')], env)
    if code:
        raise SystemExit('Finite queue stopped or failed; preserve its ledger and outputs. No qualification.')
    ledger = json.loads((out/'cases/ledger.json').read_text())
    local = {}
    for case in cases:
        folder = out/'cases'/case['id']
        result = json.loads((folder/'result.json').read_text())
        if sha(folder/'recorded.npz') != result['raw_sha256']:
            raise RuntimeError('Changed recorded arrays: '+case['id'])
        if (any(sources.get(k) != v for k, v in result['source_sha256'].items()) or
                result['library_sha256'] != sources['build/noise-sweep/orbit-fourth.so'] or
                result['agama_library_sha256'] != sources[DEPENDENCY] or
                result['forecast_sha256'] != (None if a.smoke else sources['forecast.json'])):
            raise RuntimeError('Changed scientific inputs: '+case['id'])
        if a.smoke:
            expected = dict(n=128, seed=8192, start=0, dt=.01, noise_refine=4,
                            no_bar=True, pilot=True, case='A', no_noise=case['id'].endswith('-smooth'))
            if any(result['settings'][k] != v for k, v in expected.items()):
                raise RuntimeError('Changed short unforced control: '+case['id'])
        local[case['id']] = result['all_pass']
    analysis = None
    comparison = None
    if not a.smoke:
        subprocess.run([sys.executable, str(ROOT/ANALYZER), '--root', str(out/'cases'),
                        '--forecast', str(ROOT/'forecast.json'), '--out', str(out/'analysis')],
                       cwd=ROOT, env=env, check=True, timeout=600)
        analysis = json.loads((out/'analysis/result.json').read_text())
        reference = ROOT/'reference/independent-cadence-analysis.json'
        if reference.exists():
            from verify_confirmation_reference import verify
            comparison = verify(analysis, json.loads(reference.read_text()))
            (out/'reference-comparison.json').write_text(json.dumps(comparison, indent=2)+'\n')
    receipt = dict(smoke_only=a.smoke, cases=len(cases), all_local_checks_pass=all(local.values()),
                   local_checks=local, scientific_cpu_seconds=ledger['completed_cpu_seconds'],
                   source_manifest=source_manifest, analysis_sha256=sha(out/'analysis/result.json') if analysis else None,
                   numerical_qualification=analysis['numerically_qualified'] if analysis else None,
                   reference_comparison=comparison,
                   scope='Same-seed reproduction of the fixed amended sample; no old-sample pooling or physical extension. '
                         'Smoke checks are short and unforced. A null reference comparison is not a passing reproduction. '
                         'A reproduced failed numerical decision remains failed.')
    (out/'reproduction.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))
    if not all(local.values()):
        raise SystemExit('Local checks failed; inspect the retained outputs.')


if __name__ == '__main__':
    main()
