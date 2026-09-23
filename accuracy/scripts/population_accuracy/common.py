"""Imports and immutable positive populations for the accuracy campaign."""
import os
for _key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_key] = '1'
from pathlib import Path
import hashlib
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/population_response'))
from profiles import load_table, taper
from cumulative import Population

NAMES = ('halo', 'exponential', 'gaussian8', 'gaussian32', 'gaussian128', 'gaussian512')
WINDOWS = ((24., 40.), (48., 64.))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def density(x, meta, table, name, plateau=24., cutoff=40.):
    x = np.asarray(x)
    if name == 'halo':
        if x.min() < table['x'][0] or x.max() > table['x'][-1]:
            raise ValueError('No halo-table extrapolation')
        w = np.exp(np.interp(x, table['x'], np.log(table['df']))) / meta['f_ref']
    elif name == 'exponential':
        w = np.exp(meta['g'] * x)
    elif name in NAMES and name.startswith('gaussian'):
        sigma = float(name.removeprefix('gaussian'))
        w = np.exp(meta['g'] * x - x*x/(2*sigma*sigma))
    else:
        raise ValueError(name)
    return w * taper(x, plateau, cutoff)


def populations(meta, table, spacing=1/8192):
    x = np.linspace(-96, 96, round(192/spacing)+1)
    return {f'{name}-{int(cutoff)}': Population(x, density(x, meta, table, name, plateau, cutoff))
            for plateau, cutoff in WINDOWS for name in NAMES}
