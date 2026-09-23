"""Independently read the released kernel and regenerate every frozen shape forecast."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[key]='1'
from pathlib import Path
import argparse,json
import numpy as np
from profiles import load_table
from heldout_profiles import populations
from triangle_kernel import contract_cells
from analyze_validation import interval,equivalent,sha


def main():
    p=argparse.ArgumentParser()
    for name in ['kernel','analysis','forecast','table','out']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();assessment=json.loads(a.analysis.read_text());forecast=json.loads(a.forecast.read_text())
    if sha(a.kernel)!=assessment['raw_sha256']:raise ValueError('Changed kernel')
    meta,table=load_table(a.table);pops=populations(meta);rows=[]
    with np.load(a.kernel) as archive:
        for s,tag in [(0.,'stationary'),(.25,'moving')]:
            edges=archive[tag+'_cell_edges'];Q=np.stack([archive[tag+'_primitive_batches'],archive[tag+'_primitive_coarse_batches']],axis=2)
            values={};coarsening={}
            for name,pop in pops.items():
                w=pop.evaluate(edges)[0];v=np.empty((8,2,2));low=np.empty_like(v)
                for bi in range(8):
                    for ti in range(2):
                        for li in range(2):
                            q=Q[bi,ti,li];v[bi,ti,li]=contract_cells(edges,q,w)
                            low[bi,ti,li]=contract_cells(edges[::2],q.reshape(-1,2).mean(axis=-1),w[::2])
                values[name]=v;coarsening[name]=v-low
            for name,v in values.items():
                base=name.rsplit('-',1)[0]
                for ti,t in enumerate([10.,20.]):
                    f=next(r for r in forecast['rows'] if r['s']==s and r['tau']==t and r['population']==name)
                    batches=v[:,ti,0];step=interval(batches-v[:,ti,1]);window=interval(values[base+'-64'][:,ti,0]-values[base+'-40'][:,ti,0])
                    assembly=float(abs(coarsening[name][:,ti]).max());prediction=interval(batches)
                    source_ok=all(r['numerical_window_qualified'] for r in assessment['rows'] if r['s']==s and r['tau']==t)
                    qualified=bool(source_ok and equivalent(step) and equivalent(window) and assembly<1e-5)
                    delta=max(float(abs(batches-f['batch_predictions']).max()),abs(assembly-f['maximum_kernel_coarsening_change']),
                        abs(prediction['mean']-f['prediction']['mean']),float(abs(np.array(prediction['ci95'])-f['prediction']['ci95']).max()))
                    rows.append(dict(s=s,tau=t,population=name,prediction=prediction,batch_predictions=batches.tolist(),
                        maximum_difference=delta,qualification_identical=qualified==f['forecast_qualified'],
                        all_pass=bool(delta<1e-11 and qualified==f['forecast_qualified'])))
    if len(rows)!=24:raise ValueError('Incomplete forecast regeneration')
    result=dict(rows=rows,all_pass=all(r['all_pass'] for r in rows),kernel_sha256=sha(a.kernel),forecast_sha256=sha(a.forecast),source_sha256=sha(__file__),
        scope='Arithmetic regeneration from the independently runnable released kernel. No new forced outcomes or physical validation.')
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('x') as f:f.write(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print('Regenerated24forecasts; all pass',result['all_pass'])
    if not result['all_pass']:raise SystemExit(1)

if __name__=='__main__':main()
