"""Positive physical weights at fixed central density; never normalize the mass."""
from pathlib import Path
import hashlib
import json
import numpy as np


def load_table(directory):
    directory = Path(directory)
    meta = json.loads((directory / 'result.json').read_text())
    raw = directory / 'halo-table.npz'
    if not meta['all_pass'] or hashlib.sha256(raw.read_bytes()).hexdigest() != meta['raw_sha256']:
        raise ValueError('Unqualified or changed unforced halo table')
    with np.load(raw) as d:
        table = {k: d[k].copy() for k in d.files}
    return meta, table


def taper(x, plateau, cutoff):
    if not 0 < plateau < cutoff:
        raise ValueError('Require 0 < plateau < cutoff')
    z = (np.abs(x) - plateau) / (cutoff - plateau)
    out = np.zeros_like(x, dtype=float)
    out[z <= 0] = 1
    inside = (z > 0) & (z < 1)
    a = np.exp(-1 / z[inside])
    b = np.exp(-1 / (1 - z[inside]))
    out[inside] = b / (a + b)
    return out


def weights(x, names, meta, table, plateau=24., cutoff=40.):
    x = np.asarray(x)
    if x.min() < table['x'].min() or x.max() > table['x'].max():
        raise ValueError('No extrapolation outside the unforced DF table')
    window = taper(x, plateau, cutoff)
    g = meta['g']
    halo = np.exp(np.interp(x, table['x'], np.log(table['df']))) / meta['f_ref']
    available = {
        'gaussian': np.exp(g*x - x*x/128) * window,
        'halo': halo * window,
        'exponential': np.exp(g*x) * window,
        'gaussian_untapered': np.exp(g*x - x*x/128),
    }
    out = np.stack([available[name] for name in names])
    if not np.all(np.isfinite(out)) or np.any(out < 0):
        raise ValueError('Physical initial weights must be finite and positive')
    return out
