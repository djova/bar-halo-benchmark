"""Frozen positive test shapes; physical densities, not sampling proposals."""
import numpy as np
from profiles import taper
from cumulative import Population

NAMES=['gaussian12','gaussian20','quartic20']


def density(x,g,name,plateau=24.,cutoff=40.):
    x=np.asarray(x,float)
    if name=='gaussian12':logw=g*x-x*x/(2*12**2)
    elif name=='gaussian20':logw=g*x-x*x/(2*20**2)
    elif name=='quartic20':logw=g*x-x**4/(2*20**4)
    else:raise ValueError('Unknown frozen held-out population')
    return np.exp(logw)*taper(x,plateau,cutoff)


def populations(meta,spacing=1/8192,J=96.):
    n=round(2*J/spacing)
    if abs(n*spacing-2*J)>1e-12:raise ValueError('Need integer mesh coverage')
    x=np.linspace(-J,J,n+1);out={}
    for plateau,cutoff in [(24.,40.),(48.,64.)]:
        for name in NAMES:
            out[f'{name}-{int(cutoff)}']=Population(x,density(x,meta['g'],name,plateau,cutoff))
    return out
