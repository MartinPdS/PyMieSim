"""
Qsca vs Diameter
================
"""

# sphinx_gallery_thumbnail_path = '../images/Experiment:Qsca-vs-diameter.png'

def run(Plot, Save):
    import numpy as np
    from PyMieSim            import Material
    from PyMieSim.Scatterer  import Sphere
    from PyMieSim.Source     import PlaneWave
    from PyMieSim.Detector   import Photodiode
    from PyMieSim.Experiment import ScatSet, SourceSet, Setup, DetectorSet

    scatKwargs   = { 'Diameter' : np.geomspace(6.36e-09, 10000e-9, 100),
                     'Material' : [Material('Silver')],
                     'nMedium'  : [1] }

    sourceKwargs = { 'Wavelength'   : [400e-9],
                     'Polarization' : [0]}

    scatSet   = ScatSet(Scatterer = Sphere,  kwargs = scatKwargs )

    sourceSet = SourceSet(Source = PlaneWave, kwargs = sourceKwargs )

    Experiment = Setup(ScattererSet = scatSet,
                       SourceSet    = sourceSet)

    Data = Experiment.Get(Input=['Qsca', 'Qabs'])

    print(Data)

    if Plot:
        Data.Plot(y=['Qsca', 'Qabs'], x='diameter', Scale='log')

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        Data.SaveFig(Directory=dir, y=['Qsca', 'Qabs'], x='diameter', Scale='log')


if __name__ == '__main__':
    run(Plot=True, Save=False)
