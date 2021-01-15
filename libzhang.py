#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import numpy as np

def factorial(n):

    if (n==0) or (n==1):
        fac = 1.
    else:
        fac = np.float32(np.product(list(range(1,n+1))))

    return fac

def dfactorial(n):

    if (n==0) or (n==1):
        fac = 1.
    else:
        fac = np.float32(np.product(list(range(2 - n%2,n+1,2))))

    return fac

def _find_rad(r,rPlot):
#                rPlot /= (1-self.radratio)
    Idx = np.argmin(np.abs(r - rPlot))
    return Idx

def _find_phi(phi,phiPlot):

    phiPlot = np.deg2rad(phiPlot)
    Idx = np.argmin(np.abs(phi - phiPlot))
    return Idx
