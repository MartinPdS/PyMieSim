from PyMieSim.Source import PlaneWave
from PyMieSim.Detector import Photodiode
from PyMieSim.Scatterer import Sphere

Source = PlaneWave(Wavelength   = 450e-9,
                  Polarization = 0,
                  E0           = 1)

Detector = Photodiode(Sampling     = 201,
                     NA           = 0.2,
                     GammaOffset  = 0,
                     PhiOffset    = 0,
                     CouplingMode = 'Centered')


Scat = Sphere(Diameter    = 300e-9,
             Source      = Source,
             Index       = 1.4)

Coupling = Detector.Coupling(Scatterer = Scat)

print(Coupling)
