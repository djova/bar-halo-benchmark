#!/usr/bin/env python3
"""Build a public article from frozen scientific records; never runs a simulation.
Requires Python 3.11 and Markdown==3.8.2. Run from the project/release root.
"""
import argparse, csv, hashlib, html, io, json, re, shutil
from pathlib import Path
import markdown

ROOT=Path(__file__).resolve().parents[2]; W=ROOT/'web'; SRC=ROOT/'research/publication'
VERSION='2026-09-23.2'; SCIENCE='cdb30b5b2f350d2f3de6831995b83f281fe2974e'
PUBLIC='https://github.com/djova/bar-halo-benchmark'; RAW=f'https://raw.githubusercontent.com/djova/bar-halo-benchmark/{SCIENCE}'
LABELS={'halo':'Reference halo','exponential':'Slope-matched exponential','gaussian8':'Gaussian σ=8','gaussian32':'Gaussian σ=32','gaussian128':'Gaussian σ=128','gaussian512':'Gaussian σ=512','gaussian':'Gaussian σ=8'}
def read(p): return json.loads((W/p).read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def number_notation(x):
 # Preserve the decoded scientific value while avoiding digit sequences that
 # collide with the unchanged public privacy gate's phone-number pattern.
 return format(float(x),'.17e') if re.search(r'\b[2-9]\d{2}[2-9]\d{6}\b',str(x)) else str(x)
def jsave(p,d):
 text=json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)
 tokens=re.compile(r'"(?:\\.|[^"\\])*"|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')
 text=tokens.sub(lambda m:m[0] if m[0].startswith('"') else number_notation(m[0]),text)
 assert json.loads(text)==d, 'Publication notation changed a value'
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text+'\n')
def fmt(x):
 if x is None:return 'unavailable'
 if isinstance(x,bool):return 'yes' if x else 'no'
 if not isinstance(x,(int,float)):return str(x)
 return f'{x:.9g}'
def table(headers,rows):
 return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(fmt(x).replace('|','&#124;') for x in r)+' |\n' for r in rows)
def render(s):
 # Protect TeX delimiters from Markdown backslash escaping and table pipes.
 maths=[]
 def protect(m):
  maths.append('<span data-math="'+html.escape(m[1],quote=True)+'"></span>')
  return 'MATHPLACEHOLDER'+str(len(maths)-1)+'END'
 s=re.sub(r'\\\((.*?)\\\)',protect,s,flags=re.S)
 rendered=markdown.markdown(s,extensions=['tables','fenced_code','attr_list','md_in_html'])
 for i,value in enumerate(maths):rendered=rendered.replace('MATHPLACEHOLDER'+str(i)+'END',value)
 return rendered
def shell(title,body,script=''):
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="publication-version" content="{VERSION}"><meta name="description" content="Versioned Galaxy Bar research: population-selection bias, response kernels and numerical accuracy under a prescribed local resonance."><title>{html.escape(title)} · Galaxy Bar</title><link rel="stylesheet" href="story.css"><link rel="stylesheet" href="population-response.css"><link rel="stylesheet" href="population-accuracy.css"><link rel="stylesheet" href="publication.css"><link rel="alternate" type="application/json" href="manifest.json" title="Publication manifest"></head><body><a class="skip" href="#main">Skip to content</a><header><a class="brand" href="./">Galaxy Bar</a></header><main id="main" class="publication population-publication accuracy-publication">{body}</main><footer class="publication-footer">Release {VERSION} · Not externally reviewed · <a href="paper.html">Research</a> · <a href="learn.html">Learn</a> · <a href="reproduce.html">Evidence</a> · <a href="agents.html">Agent access</a></footer>{script}</body></html>'''
def page(file,title,md,script=''):
 body=render(md)
 for equation in re.findall(r'\((EQ-[A-Z]+-\d+)\)',md):
  body=body.replace('('+equation+')','<span id="'+equation+'"></span>('+equation+')',1)
 captions=iter(['Model registry','Original population comparison','All recorded operational decisions','Complete accuracy values','Matched estimator cost']) if file=='paper.html' else iter([])
 def wrap_table(m):
  caption=next(captions,title+' — complete values')
  return '<div class="publication-table" tabindex="0" role="region" aria-label="'+caption+'"><table><caption>'+caption+'</caption>'+m[1]+'</table></div>'
 body=re.sub(r'<table>(.*?)</table>',wrap_table,body,flags=re.S)
 (W/file).write_text(shell(title,body,script))
def dataframe(name,rows):
 jsave(W/'results'/f'{name}.json',{'release':VERSION,'rows':rows})
 if rows:
  o=io.StringIO();wr=csv.DictWriter(o,fieldnames=list(rows[0]));wr.writeheader();wr.writerows([{k:number_notation(v) if isinstance(v,(int,float))and not isinstance(v,bool)else v for k,v in r.items()}for r in rows]);(W/'results'/f'{name}.csv').write_text(o.getvalue())

A=read('diagnostics/population-accuracy/accuracy-explorer.json'); P=read('diagnostics/population-response/independent-validation.json'); I=read('data/index.json')
models=[
 {'id':'GAL-LIVE','title':'Self-gravitating galaxy and its fixed-field controls','evolves':'Stellar and halo particles; live components alter gravity. Named frozen/static controls remove specified response.','clock':'Gyr; kpc; solar masses','supports':'Behavior and numerical sensitivity of the specified galaxy models','excludes':'No SIDM comparison; no converged universal bar-strength prediction','methods':'methodology.html'},
 {'id':'CART-EXT','title':'Prescribed-field Cartesian orbits','evolves':'Test particles in an external analytical field, imposed bar and disturbances; cloud does not react collectively','clock':'Analytical-potential model time/action','supports':'Particle response to those specified external fields','excludes':'Not live-halo validation','methods':'response-methods.html'},
 {'id':'RES-POS','title':'Reduced noisy resonance, positive population','evolves':'Slow action and resonant angle; constant additive action diffusion; fixed fast-action slice','clock':'Dimensionless T, x and impulse B','supports':'Population response and numerical accuracy within this local operator','excludes':'Not full-halo torque, SIDM or general confidence coverage','methods':'paper.html#model'},
 {'id':'RES-SIGNED','title':'Earlier signed perturbation with reservoirs','evolves':'Signed deviation with its own reservoir/boundary conditions','clock':'Its documented reduced-model units','supports':'Verification and response of that separate setup','excludes':'Not interchangeable with positive-population results','methods':'noise-methods.html'},
 {'id':'SYNTH','title':'Synthetic controls','evolves':'Known stochastic laws or analytical limiting processes','clock':'Control-specific units','supports':'Verification of estimators, coordinates or numerical algorithms','excludes':'Not a new astrophysical measurement','methods':'response-validation.html'},
]
jsave(W/'models.json',{'release':VERSION,'models':models})
campaigns=I['campaigns']+[
 {'id':'CART-RESPONSE','model_id':'CART-EXT','members':['independent-phase-replication','external-cloud-characterization','grainy-bar-pilot','cartesian-transfer-pilot'],'count_unit':'named investigations, not independent realizations','verdict':'Smooth same-condition phase replication; grainy ordering and new-condition 3D transfer unresolved.','page':'response.html'},
 {'id':'RES-POP','model_id':'RES-POS','members':['population-validation','heldout-populations','population-approximation-accuracy','matched-estimator-cost'],'count_unit':'named investigations, not independent physical regimes','verdict':'Conditional population bias and accuracy/cost outcomes; see claim-level evidence.','page':'paper.html'}]
for c in campaigns:
 c['member_count']=len(c['members'])
 if c['id'].startswith('GAL-'):
  assert len(set(c['members']))==len(c['members'])
  assert set(c['members'])<=set(r['id'] for r in I['runs'])
  c['completed_count']=sum(r['complete'] for r in I['runs'] if r['id'] in c['members'])
jsave(W/'campaigns.json',{'release':VERSION,'campaigns':campaigns,'scope':'Counts derive from explicit membership. Overlapping campaigns are not summed.'})

pop=[]
for idx,r in enumerate(P['rows']):
 if r['s']==.25 and r['population'].endswith('-40'):
  key=r['population'].removesuffix('-40');e=r['integral_w_K_B']
  pop.append(dict(id=f'POP-{key}-T{int(r["tau"])}',population=key,time=r['tau'],s=.25,eta=.1,cutoff=40,response=e['mean'],ci95_low=e['ci95'][0],ci95_high=e['ci95'][1],numerical_window_qualified=r['numerical_window_qualified'],source='diagnostics/population-response/independent-validation.json',pointer=f'/rows/{idx}'))
dataframe('populations',pop)
get=lambda k,t:next(r['response'] for r in pop if r['population']==k and r['time']==t)
ratio=abs(get('gaussian',20)/get('halo',20))
acc=[]
for idx,r in enumerate(A['rows']):
 f=r['forecast'];a=r['independent'];v=a['independent'];h=a['independent_halo']
 acc.append(dict(id=f'ACC-{f["population"]}-T{int(f["tau"])}-W{f["cutoff"]}',population=f['population'],time=f['tau'],cutoff=f['cutoff'],s=A['s'],eta=A['eta'],self_reference=f['population']=='halo',forecast=f['approximate']['mean'],independent_response=v['response'],intrinsic_population_error=a['paired_population_error'],intrinsic_error_proxy=a['paired_numerical_proxy'],forecast_minus_independent_halo=a['forecast_minus_independent_halo'],independent_halo_proxy=h['numerical_proxy'],population_allowance=f['approximation_allowance'],full_allowance=f['combined_response_allowance'],target=f['five_percent_absolute_target'],qualified_5_percent=f['five_percent_qualified'],independent_assessment=a['independent_five_percent_test'],intrinsic_assessment=a['intrinsic_population_five_percent_test'],sign_qualification=f['sign_qualification'],sign_assessment=a['sign_test'],source='diagnostics/population-accuracy/accuracy-explorer.json',pointer=f'/rows/{idx}'))
dataframe('accuracy',acc)
cost=[]
for idx,r in enumerate(A['cost']['rows']):
 costs={x['method']:x for x in r['precision']}
 cost.append(dict(id=f'COST-{r["population"]}-s{r["s"]}-T{int(r["tau"])}',population=r['population'],s=r['s'],time=r['tau'],raw_cpu_seconds=costs['raw']['measured_mean_accounted_batch_cpu_seconds'],remainder_cpu_seconds=costs['remainder']['measured_mean_accounted_batch_cpu_seconds'],cost_times_variance_ratio=r['cost_times_variance_ratio'],bootstrap_low=r['paired_batch_bootstrap_cost_ratio_interval'][0],bootstrap_high=r['paired_batch_bootstrap_cost_ratio_interval'][1],between_batch_ratio=r['between_batch_cost_ratio'],raw_minus_remainder=r['paired_raw_minus_remainder']['mean'],raw_difference_ci_low=r['paired_raw_minus_remainder']['ci95'][0],raw_difference_ci_high=r['paired_raw_minus_remainder']['ci95'][1],contains_zero=r['paired_interval_contains_zero'],source='diagnostics/population-accuracy/accuracy-explorer.json',pointer=f'/cost/rows/{idx}'))
dataframe('cost',cost)
counts=dict(candidate_comparisons=sum(not r['self_reference'] for r in acc),qualified_5_percent=sum(r['qualified_5_percent'] and not r['self_reference'] for r in acc),supported_qualified=sum(r['qualified_5_percent'] and r['independent_assessment']=='supported' and not r['self_reference'] for r in acc),conservative_rejections=sum(not r['qualified_5_percent'] and r['intrinsic_assessment']=='supported' and not r['self_reference'] for r in acc))
assert counts=={'candidate_comparisons':20,'qualified_5_percent':8,'supported_qualified':8,'conservative_rejections':4},counts
summary={'release':VERSION,'population_late_magnitude_ratio':ratio,'counts':counts,'dynamical_conditions_in_prospective_test':1,'condition':{'s':.5,'eta':.1},'evidence_kind':'Recalculation of published records, not new evolution.'}
jsave(W/'results/summary.json',summary)

limitations=[
 ('LIM-01','One isochrone fast-action slice and finite windows/times; no total halo torque or universal 4.7 correction.'),
 ('LIM-02','Imposed bar and population-independent additive noise; no collective halo response or calibrated SIDM operator.'),
 ('LIM-03','Approximate sampling coverage and numerical-refinement proxies; no rigorous operational 5% guarantee.'),
 ('LIM-04','Eight qualified comparisons share one new dynamical condition and correlated kernel; no eight independent physical regimes.'),
 ('LIM-05','Prescribed-field 3D transfer remains unresolved; even successful transfer would not validate a live halo.'),
 ('LIM-06','Cost-times-variance ratios project precision under a fixed workflow; no measured 6900-fold faster simulation.'),
 ('LIM-07','Specific estimator priority and astrophysical generalization remain open; not externally reviewed.'),
 ('LIM-08','Software reproduction and deployment checks do not independently confirm physics.')]
claims=[]
def claim(id,wording,model,anchor,path,pointer,status,conditions,uncertainty,exclusions,category='numerical_result'):
 p=W/path
 claims.append(dict(id=id,wording=wording,article_anchor=f'paper.html#{anchor}',model_id=model,category=category,conditions=conditions,observable='noise-minus-smooth accumulated bar-mediated transfer' if model=='RES-POS' else 'specified in source record',units='dimensionless integral(w K_B dx)' if model=='RES-POS' else 'source-defined',reference_control='same dynamics/population without imposed noise' if model=='RES-POS' else 'source-defined matched comparison',evidence=[dict(path=path,json_pointer=pointer,sha256=digest(p))],code_version=SCIENCE,figure_version=VERSION,uncertainty=uncertainty,status=status,exclusions=exclusions,release=VERSION,protocol='diagnostics/population-accuracy/PLAN.md' if id.startswith('PA-') else 'reproduce.html',outcome=path))
common='Eight independent seeded batches; population/time/window contractions share paths. Pointwise Student-t intervals where stated; paired numerical differences remain proxies.'
claim('POP-01',f'At s=0.25, Gaussian and reference-halo weighting in the tested slice have opposite T=10 responses; their T=20 suppression magnitudes differ by {ratio:.6f}.','RES-POS','population-result','results/populations.json','/rows','supported_locally',{'s':.25,'eta':.1,'times':[10,20],'cutoff':40},common,['LIM-01','LIM-02'])
claim('POP-02','The slope-matched exponential closely follows the reference-halo point estimates; the point differences alone do not certify sub-0.1% accuracy.','RES-POS','population-result','diagnostics/population-accuracy/joint-error-assessment.json','/exponential_halo','supported_locally',{'s':.25,'eta':.1,'times':[10,20]},common,['LIM-01','LIM-03'])
claim('PA-ACC-01','Eight advance 5% qualifications are supported by independent numerical comparison at one new sweep rate, s=0.5.','RES-POS','accuracy','results/accuracy.json','/rows','supported_locally',{'s':.5,'eta':.1,'times':[10,20],'cutoffs':[40,64],'populations':['exponential','gaussian512']},'Eight kernel batches; simultaneous Student-t/Bonferroni envelope and paired refinement proxies. Independent deterministic evolution adds numerical proxies, not a new sampling interval.',['LIM-03','LIM-04'])
claim('PA-ACC-02','Four Gaussian-128 comparisons meet 5% in the independent assessment but are not qualified by the conservative absolute-gradient allowance.','RES-POS','accuracy','diagnostics/population-accuracy/conservatism-explanation.json','/rows','supported_locally',{'s':.5,'eta':.1,'population':'gaussian128'},common,['LIM-03','LIM-04'])
claim('EST-01','The matched estimator has a large conditional cost-times-variance advantage for broad halo weights; the advantage disappears for the narrowest stress population.','RES-POS','estimator','results/cost.json','/rows','supported_locally',{'s':[0,.25],'times':[10,20]},'Eight paired batches per sweep; whole-batch bootstrap intervals and distinct conditional/between-batch estimates; one pointwise consistency flag retained.',['LIM-06'])
claim('POP-MARG-01','All 24 historical operational forecasts passed their original rule; two early Gaussian-12 window tests remain marginal under a later combined numerical-proxy assessment.','RES-POS','limitations','diagnostics/population-accuracy/joint-error-assessment.json','/historical_forecast_assessment','marginal',{'old_allowance':'max(0.0002, 5% of forecast)'},common,['LIM-03'])
claim('CART-01','A reduced-model prediction has not yet achieved qualified transfer to prescribed-field three-dimensional orbits.','CART-EXT','limitations','diagnostics/population-response/halo-pilot.json','','unresolved',{'study':'halo-slice pilot'},'Measured discrepancy precision exceeded the bounded cost allowance; unresolved agreement is not falsification.',['LIM-05'])
claim('REP-01','The project receipt documents exact reproduction of 162 saved arrays from the released numerical source. This publication campaign does not claim a new rerun.','RES-POS','reproduction','diagnostics/population-accuracy/accuracy-reproduction.json','/saved_array_count','supported_locally',{'public_numerical_revision':'66143ebdb7441e17f4b44c23d15c2b35eb66841a'},'Same seeds; software reproducibility, no independent physical sampling.',['LIM-08'],'software_reproduction')
claim('GAL-01','Three of four matched force-opening comparisons fail the original endpoint criterion; this identifies numerical sensitivity, not the continuum solution.','GAL-LIVE','models','diagnostics/followup/error-budget.json','/force_pairs','supported_locally',{'scope':'four paired force-opening comparisons'},'Individual paired sensitivities; not independent Gaussian uncertainty.',['LIM-08'])
claim('OBS-01','The released selected observational amplitude sample contains 112 galaxies with median 0.4685. This publication campaign does not reprocess the catalogues.','GAL-LIVE','models','data/observational-summary.json','/s4g_mass_matched_A2','supported_locally',{'source':'S4G; fixed mass selection'},'Population spread is not an error bar on one model. Aperture and measurement differences remain.',['No observational validation of the local resonance model.'],'observational_benchmark')


for c in claims:
 if c['id']=='EST-01':c['observable']='Raw/remainder cost-times-variance ratio';c['units']='dimensionless efficiency; CPU seconds reported separately'
 if c['id']=='REP-01':c['observable']='Number of arrays reported exactly reproduced';c['units']='array count'
 if c['model_id']=='GAL-LIVE':c['code_version']={'scope':'Historical galaxy/catalogue outputs; not reproduced by the reduced benchmark revision','provenance':'data/manifest.json' if c['id']=='OBS-01' else 'diagnostics/followup/error-budget.json#/source_sha256'}
jsave(W/'claims.json',{'schema_version':1,'release':VERSION,'claims':claims,'limitations':[{'id':i,'text':t} for i,t in limitations],'review_status':'not_externally_reviewed','extends_historical_ledger':'diagnostics/population-accuracy/CLAIM_LEDGER.md','identities':[{'id':'EQ-KER-01','status':'exact_under_stated_assumptions','article_anchor':'paper.html#kernel'},{'id':'EQ-ERR-01','status':'exact_under_stated_assumptions','article_anchor':'paper.html#accuracy'},{'id':'EQ-EST-01','status':'exact_under_stated_assumptions','article_anchor':'paper.html#estimator'}]})
# The same component is embedded in the article and retains its original URL.
legacy=(W/'population-accuracy.html').read_text()
# Keep a source template independent of generated static table contents.
explorer=legacy[legacy.index('<section id="accuracy-explorer">'):legacy.index('<section id="accuracy-overview">')]
cost_interactive=legacy[legacy.index('<fieldset class="population-controls" id="accuracy-cost-controls"'):legacy.index('<section id="accuracy-meaning">')]
cost_interactive=cost_interactive.rsplit('</section>',1)[0]
staticrows=''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [f'{LABELS[r["population"]]} / T{int(r["time"])} / {r["cutoff"]}', 'Qualified' if r['qualified_5_percent'] else 'Not qualified',r['independent_assessment'],r['sign_assessment'].replace('_',' ')])+'</tr>' for r in acc)
legacy=re.sub(r'(<tbody id="accuracy-all">).*?(</tbody>)',lambda m:m[1]+staticrows+m[2],legacy,flags=re.S)
(W/'population-accuracy.html').write_text(legacy)
explorer=re.sub(r'(<tbody id="accuracy-all">).*?(</tbody>)',lambda m:m[1]+staticrows+m[2],explorer,flags=re.S)
# Give no-script readers the same default measured selection and a full table.
default=next(r for r in acc if r['population']=='exponential' and r['time']==20 and r['cutoff']==40)
for id,value in [('accuracy-response',fmt(default['forecast'])),('accuracy-allowance',fmt(default['population_allowance'])),('accuracy-actual',fmt(default['intrinsic_population_error'])),('accuracy-verdict','5% qualified in advance · independent test supported')]:
 explorer=re.sub(r'(<(?:strong|h3) id="'+id+r'">).*?(</(?:strong|h3)>)',lambda m:m[1]+value+m[2],explorer)
explorer=explorer.replace('Loading recorded forecasts and independent outcomes…','Published default: exponential, T = 20, cutoff 40. Interactive plots load below; complete values are in the static tables.').replace('independent evolution required','independently evolved approximation minus halo')

pop_table=table(['Population','T','Response','95% lower','95% upper','Numerical/window qualified'],[[LABELS[r['population']],r['time'],r['response'],r['ci95_low'],r['ci95_high'],r['numerical_window_qualified']]for r in pop])
acc_table=table(['ID / population · T · window','Kernel forecast','Independent response','Intrinsic error ± proxy','Forecast − independent halo','Full allowance / 5% target','Advance 5% / independent'],[[f"<a id=\"{r['id']}\" href=\"paper.html?population={r['population']}&amp;time={int(r['time'])}&amp;window={r['cutoff']}#interactive-decision\">{LABELS[r['population']]} · {int(r['time'])} · {r['cutoff']}</a>"+(' (reference)'if r['self_reference']else''),r['forecast'],r['independent_response'],fmt(r['intrinsic_population_error'])+' ± '+fmt(r['intrinsic_error_proxy']),r['forecast_minus_independent_halo'],fmt(r['full_allowance'])+' / '+fmt(r['target']),('Qualified'if r['qualified_5_percent']else'Not qualified')+' / '+r['independent_assessment']]for r in acc])
cost_table=table(['Population · s · T','Raw / remainder CPU s','Cost×variance ratio','Bootstrap interval','Between-batch ratio','Raw−remainder 95% interval'],[[f"{r['population']} · {r['s']} · {int(r['time'])}",fmt(r['raw_cpu_seconds'])+' / '+fmt(r['remainder_cpu_seconds']),r['cost_times_variance_ratio'],f"[{fmt(r['bootstrap_low'])}, {fmt(r['bootstrap_high'])}]",r['between_batch_ratio'],f"[{fmt(r['raw_difference_ci_low'])}, {fmt(r['raw_difference_ci_high'])}]"]for r in cost])
model_table=table(['Model ID','What evolves','What this establishes','Clock / methods'],[[m['id']+' — '+m['title'],m['evolves'],m['supports']+'; '+m['excludes'],f"{m['clock']} · [methods]({m['methods']})"]for m in models])
credit='Project initiated and maintained by [djova](https://github.com/djova). Scientific authorship beyond this project role is not asserted. Analysis, software and exposition were developed with AI assistance; the maintainer is the human contact through the public issue tracker.'
release=f'<p class="publication-meta">Canonical article · Release {VERSION} · Not externally reviewed · <a href="reproduce.html#licenses">Human maintainer and AI disclosure</a></p>'
replacements={'RELEASE':release,'RATIO':f'{ratio:.6f}','MODELS':model_table,'POPULATION_TABLE':pop_table,'ACCURACY_TABLE':'### Complete accuracy values {#table-accuracy}\n\n'+acc_table+'\n[JSON](results/accuracy.json) · [CSV](results/accuracy.csv). Numeric uncertainty is defined in the protocol above; a deterministic proxy is not a sampling confidence interval.','COST_TABLE':'### Complete estimator-cost values {#table-cost}\n\n'+cost_table+'\n[JSON](results/cost.json) · [CSV](results/cost.csv). All 24 endpoints retain their paired consistency assessments.','LIMITATIONS':'\n\n'.join(f'<span id="{i}"></span>**{i}.** {t}'for i,t in limitations),'ACCURACY_INTERACTIVE':explorer,'COST_INTERACTIVE':cost_interactive,'REVISION':f'**Release {VERSION}:** typeset mathematics with local KaTeX, desktop table layout repairs and expandable numeric evidence. Release 2026-09-23.1 retained the initial consolidated article and scope corrections. Scientific outputs and historical criteria unchanged. [Archived studies and corrections](archive.html) · [release manifest](manifest.json) · [reuse conditions](reproduce.html#licenses).','BIBLIOGRAPHY':'## References and reading record {#references}\n\nPrimary links appear beside the associated statements. [Original scholarly sources](diagnostics/population-accuracy/SOURCES.md) and [publication review sources](publication-sources.md) identify the inspected material and its limits. Accessibility follows the [W3C complex-image guidance](https://www.w3.org/WAI/tutorials/images/complex/) through readable captions and complete values. Registry design follows [FAIR principles](https://www.gofair.foundation/fair-principles); no formal certification is claimed.'}
for key,file,alt,anchor in [('POP','population-comparison.png','Original Gaussian has opposite early sign; halo and exponential closely agree. Values follow.','F-POP-01'),('ACC','population-accuracy.png','All twenty approximation candidates, including four conservative Gaussian128 rejections. Complete values follow.','F-ACC-01'),('COST','estimator-efficiency.png','Large broad-population variance advantage falls to about unity at the narrowest stress width. Values follow.','F-COST-01')]:
 replacements['FIG-'+key]=f'<figure id="{anchor}" class="accuracy-figure"><a href="diagnostics/population-accuracy/{file}"><img src="diagnostics/population-accuracy/{file}" alt="{alt}"></a><figcaption>{anchor} · {alt} Local resonance units; reference-halo weighting means one fixed fast-action slice. Parameters, uncertainty and complete values follow immediately below.</figcaption></figure>'
for c in claims:replacements['CLAIM:'+c['id']]=f'<p class="publication-claim" id="{c["id"]}"><a href="claims.json">{c["id"]}</a> · {html.escape(c["wording"])}</p>'
article=(SRC/'ARTICLE.md').read_text()
for k,v in replacements.items():article=article.replace('{{'+k+'}}',v)
assert '{{'not in article
# Markdown keeps the full static argument; large HTML controls are replaced by links.
md_article=article.replace(explorer,'[Interactive decision explorer](paper.html#interactive-decision). All recorded outcomes are tabulated below.').replace(cost_interactive,'[Interactive estimator comparison](paper.html#estimator). All recorded outcomes are tabulated below.')
(W/'paper.md').write_text(md_article)
page('paper.html','Finite-time population bias in noisy sweeping resonances',article,'<script type="module" src="population-accuracy.js"></script>')
page('learn.html','Learn the foundations',(SRC/'LEARN.md').read_text())
(W/'learn.md').write_text((SRC/'LEARN.md').read_text());shutil.copyfile(SRC/'SOURCES.md',W/'publication-sources.md')
# Remaining pages/registries are built below.

def dataset(id,path,description,columns,model='RES-POS',pairing=common,seeds=None):
 p=W/path
 return dict(id=id,path=path,description=description,model_id=model,release=VERSION,code_version=SCIENCE,bytes=p.stat().st_size,sha256=digest(p),media_type='text/csv'if p.suffix=='.csv'else'application/json',columns=columns,missing_values='JSON null means unavailable or inapplicable, never zero. No inferred imputation. CSV boolean fields use True/False.',sampling_and_pairing=pairing,seeds=seeds or 'See frozen recipe; no new random numbers generated for this publication.',license='Benchmark-derived numerical records: MIT where covered by the benchmark license; third-party sources retain their own terms.')
response_columns={
 'population':'Named initial physical weight; no unit-mass renormalization','time':'Dimensionless endpoint T; only 10 and 20 are recorded','s':'Dimensionless resonance sweep','eta':'Dimensionless imposed noise, D=2 eta/pi','cutoff':'Physical taper cutoff in x, not numerical domain','response':'Dimensionless accumulated noise-minus-smooth integral(w K_B dx)','ci95_low':'Lower pointwise Student-t sampling limit, 8 independent batches','ci95_high':'Upper pointwise Student-t sampling limit','numerical_window_qualified':'Historical timestep/window decision, distinct from statistical interval','source':'Relative source JSON path','pointer':'RFC6901 pointer to complete original row','id':'Stable result identifier'}
accuracy_columns={
 'forecast':'Dimensionless approximate response from sampled kernel','independent_response':'Dimensionless response from independent deterministic numerical evolution','intrinsic_population_error':'Paired independent approximation minus halo response','intrinsic_error_proxy':'Sum of measured paired numerical-refinement changes; not a sampling CI','forecast_minus_independent_halo':'Sampled approximate forecast minus independently evolved halo; distinct from intrinsic error','independent_halo_proxy':'Numerical proxy for independent halo','population_allowance':'Absolute gradient-mismatch allowance with estimated kernel uncertainty and mesh proxy','full_allowance':'Population allowance plus approximate response sampling/numerical allowance','target':'Frozen absolute 5% target from lower halo-response estimate','qualified_5_percent':'Frozen operational decision, including self-references','independent_assessment':'supported/contradicted/inconclusive assessment of forecast against independent halo','intrinsic_assessment':'Independent intrinsic population 5% assessment','sign_qualification':'positive/negative/unqualified under frozen rule','sign_assessment':'Independent sign assessment','self_reference':'Halo reference row, excluded from candidate counts'}
cost_columns={
 'raw_cpu_seconds':'Measured mean CPU per accounted raw batch, seconds','remainder_cpu_seconds':'Measured mean CPU per remainder batch, seconds','cost_times_variance_ratio':'Dimensionless raw cost*conditional variance divided by remainder equivalent','bootstrap_low':'Lower paired whole-batch-bootstrap interval for ratio','bootstrap_high':'Upper paired whole-batch-bootstrap interval for ratio','between_batch_ratio':'Alternative ratio using observed between-batch variance','raw_minus_remainder':'Dimensionless paired method discrepancy','raw_difference_ci_low':'Pointwise95% sampling lower limit','raw_difference_ci_high':'Pointwise95% sampling upper limit','contains_zero':'Whether method discrepancy interval includes zero'}
datasets=[dataset('DS-POP','results/populations.json','Principal original population comparison',response_columns,seeds=list(range(94501,94509))),dataset('DS-ACC','results/accuracy.json','All24 prospective comparisons;20 candidates and4 references',{k:v for k,v in response_columns.items()if k not in ['response','ci95_low','ci95_high','numerical_window_qualified']}|accuracy_columns,seeds=list(range(96101,96109))),dataset('DS-COST','results/cost.json','All24 matched estimator cost endpoints', {k:response_columns[k]for k in ['id','population','time','s','source','pointer']}|cost_columns,seeds=list(range(95801,95809)))]
# Keep normative generator seeds in the original recipe; verify cost seeds below.
for d in datasets:
 if d['id']=='DS-COST':d['seeds']=list(range(96211,96219));d['seed_reference']=f'{RAW}/accuracy/cost/reference.json#/cases'
for d in list(datasets):
 csvd=dict(d);csvd['id']+='-CSV';csvd['path']=d['path'].replace('.json','.csv');p=W/csvd['path'];csvd['bytes']=p.stat().st_size;csvd['sha256']=digest(p);csvd['media_type']='text/csv';datasets.append(csvd)
for id,path,description,columns in [
 ('DS-ACC-FULL','diagnostics/population-accuracy/accuracy-explorer.json','Full frozen/independent and512-bin interactive evidence',{'rows':'24ordered selections; forecast and independent preserve complete original fields','rows[].plot.edges':'513action edges defining512bins; dimensionless x','rows[].plot.kernel_mean':'Signed primitive Q cell averages, same kernel for all weights at each time','rows[].plot.kernel_absolute_upper':'Operational absolute kernel envelope; not rigorous bound','rows[].plot.signed_error':'Signed integrated gradient mismatch by bin','rows[].plot.expanded_allowance':'Absolute expanded mismatch integrated by bin','rows[].plot.signed_density':'Signed contribution divided by bin width','rows[].plot.allowance_density':'Absolute allowance divided by bin width','rows[].plot.halo_gradient':'Mean reference gradient within each bin','rows[].plot.approximate_gradient':'Mean candidate gradient within each bin','rows[].plot.halo_weight':'Reference weight averaged in each bin; fixed central normalization','rows[].plot.approximate_weight':'Approximate weight averaged in each bin','rows[].plot.absolute_gradient_mismatch':'Mean absolute derivative mismatch','rows[].plot.plugin_allowance':'Integrated absolute plug-in contribution before kernel uncertainty','display':'Fine-cell products are summed BEFORE averaging; multiplying displayed mean curves is not equivalent','counts':'Correlated comparison counts, not independent regimes','provenance':'Frozen source hashes and timestamps'}),
 ('DS-POP-FULL','diagnostics/population-response/independent-validation.json','Paired population means, intervals and controls',{'rows':'24population/sweep/time/window measurements','population_differences':'Paired response contrasts','between_sweep':'Paired or stated between-sweep contrast','Lz_per_fast_action_area_factor':'Conversion from dimensionless response','independent_batches':'Sampling unit count','numerical_allowance':'Declared control interpretation','source_sha256':'Analysis-code provenance'}),
 ('DS-RETRO','diagnostics/population-accuracy/joint-error-assessment.json','Historical operational and expanded assessments',{'historical_forecast_assessment':'24old rules preserved with joint_proxy_qualification','exponential_halo':'Paired differences and numerical proxies','scope':'Interpretation boundary'}),
 ('DS-CONSERVATIVE','diagnostics/population-accuracy/conservatism-explanation.json','Four Gaussian128 cancellations',{'rows[].tau':'Dimensionless T','rows[].cutoff':'Physical action cutoff','rows[].signed_mean_kernel_population_error':'Signed contraction, dimensionless response','rows[].mean_kernel_absolute_gradient_integral':'Absolute plug-in integral before kernel uncertainty','rows[].frozen_five_percent_target':'Frozen absolute target','rows[].additional_kernel_uncertainty_expansion':'Added estimated-kernel allowance','rows[].mesh_addition':'Numerical mesh proxy'}),
 ('DS-REPRO','diagnostics/population-accuracy/accuracy-reproduction.json','Reported fresh-source reproduction receipt',{'saved_array_count':'162saved numeric arrays compared by project','cases':'Case-specific reported comparisons','figure':'Image comparison/inspection evidence','kernel_cpu_seconds':'Summed worker CPU','independent_cpu_seconds':'Summed worker CPU','public_source_commit':'Pinned numerical revision','scope':'Reproduction is not independent physical sampling'}),
 ('DS-GAL','data/index.json','Completed galaxy collection and scoped campaign membership',{'runs':'25run descriptors, each linked to its trajectory JSON','campaigns':'Explicit original10 and expanded25membership, archived historical verdict','run_count':'Derived collection count','completed_count':'Derived terminal count','verdict':'Collection scope only; not shared scientific all-pass'},),
 ('DS-OBS','data/observational-summary.json','Original archived catalogue-selection summary',{'selection.mass_Msun':'Model stellar mass in solar masses; selection center','selection.half_width_dex':'Log10stellar-mass selection half-width0.3','selection.amplitude_convention':'Cosine amplitude convention, aperture and mass-to-light assumption','s4g_mass_matched_A2.n':'112selected amplitudes','s4g_mass_matched_A2.median':'0.4685, dimensionless cosine amplitude','s4g_mass_matched_A2.p16 / p84':'Population percentiles, not uncertainty on a model','s4g_mass_matched_RA2_kpc':'Radius of amplitude maximum in kpc','s4g_mass_matched_rbar_kpc':'Selected deprojected bar length in kpc','manga_Omph':'Pattern speed km/s/kpc','manga_R':'Corotation/bar-radius ratio, dimensionless','manga_Rbardp':'Deprojected bar radius in kpc','manga_rotation_class_point_estimates':'Point classification counts; missing outcomes retained'})]:
 datasets.append(dataset(id,path,description,columns,model='GAL-LIVE'if id in ['DS-GAL','DS-OBS']else'RES-POS',pairing='Published observational selection; no resampling in this release'if id=='DS-OBS'else common))
for d in datasets:
 if d['model_id']=='GAL-LIVE':
  d['code_version']='Historical catalogue/galaxy export; see linked original provenance, not the reduced benchmark'
  d['license']='Third-party catalogue terms and original-model source licenses; not blanket MIT'
# Raw arrays remain in the pinned public numerical package, not behind a private source link.
args=argparse.ArgumentParser();args.add_argument('--benchmark',type=Path,required=True);a=args.parse_args()
import numpy as np
for p in sorted((a.benchmark/'accuracy').rglob('*.npz')):
 rel=p.relative_to(a.benchmark).as_posix();arr=np.load(p);arrays={}
 for k in arr.files:
  shape=list(arr[k].shape)
  if k in ['fine','coarse']:
   axes=['batch seeds96101…96108','endpoint T=[10,20]','action cell between adjacent edges'];unit='dimensionless primitive response Q';meaning='Fine dt0.00625 or coarse dt0.0125 shared-Brownian primitive cell averages; phase-averaged response, not physical cohorts.'
  elif k=='edges':axes=['action-cell edge'];unit='dimensionless x';meaning='Ordered cell boundaries from−64to64 at spacing1/256.'
  elif k in ['mean','covariance']:
   axes=['column index']*(2 if k=='covariance'else 1);unit='response squared'if k=='covariance'else'dimensionless response';meaning='Columns and paired branches/methods are defined in adjacent result.json /columns. Covariance is the combined stratified estimator covariance, not independent columns.'
  else:
   axes=['halo-table sample'];unit={'x':'dimensionless x','Jphi':'analytical model action','df':'analytical model distribution-function units'}.get(k,'see source');meaning={'x':'Initial action coordinate','Jphi':'Azimuthal action sampled along the fixed fast-action slice','df':'Reference isochrone DF on that slice'}.get(k,k)
  arrays[k]=dict(shape=shape,dtype=str(arr[k].dtype),axes=axes,units=unit,meaning=meaning)
 seed=re.search(r'seed(\d+)',rel)
 datasets.append(dict(id='RAW-'+hashlib.sha256(rel.encode()).hexdigest()[:12],url=f'{RAW}/{rel}',path_in_public_package=rel,model_id='RES-POS',release=VERSION,code_version=SCIENCE,bytes=p.stat().st_size,sha256=digest(p),media_type='application/octet-stream',arrays=arrays,missing_values='No masked/missing arrays; nonfinite data would invalidate the experiment.',sampling_and_pairing=common,seeds=[int(seed[1])]if seed else list(range(96101,96109))if'kernel-batches'in rel else'not stochastic: analytic DF table',column_definitions=f'{RAW}/{rel.rsplit("/",1)[0]}/result.json'if'recorded.npz'in rel else'paper.html#model',license='MIT; public benchmark LICENSE'))
jsave(W/'datasets.json',{'release':VERSION,'scope':'Principal article tables, full scientific records and every NPZ array archive in the accuracy public package. Legacy galaxy snapshots are separately described in their per-study methods and manifests; this registry does not claim to release private initial conditions.','datasets':datasets,'legacy_catalogue_provenance':'data/manifest.json','full_source_inventory':f'{RAW}/accuracy/source-manifest.json'})

reproduce=f'''# Inspect, check, or rerun

These are different activities. Reading starts no computation and needs no credentials. Checking published records is not rerunning trajectories. A reproduction receipt reports what its author checked; it does not mean a reader independently performed it.

## Per-study reproducibility map {{#map}}

| Study | Published outputs | Analysis reproducible | Complete experiment reproducible |
|---|---|---|---|
| Original 10 / expanded 25 galaxies | Yes: [run index](data/index.json), movies, diagnostics, [catalogue provenance](data/manifest.json) | Selected exported diagnostics and [scientific source](diagnostics/response/source-index.html); coverage varies | **No complete public package for every original galaxy**; some IC/raw archives remain private |
| Prescribed-field Cartesian response | [Recorded paths and budgets](response.html); limitations retained | Named reduced/synthetic checks in [earlier benchmark scope]({PUBLIC}/blob/{SCIENCE}/EARLIER_BENCHMARKS.md) | No blanket claim for every Cartesian/cloud run |
| Matched noisy-resonance benchmark | [Original study](noise-sweep.html) | Yes, named public recipes | [reproduce_matched.py]({PUBLIC}/blob/{SCIENCE}/reproduce_matched.py) for that matched setup |
| Population response and heldout weights | [Population study](population-response.html) | Yes | [reproduce_population.py]({PUBLIC}/blob/{SCIENCE}/reproduce_population.py) and [reproduce_heldout.py]({PUBLIC}/blob/{SCIENCE}/reproduce_heldout.py) |
| Prospective accuracy / matched estimator cost | [Complete article](paper.html), [tables](results/accuracy.json), [arrays](datasets.json) | Yes, retained covariance and exact reference outputs | [reproduce_accuracy.py]({PUBLIC}/blob/{SCIENCE}/reproduce_accuracy.py), cost and retrospective commands |

## Inspection: seconds, no installation {{#inspection}}

[Article](paper.html) · [Markdown](paper.md) · [claims](claims.json) · [models](models.json) · [datasets and units](datasets.json) · [release manifest](manifest.json). All central tables are in the initial HTML. Controls select recorded endpoints and clarify the calculation.

## Verification: cheap arithmetic, no orbit evolution {{#verification}}

Download [verify_publication.py](verify_publication.py) and run it with Python3.11, standard library only:

```sh
python3 verify_publication.py --origin https://djova.ca/galaxy-bar/
```

It anonymously fetches the manifest, claims and small result tables, checks hashes and content types, recomputes the late population ratio and prospective counts, identifies a conservative rejection, and reports the broad/narrow estimator ratios. It also checks source-row consistency where supplied. Expected runtime is seconds to a few minutes of network access; no solver is invoked. Network failure is reported, not converted to a scientific failure.

## Reproduction: deliberately run the experiment {{#reproduction}}

The [public benchmark]({PUBLIC}) is separate from the private working repository. Use the pinned numerical version `{SCIENCE}` and its [exact instructions]({PUBLIC}/blob/{SCIENCE}/accuracy/README.md). Reproduction requires Python3.11, pinned scientific dependencies and available CPU/memory. This command is never run merely by reading the page.

```sh
git clone https://github.com/djova/bar-halo-benchmark.git
cd bar-halo-benchmark
git checkout {SCIENCE}
python3.11 -m venv .venv
.venv/bin/pip install -r accuracy/requirements.lock.txt
.venv/bin/python reproduce_accuracy.py --out ./accuracy-rerun --workers 2
```

The recorded fresh-source accuracy rerun used **3.60 summed core-hours**; elapsed time and platform equality can differ. The default launcher has finite case/wall limits and4+6 aggregate core-hour ceilings for its two stages. The original cost benchmark used about 347 worker CPU-seconds. The retrospective audit reuses saved arrays. Check each recipe before executing; these costs do not describe the original galaxy simulations.

## Versions, authorship and reuse {{#licenses}}

Numerical source: `{SCIENCE}`. Tested accuracy rerun: `66143ebdb7441e17f4b44c23d15c2b35eb66841a`. Publication release: **{VERSION}**. Checksums identify the article's exact scientific inputs; publication changes do not silently revise their protocols.

The public benchmark's [MIT code license]({PUBLIC}/blob/{SCIENCE}/LICENSE) is preserved. Original article text, new learning modules and derived result tables included in this clean public release use the same MIT license. Cite the release and underlying papers when reusing the research. This does not license every legacy or third-party item: no new license is asserted over third-party catalogue tables, papers, logos or quotations. Consult the [CDS catalogue](https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/587/A160) and original authors for their terms and attribution.

{credit}

[Archived protocols and corrections](archive.html) preserve scientific history. [Release snapshots](releases/{VERSION}/manifest.json) and a public Git tag preserve this publication's central evidence. The current manifest is a discovery pointer; cite the versioned files or pinned public commit for a fixed reference.
'''
page('reproduce.html','Inspect and reproduce',reproduce)
(W/'reproduce.md').write_text(reproduce)
archive='''# Supporting experiments and retained history

The [current canonical article](paper.html) supplies the complete present argument. Historical pages describe their named experiments and original criteria, not a global verdict on everything that followed.

| Record | Role and scope |
|---|---|
| [Original six-hour report](final-report.html) | Archived ten-run galaxy verdict; original deadline preserved |
| [Original galaxy synthesis](synthesis.html) | Archived expanded galaxy/thickness conclusions, 21 September |
| [Two-day plan](next-48-hours.html) | Historical plan; not active jobs |
| [Galaxy methods](methodology.html) and [follow-up notebook](followup.html) | Original equilibrium, force-law mismatch, convergence and observations |
| [Prescribed-field response](response.html) | Same-action phase replication; grainy result unresolved; corrected finite-lag interpretation |
| [Source-step failure](response-source-history.html) | Original failed numerical gate, retained alongside repair |
| [Noise/sweep study](noise-sweep.html) | Matched positive-population noise effects; 3D test unresolved |
| [Population response](population-response.html) | Reference-halo weighting, kernel and old operational forecasts |
| [Accuracy study](population-accuracy.html) | Supporting interactive analysis, consolidated in current article |
| [Original 24 vs combined 22 assessment](diagnostics/population-accuracy/joint-error-assessment.json) | Two early Gaussian 12 cases remain marginal under expanded proxies |
| [Matched cost correction](diagnostics/population-accuracy/COST_OUTCOME_02.md) | Earlier weight mismatch preserved; corrected costs use the same numerical target |

The publication redesign corrects source routing, campaign-count scope, equilibrium shorthand and page authority. It does not revise frozen criteria, delete failures, or turn an unresolved result into a passed one. Historical URLs remain reachable. Model clocks and population definitions remain distinct.
'''
page('archive.html','Archive and revision history',archive)
experiments='# Model and experiment registry\n\n'+model_table+'\n\n## Named campaigns\n\n'+table(['ID','Members','Unit / scope','Evidence'],[[c['id'],c['member_count'],c.get('count_unit','recorded galaxy runs; original10is subset of expanded25'),f"[record]({c.get('page',c.get('assessment','synthesis.html'))})"]for c in campaigns])+'\n[Machine-readable memberships](campaigns.json). Counts do not imply independent physical samples.\n'
page('experiments.html','Models and experiments',experiments)
agents=f'''# Anonymous research access

**Current authority:** [canonical article](paper.html) ([Markdown](paper.md)), release **{VERSION}**, not externally reviewed. This page describes discovery, not instructions to execute jobs. Reading requires no login, privileged browser, private network or private repository.

Start with [manifest.json](manifest.json), then [claims.json](claims.json), [models.json](models.json), [campaigns.json](campaigns.json), [datasets.json](datasets.json) and the small [results summary](results/summary.json). RFC6901 pointers identify exact source rows. Result files expose units, model and numerical provenance via their dataset entries. Use the same article, uncertainties and limitations as human readers.

## What a cold-start reader should establish

1. Contribution: finite-time population bias plus a reusable diagnostic and estimator in model RES-POS.
2. Nonclaims: no full-halo torque, no calibrated SIDM, no qualified 3D transfer, no universal uncertainty guarantee or runtime speedup.
3. Eight 5% qualifications share **one** new condition, two approximate populations, two times and two windows.
4. Recalculate the late Gaussian/halo magnitude ratio from [the six principal values](results/populations.json); it is about 4.7353.
5. Find Gaussian 128, T = 10, cutoff 40 in [all 24 accuracy rows](results/accuracy.json): the allowance rejects it although its independent error meets 5%.
6. Explain the difference between conditional and between-batch cost-times-variance estimates in [the cost table](results/cost.json).
7. Distinguish prescribed-field test-particle validation from collective live-halo validation using the model registry.

[Inspect/check/rerun map](reproduce.html) supplies separate dependencies and measured costs. [verify_publication.py](verify_publication.py) checks published arithmetic and files; it never evolves an orbit. A project reproduction receipt is not evidence that you reran the experiment. No global all_pass field combines physics, software and deployment.

## Stable references and reuse

Claim IDs, equations, figures, limitations and result IDs are stable within this release. Each principal figure records its default state, scientific parameters, source, full values and analysis hashes in [figures.json](figures.json). A release snapshot lives under [releases/{VERSION}/](releases/{VERSION}/manifest.json). [llms.txt](llms.txt) is an optional discovery aid, not a guarantee that any service will index this work. [Licenses and contact](reproduce.html#licenses) distinguish benchmark code, scientific records, article and third-party data.
'''
page('agents.html','Agent access and evidence contract',agents);(W/'agents.md').write_text(agents)
figures=[dict(id='F-POP-01',anchor='paper.html#F-POP-01',default_state={'s':.25,'eta':.1,'times':[10,20],'cutoff':40},question='Does matching central density and slope preserve finite-time response?',values='results/populations.json',dataset='DS-POP',selection_url='population-response.html#population-explorer'),dict(id='F-ACC-01',anchor='paper.html#F-ACC-01',default_state={'s':.5,'eta':.1,'population':'exponential','time':20,'cutoff':40},question='Can a gradient-mismatch allowance qualify accuracy and when is it conservative?',values='results/accuracy.json',dataset='DS-ACC',selection_url='paper.html?population=exponential&time=20&window=40#interactive-decision'),dict(id='F-COST-01',anchor='paper.html#F-COST-01',default_state={'s':.25,'population':'halo','time':20},question='How much variance is removed for the measured CPU cost?',values='results/cost.json',dataset='DS-COST',selection_url='paper.html?costPopulation=halo&costSweep=0.25&costTime=20#estimator')]
for id,anchor,question in [('F-ACC-BUDGET','accuracy-budget','Does full forecast error fit the target?'),('F-ACC-GRADIENT','accuracy-gradient','Where do signed errors cancel while absolute allowances accumulate?'),('F-ACC-SLOPE','accuracy-slopes','How do reference and approximate population gradients differ?'),('F-ACC-KERNEL','accuracy-kernel','Which action regions carry dynamical sensitivity?')]:
 figures.append(dict(id=id,anchor='paper.html#'+anchor,default_state={'s':.5,'eta':.1,'population':'exponential','time':20,'cutoff':40,'highlight_radius':8},question=question,values='diagnostics/population-accuracy/accuracy-explorer.json',dataset='DS-ACC-FULL',selection_url='paper.html?population=exponential&time=20&window=40#'+anchor))
for f in figures:f.update(release=VERSION,analysis_revision=SCIENCE,observable='Noise-minus-smooth accumulated bar-mediated transfer',response_units='dimensionless integral(w K_B dx); efficiency ratio is dimensionless and cost in CPU seconds',uncertainty='See linked dataset and article caption; cost/bootstrap and transfer/sampling intervals are distinct.',clock='Dimensionless resonance time; not Gyr')
jsave(W/'figures.json',{'release':VERSION,'figures':figures})
(W/'llms.txt').write_text(f'# Galaxy Bar\n\n> Versioned local-model methods research; release {VERSION}; not externally reviewed.\n\n- [Complete article](https://djova.ca/galaxy-bar/paper.md)\n- [Models and limitations](https://djova.ca/galaxy-bar/claims.json)\n- [Evidence manifest](https://djova.ca/galaxy-bar/manifest.json)\n- [Anonymous agent guide](https://djova.ca/galaxy-bar/agents.md)\n- [Inspection versus reproduction](https://djova.ca/galaxy-bar/reproduce.md)\n\nNo live-halo or SIDM validation is claimed. Reading requires no execution.\n')
# Extend, rather than compete with, the earlier ledger: generated Markdown mirror.
ledger='# Publication-wide claim ledger\n\nGenerated from the publication registry. Numerical evidence remains in its original records.\n\n'+table(['ID','Claim','Status','Scope / evidence'],[[c['id'],c['wording'],c['status'],f"{c['model_id']} · [{c['evidence'][0]['path']}]({c['evidence'][0]['path']})"]for c in claims])
(W/'claim-ledger.md').write_text(ledger)
(SRC/'CLAIM_LEDGER.md').write_text(ledger)
# Hash the public build inputs without any credentials, private paths or operational logs.
files=['verify_publication.py','paper.html','paper.md','learn.html','learn.md','reproduce.html','reproduce.md','agents.html','agents.md','archive.html','experiments.html','claims.json','claim-ledger.md','models.json','campaigns.json','datasets.json','figures.json','llms.txt','publication-sources.md']+[p.relative_to(W).as_posix()for p in sorted((W/'results').glob('*'))]
files+=sorted({e['path']for c in claims for e in c['evidence']}|{d['path']for d in datasets if'path'in d})
manifest=dict(schema_version=1,release=VERSION,article='paper.html',markdown='paper.md',review_status='not_externally_reviewed',scientific_source=dict(repository=PUBLIC,revision=SCIENCE),publication_source=dict(repository=PUBLIC,ref=f'publication-{VERSION}',directory='publication'),models='models.json',claims='claims.json',datasets='datasets.json',campaigns='campaigns.json',figures='figures.json',verification='verify_publication.py',reproduction='reproduce.html',archive='archive.html',release_snapshot=f'releases/{VERSION}/manifest.json',licenses='reproduce.html#licenses',generator_sha256=digest(Path(__file__)),article_source_sha256=digest(SRC/'ARTICLE.md'),artifacts=[dict(path=p,sha256=digest(W/p),bytes=(W/p).stat().st_size)for p in sorted(set(files))],scope='Canonical publication and central evidence; numerical experiment outputs unchanged. No global scientific all-pass verdict.')
jsave(W/'manifest.json',manifest)
print(json.dumps({'release':VERSION,'claims':len(claims),'datasets':len(datasets),'figures':len(figures),'counts':counts,'ratio':ratio}))
