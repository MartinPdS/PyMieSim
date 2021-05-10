def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source    import PlaneWave

    Source = PlaneWave(Wavelength   = 450e-9,
                       Polarization = 0,
                       E0           = 1)

    Scat = Sphere(Diameter      = 800e-9,
                  Source        = Source,
                  Index         = 1.4,
                  Concentration = 0.1 ) # #.m⁻³

    print(Scat.Properties)


if __name__ == '__main__':
    run()

#___________________________OUTPUT___________________________________
#
#         Object:          Dictionary
#         Keys:            Efficiencies, cross-sections, others
#         Structured data: Yes
#         Method:          <Plot>
#         Shape:           [7, 1]
#         ========================================
# ----------------------------------------------------------------------
# Efficiencies   | Qsca             | 4.029799032677242
# ----------------------------------------------------------------------
#                | Qext             | 4.029799032677242
# ----------------------------------------------------------------------
#                | Qabs             | 0.0
# ----------------------------------------------------------------------
#                | Qback            | 4.973830378796597
# ----------------------------------------------------------------------
#                | Qratio           | 1.2342626365395144
# ----------------------------------------------------------------------
#                | Qpr              | 0.7925897259835781
# ----------------------------------------------------------------------
# cross-sections | Csca             | 2.025597925840332e-12 m²  (2.03e+00 μm²)
# ----------------------------------------------------------------------
#                | Cext             | 2.025597925840332e-12 m²  (2.03e+00 μm²)
# ----------------------------------------------------------------------
#                | Cabs             | 0 m²
# ----------------------------------------------------------------------
#                | Cback            | 2.5001198365166603e-12 m²  (2.50e+00 μm²)
# ----------------------------------------------------------------------
#                | Cratio           | 6.204080690484652e-13 m²  (6.20e+05 nm²)
# ----------------------------------------------------------------------
#                | Cpr              | 3.98399049673721e-13 m²  (3.98e+05 nm²)
# ----------------------------------------------------------------------
# others         | area             | 5.026548245743668e-13 m²  (5.03e+05 nm²)
# ----------------------------------------------------------------------
#                | index            | 1.4
# ----------------------------------------------------------------------
#                | concentration    | 0.1
# ----------------------------------------------------------------------
#                | μ sca            | 2.0255979258403322e-13 m⁻¹  (2.03e-01 Tm⁻¹)
# ----------------------------------------------------------------------
#                | μ ext            | 2.0255979258403322e-13 m⁻¹  (2.03e-01 Tm⁻¹)
# ----------------------------------------------------------------------
#                | μ abs            | 0 m²
# ----------------------------------------------------------------------
#                | g                | 0.7925897259835781
# ----------------------------------------------------------------------