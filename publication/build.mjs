// Clean standalone article build; no host tooling or simulation execution.
import {recordPrintExport} from './web/paper-download.mjs';
import {rm,cp,readFile,writeFile,readdir} from 'node:fs/promises';
import {presentPage,mathAssets} from './web/presentation-build.mjs';
import {createHash} from 'node:crypto';import {decoratePage,pages} from './web/navigation-build.mjs';
await rm('dist',{recursive:true,force:true});await cp('web','dist',{recursive:true,filter:path=>!path.split('/').includes('node_modules')});
const mathFiles=await mathAssets('dist');const exists=new Set();async function walk(path,prefix=''){for(const d of await readdir(path,{withFileTypes:true})){const name=prefix+d.name;if(d.isDirectory())await walk(path+'/'+d.name,name+'/');else exists.add(name)}}await walk('dist');
for(const page of pages){if(!exists.has(page.file))continue;let {html}=decoratePage(await readFile('dist/'+page.file,'utf8'),page.file);html=html.replace(/((?:href|src)=")([^"#]+)(")/g,(m,b,u,e)=>{if(/^(https?:|data:|mailto:)/.test(u)||u.startsWith('/'))return m;const path=u.split(/[?#]/)[0];return exists.has(path)?m:b+'https://djova.ca/galaxy-bar/'+u+e});await writeFile('dist/'+page.file,presentPage(html,page.file).html)}
const m=JSON.parse(await readFile('dist/manifest.json','utf8'));recordPrintExport(m);for(const path of [...mathFiles,'presentation.js','publication.css'])if(!m.artifacts.some(a=>a.path===path))m.artifacts.push({path});for(const a of m.artifacts){const b=await readFile('dist/'+a.path);a.sha256=createHash('sha256').update(b).digest('hex');a.bytes=b.length}await writeFile('dist/manifest.json',JSON.stringify(m,null,2)+'\n');console.log('Built the canonical article and central evidence; historical explorers link to the public site.');
