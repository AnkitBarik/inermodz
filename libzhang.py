#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pylab import *

def factorial(n):
    
    if (n==0) or (n==1):
        fac = 1.
    else:
        fac = float32(product(range(1,n+1)))

    return fac

def dfactorial(n):

    if (n==0) or (n==1):
        fac = 1.
    else:
        fac = float32(product(range(2 - n%2,n+1,2)))

    return fac

def find_rad(r,rPlot):
#                rPlot /= (1-self.radratio)
    Idx = where(abs(r - rPlot) == min(abs(r - rPlot)))[0][0]
    return Idx

def find_phi(phi,phiPlot):
   
    phiPlot = deg2rad(phiPlot) 
    Idx = where(abs(phi - phiPlot) == min(abs(phi - phiPlot)))[0][0]
    return Idx


