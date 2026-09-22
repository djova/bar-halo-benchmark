"""Plot recorded background moments; no simulation states are synthesized."""
import argparse
import hashlib
import json
from pathlib import Path
import time

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--result', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    cpu = time.process_time()
    data = json.loads(args.result.read_text())
    assert data['readback_checks_pass'] and data['coverage'] == dict(
        original_distributions=16, domain_replacements=4, stochastic_batches=24, groups=3)
    args.out.mkdir(parents=True, exist_ok=False)
    plt.rcParams.update({'font.size': 11, 'axes.titlesize': 13})
    rows = data['stochastic_groups']
    labels = [f"s = {r['s']:g}, η = {r['eta']:g}" for r in rows]
    y = np.arange(len(rows))
    fig, axes = plt.subplots(2, 1, figsize=(7, 7.4), layout='constrained')
    for index, row in enumerate(rows):
        known_se = np.sqrt(row['expected_noise_variance']/row['n'])
        mean_ci = np.array(row['mean_ci95_known_variance'])/known_se
        center = row['mean_standardized']
        axes[0].errorbar(center, index, xerr=np.array([[center-mean_ci[0]],
                         [mean_ci[1]-center]]), fmt='o', color='#276da0', capsize=4)
        ratio = row['variance_ratio']
        ci = np.array(row['variance_ci95'])/row['expected_noise_variance']
        axes[1].errorbar(ratio, index, xerr=np.array([[ratio-ci[0]], [ci[1]-ratio]]),
                         fmt='o', color='#276da0', capsize=4)
    axes[0].axvline(0, color='#555', ls='--', lw=1)
    axes[0].set(title='Do the kicks add an average push?',
                xlabel='Mean Brownian impulse / expected sampling error', xlim=(-2.5, 3.5))
    axes[1].axvline(1, color='#555', ls='--', lw=1)
    axes[1].set(title='Does the scatter match the specified noise strength?',
                xlabel='Measured variance / analytic variance', xlim=(.990, 1.010),
                xticks=[.99, .995, 1., 1.005, 1.01])
    for ax in axes:
        ax.set(yticks=y, yticklabels=labels, ylim=(2.5, -.5))
        ax.spines[['top', 'right']].set_visible(False)
    fig.suptitle('Bar off: compare the recorded kicks with their exact law', fontsize=14)
    fig.supxlabel('Each row: 262,144 paths across 8 seeds. Bars: pointwise 95% intervals.\n'
                  'Mean: known-variance normal interval. Variance: chi-square interval.\n'
                  'Rows reuse seeds; they are not independent conditions.', fontsize=8)
    for ext in ['png', 'pdf']:
        fig.savefig(args.out/f'unforced-noise-moments.{ext}', dpi=128)
    # A separate rendering of the same points keeps labels readable on phones.
    fig.set_size_inches(3.5, 7.4)
    fig.suptitle('Recorded kicks against\nthe specified noise law', fontsize=12)
    axes[0].set(title='Do the kicks add\nan average push?',
                xlabel='Mean kick / expected\nsampling error', xticks=[-2, 0, 2])
    axes[1].set(title='Does the scatter match\nthe specified strength?',
                xlabel='Measured / specified variance', xticks=[.99, 1., 1.01],
                xticklabels=['0.99', '1', '1.01'])
    for ax in axes:
        ax.set_yticklabels([f"s={r['s']:g}\nη={r['eta']:g}" for r in rows])
    fig.supxlabel('Each row: 262,144 paths; 8 seeds.\nBars: pointwise 95% intervals.\n'
                  'Normal mean; chi-square variance.\nRows reuse seeds; not independent.', fontsize=8)
    fig.savefig(args.out/'unforced-noise-moments-mobile.png', dpi=128)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5), layout='constrained')
    for index, s in enumerate([0., .1, .4, 1.2]):
        for variant, offset, color, marker, label in [
            ('original', -.10, '#b85223', 's', 'Original boundary: |j| < 64'),
            ('double_domain', .10, '#276da0', 'o', 'Moved boundary: |j| < 128'),
        ]:
            row = next(r for r in data['distribution_controls']
                       if r['s'] == s and r['eta'] == 1. and r['variant'] == variant)
            ax.scatter(abs(row['variance_error'])/1e-7, index+offset,
                       color=color, marker=marker, label=label if index == 0 else None)
    ax.set_xscale('log')
    ax.axvspan(2e-4, 1., color='#dce8e1', alpha=.6, zorder=0)
    ax.axvline(1., color='#555', ls='--', lw=1)
    ax.set(xlim=(2e-4, 100), ylim=(3.55, -.5), yticks=range(4),
           yticklabels=['s = 0', 's = 0.1', 's = 0.4', 's = 1.2'],
           xlabel='Absolute variance error / original tolerance (log scale)',
           title='Moving the boundary reduces the variance error\nBar-free distribution controls, η = 1')
    ax.legend(loc='lower right', fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)
    fig.supxlabel('Variance tolerance: 10⁻⁷ in squared action units; shaded region passes.\n'
                  'Original failures remain failed. The s = 0.4 original also fails the mean check.',
                  fontsize=8)
    for ext in ['png', 'pdf']:
        fig.savefig(args.out/f'unforced-boundary-check.{ext}', dpi=128)
    fig.set_size_inches(3.5, 5.6)
    ax.set(title='', xlabel='Variance error / original tolerance\n(log scale)',
           xticks=[.001, .1, 1., 100.], xticklabels=['0.001', '0.1', '1', '100'])
    ax.legend(loc='lower left', bbox_to_anchor=(0., 1.), fontsize=8.5, frameon=False)
    fig.suptitle('Moving the boundary\nreduces variance error', fontsize=12)
    fig.supxlabel('Bar-free η=1. Original tolerance: 10⁻⁷.\n'
                  'Shade: within variance criterion.\nOriginal failures remain failed.', fontsize=8)
    fig.savefig(args.out/'unforced-boundary-check-mobile.png', dpi=128)
    plt.close(fig)
    result = dict(input_sha256=hashlib.sha256(args.result.read_bytes()).hexdigest(),
                  plot_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  figures={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(args.out.iterdir())},
                  cpu_seconds=time.process_time()-cpu,
                  scope='Recorded moments and pointwise95% intervals only. Rows reuse '
                        'seed families, not independent conditions. Original boundary '
                        'failures are retained; bar-free checks do not qualify forced transfer.')
    (args.out/'result.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    main()
