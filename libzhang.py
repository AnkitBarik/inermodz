#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import math
import numpy as np

# Exact integer arithmetic: float32/int64 overflow for moderately large m, N

def factorial(n):

    return math.factorial(n)

def dfactorial(n):

    if n <= 0:
        return 1   # includes (-1)!! = 1

    return math.prod(range(n, 0, -2))

def _find_rad(r, rPlot):
#                rPlot /= (1-self.radratio)
    Idx = np.argmin(np.abs(r - rPlot))
    return Idx

def _find_phi(phi, phiPlot):

    phiPlot = np.deg2rad(phiPlot)
    Idx = np.argmin(np.abs(phi - phiPlot))
    return Idx
