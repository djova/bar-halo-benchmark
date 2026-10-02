"""Check published scalar-energy summaries; never evolve orbits or certify tails."""
from pathlib import Path
import argparse
import json
import time
import numpy as np


def run(path):
    start = time.process_time()
    d = json.loads(path.read_text())
    count = 0

    def equal(a, b, name):
        nonlocal count
        a, b = np.asarray(a), np.asarray(b)
        if not np.allclose(a, b, rtol=3e-12, atol=0, equal_nan=False):
            raise AssertionError(name)
        count += int(a.size)

    def require(a, name):
        nonlocal count
        if not a:
            raise AssertionError(name)
        count += 1

    require(d['schema'] == 'feedback-cusp-warm-native-v1', 'Known schema')
    require(d['sample']['n'] == 4096 and d['stellar_target']['total_mass'] == 1, 'Fixed sample and target mass')
    mass = 1 - 1.25*np.exp(-.25)
    equal(d['stellar_target']['inner_physical_mass'], mass, 'Analytical guiding mass')
    coarse, fine = d['numerical']['coarse_fine']
    require([s['name'] for s in [coarse, fine]] == ['coarse', 'fine'], 'Recorded map order')
    indexed = {}
    for stage in [coarse, fine]:
        gate = stage['inverse_scaled_error_maximum'] <= 1e-9
        require(stage['inverse_gate'] == gate and gate, 'All-state inverse scalar allowance')
        require(len(stage['capture_counts']) == 3 and all(x == 0 for x in stage['capture_counts']), 'Recorded capture counts')
        for r in stage['rows']:
            key = stage['name'], r['Rc_upper'], r['frequency']
            indexed[key] = r
            mu = r['paired']['mean']
            equal(r['actual_forward']['mean'], mu+r['zero']['mean'], 'Forward/paired/zero relation')
            tests = {
                'precision_gate': mu > 0 and r['paired']['standard_error'] <= .30*mu,
                'work_gate': r['absolute_energy_work']['mean'] <= .05*abs(mu),
                'direct_work_gate': r['direct_absolute_energy_work']['mean'] <= .05*abs(mu),
                'curvature_gate': abs(r['curvature_difference']['mean']) <= .01*abs(mu),
            }
            for label, expected in tests.items():
                require(bool(r[label]) == expected and expected, 'Reconstructed '+label)
    for r in d['numerical']['paired_timestep_action']:
        base = indexed['coarse', r['Rc_upper'], r['frequency']]['paired']['mean']
        mu = indexed['fine', r['Rc_upper'], r['frequency']]['paired']['mean']
        # Addition at the physical-mean scale avoids claiming tiny differences
        # reconstructed beyond the precision of the exported mean summaries.
        equal(base+r['fine_minus_coarse']['mean'], mu, 'Paired timestep mean identity')
        require(r['timestep_gate'] == (abs(r['fine_minus_coarse']['mean']) <= .05*abs(mu)), 'Timestep threshold')
        require(r['action_gate'] == (abs(r['action256_minus128']['mean']) <= .01*abs(mu)), 'Action threshold')
    for stage in d['numerical']['paired_original_arithmetic_changes']:
        for r in stage['rows']:
            mu = indexed[stage['name'], r['Rc_upper'], r['frequency']]['paired']['mean']
            require(r['numerical_change_gate'] == (r['absolute_change']['mean'] <= .01*abs(mu)), 'Arithmetic-change allowance')
    for j, row in enumerate(d['figure']['rows']):
        require(row['frequency'] in [5, 8], 'Recorded carrier only')
        for cohort, upper in [('whole', None), ('inner_guiding_Rc_lt_0_25', .25)]:
            reference = indexed['fine', upper, row['frequency']]
            for estimator in ['actual_forward', 'paired', 'ordinary_signed']:
                for operand in ['mean', 'standard_error']:
                    equal(row[cohort][estimator][operand], reference[estimator][operand], 'Figure/fine-map identity')
        equal(row['inner_guiding_Rc_lt_0_25']['physical_mass'], mass, 'Inner figure normalization')
        for name in ['paired', 'actual_forward']:
            q = d['dilution'][j][name]
            n, total = q['inner_absolute_per_whole_mass']['mean'], q['whole']['mean']
            exterior = q['exterior_absolute_per_whole_mass']
            cov = np.asarray(q['covariance_of_means'])
            equal(n+exterior['mean'], total, 'Absolute inner/exterior partition')
            equal(n/total, q['inner_fraction'], 'Contribution ratio')
            equal(np.sqrt(cov[0, 0]), q['inner_absolute_per_whole_mass']['standard_error'], 'Inner covariance diagonal')
            equal(np.sqrt(cov[1, 1]), q['whole']['standard_error'], 'Whole covariance diagonal')
            # Near unity, use the equivalent exterior-complement delta method.
            # Exported exterior SE supplies its stable variance, instead of
            # subtracting three nearly equal rounded covariance entries.
            outside_fraction = exterior['mean']/total
            var_outside = exterior['standard_error']**2
            cov_outside_total = cov[1, 1]-cov[0, 1]
            variance = (var_outside + outside_fraction**2*cov[1, 1]
                        - 2*outside_fraction*cov_outside_total)/total**2
            equal(np.sqrt(variance), q['fraction_delta_method_standard_error'], 'Stable covariance-aware ratio SE')
            equal(q['whole']['mean'], row['whole'][name]['mean'], 'Contribution/whole mean')
            equal(n/mass, row['inner_guiding_Rc_lt_0_25'][name]['mean'], 'Declared cohort normalization')
        for cohort in ['whole', 'inner_guiding']:
            q = d['signed_positive_agreement'][j][cohort]
            cov = np.asarray(q['covariance_of_means'])
            equal(q['positive_forward']['mean']+q['signed_minus_positive']['mean'], q['ordinary_signed']['mean'], 'Correlated estimator mean difference')
            equal(np.sqrt(cov[0, 0]+cov[1, 1]-2*cov[0, 1]), q['signed_minus_positive']['standard_error'], 'Paired estimator-difference SE')
    history = d['historical_outcomes']
    require(history['original_binary64_scientific_gate'] is False, 'Original failure retained')
    require(all(x > 1e-9 for x in history['original_binary64_inverse_failures']), 'Original inverse failures retained')
    require(history['first_all_state_numpy_extended'].startswith('COST_PARTIAL'), 'Stopped stage retained')
    require(history['reader01'].startswith('FAILED'), 'Reader01 failure retained')
    require(d['numerical']['scientific_gate'] is True and d['numerical']['reader_arithmetic_gate'] is True and not d['numerical']['failed_final_gates'], 'Recorded terminal native gates')
    return dict(status='PASS', scalar_comparisons=count,
                numerical_tolerance=dict(rtol=3e-12, atol=0),
                scope='Published summary arithmetic and scalar thresholds only; no raw-array re-contraction, trajectory reproduction, tail-coverage proof or observational validation.',
                ratio_uncertainty='Covariance-aware delta method using the stable exterior complement; rounded summary matrices limit attainable precision.',
                cpu_seconds=time.process_time()-start)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[2]/'data/warm-cost-v1.json')
    p.add_argument('--out', type=Path)
    a = p.parse_args()
    r = run(a.data)
    s = json.dumps(r, indent=2)+'\n'
    if a.out:
        a.out.write_text(s)
    print(s, end='')
