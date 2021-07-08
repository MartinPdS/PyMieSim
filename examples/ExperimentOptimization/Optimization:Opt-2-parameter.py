"""
Opt 2 parameter
===============
"""

def run(Plot, Save):
    return
    import numpy as np
    from PyMieSim.Detector  import Photodiode, LPmode
    from PyMieSim.Source    import PlaneWave
    from PyMieSim.Optimizer import Optimize
    from PyMieSim.Sets      import ExperimentalSet, ScattererSet

    Source = PlaneWave(Wavelength   = 450e-9,
                     Polarization = 0,
                     E0           = 1e5)

    Detector0 = Photodiode(NA               = 0.1,
                        Sampling          = 300,
                        GammaOffset       = 20,
                        PhiOffset         = 0,
                        CouplingMode      = 'Centered')

    Detector1 = Photodiode(NA                = 0.1,
                         Sampling          = 300,
                         GammaOffset       = 30,
                         PhiOffset         = 0,
                         CouplingMode      = 'Centered')


    ScatSet = ScattererSet(DiameterList  = np.linspace(100e-9, 1500e-9, 300),
                         IndexList        = np.linspace(1.5, 1.8, 1).round(1),
                         Source        = Source)

    Set = ExperimentalSet(ScattererSet = ScatSet, Detectors = (Detector0))


    Opt    = Optimize(ExperimentalSet = Set,
                    Metric          = 'Monotonic',
                    Parameter       = ['NA','PhiOffset'],
                    MinVal          = [1e-1, None],
                    MaxVal          = [1, None],
                    WhichDetector   = 0,
                    X0              = [0.1,30],
                    MaxIter         = 350,
                    Tol             = 1e-4,
                    FirstStride     = 30)

    print(Opt.Result)

    df = Set.DataFrame
    if Plot:
        df.Plot('Coupling') # can be "Couplimg"  or  "STD"


if __name__ == '__main__':
    run(Plot=True, Save=False)
