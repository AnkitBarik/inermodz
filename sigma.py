#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pylab import *
from libzhang import factorial

def sigma(m=0,N=0,symm='es'):

    if symm == 'es' or symm == 'ES':
        
        p = zeros(2*N+1)

        fac = factorial(2*(2*N+m))/( factorial(2*N+m) * factorial(2*N) )
        
        p[0] = fac * (m+2*N)
        p[1] = -fac * 2*N

        for j in range(1,N+1): 
            
            print p
            
            fac = -fac * ( (N-j+1.) * (2.* (N-j)+1.) / ( j*(2*(2.*N+m-j)+1.) ) )
           
            print fac
            
            if (j == N):
                p[2*j] = fac * (m + 2*N - 2*j)
            else: 
                p[2*j] = fac * (m + 2*N - 2*j)
                p[2*j + 1] = -fac * 2 * (N-j)
            
        print p
        sig = roots(p)

    if symm == 'ea' or symm == 'EA':

        p = zeros(2*N+2)

        fac = factorial(2*(2*N+m+1))/( factorial(2*N+m+1) * factorial(2*N+1 ) )

        p[0] = fac * (m+2*N+1)
        p[1] = -fac * (2*N+1)

        for j in range(1,N+1):
            
            j1 = j-1
            fac = -fac * ( (N-j+1.) * (2.* (N-j)+3.) / ( j*(2*(2.*N+m-j1)+1.) ) )
            
            p[2*j] = fac * (m + 2*N - 2*j + 1)
            p[2*j+1] = -fac * (2*N - 2*j + 1)
        
        sig = roots(p)

    return sig
