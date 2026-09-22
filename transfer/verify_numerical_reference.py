"""Compare a clean numerical-matrix reproduction without changing its gates."""
from pathlib import Path
import argparse,json,math

def verify(actual,reference):
    assert actual['n']==reference['n']==16384
    assert actual['numerical_margin']==reference['numerical_margin']
    assert actual['forecast_sha256']==reference['forecast_sha256']
    assert actual['scientific_source_sha256']==reference['scientific_source_sha256']
    assert actual['gates']==reference['gates']
    assert actual['numerically_qualified']==reference['numerically_qualified']
    records=[]
    def compare(label,x,y):
        assert x['n']==y['n']==16384
        for key in ['mean','se','half_width']:
            assert math.isfinite(x[key]) and math.isfinite(y[key]);error=abs(x[key]-y[key]);assert error<1e-9,(label,key,error)
            records.append(dict(quantity=label+'.'+key,absolute_difference=error))
        assert all(math.isfinite(v) for v in [*x['ci95'],*y['ci95']])
        errors=[abs(a-b) for a,b in zip(x['ci95'],y['ci95'])]
        assert len(x['ci95'])==len(y['ci95'])==2 and max(errors)<1e-9
        records.append(dict(quantity=label+'.ci95',maximum_absolute_difference=max(errors)))
    for key in ['candidate_raw_3D','candidate_reduced','candidate_discrepancy']:compare(key,actual[key],reference[key])
    for data in [actual,reference]:
        assert len(data['refinements'])==2
        assert {row['setting'] for row in data['refinements']}=={'halfstep','halfcadence'}
    for row in actual['refinements']:
        ref=next(r for r in reference['refinements'] if r['setting']==row['setting'])
        for key in ['raw_3D_shift','discrepancy_shift','reduced_shift']:compare(row['setting']+'.'+key,row[key],ref[key])
    for key in ['candidate','halfstep','halfcadence']:
        for setting in ['actual_microstep','noise_cadence']:
            assert actual['actual_settings'][key][setting]==reference['actual_settings'][key][setting]
    return dict(all_pass=True,absolute_tolerance=1e-9,measurements=records,gates_agree=True,
                numerical_qualification=actual['numerically_qualified'],
                scope='Same-seed clean reproduction, not an independent physical sample. '
                'The numerical qualification and original operational margin remain unchanged. '
                'Individual-array differences require the separate archive comparison.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--result',type=Path,required=True)
    p.add_argument('--reference',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    result=verify(json.loads(a.result.read_text()),json.loads(a.reference.read_text()))
    with a.out.open('x') as f:f.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
