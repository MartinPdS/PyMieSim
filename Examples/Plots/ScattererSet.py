
"""
_________________________________________________________
Optimization of RI dependence minimizing STD of detector response.
_________________________________________________________
"""

import numpy as np
import matplotlib.pyplot as plt
from PyMieCoupling.classes.Detector import fiber, LPmode, Photodiode
from PyMieCoupling.classes.Fields import Source
from PyMieCoupling.classes.Scattering import ScattererSet

LightSource = Source(Wavelength   = 450e-9,
                     Polarization = 0)

Detector = Photodiode(NA                = 0.5,
                      Source            = LightSource,
                      Npts              = 101,
                      ThetaOffset       = 0,
                      PhiOffset         = -15,
                      Filter            = 90)



Set = ScattererSet(DiameterList  = np.linspace(100e-9, 1000e-9, 400),
                   RIList        = np.linspace(1.3, 1.6, 4).round(1),
                   Detector      = Detector,
                   Source        = LightSource
                   )



#Set.Plot(part='STD::S1')  # can be  S1  -  STD::S1  -  S2  -  STD::S2

DF = Set.GetFrame(Polarization=['NoFiltered', 'Filtered'])

DF.Plot(y='Coupling')

DF.Plot(y='STD')


plt.show()

# -