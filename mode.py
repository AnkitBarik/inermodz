#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import numpy as np
import matplotlib.pyplot as plt
from .velocity import *
from .sigma import *
from .grid import *
from .libzhang import _find_rad, _find_phi
from .plotlib import *

class inerMod:

    def __init__(self,nr=33,nphi=256,ntheta=128,m=0,l=None,N=0,n=1,symm='es',norm=False):

        symm = symm.lower()

        if l is not None:
            N = int(0.5 * (l - m - (l-m)%2))

            if (l-m)%2 == 0:
                symm = 'es'
            else:
                symm = 'ea'
        else:
            if symm == 'es':
                l = 2*N + m
            elif symm == 'ea':
                l = 2*N + m - 1

        self.sig_arr = sigma(m=m, l=l, N=N, symm=symm)
        self.grid    = grid(nr=nr, nphi=nphi, ntheta=ntheta)
        self.U       = vel(m=m, l=l, N=N, n=n, nr=nr, nphi=nphi,
                           ntheta=ntheta, symm=symm, sigma = self.sig_arr[n-1],
                           grid=self.grid,norm=norm)
        self.l     = l
        self.m     = m
        self.n     = n
        self.N     = N
        self.omega = self.sig_arr[n-1]*2
        self.symm  = symm

        print('omega =', 2*self.sig_arr)
        print('omega(%d,%d,%d) = %.5f' %(l, m, n, self.omega))


    def get_data(self,field):

        field = field.lower()

        if field in ['us','vs']:
            data = self.U.Us
            titl = r'$u_s$'
        elif field in ['up','uphi','vp','vphi']:
            data = self.U.Up
            titl = r'$u_\phi$'
        elif field == ['uz','vz']:
            data = self.U.Uz
            titl = r'$u_z$'
        elif field == ['ur','vr']:
            data = self.U.Ur
            titl = r'$u_r$'
        elif field in ['ut','utheta','vt','vtheta']:
            data = self.U.Utheta
            titl = r'$u_\theta$'
        elif field in ['ke','energy']:
            data = 0.5 * (self.U.Us**2 + self.U.Up**2 + self.U.Uz**2)
            titl = r'$E_{kin}$'

        return data, titl


    def surf(self,field='us',r=1,cm='RdBu_r',levels=60,grid=False,
             mode="2D",proj="Mollweide",quivfac=0.01,col=True,l_titl=True):

        idxPlot = _find_rad(self.grid.r, r)

        data, titl = self.get_data(field)
        data = data[...,idxPlot]

        if mode == "2D":
            if l_titl:
                titl = titl + r' at $r/r_o = %.2f$' %(self.grid.r[idxPlot]/self.grid.r[-1])
            else:
                titl = None

            radContour(self.grid.theta, self.grid.phi, data, grid, levels, cm, proj, titl)

        elif mode == "3D":
            surface3D(self.grid.x3D, self.grid.y3D, self.grid.z3D, idxPlot,
                      self.U.Ux, self.U.Uy, self.U.Uz, data, cm=cm, quiv=True, fac=quivfac, col=col)
        else:
            print("mode must be 2D or 3D")

        plt.show()

    def slice(self, field='us',phi=0,cm='RdBu_r',levels=100,l_titl=True):

        idxPlot = _find_phi(self.grid.phi, phi)

        field = field.lower()

        data, titl = self.get_data(field)
        data = data[idxPlot,...]

        if l_titl:
            titl = titl + r' at $\phi=%.1f^\circ$' %(self.grid.phi[idxPlot] * 180/np.pi)
        else:
            titl = None

        merContour(self.grid.r, self.grid.theta, data, levels, cm, titl)
        plt.show()

    def equat(self, field='us',cm='RdBu_r',levels=60,l_title=True):

        field = field.lower()

        half = int(self.grid.ntheta/2)
        data, titl = self.get_data(field)
        data = data[:,half,:]

        if l_title:
            titl = titl + ' at equator'
        else:
            titl = None

        eqContour(self.grid.r, self.grid.phi, data, levels, cm, titl)
        plt.show()
