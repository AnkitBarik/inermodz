#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pylab import *

def factorial(n):
    
    if (n==0) or (n==1):
        fac = 1
    else:
        fac = n
        for i in range(1,n):
            fac = fac*i
    return fac

