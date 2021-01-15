#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import numpy as np
import matplotlib.pyplot as plt
from .velocity import *
from .sigma import *
from .grid import *
from .libzhang import _find_rad,_find_phi
from .plotlib import *

class inerMod:

    def __init__(self,nr=33,nphi=256,ntheta=128,m=0,l=None,N=0,n=1,symm='es',norm=False):

        self.sig_arr, self.N = sigma(m=m,l=l,N=N,symm=symm)
        self.U = vel(m=m,l=l,N=N,n=n,nr=nr,nphi=nphi,ntheta=ntheta,symm=symm,norm=norm)
        self.grid = grid(nr=nr,nphi=nphi,ntheta=ntheta)
        self.l = l
        self.m = m
        self.n = n
        self.omega = self.sig_arr[n-1]*2


    def surf(self,field='us',r=0.5,cm='RdBu_r',levels=60,grid=False,proj="ortho"):

        idxPlot = _find_rad(self.grid.r,r)

        field = field.lower()

        if field == 'us':
            data = self.U.Us[:,:,idxPlot]

        if field == 'up':
            data = self.U.Up[:,:,idxPlot]

        if field == 'uz':
            data = self.U.Uz[:,:,idxPlot]

        radContour(self.grid.theta,self.grid.phi,data,grid,levels,cm,proj)

        plt.show()

    def slice(self, field='us',phi=0,cm='RdBu_r',levels=100):

        idxPlot = _find_phi(self.grid.phi,phi)

        field = field.lower()

        if field == 'us':
            data = self.U.Us[idxPlot,:,:]

        if field == 'up':
            data = self.U.Up[idxPlot,:,:]

        if field == 'uz':
            data = self.U.Uz[idxPlot,:,:]

        merContour(self.grid.r,self.grid.theta,data,levels,cm)
        plt.show()
