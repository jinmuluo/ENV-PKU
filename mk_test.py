import numpy as np


def mk_test(X, level):
    # X must be an array
    s = 0
    z = 0
    t = 0
    l = X.shape[0]
    Ds = l*(l-1)*(2*l+5)/18
    for i in range(l):
        for j in range(i, l):
            s = s + sgn(X[j], X[i])
    if s > 0:
        z = (s-1)/np.sqrt(Ds)
    elif s < 0:
        z = (s+1)/np.sqrt(Ds)
    if z > level:
        t = 1
    elif z < -level:
        t = -1
    return s, z, t


def sgn(xi, xj):
    result = 0
    if xi > xj:
        result = 1
    elif xi < xj:
        result = -1
    return result
