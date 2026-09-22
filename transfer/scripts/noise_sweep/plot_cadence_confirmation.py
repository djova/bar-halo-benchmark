"""Display the complete independent confirmation beside the retained first test."""
import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--analysis', type=Path, required=True)
    parser.add_argument('--original-analysis', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert (args.root/'TERMINAL').exists(), 'Only a complete matrix may be plotted'
    ledger = json.loads((args.root/'ledger.json').read_text())
    assert len(ledger['cases']) == 20
    assert all(row['state'] == 'complete' for row in ledger['cases'].values())
    current = json.loads(args.analysis.read_text())
    original = json.loads(args.original_analysis.read_text())
    assert current['manifest_sha256'] == sha(args.root/'manifest.json')
    assert current['n'] == 131072 and original['n'] == 16384
    margin = current['numerical_margin']
    assert margin == original['numerical_margin'] == 1.8126730139721574e-7
    pairs = {}
    for label in ['candidate', 'halfcadence', 'halfstep']:
        chunks = []
        starts = [65536] if label == 'halfstep' else [65536, 98304, 131072, 163840]
        for start in starts:
            vectors = []
            for kind in ['noisy', 'smooth']:
                name = f'{label}-{kind}' if label == 'halfstep' else f'{label}-{start}-{kind}'
                folder = args.root/name
                record = current['source_sha256'][name]
                assert sha(folder/'result.json') == record['result_sha256']
                assert sha(folder/'recorded.npz') == record['raw_sha256']
                with np.load(folder/'recorded.npz') as saved:
                    ids = saved['particle_ids'].copy()
                    vectors.append((saved['final_bar_Lz'].copy(),
                                    saved['final_reduced_bar_Lz'].copy()))
                count = 16384 if label == 'halfstep' else 32768
                assert np.array_equal(ids, np.arange(start, start+count))
            x = vectors[0][0]-vectors[1][0]
            y = vectors[0][1]-vectors[1][1]
            chunks.append((x, x-y))
        pairs[label] = tuple(np.concatenate([chunk[i] for chunk in chunks]) for i in range(2))

    plt.rcParams.update({'font.size': 11, 'figure.dpi': 160,
                         'axes.spines.top': False, 'axes.spines.right': False})
    fig, axes = plt.subplots(2, 1, figsize=(5.6, 9.6))
    tailfig, tailaxes = plt.subplots(2, 1, figsize=(5.6, 9.0))
    records = []
    bounds = [-1.1, 1.1]
    for data in [original, current]:
        for row in data['refinements']:
            for key in ['raw_3D_shift', 'discrepancy_shift']:
                bounds.extend(v/margin for v in row[key]['ci95'])
    lo, hi = min(bounds), max(bounds)
    pad = .08*(hi-lo)
    for j, (key, measure) in enumerate([
            ('raw_3D_shift', '3D noise effect'),
            ('discrepancy_shift', '3D minus paired reduced\nnoise effect')]):
        ax = axes[j]
        ax.axvspan(-1, 1, color='#87ad91', alpha=.2)
        ax.axvline(0, color='.5', lw=.7)
        for boundary in [-1, 1]:
            ax.axvline(boundary, color='#527b5c', ls=':', lw=1)
        labels = []
        for i, setting in enumerate(['halfstep', 'halfcadence']):
            setting_name = 'Half step' if setting == 'halfstep' else 'Half cadence'
            for version, data in enumerate([original, current]):
                row = next(r for r in data['refinements'] if r['setting'] == setting)
                m = row[key]
                ci = np.asarray(m['ci95'])/margin
                mean = m['mean']/margin
                assert np.isfinite([mean, *ci]).all() and ci[0] <= mean <= ci[1]
                inside = max(abs(ci)) < 1
                assert bool(m['interval_pass']) == bool(inside)
                color = '#737373' if version == 0 else ('#1671a5' if inside else '#aa5026')
                y = 2*i+version
                ax.errorbar(mean, y, xerr=[[mean-ci[0]], [ci[1]-mean]],
                            fmt='o' if version == 0 else 's', color=color, capsize=4)
                n = 131072 if version == 1 and setting == 'halfcadence' else 16384
                labels.append(f'{setting_name}\n{"Original" if version == 0 else "New"} · N = {n:,}')
                records.append(dict(sample='original' if version == 0 else 'independent',
                                    setting=setting, estimator=key, n=n,
                                    mean_over_margin=float(mean), interval_over_margin=ci.tolist(),
                                    interval_pass=bool(inside)))
            new = next(r for r in current['refinements'] if r['setting'] == setting)[key]
            values = pairs[setting][j]-pairs['candidate'][j][:len(pairs[setting][j])]
            assert abs(float(values.mean())-new['mean']) < 1e-15
            square = np.sort((values-values.mean())**2)[::-1]
            cumulative = np.cumsum(square)/square.sum() if square.sum() else np.ones(len(square))
            assert abs(float(cumulative[19])-new['largest20_variance_fraction']) < 1e-12
            tailaxes[j].semilogx(np.arange(1, len(square)+1), 100*cumulative,
                                color=['#1671a5', '#aa5026'][i],
                                label=f'{setting_name} · N = {len(square):,}')
        ax.set(yticks=range(4), yticklabels=labels, ylim=(3.6, -.6),
               xlim=(lo-pad, hi+pad), title=measure,
               xlabel='Numerical change / fixed allowance')
        ax.grid(axis='x', alpha=.15)
        tailaxes[j].set(title=measure, ylim=(0, 101),
                        xlabel='Paths ranked by squared deviation\n(all retained)',
                        ylabel='Cumulative share of measured variance (%)')
        tailaxes[j].legend(frameon=False, fontsize=9, loc='lower right')
        tailaxes[j].grid(alpha=.15)
    fig.suptitle('Does the full numerical interval fit\ninside the shaded band?', fontsize=12)
    fig.text(.04, .055, 'Original and new samples are disjoint; they are not pooled.\n'
             'Bars: nominal pointwise 95% Student-t intervals.\nDots/squares: means.', fontsize=9)
    fig.text(.04, .015, 'Numerical qualification alone does not validate\nthe physical prediction.', fontsize=9)
    fig.tight_layout(rect=(0, .11, 1, .95))
    tailfig.suptitle('How concentrated is the new sample’s\nnumerical uncertainty?', fontsize=12)
    tailfig.text(.04, .012, 'Measured tail concentration is descriptive.\nNo paths are removed or replaced.', fontsize=9)
    tailfig.tight_layout(rect=(0, .055, 1, .95))
    args.out.mkdir(parents=True, exist_ok=False)
    for plot, name in [(fig, 'confirmation-comparison'), (tailfig, 'confirmation-variance')]:
        for suffix in ['png', 'pdf']:
            plot.savefig(args.out/f'{name}.{suffix}')
        plt.close(plot)
    result = dict(analysis_sha256=sha(args.analysis), original_analysis_sha256=sha(args.original_analysis),
                  source_sha256=sha(Path(__file__)), numerical_margin=margin, records=records,
                  numerically_qualified=current['numerically_qualified'],
                  scope='Display only: unchanged complete-sample estimates and criteria. '
                        'Original failure retained; no physical qualification or rigorous error bound.')
    (args.out/'result.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
