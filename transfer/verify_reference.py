"""Verify the declared means, numerical shifts and decisions against the release."""
from pathlib import Path
import argparse,json

def verify(actual,reference):
    measurements=[];decisions=[]
    labels=[case['label'] for case in actual['cases']]
    reference_labels=[case['label'] for case in reference['cases']]
    assert len(labels)==len(set(labels)) and set(labels)==set(reference_labels), 'Missing, duplicate or unexpected cases'
    def measured(name,x,y):
        difference=abs(x-y)
        measurements.append(dict(quantity=name,reproduced=x,reference=y,absolute_difference=difference))
        assert difference<1e-9,(name,difference)
    def same(name,x,y):
        decisions.append(dict(quantity=name,reproduced=x,reference=y,agrees=x==y))
        assert x==y,(name,x,y)
    for case in actual['cases']:
        label=case['label'];ref=next(r for r in reference['cases'] if r['label']==label)
        settings=[row['setting'] for row in case['refinements']]
        expected=[row['setting'] for row in ref['refinements']]
        assert len(settings)==len(set(settings)) and set(settings)==set(expected), 'Incomplete refinement comparison'
        assert set(case['unforced'])==set(ref['unforced']), 'Incomplete unforced controls'
        for key in ['raw_3D','paired_reduced','discrepancy']:
            measured(label+'.'+key+'.mean',case[key]['mean'],ref[key]['mean'])
        for row in case['refinements']:
            rr=next(r for r in ref['refinements'] if r['setting']==row['setting'])
            for key in ['raw_3D_shift','discrepancy_shift']:
                measured(label+'.'+row['setting']+'.'+key,row[key]['mean'],rr[key]['mean'])
            same(label+'.'+row['setting']+'.local_pass',row['local_pass'],rr['local_pass'])
        for key in ['local_pass','numerical_point_changes_pass','numerical_sampling_intervals_pass','extension_trigger','decision']:
            same(label+'.'+key,case[key],ref[key])
        for name,d in case['unforced'].items():
            same(label+'.'+name+'.gates',d['gates'],ref['unforced'][name]['gates'])
    return dict(all_pass=True,absolute_tolerance=1e-9,measurements=measurements,decisions=decisions,
                scope='Same-seed reproduction of declared scalar means, numerical shifts and decisions. '
                'Individual raw-array differences require a separate archive comparison; '
                'the original failed numerical qualification remains failed.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--result',type=Path,required=True)
    p.add_argument('--reference',type=Path,default=Path(__file__).parent/'reference/initial-transfer-analysis.json')
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    d=verify(json.loads(a.result.read_text()),json.loads(a.reference.read_text()))
    with a.out.open('x') as f:f.write(json.dumps(d,indent=2)+'\n')
    print(json.dumps(d,indent=2))

if __name__=='__main__':main()
