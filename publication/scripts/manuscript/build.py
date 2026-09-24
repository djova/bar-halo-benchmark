#!/usr/bin/env python3
"""Typeset existing canonical science; no simulation or new numerical inference.
Run with --pandoc PATH --tectonic PATH. Requires Pandoc 3.11 and Tectonic 0.17.0
(or compatible versions). Generated LaTeX can also be built with latexmk -pdf.
"""
import argparse,hashlib,json,re,shutil,subprocess,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'web';SRC=ROOT/'research/publication';M=SRC/'mnras'
EXPORT='2026-09-24.2'; SCIENCE_RELEASE='2026-09-24.1'
BASE='https://djova.ca/galaxy-bar/'
def load(name):return json.loads((W/name).read_text())
def raw(s):return '\n\n```{=latex}\n'+s+'\n```\n\n'
def num(v,d=6):return f'{v:.{d}g}'
def label(s):
 return {'halo':'Halo','exponential':'Exponential','gaussian':'Gaussian $\\sigma=8$','gaussian8':'Gaussian 8','gaussian32':'Gaussian 32','gaussian128':'Gaussian 128','gaussian512':'Gaussian 512','stress1':'Gaussian 1','stress0.125':'Gaussian 1/8','stress0.015625':'Gaussian 1/64'}[s]
def table(caption,name,heads,rows,align):
 return '\\begin{table*}\n\\centering\n\\caption{'+caption+'}\\label{'+name+'}\n\\small\n\\setlength{\\tabcolsep}{4pt}\n\\begin{tabular}{'+align+'}\n\\toprule\n'+' & '.join(heads)+r' \\'+'\n\\midrule\n'+'\n'.join(' & '.join(map(str,r))+r' \\' for r in rows)+'\n\\bottomrule\n\\end{tabular}\n\\end{table*}'
p=argparse.ArgumentParser();p.add_argument('--pandoc',default='pandoc');p.add_argument('--tectonic',default='tectonic');a=p.parse_args()
out=W/'downloads'/('mnras-'+EXPORT);out.mkdir(parents=True,exist_ok=True)
build=ROOT/'build'/('mnras-'+EXPORT);build.mkdir(parents=True,exist_ok=True)
for f in ['mnras.cls','mnras.bst']:shutil.copyfile(M/'vendor/mnras'/f,build/f)
shutil.copyfile(M/'references.bib',build/'references.bib')
source=(SRC/'ARTICLE.md').read_text();pop=load('results/populations.json')['rows'];acc=load('results/accuracy.json')['rows'];cost=load('results/cost.json')['rows'];claims=load('claims.json')
ratio=abs(next(r['response']for r in pop if r['population']=='gaussian'and r['time']==20)/next(r['response']for r in pop if r['population']=='halo'and r['time']==20))
source=source.replace('{{RATIO}}',f'{ratio:.6f}')
abstract=source.split('## Abstract {#abstract}\n\n',1)[1].split('\n[Learn the foundations]',1)[0].replace('\n\n',' ')
body='## '+source.split('\n## ',2)[2]
body=body.replace('{{MODELS}}','\n\n'.join('**'+m['id']+' — '+m['title']+'.** '+m['evolves'].rstrip('.')+'. '+m['supports']+'. '+m['excludes']+'. Clock: '+m['clock']+'.'for m in load('models.json')['models']))
for c in claims['claims']:
 body=body.replace('{{CLAIM:'+c['id']+'}}','**'+c['id']+'.** '+c['wording'])
body=body.replace('{{LIMITATIONS}}','\n\n'.join('**'+r['id']+'.** '+r['text']for r in claims['limitations']))
body=body.replace('{{POPULATION_TABLE}}',raw(table(
 r'Original population comparison (F-POP-01). Dimensionless noise-minus-smooth accumulated transfer at $s=0.25$, $\eta=0.1$ and cutoff 40. Pointwise 95 per cent intervals use eight independent batches. All six rows pass the declared numerical/window checks. Central density is fixed; weights are not normalized to unit mass.',
 'tab-pop',['Population','$T$','$\\mathcal R$','95 per cent lower','95 per cent upper'],
 [[label(r['population']),int(r['time']),num(r['response'],9),num(r['ci95_low'],9),num(r['ci95_high'],9)]for r in pop],'lrrrr')))
# Move full numeric records to appendices; use existing figures as the main display.
body=body.replace('{{ACCURACY_TABLE}}',r'Complete values are in Appendix `\ref{app-accuracy}`{=latex}; the interactive article provides the downloadable unrounded records.')
body=body.replace('{{COST_TABLE}}',r'Complete values are in Appendix `\ref{app-cost}`{=latex}, with paired intervals for every recorded endpoint.')
body=body.replace('### Interrogate the decision {#interactive-decision}\n\n{{ACCURACY_INTERACTIVE}}', '[Interrogate a recorded accuracy decision in the interactive article](paper.html#interactive-decision).')
body=body.replace('{{COST_INTERACTIVE}}','[Explore matched estimator costs in the interactive article](paper.html#estimator).')
body=body.replace('{{REVISION}}','This PDF export, '+EXPORT+', typesets the scientific article '+SCIENCE_RELEASE+'. It carries the editorial revision in both media; the numerical evidence and historical criteria are unchanged. Earlier releases remain archived. The [interactive article](paper.html) provides the original navigation, selection controls and versioned claim registry.')
body=body.replace('{{BIBLIOGRAPHY}}','')
# Cite scholarly sources through the MNRAS author-year bibliography.
cites={'https://arxiv.org/abs/2208.03855':'Hamilton2023','https://arxiv.org/abs/2305.00022':'Chiba2023','https://doi.org/10.1111/j.1365-2966.2006.10506.x':'OgilvieLubow2006','https://arxiv.org/pdf/2010.07321':'Elbers2021','https://arxiv.org/abs/2511.11804v2':'Dattathri2026'}
for url,key in cites.items():
 body=re.sub(r'\[[^\]]+\]\('+re.escape(url)+r'\)',lambda m:'`\\citet{'+key+'}`{=latex}'+(' (sections 2–2.3)'if key=='Elbers2021'else''),body)
# Preserve equations and scientific identifiers, while making them native LaTeX.
def equations(s):
 s=re.sub(r'<div class="equation-label" id="([^"]+)">.*?</div>\s*```math\n(.*?)\n```',lambda m:raw('\\begin{equation}\\label{'+m[1]+'}\n'+m[2]+'\n\\end{equation}'),s,flags=re.S)
 return s.replace('δf',r'\(\delta f\)').replace('η',r'\(\eta\)')
body=equations(body).replace('(sections 2–2.3), use','(sections 2–2.3) use')
# Figure caption is the actual article caption, not a newly inferred interpretation.
figs=[('POP','population-comparison','F-POP-01'),('ACC','population-accuracy','F-ACC-01'),('COST','estimator-efficiency','F-COST-01')]
def pandoc(text):
 return subprocess.check_output([a.pandoc,'--from=markdown+tex_math_single_backslash+raw_attribute','--to=latex','--top-level-division=section','--wrap=none'],input=text,text=True)
def links(s):
 return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:m[0]if re.match(r'https?://',m[2])else '['+m[1]+']('+BASE+(m[2]if not m[2].startswith('#')else'paper.html'+m[2])+')',s)
for key,filename,fid in figs:
 cap=re.search(r'\*\*Figure '+fid+r'\.\*\* (.*?)(?:\n\n|$)',body,re.S).group(1)
 body=re.sub(r'\*\*Figure '+fid+r'\.\*\* .*?(?:\n\n|$)','',body,flags=re.S)
 cap=cap.replace('[Complete table](#table-accuracy)',r'Table `\ref{tab-acc}`{=latex}').replace('[All recorded values](#table-cost)',r'Tables `\ref{tab-cost}`{=latex} and `\ref{tab-consistency}`{=latex}')
 cap=pandoc(links(equations(cap))).strip()
 shutil.copyfile(W/'diagnostics/population-accuracy'/(filename+'.png'),build/(filename+'.png'))
 body=body.replace('{{FIG-'+key+'}}',raw('\\begin{figure*}\n\\centering\n\\includegraphics[width=\\textwidth]{'+filename+'.png}\n\\caption{'+fid+'. '+cap+'}\\label{'+fid+'}\n\\end{figure*}'))
assert '{{'not in body
# Main source headings are level 2 under the web title; lift them one level.
body=re.sub(r'^(#{2,}) ',lambda m:m[1][1:]+' ',body,flags=re.M)
latex=pandoc(links(body))
# Split the long remainder identity without scaling its mathematics.
latex=latex.replace('\\int w(x)\\,\\mathbb E[B]\\,\\mathrm dx\n&=-\\int\\mathbb E\\!\\left[F(x+B)-F(x)-w(x)B\\right]\\,\\mathrm dx.',
 '\\int w(x)\\,\\mathbb E[B]\\,\\mathrm dx\n&=-\\int\\mathbb E\\!\\left[R_w(x,B)\\right]\\,\\mathrm dx,\\\\\nR_w(x,B)&=F(x+B)-F(x)-w(x)B.')
accrows=[]
for r in acc:
 status=('Q'if r['qualified_5_percent']else'NQ')+'/'+{'supported':'in','contradicted':'out','inconclusive':'?'}[r['independent_assessment']]
 accrows.append([label(r['population'])+(' (ref.)'if r['self_reference']else''),int(r['time']),r['cutoff'],num(r['forecast']),num(r['independent_response']),num(r['full_allowance']),num(r['target']),status])
app=raw('\\clearpage\n\\onecolumn\n\\makeatletter\n\\def\\fps@table{!h}\n\\makeatother\n\\appendix\n\\renewcommand{\\theHtable}{\\thesection.\\arabic{table}}\n\\section{Complete accuracy records}\\label{app-accuracy}')
app+='At $s=0.5$ and $\\eta=0.1$, Q/NQ denotes the advance qualification; in/out denotes whether the independent comparison supports accuracy within 5 per cent or lies outside it. The 24 rows contain twenty candidates and four halo references; they share one dynamical condition. Tables report rounded values; the public JSON/CSV retains full precision.\n'
app+=raw(table(r'Prospective operational decisions (PA-ACC-01, PA-ACC-02). $c$ is the physical window cutoff, $\widehat{\mathcal R}$ the kernel forecast, $\mathcal R_{\rm ind}[v]$ independent evolution of the indicated population, $A$ the full allowance and $\epsilon$ the frozen absolute 5 per cent target. The in/out assessment compares the forecast with the independently evolved halo, with the supplied numerical proxy; it is not a general confidence guarantee.', 'tab-acc',['Population','$T$','$c$','$\\widehat{\\mathcal R}$','$\\mathcal R_{\\rm ind}[v]$','$A$','$\\epsilon$','Decision'],accrows,'lrrrrrrl'))
# Intrinsic errors, not conflated with forecast discrepancy.
app+=raw(table(r'Independent intrinsic population error and forecast discrepancy. $e=\mathcal R_{\rm ind}[v]-\mathcal R_{\rm ind}[h]$; $p_e$ is its numerical-refinement proxy; $\delta=\widehat{\mathcal R}[v]-\mathcal R_{\rm ind}[h]$; $p_h$ is the halo proxy. All quantities are dimensionless accumulated response differences. Proxies are not sampling intervals or proved bounds.', 'tab-errors',['Population','$T$','$c$','$e$','$p_e$','$\\delta$','$p_h$'],[[label(r['population']),int(r['time']),r['cutoff'],num(r['intrinsic_population_error']),num(r['intrinsic_error_proxy']),num(r['forecast_minus_independent_halo']),num(r['independent_halo_proxy'])]for r in acc],'lrrrrrr'))
app+=raw('\\clearpage\n\\section{Complete matched estimator records}\\label{app-cost}')
app+='These are cost-times-variance ratios under the specified matched workload, not direct simulation speedups. All 24 endpoints retain their numerical values and paired method-consistency intervals. Gaussian stress labels give the width $\\sigma$.\n'
app+=raw(table(r'Matched estimator costs and variance ratios (EST-01). $C_{\rm raw}$ and $C_{\rm rem}$ are mean CPU seconds per accounted batch; $V_C$ is the conditional raw/remainder cost-times-variance ratio; brackets give its whole-batch bootstrap interval; $V_B$ uses between-batch variance. All $T=10$ endpoints carry the same full $T=20$ workload cost.', 'tab-cost',['Population','$s$','$T$','$C_{\\rm raw}$','$C_{\\rm rem}$','$V_C$','Bootstrap interval','$V_B$'],[[label(r['population']),r['s'],int(r['time']),num(r['raw_cpu_seconds'],5),num(r['remainder_cpu_seconds'],5),num(r['cost_times_variance_ratio'],6),'['+num(r['bootstrap_low'],5)+', '+num(r['bootstrap_high'],5)+']',num(r['between_batch_ratio'],6)]for r in cost],'lrrrrrlr'))
app+=raw(table(r'Paired raw-minus-remainder method comparison. Intervals are pointwise 95 per cent sampling intervals, not simultaneous tests across all 24 rows. A retained exclusion of zero is a multiple-comparison flag, not by itself proof of estimator bias.', 'tab-consistency',['Population','$s$','$T$','Raw minus remainder','95 per cent lower','95 per cent upper','Contains zero'],[[label(r['population']),r['s'],int(r['time']),num(r['raw_minus_remainder']),num(r['raw_difference_ci_low']),num(r['raw_difference_ci_high']),'yes'if r['contains_zero']else'no']for r in cost],'lrrrrrl'))
ack=r'''
\section*{Acknowledgements and disclosure}
This manuscript typesets the existing Galaxy Bar interactive publication \citep{GalaxyBar2026}. The human project maintainer is djova; analysis, software and exposition were developed with AI assistance. No institutional affiliation, independent scientific review or journal endorsement is asserted. The MNRAS class and BibTeX style are supplied by the Royal Astronomical Society under the LaTeX Project Public License.
\section*{Data availability}
The article, protocols, numerical records and executable benchmark are public at \url{https://github.com/djova/bar-halo-benchmark}. The interactive article is \url{https://djova.ca/galaxy-bar/paper.html}. Scientific evidence is pinned by publication release 2026-09-24.1. This PDF is export 2026-09-24.2; it does not report a new simulation. Complete derivations and data definitions are linked from the article. The benchmark's MIT licence applies as recorded there; third-party works retain their own terms.
\bibliographystyle{mnras}
\bibliography{references}
'''
tex=(M/'preamble.tex').read_text()+'\n\\begin{abstract}\n'+pandoc(abstract).strip()+'\n\\end{abstract}\n\\begin{keywords}\nmethods: numerical -- galaxies: kinematics and dynamics -- galaxies: haloes\n\\end{keywords}\n'+latex+ack+pandoc(app).replace('\\begin{table*}', '\\begin{table}').replace('\\end{table*}', '\\end{table}')+'\n\\clearpage\n\\end{document}\n'
(build/'galaxy-bar-mnras.tex').write_text(tex)
# Use a fixed clock for reproducible document metadata.
env=dict(os.environ,SOURCE_DATE_EPOCH='1790208000',FORCE_SOURCE_DATE='1')
subprocess.run([a.tectonic,'--keep-logs','--keep-intermediates','galaxy-bar-mnras.tex'],cwd=build,env=env,check=True)
artifact_names=['galaxy-bar-mnras.pdf','galaxy-bar-mnras.tex','references.bib']+[f+'.png'for _,f,_ in figs]
for name in artifact_names:
 shutil.copyfile(build/name,out/name)
# Public checksum/provenance excludes local machine paths and build logs.
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
inputs=[SRC/'ARTICLE.md',M/'preamble.tex',M/'references.bib']+[W/'results'/(n+'.json')for n in ['populations','accuracy','cost']]+[W/'diagnostics/population-accuracy'/(f+'.png')for _,f,_ in figs]
manifest={'export':EXPORT,'scientific_release':SCIENCE_RELEASE,'status':'unreviewed; not submitted to or accepted by MNRAS','template':{'name':'mnras','version':'3.2','source':'https://ctan.org/pkg/mnras','license':'LPPL-1.3-or-later'},'tools':{'pandoc':'3.11','tectonic':'0.17.0'},'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)}for p in inputs],'artifacts':[{'path':name,'bytes':(out/name).stat().st_size,'sha256':sha(out/name)}for name in artifact_names],'scope':'Typeset existing canonical science, figures and complete records; no new experiment.'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'pdf':str(out.relative_to(ROOT)/'galaxy-bar-mnras.pdf'),'bytes':(out/'galaxy-bar-mnras.pdf').stat().st_size}))
