"""Compare the two shared-input evaluations and plot the actual differences."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();cpu=time.process_time()
    paths=[a.root/name/'result.json' for name in ['original','rebuilt']]
    original,rebuilt=[json.loads(p.read_text()) for p in paths]
    assert original['reference_sha256']==rebuilt['reference_sha256']
    assert original['source_sha256']==rebuilt['source_sha256']
    assert len(original['rows'])==len(rebuilt['rows'])==544
    pairs=list(zip(original['rows'],rebuilt['rows']))
    for x,y in pairs:
        assert all(x[k]==y[k] for k in ['case','group','index','Js','h','plus_action','minus_action'])
        for row in [x,y]:
            for k in ['df_plus','df_minus']:
                assert row[k]==float.fromhex(row[k+'_hex']) and row[k]>0
    rows=[]
    for h in [1e-5,2e-5,4e-5,8e-5]:
        chosen=[(x,y) for x,y in pairs if x['h']==h]
        difference=np.array([y['ordinary_slope']-x['ordinary_slope'] for x,y in chosen])
        precise=np.array([y['high_precision_same_inputs']-x['high_precision_same_inputs'] for x,y in chosen])
        logs=np.array([y['logarithm_arithmetic_error']-x['logarithm_arithmetic_error'] for x,y in chosen])
        original_difference=np.array([x['ordinary_slope']-x['archived_slope'] for x,y in chosen])
        values=[abs(y[k]-x[k])/abs(x[k]) for x,y in chosen for k in ['df_plus','df_minus']]
        rows.append(dict(h=h,n=len(chosen),maximum_cross_build_slope_difference=float(abs(difference).max()),
            maximum_cross_build_precise_log_difference=float(abs(precise).max()),
            maximum_differential_log_arithmetic_error=float(abs(logs).max()),
            maximum_df_relative_difference=float(max(values)),
            same_df_pair_count=sum(x['df_plus_hex']==y['df_plus_hex'] and x['df_minus_hex']==y['df_minus_hex'] for x,y in chosen),
            maximum_original_vs_archived_slope_difference=float(abs(original_difference).max()) if h==1e-5 else None,
            maximum_decomposition_residual=float(abs(difference-precise-logs).max())))
    assert rows[0]['maximum_original_vs_archived_slope_difference']==0
    assert all(r['maximum_decomposition_residual']<1e-13 for r in rows)
    a.out.mkdir(parents=True,exist_ok=False)
    fig,axes=plt.subplots(1,2,figsize=(10.5,4.4),layout='constrained')
    for label,color in [('A','#135c91'),('B','#bf4d28')]:
        chosen=[(x,y) for x,y in pairs if x['h']==1e-5 and x['group']=='scan' and x['case']==label]
        js=[x['Js'] for x,y in chosen]
        ordinary=[(y['ordinary_slope']-x['ordinary_slope'])*1e9 for x,y in chosen]
        precise=[(y['high_precision_same_inputs']-x['high_precision_same_inputs'])*1e9 for x,y in chosen]
        axes[0].plot(js,ordinary,color=color,lw=1.6,label=f'{label}: ordinary logs')
        axes[0].scatter(js,precise,s=9,color=color,marker='x',label=f'{label}: 50-digit logs')
    axes[0].set(xlabel='Original slow action Js',ylabel='Rebuilt − original DF log slope (×10⁻⁹)',
                title='The log-arithmetic correction is small')
    axes[0].axhline(0,color='.7',lw=.7);axes[0].legend(fontsize=8)
    h=np.array([r['h'] for r in rows])
    axes[1].loglog(h,[r['maximum_cross_build_slope_difference'] for r in rows],'o-',label='Total slope difference')
    axes[1].loglog(h,[r['maximum_cross_build_precise_log_difference'] for r in rows],'x--',label='Using 50-digit logs')
    axes[1].loglog(h,[r['maximum_differential_log_arithmetic_error'] for r in rows],'s-',label='Log-arithmetic contribution')
    axes[1].set_xticks(h, ['1','2','4','8'])
    axes[1].xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    axes[1].set(xlabel='Finite-difference offset h in Js (×10⁻⁵)',ylabel='Maximum absolute difference across 136 rows',
                title='The difference persists at larger offsets')
    axes[1].legend(fontsize=8);axes[1].grid(alpha=.2)
    fig.suptitle('Unforced calibration: the dominant difference is in the returned DF values',fontsize=12)
    fig.savefig(a.out/'calibration-arithmetic.png',dpi=180)
    fig.savefig(a.out/'calibration-arithmetic.pdf')
    plt.close(fig)
    result=dict(rows=rows,source_sha256=sha(__file__),input_sha256={p.parent.name:sha(p) for p in paths},
        original_library_sha256=original['agama_library_sha256'],rebuilt_library_sha256=rebuilt['agama_library_sha256'],
        evaluation_cpu_seconds=original['cpu_seconds']+rebuilt['cpu_seconds'],analysis_cpu_seconds=time.process_time()-cpu,
        conclusion='On identical action inputs, the full original slope discrepancy repeats. Using50-digit logs retains it; subtraction roundoff is a small contribution. The dominant difference is already in the returned DF values. This does not isolate its origin inside the dependency.',
        limitations='Original100/1304failed checks remain failed. Larger offsets change truncation error. High precision applies only to logs of binary64 DF values, not to the DF construction. No original forecast or trajectory changes.')
    (a.out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(conclusion=result['conclusion'],analysis_cpu_seconds=result['analysis_cpu_seconds'])))


if __name__=='__main__':main()
