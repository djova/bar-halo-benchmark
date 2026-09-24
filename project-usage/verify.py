"""Independently recompute published accounting operands; no private log required."""
import csv,hashlib,json,sys
from decimal import Decimal
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else '.')
s=json.loads((p/'summary.json').read_text());rows=list(csv.DictReader((p/'requests.csv').open()));assert len(rows)==s['requests']
for name,meta in s['files'].items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==meta['sha256']
for key,want in s['tokens'].items():assert sum(int(r[key]) for r in rows)==want,key
assert all(int(r['input_tokens'])+int(r['output_tokens'])==int(r['total_tokens']) for r in rows)
assert max(int(r['input_tokens']) for r in rows)==s['max_request_input_tokens']<272000
u=s['tokens'];uncached=u['input_tokens']-u['cached_input_tokens']-u['cache_write_input_tokens'];assert uncached==s['uncached_input_tokens']
assert sum(int(r['uncached_input_tokens']) for r in rows)==uncached
cost=(10*Decimal(uncached)+Decimal(u['cached_input_tokens'])+Decimal('12.5')*u['cache_write_input_tokens']+50*Decimal(u['output_tokens']))/1000000
assert cost==Decimal(str(s['pricing']['standard_estimate_usd']))
assert 2*cost==Decimal(str(s['pricing']['fast_estimate_usd']))
def union_length(records):
 # Sweep endpoints independently of the extractor's interval-merging algorithm.
 events=[]
 for r in records:events.extend([(Decimal(r['start_seconds']),1),(Decimal(r['end_seconds']),-1)])
 active=0;total=Decimal(0);last=None
 for t,d in sorted(events):
  if active and last is not None:total+=t-last
  active+=d;last=t
 assert active==0;return total
items=list(csv.DictReader((p/'timings.csv').open()));turns=list(csv.DictReader((p/'turns.csv').open()))
model=union_length([r for r in items if r['type'] in ['Reasoning','AgentMessage','ContextCompaction']]);assert model==Decimal(str(s['timing']['model_item_seconds']))
assert union_length(turns)==Decimal(str(s['timing']['active_turn_seconds']))
assert len(turns)==s['timing']['completed_turns']+s['timing']['aborted_turns']
for phase in s['phases']:
 rr=[r for r in rows if r['phase']==phase['id']]
 for key,v in phase['tokens'].items():assert sum(int(r[key]) for r in rr)==v
assert abs(sum(x['model_interval_seconds'] for x in s['phases'])-float(model))<.01
print(json.dumps({'requests':len(rows),'total_tokens':u['total_tokens'],'standard_usd':str(cost),'model_interval_hours':float(model)/3600,'active_turn_hours':float(union_length(turns))/3600,'scope':'Consistency of sanitized metadata; no simulation or provider-invoice verification'},indent=2))
