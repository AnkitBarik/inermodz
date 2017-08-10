#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pylab import *

class grid:
    
    def __init__(self,nr = 65, np = 512, nt = 256):
        
        ri = 0.; ro = 1;

        dt = pi/nt

        self.r = linspace(ri,ro,nr)
        self.phi = linspace(0.,2*pi,np)
        self.theta = linspace(dt,pi-dt,nt)
        
        self.r3D = zeros([np,nt,nr])
        self.th3D = zeros([np,nt,nr])
        self.phi3D = zeros([np,nt,nr])

        for i in range(nr):
            self.r3D[:,:,i] = self.r[i]
                  
        for j in range(nr):
            self.th3D[:,j,:] = self.theta[j]

        for k in range(nr):
            self.phi3D[k,:,:] = self.phi[k]

        self.s3D = self.r3D*sin(self.th3D) 
        self.z3D = self.r3D*cos(self.th3D)
