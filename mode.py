#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pylab import *
from velocity import *
from sigma import *
from grid import *
from libzhang import find_rad
from mpl_toolkits.basemap import Basemap

class inerMod:

    def __init__(self,nr=33,np=256,nt=128,m=0,l=None,N=0,n=0,symm='es'):

        self.sig_arr = sigma(m=m,l=l,N=N,symm=symm)
        self.U = vel(m=m,l=l,N=N,n=n,nr=nr,np=np,nt=nt,symm=symm)
        self.grid = grid(nr=nr,np=np,nt=nt)


    def surf(self,field='us',r=0.5,cm='seismic',levels=100,proj='hammer'):
         
        th = pi/2 - self.grid.theta
        phi = pi - self.grid.phi

        m = Basemap(projection = proj, lon_0=0, lat_0=0,resolution='c')
        pphi, ttheta = meshgrid(phi, th, indexing='ij')


        lon = pphi * 180./pi
        lat = ttheta * 180./pi

        x,y = m(lon,lat)


        rPlot = 1.

        idxPlot = find_rad(self.grid.r,r)

        figure(figsize=(12,6))

        m.drawmeridians([180],linewidth=0.5)

        if field in ['us','US','uS','Us']:
            data = self.U.Us[:,:,idxPlot]

        if field in ['up','UP','uP','Up']:
            data = self.U.Up[:,:,idxPlot]

        if field in ['uz','UZ','uZ','Uz']:
            data = self.U.Uz[:,:,idxPlot]

        contourf(x,y,data,levels,cmap=cm)
        axis('off')

        show()

    def slice(self, field='us',phi=0,cm='seismic',levels=100):

        rr,tth = meshgrid(self.grid.r,self.grid.theta)

        xx = rr*sin(tth)
        yy = rr*cos(tth)

        idxPlot = find_phi(self.grid.phi,phi)

        figure(figsize=(5,10))

        if field in ['us','US','uS','Us']:
            data = self.U.Us[idxPlot,:,:]

        if field in ['up','UP','uP','Up']:
            data = self.U.Up[idxPlot,:,:]

        if field in ['uz','UZ','uZ','Uz']:
            data = self.U.Uz[idxPlot,:,:]

        contourf(xx,yy,data,levels,cmap=cm)
        axis('off')

        show()
