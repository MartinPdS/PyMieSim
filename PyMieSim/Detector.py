import numpy as np
import fibermodes

from PyMieSim.BaseClasses import BaseDetector, MeshProperty
from PyMieSim.utils import interp_at, NA2Angle, Sp2Cart
from PyMieSim.Physics import FraunhoferDiffraction, _Polarization, SMF28, Angle


class Photodiode(BaseDetector, MeshProperty):
    """Detector type class representing a photodiode, light coupling is
    thus independant of the phase of the latter.

    Parameters
    ----------
    NA : :class:`float`
        Numerical aperture of imaging system.
    Sampling : :class:`int`
        Number of sampling points for the mode (inside NA).
    GammaOffset : :class:`float`
        Angle offset of detector in the direction perpendicular to polarization.
    PhiOffset : :class:`float`
        Angle offset of detector in the direction parallel to polarization.
    Filter : :class:`float`
        Angle of polarization filter in front of detector. Default is "None"
    CouplingMode : :class:`str`
        Methode for computing mode coupling. Either Centered or Mean.

    """

    def __init__(self,
                 NA:           float,
                 Sampling:     int    = 400,
                 GammaOffset:  float  = 0,
                 PhiOffset:    float  = 0,
                 Filter:       float  = None,
                 CouplingMode: str    = 'Centered'):


        self.CouplingMode = ('Intensity', CouplingMode)

        self._GammaOffset, self._PhiOffset = GammaOffset, PhiOffset

        self._Filter = _Polarization(Filter)

        self.Mesh = self.SphericalMesh(Sampling    = Sampling,
                                       MaxAngle    = NA2Angle(NA).Radian,
                                       PhiOffset   = PhiOffset,
                                       GammaOffset = GammaOffset,
                                       Structured  = False)

        self.Scalar = self.UnstructuredFarField()


    def UnstructuredFarField(self):
        return np.ones(self.Mesh.Sampling)


    def UpdateUnstructuredFarField(self):
        self.Scalar = np.ones(self.Mesh.Sampling)


    def StructuredFarField(self, Num = 100, SFactor = None):
        """
        Compute the FarField in a structured Mesh.

        Parameters
        ----------
        Num : :class:`int`
            Dimension of the structured mesh [Num, Num].
        SFactor : :class:`float`
            Unused parameter added to match :class:`LPmode` class.

        Returns
        -------
        :class`numpy.ndarray`:
            Structured FarField value.

        """

        return np.ones([Num, Num])


    def __repr__(self):

        return f"""
        Photodiode detector
        Coupling Mode: Intensity
        Sampling:      {self.Mesh.Sampling}
        Gamma offset:  {self.Mesh.GammaOffset}
        Phi offset:    {self.Mesh.PhiOffset}
        """


class LPmode(BaseDetector, MeshProperty):
    """Detector type class representing a fiber LP mode, light coupling is
    thus dependant of the phase of the latter.

    Parameters
    ----------
    Mode : :class:`tuple`
        LP mode index l, m.
    NA : :class:`float`
        Numerical aperture of imaging system.
    Sampling : :class:`int`
        Number of sampling points for the mode (inside NA).
    InterpSampling : :class:`int`
        Number of sampling point for interpolation of FarField mode.
    GammaOffset : :class:`float`
        Angle offset of detector in the direction perpendicular to polarization.
    PhiOffset : :class:`float`
        Angle offset of detector in the direction parallel to polarization.
    Filter : :class:`float`
        Angle of polarization filter in front of detector. Default is "None"
    CouplingMode : :class:`str`
        Methode for computing mode coupling. Either [Centered or Mean].

    """

    def __init__(self,
                 Mode:           tuple,
                 NA:             float,
                 Sampling:       int   = 401,
                 InterpSampling: int   = 101,
                 GammaOffset:    float = 0,
                 PhiOffset:      float = 0,
                 Filter:         float =  None,
                 CouplingMode:   str   = 'Centered'):

        if len(Mode) <= 2: Mode = Mode[0], Mode[1], 'h'

        assert Mode[2] in ['v','h',''], "Mode orientation should either be v [vertical] or h [horizontal]"

        assert CouplingMode in ['Centered','Mean'], "Coupling mode can either be Centered or Mean"

        assert NA < 1, "Numerical aperture has to be under 1 radian"

        self.CouplingMode = ('Amplitude', CouplingMode)

        self._Filter = _Polarization(Filter)

        self.ModeNumber = Mode[0], Mode[1], Mode[2]

        self.Mesh = self.SphericalMesh(Sampling    = Sampling,
                                       MaxAngle    = NA2Angle(NA).Radian,
                                       PhiOffset   = PhiOffset,
                                       GammaOffset = GammaOffset,
                                       Structured  = False)

        self.Scalar = self.FarField(Num = InterpSampling, Interpolate=True)


    def StructuredFarField(self, Num = 100, SFactor = None):
        """
        Compute the FarField in a structured Mesh.

        Parameters
        ----------
        Num : :class:`int`
            Dimension of the structured mesh [Num, Num].
        SFactor : :class:`float`
            Unused parameter added to match :class:`LPmode` class.

        Returns
        -------
        :class`numpy.ndarray`:
            Structured FarField value.

        """

        return self.FarField(Num, Interpolate=False)


    def FarField(self, Num, Interpolate):
        """
        Compute the FarField in a structured Mesh and interpolate the Mesh.

        Parameters
        ----------
        Num : :class:`int`
            Dimension of the structured mesh [Num, Num].

        Returns
        -------
        :class:`FraunhoferDiffraction`
            Structured FarField value.

        """

        mode = SMF28(mode = (self.ModeNumber[0],self.ModeNumber[1]) , Num=Num)

        if self.ModeNumber[2] == 'h': mode = mode.T

        mode = FraunhoferDiffraction(mode)

        if not Interpolate: return FraunhoferDiffraction(mode)

        self._phi, self._theta = self.SphericalMesh(Sampling    = mode.shape[0],
                                                    MaxAngle    = self.Mesh.MaxAngle,
                                                    PhiOffset   = 0,
                                                    GammaOffset = 0,
                                                    Structured  = True)


        return interp_at(x           = self._phi.flatten(),
                         y           = self._theta.flatten(),
                         v           = mode.astype(np.complex).flatten(),
                         xp          = self.Mesh.base[0],
                         yp          = self.Mesh.base[1],
                         algorithm   = 'linear',
                         extrapolate = True)




    def __repr__(self):
        return f"""
        LP mode detector
        Coupling Mode: Amplitude
        LP Mode:       {(self.ModeNumber[0]-1, self.ModeNumber[1], self.ModeNumber[2])}
        Sampling:      {self.Mesh.Sampling}
        Gamma offset:  {self.Mesh.GammaOffset}
        Phi offset:    {self.Mesh.PhiOffset}
        """



def PlotSpherical(phi, theta, scalar=None):
    from mayavi import mlab
    X = np.linspace(-1,1,10)*1.3
    Y = np.linspace(-1,1,10)*1.3
    Z = np.linspace(-1,1,10)*2

    zeros = np.zeros_like(X)

    fig = mlab.figure(size=(600,300))

    mlab.plot3d(X, zeros, zeros, line_width=1e-12)
    mlab.plot3d(zeros, Y, zeros, line_width=1e-12)
    mlab.plot3d(zeros, zeros, Z, line_width=1e-12)


    coord = Sp2Cart(phi*0+1, phi, theta)
    if isinstance(scalar, np.ndarray):
        mlab.points3d(*coord, scalar)
    else:
        mlab.points3d(*coord)
    mlab.show()


# -
