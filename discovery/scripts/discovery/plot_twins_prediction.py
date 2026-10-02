"""Standalone figures from real saved weak-twin operands; no trajectories generated."""
from pathlib import Path
import argparse
import json
import resource
resource.setrlimit(resource.RLIMIT_CPU, (29, 30))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = ['#80bfff', '#ffd080', '#7ad8bd']


def main(data_path, out):
    data = json.loads(data_path.read_text())
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'figure.facecolor': '#10202e', 'axes.facecolor': '#10202e',
                         'axes.edgecolor': '#536477', 'axes.labelcolor': '#d8e4ed',
                         'text.color': '#d8e4ed', 'xtick.color': '#afbdcc', 'ytick.color': '#afbdcc',
                         'font.size': 11, 'grid.color': '#334558', 'savefig.facecolor': '#10202e'})
    rows = data['endpoint_data']['comparisons']
    fig, ax = plt.subplots(figsize=(9.7, 6.3))
    for i, r in enumerate(rows):
        ax.errorbar(r['mean']/1e-10, i-.11,
                    xerr=(r['sampling_envelope']+r['numerical_proxy'])/1e-10,
                    fmt='o', color=COLORS[0], capsize=3,
                    label='Direct: nominal family sampling + numerical proxy' if i == 0 else None)
        ax.errorbar(r['forecast']/1e-10, i+.11, xerr=r['forecast_proxy']/1e-10,
                    fmt='D', color=COLORS[1], markerfacecolor=COLORS[1] if r['forecast_numerically_qualified'] else '#10202e',
                    capsize=3, label='Sealed forecast: unforced numerical proxy' if i == 0 else None)
        ax.text(3.35, i, 'Unresolved', va='center', fontsize=10)
    ax.set_yticks(range(6), [f"p{r['p']} · {'full' if r['amplitude'] == data['forcing']['epsilon_full'] else 'half'}" for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(-.17, 4.05)
    ax.set_xticks([0, 1, 2, 3])
    ax.axvline(0, color='#93a8bc', lw=1)
    ax.grid(axis='x', ls=':', lw=.8)
    ax.set_xlabel(r'Accumulated $\Delta L_{z,+}-\Delta L_{z,-}$ ($10^{-10}$ action units)')
    ax.set_title('All six direct signs are positive; all six 5% magnitudes remain unresolved', fontsize=12, pad=80)
    ax.legend(loc='lower left', bbox_to_anchor=(0, 1.03), fontsize=9, facecolor='#10202e', labelcolor='#d8e4ed', framealpha=.95)
    fig.text(.12, .01, 'Endpoint 40 · full/half amplitude 0.0001/0.00005 · target population mass 1\nHollow p4 forecast: tail unqualified; interval overlap is not 5% validation.', fontsize=9)
    fig.subplots_adjust(left=.14, right=.98, top=.77, bottom=.18)
    fig.savefig(out/'twins-direct-endpoints-v1.png', dpi=160)
    plt.close(fig)

    history = np.asarray([r['recorded_time_six_contrasts'] for r in data['recorded_history']['raw_library_curves']])
    times = np.asarray(data['recorded_history']['times'])
    means = history.mean(axis=0)
    se = history.std(axis=0, ddof=1)/np.sqrt(len(history))
    critical = data['uncertainty']['nominal_pointwise_critical']
    minimum = min(0, history.min(), (means-critical*se).min())
    maximum = max(0, history.max(), (means+critical*se).max())
    pad = (maximum-minimum)*.1
    fig, ax = plt.subplots(figsize=(9.4, 5.3))
    column = data['recorded_history']['six_order'].index('full_p6')
    for curve in history[:, :, column]:
        ax.plot(times, curve/1e-10, color='#8497a9', alpha=.42, lw=.8)
    ax.fill_between(times, (means[:, column]-critical*se[:, column])/1e-10,
                    (means[:, column]+critical*se[:, column])/1e-10,
                    color=COLORS[0], alpha=.18, label='Nominal pointwise sampling interval')
    ax.plot(times, means[:, column]/1e-10, 'o-', ms=3, color=COLORS[0], lw=1.5, label='Mean at 41 saved epochs')
    ax.set_ylim((minimum-pad)/1e-10, (maximum+pad)/1e-10)
    ax.axhline(0, color='#93a8bc', lw=.8)
    ax.grid(ls=':', lw=.8)
    ax.set_xlabel('Recorded isochrone model time (separate from galaxy Gyr)')
    ax.set_ylabel(r'Accumulated transfer contrast ($10^{-10}$ action units)')
    ax.set_title('Published default: p6, full amplitude, fixed target mass 1', fontsize=12)
    ax.legend(fontsize=9, facecolor='#10202e', labelcolor='#d8e4ed')
    fig.text(.12, .01, 'Lines guide the eye between actual records; shading is not simultaneous-in-time coverage.\nAll six endpoint-40 magnitude decisions remain unresolved. The website shares one y scale across selections.', fontsize=9)
    fig.subplots_adjust(left=.12, right=.97, bottom=.2, top=.89)
    fig.savefig(out/'twins-direct-history-v1.png', dpi=160)
    plt.close(fig)

    rows = data['endpoint_data']['paired_amplitude_scaling']
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    for i, r in enumerate(rows):
        ax.errorbar(r['mean_full_minus4half']/1e-16, i,
                    xerr=(r['sampling_envelope']+r['numerical_proxy'])/1e-16,
                    fmt='o', color=COLORS[i], capsize=4)
        ax.text(-7.8, i+.23, 'Paired amplitude law supported', fontsize=9)
    ax.set_yticks(range(3), [f"p = {r['p']}" for r in rows])
    ax.invert_yaxis()
    ax.set_xlim(-8, 8)
    ax.set_ylim(2.45, -.4)
    ax.set_xticks([-8, -4, 0, 4, 8])
    ax.axvline(0, color='#93a8bc', lw=1)
    ax.grid(axis='x', ls=':', lw=.8)
    ax.set_xlabel(r'$C_\epsilon-4C_{\epsilon/2}$ ($10^{-16}$ action units)')
    ax.set_title('Halving the amplitude supports a quarter-size response', fontsize=12, pad=12)
    fig.text(.12, .01, 'Whiskers: nominal family sampling + paired numerical proxy; residual magnified.\nRegistered 5% targets are far outside this view. This tests amplitude dependence, not forecast accuracy.', fontsize=9)
    fig.subplots_adjust(left=.12, right=.97, bottom=.24, top=.88)
    fig.savefig(out/'twins-direct-scaling-v1.png', dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[2]/'data/twins-prediction-v1.json')
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    main(a.data, a.out)
