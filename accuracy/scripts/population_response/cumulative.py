"""Exact primitive of a positive piecewise-linear density approximation."""
import numpy as np
from profiles import weights


class Population:
    def __init__(self,x,w):
        self.x=np.asarray(x,dtype=float)
        self.w=np.asarray(w,dtype=float)
        self.dx=float(self.x[1]-self.x[0])
        if self.w.shape!=self.x.shape or not np.allclose(np.diff(self.x),self.dx,rtol=0,atol=1e-12):
            raise ValueError('Need uniform density nodes')
        if np.any(self.w<0) or not np.all(np.isfinite(self.w)) or self.w[0]!=0 or self.w[-1]!=0:
            raise ValueError('Need a finite nonnegative density vanishing at both ends')
        self.F=np.r_[0.,np.cumsum((self.w[:-1]+self.w[1:])*self.dx/2)]

    def evaluate(self,x):
        q=np.clip((np.asarray(x)-self.x[0])/self.dx,0,len(self.x)-1)
        index=np.minimum(q.astype(np.int64),len(self.x)-2)
        z=q-index
        delta=self.w[index+1]-self.w[index]
        w=self.w[index]+delta*z
        F=self.F[index]+self.dx*(self.w[index]*z+delta*z*z/2)
        return w,F

    def remainder(self,x,B):
        w,F=self.evaluate(x)
        _,shifted=self.evaluate(np.asarray(x)+B)
        return shifted-F-w*B


def physical_populations(meta,table,spacing=1/4096,J=96.):
    steps=int(round(2*J/spacing))
    if abs(steps*spacing-2*J)>1e-12:
        raise ValueError('Need integer grid coverage')
    x=np.linspace(-J,J,steps+1)
    populations={}
    for plateau,cutoff in [(24.,40.),(48.,64.)]:
        names=['gaussian','halo','exponential']
        w=weights(x,names,meta,table,plateau,cutoff)
        for name,value in zip(names,w):
            populations[f'{name}-{int(cutoff)}']=Population(x,value)
    return populations
