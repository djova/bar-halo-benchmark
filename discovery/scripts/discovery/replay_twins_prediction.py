"""Reconstruct saved weak-twin arithmetic; never integrate orbits or certify coverage."""
from pathlib import Path
import argparse
import json
import time
import numpy as np


def run(path):
    start = time.process_time()
    data = json.loads(path.read_text())
    e, u = data['endpoint_data'], data['uncertainty']
    count = 0

    def equal(actual, expected, name, rtol=3e-11, atol=0):
        nonlocal count
        a, b = np.asarray(actual), np.asarray(expected)
        if not np.allclose(a, b, rtol=rtol, atol=atol, equal_nan=False):
            raise AssertionError(name + ': saved operands disagree')
        count += int(a.size)

    def require(value, name):
        nonlocal count
        if not value:
            raise AssertionError(name)
        count += 1

    require(e['six_order'] == ['full_p4', 'full_p6', 'full_p8', 'half_p4', 'half_p6', 'half_p8'], 'Frozen six-response order')
    raw = e['raw_libraries']
    require(len(raw) == 8 and [r['library_id'] for r in raw] == list(range(8)), 'Eight distinct ordered libraries')
    six = np.asarray([r['six_endpoint_responses'] for r in raw])
    joint = np.asarray([r['nine_joint_endpoint_values'] for r in raw])
    equal(joint[:, :6], six, 'Shared six-component operands')
    equal(joint[:, 6:], six[:, :3] - 4*six[:, 3:], 'Paired full-minus-four-half operands')
    covariance = np.cov(joint, rowvar=False, ddof=1)
    equal(covariance, e['sample_covariance_nine_by_nine'], 'Sample covariance')
    equal(covariance/8, e['covariance_of_mean_nine_by_nine'], 'Covariance of mean')
    means, se = joint.mean(axis=0), joint.std(axis=0, ddof=1)/np.sqrt(8)
    critical, pointwise = u['nominal_family_critical'], u['nominal_pointwise_critical']
    require(u['degrees_of_freedom'] == 7 and u['family_size'] == 9, 'Frozen family size')
    equal(critical, 3.946683866320812, 'Frozen nominal family critical constant')
    equal(pointwise, 2.364624251592784, 'Frozen nominal pointwise critical constant')
    numerical = []
    classifications = []
    signs = 0
    for i, row in enumerate(e['comparisons']):
        refinement = [r for r in e['refinement_operands'] if r['p'] == row['p'] and r['amplitude'] == row['amplitude']]
        require(len(refinement) == 2 and {r['library_id'] for r in refinement} == {0, 1}, 'Paired refinement coverage')
        step = 2*max(abs(r['half_timestep_contrast'] - r['base_contrast']) for r in refinement)
        phase = 2*max(abs(r['sixteen_phase_contrast'] - r['base_contrast']) for r in refinement)
        n = step + phase
        numerical.append(n)
        sampling = critical*se[i]
        f = next(r for r in data['forecast']['full_amplitude_qualifications'] if r['p'] == row['p'])
        factor = (row['amplitude']/data['forcing']['epsilon_full'])**2
        forecast, proxy = factor*f['forecast'], factor*f['combined_numerical_proxy']
        lower = max(abs(means[i])-sampling-n, 0)
        upper = abs(means[i])+sampling+n
        allowance = sampling+n+proxy
        delta = means[i]-forecast
        decision = 'supported' if abs(delta)+allowance <= .05*lower else 'contradicted' if abs(delta)-allowance > .05*upper else 'unresolved'
        values = dict(mean=means[i], standard_error=se[i], forecast=forecast,
                      numerical_step_proxy=step, numerical_phase_proxy=phase,
                      sampling_envelope=sampling, numerical_proxy=n, forecast_proxy=proxy,
                      actual_signal_lower=lower, actual_signal_upper=upper,
                      discrepancy=delta, target_lower=.05*lower, target_upper=.05*upper,
                      combined_allowance=allowance)
        for name, value in values.items():
            equal(value, row[name], 'Endpoint.'+name)
        equal([means[i]-pointwise*se[i], means[i]+pointwise*se[i]], row['pointwise95_interval'], 'Pointwise interval')
        equal([means[i]-sampling, means[i]+sampling], row['nominal_family95_interval'], 'Family sampling interval')
        require(decision == row['assessment'], 'Magnitude classification')
        require((abs(means[i]) > sampling+n) == row['direct_sign_qualified'], 'Direct sign classification')
        require(f['numerical_5percent_proxy_qualified'] == row['forecast_numerically_qualified'], 'Forecast proxy scope')
        signs += int(row['direct_sign_qualified'])
        classifications.append(decision)
    scaling = []
    for i, row in enumerate(e['paired_amplitude_scaling']):
        j = i+6
        sampling = critical*se[j]
        n = numerical[i]+4*numerical[i+3]
        lower = e['comparisons'][i]['actual_signal_lower']
        upper = e['comparisons'][i]['actual_signal_upper']
        allowance = sampling+n
        decision = 'supported' if abs(means[j])+allowance <= .05*lower else 'contradicted' if abs(means[j])-allowance > .05*upper else 'unresolved'
        for name, value in dict(mean_full_minus4half=means[j], standard_error=se[j],
                                discrepancy=means[j], sampling_envelope=sampling,
                                numerical_proxy=n, forecast_proxy=0.,
                                combined_allowance=allowance,
                                actual_full_signal_lower=lower, actual_full_signal_upper=upper,
                                target_lower=.05*lower, target_upper=.05*upper).items():
            equal(value, row[name], 'Paired amplitude.'+name)
        require(decision == row['assessment'], 'Amplitude-law classification')
        scaling.append(decision)
    for lib in raw:
        for amplitude in ['full', 'half']:
            for row in lib['population_transfer_context'][amplitude]:
                equal(row['plus']-row['minus'], row['contrast'], 'Context contrast')
                equal((row['plus']+row['minus'])/2, row['reference'], 'Context reference')
    history = data['recorded_history']
    require(history['times'] == list(range(41)), 'Only 41 recorded integer epochs')
    curves = np.asarray([r['recorded_time_six_contrasts'] for r in history['raw_library_curves']])
    require(curves.shape == (8, 41, 6) and np.isfinite(curves).all(), 'Complete finite recorded histories')
    equal(curves[:, 0], np.zeros((8, 6)), 'Initial accumulated response')
    equal(curves[:, -1], six, 'History/endpoint identity')
    require(data['claims']['direct_signs_qualified'] == signs == 6, 'Sign count')
    require(classifications.count('unresolved') == data['claims']['five_percent_magnitude_forecasts_unresolved'] == 6, 'Unresolved magnitude count')
    require(scaling.count('supported') == data['claims']['paired_second_order_amplitude_checks_supported'] == 3, 'Amplitude-law count')
    return dict(status='PASS', scalar_comparisons=count,
                direct_signs_qualified=signs, magnitude_decisions=classifications,
                paired_amplitude_decisions=scaling, recorded_history_shape=list(curves.shape),
                scope='Saved-operand arithmetic only; no orbit integration, full-array reproduction, coverage calibration, or physical validation.',
                numerical_tolerance=dict(rtol=3e-11, atol=0), cpu_seconds=time.process_time()-start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[2]/'data/twins-prediction-v1.json')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = run(args.data)
    text = json.dumps(result, indent=2)+'\n'
    if args.out:
        args.out.write_text(text)
    print(text, end='')
