#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pylab import *
from mpl_toolkits.mplot3d import axes3d

k = 10.*array([1., 1., 1.])
v = 10.*array([1, -0.5, -0.5])

nx = 10
ny = 10
nz = 5
nt = 500

x = linspace(0., 2., nx)
y = linspace(0., 1., ny)
z = linspace(0., 0.5, nz)
t = linspace(0., 10., nt)

zhat = array([0., 0., 1.])
khat = k/linalg.norm(k)

khatxv = cross(khat, v)
omega = 2. * dot(zhat, khat) 

x3D = zeros([nx, ny, nz])
y3D = zeros([nx, ny, nz])
z3D = zeros([nx, ny, nz])

kx3D = ones([nx*ny*nz])*k[0]
ky3D = ones([nx*ny*nz])*k[1]
kz3D = ones([nx*ny*nz])*k[2]

kx3D = reshape(kx3D, [nx, ny, nz])
ky3D = reshape(ky3D, [nx, ny, nz])
kz3D = reshape(kz3D, [nx, ny, nz])


for xi in range(nx):
    x3D[xi, ...] = x[xi]

for yi in range(ny):
    y3D[:, yi,:] = y[yi]

for zi in range(nz):
    z3D[..., zi] = z[zi]

del xi, yi, zi

kr = kx3D * x3D + ky3D * y3D + kz3D * z3D

def get_q(nt, nx, ny, nz, t, x3D, y3D, z3D, k, v):
    
    qx = zeros([nx, ny, nz])
    qy = zeros([nx, ny, nz])
    qz = zeros([nx, ny, nz])

    for ti in range(nt):
        print(ti)
        
        phase = kr - omega * t[ti]
                
        qx = khatxv[0] * cos(phase) - v[0] * sin(phase)
        qy = khatxv[1] * cos(phase) - v[1] * sin(phase)
        qz = khatxv[2] * cos(phase) - v[2] * sin(phase)

        fig = figure(figsize=(16, 9))
        ax = fig.gca(projection='3d')

        ax.quiver(x3D, y3D, z3D, qx, qy, qz, length=0.1, normalize=True)
        
#        show()
        savefig("inerWav/img%03d.png" %ti)

        close()

get_q(nt, nx, ny, nz, t, x3D, y3D, z3D, k, v)

