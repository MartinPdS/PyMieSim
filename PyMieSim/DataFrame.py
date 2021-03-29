import pandas as pd
import matplotlib.pyplot as plt
#plt.rcParams["font.family"] = "serif"
#plt.rcParams["mathtext.fontset"] = "dejavuserif"



class ExperimentalDataFrame(pd.DataFrame):

    def __init__(self,**kwargs):
        pd.DataFrame.__init__(self, **kwargs)
        self.ax = None

    @property
    def Parallel(self):
        return self.xs('Parallel')

    @property
    def Perpendicular(self):
        return self.xs('Perpendicular')


    def Plot(self, y='Coupling', **kwargs):

        fig = self.unstack(level=[-3,-1]).plot(y       = y,
                                              grid    = True,
                                              figsize = (8,4),
                                              xlabel  = r'Scatterer diameter [m]',
                                              ylabel  = r'Coupling [u.a.]',
                                              **kwargs)

        fig.legend(prop={'size': 8})

        return fig


    def Show(self,*args,**kwargs):
        return plt.show(*args, **kwargs)


class S1S2DataFrame(pd.DataFrame):

    def __init__(self,**kwargs):
        pd.DataFrame.__init__(self,**kwargs)
        self.ax = None

    @property
    def Parallel(self):
        return self.xs('Parallel')

    @property
    def Perpendicular(self):
        return self.xs('Perpendicular')


    def Plot(self, **kwargs):

        fig = self.unstack(level=[0,1]).plot(y       = 'S1',
                                            grid    = True,
                                            figsize = (8,4),
                                            xlabel  = r'$\phi$ angle [degree]',
                                            ylabel  = r'$|S1|$',
                                            **kwargs)

        fig1 = self.unstack(level=[0,1]).plot(y       = 'S2',
                                             grid    = True,
                                             figsize = (8,4),
                                             xlabel  = r'$\phi$ angle [degree]',
                                             ylabel  = r'$|S2|$',
                                             **kwargs)

        fig.legend(prop={'size': 8})

        fig1.legend(prop={'size': 8})

        return(fig, fig1)


    def Show(self,*args,**kwargs):
        return plt.show(*args, **kwargs)


class QscaDataFrame(pd.DataFrame):

    def __init__(self,**kwargs):
        pd.DataFrame.__init__(self,**kwargs)
        self.ax = None

    @property
    def Parallel(self):
        return self.xs('Parallel')

    @property
    def Perpendicular(self):
        return self.xs('Perpendicular')


    def Plot(self, **kwargs):

        fig = self.unstack(level=[1]).plot(y       = 'Qsca',
                                          grid    = True,
                                          figsize = (8,4),
                                          xlabel  = r'Scatterer diameter [m]',
                                          ylabel  = r'Q$_{Scattering}$',
                                          **kwargs)

        fig.legend(prop={'size': 8})

        return fig


    def Show(self,*args,**kwargs):
        return plt.show(*args, **kwargs)
















# -
