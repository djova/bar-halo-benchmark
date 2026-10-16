"""Exact AST-selected frozen scientific functions; same-code port, not independent validation."""
import math


def tensor_basis(np):
    basis = np.zeros((5, 3, 3))
    basis[0] = np.diag([1., -1., 0.])/math.sqrt(2)
    for index, (i, j) in enumerate(((0, 1), (0, 2), (1, 2)), 1):
        basis[index, i, j] = basis[index, j, i] = 1/math.sqrt(2)
    basis[4] = np.diag([-1., -1., 2.])/math.sqrt(6)
    return basis


def gegenbauer(z, alpha, count, np):
    values = [np.ones_like(z)]
    if count > 1:
        values.append(2*alpha*z)
    for n in range(2, count):
        values.append((2*(n+alpha-1)*z*values[-1]-(n+2*alpha-2)*values[-2])/n)
    return np.stack(values, axis=-1)


def profiles(x, np, jets=False):
    s = np.sum(x*x, axis=1)
    psi = 1/np.sqrt(1+s)
    z = (s-1)/(s+1)
    c = gegenbauer(z, 3, 7, np)
    cp = np.column_stack([np.zeros_like(s), 6*gegenbauer(z, 4, 6, np)])
    a, ap = -psi**5, 2.5*psi**7
    zp = 2*psi**4
    f = a[:, None]*c
    fs = ap[:, None]*c+(a*zp)[:, None]*cp
    if not jets:
        return f, 2*fs
    cpp = np.column_stack([np.zeros((len(s), 2)), 48*gegenbauer(z, 5, 5, np)])
    cppp = np.column_stack([np.zeros((len(s), 3)), 480*gegenbauer(z, 6, 4, np)])
    app, appp = -8.75*psi**9, 39.375*psi**11
    zpp, zppp = -4*psi**6, 12*psi**8
    fss = app[:, None]*c+(2*ap*zp+a*zpp)[:, None]*cp+(a*zp*zp)[:, None]*cpp
    fsss = (appp[:, None]*c+(3*app*zp+3*ap*zpp+a*zppp)[:, None]*cp
             +(3*ap*zp*zp+3*a*zp*zpp)[:, None]*cpp+(a*zp**3)[:, None]*cppp)
    return f, fs, fss, fsss
