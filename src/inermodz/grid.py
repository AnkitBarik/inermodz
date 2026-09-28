#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import numpy as np

class grid:

    def __init__(self,nr = 65, nphi = 512, ntheta = 256):

        ri = 0.; ro = 1;

        self.nr    = nr
        self.ntheta= ntheta
        self.nphi  = nphi

        self.r     = np.linspace(ri, ro, nr)
        self.phi   = np.linspace(0., 2*np.pi, nphi)
        self.theta = np.linspace(0., np.pi, ntheta)

        self.r3D   = np.zeros([nphi, ntheta, nr])
        self.th3D  = np.zeros([nphi, ntheta, nr])
        self.phi3D = np.zeros([nphi, ntheta, nr])

        self.th2D  = np.zeros([ntheta,nr]) # For integration

        for i in range(nr):
            self.r3D[:,:, i] = self.r[i]

        for j in range(ntheta):
            self.th3D[:, j,:] = self.theta[j]
            self.th2D[j,:]    = self.theta[j]

        for k in range(nphi):
            self.phi3D[k,:,:] = self.phi[k]

        self.s3D = self.r3D*np.sin(self.th3D)
        self.z3D = self.r3D*np.cos(self.th3D)
        self.x3D = self.s3D*np.cos(self.phi3D)
        self.y3D = self.s3D*np.sin(self.phi3D)