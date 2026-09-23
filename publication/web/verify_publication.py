#!/usr/bin/env python3
"""Anonymous checks of published records; no simulation, credentials or installs."""
import argparse, hashlib, json, math, urllib.request
from urllib.parse import urljoin
p=argparse.ArgumentParser();p.add_argument('--origin',default='https://djova.ca/galaxy-bar/');p.add_argument('--out');a=p.parse_args();origin=a.origin.rstrip('/')+'/'
receipts=[]
def fetch(path):
 u=urljoin(origin,path)
 req=urllib.request.Request(u,headers={'User-Agent':'GalaxyBar-PublicVerification/1.0','Accept':'application/json,text/plain;q=0.9,*/*;q=0.1'})
 with urllib.request.urlopen(req,timeout=45)as r:
  b=r.read();typ=r.headers.get_content_type();status=r.status
 if path.endswith('.json')and typ!='application/json':raise RuntimeError(f'{path}: expected JSON, received {typ}')
 receipts.append(dict(path=path,status=status,content_type=typ,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 return b
manifest=json.loads(fetch('manifest.json')); artifacts={r['path']:r for r in manifest['artifacts']}
def record(path):
 b=fetch(path);assert hashlib.sha256(b).hexdigest()==artifacts[path]['sha256'],f'Hash mismatch: {path}'
 return json.loads(b)
claims=record('claims.json');models=record('models.json');campaigns=record('campaigns.json');datasets=record('datasets.json')
pop=record('results/populations.json')['rows'];acc=record('results/accuracy.json')['rows'];cost=record('results/cost.json')['rows'];summary=record('results/summary.json')
get=lambda k,t:next(r['response']for r in pop if r['population']==k and r['time']==t)
ratio=abs(get('gaussian',20)/get('halo',20));assert math.isclose(ratio,summary['population_late_magnitude_ratio'],rel_tol=1e-14)
assert get('gaussian',10)>0>get('halo',10)
candidates=[r for r in acc if not r['self_reference']];qualified=[r for r in candidates if r['qualified_5_percent']];rejected=[r for r in candidates if not r['qualified_5_percent']and r['intrinsic_assessment']=='supported']
assert len(candidates)==20 and len(qualified)==8 and len(rejected)==4
assert all(r['independent_assessment']=='supported'for r in qualified)
assert len({(r['s'],r['eta'])for r in candidates})==1
for c in campaigns['campaigns']:assert c['member_count']==len(c['members'])
full=record('diagnostics/population-response/independent-validation.json')
for r in pop:
 source=full['rows'][int(r['pointer'].rsplit('/',1)[1])]
 assert r['response']==source['integral_w_K_B']['mean']
full=record('diagnostics/population-accuracy/accuracy-explorer.json')
for r in acc:
 source=full['rows'][int(r['pointer'].rsplit('/',1)[1])]
 assert r['forecast']==source['forecast']['approximate']['mean']
 assert r['intrinsic_population_error']==source['independent']['paired_population_error']
for r in cost:
 source=full['cost']['rows'][int(r['pointer'].rsplit('/',1)[1])]
 assert r['cost_times_variance_ratio']==source['cost_times_variance_ratio']
broad=next(r for r in cost if r['population']=='halo'and r['s']==.25 and r['time']==20)
narrow=next(r for r in cost if r['population']=='stress0.015625'and r['s']==.25 and r['time']==20)
result=dict(release=manifest['release'],activity='Verification of supplied records, not simulation reproduction or new physics',population_late_magnitude_ratio=ratio,candidate_count=len(candidates),qualified_count=len(qualified),independently_supported=sum(r['independent_assessment']=='supported'for r in qualified),distinct_new_conditions=1,conservative_rejections=[r['id']for r in rejected],broad_conditional_cost_variance_ratio=broad['cost_times_variance_ratio'],broad_between_batch_ratio=broad['between_batch_ratio'],narrow_ratio=narrow['cost_times_variance_ratio'],scope='Prescribed local operator; Cartesian transfer unresolved and live-halo/SIDM inference not established.',downloads=receipts)
if a.out:open(a.out,'w').write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
