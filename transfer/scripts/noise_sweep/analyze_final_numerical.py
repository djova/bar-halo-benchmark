"""Read the last predeclared joint numerical matrix; preserve both estimands."""
from pathlib import Path
import argparse,hashlib,json,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from analyze_transfer import estimate

def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    p.add_argument('--recovery-root',type=Path,help='Explicit terminal recovery containing only the four unfinished cases.')
    p.add_argument('--forecast',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    assert ((a.recovery_root or a.root)/'TERMINAL').exists()
    forecast_sha=hashlib.sha256(a.forecast.read_bytes()).hexdigest()
    case=next(c for c in json.loads(a.forecast.read_text())['cases'] if c['label']=='B')
    margin=.1*case['adequacy_half_width'];sources={};pairs={};local=True;identity=True
    sources_common=None;library_common=None
    for label,dt,refinement in [('candidate',.01,4),('halfstep',.005,4),('halfcadence',.01,8)]:
        loaded=[];all_d=[]
        for kind in ['noisy','smooth']:
            case_root=a.recovery_root if a.recovery_root and label!='candidate' else a.root
            folder=case_root/(label+'-'+kind);assert (folder/'COMPLETE').exists()
            d=json.loads((folder/'result.json').read_text());digest=hashlib.sha256((folder/'recorded.npz').read_bytes()).hexdigest()
            assert digest==d['raw_sha256'] and d['forecast_sha256']==forecast_sha
            settings=d['settings'];assert settings['dt']==dt and settings['noise_refine']==refinement
            assert settings['n']==16384 and settings['start']==0 and settings['seed']==8302
            assert settings['no_noise']==(kind=='smooth') and not settings['no_bar']
            assert d['config']==case['orbit_config']
            if sources_common is None:sources_common=d['source_sha256'];library_common=(d['library_sha256'],d['agama_library_sha256'])
            assert sources_common==d['source_sha256'] and library_common==(d['library_sha256'],d['agama_library_sha256'])
            sources[folder.name]=dict(result_sha256=hashlib.sha256((folder/'result.json').read_bytes()).hexdigest(),raw_sha256=digest)
            with np.load(folder/'recorded.npz') as z:
                loaded.append({k:z[k].copy() for k in ['particle_ids','initial_actions_angles','final_bar_Lz','final_reduced_bar_Lz','final_noise_Js']})
            local &= d['all_pass'];all_d.append(d)
        noisy,smooth=loaded
        assert np.array_equal(noisy['initial_actions_angles'],smooth['initial_actions_angles'])
        assert np.array_equal(noisy['particle_ids'],smooth['particle_ids'])
        length=case['orbit_config']['end']/np.ceil(case['orbit_config']['end']/2)/refinement
        actual_dt=length/(2*np.ceil(length/(2*dt)))
        pairs[label]=dict(x=noisy['final_bar_Lz']-smooth['final_bar_Lz'],
                          y=noisy['final_reduced_bar_Lz']-smooth['final_reduced_bar_Lz'],
                          initial=noisy['initial_actions_angles'],ids=noisy['particle_ids'],
                          noise=noisy['final_noise_Js'],actual_microstep=float(actual_dt),
                          noise_cadence=float(length),maximum_work_residual=max(d['maximum_work_residual'] for d in all_d))
    c=pairs['candidate'];refinements=[]
    def measured(values):
        summary=estimate(values);centered=values-values.mean();squares=centered**2;total=float(squares.sum())
        indices=np.argsort(squares)[-20:][::-1]
        summary.update(largest20_ids=c['ids'][indices].tolist(),
                       largest20_variance_fraction=float(squares[indices].sum()/total) if total else 0.,
                       maximum_absolute_individual_change=float(abs(values).max()))
        summary['point_pass']=abs(summary['mean'])<margin
        summary['interval_pass']=max(abs(x) for x in summary['ci95'])<margin
        return summary
    for label in ['halfstep','halfcadence']:
        r=pairs[label]
        assert np.array_equal(r['initial'],c['initial']) and np.array_equal(r['ids'],c['ids'])
        endpoint=float(abs(r['noise']-c['noise']).max());assert endpoint<1e-12
        if label=='halfstep':assert np.array_equal(r['y'],c['y'])
        refinements.append(dict(setting=label,raw_3D_shift=measured(r['x']-c['x']),
                                discrepancy_shift=measured((r['x']-r['y'])-(c['x']-c['y'])),
                                reduced_shift=estimate(r['y']-c['y']),brownian_endpoint_difference=endpoint))
    gates=dict(local=bool(local),paired_identity=identity,
               raw_points=all(r['raw_3D_shift']['point_pass'] for r in refinements),
               raw_intervals=all(r['raw_3D_shift']['interval_pass'] for r in refinements),
               discrepancy_points=all(r['discrepancy_shift']['point_pass'] for r in refinements),
               discrepancy_intervals=all(r['discrepancy_shift']['interval_pass'] for r in refinements))
    result=dict(n=16384,numerical_margin=margin,gates=gates,numerically_qualified=all(gates.values()),
                candidate_raw_3D=estimate(c['x']),candidate_reduced=estimate(c['y']),
                candidate_discrepancy=estimate(c['x']-c['y']),refinements=refinements,
                actual_settings={k:{j:v[j] for j in ['actual_microstep','noise_cadence','maximum_work_residual']} for k,v in pairs.items()},
                source_sha256=sources,scientific_source_sha256=sources_common,forecast_sha256=forecast_sha,
                recovered_cases=bool(a.recovery_root),
                interval_scope='Pointwise Student-t iid particle intervals; finite-sample tail concentration is reported, not trimmed. Not a simultaneous or rigorous truncation-error bound.',
                scope='Last predeclared numerical matrix on an unchanged prefix. Neither qualification nor failure establishes full-population physical adequacy. Original failed attempts and frozen prediction remain unchanged.')
    a.out.mkdir(parents=True,exist_ok=False);(a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if 'source' not in k},indent=2))

if __name__=='__main__':main()
