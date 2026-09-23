"""Evaluate all frozen accuracy decisions against independently evolved populations."""
from common import ROOT, NAMES, sha
from analyze_refinement import read_matrix, noisy_B
import argparse
import json
import time
from pathlib import Path
import numpy as np


def absolute_test(value, uncertainty, allowance):
    """Three-way decision; a tolerance overlap is not a confirmation."""
    if abs(value)+uncertainty <= allowance:
        return 'supported'
    if max(0.,abs(value)-uncertainty) > allowance:
        return 'contradicted'
    return 'inconclusive'


def relative_test(value, uncertainty, reference, reference_uncertainty, fraction=.05):
    lower = max(0.,abs(reference)-reference_uncertainty)
    upper = abs(reference)+reference_uncertainty
    if lower>0 and abs(value)+uncertainty <= fraction*lower:
        return 'supported'
    if max(0.,abs(value)-uncertainty) > fraction*upper:
        return 'contradicted'
    return 'inconclusive'


def main():
    p = argparse.ArgumentParser()
    for name in ('matrix','forecast','out'):
        p.add_argument('--'+name,type=Path,required=True)
    a = p.parse_args()
    start = time.process_time()
    records = read_matrix(a.matrix)
    forecast = json.loads(a.forecast.read_text())
    if len(records) != 14 or len(forecast['rows']) != 24 or forecast['developmental']:
        raise ValueError('Complete prospective matrix and family required')
    if any(r['forecast_sha256'] != sha(a.forecast) for r in records.values()):
        raise ValueError('Changed forecast')
    local = all(r['all_pass'] for r in records.values())
    rows = []
    for ti,tau in enumerate((10.,20.)):
        def c(key,name,cut):
            r = records['smooth-'+key]
            return float(r['remainder_bar_impulse'][ti][r['populations'].index(name+'-'+str(cut))])
        def n(key,name):
            return float(noisy_B(records['noisy-'+key],tau)[list(NAMES).index(name)])
        details = {}
        for cut in (40,64):
            for name in NAMES:
                nb,nf,nh,nd = ('base','fine','halfstep','domain') if cut==40 else ('wide','wide-fine','wide-halfstep','wide-domain')
                changes = dict(characteristic_quadrature=c('finer',name,cut)-c('fine',name,cut),
                    characteristic_timestep=c('halfstep',name,cut)-c('base',name,cut),
                    characteristic_domain=c('domain',name,cut)-c('base',name,cut),
                    noisy_mesh=n(nf,name)-n(nb,name),noisy_timestep=n(nh,name)-n(nb,name),
                    noisy_domain=n(nd,name)-n(nb,name))
                details[name,cut] = dict(response=n(nf,name)-c('finer',name,cut),changes=changes,
                    numerical_proxy=sum(abs(v) for v in changes.values()),
                    retained_characteristic_base_fine=c('fine',name,cut)-c('base',name,cut))
        for prediction in [r for r in forecast['rows'] if r['tau']==tau]:
            name,cut = prediction['population'],prediction['cutoff']
            actual,halo = details[name,cut],details['halo',cut]
            paired_changes = {key:actual['changes'][key]-halo['changes'][key] for key in actual['changes']}
            paired_numerical = sum(abs(v) for v in paired_changes.values())
            difference = actual['response']-halo['response']
            bound_check = absolute_test(difference,paired_numerical,prediction['approximation_allowance'])
            halo_lower = max(0.,abs(halo['response'])-halo['numerical_proxy'])
            halo_upper = abs(halo['response'])+halo['numerical_proxy']
            forecast_error = prediction['approximate']['mean']-halo['response']
            if abs(forecast_error)+halo['numerical_proxy'] <= .05*halo_lower and halo_lower>0:
                five_percent = 'supported'
            elif max(0.,abs(forecast_error)-halo['numerical_proxy']) > .05*halo_upper:
                five_percent = 'contradicted'
            else:
                five_percent = 'inconclusive'
            intrinsic_error = relative_test(difference,paired_numerical,halo['response'],halo['numerical_proxy'])
            independent_sign = 'positive' if halo['response']>halo['numerical_proxy'] else (
                'negative' if halo['response']<-halo['numerical_proxy'] else 'unresolved')
            predicted_sign = prediction['sign_qualification']
            sign_check = ('not_qualified' if predicted_sign=='unqualified' else
                'inconclusive' if independent_sign=='unresolved' else
                'supported' if predicted_sign==independent_sign else 'contradicted')
            self_prediction_error = prediction['approximate']['mean']-actual['response']
            self_check = absolute_test(self_prediction_error,actual['numerical_proxy'],prediction['approximate']['total_allowance'])
            window_change = details[name,64]['response']-details[name,40]['response']
            shared_five = five_percent
            # Shared-window qualification must hold against the other independently
            # evolved halo as well, rather than ignoring the selected physical taper.
            other_halo = details['halo',104-cut]
            other_lower = max(0.,abs(other_halo['response'])-other_halo['numerical_proxy'])
            other_error = prediction['approximate']['mean']-other_halo['response']
            other_test = relative_test(other_error,other_halo['numerical_proxy'],other_halo['response'],other_halo['numerical_proxy'])
            if 'contradicted' in (five_percent,other_test):
                shared_five = 'contradicted'
            elif 'inconclusive' in (five_percent,other_test):
                shared_five = 'inconclusive'
            if not local:
                bound_check=five_percent=intrinsic_error=sign_check=self_check=shared_five='unqualified_numerics'
            rows.append(dict(tau=tau,population=name,cutoff=cut,forecast=prediction,
                independent=actual,independent_halo=halo,
                paired_population_error=difference,paired_numerical_changes=paired_changes,
                paired_numerical_proxy=paired_numerical,gradient_allowance_test=bound_check,
                forecast_minus_independent_halo=forecast_error,
                independent_five_percent_test=five_percent,
                intrinsic_population_five_percent_test=intrinsic_error,
                independent_sign=independent_sign,sign_test=sign_check,
                self_prediction_error=self_prediction_error,self_prediction_test=self_check,
                independent_physical_window_change=window_change,
                independent_shared_window_five_percent_test=shared_five,
                all_local_gates_pass=local))
    candidate = [r for r in rows if r['population']!='halo']
    totals = dict(all_comparisons=len(rows),candidate_comparisons=len(candidate),
        qualified_signs=sum(r['forecast']['sign_qualification']!='unqualified' for r in candidate),
        false_qualified_signs=sum(r['sign_test']=='contradicted' for r in candidate),
        qualified_five_percent=sum(r['forecast']['five_percent_qualified'] for r in candidate),
        false_five_percent_qualifications=sum(r['forecast']['five_percent_qualified'] and r['independent_five_percent_test']=='contradicted' for r in candidate),
        supported_five_percent_qualifications=sum(r['forecast']['five_percent_qualified'] and r['independent_five_percent_test']=='supported' for r in candidate),
        inconclusive_five_percent_qualifications=sum(r['forecast']['five_percent_qualified'] and r['independent_five_percent_test'] not in ('supported','contradicted') for r in candidate),
        conservative_five_percent_rejections=sum(not r['forecast']['five_percent_qualified'] and r['independent_five_percent_test']=='supported' for r in candidate))
    result = dict(rows=rows,counts=totals,forecast_sha256=sha(a.forecast),
        inputs={str(p):sha(p) for p in [a.matrix/'manifest.json',a.matrix/'ledger.json',*sorted(a.matrix.glob('*/result.json'))]},
        source_sha256=sha(__file__),cpu_seconds=time.process_time()-start,
        scope='All frozen comparisons, including failures and inconclusive tests. Numerical refinements are practical proxies, not rigorous bounds. Twenty candidate comparisons share one new dynamical kernel; four halo self-comparisons are numerical references, not additional physical confirmations. No extrapolation to live haloes or SIDM.')
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(totals,indent=2))


if __name__ == '__main__':
    main()
