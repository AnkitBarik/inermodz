# InerModZ
[![Tests](https://github.com/AnkitBarik/inermodz/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/AnkitBarik/inermodz/actions/workflows/tests.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Python routines to compute and display inertial modes of a full sphere according to the analytical solution provided by Zhang et al. 2001, JFM.

Requires the libraries [cartopy](https://scitools.org.uk/cartopy/docs/latest/) and [pyvista](https://docs.pyvista.org/) for 2D map projections and 3D plots (surfaces of constant radius and isosurfaces). Install all dependencies with `pip install -r requirements.txt`.

## Classes

* ```inerMod``` : This is the inertial mode class. Contains the subclasses ```vel``` and ```grid``` and methods ```surf```, ```slice```, ```equat``` and ```iso``` for visualisation.

* ```vel``` : This is the velocity class. Provides the three velocity components of a mode. Contains the subclass ```grid```.

* ```grid``` : This provides access to the grid variables (r,\theta,\phi), including 3D ones.

* ```sigma```: This provides the half-frequencies for a single mode defined by (`l`,`m`,`N`).

## Tests

Run the test suite with `pytest` from the repository root. It checks the frequencies against the values in Zhang et al. (2001) (figures 1, 2 and table 1), verifies that the velocity fields satisfy the governing equations, boundary condition and equatorial symmetries, and renders every plot off-screen. The 3D plotting tests are skipped if pyvista is not installed.
