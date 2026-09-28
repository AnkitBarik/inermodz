"""Frequencies against Zhang et al. (2001), eqs. (2.15), (2.16)."""

import math

import numpy as np
import pytest

from inermodz.libzhang import factorial, dfactorial
from inermodz.sigma import sigma


def omegas(m, N, symm='es'):
    return np.sort(np.real(sigma(m=m, N=N, symm=symm))) * 2


# Figures 1 and 2 of the paper, N = 2
@pytest.mark.parametrize('m, ref', [
    (8, [-0.8107, -0.1450, 0.5037, 1.1187]),
    (1, [-1.1834, -0.0682, 1.0456, 1.8060]),
])
def test_figure_frequencies(m, ref):
    np.testing.assert_allclose(omegas(m, 2), ref, atol=1e-4)


# Table 1 of the paper: exact frequencies of the slow, nearly geostrophic
# (retrograde, smallest |omega|) waves. The row labelled "2" between N = 5
# and N = 7 in the paper is a typo for N = 6.
TABLE1 = {
    1: {1: -0.17661, 2: -0.06819, 3: -0.03615, 4: -0.02239, 5: -0.01523,
        6: -0.01103, 7: -0.00836, 8: -0.00655, 10: -0.00433},
    8: {1: -0.25653, 2: -0.14502, 3: -0.09681, 4: -0.07023, 5: -0.05366,
        6: -0.04251, 7: -0.03459, 8: -0.02874, 10: -0.02081},
}


@pytest.mark.parametrize('m, N, ref', [(m, N, ref) for m in TABLE1
                                       for N, ref in TABLE1[m].items()])
def test_geostrophic_table(m, N, ref):
    om = omegas(m, N)
    assert om[om < 0].max() == pytest.approx(ref, abs=1e-5)


@pytest.mark.parametrize('m, N, ref', [(1, 1, -0.17661), (8, 1, -0.25653)])
def test_geostrophic_approximation_exact_for_N1(m, N, ref):
    # Eq. (4.5) is exact for N = 1
    approx = -2. / (m + 2) * (np.sqrt(1 + m * (m + 2) / (N * (2 * N + 2 * m + 1))) - 1)
    assert approx == pytest.approx(ref, abs=1e-5)


@pytest.mark.parametrize('symm, nroots', [('es', lambda N: 2 * N),
                                          ('ea', lambda N: 2 * N + 1)])
@pytest.mark.parametrize('m', [1, 2, 5, 20])
@pytest.mark.parametrize('N', [1, 2, 4, 6])
def test_roots_real_and_bounded(symm, nroots, m, N):
    sig = sigma(m=m, N=N, symm=symm)
    assert len(sig) == nroots(N)
    assert np.all(np.abs(np.imag(sig)) < 1e-10)
    assert np.all(np.abs(np.real(sig)) < 1)      # |omega| < 2
    assert len(np.unique(np.round(np.real(sig), 10))) == len(sig)


def test_spin_over_mode():
    # (l, m) = (2, 1) antisymmetric mode: omega = 1
    assert omegas(1, 0, 'ea') == pytest.approx([1.0])


@pytest.mark.parametrize('n', [0, 1, 2, 5, 21, 40, 60])
def test_factorials_exact(n):
    assert factorial(n) == math.factorial(n)
    assert dfactorial(n) == math.prod(range(n, 0, -2))


def test_dfactorial_minus_one():
    assert dfactorial(-1) == 1
