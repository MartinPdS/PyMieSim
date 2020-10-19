
"""
_________________________________________________________
Scattering Parallel Field coupling with en-face LP01 and LP11 Mode
For different scatterer diameters.
_________________________________________________________
"""



import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar

from miecoupling.src.classes.Fiber import fiber
from miecoupling.src.classes.Modes import mode
from miecoupling.src.classes.Scattering import Scatterer
from miecoupling.src.functions.couplings import PointFieldCoupling

npts=101

Fiber = fiber(core_radius = 4.2e-6,
              core_index  = 1.4456,
              clad_radius = 20.5e-6,
              clad_index  = 1.4444)

LP11 = mode(fiber      = Fiber,
            LPmode     = (2, 1),
            wavelength = 400e-9,
            npts       = npts,
            )

LP01 = mode(fiber       = Fiber,
            LPmode      = (1, 1),
            wavelength  = 400e-9,
            npts        = npts,
            )


LP01.magnificate(magnification=2.)

LP11.magnificate(magnification=2.)

DiameterList = np.linspace(100,9000,2) * 1e-9

CouplingLP01, CouplingLP11 = [], []

with Bar('Processing...', max = len(DiameterList)) as bar:
    for Diameter in DiameterList:

        Scat = Scatterer(diameter    = Diameter,
                         wavelength  = 400e-9,
                         index       = 1.4,
                         npts        = 101,
                         ThetaBound  = [-20,20],
                         ThetaOffset = 0,
                         PhiBound    = [-20,20],
                         PhiOffset   = 10)

        CouplingLP01.append( PointFieldCoupling(Detector = LP01,
                                                Source   = Scat.Field.Parallel,
                                                Mesh     = Scat.Meshes) )

        CouplingLP11.append( PointFieldCoupling(Detector = LP11,
                                                Source   = Scat.Field.Parallel,
                                                Mesh     = Scat.Meshes) )
        bar.next()



fig = plt.figure(figsize=(15,5))
ax0 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)

ax0.plot(DiameterList*1e6, CouplingLP01, 'C0', label=r'LP$_{01}$')
ax0.plot(DiameterList*1e6, CouplingLP11, 'C1', label=r'LP$_{11+}$')
ax0.set_title('Mode coupling vs. Scatterer diameter')
ax0.legend()
ax0.set_xlabel(r'Scatterer diameter [$\mu m$]')
ax0.set_ylabel('Modal Coupling')
ax0.set_yscale('log')
ax0.grid()

ax1.plot(DiameterList*1e6, np.array(CouplingLP11)/np.array(CouplingLP01))
ax1.set_title('Coupling ratio')
ax1.set_yscale('log')
ax1.grid()



plt.show()










# -