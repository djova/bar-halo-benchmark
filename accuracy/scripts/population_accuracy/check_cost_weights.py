"""Require identical discrete populations in the two timed estimators."""
from benchmark_estimators import numerical_weight, weight, NAMES
from common import ROOT, Population, load_table, sha
from pathlib import Path
import argparse
import json
import time
import numpy as np


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    start=time.process_time()
    meta,table=load_table(ROOT/'results/population-response/preflight-02')
    rng=np.random.default_rng(96204)
    x=np.r_[rng.uniform(-88,88,20000),rng.uniform(-.05,.05,20000)]
    grid=np.linspace(-96,96,192*8192+1)
    rows=[]
    for name in NAMES:
        pop=Population(grid,weight(grid,name,meta,table))
        reference=pop.evaluate(x)[0]
        actual=numerical_weight(x,name,meta,table)
        rows.append(dict(population=name,maximum_difference=float(abs(reference-actual).max()),identical=bool(np.array_equal(reference,actual))))
    result=dict(rows=rows,all_pass=all(r['identical'] for r in rows),
        source_sha256={n:sha(Path(__file__).with_name(n)) for n in ['check_cost_weights.py','benchmark_estimators.py','common.py']},
        cpu_seconds=time.process_time()-start,
        scope='Direct discrete weight equivalence, including dense samples in the narrowest stress population; not new forced trajectories.')
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if not result['all_pass']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
