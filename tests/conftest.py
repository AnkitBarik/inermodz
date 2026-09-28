import os
import sys

import numpy as np
import pytest

# The repository root is the package itself, so put its parent on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Non-interactive backends so plotting tests never open windows
os.environ.setdefault('MPLBACKEND', 'Agg')
os.environ.setdefault('PYVISTA_OFF_SCREEN', 'true')


class PointGrid:
    """Minimal stand-in for inermodz.grid.grid holding arbitrary points."""

    def __init__(self, s, z, phi):
        self.s3D = s
        self.z3D = z
        self.phi3D = np.full_like(s, phi)
        self.th3D = np.arctan2(s, z)


@pytest.fixture
def point_grid():
    return PointGrid
