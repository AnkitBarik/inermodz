import numpy as np
import pytest

from inermodz.mode import inerMod

SMALL = dict(nr=5, nphi=8, ntheta=8)


def test_default_mode():
    M = inerMod(**SMALL)
    assert (M.l, M.m, M.N, M.n, M.symm) == (3, 1, 1, 1, 'es')
    assert M.omega == pytest.approx(1.50994, abs=1e-5)


@pytest.mark.parametrize('kw, l, N, symm', [
    (dict(l=6, m=2), 6, 2, 'es'),
    (dict(l=7, m=2), 7, 2, 'ea'),
    (dict(l=3, m=2), 3, 0, 'ea'),
    (dict(m=2, N=2, symm='es'), 6, 2, 'es'),
    (dict(m=2, N=2, symm='ea'), 7, 2, 'ea'),
    (dict(m=2, N=2, symm='EA'), 7, 2, 'ea'),
])
def test_l_N_symm_consistent(kw, l, N, symm):
    M = inerMod(**SMALL, **kw)
    assert (M.l, M.N, M.symm) == (l, N, symm)


@pytest.mark.parametrize('kw, match', [
    (dict(m=0, N=2), 'm must be >= 1'),
    (dict(m=2, N=0), 'No es modes'),
    (dict(l=2, m=2), 'No es modes'),
    (dict(m=2, N=1, n=5), 'n must be between 1 and 2'),
    (dict(m=2, N=1, n=0), 'n must be between'),
    (dict(m=2, symm='xx'), "symm must be 'es' or 'ea'"),
])
def test_invalid_input(kw, match):
    with pytest.raises(ValueError, match=match):
        inerMod(**SMALL, **kw)


@pytest.mark.parametrize('field, attr', [
    ('us', 'Us'), ('vs', 'Us'), ('up', 'Up'), ('uphi', 'Up'), ('uz', 'Uz'),
    ('vz', 'Uz'), ('ur', 'Ur'), ('vr', 'Ur'), ('ut', 'Utheta'), ('UTHETA', 'Utheta'),
])
def test_get_data(field, attr):
    M = inerMod(**SMALL)
    data, titl = M.get_data(field)
    assert data is getattr(M.U, attr)
    assert titl.startswith('$')


def test_get_data_energy():
    M = inerMod(**SMALL)
    data, _ = M.get_data('ke')
    np.testing.assert_allclose(data, 0.5 * (M.U.Us**2 + M.U.Up**2 + M.U.Uz**2))


@pytest.mark.parametrize('field, cm, expected', [
    ('ke', None, 'viridis'), ('energy', None, 'viridis'),
    ('us', None, 'RdBu_r'), ('ke', 'magma', 'magma'),
])
def test_default_colormap(field, cm, expected):
    assert inerMod(**SMALL)._cmap(field, cm) == expected
