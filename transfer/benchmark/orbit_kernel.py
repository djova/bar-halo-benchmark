"""ctypes interface and separate NumPy reference field for the 3D benchmark."""
from pathlib import Path
import ctypes
import numpy as np


def energy(jr,jz,js):
    L=jz+2*js;I=jr+(L+np.sqrt(L*L+2))/2
    return -.5/(I*I)


def reference(states,t,p):
    amplitude,jr,jz,js0,speed=p;L=jz+2*(js0+speed*t);I=jr+(L+np.sqrt(L*L+2))/2
    omega=.5*(1+L/np.sqrt(L*L+2))/I**3
    angle=omega*t if speed==0 else (energy(jr,jz,js0+speed*t)-energy(jr,jz,js0))/(2*speed)
    c,s=np.cos(2*angle),np.sin(2*angle);x=states[:,:3];r=np.linalg.norm(x,axis=1);z=np.sqrt(.25+r*r)
    Q=(x[:,0]**2-x[:,1]**2)*c+2*x[:,0]*x[:,1]*s
    C=-amplitude*.42**2/(2*.34**2)*(1.28/(.28+r/.34))**5
    gradQ=np.column_stack((2*x[:,0]*c+2*x[:,1]*s,-2*x[:,1]*c+2*x[:,0]*s,np.zeros(len(x))))
    bg=-x/(z*(.5+z)**2)[:,None]
    radial=np.divide(-5*C*Q,(.28*.34+r)*r,out=np.zeros_like(r),where=r>0)
    force=bg-C[:,None]*gradQ-radial[:,None]*x
    torque=np.cross(x,force)[:,2]
    return np.column_stack((-1/(.5+z)+C*Q,force,omega*torque,torque))


class Kernel:
    def __init__(self,path):
        self.lib=ctypes.CDLL(str(Path(path).resolve()))
        array=np.ctypeslib.ndpointer(dtype=np.float64,flags='C_CONTIGUOUS')
        self.lib.evaluate.argtypes=[array,ctypes.c_int,ctypes.c_double,array,array]
        self.lib.evaluate.restype=None
        self.lib.evolve.argtypes=[array,ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.c_double,array,array,array]
        self.lib.evolve.restype=None

    def evaluate(self,states,t,p):
        states=np.ascontiguousarray(states,dtype=float);p=np.ascontiguousarray(p,dtype=float);out=np.empty_like(states)
        self.lib.evaluate(states,len(states),t,p,out);return out

    def evolve(self,states,steps,t,dt,p,torque,work):
        assert states.flags.c_contiguous and states.dtype==np.float64
        self.lib.evolve(states,len(states),steps,t,dt,np.ascontiguousarray(p,dtype=float),torque,work)
