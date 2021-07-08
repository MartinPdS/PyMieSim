"""
Mean Qsca vs Diameter
=====================
"""

def run(Plot, Save):
    import numpy as np
    from PyMieSim            import Material
    from PyMieSim.Scatterer  import Sphere
    from PyMieSim.Source     import PlaneWave
    from PyMieSim.Detector   import Photodiode
    from PyMieSim.Experiment import ScatSet, SourceSet, Setup, DetectorSet

    scatKwargs   = { 'Diameter' : np.geomspace(6.36e-09, 10000e-9, 500),
                     'Material' : [Material('Silver')],
                     'nMedium'  : [1] }

    sourceKwargs = { 'Wavelength'   : [400e-9, 900e-9, 1200e-9, 1600e-9],
                     'Polarization' : [0]}

    scatSet   = ScatSet(Scatterer = Sphere,  kwargs = scatKwargs )

    sourceSet = SourceSet(Source = PlaneWave, kwargs = sourceKwargs )

    Experiment = Setup(ScattererSet = scatSet,
                       SourceSet    = sourceSet)

    Data = Experiment.Get(Input=['Qsca', 'Qabs'])

    MeanData = Data.Mean('wavelength')

    print(MeanData)

    if Plot:
        Data.Plot(y='Qabs', x='diameter', Scale='log')

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        Data.SaveFig(Directory=dir, y='Qabs', x='diameter', Scale='log')

if __name__ == '__main__':
    run(Plot=True, Save=False)


#___________________________OUTPUT___________________________________
#
# PyMieArray
# Variable: ['qsca', 'qabs']
# ========================================================================================================================
# Parameter
# ------------------------------------------------------------------------------------------------------------------------
# Polarization [Degree]                                 | dimension = 0                        | size      = 1
# Diameter [m]                                          | dimension = 1                        | size      = 500
# Material refractive index [1]                         | dimension = 2                        | size      = 1
# Medium refractive index [1]                           | dimension = 3                        | size      = 1
# ========================================================================================================================
