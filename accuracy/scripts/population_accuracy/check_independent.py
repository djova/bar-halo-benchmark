"""Control the decision arithmetic and population conventions before new outcomes."""
from common import ROOT, NAMES, density, load_table, populations, sha
from analyze_independent import absolute_test, relative_test
from characteristic_remainder import assembly_control, identities
import argparse
import json
import time
from pathlib import Path
import numpy as np


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    a = p.parse_args()
    cpu = time.process_time()
    checks = dict(inside_absolute=absolute_test(.01,.002,.02)=='supported',
        outside_absolute=absolute_test(.03,.002,.02)=='contradicted',
        overlap_absolute=absolute_test(.019,.002,.02)=='inconclusive',
        zero_reference_unqualified=relative_test(0,0,0,0)=='inconclusive',
        uncertain_denominator_not_false_failure=relative_test(.05,0,1,.1)=='inconclusive',
        resolved_relative_success=relative_test(.01,.001,1,.1)=='supported',
        resolved_relative_failure=relative_test(.1,.001,1,.1)=='contradicted')
    meta,table = load_table(ROOT/'results/population-response/preflight-02')
    x = np.linspace(-96,96,196609)
    values = np.stack([density(x,meta,table,name) for name in NAMES])
    center = np.argmin(abs(x))
    checks['same_central_density'] = bool(np.allclose(values[:,center],1,rtol=0,atol=1e-12))
    slope = (np.log(values[:,center+1])-np.log(values[:,center-1]))/(x[center+1]-x[center-1])
    checks['same_initial_log_slope'] = bool(np.max(abs(slope-meta['g']))<1e-7)
    checks['positive_compact_populations'] = bool(np.all(values>=0) and np.all(values[:,[0,-1]]==0))
    masses = np.trapz(values,x,axis=1)
    checks['physical_mass_not_renormalized'] = bool(masses.max()>2*masses.min())
    # The shared canonical integrator is checked on its previously defined,
    # short known-weight control, not on any new-condition halo outcome.
    control = assembly_control()
    checks['old_canonical_assembly_control'] = abs(control['difference'])<1e-10
    checks['canonical_analytic_identities'] = identities()<1e-10
    result = dict(checks={k:bool(v) for k,v in checks.items()},all_pass=all(checks.values()),
        central_slopes=slope.tolist(),window_masses=masses.tolist(),old_control=control,
        source_sha256={name:sha(Path(__file__).with_name(name)) for name in ['check_independent.py','analyze_independent.py','evolve_independent.py','prepare_matrix.py','common.py']},
        cpu_seconds=time.process_time()-cpu,
        scope='Decision arithmetic, positive-profile normalization, and previously defined canonical assembly controls. No new-condition forced population was evolved.')
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if not result['all_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
