from matplotlib import pyplot as plt
from .plotfunc import plot_quiver, plot_textbox, plot_aux_line, add_point, nplot
from abc import ABC, abstractmethod
from functools import partial
from math import cos, sin, pi
from typing import Iterable, Callable
import numpy as np

plt.ioff() # to prevent figure window from showing until plt.show() is called.

# Concept
# Specielle plots from RXplot, PhasorPlot og PolarPlot arver fra ComplexPlot
# De deler en masse metoder til at plotte med.
# Alle special plot definere deres standard layout
# Ønsker man at overwrite eller added ved at bruge axis, så er der lavet en
# axis til at opsamle alle metode cal til plt.Axes.
# E.g. myplot.axes.set_xlim([-1, 5]) bliver gemt i FakeAx og bliver derefter
# først kaldt når ComplexPlot.Show() kaldes.

class FakeAx:
    def __init__(self, axes):
        self.actions = []
        self.axes = axes
        
    def __getattr__(self, name):
        def method(*args, **kwargs):
            try:
                getattr(self.axes, name)
            except:
                print(f'Method *{name}* do not exist in matplotlib.Axes')
                return method
            func = partial(getattr(self.axes, name), *args, **kwargs)
            self.actions.append(func)
        return method
    
    def overwrite(self):
        for action in self.actions:
            action()
        
class CombineFigure():
    
    def __init__(self, nrows : int, ncols : int, figsize : tuple = (8, 8)):
        """
        Constructs all the necessary attributes for the CombineFigure object.

        Parameters
        ----------
        nrows : int
            Number of rows.
        ncols : int
            Number of columns.
        figsize : tuple, optional
            Figure size of the matplotlib.pylot figure. The default is (8, 8).

        Returns
        -------
        None.

        """
        self.nrows = nrows
        self.ncols = ncols
        self.figsize = figsize
        self.fig = plt.figure(figsize=self.figsize, layout="constrained")
        self.axes = []
        self.i = 0
        
    def add_axis(self, projection = None):
        self.i += 1
        ax = self.fig.add_subplot(self.nrows, self.ncols, self.i, projection=projection)
        self.axes.append(ax)
        return ax
        
    def _maximize_window(self):
        """
        Method to maximize the figure. 

        Returns
        -------
        None.

        """
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
    
    def show(self, maximize : bool = False):
        '''
        Method to show the stored plot. 

        Parameters
        ----------
        maximize : bool, optional
            Option to maximize the plot window. The default is False.

        Returns
        -------
        None.

        '''
        if maximize:
            self._maximize_window()
        plt.show()

class ComplexPlot(ABC):    
    """
    A class to represent a plot using complex numbers.
    This class utilize the matplotlib.pyplot module for plotting.
    
    ...
    
    Attributes
    ----------
    title : str
        Title of the plot. 
    projection : str | None
        Parameter for the matplotlib.pyplot.figure.add_subplot function
    coordinates : list
        List of coordinates to be considered for setting the x and y limits of
        the plot.
    axes : plt.Axes
        List of coordinates to be considered for setting the x and y limits of
        the plot.
    
    
    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    """
    def __init__(self, title : str, axes : plt.Axes = None, projection : str = None):
        """
        Constructs all the necessary attributes for the abstract class
        ComplexPlot object.

        Parameters
        ----------
        title : str
            Title of the plot.
        axes : plt.Axes
            Axes object to be used for the plotting in case the figure is
            created elsewhere. If no axes is given the class creates it own
            figures and axes. The default is None.
        projection : str, optional
            Parameter for the matplotlib.pyplot.figure.add_subplot function.
            Options: {None, 'aitoff', 'hammer', 'lambert', 'mollweide',
             'polar', 'rectilinear', str}
            The default is None resulting in a rectilinear projection.

        Returns
        -------
        None.

        """
        self.title = title
        self.projection = projection
        self.coordinates = []

        if axes:
            self._axes = axes
        else:
            self.fig = plt.figure(figsize=(8,8))
            self._axes = self.fig.add_subplot(111, projection=self.projection)
            self._axes.set_title(self.title)
            self.axes = FakeAx(self._axes)
    
    ##########################################################################
    # plot functionalities
    ##########################################################################
    
    def add_phasor(self, value : complex, ref : tuple = (0,0), name : str = "", color : str = None, polar : bool = False, **kwargs):
        '''
        This functions adds a phasor to the plot (axes object). 

        Parameters
        ----------
        value : complex
            Value of the phasor with respect to (0,0). If you wish to simple 
            move with respect to ref = (1,1), you need to add 1+1j to value.
        ref : tuple, optional
            Tuple with coordinates for the beginning of of the phasos.
            The default is (0,0).
        name : str, optional
            Name of the phasor. This will be plotted on as a textbox close to 
            the phasor. The default is "".
        color : str, optional
            Select the color of the phasor. The default is None.
        polar : bool, optional
            Option for plotting on a axes with polar projection.
            The default is False, which is equial to a cartesian axes.
        **kwargs : N/A
            Additional arguements can be added for the underlaying axes.quiver
            object.

        Returns
        -------
        None.

        '''
        plot_quiver(axes = self._axes,
                    phasor = value,
                    ref = ref,
                    color = color,
                    text = name,
                    polar = polar,
                    alpha = 0.7,
                    **kwargs)
        
        self.coordinates.append((value.real, value.imag))
        
    def add_textbox(self, x : float, y : float, s : str, box : dict = {}, **kwargs):
        '''
        Method for plotting a textbox.

        Parameters
        ----------
        x : float
            x-coordinate for the postion.
        y : float
            y-coordinate for the postion.
        s : str
            Text for the textbox.
        box : dict, optional
            Added a box around the text box. The default is {}.
            Specfic any argument to add the box e.g. {'color' : 'red'}.
        **kwargs : TYPE
            Additional arguements can be added for the underlaying axes.text
            object.

        Returns
        -------
        None.

        '''
        plot_textbox(self._axes,
                     x = x,
                     y = y,
                     s = s,
                     box = box,
                     **kwargs)
 
        self.coordinates.append((x, y))
        
    def add_point(self, value : complex|tuple, **kwargs):
        '''
        Method to add a point to the plot.

        Parameters
        ----------
        value : complex|tuple
            x and y coordinate for the point specified either a coordinate
            (x,y) or a complex number x+jy.
        **kwargs : TYPE
            Additional arguements can be added for the underlaying axes.plot
            object.

        Returns
        -------
        None.

        '''
        add_point(self._axes, 
                  value = value,
                  **kwargs)
        
        self.coordinates.append((value.real, value.imag))
    
    def add_line(self, arange : Iterable, afunc : Callable, **kwargs):
        '''
        Method to add a line to the plot based on a range and function. 

        Parameters
        ----------
        arange : Iterable
            A range of values for the x-axis.
        afunc : Callable
            A function to be called afunc(x).
        **kwargs : N/A
            Additional arguements can be added for the underlaying axes.plot
            object.

        Returns
        -------
        None.

        '''
        x = arange
        y = list(map(afunc, arange))
        nplot(self._axes,
              x = x,
              y = y,
              **kwargs)

        for p in zip(x, y):
            self.coordinates.append(p)
       
    def add_limit(self, magnitude, angle, x0 = 0, y0 = 0, text = '', deg = True, polar = False):
        plot_aux_line(self._axes,
                      x0 = x0,
                      y0 = y0,
                      magnitude = magnitude,
                      angle = angle,
                      text = text,
                      deg = deg,
                      polar = polar)
        
        self.coordinates.append((x0, y0))
        x1 = x0 + magnitude * cos(angle / 180 * pi)
        y1 = x0 + magnitude * sin(angle / 180 * pi)
        self.coordinates.append((x1, y1))
    
    def add_plot(self, x : float, y : float, **kwargs):
        nplot(self._axes,
              x = x,
              y = y,
              **kwargs)
        
        for p in zip(x, y):
            self.coordinates.append(p)

    def add_angle(self):
        raise NotImplementedError("Subclasses must implement this method")
                       
    def add_impedance_trace(self, imp: Iterable[complex], start : complex = 0+0j, **kwargs):
        '''
        Method for adding an trace of impedance to the plot. The method is
        intended for plotting the combined posistive sequence of multiple
        cable/line sections in a radial topology.

        Parameters
        ----------
        imp : Iterable[complex]
            A Iterable (e.g. list or tuple) of complex numbers to be plotted.
        start : complex, optional
            Start of the trace. The default is 0+0j.
        **kwargs : N/A
            Additional arguements can be added for the underlaying axes.plot
            object.

        Raises
        ------
        ValueError
            The variable imp has to be either iterable[complex] or a complex number.

        Returns
        -------
        None.

        '''
        
        if isinstance(imp, complex):
            impedances = np.cumsum([start, imp])
        elif all(isinstance(d, complex) for d in imp):
            impedances = np.cumsum([start, *imp])
        else:
            raise ValueError('The variable imp has to be either iterable[complex] or a complex number')
            
        real = [x.real for x in impedances]
        imag = [x.imag for x in impedances]
        
        kwargs.setdefault('color', 'black')
        kwargs.setdefault('linestyle', 'dashed')
        kwargs.setdefault('label', 'impedance trace 1')
        
        self.add_plot(real, imag, **kwargs)
    
    
    def _get_rmax(self):
        '''
        Method to return 110% of the maximum x and y values use for the plot.
        This value can be used to set the x and y plot limit for the plot
        automatically.

        Returns
        -------
        float
            Maximum x/y value used in the plot times 110%. 

        '''
        xmax = max(map(abs, [x for x, y in self.coordinates]))
        ymax = max(map(abs, [y for x, y in self.coordinates]))
        
        return max(xmax, ymax) * 1.1
    
    def show(self):
        '''
        Method to show the plot.

        Returns
        -------
        None.

        '''
        self.layout(self._axes)
        self.axes.overwrite()
        plt.show()

     
    ##########################################################################
    @abstractmethod
    def layout(self):
        pass


def get_centroid(A : complex, B : complex, C : complex):
    x = (A.real + B.real + C.real)/3
    y = (A.imag + B.imag + C.imag)/3
    return complex(x,y)

def phase_to_line(xA : complex, xB : complex, xC : complex):
    xAL = xA - xB
    xBL = xB - xC
    xCL = xC - xA
    return xAL, xBL, xCL

def line_to_phase(xAL : complex, xBL : complex, xCL : complex):
    xA = - (1/3) * xBL - (2/3) * xCL
    xB = (2/3) * xBL + (1/3) * xCL
    xC = - (1/3) * xBL + (1/3) * xCL
    return xA, xB, xC
    

class PlotPolar(ComplexPlot):
    '''A class for creating a phasor plot using a polar projection.'''
    
    def __init__(self, title : str, axes : plt.Axes = None):
        super().__init__(title = title, axes = axes, projection = 'polar')
    
    def add_phasor(self, value : complex, ref : tuple = (0,0), name : str = "", color : str = None, polar : bool = False, **kwargs):
        plot_quiver(axes = self._axes,
                    phasor = value,
                    ref = ref,
                    color = color,
                    text = name,
                    polar = polar,
                    alpha = 0.7,
                    **kwargs)   
        self.coordinates.append((value.real, value.imag))
    
    def layout(self, axes):
        axes.set_rlabel_position(90) 
        axes.set_rlim(0, self._get_rmax() + 0.5)


class PlotPhasor(ComplexPlot):    
    '''
    A class for creating a phasor plot using a cartesian projection.
    The plot will have a centered x and y axis.
    '''
    
    def __init__(self, title : str, axes : plt.Axes = None):
        super().__init__(title = title, axes = axes)
    
    def layout(self, axes : plt.Axes):
        #axes.axis('equal')
        
        axes.set_xlim([- self._get_rmax(), self._get_rmax()])
        axes.set_ylim([- self._get_rmax(), self._get_rmax()])

        axes.set_aspect('equal', 'box')
   
        axes.grid(color='lightgrey', linestyle='-')
        
        
        axes.spines['left'].set_position('zero')
        axes.spines['bottom'].set_position('zero')
        
        #ax = ax_dict['center']

        axes.spines[['left', 'bottom']].set_position('zero')
        axes.spines[['top', 'right']].set_visible(False)
        
        
        axes.set_xlabel('Re', fontweight='bold')
        axes.set_ylabel('Im', fontweight='bold', rotation = 0)
        
        axes.spines['left'].set_linewidth(1)
        axes.spines['left'].set_color('black')
        axes.spines['left'].set_alpha(0.8)
        axes.spines['bottom'].set_linewidth(1)
        axes.spines['bottom'].set_color('black')
        axes.spines['bottom'].set_alpha(0.8)
        
        # Remove dublicate zero in the ticks
        locs, labels = plt.yticks() # get current ticks
        locs = [n for n in locs if n != 0.0] # remove 0.0
        axes.set_yticks(locs)
        
        # Put axis label outside the plot
        axes.xaxis.set_label_coords(0.5, -0.05)
        axes.yaxis.set_label_coords(-0.05, 0.5)
        
        # Alternative to centered axis
        #axes.axhline(linewidth = 1, color ="black", linestyle ="--")
        #axes.axvline(linewidth = 1, color ="black", linestyle ="--")


class RXplot(ComplexPlot):
    '''A class for creating a complex plot.'''
    
    def __init__(self, title : str):
        super().__init__(title)
    
    def layout(self, axes : plt.Axes):
        
        axes.set_xlim([- self._get_rmax(), self._get_rmax()])
        axes.set_ylim([- self._get_rmax(), self._get_rmax()])
        
        axes.set_xlabel(r'R [$\Omega$]')
        axes.set_ylabel(r'X [$\Omega$]')
        axes.grid(True)

'''
#Creating a new special plot

class myspecialplot(ComplexPlot):
    def __init__(self, title : str):
        super().__init__(title)
    
    def layout(self, axes : plt.Axes):
        # define layout for the plot
        axes.set_xlabel(r'R [$\Omega$]')
        axes.set_ylabel(r'X [$\Omega$]')

# View the methods that are inherited:
help(myspecialplot)

aplot = myspecialplot('mytitle')
aplot.add_phasor(value=1+1j, color='Blue', name='VA')
aplot.show()
'''


# testing
'''
from psp import P2R

myplot1 = PlotPolar(title = 'Polar plot')
myplot1.add_phasor(value=P2R(1, 180), color='Blue', name='V1')
myplot1.add_phasor(value=P2R(1, 30), color='Red', name='I1')
myplot1.add_limit(1, 85, text='test', polar = True)

myplot1.add_textbox(0.5, 0.5, 'Test')
myplot1.show()

myplot2 = PlotPhasor(title = 'Phasor plot')
myplot2.add_phasor(value=P2R(4, 45), color='Blue', name='V1', polar=False)
myplot2.add_phasor(value=P2R(6, 30), color='Red', name='I1',  polar=False)

myplot2.axes.set_xlabel('hejdff')

#myplot2.axes.set_xlim([-1, 6])
#myplot2.set_limits([-1, 10, -1, 10])
#myplot2.add_phasor(value=P2R(6, 180), color='Red', name='I1',  polar=False)
#myplot2.add_point(value=P2R(10, 30), color='Red', label='I1')
#myplot2.add_line(range(4), lambda x : x*2)
#myplot2.add_angle(radius=1, centX=0, centY=0, startangle=10, angle=230, text = '$\Theta$')
#myplot2.add_limit(8, 85, text='test', polar = False)
myplot2.show()


myplot3 = RXplot('test')
myplot3.add_impedance_trace([0+0j, 1+1j, 2+3j])
myplot3.add_textbox(1, 1, 'array', box={'color':'red'})
myplot3.show()


'''
# Good source for fft
# https://pysdr.org/content/frequency_domain.html

# style exmaples:
# C:\Users\ASGRM\Anaconda3\envs\py10\Lib\site-packages\matplotlib\mpl-data\stylelib
# https://github.com/jeremyworsfold/mplstyles/blob/main/mplstyles/notebook.mplstyle
# https://matplotlib.org/stable/users/explain/customizing.html

