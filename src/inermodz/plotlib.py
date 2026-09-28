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

def _clim(data):
    # Colour range: symmetric about 0 for signed fields, [0, max] for
    # non-negative ones such as the kinetic energy
    if data.min() >= 0:
        return 0., data.max()
    datMax = np.abs(data).max()
    return -datMax, datMax

def _mplnorm(data):
    vmin, vmax = _clim(data)
    if vmin == 0:
        return colors.Normalize(vmin=vmin, vmax=vmax)
    return colors.TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)


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

    divnorm = _mplnorm(data)

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


        cont.set_edgecolor("face")

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

    divnorm = _mplnorm(data)

    cont = plt.contourf(xx, yy, data, levels, cmap=cm, norm=divnorm)

    plt.plot(r[0]*np.sin(theta), r[0]*np.cos(theta), lc, lw=1)
    plt.plot(r[-1]*np.sin(theta), r[-1]*np.cos(theta), lc, lw=1)
    plt.plot([0, 0], [ r.min(), r.max() ], lc, lw=1)
    plt.plot([0, 0], [ -r.max(), -r.min() ], lc, lw=1)

    cont.set_edgecolor("face")

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

    divnorm = _mplnorm(data)
    cont = plt.contourf(xx, yy, data, levels, cmap=cm, norm=divnorm)

    plt.plot(r[0]*np.cos(phi), r[0]*np.sin(phi), lc, lw=1)
    plt.plot(r[-1]*np.cos(phi), r[-1]*np.sin(phi), lc, lw=1)

    cont.set_edgecolor("face")

    if titl is not None:
        plt.title(titl,fontsize=20)

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

def _pv_title(titl):
    # VTK text does not render mathtext, so strip it: r'$u_\phi$' -> 'u_phi'
    if titl is None:
        return None
    return titl.replace('$', '').replace('\\', '')

def _pv_plotter(plotbg, screenshot):
    import pyvista as pv

    pl = pv.Plotter(off_screen=screenshot is not None, window_size=(800, 800))
    if plotbg == 'dark':
        pl.set_background('#1b1b1b')
        fg = 'w'
    else:
        pl.set_background('white')
        fg = 'k'

    return pl, fg

def _pv_sbar(fg):
    return {'title': '', 'color': fg, 'fmt': '%.3g', 'vertical': True,
            'position_x': 0.85, 'position_y': 0.2, 'height': 0.6}

def _pv_finish(pl, titl, fg, screenshot):
    if titl is not None:
        pl.add_text(titl, font_size=14, color=fg)
    pl.view_vector((1., 1., 0.4), viewup=(0., 0., 1.))
    if screenshot is not None:
        pl.screenshot(screenshot)
        pl.close()
    else:
        pl.show()

def _pv_structured(x, y, z, dat):
    import pyvista as pv

    grid = pv.StructuredGrid(x, y, z)
    grid.point_data['data'] = dat.ravel(order='F')

    return grid

def surface3D(x,y,z,idx,ux,uy,uz,dat,cm='seismic',quiv=True,fac=0.1,col=True,
              plotbg='light',titl=None,stride=4,screenshot=None):
    """
    Plot a field on the spherical surface r = r[idx] using pyvista, with
    optional velocity arrows on the same surface. The longest arrow has
    length fac (in units of the outer radius).
    """

    import pyvista as pv

    sl = np.s_[..., idx:idx+1]
    surf = _pv_structured(x[sl], y[sl], z[sl], dat[..., np.newaxis])

    pl, fg = _pv_plotter(plotbg, screenshot)

    pl.add_mesh(surf, scalars='data', cmap=cm, clim=_clim(dat),
                smooth_shading=True,
                scalar_bar_args=_pv_sbar(fg))

    if quiv:
        ss = np.s_[::stride, ::stride, idx]
        pts = np.column_stack([x[ss].ravel(), y[ss].ravel(), z[ss].ravel()])
        vec = np.column_stack([ux[ss].ravel(), uy[ss].ravel(), uz[ss].ravel()])
        umax = np.linalg.norm(vec, axis=1).max()
        if umax > 0:
            cloud = pv.PolyData(pts)
            cloud.point_data['vec'] = vec / umax
            arrows = cloud.glyph(orient='vec', scale='vec', factor=fac)
            if col:
                pl.add_mesh(arrows, color=(0.43, 0.43, 0.43))
            else:
                pl.add_mesh(arrows, scalars='GlyphScale', cmap='viridis',
                            show_scalar_bar=False)

    _pv_finish(pl, _pv_title(titl), fg, screenshot)

def isosurface3D(x,y,z,dat,frac=0.5,levels=None,cm='RdBu_r',opacity=1.0,
                 shell=True,plotbg='light',titl=None,screenshot=None):
    """
    Plot isosurfaces of a 3D field using pyvista. By default two surfaces are
    drawn at +/- frac * max|dat| (one at frac * max for a non-negative field);
    pass levels to choose the values explicitly.
    shell=True draws the translucent outer boundary for reference.
    """

    import pyvista as pv

    vmin, vmax = _clim(dat)
    if levels is None:
        if vmin == 0:
            levels = [frac*vmax]
        else:
            levels = [-frac*vmax, frac*vmax]

    vol = _pv_structured(x, y, z, dat)
    iso = vol.contour(isosurfaces=list(levels), scalars='data')
    # contour() returns float32; match the caps, or merge() drops the array
    iso.point_data['data'] = iso.point_data['data'].astype(np.float64)

    # Isosurfaces that reach r = ro are open there: cap them with the part of
    # the outer surface beyond each level, coloured by the boundary values.
    sl = np.s_[..., -1:]
    outer = _pv_structured(x[sl], y[sl], z[sl], dat[sl])
    for lev in levels:
        cap = outer.clip_scalar(scalars='data', value=lev, invert=bool(lev < 0))
        if cap.n_points > 0:
            iso = iso.merge(cap.extract_surface(algorithm='dataset_surface'))

    # clean() merges the duplicated points at phi = 0, 2 pi and at the poles,
    # which differ by round-off (sin(2 pi) != 0), and joins caps to surfaces
    iso = iso.extract_surface(algorithm='dataset_surface').clean(tolerance=1e-9, absolute=True)

    pl, fg = _pv_plotter(plotbg, screenshot)

    if iso.n_points > 0:
        pl.add_mesh(iso, scalars='data', cmap=cm, clim=[vmin, vmax],
                    opacity=opacity, smooth_shading=True, split_sharp_edges=True,
                    scalar_bar_args=_pv_sbar(fg))
    else:
        print("No isosurface found at levels", levels)

    if shell:
        # slightly inside ro so it does not poke through the caps
        ro = np.sqrt(x**2 + y**2 + z**2).max()
        pl.add_mesh(pv.Sphere(radius=0.99*ro, theta_resolution=90, phi_resolution=90),
                    color=fg, opacity=0.08)

    _pv_finish(pl, _pv_title(titl), fg, screenshot)
