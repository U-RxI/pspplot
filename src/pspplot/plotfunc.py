from cmath import cos, sin
from math import atan2, radians
import matplotlib.pyplot as plt
import numpy as np


# Styling
ALPHA_BASE = 0.5 # For quiver
TEXT_FONTSIZE = 10

def nplot(axes : plt.Axes, x : float, y : float, **kvargs):
    #Normal plot
    p = axes.plot(x, y, **kvargs)
    return p

def plot_textbox(axes : plt.Axes, x : float, y : float, s : str, box : dict = {}, **kwargs):
    textbox = axes.text(x, y, s, fontsize = TEXT_FONTSIZE, alpha = 1, **kwargs)
    if box:
        textbox.set_bbox(box)
    return textbox
    
def plot_quiver(axes : plt.Axes, phasor : complex, ref : tuple, color : str, text : str, dx : float = 0, dy : float = 0, polar : bool = True, **kwargs):
    if polar:
        u = atan2(phasor.imag,phasor.real)
        v = abs(phasor)
        coor = [ref[0], ref[1], u, v]
    else:
        coor = [ref[0], ref[1], phasor.real, phasor.imag]
    
    quiver = axes.quiver(*coor,
                         color = color,
                         angles='xy',
                         scale_units = 'xy',
                         scale = 1,
                         **kwargs)
    if text:
        plot_textbox(axes = axes,
                     x = quiver.U + dx,
                     y = quiver.V + dy,
                     s = text)
    return quiver 

# def plot_quiver(axes : plt.Axes, phasor : complex, color : str, text : str, dx : float = 0, dy : float = 0, polar : bool = True, **kwargs):
#     if polar:
#         u = atan2(phasor.imag,phasor.real)
#         v = abs(phasor)
#         coor = [0, 0, u, v]
#     else:
#         coor = [0, 0, phasor.real, phasor.imag]
    
#     quiver = axes.quiver(*coor,
#                          color = color,
#                          angles='xy',
#                          scale_units = 'xy',
#                          scale = 1,
#                          **kwargs)
    
#     plot_textbox(axes = axes,
#                  x = quiver.U + dx,
#                  y = quiver.V + dy,
#                  s = text)
#     return quiver 

def plot_aux_line(axes : plt.Axes, x0 : float = 0, y0 : float = 0, magnitude : float = 1, angle : float = 0, text : str = '', deg : bool = False, dx : float = 0, dy : float = 0, polar : bool = False, **kwargs):
    if deg:
        _angle =  radians(angle)
    
    x1 = ( magnitude*cos(_angle) ).real
    y1 = ( magnitude*sin(_angle) ).real
    
    if polar:
        coor_line = ( [x0, _angle], [y0, magnitude] )
        coor_text_x = _angle
        coor_text_y = magnitude/2
    else:
        coor_line = ([x0, x1], [y0, y1] )
        coor_text_x = (x1+x0)/2+dx
        coor_text_y = (y1+y0)/2+dy
        
    line = axes.plot( *coor_line,'--k')
    # plot textbox in middel of line
    plot_textbox(axes = axes, x = coor_text_x, y = coor_text_y, s = text, **kwargs)
    return line

def add_point(axes : plt.Axes, value:complex|tuple, **kwargs):
    if isinstance(value, complex):
        x = value.real
        y = value.imag
    if isinstance(value, tuple):
        x = value[0]
        y = value[1]
    point = axes.plot(x, y, 'o', **kwargs)
    return point

# def add_angle(radius, xrange):
#     '''
#     radius
#     range -> start end
#     arrow_start = False
#     arrow_end = True
#     head_scale = 1
#     text = ""
#     text_loc = Mid / Start / End
#     text_loc = On / Over / Under
#     '''
#     def xy(r,phi):
#         return r*np.cos(phi), r*np.sin(phi)
    
#     phi = np.linspace(xrange["start"], xrange['end'], 1000)
    
#     return xy(radius, phi)
