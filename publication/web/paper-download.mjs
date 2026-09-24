// Versioned PDF supplement; numerical article release and archived bytes stay fixed.
import {readFileSync} from 'node:fs';
const directory='downloads/mnras-2026-09-24.3/';
export const printExport=JSON.parse(readFileSync(new URL('./'+directory+'manifest.json',import.meta.url),'utf8'));
export function decorateDownload(document){
 if(document.querySelector('#paper-downloads'))return;
 const panel=document.createElement('aside');panel.id='paper-downloads';panel.className='paper-downloads';
 panel.setAttribute('aria-label','Download the typeset paper');
 const pdf=printExport.artifacts.find(a=>a.path==='galaxy-bar-mnras.pdf');
 panel.innerHTML=`<a class="paper-pdf-button" href="${directory}galaxy-bar-mnras.pdf" download="galaxy-bar-mnras.pdf" type="application/pdf"><span aria-hidden="true">↓</span> Download PDF <span class="pdf-format">MNRAS format · ${(pdf.bytes/1024/1024).toFixed(1)} MB</span></a><p>Includes figures, complete result tables and bibliography. Unreviewed manuscript.<br><a href="https://github.com/djova/bar-halo-benchmark/tree/manuscript-${printExport.export}/manuscript">LaTeX source and build instructions</a> · <a href="${directory}manifest.json">PDF version ${printExport.export}</a></p>`;
 (document.querySelector('.publication-meta')||document.querySelector('main h1')).after(panel);
 const alt=document.createElement('link');alt.rel='alternate';alt.type='application/pdf';alt.href=directory+'galaxy-bar-mnras.pdf';alt.title='MNRAS-format PDF with bibliography';document.head.append(alt);
}
export function recordPrintExport(manifest){
 manifest.print_export={export:printExport.export,scientific_release:printExport.scientific_release,pdf:directory+'galaxy-bar-mnras.pdf',manifest:directory+'manifest.json',review_status:'not_externally_reviewed'};
 for(const path of [...printExport.artifacts.map(a=>directory+a.path),directory+'manifest.json'])if(!manifest.artifacts.some(a=>a.path===path))manifest.artifacts.push({path});
}
