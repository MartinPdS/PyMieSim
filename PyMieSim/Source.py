import numpy as np


class _Polarization(object):

    def __init__(self, input):
        if input == None:
            self.Degree = None
            self.Radian = None
        else:
            self.Degree = input
            self.Radian = np.deg2rad(input)


class PlaneWave(object):
    def __init__(self,
                 Wavelength,
                 Polarization,
                 NA = 0.2):
        self.Wavelength = Wavelength
        self.k = 2 * np.pi / Wavelength
        self.Polarization = _Polarization(Polarization)

    def expansion(self, n):
        return (-1j)**n/(self.k*1j) * (2*n+1) / (n*(n+1));

    def BSC(self, n, m, mode='TE'):
        """Return the beam shape coefficients
         (:math:`g^{l}_{n, TE}`, :math:`g^{l}_{n, TM}`) for a plane wave.
         (Eq: VI.77 of G&G)

        Parameters
        ----------
        n : class:`int`
            Order of the expansion.
        m : class:`int`
            Description of parameter `m`.
        mode : class:`str`
            Mode of the plane wave, either 'TE' or 'TM'.

        Returns
        -------
        class:`float`
            Expansion coefficient.

        """
        if m not in [-1,1]: return 0

        if mode == 'TM': return 1 / 2

        if mode == 'TE': return 1j / 2