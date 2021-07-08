"""
SPF
===
"""

# sphinx_gallery_thumbnail_path = '../images/Fields:SPF.png'

def run(Plot, Save):
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source    import PlaneWave

    Source = PlaneWave(Wavelength   = 450e-9,
                      Polarization = 0,
                      E0           = 1)

    Scat = Sphere(Diameter    = 800e-9,
                Source      = Source,
                Index       = 1.4)

    SPF = Scat.SPF(Num=100)

    if Plot:
        SPF.Plot()

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        SPF.SaveFig(Directory=dir)

if __name__ == '__main__':
    run(Plot=True, Save=False)
