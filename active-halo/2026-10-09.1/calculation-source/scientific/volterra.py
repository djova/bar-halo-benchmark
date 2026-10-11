"""Retarded convolution, independent of the old orbit-generator Schur solve.

K maps total potential coefficient history to induced potential coefficients.
Numerical backend is injected. Raw K(0) is retained, including Ward error.
"""
import time


def solve(kernel,drive,dt,np,guard=None,checkpoint=None,self_gravity=1):
    if kernel.ndim!=3 or drive.ndim!=2 or kernel.shape[0]!=len(drive) or kernel.shape[1:]!=(drive.shape[1],)*2:
        raise ValueError('Kernel [time,out,in] and drive [time,in] required')
    if dt<=0 or not np.all(np.isfinite(kernel)) or not np.all(np.isfinite(drive)):
        raise ValueError('Finite retarded operands and positive step required')
    count,channels=drive.shape
    response=np.zeros_like(drive,dtype=complex)
    total=drive.astype(complex).copy()
    if self_gravity not in (0,1):raise ValueError('Explicit bare or own-field solve required')
    lhs=np.eye(channels)-self_gravity*dt*kernel[0]/2
    if np.linalg.cond(lhs)>1e10:raise ArithmeticError('Unresolved retarded endpoint solve')
    last=time.monotonic()
    for j in range(1,count):
        rhs=dt*(kernel[j]@total[0]/2+kernel[0]@drive[j]/2)
        if j>1:rhs+=dt*np.einsum('tbi,ti->b',kernel[1:j][::-1],total[1:j],optimize=False)
        response[j]=np.linalg.solve(lhs,rhs)
        total[j]+=self_gravity*response[j]
        if time.monotonic()-last>20:
            if guard:guard.check()
            if checkpoint:checkpoint(j,response[:j+1])
            last=time.monotonic()
    return response


def pulse(t,duration,rise,fall,shape,pattern_speed,np):
    if min(duration,rise,fall)<=0 or rise+fall>duration:raise ValueError('Complete positive cycle required')
    x=np.minimum(np.minimum(t/rise,(duration-t)/fall),1.)
    x=np.maximum(x,0.)
    amp=shape*x**3*(10-15*x+6*x*x)
    sign=np.where(t<rise,1/rise,np.where(t>duration-fall,-1/fall,0.))
    adot=shape*30*x*x*(1-x)**2*sign
    angular=np.exp(-2j*pattern_speed*t)
    return amp*angular,(adot-2j*pattern_speed*amp)*angular,adot*angular
