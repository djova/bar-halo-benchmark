"""Immutable finite cases with a measured aggregate CPU and UTC stop guard."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cpu_seconds(pid):
    try:
        fields = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()
        return (int(fields[11]) + int(fields[12])) / os.sysconf('SC_CLK_TCK')
    except FileNotFoundError:
        return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--spec', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    spec = json.loads(args.spec.read_text())
    assert 1 <= spec['workers'] <= 4
    assert 0 < spec['cpu_ceiling_seconds'] <= 48*3600
    stop = dt.datetime.fromisoformat(spec['stop_utc'].replace('Z', '+00:00'))
    assert stop.tzinfo is not None
    sources = spec['source_sha256']
    for path, expected in sources.items():
        assert sha(ROOT/path) == expected, path
    assert len({c['id'] for c in spec['cases']}) == len(spec['cases'])
    for c in spec['cases']:
        assert Path(c['id']).name == c['id'] and c['id'] not in ('.', '..')
        assert (ROOT/c['script']).resolve().is_relative_to(ROOT/'scripts')
        assert c['script'] in sources
        assert '--out' not in c['arguments'] and 0 < c['wall_seconds'] <= 7200
    args.out.mkdir(parents=True, exist_ok=False)
    manifest = dict(spec=spec, spec_sha256=sha(args.spec),
                    protocol_sha256=sha(ROOT/spec['protocol']),
                    supervisor_sha256=sha(__file__),
                    created_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    (args.out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    states = {c['id']: dict(state='pending') for c in spec['cases']}
    pending = list(spec['cases'])
    active = {}
    completed_cpu = 0.
    stopped = None

    def save():
        record = dict(cases=states, completed_cpu_seconds=completed_cpu,
                      active_cpu_seconds=sum(v['cpu'] for v in active.values()),
                      stop_reason=stopped,
                      checked_utc=dt.datetime.now(dt.timezone.utc).isoformat())
        (args.out/'ledger.tmp').write_text(json.dumps(record, indent=2)+'\n')
        (args.out/'ledger.tmp').replace(args.out/'ledger.json')

    while pending or active:
        for key, v in list(active.items()):
            measured = cpu_seconds(v['proc'].pid)
            if measured is not None:
                v['cpu'] = max(v['cpu'], measured)
            # wait4 supplies the final CPU even for stopped or failed children.
            pid, status, usage = os.wait4(v['proc'].pid, os.WNOHANG)
            if pid:
                code = os.waitstatus_to_exitcode(status)
                v['proc'].returncode = code
                actual = usage.ru_utime + usage.ru_stime
                completed_cpu += actual
                v['log'].close()
                states[key] = dict(state='complete' if code == 0 and
                    (args.out/key/'COMPLETE').exists() else 'failed_or_stopped',
                    exit_code=code, cpu_seconds=actual,
                    wall_seconds=time.monotonic()-v['start'])
                del active[key]
                print(key, states[key], flush=True)
        total = completed_cpu + sum(v['cpu'] for v in active.values())
        # Reserve one polling interval plus termination overhead below the cap.
        if not stopped and total >= spec['cpu_ceiling_seconds']-15:
            stopped = 'aggregate CPU limit'
        if not stopped and dt.datetime.now(dt.timezone.utc) >= stop:
            stopped = 'production UTC stop'
        for v in active.values():
            expired = time.monotonic()-v['start'] >= v['case']['wall_seconds']
            if (stopped or expired) and not v.get('terminated'):
                v['proc'].terminate()
                v['terminated'] = time.monotonic()
            elif v.get('terminated') and time.monotonic()-v['terminated'] >= 3:
                v['proc'].kill()
        if stopped:
            for c in pending:
                states[c['id']] = dict(state='not_started', reason=stopped)
            pending.clear()
        while pending and len(active) < spec['workers']:
            c = pending.pop(0)
            for path, expected in sources.items():
                if sha(ROOT/path) != expected:
                    raise RuntimeError('Frozen source changed: '+path)
            env = os.environ.copy()
            env.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
                       MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
            cmd = ['nice', '-n', '10', sys.executable,
                   str(ROOT/c['script']), '--out', str(args.out.resolve()/c['id']),
                   *c['arguments']]
            log = (args.out/(c['id']+'.log')).open('x')
            proc = subprocess.Popen(cmd, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                                    stdout=log, stderr=subprocess.STDOUT)
            process = dict(pid=proc.pid, command=cmd,
                           started_utc=dt.datetime.now(dt.timezone.utc).isoformat())
            (args.out/(c['id']+'-process.json')).write_text(json.dumps(process, indent=2)+'\n')
            states[c['id']] = dict(state='running', pid=proc.pid)
            active[c['id']] = dict(proc=proc, log=log, start=time.monotonic(),
                                   cpu=0., case=c)
        save()
        if active:
            time.sleep(1)
    (args.out/'TERMINAL').write_text('All cases terminal; inspect completion and scientific gates.\n')
    return 0 if all(v['state'] == 'complete' for v in states.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
