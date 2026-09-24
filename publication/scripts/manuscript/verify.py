#!/usr/bin/env python3
"""Check the typeset export against its recorded inputs; does not validate physics."""
import hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'web/downloads/mnras-2026-09-24.3';B=R/'build/mnras-2026-09-24.3'
m=json.loads((D/'manifest.json').read_text())
for r in m['inputs']:assert hashlib.sha256((R/r['path']).read_bytes()).hexdigest()==r['sha256'],r
for r in m['artifacts']:assert hashlib.sha256((D/r['path']).read_bytes()).hexdigest()==r['sha256'],r
tex=(D/'galaxy-bar-mnras.tex').read_text();text=subprocess.check_output(['pdftotext','-layout',str(D/'galaxy-bar-mnras.pdf'),'-'],text=True)
assert '{{'not in tex and '[!ht]'not in text and '??'not in text
assert '=latex'not in text, 'Raw reference markup leaked into rendered PDF'
assert tex.count('\\includegraphics')==4
assert all(k in (B/'galaxy-bar-mnras.bbl').read_text()for k in ['Hamilton2023','Chiba2023','Elbers2021','OgilvieLubow2006','GalaxyBar2026','Dattathri2026','Vasiliev2019'])
assert 'REFERENCES'in text and 'APPENDIX A'in text and 'APPENDIX B'in text
flow=subprocess.check_output(['pdftotext',str(D/'galaxy-bar-mnras.pdf'),'-'],text=True)
assert 'These experiments do not test CDM against SIDM.'in re.sub(r'\s+',' ',flow)
assert '4.735323'in text and '0.00150764622'in text and '-0.0342002314'in text
log=(B/'galaxy-bar-mnras.log').read_text()
assert not re.search(r'Overfull|undefined references|Missing character|Citation .*undefined',log)
# Inspect the table serialization independently: all rows and signs survive export.
tables=re.findall(r'\\begin\{tabular\}.*?\\midrule\n(.*?)\\bottomrule',tex,re.S)
assert [len(t.strip().splitlines())for t in tables]==[6,24,24,24,24]
pop=json.loads((R/'web/results/populations.json').read_text())['rows']
for line,row in zip(tables[0].strip().splitlines(),pop):
 cells=line.rstrip('\\ ').split('&')
 for cell,key in zip(cells[2:],['response','ci95_low','ci95_high']):assert abs(float(cell)-row[key])<=max(abs(row[key])*5e-9,5e-12)
info=subprocess.check_output(['pdfinfo',str(D/'galaxy-bar-mnras.pdf')],text=True)
result={'export':m['export'],'scientific_release':m['scientific_release'],'pages':int(re.search(r'Pages:\s+(\d+)',info)[1]),'figures':4,'bibliography_entries':7,'table_rows':[6,24,24,24,24],'source_and_artifact_hashes_match':True,'unresolved_references':False,'overflowing_tex_boxes':False,'science_rerun':False,'limitations':'Checks export fidelity and layout diagnostics, not numerical error coverage or astrophysical validity.'}
(R/'results/editorial-repair').mkdir(parents=True,exist_ok=True)
(R/'results/editorial-repair/document-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
