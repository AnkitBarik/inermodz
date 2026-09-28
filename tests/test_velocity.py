"""Velocity fields (Zhang et al. 2001, eqs. 4.1, 4.6) satisfy the inviscid
equations (2.7a-c), the boundary condition (2.8) and the symmetries (2.9)."""

import numpy as np
import pytest

from inermodz.sigma import sigma
from inermodz.velocity import vel

rng = np.random.default_rng(0)
R = rng.uniform(0.2, 0.9, 100)
TH = rng.uniform(0.2, np.pi - 0.2, 100)
S0, Z0 = R * np.sin(TH), R * np.cos(TH)


def amplitudes(point_grid, m, N, symm, sig, s, z):
    """Return real A, B, D with (Us, Uphi, Uz) = (-iA, B, iD) e^{i m phi}."""
    kw = dict(m=m, N=N, symm=symm, sigma=sig, nr=1, nphi=1, ntheta=1)
    v1 = vel(grid=point_grid(s, z, np.pi / (2 * m)), **kw)   # sin(m phi) = 1
    v0 = vel(grid=point_grid(s, z, 0.), **kw)                # cos(m phi) = 1
    return v1.Us, v0.Up, -v1.Uz


CASES = ([('es', m, N) for m in (1, 3, 10, 20) for N in (1, 2, 3, 4)] +
         [('ea', m, N) for m in (1, 3, 10, 20) for N in (0, 1, 2, 3, 4)])


@pytest.mark.parametrize('symm, m, N', CASES)
def test_equations_and_boundary(point_grid, symm, m, N):
    h = 1e-5
    for sig in np.real(sigma(m=m, N=N, symm=symm)):
        f = lambda s, z: amplitudes(point_grid, m, N, symm, sig, s, z)
        A, B, D = f(S0, Z0)
        Ap, Bp, _ = f(S0 + h, Z0)
        Am, Bm, _ = f(S0 - h, Z0)
        Azp, Bzp, Dzp = f(S0, Z0 + h)
        Azm, Bzm, Dzm = f(S0, Z0 - h)
        dsA = ((S0 + h) * Ap - (S0 - h) * Am) / (2 * h)
        dsB = ((S0 + h) * Bp - (S0 - h) * Bm) / (2 * h)
        Az, Bz, Dz = [(p - q) / (2 * h) for p, q in
                      ((Azp, Azm), (Bzp, Bzm), (Dzp, Dzm))]
        scale = np.abs([A, B, D]).max()

        # (2.7a-c) with Us = -iA, Uphi = B, Uz = iD
        res_a = -S0 * Az + sig * S0 * Bz + m * sig * D
        res_b = -dsA + sig * dsB + m * B - m * sig * A
        res_c = -dsA + m * B + S0 * Dz
        for res in (res_a, res_b, res_c):
            assert np.abs(res).max() / scale < 1e-5

        # (2.8): s Us + z Uz = 0 on r = 1 (no finite differences: tight)
        sb, zb = np.sin(TH), np.cos(TH)
        Ab, _, Db = f(sb, zb)
        assert np.abs(-sb * Ab + zb * Db).max() / scale < 1e-9


@pytest.mark.parametrize('symm, m, N', [('es', 2, 2), ('ea', 3, 2)])
def test_equatorial_symmetry(symm, m, N):
    v = vel(m=m, N=N, symm=symm, sigma=sigma(m=m, N=N, symm=symm)[0],
            nr=9, nphi=16, ntheta=33)
    flip = lambda a: a[:, ::-1, :]    # theta -> pi - theta, i.e. z -> -z
    sign = 1 if symm == 'es' else -1  # (2.9a) and (2.9b)
    np.testing.assert_allclose(v.Up, sign * flip(v.Up), atol=1e-12 * np.abs(v.Up).max())
    np.testing.assert_allclose(v.Us, sign * flip(v.Us), atol=1e-12 * np.abs(v.Us).max())
    np.testing.assert_allclose(v.Uz, -sign * flip(v.Uz), atol=1e-12 * np.abs(v.Uz).max())


def test_sigma_computed_when_not_given():
    sig = sigma(m=2, N=1, symm='ea')[1]
    a = vel(m=2, N=1, n=2, symm='ea', nr=5, nphi=8, ntheta=8)
    b = vel(m=2, N=1, symm='ea', sigma=sig, nr=5, nphi=8, ntheta=8)
    np.testing.assert_allclose(a.Us, b.Us)


def test_normalisation_all_components():
    v = vel(m=2, N=2, symm='es', sigma=sigma(m=2, N=2)[1],
            nr=65, nphi=128, ntheta=128, norm=True)
    g = v.grid

    def mean_sq(*comps):
        e = sum(c**2 for c in comps) * g.r3D**2 * np.sin(g.th3D)
        I = np.trapezoid(np.trapezoid(np.trapezoid(e, g.phi, axis=0),
                                      g.theta, axis=0), g.r)
        return I / (4. / 3. * np.pi)

    assert mean_sq(v.Us, v.Up, v.Uz) == pytest.approx(1, rel=1e-6)
    assert mean_sq(v.Ur, v.Utheta, v.Up) == pytest.approx(1, rel=1e-6)
    assert mean_sq(v.Ux, v.Uy, v.Uz) == pytest.approx(1, rel=1e-6)
