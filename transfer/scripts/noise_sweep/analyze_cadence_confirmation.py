"""One fixed independent confirmation, without pooling earlier numerical samples."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_transfer import estimate


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--forecast',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    assert (args.root/'TERMINAL').exists()
    ledger=json.loads((args.root/'ledger.json').read_text())
    assert all(v['state']=='complete' for v in ledger['cases'].values())
    manifest=json.loads((args.root/'manifest.json').read_text())
    assert len(manifest['spec']['cases'])==20
    forecast=json.loads(args.forecast.read_text())
    case=next(c for c in forecast['cases'] if c['label']=='B')
    margin=.1*case['adequacy_half_width']
    assert margin==1.8126730139721574e-7
    source_records={}; local=[]; libraries=set(); pair_records=[]

    def read(label,kind,start,n,step,refinement,unforced=False):
        folder=args.root/f'{label}-{kind}'
        assert (folder/'COMPLETE').exists()
        result=json.loads((folder/'result.json').read_text())
        assert result['raw_sha256']==sha(folder/'recorded.npz')
        assert result['forecast_sha256']==sha(args.forecast)
        assert result['config']==case['orbit_config']
        expected=dict(seed=8302,start=start,n=n,dt=step,noise_refine=refinement,
                      no_noise=kind=='smooth',no_bar=unforced,pilot=False,case='B')
        assert all(result['settings'][k]==v for k,v in expected.items())
        for path,digest in result['source_sha256'].items():
            assert manifest['spec']['source_sha256'][path]==digest
        libraries.add((result['library_sha256'],result['agama_library_sha256']))
        with np.load(folder/'recorded.npz') as data:
            for key in data.files:
                assert np.isfinite(data[key]).all(), (folder,key)
            arrays={k:data[k].copy() for k in ['particle_ids','initial_actions_angles',
                'final_bar_Lz','final_reduced_bar_Lz','final_noise_Js']}
        assert np.array_equal(arrays['particle_ids'],np.arange(start,start+n))
        for k in ['final_bar_Lz','final_reduced_bar_Lz','final_noise_Js']:
            assert arrays[k].shape==(n,)
        assert arrays['initial_actions_angles'].shape==(n,6)
        local.append(result['all_pass'])
        source_records[folder.name]=dict(result_sha256=sha(folder/'result.json'),
                                         raw_sha256=result['raw_sha256'])
        return arrays,result

    def pair(label,start,n,step,refinement,unforced=False):
        noisy,dn=read(label,'noisy',start,n,step,refinement,unforced)
        smooth,ds=read(label,'smooth',start,n,step,refinement,unforced)
        assert np.array_equal(noisy['initial_actions_angles'],smooth['initial_actions_angles'])
        assert np.count_nonzero(smooth['final_noise_Js'])==0
        x=noisy['final_bar_Lz']-smooth['final_bar_Lz']
        y=noisy['final_reduced_bar_Lz']-smooth['final_reduced_bar_Lz']
        pair_records.append(dict(label=label,start=start,n=n,raw=estimate(x),
            reduced=estimate(y),discrepancy=estimate(x-y),
            maximum_work_residual=max(dn['maximum_work_residual'],ds['maximum_work_residual'])))
        return dict(x=x,y=y,initial=noisy['initial_actions_angles'],
                    ids=noisy['particle_ids'],noise=noisy['final_noise_Js'])

    def measured(values,ids):
        result=estimate(values);square=(values-values.mean())**2
        order=np.argsort(square)[::-1];total=float(square.sum())
        result.update(point_pass=abs(result['mean'])<margin,
                      interval_pass=max(abs(v) for v in result['ci95'])<margin,
                      largest20_ids=ids[order[:20]].tolist(),
                      largest20_variance_fraction=float(square[order[:20]].sum()/total) if total else 0.,
                      maximum_absolute_individual_change=float(np.max(abs(values))))
        return result

    pairs={}
    for setting,refinement in [('candidate',4),('halfcadence',8)]:
        chunks=[pair(f'{setting}-{start}',start,32768,.01,refinement)
                for start in [65536,98304,131072,163840]]
        pairs[setting]={key:np.concatenate([v[key] for v in chunks]) for key in chunks[0]}
    c=pairs['candidate']; h=pairs['halfcadence']
    assert np.array_equal(c['ids'],np.arange(65536,196608))
    assert np.array_equal(c['ids'],h['ids']) and np.array_equal(c['initial'],h['initial'])
    cadence_endpoint=float(np.max(abs(c['noise']-h['noise'])))
    assert cadence_endpoint<1e-12
    step=pair('halfstep',65536,16384,.005,4)
    assert np.array_equal(c['ids'][:16384],step['ids'])
    assert np.array_equal(c['initial'][:16384],step['initial'])
    assert np.array_equal(c['noise'][:16384],step['noise'])
    assert np.array_equal(c['y'][:16384],step['y'])
    unforced=pair('unforced',65536,4096,.01,4,True)
    assert np.array_equal(c['initial'][:4096],unforced['initial'])
    assert np.array_equal(c['noise'][:4096],unforced['noise'])
    assert len(libraries)==1
    library,agama=next(iter(libraries))
    assert library==manifest['spec']['source_sha256']['build/noise-sweep/orbit-fourth.so']
    assert agama==manifest['spec']['source_sha256']['build/noise-sweep/Agama-stable-v2/agama.so']
    refinements=[]
    for label,r,base in [('halfstep',step,{k:v[:16384] for k,v in c.items()}),('halfcadence',h,c)]:
        refinements.append(dict(setting=label,raw_3D_shift=measured(r['x']-base['x'],r['ids']),
            discrepancy_shift=measured((r['x']-r['y'])-(base['x']-base['y']),r['ids']),
            reduced_shift=estimate(r['y']-base['y'])))
    gates=dict(local=all(local),identities=True,
               raw_points=all(r['raw_3D_shift']['point_pass'] for r in refinements),
               raw_intervals=all(r['raw_3D_shift']['interval_pass'] for r in refinements),
               discrepancy_points=all(r['discrepancy_shift']['point_pass'] for r in refinements),
               discrepancy_intervals=all(r['discrepancy_shift']['interval_pass'] for r in refinements))
    result=dict(n=131072,first_id=65536,last_id=196607,numerical_margin=margin,
                gates=gates,numerically_qualified=all(gates.values()),refinements=refinements,
                candidate_raw_3D=estimate(c['x']),candidate_reduced=estimate(c['y']),
                candidate_discrepancy=estimate(c['x']-c['y']),chunks_and_controls=pair_records,
                brownian_endpoint_difference=cadence_endpoint,
                source_sha256=source_records,manifest_sha256=sha(args.root/'manifest.json'),
                forecast_sha256=sha(args.forecast),analysis_sha256=sha(__file__),
                interval_scope='Fixed new sample; pointwise iid Student-t intervals, no old-sample pooling or path trimming. Not rigorous discretization-error bounds.',
                scope='Explicit post-failure protocol amendment. Independent numerical confirmation; not a physical transfer qualification by itself.')
    args.out.mkdir(parents=True,exist_ok=False)
    (args.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(numerically_qualified=result['numerically_qualified'],gates=gates,refinements=refinements),indent=2))


if __name__=='__main__':main()
