import numpy as np


""" Coupling Reference: Estimation of Coupling Efficiency of Optical Fiber by Far-Field Method """






def CenteredCoupling_Para(Detector, Scatterer):
    if Detector._coupling == "Intensity":
        Para = (Detector.Fourier * Scatterer.Field.Parallel).__abs__()**2
        Para = Para * np.abs(np.sin(Detector.Meshes.Phi.Mesh.Radian) )
        Para = Para.sum() * Detector.Meshes.dOmega.Radian


    if Detector._coupling == "Amplitude":
        Para = (Detector.Fourier * Scatterer.Field.Parallel)
        Para = Para * np.abs(np.sin(Detector.Meshes.Phi.Mesh.Radian) )
        Para = Para.sum() * Detector.Meshes.dOmega.Radian
        Para = Para.__abs__()**2

    return np.asscalar( Para )


def CenteredCoupling_Perp(Detector, Scatterer):
    if Detector._coupling == "Intensity":
        Perp = (Detector.Fourier * Scatterer.Field.Perpendicular ).__abs__()**2
        Perp = Perp * np.abs(np.sin(Detector.Meshes.Phi.Mesh.Radian) )
        Perp = Perp.sum() * Detector.Meshes.dOmega.Radian

    if Detector._coupling == "Amplitude":
        Perp = (Detector.Fourier * Scatterer.Field.Perpendicular)
        Perp = Perp * np.abs(np.sin(Detector.Meshes.Phi.Mesh.Radian) )
        Perp = Perp.sum()
        Perp = Perp * Detector.Meshes.dOmega.Radian
        Perp = Perp.__abs__()**2

    return np.asscalar( Perp )



def MeanCoupling_Para(Detector, Scatterer):
    Para = (Detector.Fourier * Scatterer.Field.Parallel).__abs__()**2
    Para = Para.sum()

    return np.asscalar( Para )


def MeanCoupling_Perp(Detector, Scatterer):
    Perp = (Detector.Fourier * Scatterer.Field.Perpendicular).__abs__()**2
    Perp = Perp.sum()

    return np.asscalar( Perp )


def GetFootprint(Detector, Scatterer):
    Perp = (Detector.Fourier * Scatterer.Field.Perpendicular).__abs__()**2
    Para = (Detector.Fourier * Scatterer.Field.Parallel).__abs__()**2

    return Perp + Para



def Coupling(Scatterer, Detector, Mode='Centered'):

    if Mode == 'Centered':
        return CenteredCoupling(Scatterer, Detector)

    if Mode == 'Mean':
        return MeanCoupling(Scatterer, Detector)



def CenteredCoupling(Scatterer, Detector):

    if Detector._Filter.Radian != None:
        Perp = CenteredCoupling_Perp(Detector, Scatterer) * np.cos(Detector._Filter.Radian)**2
        Para = CenteredCoupling_Para(Detector, Scatterer) * np.sin(Detector._Filter.Radian)**2
    else:
        Perp = CenteredCoupling_Perp(Detector, Scatterer)
        Para = CenteredCoupling_Para(Detector, Scatterer)

    return Perp + Para




def MeanCoupling(Scatterer, Detector):
    if Detector._Filter.Radian != None:
        Perp = MeanCoupling_Perp(Detector, Scatterer) * np.cos(Detector.Filter.Radian)**2
        Para = MeanCoupling_Para(Detector, Scatterer) * np.sin(Detector.Filter.Radian)**2
    else:
        Perp = MeanCoupling_Perp(Detector, Scatterer)
        Para = MeanCoupling_Para(Detector, Scatterer)

    return Perp + Para