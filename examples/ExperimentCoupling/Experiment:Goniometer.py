"""
Goniometer
==========
"""

# sphinx_gallery_thumbnail_path = '../images/Experiment:Goniometer.png'

def run(Plot, Save):
    import numpy as np
    from PyMieSim            import Material
    from PyMieSim.Scatterer  import Sphere
    from PyMieSim.Source     import PlaneWave
    from PyMieSim.Detector   import Photodiode
    from PyMieSim.Experiment import ScatSet, SourceSet, Setup, DetectorSet

    scatKwargs   = { 'Diameter'     : 1200e-9,
                     'Material'     : Material('BK7'),
                     'nMedium'      : [1] }

    sourceKwargs = { 'Wavelength'   : 400e-9,
                     'Polarization' : [0]}

    detecKwargs = { 'NA'            : [0.05],
                   'Sampling'       : 300,
                   'GammaOffset'    : 0,
                   'PhiOffset'      : np.linspace(0,180,100),
                   'CouplingMode'   : 'Centered'}

    detecSet   = DetectorSet(Detector = Photodiode, kwargs = detecKwargs)

    scatSet    = ScatSet(Scatterer = Sphere,  kwargs = scatKwargs )

    sourceSet  = SourceSet(Source = PlaneWave, kwargs = sourceKwargs )

    Experiment = Setup(ScattererSet = scatSet,
                       SourceSet    = sourceSet,
                       DetectorSet  = detecSet)

    Data = Experiment.Get(['Coupling'])



    if Plot:
        Data.Plot(y='Coupling', x='PhiOffset')

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        Data.SaveFig(Directory=dir, y='Coupling', x='PhiOffset')

if __name__ == '__main__':
    run(Plot=True, Save=False)
