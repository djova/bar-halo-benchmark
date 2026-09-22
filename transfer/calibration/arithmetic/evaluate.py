"""Unforced shared-grid DF values; isolate logarithm subtraction roundoff."""
import os
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
import mpmath as mp


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--agama',type=Path,required=True)
    p.add_argument('--reference',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();cpu=time.process_time()
    sys.path.insert(0,str(a.agama.resolve()));import agama
    table=json.loads(a.reference.read_text())
    potential=agama.Potential(type='Isochrone',mass=1,scaleRadius=.5)
    df=agama.DistributionFunction(type='QuasiSpherical',density=potential,potential=potential)
    rows=[]
    with mp.workdps(50):
        for case in table['cases']:
            for group in ['central','scan']:
                for index,old in enumerate(case[group]):
                    for h in [1e-5,2e-5,4e-5,8e-5]:
                        action=np.array([case['actions'][0],case['actions'][1],2*old['Js']])
                        plus=action.copy();minus=action.copy()
                        plus[2]+=2*h;minus[2]-=2*h
                        fp=float(df(plus));fm=float(df(minus));assert fp>0 and fm>0
                        ordinary=float((np.log(fp)-np.log(fm))/(2*h))
                        precise=(mp.log(mp.mpf(fp))-mp.log(mp.mpf(fm)))/(2*mp.mpf(h))
                        rows.append(dict(case=case['label'],group=group,index=index,Js=old['Js'],h=h,
                            plus_action=plus.tolist(),minus_action=minus.tolist(),
                            df_plus=fp,df_minus=fm,df_plus_hex=fp.hex(),df_minus_hex=fm.hex(),
                            ordinary_slope=ordinary,high_precision_same_inputs=float(precise),
                            logarithm_arithmetic_error=float(mp.mpf(ordinary)-precise),
                            archived_slope=old['dlogf_dJs']))
    out=dict(rows=rows,cpu_seconds=time.process_time()-cpu,
             source_sha256=sha(__file__),reference_sha256=sha(a.reference),
             agama_library_sha256=sha(agama.__file__),numpy_version=np.__version__,
             mpmath_version=mp.__version__,precision_decimal_digits=50,
             scope='Unforced DF on shared original actions. High precision applies to logs of returned binary64 DF values, not the DF itself. No changed calibration or forced outcomes.')
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(rows=len(rows),cpu_seconds=out['cpu_seconds'])))


if __name__=='__main__':main()
