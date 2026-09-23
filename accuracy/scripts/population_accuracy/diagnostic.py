"""Frozen, uncertainty-aware gradient-mismatch diagnostic; not a rigorous bound.

The exact triangle inequality is rigorous. Its Monte Carlo Student-t envelopes
and measured numerical-refinement allowances are operational approximations.
No independence between bins or population contractions is assumed.
"""
from common import NAMES, WINDOWS, density
import numpy as np
from scipy.stats import t as student


def summarize(v, critical):
    v = np.asarray(v, float)
    if v.shape[0] != 8 or not np.all(np.isfinite(v)):
        raise ValueError('All eight independent batches are required')
    mean = v.mean(axis=0)
    half = critical*v.std(axis=0, ddof=1)/np.sqrt(8)
    return mean, half


def bounded_contraction(q, qc, weights, critical):
    dw = np.diff(weights)
    r = -q @ dw
    step = -(q-qc) @ dw
    mean, half = summarize(r, critical)
    step_mean, step_half = summarize(step, critical)
    coarse_r = -q.reshape(8, -1, 2).mean(axis=2) @ np.diff(weights[::2])
    mesh = 2*float(np.max(abs(r-coarse_r)))
    numerical = abs(float(step_mean))+float(step_half)+mesh
    return dict(mean=float(mean), sampling_half=float(half), batches=r.tolist(),
                step_mean=float(step_mean), step_half=float(step_half),
                doubled_maximum_mesh_change=mesh,
                numerical_proxy=numerical, total_allowance=float(half)+numerical)


def envelope(q, qc, critical):
    mean, half = summarize(q, critical)
    change, change_half = summarize(q-qc, critical)
    return abs(mean)+half+abs(change)+change_half


def assess(edges, fine, coarse, meta, table):
    """All six populations, two times and two physical windows, one dynamics."""
    if fine.shape != coarse.shape or fine.shape != (8, 2, len(edges)-1):
        raise ValueError('Expected eight paired batches and both fixed endpoints')
    if len(edges) % 2 != 1 or not np.all(np.diff(edges) > 0):
        raise ValueError('Ordered, factor-two coarsenable kernel required')
    # 2 times x {Q, Qfine-Qcoarse}; reserve alpha=.025 for this family.
    kernel_tests = 4*(len(edges)-1)
    kernel_critical = float(student.ppf(1-.025/(2*kernel_tests), 7))
    # 6 profiles x 2 times x 2 windows x {response, timestep, window}.
    # Window timestep is also estimated: reserve a fourth scalar family.
    scalar_tests = 4*len(NAMES)*2*len(WINDOWS)
    scalar_critical = float(student.ppf(1-.025/(2*scalar_tests), 7))
    weights = {(name, int(cut)): density(edges, meta, table, name, plateau, cut)
               for plateau, cut in WINDOWS for name in NAMES}
    if any(w[0] != 0 or w[-1] != 0 for w in weights.values()):
        raise ValueError('Boundary terms are nonzero or physical support is missing')
    rows = []
    for ti, tau in enumerate((10., 20.)):
        q, qc = fine[:, ti], coarse[:, ti]
        upper = envelope(q, qc, kernel_critical)
        q2, qc2 = (v.reshape(8, -1, 2).mean(axis=2) for v in (q, qc))
        upper2 = envelope(q2, qc2, kernel_critical)
        for _, cut in WINDOWS:
            cut = int(cut)
            h = weights['halo', cut]
            halo = bounded_contraction(q, qc, h, scalar_critical)
            halo_abs_lower = max(0., abs(halo['mean'])-halo['total_allowance'])
            halo_window = bounded_contraction(q, qc, weights['halo', 64]-weights['halo', 40], scalar_critical)
            halo_window_allowance = abs(halo_window['mean'])+halo_window['total_allowance']
            for name in NAMES:
                w = weights[name, cut]
                approximate = bounded_contraction(q, qc, w, scalar_critical)
                mismatch = np.diff(w-h)
                plugin = float(abs(mismatch) @ abs(q.mean(axis=0)))
                expanded = float(abs(mismatch) @ upper)
                coarse_expanded = float(abs(np.diff((w-h)[::2])) @ upper2)
                mesh_addition = 2*abs(expanded-coarse_expanded)
                approximation_allowance = expanded+mesh_addition
                combined = approximation_allowance+approximate['total_allowance']
                window = bounded_contraction(q, qc, weights[name, 64]-weights[name, 40], scalar_critical)
                window_allowance = abs(window['mean'])+window['total_allowance']
                paired_mean, paired_half = summarize(-(q @ mismatch), scalar_critical)
                sign = 'positive' if approximate['mean'] > combined else (
                    'negative' if approximate['mean'] < -combined else 'unqualified')
                mag = bool(halo_abs_lower > 0 and combined <= .05*halo_abs_lower)
                shared_window_allowance = max(window_allowance, halo_window_allowance)
                shared = bool(halo_abs_lower > 0 and combined+shared_window_allowance <= .05*halo_abs_lower)
                rows.append(dict(tau=tau, population=name, cutoff=cut,
                    approximate=approximate, halo=halo,
                    paired_error_mean=float(paired_mean), paired_error_half=float(paired_half),
                    plugin_mismatch=plugin, expanded_mismatch=expanded,
                    doubled_mismatch_mesh_change=mesh_addition,
                    approximation_allowance=approximation_allowance,
                    combined_response_allowance=combined,
                    window=window, window_allowance=window_allowance,
                    halo_window_allowance=halo_window_allowance,
                    halo_absolute_lower=halo_abs_lower,
                    five_percent_absolute_target=.05*halo_abs_lower,
                    sign_qualification=sign,
                    five_percent_qualified=mag,
                    five_percent_across_windows_qualified=shared))
    return dict(rows=rows, kernel_critical=kernel_critical, scalar_critical=scalar_critical,
                kernel_tests=kernel_tests, scalar_tests=scalar_tests,
                scope='Nominal simultaneous Student-t batch envelopes plus practical numerical-refinement proxies. Not a distribution-free bound or certified truncation estimate. The gradient triangle inequality is exact only for the true kernel and specified boundary treatment. Six frozen profiles, both endpoints and both windows; no absolute floor in the five-percent test.')
