"""Assemble the fixed full population only after independent qualification."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent))
from analyze_transfer import estimate

ROOT=Path(__file__).resolve().parents[2]
RECORDED_SOURCES={
    'scripts/noise_sweep/run_orbits_cadence.py','benchmark/brownian_leaves.py',
    'benchmark/orbit_fourth.cpp','benchmark/orbit_fourth.py',
    'benchmark/orbit_kernel.cpp','benchmark/orbit_kernel.py'}
LOCAL_GATES={'reduced_budget','torque_budget','noise_Lz','noise_fast_actions','noise_angles','roundtrip'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition,message):
    if not condition:
        raise ValueError(message)


def validate_coverage(parts,count):
    require(bool(parts),'No particle chunks supplied')
    ids=np.concatenate([part['ids'] for part in parts])
    require(np.issubdtype(ids.dtype,np.integer),'Particle IDs must be integers')
    require(np.array_equal(ids,np.arange(count)),'Particle IDs have a gap, overlap, wrong order or endpoint')
    return ids


def summarize(x,y,case,numerical):
    x=np.asarray(x);y=np.asarray(y)
    require(x.ndim==1 and x.shape==y.shape and len(x)>1,'Invalid paired population shape')
    require(np.isfinite(x).all() and np.isfinite(y).all(),'Nonfinite physical population')
    raw,reduced,discrepancy=estimate(x),estimate(y),estimate(x-y)
    band=case['adequacy_half_width']
    shifts=[row['discrepancy_shift'] for row in numerical['refinements']]
    require(len(shifts)==2,'Both numerical interventions are required')
    require(all(np.isfinite([r['mean'],*r['ci95']]).all() and len(r['ci95'])==2 and
                r['ci95'][0]<=r['mean']<=r['ci95'][1] for r in shifts),'Invalid numerical intervals')
    envelope=case['numerical_envelope_Lz']+sum(max(abs(v) for v in r['ci95']) for r in shifts)
    interval=[discrepancy['ci95'][0]-envelope,discrepancy['ci95'][1]+envelope]
    if not numerical['numerically_qualified']:
        decision='Numerical qualification unresolved or failed.'
    elif interval[0]>=-band and interval[1]<=band:
        decision='Qualified within the frozen operational approximation band.'
    elif interval[1]<-band or interval[0]>band:
        decision='Resolved failure of the frozen constant-coefficient prediction.'
    else:
        decision='Unresolved model adequacy: enlarged interval overlaps a band boundary.'
    cov=np.cov(x,y,ddof=1)
    denom=float(np.sqrt(cov[0,0]*cov[1,1]))
    return dict(n=len(x),raw_3D=raw,paired_reduced=reduced,discrepancy=discrepancy,
                covariance_xy=float(cov[0,1]),correlation_xy=float(cov[0,1]/denom) if denom else None,
                forecast_Lz=case['physical_Lz_contrast'],adequacy_half_width=band,
                variance_reduced_3D_estimate=case['physical_Lz_contrast']+discrepancy['mean'],
                conservative_numerical_envelope=envelope,enlarged_discrepancy_interval=interval,
                precision_target_met=discrepancy['half_width']<=.1*abs(case['physical_Lz_contrast']),
                decision=decision)


class PairReader:
    def __init__(self,case,forecast_hash,frozen_sources):
        self.case=case;self.forecast_hash=forecast_hash;self.frozen=frozen_sources
        self.records={};self.local=[]

    def read(self,folder,start,n,kind):
        require((folder/'COMPLETE').exists(),f'Missing complete case: {folder.name}')
        path=folder/'result.json';result=json.loads(path.read_text())
        require(sha(folder/'recorded.npz')==result['raw_sha256'],'Raw array checksum mismatch')
        require(result['forecast_sha256']==self.forecast_hash,'Changed forecast')
        require(result['config']==self.case['orbit_config'],'Changed physical configuration')
        expected=dict(seed=8302,n=n,start=start,dt=.01,noise_refine=4,
                      no_noise=kind=='smooth',no_bar=False,pilot=False,case='B')
        require(all(result['settings'].get(k)==v for k,v in expected.items()),'Mixed numerical operator or sample')
        require(set(result['source_sha256'])==RECORDED_SOURCES and all(self.frozen.get(k)==v for k,v in result['source_sha256'].items()),'Changed or incomplete scientific source record')
        require(result['library_sha256']==self.frozen['build/noise-sweep/orbit-fourth.so'],'Changed force kernel')
        require(result['agama_library_sha256']==self.frozen['build/noise-sweep/Agama-stable-v2/agama.so'],'Changed simulation dependency')
        require(set(result['gates'])==LOCAL_GATES and result['all_pass']==all(result['gates'].values()),'Inconsistent local gate record')
        with np.load(folder/'recorded.npz') as data:
            for key in data.files:
                require(np.isfinite(data[key]).all(),'Nonfinite recorded array: '+key)
            arrays={k:data[k].copy() for k in ['particle_ids','initial_actions_angles','initial_cartesian',
                    'final_bar_Lz','final_reduced_bar_Lz','final_noise_Js']}
        require(np.array_equal(arrays['particle_ids'],np.arange(start,start+n)),'Wrong case particle IDs')
        require(arrays['initial_actions_angles'].shape==(n,6) and arrays['initial_cartesian'].shape==(n,6),'Invalid initial state shape')
        for key in ['final_bar_Lz','final_reduced_bar_Lz','final_noise_Js']:
            require(arrays[key].shape==(n,),'Invalid final vector shape')
        if kind=='smooth':
            require(np.count_nonzero(arrays['final_noise_Js'])==0,'Noise in collisionless control')
        self.local.append(result['all_pass'])
        return arrays,dict(result_sha256=sha(path),raw_sha256=result['raw_sha256'],n=n,start=start,
                           cpu_seconds=result['cpu_seconds'],maximum_work_residual=result['maximum_work_residual'])

    def pair(self,root,label,start,n,source_label):
        noisy,dn=self.read(root/(label+'-noisy'),start,n,'noisy')
        smooth,ds=self.read(root/(label+'-smooth'),start,n,'smooth')
        for key in ['particle_ids','initial_actions_angles','initial_cartesian']:
            require(np.array_equal(noisy[key],smooth[key]),'Paired initial identity failure: '+key)
        self.records[source_label]={'noisy':dn,'smooth':ds}
        return dict(ids=noisy['particle_ids'],initial=noisy['initial_actions_angles'],
                    x=noisy['final_bar_Lz']-smooth['final_bar_Lz'],
                    y=noisy['final_reduced_bar_Lz']-smooth['final_reduced_bar_Lz'])


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--prefix-root',type=Path,required=True)
    p.add_argument('--confirmation-root',type=Path,required=True)
    p.add_argument('--confirmation-analysis',type=Path,required=True)
    p.add_argument('--physical-root',type=Path,required=True)
    p.add_argument('--forecast',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    for root in [a.confirmation_root,a.physical_root]:
        require((root/'TERMINAL').exists(),'Nonterminal matrix: '+root.name)
        ledger=json.loads((root/'ledger.json').read_text())
        require(all(c['state']=='complete' for c in ledger['cases'].values()),'Incomplete or stopped matrix')
    manifest_path=a.confirmation_root/'manifest.json'
    manifest=json.loads(manifest_path.read_text());frozen=manifest['spec']['source_sha256']
    physical_manifest=json.loads((a.physical_root/'manifest.json').read_text())
    require(all(physical_manifest['spec']['source_sha256'].get(k)==v for k,v in frozen.items()),'Physical queue differs from frozen confirmation inputs')
    numerical=json.loads(a.confirmation_analysis.read_text())
    require(numerical['manifest_sha256']==sha(manifest_path),'Wrong numerical manifest')
    require(numerical['analysis_sha256']==frozen['scripts/noise_sweep/analyze_cadence_confirmation.py'],'Changed numerical readback source')
    require(numerical['n']==131072 and numerical['first_id']==65536 and numerical['last_id']==196607,'Wrong numerical sample')
    require(numerical['numerically_qualified'] and all(numerical['gates'].values()),'Independent numerical qualification failed')
    for name,record in numerical['source_sha256'].items():
        folder=a.confirmation_root/name
        require(sha(folder/'result.json')==record['result_sha256'] and sha(folder/'recorded.npz')==record['raw_sha256'],'Stale numerical readback')
    forecast_hash=sha(a.forecast)
    require(numerical['forecast_sha256']==forecast_hash,'Numerical forecast mismatch')
    forecast=json.loads(a.forecast.read_text());case=next(c for c in forecast['cases'] if c['label']=='B')
    require(case['qualified'] and forecast['frozen_before_3d'],'Unqualified original forecast')
    require(numerical['numerical_margin']==.1*case['adequacy_half_width'],'Changed numerical margin')
    require({r['setting'] for r in numerical['refinements']}=={'halfstep','halfcadence'},'Missing numerical comparison')
    for row in numerical['refinements']:
        for key in ['raw_3D_shift','discrepancy_shift']:
            measured=row[key]
            require(abs(measured['mean'])<numerical['numerical_margin'] and
                    max(abs(v) for v in measured['ci95'])<numerical['numerical_margin'],'Unqualified numerical interval')
    reader=PairReader(case,forecast_hash,frozen)
    parts=[reader.pair(a.prefix_root,'candidate',0,16384,'original candidate prefix'),
           reader.pair(a.physical_root,'candidate-16384',16384,49152,'physical16384')]
    for start in [65536,98304,131072,163840]:
        parts.append(reader.pair(a.confirmation_root,f'candidate-{start}',start,32768,f'confirmation{start}'))
    for start in [196608,262144,327680,393216,458752]:
        parts.append(reader.pair(a.physical_root,f'candidate-{start}',start,65536,f'physical{start}'))
    ids=validate_coverage(parts,524288)
    require(all(reader.local),'A physical sample fails a local budget or identity gate')
    initial=np.concatenate([r['initial'] for r in parts]);cfg=case['orbit_config']
    js=np.random.default_rng(np.random.SeedSequence([8302,0])).normal(cfg['mean'],cfg['width'],524288)
    phases=np.random.default_rng(np.random.SeedSequence([8302,1])).uniform(0,2*np.pi,(524288,3))
    expected=np.column_stack((np.full(524288,cfg['jr']),np.full(524288,cfg['jz']),2*js,phases))
    require(np.array_equal(initial,expected),'Full population differs from fixed seeded initial states')
    x=np.concatenate([r['x'] for r in parts]);y=np.concatenate([r['y'] for r in parts])
    disjoint=(ids<65536)|(ids>=196608);require(int(disjoint.sum())==393216,'Wrong disjoint diagnostic coverage')
    result=dict(primary=summarize(x,y,case,numerical),disjoint_diagnostic=summarize(x[disjoint],y[disjoint],case,numerical),
        qualification_conditional_on_numerical_screen=True,all_identity_and_local_checks_pass=True,
        candidate_settings=dict(dtmax=.01,noise_refine=4,seed=8302),
        source_sha256=reader.records,forecast_sha256=forecast_hash,
        confirmation_analysis_sha256=sha(a.confirmation_analysis),analysis_sha256=sha(__file__),
        physical_manifest_sha256=sha(a.physical_root/'manifest.json'),
        interval_scope='Pointwise iid Student-t sampling intervals with separately added numerical intervals, not a simultaneous guarantee. Primary includes confirmation IDs; fixed disjoint diagnostic excludes them.',
        inference='Finite selected tracers in a prescribed bar with imposed white canonical action noise. No live-halo, physical SIDM or observational population inference.')
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ['primary','disjoint_diagnostic']},indent=2))


if __name__=='__main__':main()
