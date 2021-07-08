"""
Coupling vs Diameter
====================
"""

# sphinx_gallery_thumbnail_path = '../images/Experiment:Coupling-vs-diameter.png'

def run(Plot, Save):
    import numpy as np
    from PyMieSim            import Material
    from PyMieSim.Scatterer  import Sphere
    from PyMieSim.Source     import PlaneWave
    from PyMieSim.Detector   import Photodiode
    from PyMieSim.Experiment import ScatSet, SourceSet, Setup, DetectorSet

    scatKwargs   = { 'Diameter'    : np.linspace(400e-9, 2000e-9, 200),
                     'Material'    : Material('BK7'),
                     'nMedium'     : [1] }

    sourceKwargs = { 'Wavelength'   : 1e-6,
                     'Polarization' : [0,30,60,90]}

    detecKwargs  = { 'NA'           : 0.2,
                     'Sampling'     : 300,
                     'GammaOffset'  : 70,
                     'PhiOffset'    : [0],
                     'CouplingMode' : 'Centered'}


    detecSet   = DetectorSet(Detector = Photodiode, kwargs = detecKwargs)

    scatSet    = ScatSet(Scatterer = Sphere,  kwargs = scatKwargs )

    sourceSet  = SourceSet(Source = PlaneWave, kwargs = sourceKwargs )

    Experiment = Setup(ScattererSet = scatSet,
                       SourceSet    = sourceSet,
                       DetectorSet  = detecSet)

    Data = Experiment.Get('Coupling')

    if Plot:
        Data.Plot(y='Coupling', x='Diameter')

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        Data.SaveFig(Directory=dir, y='Coupling', x='Diameter')


if __name__ == '__main__':
    run(Plot=True, Save=False)
