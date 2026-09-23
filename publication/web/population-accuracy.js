const $=id=>document.getElementById(id);
const ns='http://www.w3.org/2000/svg';
const labels={halo:'Reference halo',exponential:'Slope-matched exponential',gaussian8:'Gaussian σ = 8',gaussian32:'Gaussian σ = 32',gaussian128:'Gaussian σ = 128',gaussian512:'Gaussian σ = 512'};
const fmt=v=>Number.isFinite(v)?v===0?'0':Math.abs(v)<.001?v.toExponential(3):Math.abs(v)<1?v.toFixed(6):v.toLocaleString('en-US',{maximumFractionDigits:3}):'unavailable';
const el=(tag,attrs={},text)=>{const n=document.createElementNS(ns,tag);for(const [k,v]of Object.entries(attrs))n.setAttribute(k,v);if(text!==undefined)n.textContent=text;return n;};
const add=(svg,tag,attrs,text)=>svg.appendChild(el(tag,attrs,text));
let data,current;
function svgSetup(id,height){const svg=$(id),w=Math.max(240,svg.clientWidth);svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${w} ${height}`);return [svg,w];}
function line(svg,x1,y1,x2,y2,color,dash){add(svg,'line',{x1,y1,x2,y2,stroke:color,'stroke-width':1.4,...(dash?{'stroke-dasharray':dash}:{})});}
function budget(row){
 const f=row.forecast,a=row.independent,target=f.five_percent_absolute_target;
 const actual=a?Math.abs(a.forecast_minus_independent_halo):null,unc=a?.independent_halo.numerical_proxy||0;
 const values=[f.approximation_allowance,f.combined_response_allowance,actual];
 const [svg,w]=svgSetup('accuracy-budget',280),left=12,right=w-18,max=1.12*Math.max(target,...values.filter(v=>v!==null),actual===null?0:actual+unc,1e-15),x=v=>left+(right-left)*v/max;
 add(svg,'title',{},'Absolute errors and the frozen five-percent target');
 const descriptions=['Population mismatch','Full predicted error','Independent discrepancy'];
 descriptions.forEach((label,i)=>{
  const y=46+75*i;add(svg,'text',{x:left,y:y-11},label);
  line(svg,left,y+12,right,y+12,'#293b50');
  if(values[i]===null){add(svg,'text',{x:left,y:y+18},'Independent result pending');return;}
  add(svg,'rect',{x:left,y,width:Math.max(0,x(values[i])-left),height:24,rx:3,fill:i===0?'#f3c785':i===1?'#ac8ade':'#83caff'});
  if(i===2){line(svg,x(Math.max(0,actual-unc)),y+12,x(actual+unc),y+12,'#edf2f6');for(const v of [Math.max(0,actual-unc),actual+unc])line(svg,x(v),y+5,x(v),y+19,'#edf2f6');}
  add(svg,'text',{x:right,y:y-11,'text-anchor':'end'},fmt(values[i]));
 });
 line(svg,x(target),24,x(target),235,'#a5d9bf','4 4');
 add(svg,'text',{x:left,y:255},`5% target = ${fmt(target)}`);add(svg,'text',{x:right,y:275,'text-anchor':'end'},'Absolute response units');
 $('accuracy-budget-copy').textContent=`The full predicted allowance is ${fmt(f.combined_response_allowance)}: population error ${fmt(f.approximation_allowance)} plus the approximate response’s sampling/numerical allowance ${fmt(f.approximate.total_allowance)}. The frozen five-percent target is ${fmt(target)}. ${a?'The independent error bar adds the measured halo numerical proxy; it is not a new statistical sample.':'Independent evolution is still pending.'}`;
}
function gradient(row){
 const p=row.plot,cut=row.forecast.cutoff,r=Number($('accuracy-radius').value),bins=[];
 for(let i=0;i<p.edges.length-1;i++)if(p.edges[i]>=-cut&&p.edges[i+1]<=cut)bins.push(i);
 const selected=bins.filter(i=>p.edges[i]>=-r&&p.edges[i+1]<=r);
 const effective=selected.length?Math.max(...selected.map(i=>Math.abs(p.edges[i+1]))):0;
 $('accuracy-radius-value').textContent=fmt(effective);
 const [svg,w]=svgSetup('accuracy-gradient',280),left=58,right=w-12,top=25,bottom=232;
 const extent=1.1*Math.max(...bins.flatMap(i=>[Math.abs(p.signed_density[i]),p.allowance_density[i]]),1e-15);
 const x=v=>left+(right-left)*(v+cut)/(2*cut),y=v=>(top+bottom)/2-v/extent*(bottom-top)/2;
 add(svg,'title',{},'Gradient-coordinate contributions to signed error and absolute allowance');
 if(selected.length)add(svg,'rect',{x:x(-effective),y:top,width:x(effective)-x(-effective),height:bottom-top,fill:'#83caff',opacity:.08});
 for(const v of [-extent/1.1,0,extent/1.1]){line(svg,left,y(v),right,y(v),'#293b50');add(svg,'text',{x:left-5,y:y(v)+4,'text-anchor':'end'},v===0?'0':v.toExponential(1));}
 const steps=key=>bins.flatMap(i=>[[x(p.edges[i]),y(p[key][i])],[x(p.edges[i+1]),y(p[key][i])]]);
 const path=points=>points.map(([a,b],i)=>(i?'L':'M')+a.toFixed(2)+','+b.toFixed(2)).join(' ');
 const orange=steps('allowance_density');
 add(svg,'path',{d:`M${x(-cut)},${y(0)} ${path(orange).replace(/^M/,'L')} L${x(cut)},${y(0)} Z`,fill:'#f3c785',opacity:.45});
 add(svg,'path',{d:path(steps('signed_density')),fill:'none',stroke:'#83caff','stroke-width':1.8,'stroke-dasharray':'6 3'});
 line(svg,left,y(0),right,y(0),'#61758d');
 for(const v of [-cut,0,cut])add(svg,'text',{x:x(v),y:252,'text-anchor':'middle'},String(v));
 add(svg,'text',{x:right,y:275,'text-anchor':'end'},'Initial action coordinate x');
 add(svg,'text',{x:left,y:14},'Contribution / unit x');
 const total=p.expanded_allowance.reduce((a,b)=>a+b,0),inside=selected.reduce((a,i)=>a+p.expanded_allowance[i],0),signed=selected.reduce((a,i)=>a+p.signed_error[i],0);
 $('accuracy-region').textContent=`Inside the selected complete bins: ${fmt(signed)} signed error and ${fmt(inside)} absolute allowance${total>0?` (${(100*inside/total).toFixed(1)}% of the full orange area)`:'; the halo self-comparison has zero population mismatch'}. The separate mesh allowance is ${fmt(row.forecast.doubled_mismatch_mesh_change)}.`;
 ingredients(row,bins,effective);
}
function ingredients(row,bins,radius){
 if(!$('accuracy-ingredients').open)return;
 const p=row.plot,cut=row.forecast.cutoff;
 const f=row.forecast;
 $('accuracy-cancellation').textContent=`For this recorded kernel, the signed population contrast is ${fmt(f.paired_error_mean)}. Adding the absolute contributions gives ${fmt(f.plugin_mismatch)} before explicit kernel uncertainty. The uncertainty expansion adds ${fmt(f.expanded_mismatch-f.plugin_mismatch)}, and the mesh allowance adds ${fmt(f.doubled_mismatch_mesh_change)}. These make the orange population allowance; the approximate response’s own ${fmt(f.approximate.total_allowance)} allowance is added separately. These are gradient-coordinate contractions, not counts of orbital cohorts.`;
 for(const [id,blue,orange,title]of [['accuracy-slopes','halo_gradient','approximate_gradient','Initial population gradient'],['accuracy-kernel','kernel_mean','kernel_absolute_upper','Primitive response kernel']]){
  const [svg,w]=svgSetup(id,260),left=58,right=w-12,top=25,bottom=212;
  const extent=1.1*Math.max(...bins.flatMap(i=>[Math.abs(p[blue][i]),Math.abs(p[orange][i])]),1e-15);
  const x=v=>left+(right-left)*(v+cut)/(2*cut),y=v=>(top+bottom)/2-v/extent*(bottom-top)/2;
  add(svg,'title',{},title);add(svg,'text',{x:left,y:14},title);
  if(radius>0)add(svg,'rect',{x:x(-radius),y:top,width:x(radius)-x(-radius),height:bottom-top,fill:'#83caff',opacity:.08});
  for(const v of [-extent/1.1,0,extent/1.1]){line(svg,left,y(v),right,y(v),'#293b50');add(svg,'text',{x:left-5,y:y(v)+4,'text-anchor':'end'},v===0?'0':v.toExponential(1));}
  for(const [key,color]of [[orange,'#f3c785'],[blue,'#83caff']]){
   const points=bins.flatMap(i=>[[x(p.edges[i]),y(p[key][i])],[x(p.edges[i+1]),y(p[key][i])]]);
   add(svg,'path',{d:points.map(([a,b],i)=>(i?'L':'M')+a.toFixed(2)+','+b.toFixed(2)).join(' '),fill:'none',stroke:color,'stroke-width':1.6,...(key===blue?{'stroke-dasharray':'6 3'}:{})});
  }
  for(const v of [-cut,0,cut])add(svg,'text',{x:x(v),y:235,'text-anchor':'middle'},String(v));
  add(svg,'text',{x:right,y:258,'text-anchor':'end'},'Initial action coordinate x');
 }
}
function render(){
 current=data.rows.find(r=>r.forecast.population===$('accuracy-population').value&&r.forecast.tau===Number($('accuracy-time').value)&&r.forecast.cutoff===Number($('accuracy-window').value));
 if(!current)throw new Error('Recorded selection is missing');
 const f=current.forecast,a=current.independent,qualified=f.five_percent_qualified;
 $('accuracy-response').textContent=fmt(f.approximate.mean);$('accuracy-allowance').textContent=fmt(f.approximation_allowance);
 $('accuracy-actual').textContent=a?fmt(a.paired_population_error):'Pending';
 $('accuracy-actual-note').textContent=a?`approximation − halo, ±${fmt(a.paired_numerical_proxy)} numerical proxy`:'independent evolution required';
 $('accuracy-verdict').textContent=`${qualified?'5% accuracy qualified in advance':'5% accuracy not qualified'}${a?` · independent test ${a.independent_five_percent_test}`:' · independent test pending'}`;
 $('accuracy-verdict').parentElement.dataset.qualified=String(qualified);
 $('accuracy-verdict').parentElement.dataset.assessment=a?(qualified?a.independent_five_percent_test:'unqualified'):'pending';
 $('accuracy-verdict-detail').textContent=`${labels[f.population]}, T = ${f.tau}, cutoff ${f.cutoff}. Sign ${f.sign_qualification==='unqualified'?'not qualified':f.sign_qualification+' qualified'} by the frozen rule. ${a?`Independent sign assessment: ${a.sign_test.replaceAll('_',' ')}.`:'No prospective accuracy success is claimed before the independent test.'} ${f.five_percent_across_windows_qualified?'The frozen 5% rule also qualifies the shared-window comparison.':'The shared-window 5% rule does not qualify this comparison.'}`;
 budget(current);gradient(current);
 const params=new URLSearchParams(location.search);params.set('population',f.population);params.set('time',f.tau);params.set('window',f.cutoff);history.replaceState(null,'',`${location.pathname}?${params}${location.hash}`);
}
function cost(){
 const selection=new URLSearchParams(location.search);for(const [key,id]of [['costPopulation','accuracy-cost-population'],['costSweep','accuracy-cost-sweep'],['costTime','accuracy-cost-time']])selection.set(key,$(id).value);history.replaceState(null,'',`${location.pathname}?${selection}${location.hash}`);
 const r=data.cost.rows.find(r=>r.population===$('accuracy-cost-population').value&&r.s===Number($('accuracy-cost-sweep').value)&&r.tau===Number($('accuracy-cost-time').value));
 if(!r)throw new Error('Recorded cost selection is missing');
 const raw=r.precision.find(p=>p.method==='raw'),rem=r.precision.find(p=>p.method==='remainder');
 $('accuracy-raw-cost').textContent=raw.measured_mean_accounted_batch_cpu_seconds.toFixed(2)+' s';$('accuracy-rem-cost').textContent=rem.measured_mean_accounted_batch_cpu_seconds.toFixed(2)+' s';$('accuracy-gain').textContent=fmt(r.cost_times_variance_ratio)+'×';
 $('accuracy-cost-copy').textContent=`The measured conditional cost × variance ratio is ${fmt(r.cost_times_variance_ratio)}; paired batch-bootstrap interval [${r.paired_batch_bootstrap_cost_ratio_interval.map(fmt).join(', ')}]. Values above one favor the remainder. The noisier between-batch estimate is ${fmt(r.between_batch_cost_ratio)}. These are two variance estimates from the same eight batches, not independent confirmations.`;
 $('accuracy-cost-consistency').textContent=`Raw minus remainder: ${fmt(r.paired_raw_minus_remainder.mean)}, pointwise 95% interval [${r.paired_raw_minus_remainder.ci95.map(fmt).join(', ')}]. ${r.paired_interval_contains_zero?'This interval includes zero.':'This is the retained one-of-24 consistency flag: the interval excludes zero. It is not by itself evidence of bias after multiple correlated comparisons.'}`;
}
function table(){
 const tbody=$('accuracy-all');tbody.replaceChildren();
 for(const r of data.rows){const f=r.forecast,a=r.independent,tr=document.createElement('tr');for(const s of [`${labels[f.population]} / T${f.tau} / ${f.cutoff}`,f.five_percent_qualified?'Qualified':'Not qualified',a?a.independent_five_percent_test:'Pending',a?a.sign_test.replaceAll('_',' '):'Pending']){const td=document.createElement('td');td.textContent=s;tr.append(td);}tbody.append(tr);}
}
function fail(error){console.error(error);$('accuracy-load').dataset.error='true';$('accuracy-load').textContent='The recorded evidence could not be loaded. Reload the page or use the linked methods and downloadable records; no result is substituted.';$('accuracy-controls').disabled=true;$('accuracy-cost-controls').disabled=true;}
async function start(){
 const response=await fetch('diagnostics/population-accuracy/accuracy-explorer.json',{cache:'no-cache'});if(!response.ok)throw new Error(`Evidence HTTP ${response.status}`);data=await response.json();if(data.rows?.length!==24||data.s!==.5||data.eta!==.1||data.rows.some(r=>!r.plot.kernel_mean))throw new Error('Unexpected evidence record');
 const params=new URLSearchParams(location.search);for(const [key,id]of [['population','accuracy-population'],['time','accuracy-time'],['window','accuracy-window'],['costPopulation','accuracy-cost-population'],['costSweep','accuracy-cost-sweep'],['costTime','accuracy-cost-time']]){const value=params.get(key),control=$(id);if([...control.options].some(o=>o.value===value))control.value=value;}
 $('accuracy-controls').disabled=false;$('accuracy-cost-controls').disabled=false;$('accuracy-load').textContent=data.status==='independent_results_available'?'':'Numerical forecasts are frozen. Independent evolution is in progress; qualifications shown below are predictions.';
 for(const id of ['accuracy-population','accuracy-time','accuracy-window'])$(id).addEventListener('change',()=>{try{render();}catch(e){fail(e);}});
 $('accuracy-radius').addEventListener('input',()=>gradient(current));
 $('accuracy-ingredients').addEventListener('toggle',()=>{if(current)gradient(current);});
 for(const id of ['accuracy-cost-population','accuracy-cost-sweep','accuracy-cost-time'])$(id).addEventListener('change',cost);
 table();render();cost();let timer;window.addEventListener('resize',()=>{clearTimeout(timer);timer=setTimeout(()=>{budget(current);gradient(current);},100);});
}
start().catch(fail);
