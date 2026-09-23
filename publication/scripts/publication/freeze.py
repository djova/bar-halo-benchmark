#!/usr/bin/env python3
"""Freeze reviewed publication build bytes. Existing releases are never replaced."""
import hashlib,json,re,shutil,posixpath
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[2];built=ROOT/'web/dist/client';manifest=json.loads((built/'manifest.json').read_text());version=manifest['release'];dest=ROOT/'web/releases'/version
if dest.exists():raise SystemExit('Existing release is immutable; choose a new version.')
files={x['path']for x in manifest['artifacts']}
files|={'data/manifest.json','data/archive/index-2026-09-21.json'}
files|={f'diagnostics/population-accuracy/{name}.md'for name in ['PLAN','SOURCES','CLAIM_LEDGER','ACCURACY_OUTCOME_01','COST_OUTCOME_02','EXTERNAL_REVIEW_QUESTIONS']}
files|={'story.css','population-response.css','population-accuracy.css','publication.css','population-accuracy.js','presentation.js','navigation.js','navigation.css','verify_publication.py'}
files|={f'diagnostics/population-accuracy/{name}.png'for name in ['population-comparison','population-accuracy','estimator-efficiency']}
# A snapshot retains core scientific pages and files. Deeper historical pages keep stable current-site links.
def rewrite(text,path):
 def attr(m):
  link=m[2];u=urlsplit(link)
  if not link or u.scheme or u.netloc or link.startswith(('#','/')):return m[0]
  relative=posixpath.normpath((Path(path).parent/u.path).as_posix())
  if relative not in files and relative!='manifest.json':link='../'*(2+len(Path(path).parent.parts))+relative+('?' + u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
  return m[1]+link+m[3]
 return re.sub(r'((?:href|src)=")([^"]+)(")',attr,text)
for name in sorted(files):
 src=built/name;out=dest/name;out.parent.mkdir(parents=True,exist_ok=True)
 if src.suffix=='.html':out.write_text(rewrite(src.read_text(),name))
 elif src.suffix=='.md':
  def link(m):
   u=urlsplit(m[2]);target=posixpath.normpath((Path(name).parent/u.path).as_posix())
   return m[0] if not u.path or u.scheme or u.netloc or target in files else m[1]+'../'*(2+len(Path(name).parent.parts))+target+('?' + u.query if u.query else '')+('#'+u.fragment if u.fragment else '')+')'
  out.write_text(re.sub(r'(\[[^\]]*\]\()([^)]*)\)',link,src.read_text()))
 else:shutil.copyfile(src,out)
manifest['snapshot']=True;manifest['release_snapshot']='manifest.json';manifest['artifacts']=[dict(path=n,bytes=(dest/n).stat().st_size,sha256=hashlib.sha256((dest/n).read_bytes()).hexdigest())for n in sorted(files)]
(dest/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'release':version,'frozen_files':len(files)}))
