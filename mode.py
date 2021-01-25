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


    def surf(self,field='us',r=0.5,cm='RdBu_r',levels=60,grid=False,mode="2D",proj="ortho",quivfac=0.01,col=True):

        idxPlot = _find_rad(self.grid.r,r)

        field = field.lower()

        if field == 'us':
            data = self.U.Us

        if field == 'up':
            data = self.U.Up

        if field == 'uz':
            data = self.U.Uz

        if mode == "2D":
            radContour(self.grid.theta,self.grid.phi,data,idxPlot,grid,levels,cm,proj)
        elif mode == "3D":
            surface3D(self.grid.x3D,self.grid.y3D,self.grid.z3D,idxPlot,
                      self.U.Ux,self.U.Uy,self.U.Uz,data,cm=cm,quiv=True,fac=quivfac,col=col)
        else:
            print("mode must be 2D or 3D")

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

    def equat(self, field='us',cm='seismic',levels=60):

        field = field.lower()

        half = int(self.grid.ntheta/2)

        if field == 'us':
            data = self.U.Us[:,half,:]

        if field == 'up':
            data = self.U.Up[:,half,:]

        if field == 'uz':
            data = self.U.Uz[:,half,:]

        eqContour(self.grid.r,self.grid.phi,data,levels,cm)
        plt.show()
