"""Known arithmetic and publication-input checks, without forced evolution."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1'
from pathlib import Path
import argparse,hashlib,json,time
import numpy as np
from analyze_validation import interval,equivalent,T7_975,load_validation
from heldout_profiles import populations,density,NAMES
from profiles import load_table


def main():
    p=argparse.ArgumentParser();p.add_argument('--table',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False);start=time.process_time()
    v=np.arange(8,dtype=float);r=interval(v)
    exact_mean=3.5;exact_se=np.sqrt(.75)
    stats_error=max(abs(r['mean']-exact_mean),abs(r['se']-exact_se),abs(r['ci95'][1]-exact_mean-T7_975*exact_se))
    # Perfectly shared fluctuations must cancel before calculating uncertainty.
    paired=interval((1+v*3)-(v*3));pair_error=max(abs(paired['mean']-1),abs(paired['se']))
    wrong_size=False
    try:interval(v[:7])
    except ValueError:wrong_size=True
    thresholds=equivalent(dict(ci95=[-2e-4,2e-4])) and not equivalent(dict(ci95=[-1e-5,2.01e-4]))
    meta,table=load_table(a.table);fine=populations(meta);coarse=populations(meta,spacing=1/4096)
    rng=np.random.default_rng(94600);x=rng.uniform(-88,88,32768);B=rng.uniform(-20,20,len(x))
    errors={};positive=True;match={}
    for key,pop in fine.items():
        errors[key]=float(abs(pop.remainder(x,B)-coarse[key].remainder(x,B)).max())
        positive=positive and bool(np.all(pop.w>=0))
    h=1e-3
    for name in NAMES:
        w=density(np.array([-h,0,h]),meta['g'],name)
        slope=(np.log(w[2])-np.log(w[0]))/(2*h)
        curvature=(np.log(w[2])+np.log(w[0])-2*np.log(w[1]))/h**2
        expected=-1/12**2 if name=='gaussian12' else -1/20**2 if name=='gaussian20' else 0.
        match[name]=dict(central_density_error=float(abs(w[1]-1)),log_slope_error=float(abs(slope-meta['g'])),log_curvature_error=float(abs(curvature-expected)))
    gates=dict(student_arithmetic=stats_error<1e-14,paired_covariance=pair_error<1e-14,
        reject_subset=wrong_size,whole_interval_threshold=thresholds,positive_density=positive,
        primitive_mesh=max(errors.values())<1e-8,
        initial_local_values=all(max(v.values())<1e-8 for v in match.values()))
    gates={key:bool(value) for key,value in gates.items()}
    result=dict(gates=gates,all_pass=all(gates.values()),student_error=stats_error,paired_error=pair_error,
        primitive_remainder_changes=errors,local_matching=match,cpu_seconds=time.process_time()-start,
        source_sha256={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in ['check_analysis.py','analyze_validation.py','heldout_profiles.py','cumulative.py','profiles.py']},
        scope='Analytical statistical arithmetic and unforced positive-density controls only; no held-out forced outcome generated.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    if not result['all_pass']:raise SystemExit(1)


if __name__=='__main__':main()
