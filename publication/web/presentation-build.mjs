// Typeset authored TeX at build time. Readers need neither a CDN nor JavaScript.
import katex from 'katex';
import {decorateDownload} from './paper-download.mjs';
import {parseHTML} from 'linkedom';
import {cp,mkdir,readFile,writeFile,readdir} from 'node:fs/promises';
import {createRequire} from 'node:module';
import {dirname,join,posix} from 'node:path';
const require=createRequire(import.meta.url);
const katexRoot=dirname(require.resolve('katex/package.json'));

export async function mathAssets(out){
 const dest=join(out,'math');await mkdir(dest,{recursive:true});
 // Modern target browsers use WOFF2. Do not ship unused legacy font formats.
 const css=(await readFile(join(katexRoot,'dist/katex.min.css'),'utf8')).replace(/,url\([^)]*\.(?:woff|ttf)\) format\("[^"]+"\)/g,'');
 await writeFile(join(dest,'katex.min.css'),css);
 await mkdir(join(dest,'fonts'),{recursive:true});
 for(const file of await readdir(join(katexRoot,'dist/fonts')))if(file.endsWith('.woff2'))await cp(join(katexRoot,'dist/fonts',file),join(dest,'fonts',file));
 await cp(join(katexRoot,'LICENSE'),join(dest,'LICENSE'));
 await writeFile(join(dest,'VERSION.txt'),'KaTeX 0.18.9; MIT. Typeset at build time; local fonts.\n');
 return ['math/katex.min.css','math/LICENSE','math/VERSION.txt',...(await readdir(join(dest,'fonts'))).map(f=>'math/fonts/'+f)];
}

export function presentPage(input,file){
 const {document}=parseHTML(input);let equations=0;
 if(file==='paper.html')decorateDownload(document);
 const typeset=(tex,display)=>{
  const node=document.createElement(display?'div':'span');node.className=display?'math-block':'math-inline';
  node.setAttribute('data-tex',tex);
  node.innerHTML=katex.renderToString(tex,{displayMode:display,throwOnError:true,strict:'error',trust:false,output:'htmlAndMathml'});
  if(display){node.setAttribute('tabindex','0');node.setAttribute('role','group');node.setAttribute('aria-label','Equation; scroll horizontally if needed');}
  equations++;return node;
 };
 for(const code of document.querySelectorAll('pre > code.language-math'))code.parentElement.replaceWith(typeset(code.textContent.trim(),true));
 for(const node of document.querySelectorAll('[data-math]'))node.replaceWith(typeset(node.getAttribute('data-math'),node.tagName!=='SPAN'));
 const nodes=[];
 function visit(node){if(node.nodeType===3)nodes.push(node);else if(node.nodeType===1&&!['SCRIPT','STYLE','PRE','CODE','TEXTAREA','SVG','MATH'].includes(node.tagName)&&!node.classList.contains('math-block')&&!node.classList.contains('math-inline'))for(const child of node.childNodes)visit(child);}
 visit(document.body);
 for(const node of nodes){const text=node.textContent;const re=/\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)/g;let m,start=0;const fragment=document.createDocumentFragment();
  while((m=re.exec(text))){fragment.append(document.createTextNode(text.slice(start,m.index)),typeset(m[1]??m[2],m[1]!==undefined));start=re.lastIndex;}
  if(start){fragment.append(document.createTextNode(text.slice(start)));node.replaceWith(fragment);}
 }
 // Tables are inspectable evidence, not the default visual explanation.
 let collapsed=0;
 for(const table of document.querySelectorAll('main table')){
  const rows=[...table.querySelectorAll('tbody tr')];const allRows=[...table.querySelectorAll('tr')];
  const dataRows=rows.length?rows:allRows.filter(r=>r.querySelector('td'));
  const cells=[...table.querySelectorAll('td')];const numeric=cells.filter(c=>/\d/.test(c.textContent)).length;
  const count=dataRows.length;const wide=(allRows[0]?.children.length||0)>=6;
  table.classList.add('readable-table');
  for(const c of cells)if(/^\s*[+−\-\d.[(]/.test(c.textContent)&&c.textContent.trim().length<100)c.classList.add('numeric-cell');
  let wrap=table.parentElement;
  if(!wrap.classList.contains('publication-table')&&!wrap.classList.contains('population-table-wrap')&&!wrap.classList.contains('table-scroll')){
   const region=document.createElement('div');region.className='table-scroll';table.replaceWith(region);region.append(table);wrap=region;
  }
  wrap.classList.add('evidence-table-scroll');wrap.setAttribute('tabindex','0');wrap.setAttribute('role','region');
  const label=table.querySelector('caption')?.textContent.trim()||'Complete recorded values';wrap.setAttribute('aria-label',label+'; scroll horizontally if needed');
  if((count>=6&&numeric>cells.length*.2)||wide||table.querySelector('#accuracy-all')||table.querySelector('#population-all')){
   if(wrap.closest('details'))continue;
   const details=document.createElement('details');details.className='evidence-values';
   const summary=document.createElement('summary');
   summary.textContent=table.querySelector('#accuracy-all')?'Inspect all 24 recorded decisions':`Inspect ${count||'all'} recorded rows and exact values`;
   wrap.replaceWith(details);details.append(summary,wrap);collapsed++;
  }
 }
 if(equations){const prefix=posix.relative(posix.dirname(file),'.');const link=document.createElement('link');link.rel='stylesheet';link.href=(prefix?prefix+'/':'')+'math/katex.min.css';document.head.append(link);}
 const script=document.createElement('script');script.type='module';const prefix=posix.relative(posix.dirname(file),'.');script.src=(prefix?prefix+'/':'')+'presentation.js';document.body.append(script);
 return {html:document.toString(),equations,collapsed};
}
