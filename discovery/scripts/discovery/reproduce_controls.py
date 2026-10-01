"""Regenerate three known-limit controls; not the five discovery experiments.

Portable package layout: ROOT/scripts/discovery, ROOT/research/discovery-20261001.
Runs offline after dependencies are installed. No archived trajectories are inputs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    args.out = args.out.resolve()
    os.nice(max(0, 10-os.getpriority(os.PRIO_PROCESS, 0)))
    env = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    jobs = []
    specs = [('inertia', 'inertia_screen.py', []),
             ('elastic_operator', 'scatter_moment_screen.py', ['--operator']),
             ('known_echo', 'echo_reduced.py', [])]
    for name, source, extra in specs:
        script = ROOT/'scripts/discovery'/source
        output = args.out/name
        start = time.monotonic()
        prior = resource.getrusage(resource.RUSAGE_CHILDREN)
        with (args.out/(name+'.log')).open('w') as stream:
            result = subprocess.run([sys.executable, str(script), '--out', str(output), *extra],
                                    cwd=ROOT, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=180)
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        row = dict(id=name, source=source, source_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                   exit_code=result.returncode, wall_seconds=time.monotonic()-start,
                   cpu_seconds=usage.ru_utime+usage.ru_stime-prior.ru_utime-prior.ru_stime)
        jobs.append(row)
        (args.out/'jobs.json').write_text(json.dumps(jobs, indent=2)+'\n')
        if result.returncode:
            raise RuntimeError(f'{name} failed; inspect retained output/log')
    inertia = json.loads((args.out/'inertia/result.json').read_text())
    operator = json.loads((args.out/'elastic_operator/result.json').read_text())
    echo = json.loads((args.out/'known_echo/result.json').read_text())
    gates = dict(harmonic_reference=bool(inertia['all_benchmark_gates_pass']),
                 conservative_operator=bool(operator['all_pass']),
                 fourth_angular_ratio=abs(operator['l4_decay_ratio']-53/32)<1e-14,
                 constant_shear_echo=bool(echo['all_pass']))
    receipt = dict(gates=gates, all_known_limit_controls_pass=all(gates.values()), jobs=jobs,
                   summed_child_cpu_seconds=sum(row['cpu_seconds'] for row in jobs),
                   scope='Regenerates known-limit controls from equations and seeds. Does not reproduce halo echoes, collision-law response ensembles, heating, twins, live galaxies or observations.',
                   uncertainty='Deterministic reference checks and fixed-seed operator checks; no new independent physical evidence.')
    (args.out/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))
    if not all(gates.values()):
        raise RuntimeError('A known-limit control failed; original criteria retained')


if __name__ == '__main__':
    main()
