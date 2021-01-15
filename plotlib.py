#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.colors as colors

def radContour(theta,phi,data,grid,levels,cm):

        th  = np.pi/2 - theta
        phi = phi - np.pi

        pphi, ttheta = np.meshgrid(phi, th, indexing='ij')


        lon = pphi * 180./np.pi
        lat = ttheta * 180./np.pi

        fig = plt.figure(figsize=(10,10))

        plotcrs = ccrs.Orthographic(0, 30)
        ax = fig.add_subplot(1, 1, 1, projection=plotcrs)

        datMax = (np.abs(data)).max()
        divnorm = colors.TwoSlopeNorm(vmin=-datMax, vcenter=0, vmax=datMax)

        if grid:
            ax.gridlines(ls=':',color='k')

        cont = ax.contourf(lon.transpose(),lat.transpose(),data,levels,\
                           transform=ccrs.PlateCarree(),cmap='RdBu_r', \
                           norm=divnorm)
        
        for c in cont.collections:
            c.set_edgecolor("face")

#        if vec:
#            ut = self.U.Us*cos(self.grid.th3D) - self.U.Uz*sin(self.grid.th3D)
#            ut = ut[::vecStride,::vecStride,idxPlot]
#            up = self.U.Up[::vecStride,::vecStride,idxPlot]
#            lon = lon[::vecStride,::vecStride]
#            lat = lat[::vecStride,::vecStride]
#            #ax.quiver(lon,lat,up,ut,transform=plotcrs,width=vecWidth,scale=vecScale,regrid_shape=20)
#            ax.quiver(lon,lat,up,ut,transform=plotcrs)#,regrid_shape=regrid_shape)

        plt.axis('off')

def merContour(r,theta,data,levels,cm):
    
        rr,tth = np.meshgrid(r,theta)

        xx = rr*np.sin(tth)
        yy = rr*np.cos(tth)

        plt.figure(figsize=(5,10))

        datMax = (np.abs(data)).max()
        divnorm = colors.TwoSlopeNorm(vmin=-datMax, vcenter=0, vmax=datMax)
        
        cont = plt.contourf(xx,yy,data,levels,cmap=cm,norm=divnorm)
        
        for c in cont.collections:
            c.set_edgecolor("face")

        plt.axis('off')
