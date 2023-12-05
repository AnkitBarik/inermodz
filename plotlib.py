#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.colors as colors

def get_grid2D(theta, phi):

    nphi  = len(phi)
    ntheta = len(theta)
    p2D  = np.zeros([nphi, ntheta])
    th2D = np.zeros([nphi, ntheta])

    for i in range(nphi):
        p2D[i,:] = phi[i]

    for j in range(ntheta):
        th2D[:, j] = theta[j]

    return p2D, th2D


def radContour(theta, phi, data, grid, levels, cm, proj, plotbg, titl=None):
    if plotbg == 'dark':
        plt.style.use("dark_background")
        plt.rcParams.update({
            "axes.facecolor"   : "#1b1b1b",
            "figure.facecolor" : "#1b1b1b",
            "figure.edgecolor" : "#1b1b1b",
            "savefig.facecolor": "#1b1b1b",
            "savefig.edgecolor": "#1b1b1b"})
        lc = 'w'
    elif plotbg == 'light':
        lc = 'k'

    p2D, th2D = get_grid2D(theta, phi)

    p2D = p2D - np.pi
    th2D= np.pi/2 - th2D

    lon = p2D * 180./np.pi
    lat = th2D * 180./np.pi

    fig = plt.figure(figsize=(12,6.75))

    if proj == 'Orthographic':
        fig = plt.figure(figsize=(10, 10))
        plotcrs = ccrs.Orthographic(0, 40)
    else:
        plotcrs = eval('ccrs.'+proj+'()')

    ax = fig.add_subplot(1, 1, 1, projection=plotcrs)

    datMax = (np.abs(data)).max()
    divnorm = colors.TwoSlopeNorm(vmin=-datMax, vcenter=0, vmax=datMax)

    if grid:
        ax.gridlines(linewidth=1, color='gray', alpha=0.5, linestyle=':')

    if proj == "Orthographic":
        cont = ax.pcolormesh(lon, lat, data, \
                           transform=ccrs.PlateCarree(), cmap=cm, \
                           norm=divnorm)
    else:
        cont = ax.contourf(lon, lat, data, levels, \
                           transform=ccrs.PlateCarree(), cmap=cm, \
                           norm=divnorm)


        for c in cont.collections:
            c.set_edgecolor("face")

    if titl is not None:
        ax.set_title(titl,fontsize=30)
#        if vec:
#            ut = self.U.Us*cos(self.grid.th3D) - self.U.Uz*sin(self.grid.th3D)
#            ut = ut[::vecStride,::vecStride,idxPlot]
#            up = self.U.Up[::vecStride,::vecStride,idxPlot]
#            lon = lon[::vecStride,::vecStride]
#            lat = lat[::vecStride,::vecStride]
#            #ax.quiver(lon,lat,up,ut,transform=plotcrs,width=vecWidth,scale=vecScale,regrid_shape=20)
#            ax.quiver(lon,lat,up,ut,transform=plotcrs)#,regrid_shape=regrid_shape)

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

def merContour(r, theta, data, levels, cm, plotbg, titl=None):
    if plotbg == 'dark':
        plt.style.use("dark_background")
        plt.rcParams.update({
            "axes.facecolor"   : "#1b1b1b",
            "figure.facecolor" : "#1b1b1b",
            "figure.edgecolor" : "#1b1b1b",
            "savefig.facecolor": "#1b1b1b",
            "savefig.edgecolor": "#1b1b1b"})
        lc = 'w'
    elif plotbg == 'light':
        lc = 'k'
    rr, tth = np.meshgrid(r, theta)

    xx = rr*np.sin(tth)
    yy = rr*np.cos(tth)

    plt.figure(figsize=(5, 10))

    datMax = (np.abs(data)).max()
    divnorm = colors.TwoSlopeNorm(vmin=-datMax, vcenter=0, vmax=datMax)

    cont = plt.contourf(xx, yy, data, levels, cmap=cm, norm=divnorm)

    plt.plot(r[0]*np.sin(theta), r[0]*np.cos(theta), lc, lw=1)
    plt.plot(r[-1]*np.sin(theta), r[-1]*np.cos(theta), lc, lw=1)
    plt.plot([0, 0], [ r.min(), r.max() ], lc, lw=1)
    plt.plot([0, 0], [ -r.max(), -r.min() ], lc, lw=1)

    for c in cont.collections:
        c.set_edgecolor("face")

    if titl is not None:
        plt.title(titl,fontsize=20)

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

def eqContour(r, phi, data, levels, cm, plotbg, titl=None):
    if plotbg == 'dark':
        plt.style.use("dark_background")
        plt.rcParams.update({
            "axes.facecolor"   : "#1b1b1b",
            "figure.facecolor" : "#1b1b1b",
            "figure.edgecolor" : "#1b1b1b",
            "savefig.facecolor": "#1b1b1b",
            "savefig.edgecolor": "#1b1b1b"})
        lc = 'w'
    elif plotbg == 'light':
        lc = 'k'
    phi2D, r2D = np.meshgrid(phi, r, indexing='ij')
    xx = r2D * np.cos(phi2D)
    yy = r2D * np.sin(phi2D)

    plt.figure(figsize=(10, 10))

    datMax = (np.abs(data)).max()
    divnorm = colors.TwoSlopeNorm(vmin=-datMax, vcenter=0, vmax=datMax)
    cont = plt.contourf(xx, yy, data, levels, cmap=cm, norm=divnorm)

    plt.plot(r[0]*np.cos(phi), r[0]*np.sin(phi), lc, lw=1)
    plt.plot(r[-1]*np.cos(phi), r[-1]*np.sin(phi), lc, lw=1)

    for c in cont.collections:
        c.set_edgecolor("face")

    if titl is not None:
        plt.title(titl,fontsize=20)

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

def surface3D(x,y,z,idx,ux,uy,uz,dat,cm='seismic',quiv=True,fac=0.01,col=True):

    from mayavi import mlab

    lut=eval('plt.cm.'+cm+'(np.linspace(0,1,255))*255')

    if col:
        col = (0.43, 0.43, 0.43)
    else:
        col = None
    mlab.figure(size=(800, 800))
    mesh_handle = mlab.mesh(x[..., idx], y[..., idx], z[..., idx], scalars=dat)
    mesh_handle.module_manager.scalar_lut_manager.lut.table = lut
#    mesh_handle.module_manager.scalar_lut_manager.reverse_lut = True
    if quiv:
        mlab.quiver3d(x, y, z, ux, uy, uz, color=col, scale_mode='vector',
                      mode='arrow', mask_points=4, scale_factor=fac)
    #mlab.show()
    mlab.draw()
