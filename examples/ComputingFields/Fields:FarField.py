"""
Far Field
=========
"""

# sphinx_gallery_thumbnail_path = '../images/Fields:FarField.png'

def run(Plot, Save):
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source   import PlaneWave


    Source = PlaneWave(Wavelength   = 450e-9,
                      Polarization = 0,
                      E0           = 1)

    Scat = Sphere(Diameter    = 300e-9,
                 Source      = Source,
                 Index       = 1.4)


    Fields = Scat.FarField(Num=100)

    if Plot:
        Fields.Plot()

    if Save:
        from pathlib import Path
        dir = f'docs/images/{Path(__file__).stem}'
        Fields.SaveFig(Directory=dir)


if __name__ == '__main__':
    run(Plot=True, Save=False)
