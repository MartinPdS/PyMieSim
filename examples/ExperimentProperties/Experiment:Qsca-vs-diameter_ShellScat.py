"""
Qsca vs Diameter Shell Scat
===========================
"""

def run(Plot, Save):
    import numpy as np
    from PyMieSim            import Material
    from PyMieSim.Scatterer  import ShellSphere
    from PyMieSim.Source     import PlaneWave
    from PyMieSim.Detector   import Photodiode
    from PyMieSim.Experiment import ScatSet, SourceSet, Setup, DetectorSet

    scatKwargs   = { 'CoreDiameter'     : np.geomspace(10e-09, 600e-9, 500),
                     'ShellWidth'       : [200e-9, 400e-9],
                     'CoreIndex'        : [1],
                     'ShellIndex'       : [1.3],
                     'nMedium'          : 1 }

    sourceKwargs = { 'Wavelength'   : [200e-9],
                     'Polarization' : [0]}

    scatSet   = ScatSet(Scatterer = ShellSphere,  kwargs = scatKwargs )

    sourceSet = SourceSet(Source = PlaneWave, kwargs = sourceKwargs )

    Experiment = Setup(ScattererSet = scatSet,
                       SourceSet    = sourceSet)

    Data = Experiment.Get(Input=['Qsca', 'Qback'])

    print(Data)

    if Plot:
        Data.Plot(y=['Qsca'], x='Core diameter', Scale='lin')

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        Data.SaveFig(Directory=dir, y=['Qsca'], x='Core diameter', Scale='lin')

if __name__ == '__main__':
    run(Plot=True, Save=False)




#___________________________OUTPUT___________________________________
#
# PyMieArray
# Variable: ['qsca', 'qback']
# ==========================================================================================
# Parameter
# ------------------------------------------------------------------------------------------
# wavelength                           | dimension =  0                        | size =  1
# polarization                         | dimension =  1                        | size =  1
# corediameter                         | dimension =  2                        | size = 500
# shellwidth                           | dimension =  3                        | size =  2
# coreindex                            | dimension =  4                        | size =  1
# shellindex                           | dimension =  5                        | size =  1
# nmedium                              | dimension =  6                        | size =  1
# ==========================================================================================
