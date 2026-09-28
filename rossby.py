#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import shtns
import sys
import pyvista as pv

def get_grid(theta, phi):
   
    th2D, p2D = np.meshgrid(theta, phi, indexing='ij')

    x = np.sin(th2D) * np.cos(p2D)
    y = np.sin(th2D) * np.sin(p2D)
    z = np.cos(th2D)

    return x, y, z, th2D, p2D

def get_cart(vt, vp, th2D, p2D):

    vs =   vt * np.cos(th2D)
    vz = - vt * np.sin(th2D)

    vx = vs * np.cos(p2D) - vp * np.sin(p2D)
    vy = vs * np.sin(p2D) + vp * np.cos(p2D)

    return vx, vy, vz

m = 20
lmax = 20

lUsr = int(sys.argv[1])
mUsr = int(sys.argv[2])

ntheta, nphi = [128, 256]

polar_opt = 1e-10

norm = shtns.sht_orthonormal | shtns.SHT_NO_CS_PHASE

sh = shtns.sht(lmax, mmax=m, norm=norm, nthreads=1)

ntheta, nphi = sh.set_grid(ntheta, nphi, polar_opt=polar_opt)

S = sh.spec_array()
T = sh.spec_array()

T[sh.idx(lUsr, mUsr)] = 1.

utheta, uphi = sh.synth(S, T)
psi = sh.synth(T)

x, y, z, th2D, p2D = get_grid(np.arccos(sh.cos_theta), np.linspace(0., 2*np.pi, nphi))

ux, uy, uz = get_cart(utheta, uphi, th2D, p2D)

col = (0.43, 0.43, 0.43)

surf = pv.StructuredGrid(x, y, z)
surf.point_data['psi'] = psi.ravel(order='F')

stride = 4
pts = np.column_stack([x[::stride, ::stride].ravel(), y[::stride, ::stride].ravel(),
                       z[::stride, ::stride].ravel()])
vec = np.column_stack([ux[::stride, ::stride].ravel(), uy[::stride, ::stride].ravel(),
                       uz[::stride, ::stride].ravel()])
cloud = pv.PolyData(pts)
cloud.point_data['vec'] = vec / np.linalg.norm(vec, axis=1).max()

psiMax = np.abs(psi).max()

pl = pv.Plotter(window_size=(800, 800))
pl.add_mesh(surf, scalars='psi', cmap='RdBu_r', clim=[-psiMax, psiMax],
            smooth_shading=True)
pl.add_mesh(cloud.glyph(orient='vec', scale='vec', factor=0.1), color=col)
pl.show()
