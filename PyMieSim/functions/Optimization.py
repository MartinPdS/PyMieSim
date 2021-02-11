from tqdm import tqdm
import numpy as np

import matplotlib.pyplot as plt
from typing import Union
from PyMieSim.classes.Detector import LPmode, Photodiode
from PyMieSim.classes.Scattering import Scatterer




def LoopRIDiameter(RIList:       list,
                   DiameterList: list,
                   Detector:     Union[LPmode, Photodiode],
                   QuietMode:    bool = False,
                   Polarization: str  = 'Parallel',
                   **SKwargs):

    temp = np.empty( [ len(RIList), len(DiameterList) ] )


    for nr, RI in enumerate( tqdm(RIList, total = len(RIList), desc ="Progress", disable = QuietMode) ):
        for nd, Diameter in enumerate(DiameterList):

            Scat = Scatterer(Diameter  = Diameter,
                             Index     = RI,
                             Source    = SKwargs['Source'],
                             Mesh    = Detector.Mesh
                             )

            Coupling = Detector.Coupling(Scatterer = Scat, Polarization = Polarization)

            temp[nr, nd] = Coupling

    return Array(temp)


def PlotRI(Diameter:     float,
           RIList:       list,
           Detector:     Union[LPmode, Photodiode],
           QuietMode:    bool = False,
           Source             = None):

    temp = np.empty( [ len(RIList),1 ] )

    fig = plt.figure(figsize=(7,3))

    ax = fig.add_subplot(1,1,1)

    for nr, RI in enumerate( tqdm( RIList,
                                   total = len(RIList),
                                   desc ="Progress",
                                   disable = QuietMode) ):


        Scat = Scatterer(Diameter    = Diameter,
                         Index       = RI,
                         Source      = Source,
                         ThetaBound  = [-180,180],
                         PhiBound    = [-90,90],
                         Npts        = Detector.Npts,
                         )


        x = Scat.Mesh.Phi.Vector.Degree
        y = np.abs(Scat.S1S2.S1S2[0])**2

        plt.plot(x, y, label="{0:.3f}".format(RI))

    if Detector:
        ymin = ax.get_ylim()[0]
        ymax = ax.get_ylim()[1]*3



        ax.fill_between(Scat.Mesh.Phi.Vector.Degree,
                        ymin,
                        ymax,
                        where= (x > Detector.Mesh.Phi.Boundary.Degree[0]) & (x < Detector.Mesh.Phi.Boundary.Degree[1]) ,
                        label='Detector',
                        color='green',
                        alpha=0.5)
    ax.grid()

    ax.set_xlabel(r'Scattering Angle [degree]')

    ax.set_ylabel(r'Scattered light intensity [a.u]')

    ax.set_yscale('log')

    ax.tick_params(labelsize=8)

    plt.legend()

    plt.show()






def PlotDiameter(DiameterList: float,
                 RI:           list,
                 Detector:     Union[LPmode, Photodiode],
                 QuietMode:    bool = False,
                 Source        = None
                 ):

    temp = np.empty( [ len(DiameterList),1 ] )

    fig = plt.figure(figsize=(7,3))
    ax = fig.add_subplot(1,1,1)
    for nr, Diameter in enumerate( tqdm( DiameterList,
                                         total = len(DiameterList),
                                         desc ="Progress",
                                         disable = QuietMode ) ):


        Scat = Scatterer(Diameter    = Diameter,
                         Index       = RI,
                         Source      = Source,
                         ThetaBound  = [-180,180],
                         PhiBound    = [-180,180],
                         Npts        = Detector.Npts,
                         )


        x = Scat.Mesh.Phi.Vector.Degree
        y = np.abs(Scat.S1S2.S1S2[0])**2

        plt.plot(x, y, label="{0:.1e}".format(Diameter))


    ymin = ax.get_ylim()[0]
    ymax = ax.get_ylim()[1]*3



    ax.fill_between(Scat.Mesh.Phi.Vector.Degree,
                    ymin,
                    ymax,
                    where= (x > Detector.Mesh.Phi.Boundary.Degree[0]) & (x < Detector.Mesh.Phi.Boundary.Degree[1]) ,
                    color='green', alpha=0.5)

    ax.grid()

    ax.set_xlabel(r'Scattering Angle [degree]')

    ax.set_ylabel(r'Scattered light intensity [a.u]')

    ax.set_yscale('log')

    plt.legend()

    plt.show()





# -