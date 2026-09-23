"""Population-response primitive from measured bar displacements.

R_w(x,B)=integral w'(z) q(x,B,z) dz. q is a one-sided triangle,
not an orbit history. Its height at x is |B| and its height at x+B is zero.
"""
import numpy as np


def primitive_kernel(grid,initial,impulse,quadrature_weight):
    grid=np.asarray(grid);initial=np.asarray(initial);impulse=np.asarray(impulse)
    if not np.all(np.diff(grid)>0):
        raise ValueError('Kernel coordinates must increase')
    end=initial+impulse
    first=np.searchsorted(grid,np.minimum(initial,end),side='left')
    stop=np.searchsorted(grid,np.maximum(initial,end),side='right')
    sign=np.sign(impulse)
    intercept=sign*end*quadrature_weight
    slope=-sign*quadrature_weight
    def accumulate(value):
        change=np.bincount(first,weights=value,minlength=len(grid)+1)
        change-=np.bincount(stop,weights=value,minlength=len(grid)+1)
        return np.cumsum(change[:-1])
    return accumulate(intercept)+grid*accumulate(slope)


def contract_primitive(grid,Q,w):
    """Discrete integral w dQ; w must vanish at both physical window edges."""
    if len(grid)!=len(Q) or len(grid)!=len(w) or not np.all(np.diff(grid)>0):
        raise ValueError('Weights and kernel must share ordered coordinates')
    if abs(w[0])>1e-14 or abs(w[-1])>1e-14:
        raise ValueError('Keep the boundary term or use the full physical support')
    return np.sum((w[:-1]+w[1:])/2*np.diff(Q))


def primitive_cell_average(edges,initial,impulse,quadrature_weight):
    """Exact cell averages of the sampled triangles, including their jumps."""
    initial=np.asarray(initial);impulse=np.asarray(impulse);edges=np.asarray(edges)
    end=initial+impulse
    lo=np.minimum(initial,end);hi=np.maximum(initial,end)
    first=np.searchsorted(edges,lo,side='left')
    stop=np.searchsorted(edges,hi,side='right')
    sign=np.sign(impulse)
    quadratic=-sign/2
    linear=sign*end
    constant=-linear*lo-quadratic*lo**2
    area=impulse**2/2*quadrature_weight
    def accumulate(value,after=None):
        value=value*quadrature_weight
        delta=np.bincount(first,weights=value,minlength=len(edges)+1)
        delta-=np.bincount(stop,weights=value,minlength=len(edges)+1)
        if after is not None:
            delta+=np.bincount(stop,weights=after,minlength=len(edges)+1)
        return np.cumsum(delta[:-1])
    S=accumulate(constant,area)+edges*accumulate(linear)+edges**2*accumulate(quadratic)
    return np.diff(S)/np.diff(edges)


def contract_cells(edges,Qaverage,w):
    if len(edges)!=len(Qaverage)+1 or len(edges)!=len(w):
        raise ValueError('Need weights on edges and kernel averages in cells')
    if abs(w[0])>1e-14 or abs(w[-1])>1e-14:
        raise ValueError('Keep the boundary term or use the full physical support')
    return -np.sum(Qaverage*np.diff(w))
