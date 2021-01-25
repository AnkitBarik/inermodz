# InerModZ
Python routines to compute and display inertial modes of a full sphere according to the analytical solution provided by Zhang et al. 2001, JFM.

Requires the libraries [cartopy](https://scitools.org.uk/cartopy/docs/latest/) and [mayavi](https://docs.enthought.com/mayavi/mayavi/) for 2D map projections and 3D surface plots on constant radial surfaces.

## Classes

* ```inerMod``` : This is the inertial mode class. Contains the subclasses ```vel``` and ```grid``` and methods ```surf``` and ```slice``` for visualisation.

* ```vel``` : This is the velocity class. Provides the three velocity components of a mode. Contains the subclass ```grid```.

* ```grid``` : This provides access to the grid variables (r,\theta,\phi), including 3D ones.

* ```sigma```: This provides the half-frequencies for a single mode defined by (`l`,`m`,`N`).
