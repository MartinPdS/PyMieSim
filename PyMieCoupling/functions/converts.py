import numpy as np
import cupy as cp
from PyMieCoupling.classes.Misc import Operation as Op


def rad2deg(RadSpace):

        return RadSpace * 180/Op.pi


def deg2rad(AngleSpace):

    return AngleSpace * Op.pi/180



def Angle2Direct(AngleVec, k, cuda=False):

    RadSpace = AngleVec*np.pi/180

    FourierSpace = Op.sin(RadSpace)*k/(2*np.pi)

    fourier_unit = (FourierSpace[1]-FourierSpace[0]).__abs__()

    DirectSpace = Op.fft(cuda).fftshift(np.fft.fftfreq(np.shape(AngleVec)[0], d=fourier_unit))

    return DirectSpace


def Direct2Angle(DirectVec, k, cuda=False):

    direct_unit = (DirectVec[1]-DirectVec[0]).__abs__()

    FourierSpace = Op.fft(cuda).fftshift(Op.fft(cuda).fftfreq(np.shape(DirectVec)[0], d=direct_unit))

    AngleVec = Op.arcsin(2 * Op.pi * FourierSpace / k) #conversion spatial frequency to angular space

    if np.nan in AngleVec:
        raise Exception('Warning ill defined resolution -> angle definition!')

    return AngleVec* 180/Op.pi



def NA2Angle(NA, cuda=False):

    Angle = rad2deg( Op.arcsin(NA) )

    __ThetaBound = Op.array(cuda)([-Angle, Angle])

    __PhiBound = Op.array(cuda)([-Angle, Angle])


    return __ThetaBound, __PhiBound



def CuPy2NumPy(*items):
    ItemList = []
    for item in items:
        if isinstance(item, cp.ndarray):
            ItemList.append(cp.asnumpy(item))
        else:
            ItemList.append(item)

    temp = tuple(ItemList)

    return (*temp,)






# -
