"""
Material
========
"""

def run(Plot, Save):
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source    import PlaneWave
    from PyMieSim           import Material

    Source = PlaneWave(Wavelength   = 450e-9,
                       Polarization = 0,
                       E0           = 1)

    Scat = Sphere(Diameter    = 300e-9,
                  Source       = Source,
                  Material     = Material('BK7'))


    # Material can be 'FusedSilica'
    #                 'Aluminium'
    #                 'Silver'
    #                 'SodaLimeGlass'
    # More information in Material section of documentation


if __name__ == '__main__':
    run(Plot=False, Save=False)
