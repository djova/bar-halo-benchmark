"""Check saved scientific operands, not orbital evolution or physical validity."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import time
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


class Check:
    def __init__(self):
        self.count = 0

    def equal(self, actual, expected, name, rtol=3e-11, atol=0):
        a, b = np.asarray(actual), np.asarray(expected)
        if not np.allclose(a, b, rtol=rtol, atol=atol, equal_nan=False):
            raise AssertionError(f'{name}: operands disagree')
        self.count += int(a.size)

    def true(self, condition, name):
        if not condition:
            raise AssertionError(name)
        self.count += 1


def summary(y):
    return dict(mean=float(np.mean(y)), standard_error=float(np.std(y, ddof=1)/np.sqrt(len(y))))


def moment(check, y, saved, name):
    for k, v in summary(y).items():
        check.equal(v, saved[k], name+'.'+k)


def field(record):
    return np.asarray(record['real'])+1j*np.asarray(record['imag'])


def warm(check, data, directory):
    w = data['warm_population']
    n = w['n']
    cutoff = w['inner_Rc_upper']
    mass = 1-(1+cutoff)*math.exp(-cutoff)
    check.equal(mass, w['inner_guiding_mass'], 'analytic guiding mass')
    with np.load(directory/'warm-fine-dilution.npz', allow_pickle=False) as z:
        check.true(z['Rc'].shape == (n,), 'fine count')
        inner = z['Rc'] < cutoff
        check.true(np.array_equal(inner, z['inner_mask']), 'guiding selection')
        check.equal(z['paired'], z['positive'][1:]-z['positive'][0], 'fine paired paths')
        for j, row in enumerate(w['original_fine_dilution']):
            for mode, y in [('paired', z['paired'][j]), ('actual_positive', z['positive'][j+1])]:
                r = row[mode]
                inside = y*inner
                moment(check, y, r['whole'], mode+'.whole')
                moment(check, inside, r['inner_absolute_per_whole_mass'], mode+'.inner')
                moment(check, y*(~inner), r['exterior_absolute_per_whole_mass'], mode+'.exterior')
                u = inside.mean()/y.mean()
                influence = y*(inner-u)/y.mean()
                check.equal(u, r['inner_fraction'], mode+'.fraction')
                check.equal(summary(influence)['standard_error'], r['fraction_delta_method_standard_error'], mode+'.paired ratio SE')
                check.equal(np.cov(np.array([inside, y]), ddof=1)/n, r['covariance_of_means'], mode+'.covariance')
    with np.load(directory/'warm-coarse-comparison.npz', allow_pickle=False) as z:
        check.true(z['Rc'].shape == (n,), 'coarse count')
        old, new = z['old_positive'], z['new_positive']
        for name, a in [('old', old), ('new', new)]:
            computed = z['guide_weight']*(z[name+'_forward_remainder']+z[name+'_inverse_capture'])/z['radial_q']
            check.equal(computed, a, name+'.positive remainder identity')
        yp, op = new[1:]-new[0], old[1:]-old[0]
        for row in w['arithmetic']['rows']:
            R = row['Rc_upper']
            mass = 1 if R is None else 1-(1+R)*math.exp(-R)
            mask = np.ones(n) if R is None else (z['Rc'] < R).astype(float)/mass
            j = [5, 8].index(row['frequency'])
            values = {'actual_positive':new[j+1], 'zero':new[0], 'new_paired':yp[j], 'old_paired':op[j],
                      'new_minus_old_paired':yp[j]-op[j], 'absolute_response_change':abs(yp[j]-op[j])}
            for name, a in values.items():
                moment(check, a*mask, row[name], 'coarse.'+name)
            check.equal(mass, row['exact_physical_mass'], 'cohort analytic normalization')
            check.equal(row['new_minus_old_paired']['mean']/row['old_paired']['mean'], row['relative_mean_change'], 'coarse relative change')
        columns = np.array([old[1], new[1], old[2], new[2], old[0], new[0], op[0], yp[0], op[1], yp[1]])
        for row in w['arithmetic']['covariance']:
            R = row['Rc_upper']
            mask = np.ones(n) if R is None else (z['Rc'] < R)/(1-(1+R)*math.exp(-R))
            check.equal(np.cov(columns*mask, ddof=1)/n, row['covariance_of_means'], 'coarse covariance')
    check.true(all(r['maximum']>r['allowance'] for r in w['original_inverse_failures']), 'original inverse failures retained')
    check.true(w['extended']['status']=='COST_PARTIAL' and not w['extended']['gate'], 'incomplete qualification retained')
    check.true(w['arithmetic']['gate'] and not w['arithmetic']['scientific_gate'], 'arithmetic distinct from science')


def echoes(check, data):
    e = data['echo_late']
    q = np.asarray(e['local_scale_Q'])
    for r in e['rows']:
        cases = field(r['case_values'])
        computed = np.array(e['forcing']['contrast_weights'])@cases
        # Direct signed accumulation and subtraction of rounded case fields
        # have different cancellation errors; retain the measured discrepancy.
        budget = r['direct_contrast_vs_case_sum_error']+8*np.finfo(float).eps*np.max(abs(cases))
        check.equal(computed, field(r['mixed']), 'four-case complex contrast', rtol=1e-12, atol=budget)
        check.equal(np.array(e['forcing']['contrast_weights'])@np.array(r['case_absolute_masses']), r['mixed_absolute_mass'], 'case mass contrast', rtol=0, atol=8*np.finfo(float).eps)
        check.true(r['grid_points']==math.prod(r['grid'].values()), 'full grid membership')
        if 'saved_leading_prediction' in r:
            lead = field(r['saved_leading_prediction'])
            check.equal(field(r['mixed'])-lead, field(r['signed_difference_from_leading']), 'cross leading signed difference', atol=1e-35)
            check.equal(abs(field(r['mixed'])-lead)/q, r['leading_difference_over_fixed_local_Q'], 'cross full complex local scale')
        if 'saved_leading_prediction_scaled' in r:
            lead = field(r['saved_leading_prediction_scaled'])
            check.equal(field(r['mixed'])-lead, field(r['signed_difference_from_leading_scaled']), 'leading signed difference', atol=1e-35)
            check.equal(abs(field(r['mixed'])-lead)/q, r['leading_difference_over_fixed_local_Q_scaled'], 'full complex local scale')
    names = ['coarse_E704_L4_eta16','cross_L8_eta16','cross_L4_eta32','fine_E704_L8_eta32']
    C, XL, XE, F = [field(next(r['mixed'] for r in e['rows'] if r['label']==name and r['time']==28)) for name in names]
    terms = dict(L_change_at_coarse_eta=XL-C, eta_change_at_coarse_L=XE-C,
                 joint_interaction=F-XL-XE+C, L_change_at_fine_eta=F-XE, eta_change_at_fine_L=F-XL)
    for name, v in terms.items():
        check.equal(v, field(e['cross_diagnosis']['signed_terms'][name]), 'cross.'+name, atol=1e-34)
        check.equal(abs(v)/q, e['cross_diagnosis']['term_magnitudes_over_fixed_local_Q'][name], 'cross scaled.'+name)
    check.equal(terms['L_change_at_coarse_eta']+terms['eta_change_at_coarse_L']+terms['joint_interaction'], F-C, 'operator algebra identity', atol=1e-34)
    diff = abs(F-C)/q
    check.equal(diff, e['original_failed_screen']['refinement_difference_over_fixed_local_Q'], 'retained original failure')
    check.true([bool(v<=.05) for v in diff]==e['original_failed_screen']['refinement_gate_components'], 'refinement decision')
    check.true(not e['original_failed_screen']['local_refinement_pass'], 'no convergence upgrade')


def forecasts(check, data):
    f = data['twin_forecast']
    stages = {s['id']:s for s in f['stages']}
    check.true(list(stages)==list('abcdefg'), 'all seven grids')
    for stage in stages.values():
        for r in stage['rows']:
            check.equal(sum(r['signed_inplane_contributions']), r['forecast'], 'signed spectral sum')
            check.equal(r['absolute_mode_contribution']/abs(r['forecast']), r['absolute_over_net'], 'cancellation')
    for r in f['qualifications']:
        final = next(a for a in stages['g']['rows'] if a['p']==r['p'])
        coarse = next(a for a in stages['f']['rows'] if a['p']==r['p'])
        action = next(a for a in stages['e']['rows'] if a['p']==r['p'])
        anomaly = abs(final['forecast']-coarse['forecast'])
        grid = abs(final['forecast']-action['forecast'])
        tail = final['tail_proxy_residual_norm']
        for name, v in [('forecast',final['forecast']), ('quadrature_change',anomaly), ('action_grid_change',grid),
                        ('tail_proxy',tail), ('combined_numerical_proxy',anomaly+grid+tail), ('target',.05*abs(final['forecast']))]:
            check.equal(v, r[name], 'forecast.'+name)
        check.true((anomaly+grid+tail <= r['target'])==r['numerical_5percent_proxy_qualified'], 'five percent proxy decision')
        check.true((anomaly+grid+tail < abs(final['forecast']))==r['sign_numerically_qualified'], 'numerical sign decision')
    check.true(f['no_forced_outcomes_read'] and f['status']=='sealed_forecast_driven_test_pending', 'prospective scope')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, default=ROOT/'data/checks-v2.json')
    p.add_argument('--operands', type=Path, default=ROOT/'operands/checks-v2')
    p.add_argument('--expected-release', default='discovery-2026-10-01.6')
    a = p.parse_args()
    start = time.process_time()
    data = json.loads(a.data.read_text())
    check = Check()
    check.true(data['release']==a.expected_release, 'requested release')
    manifest = json.loads((a.operands/'operand-manifest.json').read_text())
    for r in manifest['artifacts']:
        path = a.data if r['path']=='checks-v2.json' else a.operands/r['path']
        check.true(path.stat().st_size==r['bytes'], 'operand size')
        check.true(hashlib.sha256(path.read_bytes()).hexdigest()==r['sha256'], 'operand hash')
    warm(check, data, a.operands)
    echoes(check, data)
    forecasts(check, data)
    print(json.dumps(dict(status='PASS', compared_values=check.count, cpu_seconds=time.process_time()-start,
                         scope='Saved-array and recorded-value arithmetic only; no evolution, physical qualification or rigorous error bound.')))


if __name__=='__main__':
    main()
