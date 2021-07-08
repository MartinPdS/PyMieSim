"""
Photodiode
==========
"""

# sphinx_gallery_thumbnail_path = '../images/Coupling:Photodiode.png'

def run(Plot, Save):
    from PyMieSim.Source   import PlaneWave
    from PyMieSim.Detector import Photodiode


    Source = PlaneWave(Wavelength   = 450e-9,
                       Polarization = 0,
                       E0           = 1)

    Detector = Photodiode(NA                = 0.8,
                         Sampling          = 1001,
                         GammaOffset       = 0,
                         PhiOffset         = 0)

    if Plot:
        Detector.Plot()

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        Detector.SaveFig(dir)

if __name__ == '__main__':
    run(Plot=True, Save=False)
