"""Analyze the complete frozen eight-batch population validation, without selection."""
import os
os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['MKL_NUM_THREADS']='1'
from pathlib import Path
import argparse,hashlib,json
import numpy as np
T7_975=2.3646242515927844  # two-sided95% Student-t quantile, seven degrees of freedom
from profiles import load_table
from cumulative import physical_populations
from triangle_kernel import contract_cells


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def interval(values):
    v=np.asarray(values,float)
    if v.shape[0]!=8 or not np.all(np.isfinite(v)):
        raise ValueError('Require all eight finite independent batches')
    mean=v.mean(axis=0);se=v.std(axis=0,ddof=1)/np.sqrt(8)
    half=T7_975*se
    return dict(mean=mean.tolist(),se=se.tolist(),ci95=np.stack([mean-half,mean+half],axis=-1).tolist())


def equivalent(summary,allowance=2e-4):
    lo,hi=summary['ci95']
    return bool(lo>=-allowance and hi<=allowance)


def load_validation(batch):
    ledger=json.loads((batch/'ledger.json').read_text())
    wanted={f's{s}-seed{seed}' for s in ['0','.25'] for seed in range(94501,94509)}
    if not (batch/'TERMINAL').exists() or set(ledger['cases'])!=wanted or any(v['state']!='complete' for v in ledger['cases'].values()):
        raise ValueError('The complete frozen 16-case validation is required; subsets are not analyzed')
    manifest=json.loads((batch/'manifest.json').read_text())
    records={};provenance={};cols=None
    for key in sorted(wanted):
        folder=batch/key;r=json.loads((folder/'result.json').read_text())
        if not (folder/'COMPLETE').exists() or sha(folder/'recorded.npz')!=r['raw_sha256']:
            raise ValueError('Missing/altered recorded data: '+key)
        c=r['config']
        s,seed=key.split('-seed')
        if c['seed']!=int(seed) or c['s']!=float(s[1:]) or c['dt']!=.0125 or r['independent_initial_paths']!=1572864:
            raise ValueError('Frozen sample/configuration mismatch')
        if cols is None:cols=r['columns']
        elif r['columns']!=cols:raise ValueError('Column ordering changed')
        for name,value in r['source_sha256'].items():
            if manifest['spec']['source_sha256']['scripts/population_response/'+name]!=value:
                raise ValueError('Frozen source hash mismatch')
        with np.load(folder/'recorded.npz') as z:
            data={name:z[name].copy() for name in ['mean','covariance','edges','counts','kernel_edges','kernel_primitive_cell_average','kernel_primitive_at_edges','raw_conditional_kernel']}
        if not np.array_equal(data['mean'],r['mean']):raise ValueError('JSON and array means disagree')
        records[key]=(r,data);provenance[str(folder/'result.json')]=sha(folder/'result.json')
    return records,cols,provenance,ledger


def main():
    p=argparse.ArgumentParser();p.add_argument('--batch',type=Path,required=True)
    p.add_argument('--table',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();records,cols,provenance,ledger=load_validation(a.batch)
    meta,table=load_table(a.table);pops=physical_populations(meta,table,spacing=1/8192)
    def idx(t,pop,method='remainder',level='fine',branch='antithetic'):
        return cols.index(dict(tau=t,level=level,branch=branch,method=method,population=pop))
    rows=[];between=[];population_differences=[];kernel_records={};means_by_s={}
    factor=4*meta['action_unit']**2*(2*np.pi)**3*meta['f_ref']
    for s in ['0','.25']:
        items=[records[f's{s}-seed{seed}'] for seed in range(94501,94509)]
        means=np.stack([v[1]['mean'] for v in items]);means_by_s[s]=means
        local=all(v[0]['all_performed_gates_pass'] for v in items)
        edges=items[0][1]['kernel_edges'];Q=np.stack([v[1]['kernel_primitive_cell_average'][:,0,1] for v in items])
        rawK=np.stack([v[1]['raw_conditional_kernel'][:,0,1] for v in items])
        for r,d in items:
            if not np.array_equal(d['kernel_edges'],edges):raise ValueError('Kernel mesh changed')
        kernel_records[s]=dict(cell_edges=edges,primitive_batches=Q,
            primitive_coarse_batches=np.stack([v[1]['kernel_primitive_cell_average'][:,1,1] for v in items]),
            raw_initial_action_edges=items[0][1]['edges'],raw_conditional_batches=rawK)
        for ti,time in enumerate([10.,20.]):
            for pop in pops:
                i=idx(time,pop);fine=means[:,i];step=fine-means[:,idx(time,pop,level='coarse')]
                name=pop.rsplit('-',1)[0]
                window=means[:,idx(time,name+'-64')]-means[:,idx(time,name+'-40')]
                physical=interval(fine);step_stats=interval(step);window_stats=interval(window)
                control=interval(means[:,idx(time,pop,method='raw')]-fine)
                control_ci=control['ci95']
                qualified=local and equivalent(step_stats) and equivalent(window_stats)
                ci=physical['ci95'];sign='positive' if ci[0]>0 else 'negative' if ci[1]<0 else 'unresolved'
                # Numerical allowance is a declared practical scale, not an error bound.
                conservative=[ci[0]-2e-4,ci[1]+2e-4]
                survives=bool(conservative[0]>0 or conservative[1]<0)
                density=pops[pop].evaluate(edges)[0]
                predicted=np.array([contract_cells(edges,q,density) for q in Q[:,ti]])
                delta=predicted-fine
                # Prescribed gradient-space regions. These are not initial orbit cohorts.
                mid=(edges[:-1]+edges[1:])/2;pieces=-Q[:,ti]*np.diff(density)
                regions=[]
                for radius in [4.,8.,16.,24.,40.,64.]:
                    mask=abs(mid)<=radius
                    regions.append(dict(radius=radius,signed_inside=interval(pieces[:,mask].sum(axis=1)),
                        signed_outside=interval(pieces[:,~mask].sum(axis=1))))
                rows.append(dict(s=float(s),tau=time,population=pop,integral_w_K_B=physical,
                    Lz_per_fast_action_area=interval(fine*factor),fine_minus_coarse=step_stats,
                    wider_minus_narrower=window_stats,raw_minus_remainder=control,
                    raw_control_interval_contains_zero=bool(control_ci[0]<=0<=control_ci[1]),
                    local_gates_pass=local,timestep_pass=equivalent(step_stats),window_pass=equivalent(window_stats),
                    numerical_window_qualified=qualified,sampling_sign=sign,
                    sign_survives_one_numerical_allowance=survives,
                    qualified_sign=sign if qualified and survives else 'unqualified',
                    kernel_contraction_maximum_difference=float(abs(delta).max()),
                    gradient_coordinate_regions=regions,
                    primary_endpoint=bool(time==20 and pop in ['halo-40','gaussian-40'])))
            for alternative in ['gaussian','exponential']:
                delta=means[:,idx(time,alternative+'-40')]-means[:,idx(time,'halo-40')]
                population_differences.append(dict(s=float(s),tau=time,contrast=alternative+' minus halo',paired=interval(delta)))
    for time in [10.,20.]:
        for pop in pops:
            i=idx(time,pop)
            between.append(dict(tau=time,population=pop,moving_minus_stationary=interval(means_by_s['.25'][:,i]-means_by_s['0'][:,i])))
    # Retain each independent batch so downstream linear contractions preserve covariance.
    raw={}
    for key,value in kernel_records.items():
        tag='stationary' if key=='0' else 'moving'
        for name,array in value.items():raw[tag+'_'+name]=array
    a.out.mkdir(parents=True,exist_ok=False)
    np.savez_compressed(a.out/'kernel-batches.npz',**raw)
    result=dict(rows=rows,population_differences=population_differences,between_sweep=between,
        pointwise_confidence=.95,independent_batches=8,degrees_of_freedom=7,
        numerical_allowance=2e-4,Lz_per_fast_action_area_factor=factor,
        raw_sha256=sha(a.out/'kernel-batches.npz'),inputs=provenance,
        batch_cpu_seconds=ledger['completed_cpu_seconds'],source_sha256=sha(__file__),
        scope='Complete fixed validation; pilots excluded. Pointwise Student-t intervals, not simultaneous bands. All populations have the same central absolute DF normalization. Differential fixed-fast-action contribution, not total halo torque. Raw/remainder and inter-population comparisons retain pairing. Region contractions weight gradients in the primitive-kernel coordinate; they are not literal initial-orbit cohorts. Kernel predictions on these original six populations are assembly checks, not held-out predictions. A numerical allowance is not a rigorous bound.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for row in rows:
        if row['population'].endswith('-40'):
            print(row['s'],row['tau'],row['population'],row['integral_w_K_B'],row['qualified_sign'])


if __name__=='__main__':main()
