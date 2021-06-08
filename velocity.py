#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import numpy as np
from .sigma import sigma
from .libzhang import *
from .grid import grid

class vel:

    def __init__(self,m=0,N=0,n=1,l=None,nr=33,nphi=256,ntheta=128,symm='es',norm=False):

        n = n-1   # The definition of n starts from 1 :(
#        N = (l - m - ((l-m)%2))/2

        self.grid = grid(nr=nr, nphi=nphi, ntheta=ntheta)
        self.Us = np.zeros([nphi, ntheta, nr])
        self.Up = np.zeros([nphi, ntheta, nr])
        self.Uz = np.zeros([nphi, ntheta, nr])

        sig_arr, N = sigma(m=m, N=N, l=l, symm=symm)
        print(('omega =', sig_arr*2))
        sig = sig_arr[n]

        print(('omega(%d,%d,%d) = %.4f' %(l, m, n+1, sig*2)))


        if l is not None:
            if (l-m)%2 == 0:
                symm = 'es'
            else:
                symm = 'ea'

        if (symm == 'es') or (symm == 'ES'):

            for i in range(N+1):
                for j in range(N-i+1):
                    C = (-1)**(i+j) * dfactorial(2*(m+N+i+j)-1)/  \
                        ( 2**(j+1) * dfactorial(2*i-1) * factorial(N-i-j)  \
                        * factorial(i) * factorial(j) * factorial(m+j) )

                    if i > 0:

                        UTemp = C * sig**(2*i-1) * ( 1 - sig**2)**j * 2*i * \
                                self.grid.s3D**(m+2*j) * self.grid.z3D**(2*i-1)

                        self.Uz = self.Uz + UTemp


                    UTemp = C * sig**(2*i) * (1-sig**2)**(j-1) * (m + m*sig + 2*j*sig)\
                            * self.grid.s3D**(m+2*j-1) * self.grid.z3D**(2*i)

                    self.Us = self.Us + UTemp

                    UTemp = C * sig**(2*i) * (1-sig**2)**(j-1) * (m + m*sig + 2*j)\
                            * self.grid.s3D**(m+2*j-1) * self.grid.z3D**(2*i)

                    self.Up = self.Up + UTemp


            self.Us = self.Us  * np.sin(m*self.grid.phi3D)
            self.Uz = -self.Uz * np.sin(m*self.grid.phi3D)
            self.Up = self.Up  * np.cos(m*self.grid.phi3D)
            self.Ux = self.Us * np.cos(self.grid.phi3D) - self.Up * np.sin(self.grid.phi3D)
            self.Uy = self.Us * np.sin(self.grid.phi3D) + self.Up * np.cos(self.grid.phi3D)


        if (symm == 'ea') or (symm == 'EA'):


            for i in range(N+1):
                for j in range(N-i+1):


                    C = (-1)**(i+j) * dfactorial(2*(m+N+i+j)+1)/  \
                        ( 2**(j+1) * dfactorial(2*i+1) * factorial(N-i-j)  \
                        * factorial(i) * factorial(j) * factorial(m+j) )

                    UTemp = C * sig**(2*i-1) * ( 1 - sig**2)**j * (2*i+1) * \
                            self.grid.s3D**(m+2*j) * self.grid.z3D**(2*j)

                    self.Uz = self.Uz + UTemp


                    UTemp = C * sig**(2*i) * (1-sig**2)**(j-1) * (m + m*sig + 2*j*sig)\
                            * self.grid.s3D**(m+2*j-1) * self.grid.z3D**(2*i+1)

                    self.Us = self.Us + UTemp


                    UTemp = C * sig**(2*i) * (1-sig**2)**(j-1) * (m + m*sig + 2*j)\
                            * self.grid.s3D**(m+2*j-1) * self.grid.z3D**(2*i+1)


                    self.Up = self.Up + UTemp


            self.Us = self.Us  * np.sin(m*self.grid.phi3D)
            self.Uz = -self.Uz * np.sin(m*self.grid.phi3D)
            self.Up = self.Up  * np.cos(m*self.grid.phi3D)
            self.Ux = self.Us * np.cos(self.grid.phi3D) - self.Up * np.sin(self.grid.phi3D)
            self.Uy = self.Us * np.sin(self.grid.phi3D) + self.Up * np.cos(self.grid.phi3D)

            del UTemp


        if norm:
            U2 = self.Us**2 + self.Up**2 + self.Uz**2
            U2p = np.trapz(U2, x=self.grid.phi, axis=0)
            U2t = np.trapz(U2p, self.grid.theta, axis=0)
            U2r = np.trapz(U2t, self.grid.r, axis=0)
            Vol = 4./3. * np.pi * (self.grid.r.max()**3 - self.grid.r.min()**3)
            U2r /= Vol

            self.Us /= np.sqrt(U2r)
            self.Up /= np.sqrt(U2r)
            self.Uz /= np.sqrt(U2r)
