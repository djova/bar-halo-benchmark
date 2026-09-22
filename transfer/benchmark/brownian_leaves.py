"""Nested canonical Brownian increments retaining the original two-leaf stream."""
import numpy as np

def increments(seed,block,n,start,D,h,refinement):
    if refinement not in (1,2,4,8):raise ValueError('Declared refinements are1,2,4,8')
    base=np.random.default_rng(np.random.SeedSequence([seed,2,block])).normal(size=(start+n,2))[start:].T
    if refinement==1:return [np.sqrt(D*h)*(base[0]+base[1])]
    values=np.sqrt(D*h)*base
    level=0
    while len(values)<refinement:
        count=len(values)
        bridge=np.random.default_rng(np.random.SeedSequence([seed,3,block,level])).normal(size=(start+n,count))[start:].T
        delta=np.sqrt(D*h/(2*count))*bridge
        finer=np.empty((count*2,n))
        finer[0::2]=values/2+delta;finer[1::2]=values/2-delta
        values=finer;level+=1
    return list(values)
