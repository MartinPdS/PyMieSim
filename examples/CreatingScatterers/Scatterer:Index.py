"""
Index
=====
"""

def run(Plot, Save):
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source    import PlaneWave
    from PyMieSim           import Material

    Source = PlaneWave(Wavelength    = 450e-9,
                      Polarization   = 0,
                      E0             = 1)

    Scat = Sphere(Diameter     = 800e-9,
                  Source       = Source,
                  Index        = 1.445)


if __name__ == '__main__':
    run(Plot=False, Save=False)
