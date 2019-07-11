#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pylab import *
from velocity import *
from sigma import *
from grid import *
from libzhang import _find_rad,_find_phi
from mpl_toolkits.basemap import Basemap

class inerMod:

    def __init__(self,nr=33,np=256,nt=128,m=0,l=None,N=0,n=1,symm='es',norm=False):

        self.sig_arr, self.N = sigma(m=m,l=l,N=N,symm=symm)
        self.U = vel(m=m,l=l,N=N,n=n,nr=nr,np=np,nt=nt,symm=symm,norm=norm)
        self.grid = grid(nr=nr,np=np,nt=nt)
        self.l = l
        self.m = m
        self.n = n
        self.omega = self.sig_arr[n-1]*2


    def surf(self,field='us',r=0.5,cm='seismic',levels=100,vec=False,vecStride=5,vecWidth=2e-3,vecScale=1e2,proj='hammer'):
         
        th = pi/2 - self.grid.theta
        phi = pi - self.grid.phi

        m = Basemap(projection = proj, lon_0=0, lat_0=0,resolution='c')
        pphi, ttheta = meshgrid(phi, th, indexing='ij')


        lon = pphi * 180./pi
        lat = ttheta * 180./pi

        x,y = m(lon,lat)


        rPlot = 1.

        idxPlot = _find_rad(self.grid.r,r)

        figure(figsize=(12,6))

        m.drawmeridians([180],linewidth=0.5)

        if field in ['us','US','uS','Us']:
            data = self.U.Us[:,:,idxPlot]

        if field in ['up','UP','uP','Up']:
            data = self.U.Up[:,:,idxPlot]

        if field in ['uz','UZ','uZ','Uz']:
            data = self.U.Uz[:,:,idxPlot]

        contourf(x,y,data,levels,cmap=cm)

        if vec:
            ut = self.U.Us*cos(self.grid.th3D) - self.U.Uz*sin(self.grid.th3D)
            ut = ut[::vecStride,::vecStride,idxPlot]
            up = self.U.Up[::vecStride,::vecStride,idxPlot]
            lon = lon[::vecStride,::vecStride]
            lat = lat[::vecStride,::vecStride]
            uprot,utrot,x,y = m.rotate_vector(up,ut,lon,lat,returnxy=True)
            quiver(x,y,up,ut,width=vecWidth,scale=vecScale)

        axis('off')

        show()

    def slice(self, field='us',phi=0,cm='seismic',levels=100):

        rr,tth = meshgrid(self.grid.r,self.grid.theta)

        xx = rr*sin(tth)
        yy = rr*cos(tth)

        idxPlot = _find_phi(self.grid.phi,phi)

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
