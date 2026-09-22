"""Fourth-order time-extended Hamiltonian composition of Cartesian leapfrog."""
from orbit_kernel import Kernel as BaseKernel
import ctypes
import numpy as np

class Kernel(BaseKernel):
    def __init__(self,path):
        super().__init__(path)
        array=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
        self.lib.evolve_fourth.argtypes=[array,ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.c_double,array,array,array]
        self.lib.evolve_fourth.restype=None

    def evolve(self,states,steps,t,dt,p,torque,work):
        assert states.flags.c_contiguous and states.dtype==np.float64
        self.lib.evolve_fourth(states,len(states),steps,t,dt,np.ascontiguousarray(p,dtype=float),torque,work)
