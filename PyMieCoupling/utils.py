import numpy as np
import fibermodes
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import scipy
import numpy

class Source(object):

    def __init__(self,
                 Wavelength:   float,
                 Polarization: float,
                 Power:        float = 1):

        self.Wavelength = Wavelength

        self.k = 2 * np.pi / Wavelength

        self.Power = Power

        if Polarization != None:
            self.Polarization = _Polarization(Polarization)
        else:
            self.Polarization = None


class _Polarization(object):

    def __init__(self, input,):
        if input == 'None':
            self.Degree = 'None'
            self.Radian = 'None'
        else:
            self.Degree = input
            self.Radian = np.deg2rad(input)



class Angle(object):

    def __init__(self, input, unit='Degree'):
        if input == 'None':
            self.Degree = 'None'
            self.Radian = 'None'

        if unit == 'Degree':
            self.Degree = input
            self.Radian = np.deg2rad(input)
        if unit == 'Radian':
            self.Degree = np.rad2deg(input)
            self.Radian = input


def SMF28():
    CoreDiameter = 8.2e-6
    cladDiameter = 125e-6

    Fiber = fiber(core_radius = CoreDiameter,
                  core_index  = 1.4456,
                  clad_radius = cladDiameter,
                  clad_index  = 1.4444)

    return Fiber, CoreDiameter



class fiber(object):

    def __init__(self,
                 core_radius,
                 core_index,
                 clad_radius,
                 clad_index):

        self.MaxDirect = 2 * clad_radius

        factory = fibermodes.FiberFactory()

        factory.addLayer(name     = 'core',
                         radius   = core_radius,
                         material = 'Fixed',
                         geometry = "StepIndex",
                         index    = 1.4489)

        factory.addLayer(name     = 'cladding',
                         material = 'Fixed',
                         index    = 1)

        self.source = factory[0]


def _InterpFull(Meshes, Scalar, Shape):

    ThetaMesh, PhiMesh = np.mgrid[-np.pi:np.pi:complex(Shape[0]),
                                  -np.pi/2:np.pi/2:complex(Shape[1])]

    ZReal = griddata((Meshes.Theta.Radian, Meshes.Phi.Radian),
                      Scalar.astype(np.complex).flatten(),
                      (ThetaMesh.flatten(), PhiMesh.flatten()),
                      fill_value = np.nan + np.nan*1j,
                      method     = 'linear')



    return ZReal, PhiMesh, ThetaMesh


def InterpFull(Meshes, Scalar, Shape):

    ThetaMesh, PhiMesh = np.mgrid[-np.pi:np.pi:complex(Shape[0]),
                                  -np.pi/2:np.pi/2:complex(Shape[1])]

    Para, Perp = GetFieldsFromMesh(m                    = self.Index,
                                   x                    = self.SizeParam,
                                   ThetaMesh            = ThetaMesh.flatten(),
                                   PhiMesh              = PhiMesh.flatten(),
                                   Polarization         = 0);


    ZReal = griddata((Meshes.Theta.Radian, Meshes.Phi.Radian),
                      Scalar.astype(np.complex).flatten(),
                      (ThetaMesh.flatten(), PhiMesh.flatten()),
                      fill_value = np.nan + np.nan*1j,
                      method     = 'linear')



    return ZReal, PhiMesh, ThetaMesh



def PlotUnstructureData(Scalar, phi, theta):

    fig, ax = plt.subplots(1,2,figsize=(15,8))
    im0 = ax[0].tripcolor(theta, phi, Scalar.real)
    im1 = ax[1].tripcolor(theta, phi, Scalar.imag)
    plt.colorbar(mappable=im0, ax=ax[0])
    plt.colorbar(mappable=im1, ax=ax[1])
    ax[0].plot(theta, phi, 'ko ', markersize=2)
    ax[1].plot(theta, phi, 'ko ', markersize=2)

    plt.show()



def interp_at(x, y, v, xp, yp, algorithm='cubic', extrapolate=False):
    """
    Interpolate data onto the specified points.

    Parameters:

    * x, y : 1D arrays
        Arrays with the x and y coordinates of the data points.
    * v : 1D array
        Array with the scalar value assigned to the data points.
    * xp, yp : 1D arrays
        Points where the data values will be interpolated
    * algorithm : string
        Interpolation algorithm. Either ``'cubic'``, ``'nearest'``,
        ``'linear'`` (see scipy.interpolate.griddata)
    * extrapolate : True or False
        If True, will extrapolate values outside of the convex hull of the data
        points.

    Returns:

    * v : 1D array
        1D array with the interpolated v values.

    """
    if algorithm not in ['cubic', 'linear', 'nearest']:
        raise ValueError("Invalid interpolation algorithm: " + str(algorithm))
    grid = scipy.interpolate.griddata((x, y),
                                      v,
                                      (xp, yp),
                                      method=algorithm).ravel()
    if extrapolate and algorithm != 'nearest' and numpy.any(numpy.isnan(grid)):
        grid = extrapolate_nans(xp, yp, grid)
    return grid

def extrapolate_nans(x, y, v):
    """
    Extrapolate the NaNs or masked values in a grid INPLACE using nearest
    value.

    .. warning:: Replaces the NaN or masked values of the original array!

    Parameters:

    * x, y : 1D arrays
        Arrays with the x and y coordinates of the data points.
    * v : 1D array
        Array with the scalar value assigned to the data points.

    Returns:

    * v : 1D array
        The array with NaNs or masked values extrapolated.

    """
    if numpy.ma.is_masked(v):
        nans = v.mask
    else:
        nans = numpy.isnan(v)
    notnans = numpy.logical_not(nans)
    v[nans] = scipy.interpolate.griddata((x[notnans], y[notnans]), v[notnans],
                                         (x[nans], y[nans]),
                                         method='nearest').ravel()
    return v
