"""Freeze all independent cases, only after the prospective forecasts are committed."""
from common import ROOT, sha
from pathlib import Path
import argparse
import json
import subprocess


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--forecast',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a = p.parse_args()
    forecast = a.forecast.resolve()
    relative = str(forecast.relative_to(ROOT))
    record = json.loads(forecast.read_text())
    if record['developmental'] or not (forecast.parent/'FROZEN_PREDICTIONS').exists():
        raise ValueError('Prospective frozen forecast required')
    if subprocess.check_output(['git','show','HEAD:'+relative],cwd=ROOT) != forecast.read_bytes():
        raise ValueError('All numerical forecasts must be committed first')
    inputs = ['scripts/population_accuracy/evolve_independent.py','scripts/population_accuracy/common.py',
              'scripts/population_accuracy/diagnostic.py','scripts/population_accuracy/analyze_independent.py',
              'scripts/population_response/forward.py','scripts/population_response/characteristic_remainder.py',
              'scripts/population_response/cumulative.py','scripts/population_response/profiles.py',
              'scripts/population_response/check_cumulative_identity.py','benchmark/characteristics.py',
              'scripts/noise_sweep/guarded_queue.py','research/population-accuracy/INDEPENDENT_MATRIX_01.md',
              'research/population-accuracy/PLAN.md','results/population-response/preflight-02/halo-table.npz',
              'results/population-response/preflight-02/result.json',relative,
              str((forecast.parent/'kernel-batches.npz').relative_to(ROOT)),
              str((forecast.parent/'FROZEN_PREDICTIONS').relative_to(ROOT))]
    common = ['--forecast',relative,'--table','results/population-response/preflight-02']
    cases = []
    configs = [('base',96,3072,128,.025,False,False),('fine',96,6144,256,.025,False,False),
               ('halfstep',96,3072,128,.0125,False,False),('domain',128,4096,128,.025,False,False),
               ('wide',128,4096,128,.025,True,False),('wide-fine',128,8192,256,.025,True,False),
               ('wide-halfstep',128,4096,128,.0125,True,False),('wide-domain',160,5120,128,.025,True,False),
               ('unforced-wide',128,4096,128,.025,True,True)]
    for name,J,nj,nphi,dt,wide,unforced in configs:
        args = common+['--method','distribution','--J',str(J),'--nj',str(nj),'--nphi',str(nphi),'--dt',str(dt)]
        if wide:
            args += ['--wide']
        if unforced:
            args += ['--no-bar']
        cases.append(dict(id='noisy-'+name,script=inputs[0],arguments=args,wall_seconds=3600 if 'fine' in name else 1800))
    for name,J,nj,nphi,dt in [('base',160,10240,256,.025),('fine',160,20480,512,.025),
                             ('finer',160,40960,1024,.025),('halfstep',160,10240,256,.0125),('domain',192,12288,256,.025)]:
        args = common+['--method','characteristic','--J',str(J),'--nj',str(nj),'--nphi',str(nphi),'--dt',str(dt),'--chunk','8']
        cases.append(dict(id='smooth-'+name,script=inputs[0],arguments=args,wall_seconds=3600 if 'fine' in name else 1800))
    assert len(cases) == 14
    spec = dict(protocol='research/population-accuracy/INDEPENDENT_MATRIX_01.md',workers=2,
        cpu_ceiling_seconds=21600,stop_utc='2026-09-24T03:35:36Z',
        source_sha256={n:sha(ROOT/n) for n in inputs},
        forecast_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),cases=cases)
    with a.out.open('x') as f:
        f.write(json.dumps(spec,indent=2)+'\n')
    print('Frozen all14independent cases; no new evolution launched')


if __name__ == '__main__':
    main()
