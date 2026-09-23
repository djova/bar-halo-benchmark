import {posix} from 'node:path';

// One publication map drives every drawer, breadcrumb and directory entry.
export const groups = [
  {id:'start', title:'Start here', pages:[
    {file:'index.html', title:'Galaxy Bar overview', description:'The current contribution, with the original galaxies as an introduction.'},
    {file:'paper.html', title:'Research article · current', description:'The complete argument: population bias, accuracy and estimator cost.'},
    {file:'learn.html', title:'Learn the foundations', description:'Six ordered modules from stars and patterns to the research inference.'},
    {file:'reproduce.html', title:'Inspect & reproduce', description:'Public evidence and per-study reproduction scope.'},
    {file:'agents.html', title:'Agent access', description:'Anonymous discovery, claim IDs, datasets and verification.'},
    {file:'experiments.html', title:'Models & experiments', description:'Which physical system and clock does each result concern?'},
    {file:'archive.html', title:'Archive & revisions', description:'Historical studies, retained failures and corrections.'},
    {file:'guide.html', title:'Contents & evidence guide', description:'Find a page, a scientific question, or the evidence behind a claim.'},
  ]},
  {id:'explore', title:'Interactive explorers', pages:[
    {file:'lab.html', title:'Galaxy simulation lab', description:'25 recorded galaxies: stars, bar growth, halo shape and mock observations.'},
    {file:'response-coupling.html', title:'Paths & torque explorer', description:'The same halo particles under no bar, a steady bar and a slowing bar.'},
    {file:'response-orbits.html', title:'Smooth halo orbits', description:'Follow orbital motion and angular momentum in the smooth reference.'},
    {file:'response-forces.html', title:'Forces & torque', description:'Inspect the recorded force components acting on one halo particle.'},
  ]},
  {id:'findings', title:'Supporting studies & verification', pages:[
    {file:'population-accuracy.html', title:'When is an approximation safe?', description:'Explore population error budgets, independent tests and measured estimator efficiency.'},
    {file:'population-response.html', title:'Population & resonant transfer', description:'Change the material weighting the recorded response; inspect halo, tracer and kernel predictions.'},
    {file:'noise-sweep.html', title:'Noise & moving resonances', description:'Matched noise effects, recorded trajectories and the new-condition 3D test.'},
    {file:'synthesis.html', title:'Archived galaxy findings', description:'What the original galaxies and thickness controls establish.'},
    {file:'response.html', title:'Bar–halo response findings', description:'Independent-phase replication, disturbance tests and unresolved response.'},
    {file:'response-validation.html', title:'Response numerical checks', description:'Accuracy, transport, orbital coordinates and collision checks.'},
    {file:'response-source-history.html', title:'Original source-step failure', description:'The earlier failed gate, retained alongside its later repair.'},
  ]},
  {id:'methods', title:'Methods & data', pages:[
    {file:'population-methods.html', title:'Population response methods', description:'Absolute halo weighting, response kernels, independent checks and prospective population predictions.'},
    {file:'noise-methods.html', title:'Resonance model & methods', description:'Canonical actions, imposed noise, population limits and prediction criteria.'},
    {file:'methodology.html', title:'Galaxy methods', description:'Initial conditions, softening, measurements and verification plots.'},
    {file:'followup.html', title:'Galaxy follow-up notebook', description:'Detailed thickness, numerical and observational control evidence.'},
    {file:'response-methods.html', title:'Response methods', description:'Critical assessment, frozen protocols and the final campaign assessment.'},
    {file:'diagnostics/response/source-index.html', title:'Response source & checksums', description:'Download the reviewed scientific code and inspect its provenance.'},
  ]},
  {id:'context', title:'Research context & history', pages:[
    {file:'research.html', title:'Literature review', description:'Primary papers, open questions and testable research directions.'},
    {file:'sidm-critical-review.html', title:'SIDM paper assessment', description:'The scope and limitations of the gas-dependent SIDM argument.'},
    {file:'final-report.html', title:'Original six-hour report', description:'Archived results from the first completed experiment.'},
    {file:'next-48-hours.html', title:'Original two-day plan', description:'The historical follow-up plan; not a queue of active jobs.'},
    {file:'project-brief.html', title:'Project brief & prompts', description:'The scientific priorities and presentation guidance behind this project.'},
    {file:'communication.html', title:'Publication design', description:'The paper review and principles used to explain the research.'},
  ]},
];

const escape = s => s.replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const text = s => s.replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
const icon = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>';
export const pages = groups.flatMap(group=>group.pages.map(page=>({...page,group})));

export function decoratePage(input, file) {
  const page=pages.find(p=>p.file===file);
  if(!page) throw new Error(`Page missing from publication navigation: ${file}`);
  const prefix=posix.relative(posix.dirname(file),'.');
  const href=f=>(prefix?prefix+'/':'')+(f==='index.html'?'./':f);
  let html=input;
  // The generated source index was originally a minimal standalone HTML document.
  if(!/<body\b/i.test(html)) {
    html=html.replace(/<html([^>]*)>/i,'<html$1><head>').replace('</style>','</style></head><body class="gb-source-page"><main class="gb-source-content">');
    html=html.replace(/<\/html>\s*$/i,'')+'</main></body></html>';
  }
  html=html.replace('<!-- SITE_DIRECTORY -->',`<section id="directory"><h2>All pages, organized by purpose.</h2><p>Interactive views use recorded data. The galaxy views share a clock in billion years; the controlled halo experiments have their own model-time clocks.</p><div class="gb-directory">${groups.map(g=>`<section id="directory-${g.id}"><h3>${escape(g.title)}</h3><ul>${g.pages.map(p=>`<li><a href="${href(p.file)}">${escape(p.title)}</a><p>${escape(p.description)}</p></li>`).join('')}</ul></section>`).join('')}</div></section>`);
  const headings=[];
  const used=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
  html=html.replace(/<h2\b([^>]*)>([\s\S]*?)<\/h2>/gi,(full,attrs,body)=>{
    const label=text(body); let id=attrs.match(/\bid="([^"]+)"/)?.[1];
    if(!id){const base='contents-'+label.toLowerCase().replace(/&[^;]+;/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');id=base;let n=2;while(used.has(id))id=base+'-'+n++;used.add(id);attrs+=` id="${id}"`;}
    headings.push({id,label});return `<h2${attrs}>${body}</h2>`;
  });
  const toggle=`<a class="gb-menu-toggle" href="#site-navigation" aria-label="Open table of contents" title="Table of contents">${icon}</a>`;
  const plainHeader=`<header class="gb-document-header">${toggle}<a class="brand" href="${href('index.html')}">Galaxy Bar</a><span class="gb-header-location">${escape(page.title)}</span></header>`;
  let playback=false;
  if(/<header\b/i.test(html)) html=html.replace(/<header\b[^>]*>[\s\S]*?<\/header>/i,header=>{
    if(!/<input\b/.test(header))return plainHeader;
    playback=true;return header.replace(/<a\b[^>]*class="brand"/,toggle+'<a class="brand"');
  });
  else html=html.replace(/<body\b[^>]*>/i,match=>match+plainHeader);
  if(!html.includes(toggle))throw new Error(`No menu button inserted: ${file}`);
  const breadcrumb=`<nav class="gb-breadcrumb" aria-label="Breadcrumb"><a href="${href('index.html')}">Home</a><span aria-hidden="true">/</span><a href="${href('guide.html')}#directory-${page.group.id}">${escape(page.group.title)}</a><span aria-hidden="true">/</span><span aria-current="page">${escape(page.title)}</span></nav>`;
  html=html.replace('</header>','</header>'+breadcrumb);
  const archived=['synthesis.html','final-report.html','next-48-hours.html'];
  const supporting=['population-accuracy.html','population-response.html','noise-sweep.html','response.html','population-methods.html','response-methods.html'];
  if(archived.includes(file)||supporting.includes(file)){
    const label=archived.includes(file)?'Archived: original galaxy campaign.':'Supporting experiment: study-specific scope.';
    html=html.replace(/(<main\b[^>]*>)/i,'$1'+`<aside class="publication-status"><strong>${label}</strong> Conclusions apply to the named experiments and original criteria here. Read the <a href="${href('paper.html')}">current canonical research article</a> for the consolidated argument and subsequent results. <a href="${href('archive.html')}">Revision history</a>.</aside>`);
  }
  html=html.replace(/<nav class="research-depth-nav"[\s\S]*?<\/nav>/g,'');
  const item=p=>`<li><a href="${href(p.file)}"${p.file===file?' aria-current="page"':''}><span>${escape(p.title)}</span>${p.file===file?'<small>You are here</small>':''}</a></li>`;
  const sections=headings.length?`<details class="gb-page-sections"><summary>On this page <span>${headings.length} sections</span></summary><ol>${headings.map(h=>`<li><a href="#${escape(h.id)}">${h.label}</a></li>`).join('')}</ol></details>`:'';
  const drawer=`<aside id="site-navigation" class="gb-navigation" tabindex="-1"><div class="gb-drawer-heading"><div><span class="gb-kicker">GALAXY BAR</span><h2 id="site-navigation-title">Contents</h2></div><button class="gb-menu-close" type="button" aria-label="Close table of contents" hidden>×</button></div><p class="gb-current-location">${escape(page.group.title)}<br><strong>${escape(page.title)}</strong></p>${sections}<nav class="gb-tree" aria-label="Site pages">${groups.map(g=>`<details class="gb-nav-group"${g.id===page.group.id||g.id==='explore'?' open':''}><summary>${escape(g.title)}</summary><ul>${g.pages.map(item).join('')}</ul></details>`).join('')}</nav><a class="gb-all-pages" href="${href('guide.html')}#directory">View the full site & evidence guide ↗</a></aside>`;
  html=html.replace('</body>',drawer+`<script type="module" src="${href('navigation.js')}"></script></body>`);
  html=html.replace('</head>',`<link rel="stylesheet" href="${href('navigation.css')}"><link rel="stylesheet" href="${href('publication.css')}"></head>`);

  return {html,page,headings,playback};
}
