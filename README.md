# InerModZ
Python routines to compute and display inertial modes of a full sphere according to the analytical solution provided by Zhang et al. 2001, JFM.

## Classes

* ```inerMod``` : This is the inertial mode class. Contains the subclasses ```vel``` and ```grid``` and methods ```surf``` and ```slice``` for visualisation.

* ```vel``` : This is the velocity class. Provides the three velocity components of a mode. Contains the subclass ```grid```.

* ```grid``` : This provides access to the grid variables $(r,\theta,\phi,s,z)$, including 3D ones.

* ```sigma```: This provides the half-frequencies for a single mode defined by (`l`,`m`,`N`).
