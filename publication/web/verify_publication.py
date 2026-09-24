#!/usr/bin/env python3
"""Check supplied publication records, not simulations or general scientific validity.
Standard library only. Supports an anonymous HTTP(S) origin or a local directory.
"""
import argparse
import csv
import hashlib
import io
import json
import math
from html.parser import HTMLParser
from pathlib import Path
import urllib.request
from urllib.parse import urljoin, urlsplit


class VerificationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def near(a, b, label):
    require(math.isfinite(a) and math.isfinite(b) and math.isclose(a, b, rel_tol=2e-13, abs_tol=1e-18), label)


def pointer(value, path):
    require(path == '' or path.startswith('/'), f'Invalid JSON pointer: {path}')
    try:
        for key in path.split('/')[1:]:
            key = key.replace('~1', '/').replace('~0', '~')
            value = value[int(key)] if isinstance(value, list) else value[key]
    except (KeyError, IndexError, ValueError, TypeError) as e:
        raise VerificationError(f'Unresolved JSON pointer: {path}') from e
    return value


def relative_assessment(value, proxy, reference, reference_proxy):
    lower = max(0., abs(reference) - reference_proxy)
    upper = abs(reference) + reference_proxy
    if lower > 0 and abs(value) + proxy <= .05 * lower:
        return 'supported'
    if max(0., abs(value) - proxy) > .05 * upper:
        return 'contradicted'
    return 'inconclusive'


def advance_sign(mean, allowance):
    return 'positive' if mean > allowance else 'negative' if mean < -allowance else 'unqualified'


class ArticleParser(HTMLParser):
    """Read visible numeric cells, retaining their stable result/field identifiers."""
    def __init__(self):
        super().__init__()
        self.values = []; self.stack = []; self.ids = set(); self.text = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'span':
            self.stack.append((attrs, []))
    def handle_data(self, text):
        self.text.append(text)
        for _, parts in self.stack:
            parts.append(text)
    def handle_endtag(self, tag):
        if tag == 'span' and self.stack:
            attrs, parts = self.stack.pop()
            if 'data-record' in attrs or 'data-publication-scalar' in attrs:
                self.values.append((attrs, ''.join(parts)))


class Reader:
    def __init__(self, origin):
        self.origin = origin.rstrip('/') + '/'; self.receipts = []; self.cache = {}
    def __call__(self, path):
        if path in self.cache:
            return self.cache[path]
        require(not urlsplit(path).scheme and not path.startswith('/') and '..' not in Path(path).parts, f'Nonlocal manifest path: {path}')
        if urlsplit(self.origin).scheme in ('http', 'https'):
            req = urllib.request.Request(urljoin(self.origin, path), headers={'User-Agent': 'GalaxyBar-PublicVerification/2.0', 'Accept': '*/*'})
            with urllib.request.urlopen(req, timeout=60) as response:
                data = response.read(); typ = response.headers.get_content_type(); status = response.status
            # Raw GitHub deliberately serves JSON/Markdown as text/plain.
            allowed = {'.json': ('application/json', 'text/plain'), '.html': ('text/html', 'text/plain'), '.md': ('text/plain', 'text/markdown')}
            if Path(path).suffix in allowed:
                require(typ in allowed[Path(path).suffix], f'Unexpected content type {typ}: {path}')
        else:
            data = (Path(self.origin) / path).read_bytes(); typ = 'local-file'; status = None
        self.receipts.append(dict(path=path, status=status, content_type=typ, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
        self.cache[path] = data
        return data


def verify(fetch, expected_release=None):
    manifest = json.loads(fetch('manifest.json'))
    version = manifest['release']
    require(expected_release is None or version == expected_release, f'Unexpected release: requested {expected_release}, got {version}')
    artifacts = {r['path']: r for r in manifest['artifacts']}
    require(len(artifacts) == len(manifest['artifacts']), 'Duplicate artifact paths')
    for path, record in artifacts.items():
        data = fetch(path)
        require(len(data) == record['bytes'], f'Byte count mismatch: {path}')
        require(hashlib.sha256(data).hexdigest() == record['sha256'], f'Hash mismatch: {path}')
    def record(path):
        require(path in artifacts, f'Unmanifested evidence: {path}')
        return json.loads(fetch(path))
    def same(a, b, label):
        require(a == b, label)
    claims = record('claims.json'); models = record('models.json'); campaigns = record('campaigns.json')
    datasets = record('datasets.json'); summary = record('results/summary.json')
    for name in ('claims.json','models.json','campaigns.json','datasets.json','figures.json','results/summary.json','results/populations.json','results/accuracy.json','results/cost.json'):
        same(record(name)['release'], version, f'Release mismatch: {name}')
    pop = record('results/populations.json')['rows']; acc = record('results/accuracy.json')['rows']; cost = record('results/cost.json')['rows']
    for dataset in datasets['datasets']:
        if 'path' in dataset:
            path = dataset['path']; require(path in artifacts, f'Dataset missing: {path}')
            same(dataset['sha256'], artifacts[path]['sha256'], f'Dataset hash: {path}')
            same(dataset['bytes'], artifacts[path]['bytes'], f'Dataset bytes: {path}')
    # JSON and CSV are two public representations of the same records.
    for name, rows in [('populations',pop),('accuracy',acc),('cost',cost)]:
        csvrows = list(csv.DictReader(io.StringIO(fetch(f'results/{name}.csv').decode())))
        same(len(csvrows),len(rows),f'{name}: CSV rows')
        for row, csvrow in zip(rows,csvrows):
            same(set(row),set(csvrow),f'{name}: CSV columns')
            for key, value in row.items():
                if isinstance(value,(int,float)) and not isinstance(value,bool): near(float(csvrow[key]),value,f'{name}: CSV {key}')
                else: same(csvrow[key],str(value),f'{name}: CSV {key}')
    original = record('diagnostics/population-response/independent-validation.json')
    for row in pop:
        source = pointer(original,row['pointer'])
        same((row['population']+'-40',row['time'],row['s']), (source['population'],source['tau'],source['s']), 'Population source identity')
        for key, value in [('response',source['integral_w_K_B']['mean']),('ci95_low',source['integral_w_K_B']['ci95'][0]),('ci95_high',source['integral_w_K_B']['ci95'][1])]: near(row[key],value,'Population source '+key)
    full = record('diagnostics/population-accuracy/accuracy-explorer.json')
    calculations = []
    for row in acc:
        source = pointer(full,row['pointer']); f=source['forecast']; a=source['independent']; halo=a['independent_halo']; actual=a['independent']
        same((row['population'],row['time'],row['cutoff']),(f['population'],f['tau'],f['cutoff']),'Accuracy source identity')
        require(a['all_local_gates_pass'], 'Numerical gate not qualified: '+row['id'])
        operands = dict(forecast=f['approximate']['mean'],independent_response=actual['response'],independent_halo_response=halo['response'],intrinsic_population_error=a['paired_population_error'],intrinsic_error_proxy=a['paired_numerical_proxy'],forecast_minus_independent_halo=a['forecast_minus_independent_halo'],independent_halo_proxy=halo['numerical_proxy'],population_allowance=f['approximation_allowance'],full_allowance=f['combined_response_allowance'],target=f['five_percent_absolute_target'])
        for key,value in operands.items():near(row[key],value,row['id']+': source operand '+key)
        # Reconstruct additive proxies/allowances from supplied refinements; this
        # checks arithmetic, not the scientific coverage of those proxies.
        near(halo['numerical_proxy'],sum(abs(v) for v in halo['changes'].values()),'Halo proxy sum')
        near(a['paired_numerical_proxy'],sum(abs(v) for v in a['paired_numerical_changes'].values()),'Paired proxy sum')
        near(row['population_allowance'],f['expanded_mismatch']+f['doubled_mismatch_mesh_change'],'Population allowance sum')
        near(row['full_allowance'],row['population_allowance']+f['approximate']['total_allowance'],'Full allowance sum')
        near(row['target'],.05*max(0.,abs(f['halo']['mean'])-f['halo']['total_allowance']),'Frozen target')
        discrepancy = row['forecast']-halo['response']; intrinsic=actual['response']-halo['response']
        near(discrepancy,row['forecast_minus_independent_halo'],'Forecast discrepancy')
        near(intrinsic,row['intrinsic_population_error'],'Intrinsic discrepancy')
        qualified=row['target']>0 and row['full_allowance']<=row['target']
        assessment=relative_assessment(discrepancy,halo['numerical_proxy'],halo['response'],halo['numerical_proxy'])
        intrinsic_assessment=relative_assessment(intrinsic,a['paired_numerical_proxy'],halo['response'],halo['numerical_proxy'])
        sign=advance_sign(row['forecast'],row['full_allowance'])
        independent_sign='positive' if halo['response']>halo['numerical_proxy'] else 'negative' if halo['response']<-halo['numerical_proxy'] else 'unresolved'
        sign_assessment='not_qualified' if sign=='unqualified' else 'inconclusive' if independent_sign=='unresolved' else 'supported' if sign==independent_sign else 'contradicted'
        for key,value in [('qualified_5_percent',qualified),('independent_assessment',assessment),('intrinsic_assessment',intrinsic_assessment),('sign_qualification',sign),('sign_assessment',sign_assessment)]:same(row[key],value,row['id']+': reconstructed '+key)
        for key,value in [('five_percent_qualified',qualified),('sign_qualification',sign)]:same(f[key],value,'Source forecast label: '+key)
        for key,value in [('independent_five_percent_test',assessment),('intrinsic_population_five_percent_test',intrinsic_assessment),('sign_test',sign_assessment)]:same(a[key],value,'Source outcome label: '+key)
        allowance_covers=abs(intrinsic)+a['paired_numerical_proxy']<=row['population_allowance']
        require(allowance_covers,'Population allowance does not cover supplied error/proxy')
        calculations.append(dict(id=row['id'],reference=row['self_reference'],qualified=qualified,assessment=assessment,intrinsic_assessment=intrinsic_assessment,sign=sign,sign_assessment=sign_assessment,allowance_covers=allowance_covers))
    for row in cost:
        source=pointer(full,row['pointer'])
        same((row['population'],row['s'],row['time']),(source['population'],source['s'],source['tau']),'Cost source identity')
        near(row['cost_times_variance_ratio'],source['cost_times_variance_ratio'],'Cost source ratio')
        near(row['between_batch_ratio'],source['between_batch_cost_ratio'],'Cost between-batch ratio')
    get=lambda k,t:next(r['response'] for r in pop if r['population']==k and r['time']==t)
    ratio=abs(get('gaussian',20)/get('halo',20));near(ratio,summary['population_late_magnitude_ratio'],'Population ratio')
    require(get('gaussian',10)>0>get('halo',10),'Early population signs')
    candidates=[r for r in calculations if not r['reference']]; qualified=[r for r in candidates if r['qualified']]
    conservative=[r['id'] for r in candidates if not r['qualified'] and r['intrinsic_assessment']=='supported']
    counts=dict(candidate_comparisons=len(candidates),qualified_5_percent=len(qualified),supported_qualified=sum(r['assessment']=='supported' for r in qualified),conservative_rejections=len(conservative))
    same(counts,summary['counts'],'Reconstructed summary counts')
    same(len({(r['s'],r['eta']) for r in acc}),summary['dynamical_conditions_in_prospective_test'],'Condition count')
    for campaign in campaigns['campaigns']:same(campaign['member_count'],len(campaign['members']),'Campaign membership count')
    # Every claim pointer is resolved; selected rows must have their intended
    # identities, not merely an existing position in an array.
    pointer_count=0; protocols=set()
    modelids={r['id'] for r in models['models']}
    for claim in claims['claims']:
        require(claim['model_id'] in modelids,'Unknown claim model')
        require('physical_control' in claim and claim['comparison'] and claim['uncertainty_method'],'Missing claim-specific metadata')
        for e in claim['evidence']:
            value=pointer(record(e['path']),e['json_pointer']);pointer_count+=1
            same(e['sha256'],artifacts[e['path']]['sha256'],'Claim hash: '+claim['id'])
            for k,v in e.get('expected_identity',{}).items():same(value[k],v,'Claim evidence identity: '+claim['id'])
            if claim['id']=='PA-ACC-01':require(value['population'] in ('exponential','gaussian512'),'Wrong qualified-family claim selection')
            if claim['id']=='PA-ACC-02' and e['path']=='results/accuracy.json':same(value['population'],'gaussian128','Wrong conservative claim selection')
        for protocol in claim['protocols']:
            require(protocol in artifacts,'Protocol missing from manifest: '+protocol);protocols.add(protocol)
    # Both article representations expose the same numeric text. Hash checks
    # alone would not catch a generator publishing the wrong number consistently.
    byid={r['id']:r for r in pop+acc+cost}; expected_cells=sum(3 for r in pop)+sum(7 for r in acc)
    for name in ('paper.html','paper.md'):
        parser=ArticleParser();parser.feed(fetch(name).decode());numeric_count=0;scalars=0
        for attrs,text in parser.values:
            if 'data-record' in attrs:
                rid=attrs['data-record'];field=attrs['data-field'];require(rid in byid and field in byid[rid],'Unknown article result pointer')
                same(text,format(byid[rid][field],'.9g'),f'{name}: article number {rid}/{field}');numeric_count+=1
            else:
                same(text,format(summary[attrs['data-publication-scalar']],'.6f'),f'{name}: article headline number');scalars+=1
        same(numeric_count,expected_cells,f'{name}: numeric-cell coverage');same(scalars,1,f'{name}: scalar coverage')
        require('The first-order contribution has known zero ensemble integral' not in fetch(name).decode(),'Obsolete estimator explanation')
        require('left-hand side is the generally nonzero transfer' in ''.join(parser.text),'Missing estimator distinction')
        if name.endswith('.html'):
            for claim in claims['claims']:require(claim['article_anchor'].split('#')[1] in parser.ids,'Unresolved article claim anchor')
            require(f'content="{version}"' in fetch(name).decode(),'Article release metadata')
    broad=next(r for r in cost if r['population']=='halo' and r['s']==.25 and r['time']==20)
    narrow=next(r for r in cost if r['population']=='stress0.015625' and r['s']==.25 and r['time']==20)
    return dict(release=version,expected_release=expected_release,activity='Publication consistency checking from supplied numerical records; no orbit evolution',population_late_magnitude_ratio=ratio,exponential_halo_point_difference_percent={str(t):100*abs(get('exponential',t)/get('halo',t)-1) for t in (10,20)},candidate_count=len(candidates),qualified_count=len(qualified),independently_supported=counts['supported_qualified'],qualified_contradicted=sum(r['assessment']=='contradicted' for r in qualified),distinct_new_conditions=1,conservative_rejections=conservative,unqualified_independently_outside=sum(not r['qualified'] and r['assessment']=='contradicted' for r in candidates),qualified_signs=sum(r['sign']!='unqualified' for r in candidates),supported_signs=sum(r['sign_assessment']=='supported' for r in candidates),broad_conditional_cost_variance_ratio=broad['cost_times_variance_ratio'],broad_between_batch_ratio=broad['between_batch_ratio'],narrow_ratio=narrow['cost_times_variance_ratio'],coverage=dict(manifest_artifacts_hashed=len(artifacts),claim_evidence_pointers=pointer_count,protocols=len(protocols),reconstructed_accuracy_rows=len(calculations),article_numeric_cells_per_representation=expected_cells,article_representations=['HTML','Markdown']),exclusions=['No simulation or array reproduction','No proof of numerical-proxy bounds or general confidence coverage','No verification of every external archive or historical explorer','No external scientific review, novelty or live-halo/SIDM validation'],decisions=calculations)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--origin',default='https://djova.ca/galaxy-bar/');p.add_argument('--expected-release');p.add_argument('--out');a=p.parse_args()
    reader=Reader(a.origin);result=verify(reader,a.expected_release);result['downloads']=reader.receipts
    if a.out:Path(a.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
