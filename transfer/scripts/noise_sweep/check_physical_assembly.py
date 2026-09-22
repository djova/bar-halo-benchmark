"""Known-estimator and corrupted-input controls; fixtures are never scientific data."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import numpy as np
from analyze_physical_transfer import PairReader,RECORDED_SOURCES,LOCAL_GATES,summarize,validate_coverage


def refused(action):
    try:
        action()
    except ValueError:
        return
    raise AssertionError('Malformed assembly was accepted')


def main():
    case=dict(adequacy_half_width=2.,physical_Lz_contrast=-10.,numerical_envelope_Lz=.1,orbit_config={'fixture':True})
    numerical=dict(numerically_qualified=True,refinements=[{'discrepancy_shift':{'mean':0.,'ci95':[-.1,.1]}}]*2)
    y=np.arange(8.)
    for delta,text in [(0.,'Qualified within'),(3.,'Resolved failure'),(-3.,'Resolved failure'),(2.,'Unresolved model adequacy')]:
        result=summarize(y+delta,y,case,numerical)
        assert result['decision'].startswith(text)
        assert result['discrepancy']['mean']==delta and result['discrepancy']['se']==0
        assert np.isclose(result['conservative_numerical_envelope'],.3)
    bad=copy.deepcopy(numerical);bad['numerically_qualified']=False
    assert summarize(y,y,case,bad)['decision'].startswith('Numerical qualification')
    refused(lambda:summarize([0,np.nan],[0,1],case,numerical))
    assert np.array_equal(validate_coverage([{'ids':np.arange(3)},{'ids':np.arange(3,8)}],8),np.arange(8))
    for arrays in [[np.arange(4),np.arange(3,8)],[np.arange(3),np.arange(4,8)],[np.arange(3,8),np.arange(3)]]:
        refused(lambda:validate_coverage([{'ids':x} for x in arrays],8))
    frozen={x:'fixture-source' for x in RECORDED_SOURCES}
    frozen.update({'build/noise-sweep/orbit-fourth.so':'fixture-kernel','build/noise-sweep/Agama-stable-v2/agama.so':'fixture-dependency'})
    with tempfile.TemporaryDirectory(prefix='galaxy-assembly-controls-') as temp:
        root=Path(temp)
        arrays=dict(particle_ids=np.arange(8),initial_actions_angles=np.zeros((8,6)),initial_cartesian=np.zeros((8,6)),
                    final_bar_Lz=y,final_reduced_bar_Lz=y,final_noise_Js=np.zeros(8))
        template=dict(config=case['orbit_config'],forecast_sha256='fixture-forecast',source_sha256={k:frozen[k] for k in RECORDED_SOURCES},
            library_sha256='fixture-kernel',agama_library_sha256='fixture-dependency',gates={k:True for k in LOCAL_GATES},
            all_pass=True,cpu_seconds=0.,maximum_work_residual=0.)
        def write(kind,changes=None,data=None):
            folder=root/('pair-'+kind);folder.mkdir(exist_ok=True)
            np.savez(folder/'recorded.npz',**(arrays if data is None else data))
            result=copy.deepcopy(template)
            result['settings']=dict(seed=8302,n=8,start=0,dt=.01,noise_refine=4,no_noise=kind=='smooth',no_bar=False,pilot=False,case='B')
            if changes:result['settings'].update(changes)
            result['raw_sha256']=hashlib.sha256((folder/'recorded.npz').read_bytes()).hexdigest()
            (folder/'result.json').write_text(json.dumps(result));(folder/'COMPLETE').write_text('Disposable fixture, not a simulation.\n')
        def reader():return PairReader(case,'fixture-forecast',frozen)
        write('noisy');write('smooth')
        assert len(reader().pair(root,'pair',0,8,'fixture')['ids'])==8
        write('smooth',{'dt':.02});refused(lambda:reader().pair(root,'pair',0,8,'fixture'))
        write('smooth');corrupt=copy.deepcopy(arrays);corrupt['initial_actions_angles'][0,0]=1.
        write('noisy',data=corrupt);refused(lambda:reader().pair(root,'pair',0,8,'fixture'))
        corrupt=copy.deepcopy(arrays);corrupt['final_bar_Lz'][0]=np.nan
        write('noisy',data=corrupt);refused(lambda:reader().pair(root,'pair',0,8,'fixture'))
    print(json.dumps(dict(known_decisions=True,numerical_failure_preserved=True,
        duplicate_gap_and_order_refused=True,mixed_operator_refused=True,
        mismatched_initial_states_refused=True,nonfinite_refused=True,
        scope='Disposable known-value and corrupted-input controls. Does not verify an unrun full physical population.'),indent=2))


if __name__=='__main__':main()
