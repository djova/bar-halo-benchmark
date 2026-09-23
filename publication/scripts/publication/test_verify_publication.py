"""Mutation tests for public checking coverage; no physical simulation."""
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import unittest
from verify_publication import verify, VerificationError, relative_assessment, advance_sign

ROOT=Path(__file__).resolve().parents[2]/'web'
VERSION=json.loads((ROOT/'manifest.json').read_text())['release']
BASE={'manifest.json':(ROOT/'manifest.json').read_bytes()}
for row in json.loads(BASE['manifest.json'])['artifacts']:
    BASE[row['path']]=(ROOT/row['path']).read_bytes()


def put(files,path,data):files[path]=json.dumps(data,ensure_ascii=False).encode()
def read(files,path):return json.loads(files[path])
def refresh(files):
    # Simulate a generator that consistently rehashes changed contents. These
    # tests must catch semantic mistakes beyond an outdated checksum.
    for path, array, key in [('claims.json','claims','evidence'),('datasets.json','datasets',None)]:
        data=read(files,path)
        for entry in data[array]:
            for e in entry[key] if key else [entry]:
                if 'path' in e:
                    e['sha256']=hashlib.sha256(files[e['path']]).hexdigest()
                    if 'bytes' in e:e['bytes']=len(files[e['path']])
        put(files,path,data)
    m=read(files,'manifest.json')
    for r in m['artifacts']:
        r['sha256']=hashlib.sha256(files[r['path']]).hexdigest();r['bytes']=len(files[r['path']])
    put(files,'manifest.json',m)


class MutationTests(unittest.TestCase):
    def setUp(self):self.files=copy.deepcopy(BASE)
    def check(self):return verify(self.files.__getitem__,VERSION)
    def test_baseline(self):
        result=self.check();self.assertEqual(result['qualified_count'],8);self.assertEqual(result['qualified_signs'],15);self.assertEqual(result['unqualified_independently_outside'],8)
    def test_reject_saved_classification_change(self):
        data=read(self.files,'results/accuracy.json');data['rows'][1]['qualified_5_percent']=False
        put(self.files,'results/accuracy.json',data);self.csv(data);refresh(self.files)
        with self.assertRaisesRegex(VerificationError,'reconstructed qualified'):self.check()
    def csv(self,data):
        out=io.StringIO();w=csv.DictWriter(out,fieldnames=list(data['rows'][0]));w.writeheader();w.writerows(data['rows']);self.files['results/accuracy.csv']=out.getvalue().encode()
    def test_reject_operand_change_with_fresh_hashes(self):
        data=read(self.files,'results/accuracy.json');data['rows'][1]['full_allowance']*=2
        put(self.files,'results/accuracy.json',data);self.csv(data);refresh(self.files)
        with self.assertRaisesRegex(VerificationError,'source operand full_allowance'):self.check()
    def test_reject_existing_but_wrong_claim_row(self):
        data=read(self.files,'claims.json');c=next(c for c in data['claims'] if c['id']=='PA-ACC-01');c['evidence'][0]['json_pointer']='/rows/0'
        put(self.files,'claims.json',data);refresh(self.files)
        with self.assertRaisesRegex(VerificationError,'Claim evidence identity'):self.check()
    def test_reject_missing_source_pointer(self):
        data=read(self.files,'claims.json');data['claims'][0]['evidence'][0]['json_pointer']='/rows/999'
        put(self.files,'claims.json',data);refresh(self.files)
        with self.assertRaisesRegex(VerificationError,'Unresolved JSON pointer'):self.check()
    def test_reject_stale_release(self):
        data=read(self.files,'manifest.json');data['release']='2026-09-23.1';put(self.files,'manifest.json',data)
        with self.assertRaisesRegex(VerificationError,'Unexpected release'):self.check()
    def test_reject_record_release_mismatch(self):
        data=read(self.files,'results/accuracy.json');data['release']='stale';put(self.files,'results/accuracy.json',data);refresh(self.files)
        with self.assertRaisesRegex(VerificationError,'Release mismatch'):self.check()
    def test_reject_article_number_with_refreshed_hash(self):
        self.files['paper.html']=self.files['paper.html'].replace(b'data-publication-scalar="population_late_magnitude_ratio">4.735323',b'data-publication-scalar="population_late_magnitude_ratio">9.735323')
        refresh(self.files)
        with self.assertRaisesRegex(VerificationError,'article headline number'):self.check()
    def test_reject_article_cell_with_refreshed_hash(self):
        text=self.files['paper.md'].decode();import re
        text,n=re.subn(r'(data-record="ACC-exponential-T10-W40" data-field="forecast">)[^<]+',r'\g<1>123',text)
        self.assertEqual(n,1);self.files['paper.md']=text.encode();refresh(self.files)
        with self.assertRaisesRegex(VerificationError,'article number'):self.check()
    def test_hash_check(self):
        self.files['paper.md']+=b' changed'
        with self.assertRaisesRegex(VerificationError,'Byte count mismatch'):self.check()
    def test_protocol_pointer(self):
        data=read(self.files,'claims.json');data['claims'][0]['protocols']=['protocols/missing.md'];put(self.files,'claims.json',data);refresh(self.files)
        with self.assertRaisesRegex(VerificationError,'Protocol missing'):self.check()
    def test_three_way_and_sign_boundaries(self):
        self.assertEqual(relative_assessment(.01,.001,1.,.01),'supported')
        self.assertEqual(relative_assessment(.1,.001,1.,.01),'contradicted')
        self.assertEqual(relative_assessment(.05,.01,1.,.01),'inconclusive')
        self.assertEqual(relative_assessment(0.,0.,0.,0.),'inconclusive')
        self.assertEqual(advance_sign(1.,1.),'unqualified');self.assertEqual(advance_sign(-2.,1.),'negative');self.assertEqual(advance_sign(2.,1.),'positive')


if __name__=='__main__':unittest.main()
