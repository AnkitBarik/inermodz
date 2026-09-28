"""Smoke tests for the plotting routines (rendered off-screen)."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pytest

from inermodz.mode import inerMod
from inermodz.plotlib import _clim


@pytest.fixture(scope='module')
def mode():
    return inerMod(l=7, m=3, n=1, nr=17, nphi=64, ntheta=33, norm=True)


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close('all')


def test_clim():
    assert _clim(np.array([0., 2., 3.])) == (0., 3.)
    assert _clim(np.array([-1., 2.])) == (-2., 2.)


@pytest.mark.parametrize('field', ['up', 'ke'])
@pytest.mark.parametrize('method', ['surf', 'slice', 'equat'])
def test_2d_plots(mode, method, field):
    getattr(mode, method)(field)
    assert plt.get_fignums()


def test_orthographic(mode):
    mode.surf('us', proj='Orthographic')
    assert plt.get_fignums()


# ---------------------------------------------------------------- pyvista

pv = pytest.importorskip('pyvista')


@pytest.fixture
def captured_meshes(monkeypatch):
    meshes = []
    orig = pv.Plotter.add_mesh

    def spy(self, mesh, *args, **kwargs):
        meshes.append((mesh, kwargs))
        return orig(self, mesh, *args, **kwargs)

    monkeypatch.setattr(pv.Plotter, 'add_mesh', spy)
    return meshes


def open_edges(mesh):
    return mesh.extract_feature_edges(boundary_edges=True, feature_edges=False,
                                      manifold_edges=False,
                                      non_manifold_edges=False).n_cells


@pytest.mark.parametrize('field', ['up', 'uz', 'ur', 'ke'])
def test_isosurfaces_closed(mode, field, tmp_path, captured_meshes):
    out = tmp_path / 'iso.png'
    mode.iso(field, frac=0.4, screenshot=str(out))
    assert out.stat().st_size > 0
    iso, kwargs = captured_meshes[0]
    assert iso.n_points > 0
    assert open_edges(iso) == 0     # capped on r = ro and joined at phi = 0


def test_iso_energy_colours(mode, tmp_path, captured_meshes):
    mode.iso('ke', screenshot=str(tmp_path / 'ke.png'))
    _, kwargs = captured_meshes[0]
    assert kwargs['cmap'] == 'viridis'
    assert kwargs['clim'][0] == 0


def test_iso_explicit_levels(mode, tmp_path, captured_meshes):
    mode.iso('uz', levels=[0.3], screenshot=str(tmp_path / 'l.png'))
    iso, _ = captured_meshes[0]
    assert iso.n_points > 0


@pytest.mark.parametrize('col', [True, False])
def test_surface3D(mode, col, tmp_path):
    out = tmp_path / 'surf.png'
    mode.surf('ur', r=0.7, mode='3D', col=col, screenshot=str(out))
    assert out.stat().st_size > 0


def test_surface3D_dark(tmp_path):
    M = inerMod(l=4, m=2, nr=9, nphi=32, ntheta=17, plotbg='dark')
    M.surf('ke', mode='3D', quiv=False, screenshot=str(tmp_path / 'd.png'))
    M.iso('us', screenshot=str(tmp_path / 'i.png'))
