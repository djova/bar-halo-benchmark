"""Two all-forward elastic laws with matched conditional drift/raw covariance.

The legacy conservative DSMC engine remains unmodified. Every output records
both the engine hash and this operator wrapper's hash.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from scipy.special import eval_legendre
import scatter_screen as engine

ROOT=Path(__file__).resolve().parents[2]
PROTOCOL=ROOT/'research/discovery-20261001/SCATTER_MOMENT_PROTOCOL.md'
LAW=None


def weight(law):
    return 2/3 if law=='A' else 8/9


def elastic(v1,v2,rng,delta):
    center=(v1+v2)/2
    relative=v1-v2
    speed=np.linalg.norm(relative,axis=1)
    unit=relative/np.maximum(speed[:,None],1e-300)
    cosine=np.where(rng.random(len(speed))<.25,0.,2/3) if LAW=='A' else np.full(len(speed),1/3)
    random=rng.normal(size=relative.shape)
    tangent=random-np.sum(random*unit,axis=1)[:,None]*unit
    tangent/=np.linalg.norm(tangent,axis=1)[:,None]
    direction=cosine[:,None]*unit+np.sqrt(1-cosine*cosine)[:,None]*tangent
    offset=speed[:,None]*direction/2
    return center+offset,center-offset


def hashes():
    return dict(wrapper_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        moment_protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest())


def operator(out):
    global LAW
    out.mkdir(parents=True,exist_ok=False)
    start,cpu=time.monotonic(),time.process_time()
    begin=datetime.now(timezone.utc).isoformat()
    rng=np.random.default_rng(260510)
    n=262144
    u=np.array([1.,2.,-.5]);g2=float(u@u)
    center=rng.normal(size=(n,3))
    v1,v2=center+u/2,center-u/2
    rows=[]
    for law,m1,m2,ep4 in [('A',.5,1/3,-49/216),('B',1/3,1/9,1/81)]:
        LAW=law
        a,b=elastic(v1,v2,rng,0.)
        kick=a-v1
        cosine=np.sum((a-b)*u,axis=1)/g2
        rate_ratio=(2/3)/weight(law)
        drift=rate_ratio*(m1-1)*u/2
        raw=rate_ratio*(g2*(1-m2)*np.eye(3)+(3*m2+1-4*m1)*np.outer(u,u))/8
        empirical_drift=rate_ratio*kick.mean(axis=0)
        empirical_raw=rate_ratio*np.einsum('ni,nj->ij',kick,kick)/n
        drift_se=rate_ratio*kick.std(axis=0,ddof=1)/np.sqrt(n)
        products=kick[:,:,None]*kick[:,None,:]
        raw_se=rate_ratio*products.std(axis=0,ddof=1)/np.sqrt(n)
        p4=eval_legendre(4,cosine)
        sinsq=1-cosine*cosine
        gates=dict(conservation_energy=float(np.max(abs(np.sum(a*a+b*b-v1*v1-v2*v2,axis=1))))<1e-12,
            conservation_momentum=float(np.max(abs(a+b-v1-v2)))<1e-12,
            sampled_drift=bool(np.all(abs(empirical_drift-drift)<5*drift_se+1e-12)),
            sampled_raw_second=bool(np.all(abs(empirical_raw-raw)<5*raw_se+1e-12)),
            sampled_viscosity=bool(abs(sinsq.mean()-weight(law))<5*sinsq.std(ddof=1)/np.sqrt(n)+1e-12),
            sampled_l4=bool(abs(p4.mean()-ep4)<5*p4.std(ddof=1)/np.sqrt(n)+1e-12),
            exact_drift_match=bool(np.max(abs(drift+u/4))<1e-12),
            exact_raw_second_match=bool(np.max(abs(raw-g2*np.eye(3)/12))<1e-12))
        rows.append(dict(law=law,m1=m1,m2=m2,rate_ratio=rate_ratio,angular_weight=weight(law),
            expected_drift=drift.tolist(),empirical_drift=empirical_drift.tolist(),drift_se=drift_se.tolist(),
            expected_raw_second=raw.tolist(),empirical_raw_second=empirical_raw.tolist(),raw_second_se=raw_se.tolist(),
            expected_p4=ep4,empirical_p4=float(p4.mean()),l4_decay_over_GammaA=rate_ratio*(1-ep4),
            pair_energy_max=float(np.max(abs(np.sum(a*a+b*b-v1*v1-v2*v2,axis=1)))),
            pair_momentum_max=float(np.max(abs(a+b-v1-v2))),gates=gates))
    result=dict(config=dict(role='operator',seed=260510,n=n,relative_velocity=u.tolist()),rows=rows,
        all_pass=all(all(r['gates'].values()) for r in rows),l4_decay_ratio=rows[0]['l4_decay_over_GammaA']/rows[1]['l4_decay_over_GammaA'],
        pid=os.getpid(),state='complete',started_utc=begin,ended_utc=datetime.now(timezone.utc).isoformat(),
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-start,
        source_sha256=hashlib.sha256(Path(engine.__file__).read_bytes()).hexdigest(),**hashes())
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(all_pass=result['all_pass'],cpu_seconds=result['cpu_seconds'],l4_decay_ratio=result['l4_decay_ratio'])))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    p.add_argument('--operator',action='store_true')
    p.add_argument('--law',choices=('A','B'),default='A')
    p.add_argument('--role',choices=('equilibrium','stress','resonance'),default='resonance')
    p.add_argument('--seed',type=int,default=260511)
    p.add_argument('--n',type=int,default=8192)
    p.add_argument('--cells',type=int,default=32)
    p.add_argument('--dt',type=float,default=.01)
    p.add_argument('--duration',type=float,default=40.)
    p.add_argument('--kappa',type=float,default=.02)
    p.add_argument('--delta',type=float,default=0.)
    p.add_argument('--epsilon',type=float,default=.25)
    p.add_argument('--omega0',type=float,default=.5)
    p.add_argument('--sweep',type=float,default=.025)
    a=p.parse_args()
    if a.operator:
        operator(Path(a.out))
    else:
        LAW=a.law
        engine.elastic=elastic
        engine.angular_weight=lambda delta:weight(LAW)
        engine.run(a)
        path=Path(a.out)/'result.json';r=json.loads(path.read_text())
        r.update(**hashes(),law=LAW,scope='All-forward equal-mass elastic laws match conditional velocity drift, raw second tensor and viscosity at each relative speed; linear vx action only. Higher energy-jump moments and halo actions are not matched. Prescribed gas experiment, no SIDM or live halo validation.')
        path.write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
