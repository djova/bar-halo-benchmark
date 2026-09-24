"""Export accounting metadata only from one authorized Codex rollout.
Never exports message, reasoning, tool arguments/results, identifiers or host paths.
"""
from __future__ import annotations
import argparse, bisect, collections, csv, datetime as dt, hashlib, io, json
from pathlib import Path

CUTOFF = '2026-09-24T01:45:24.312Z'
PHASES = [
 ('2026-09-20T14:25:46.798Z', 'galaxies', 'Galaxy simulations, controls and first website'),
 ('2026-09-21T17:41:00.222Z', 'response', 'Prescribed-field response and numerical diagnostics'),
 ('2026-09-22T02:46:12.854Z', 'resonance', 'Noisy moving-resonance benchmark and reproduction'),
 ('2026-09-22T23:30:39.293Z', 'population', 'Halo population weighting and response kernels'),
 ('2026-09-23T11:31:49.545Z', 'accuracy', 'Population accuracy diagnostic and estimator cost'),
 ('2026-09-23T17:18:19.443Z', 'publication', 'Canonical article, learning guide and editorial releases'),
]
FIELDS = ['input_tokens','cached_input_tokens','cache_write_input_tokens','output_tokens','reasoning_output_tokens','total_tokens']
def ms(s): return round(dt.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
def merged(intervals):
 result=[]
 for a,b in sorted(intervals):
  if b<a: raise ValueError('Negative interval')
  if result and a<=result[-1][1]: result[-1][1]=max(result[-1][1],b)
  else: result.append([a,b])
 return result
def seconds(intervals):return sum(b-a for a,b in merged(intervals))/1000

def analyze(path, out, cutoff=CUTOFF):
 cut=ms(cutoff);edges=[ms(p[0]) for p in PHASES]+[cut];requests=[];timings=[];turns=[]
 total=collections.Counter();seen=set();item_seen=set();contexts={};current=None;last=None;prefix=hashlib.sha256();first=None
 models=collections.Counter();efforts=collections.Counter();calls=collections.Counter();max_input=0;complete_counts=collections.Counter()
 def phase(t):return PHASES[max(0,bisect.bisect_right(edges[:-1],t)-1)][1]
 with path.open('rb') as f:
  for raw in f:
   r=json.loads(raw);stamp=ms(r['timestamp'])
   if stamp>=cut:break
   prefix.update(raw);v=r['payload'];kind=r['type'];first=stamp if first is None else first
   if kind=='turn_context':current=v;contexts[v['turn_id']]=v
   if kind=='response_item' and v.get('type') in ['function_call','custom_tool_call']:calls[v.get('name','unknown')]+=1
   if kind=='token_usage_record':
    rid=v['response_id']
    if rid in seen:raise ValueError('Duplicate response usage')
    seen.add(rid);u={k:v['usage'][k] for k in FIELDS}
    assert u['input_tokens']+u['output_tokens']==u['total_tokens']
    assert u['cached_input_tokens']+u['cache_write_input_tokens']<=u['input_tokens']
    assert u['reasoning_output_tokens']<=u['output_tokens']
    ctx=contexts.get(v['turn_id'],current);assert ctx
    model=ctx['model'];effort=ctx['effort'];assert model=='gpt-6-astra'
    total.update(u);last=v['thread_token_usage'];max_input=max(max_input,u['input_tokens']);models[model]+=1;efforts[effort]+=1
    uncached=u['input_tokens']-u['cached_input_tokens']-u['cache_write_input_tokens']
    factor=2 if u['input_tokens']>272000 else 1;ofactor=1.5 if factor==2 else 1
    cost=(factor*(10*uncached+u['cached_input_tokens']+12.5*u['cache_write_input_tokens'])+50*ofactor*u['output_tokens'])/1e6
    requests.append(dict(sequence=len(requests)+1,timestamp_utc=r['timestamp'],phase=phase(stamp),model=model,reasoning_effort=effort,**u,uncached_input_tokens=uncached,standard_cost_usd=cost))
   if kind=='event_msg' and v.get('type')=='item_completed':
    item=v['item'];key=(v.get('turn_id'),item.get('id'),item['type']);assert key not in item_seen;item_seen.add(key)
    # Use timings only, never raw_content, arguments, commands or output.
    a,b=v['started_at_ms'],v['completed_at_ms'];assert b>=a
    typ=item['type']
    if typ in ['Reasoning','AgentMessage','ContextCompaction','CommandExecution','Extension','McpToolCall']:
     timings.append(dict(type=typ,start_ms=a,end_ms=b))
   if kind=='event_msg' and v.get('type') in ['task_complete','turn_aborted']:
    duration=v['duration_ms'];assert duration>=0
    turns.append((stamp-duration,stamp));complete_counts[v['type']]+=1
 assert dict(total)=={k:last[k] for k in FIELDS},'Per-response sum differs from cumulative thread counter'
 # Public intervals are relative to session origin and contain no private IDs.
 origin=ms(PHASES[0][0]);model_intervals=[(v['start_ms'],v['end_ms']) for v in timings if v['type'] in ['Reasoning','AgentMessage','ContextCompaction']]
 phase_rows=[]
 for i,(_,key,title) in enumerate(PHASES):
  rows=[r for r in requests if r['phase']==key];a,b=edges[i:i+2]
  clip=lambda seq:[(max(x,a),min(y,b)) for x,y in seq if x<b and y>a]
  phase_rows.append(dict(id=key,title=title,start_utc=PHASES[i][0],end_utc=PHASES[i+1][0] if i+1<len(PHASES) else cutoff,requests=len(rows),tokens={k:sum(r[k] for r in rows) for k in FIELDS},standard_cost_usd=sum(r['standard_cost_usd'] for r in rows),model_interval_seconds=seconds(clip(model_intervals)),active_turn_seconds=seconds(clip(turns))))
 by_type={k:seconds([(v['start_ms'],v['end_ms']) for v in timings if v['type']==k]) for k in sorted({v['type'] for v in timings})}
 result=dict(schema_version=1,snapshot='2026-09-24-session-accounting',cutoff_utc=cutoff,started_utc=PHASES[0][0],last_usage_utc=requests[-1]['timestamp_utc'],scope='This single Galaxy Bar thread, before the accounting request; no other chats or this accounting/deployment turn.',tokens=dict(total),uncached_input_tokens=total['input_tokens']-total['cached_input_tokens']-total['cache_write_input_tokens'],requests=len(requests),models=dict(models),request_counts_by_reasoning_effort=dict(efforts),max_request_input_tokens=max_input,long_context_requests=sum(r['input_tokens']>272000 for r in requests),cache_input_fraction=total['cached_input_tokens']/total['input_tokens'],timing=dict(elapsed_to_cutoff_seconds=(cut-origin)/1000,active_turn_seconds=seconds(turns),completed_turns=complete_counts['task_complete'],aborted_turns=complete_counts['turn_aborted'],model_item_seconds=seconds(model_intervals),item_seconds_by_type=by_type,tool_interval_union_seconds=seconds([(v['start_ms'],v['end_ms']) for v in timings if v['type'] in ['CommandExecution','Extension','McpToolCall']]),server_gpu_seconds=None),phases=phase_rows,pricing=dict(checked_utc='2026-09-24',currency='USD',per_million=dict(uncached_input=10,cached_input=1,cache_write=12.5,output=50),standard_estimate_usd=sum(r['standard_cost_usd'] for r in requests),fast_estimate_usd=2*sum(r['standard_cost_usd'] for r in requests),actual_service_tier='not recorded',sources=['https://developers.openai.com/api/docs/models/gpt-6-astra','https://developers.openai.com/api/docs/pricing','https://developers.openai.com/api/docs/guides/prompt-caching']),reconciliation=dict(unique_response_records=len(seen),duplicate_response_records=0,per_response_sum_equals_thread_cumulative=True,source_prefix_sha256=prefix.hexdigest(),raw_transcript_published=False),top_level_tools=dict(calls),limits=['Repeated cached context is counted on each request; this is not unique authored text.','Reasoning tokens are a subset of output tokens, not an additional billed category.','Model-item intervals are client-recorded latency, not provider GPU execution time; prefill, queueing and unreported work are not separately measured.','Active turns include tool execution, computation monitoring and waiting. Tool intervals overlap each other and model intervals, so their durations must not be added.','Phase labels summarize the task timeline; they are not a claim that every moment within a phase was spent on that topic.','API estimates are hypothetical token-only prices at the snapshot date, not a ChatGPT subscription invoice. They exclude tool fees, hardware, electricity, hosting and external reviewers.','The raw session and private instructions are not published; the public data contain accounting metadata only.'])
 out.mkdir(parents=True,exist_ok=True)
 def csvwrite(name,rows):
  s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows);(out/name).write_text(s.getvalue())
 csvwrite('requests.csv',requests)
 csvwrite('timings.csv',[dict(type=v['type'],start_seconds=(v['start_ms']-origin)/1000,end_seconds=(v['end_ms']-origin)/1000) for v in timings])
 csvwrite('turns.csv',[dict(start_seconds=(a-origin)/1000,end_seconds=(b-origin)/1000) for a,b in turns])
 result['files']={name:dict(bytes=(out/name).stat().st_size,sha256=hashlib.sha256((out/name).read_bytes()).hexdigest()) for name in ['requests.csv','timings.csv','turns.csv']}
 (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('rollout',type=Path);p.add_argument('output',type=Path);p.add_argument('--cutoff',default=CUTOFF);a=p.parse_args();r=analyze(a.rollout,a.output,a.cutoff);print(json.dumps({k:r[k] for k in ['tokens','timing','pricing','phases']},indent=2))
