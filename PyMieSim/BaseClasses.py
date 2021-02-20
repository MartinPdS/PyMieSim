#!/usr/bin/env python
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
import numpy as np
import matplotlib
import cartopy.crs as ccrs
from ai import cs

from PyMieSim.Representations import S1S2, SPF, Stokes, Field, ScalarFarField
from PyMieSim.functions.Couplings import Coupling as Coupling, GetFootprint
from PyMieSim.cpp.Sphere import GetFields, GetEfficiencies
from PyMieSim.functions.converts import NA2Angle
from PyMieSim.Physics import _Polarization, Angle
from PyMieSim.utils import PlotFarField, InterpFull, PlotUnstructuredSphere, PlotStructuredSphere


##__ref__: efficiencies: https://www.osapublishing.org/DirectPDFAccess/EDD7305D-C863-9711-44D9A02B1BAD39CF_380136/josaa-35-1-163.pdf?da=1&id=380136&seq=0&mobile=no

class BaseSource(object):

    def __init__(self,
                 Wavelength,
                 Polarization,
                 NA = 0.2):

        self.Wavelength = Wavelength
        self.k = 2 * np.pi / Wavelength
        self.Polarization = _Polarization(Polarization)

class MeshProperty(object):
    """Short summary.

    """
    def __init__(self):
        pass

    @property
    def Filter(self):
        return self._Filter

    @Filter.setter
    def Filter(self, val):
        self._Filter = Polarization(val)

    @property
    def PhiOffset(self):
        return self.Mesh.PhiOffset

    @PhiOffset.setter
    def PhiOffset(self, val):
        self.Mesh.UpdateSphere(PhiOffset = val)
        self.GetSpherical()

    @property
    def GammaOffset(self):
        return self.Mesh.GammaOffset

    @GammaOffset.setter
    def GammaOffset(self, val):
        self.Mesh.UpdateSphere(GammaOffset = val)
        self.UnstructuredFarField()

    @property
    def NA(self):
        return self._NA

    @NA.setter
    def NA(self, val):
        if val >= 0.99: val = 0.99
        if val <= 0.01: val = 0.01
        self.MaxAngle = NA2Angle(val).Radian
        self.Mesh.UpdateSphere(MaxAngle = self.MaxAngle)
        #self.UpdateUnstructuredFarField()






class BaseDetector(object):

    def Coupling(self, Scatterer):
        return Coupling(Scatterer = Scatterer, Detector = self)


    def Footprint(self, Scatterer, Num = 200):
        return GetFootprint(Scatterer = Scatterer, Detector = self, Num = Num)


    def StructuredSphericalMesh(self, Num, MaxAngle):

        x, y = np.mgrid[-50: 50: complex(Num), -50: 50: complex(Num)]

        z = 50 / np.tan(MaxAngle)

        _, phi, theta = cs.cart2sp(x, y, x*0+z)

        return phi, theta


    def Plot(self):
        Name = 'Mode Field'
        ThetaMean = np.mean(self.Mesh.Theta.Degree).round(1)
        PhiMean = np.mean(self.Mesh.Phi.Degree).round(1)

        fig, (ax0, ax1) = plt.subplots(1,
                                 2,
                                 figsize=(8,4),
                                 subplot_kw = {'projection':ccrs.LambertAzimuthalEqualArea(central_latitude=PhiMean, central_longitude=ThetaMean)})

        im0 = ax0.tricontour(self.Mesh.Theta.Degree,
                             self.Mesh.Phi.Degree,
                             self.Scalar.real,
                             levels=13,
                             linewidths=0.5,
                             colors='k',
                             transform = ccrs.PlateCarree())

        cntr0 = ax0.tricontourf(self.Mesh.Theta.Degree,
                                self.Mesh.Phi.Degree,
                                self.Scalar.real,
                                levels=13,
                                cmap="inferno",
                                transform = ccrs.PlateCarree())


        im1 = ax1.tricontour(self.Mesh.Theta.Degree,
                             self.Mesh.Phi.Degree,
                             self.Scalar.imag,
                             levels=14,
                             linewidths=0.5,
                             colors='k',
                             transform = ccrs.PlateCarree())

        cntr1 = ax1.tricontourf(self.Mesh.Theta.Degree,
                                self.Mesh.Phi.Degree,
                                self.Scalar.imag,
                                levels=14,
                                cmap="inferno",
                                transform = ccrs.PlateCarree())

        plt.colorbar(mappable=cntr1, fraction=0.046, orientation='horizontal', ax=ax1)
        plt.colorbar(mappable=cntr0, fraction=0.046, orientation='horizontal', ax=ax0)


        ax1.plot(self.Mesh.Theta.Degree,
                 self.Mesh.Phi.Degree,
                 'ko',
                 ms=0.1,
                 transform = ccrs.PlateCarree())

        ax0.plot(self.Mesh.Theta.Degree,
                 self.Mesh.Phi.Degree,
                 'ko',
                 ms=0.1,
                 transform = ccrs.PlateCarree())

        gl = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, x_inline=False, y_inline=False)
        gl.top_labels = False
        gl.left_labels = False
        gl.right_labels = False
        gl.bottom_labels = True

        gl = ax0.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, x_inline=False, y_inline=False)
        #gl.xlocator = matplotlib.ticker.FixedLocator([])
        gl.top_labels = False
        gl.left_labels = False
        gl.right_labels = False
        gl.bottom_labels = True


        ax1.set_title(f'Real Part {Name}')
        ax1.set_ylabel(r'Angle $\phi$ [Degree]')
        ax1.set_xlabel(r'Angle $\theta$ [Degree]')

        ax0.set_title(f'Imaginary Part {Name}')
        ax0.set_ylabel(r'Angle $\phi$ [Degree]')
        ax0.set_xlabel(r'Angle $\theta$ [Degree]')

        plt.show()



class EfficienciesProperties(object):
    @property
    def Qext(self):
        """Extinction efficiency:
        :math:`Q_{ext}=\\frac{2}{x^2}\sum_{n=1}^{n_{max}}(2n+1) / \\text{real} \{ a_n+b_n \}`

        """
        if self._Qext:
            return self._Qext
        else:
            self.GetEfficiencies()
            return self._Qext

    @property
    def Qsca(self):
        """Scattering efficiency:
        :math:`Q_{sca}=\\frac{2}{x^2}\sum_{n=1}^{n_{max}}(2n+1)(|a_n|^2+|b_n|^2)`

        """
        if self._Qsca:
            return self._Qsca
        else:
            self.GetEfficiencies()
            return self._Qsca

    @property
    def Qabs(self):
        """Absorption efficiency:
        :math:`Q_{abs}=Q_{ext}-Q_{sca}`

        """
        if self._Qabs:
            return self._Qabs
        else:
            self.GetEfficiencies()
            return self._Qabs



class BaseScatterer(object):
    """Base class for <Scatterer> instance.
    This class containes all the methodes that output something interesting for
    the user.

    Parameters
    ----------
    diameter : float
        Diameter of the scatterer.
    wavelength : float
        Wavelength of the incident lightfield.
    index : float
        Refractive index of the scatterer.
    npts : int
        Number of points for the full solid angle of the far-field, later to
        be interpolated.

    Attributes
    ----------
    Full : <Fields class>
        It represents the entire Far-field representation of the scatterer.
    ComputeS1S2 : type
        Methode using package PyMieScatt to compute S1 and S2 parameter form mu value.


    """

    def __init__(self):
        pass

    def GetEfficiencies(self):
        self._Qsca, self._Qext, self._Qabs = GetEfficiencies(m = self.Index,
                                                             x = self.SizeParam)


    def S1S2(self, Num=200):
        """Methode return <Representation> instance S1S2.
        For spherical Scatterer such as here S1 and S2 are computed as follow:

        :math:`S_1=\sum\limits_{n=1}^{n_{max}} \\frac{2n+1}{n(n+1)}(a_n\pi_n+b_n\\tau_n)`

        :math:`S_2=\sum\limits_{n=1}^{n_{max}}\\frac{2n+1}{n(n+1)}(a_n\\tau_n+b_n\pi_n)`

        Parameters
        ----------
        Num : type
            Description of parameter `Num`.

        Returns
        -------
        type
            Description of returned object.

        """

        if self._S1S2 is None:
            self._S1S2 = S1S2(Parent=self, Num=Num)
            return self._S1S2

        else:
            return self._S1S2


    def Field(self, Num=200):
        """Scattering phase function:
        Fields = :math:`E_{||}^2, E_{\\perp}^2`

        Parameters
        ----------
        Num : int
            Number of point to spatially (:math:`\\theta , \\phi`) evaluate the Fields [Num, Num].

        Returns
        -------
        <Field> instance
            Dictionnay subclass with all pertient information as keys.

        """
        self._Field = ScalarFarField(Num = Num, Parent = self)

        return self._Field


    def Parallel(self, Phi, Theta):
        if not np.array_equal(self._phi, Phi) or not np.array_equal(self._theta, Theta):
            self._phi, self._theta = Phi, Theta
            self._Parallel, self._Perpendicular = self.GenField(Phi, Theta)
            return self._Parallel
        else:
            return self._Parallel


    def Perpendicular(self, Phi, Theta):
        if not np.array_equal(self._phi, Phi) or not np.array_equal(self._theta, Theta):
            self._phi, self._theta = Phi, Theta
            self._Parallel, self._Perpendicular = self.GenField(Phi, Theta)
            return self._Perpendicular
        else:
            return self._Perpendicular


    def SPF(self, Num=100):
        """Scattering phase function:
        SPF = :math:`E_{||}^2 + E_{\\perp}^2`

        Parameters
        ----------
        Num : int
            Number of point to spatially (:math:`\\theta , \\phi`) evaluate the SPF [Num, Num].

        Returns
        -------
        <SPF> instance
            Dictionnay subclass with all pertient information as keys.

        """

        if not self._SPF:
            self._SPF = SPF(Parent=self, Num=Num)
            return self._SPF
        else:
            return self._SPF


    def GenField(self, Phi, Theta):
        """The methode generate the <Fields> class from S1 and S2 value computed
        with the PyMieScatt package.

        """

        return GetFields(index        = self.Index,
                         diameter     = self.Diameter,
                         wavelength   = self.Source.Wavelength,
                         nMedium      = self.nMedium,
                         ThetaMesh    = Theta,
                         PhiMesh      = Phi - np.pi/2,
                         Polarization = self.Source.Polarization.Radian)

    def Plot(self, Num=200, scatter=False):

        Theta, Phi = np.mgrid[0:2*np.pi:complex(Num), -np.pi/2:np.pi/2:complex(Num)]

        Para, Perp = self.GenField(Phi.flatten(), Theta.flatten())

        fig0 = PlotStructuredSphere(Phi     = np.rad2deg(Phi),
                                    Theta   = np.rad2deg(Theta),
                                    Scalar  = Para.reshape(Theta.shape))

        fig1 = PlotStructuredSphere(Phi     = np.rad2deg(Phi),
                                    Theta   = np.rad2deg(Theta),
                                    Scalar  = Perp.reshape(Theta.shape))

        return fig0, fig1


    def Footprint(self, Detector):
        return GetFootprint(Scatterer = self, Detector = Detector)






# -
