#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import numpy as np
from .libzhang import factorial

def sigma(m=0,N=0,l=None,symm='es'):

    if symm == 'es' or symm == 'ES':

        p = np.zeros(2*N+1)

        fac = factorial(2*(2*N+m))/( factorial(2*N+m) * factorial(2*N) )

        p[0] = fac * (m+2*N)
        p[1] = -fac * 2*N

        for j in range(1, N+1):


            fac = -fac * ( (N-j+1.) * (2.* (N-j)+1.) / ( j*(2*(2.*N+m-j)+1.) ) )

            if (j == N):
                p[2*j] = fac * (m + 2*N - 2*j)
            else:
                p[2*j] = fac * (m + 2*N - 2*j)
                p[2*j + 1] = -fac * 2 * (N-j)

        sig = np.roots(p)

    if symm == 'ea' or symm == 'EA':

        p = np.zeros(2*N+2)

        fac = factorial(2*(2*N+m+1))/( factorial(2*N+m+1) * factorial(2*N+1 ) )

        p[0] = fac * (m+2*N+1)
        p[1] = -fac * (2*N+1)

        for j in range(1, N+1):

            j1 = j-1
            fac = -fac * ( (N-j+1.) * (2.* (N-j)+3.) / ( j*(2*(2.*N+m-j1)+1.) ) )

            p[2*j] = fac * (m + 2*N - 2*j + 1)
            p[2*j+1] = -fac * (2*N - 2*j + 1)

        sig = np.roots(p)

    return sig

def get_mode_sigma(om = 0.,m=2,Nmax=4,symm='es',info='lm'):

    sig = om/2.
    if (symm=='es' or symm=='ES'):
        for N in range(1, Nmax+1):
            l = 2*N + m
            sig_test = sigma(m = m, N = N, symm=symm)
            idx = np.argmin(abs(sig - sig_test))
            if info == 'lm':
                print(("(l,m) = (%d,%d)  om = %f" %(l, m, sig_test[idx]*2)))
            elif info == 'all':
                print(("m = %d, l = %d, N = %d, n = %d, om = %f" %(m, l, N, idx+1, sig_test[idx]*2)))
    elif (symm=='ea' or symm=='EA'):
        for N in range(Nmax+1):
            l = 2*N + m + 1
            sig_test = sigma(m = m, N = N, symm=symm)
            idx = np.argmin(abs(sig - sig_test))
            if info == 'lm':
                print(("(l,m) = (%d,%d)  om = %f" %(l, m, sig_test[idx]*2)))
            elif info == 'all':
                print(("m = %d, l = %d, N = %d, n = %d, om = %f" %(m, l, N, idx+1, sig_test[idx]*2)))
