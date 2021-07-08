"""
LP Mode
=======
"""

# sphinx_gallery_thumbnail_path = '../images/Coupling:LPMode.png'

def run(Plot, Save):
    from PyMieSim.Source   import PlaneWave
    from PyMieSim.Detector import LPmode


    Source = PlaneWave(Wavelength   = 450e-9,
                      Polarization = 0,
                      E0           = 0)

    Detector = LPmode(Mode         = (1, 1),
                     Rotation     = 0.,
                     Sampling     = 201,
                     NA           = 0.4,
                     GammaOffset  = 0,
                     PhiOffset    = 40,
                     CouplingMode = 'Centered')

    if Plot:
        Detector.Plot()

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        Detector.SaveFig(dir)

if __name__ == '__main__':
    run(Plot=True, Save=False)
