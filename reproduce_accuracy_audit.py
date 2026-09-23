"""Recompute the paired retrospective assessment from historical statistics."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent/'accuracy'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    out=a.out.resolve()
    manifest=json.loads((ROOT/'source-manifest.json').read_text())
    for path,expected in manifest.items():
        if sha(ROOT/path)!=expected:
            raise ValueError('Changed released file '+path)
    subprocess.run([sys.executable,str(ROOT/'scripts/population_accuracy/audit_existing.py'),
        '--out',str(out)],cwd=ROOT,check=True)
    actual=json.loads((out/'result.json').read_text());reference=json.loads((ROOT/'retrospective/reference.json').read_text())
    keys=['historical_forecast_assessment','exponential_halo','estimator_variance']
    checks={key:actual[key]==reference[key] for key in keys}
    receipt=dict(all_scientific_values_reproduced=all(checks.values()),groups=checks,
        source_manifest_sha256=sha(ROOT/'source-manifest.json'),
        extracted_statistics_provenance_sha256=sha(ROOT/'retrospective/extraction.json'),
        scope='Exact paired arithmetic reproduction from recorded historical mean/covariance statistics. This does not rerun the original orbital dynamics or supply new physical samples; use the separate population and held-out commands for those experiments.')
    (out/'reproduction.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if not receipt['all_scientific_values_reproduced']:
        raise SystemExit('Retrospective scientific values differ; retained records require review')
    print('All paired retrospective scientific values reproduced exactly.')


if __name__=='__main__':
    main()
