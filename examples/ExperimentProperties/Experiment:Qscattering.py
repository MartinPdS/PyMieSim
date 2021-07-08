"""
Qscattering
===========
"""

# sphinx_gallery_thumbnail_path = '../images/Experiment:Qscattering.png'

def run(Plot, Save):
    import numpy as np
    from PyMieSim.Scatterer  import Sphere
    from PyMieSim.Source     import PlaneWave
    from PyMieSim.Detector   import Photodiode
    from PyMieSim.Experiment import ScatSet, SourceSet, Setup, DetectorSet

    scatKwargs   = { 'Diameter' : np.linspace(100e-9, 10000e-9, 400),
                     'Index'    : [1.4, 1.6],
                     'nMedium'  : [1] }

    sourceKwargs = { 'Wavelength'   : [400e-9],
                     'Polarization' : [0]}

    scatSet    = ScatSet(Scatterer = Sphere,  kwargs = scatKwargs )

    sourceSet  = SourceSet(Source = PlaneWave, kwargs = sourceKwargs )

    Experiment = Setup(ScattererSet = scatSet,
                       SourceSet    = sourceSet,
                       DetectorSet  = None)

    Data = Experiment.Get('Qsca')

    if Plot:
        Data.Plot(y='Qsca', x='Diameter')

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        Data.SaveFig(Directory=dir, y='Qsca', x='Diameter')

if __name__ == '__main__':
    run(Plot=True, Save=False)
