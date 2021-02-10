import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
import numpy as np
import matplotlib
import cartopy.crs as ccrs
from ai import cs

from PyMieCoupling.classes.Representations import S1S2, SPF, Stokes, Field, ScalarFarField
from PyMieCoupling.functions.Couplings import Coupling as Coupling, GetFootprint
from PyMieCoupling.cpp.Interface import GetFields, GetEfficiencies
from PyMieCoupling.functions.converts import NA2Angle
from PyMieCoupling.Physics import _Polarization, Angle
from PyMieCoupling.utils import PlotFarField, InterpFull, PlotUnstructuredSphere, PlotStructuredSphere


##__ref__: efficiencies: https://www.osapublishing.org/DirectPDFAccess/EDD7305D-C863-9711-44D9A02B1BAD39CF_380136/josaa-35-1-163.pdf?da=1&id=380136&seq=0&mobile=no



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
    """Short summary.

    Parameters
    ----------
    size : float
        Size of the detector, [diameter for circle shaped/ side for square].
    shape : str
        Shape of the detector.
    wavelength : float
        Wavelength of the incoming source.
    npts : int
        Number of points defining the rastered meshes.
    GammaOffset : float
        Offset of theta angle between the detector and source.
    PhiOffset : float
        Offset of phi angle between the detector and source.
    Magnification : float
        Magnification induced by the lense.
    Name : str
        Name of detector [optional for plots].

    """


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

        #ax1.set_extent([-170, 170, -90, 90], crs=ccrs.PlateCarree())

        #fig.tight_layout()
        plt.show()






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
    diameter
    wavelength
    index
    npts

    """
    def __init__(self):
        pass

    def GetEfficiencies(self):
        self._Qsca, self._Qext, self._Qabs = GetEfficiencies(m = self.Index,
                                                             x = self.SizeParam)



    def S1S2(self, Num=200):
        if self._S1S2 is None:
            self._S1S2 = S1S2(Parent=self, Num=Num)
            return self._S1S2

        else:
            return self._S1S2

    @property
    def Qext(self):
        if self._Qext:
            return self._Qext
        else:
            self.GetEfficiencies()
            return self._Qext

    @property
    def Qsca(self):
        if self._Qsca:
            return self._Qsca
        else:
            self.GetEfficiencies()
            return self._Qsca

    @property
    def Qabs(self):
        if self._Qabs:
            return self._Qabs
        else:
            self.GetEfficiencies()
            return self._Qabs




    def Field(self, Num=200):
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
        if not self._SPF:
            self._SPF = SPF(Parent=self, Num=Num)
            return self._SPF
        else:
            return self._SPF


    def GenField(self, Phi, Theta):
        """The methode generate the <Fields> class from S1 and S2 value computed
        with the PyMieScatt package.
        """

        return GetFields(m            = self.Index,
                         x            = self.SizeParam,
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