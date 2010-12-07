#!/usr/bin/env python3

"""Write svg images using pySVG."""

# all imports used in any test
from pysvg.builders import *
from pysvg.core import *
from pysvg.filter import  *
from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *

def HelloWorld1():
    s = svg()
    t = text("Hello World", 0, 100)
    s.addElement(t)
    print(s.getXML())
#    s.save('./testoutput/1_HelloWorld1.svg')

def colorwheel(idx=0):
    """get a color by index, going from red to blue.
    @param idx: color index between 0 and 1020.
    255,0,0
    255,255,0
    0,255,0
    0,255,255
    0,0,255
    """
    if idx < 0:
        raise ValueError("idx outside the valid range between 0 and 1020")
    if idx<=255: return 255, idx, 0
    if idx<=510: return 510-idx, 255, 0
    if idx<=765: return 0,255,idx-510
    if idx<=1020: return 0,1020-idx,255
    raise ValueError("idx outside the valid range between 0 and 1020")

def line(color=(255,0,0), xy0=(0,0), xy1=(200,400), width=3, upstroke=True):
    """Draw a single curved line."""
    mySVG = svg("Belegung")
    d = defs()

    to_right = xy1[0] > xy0[0]

    color_string = "rgb(" + ",".join(str(c) for c in color) + ")"
        
    lg = linearGradient()
    lg.set_id("orange_red")
    s = stop(offset="0%")
    s.set_stop_color(color_string)

    if to_right:
        s.set_stop_opacity(0)
    else: s.set_stop_opacity(1)

    lg.addElement(s)
    s = stop(offset="100%")
    s.set_stop_color('rgb(255,0,0)')

    if to_right:
        s.set_stop_opacity(1)
    else: s.set_stop_opacity(0)
    
    lg.addElement(s)
    d.addElement(lg)

    sh=StyleBuilder()
    sh.setFilling('none')
    sh.setStroke('url(#orange_red)')
    sh.setStrokeWidth(str(width)+'px')

    start = "M " + ",".join([str(p) for p in xy0])
    
    path3=path(start, style=sh.getStyle())

    if not upstroke and xy1[1] > xy0[1]:
        control_y = 1.2*(xy1[1]-xy0[1])
    elif not upstroke and not xy1[1] > xy0[1]:
        control_y = 0.2*(xy1[1]-xy0[1])
    elif upstroke and xy1[1] > xy0[1]:
        control_y = 0.2*(xy1[1]-xy0[1])
    else: 
        control_y = 1.2*(xy1[1]-xy0[1])
        
    path3.appendQuadraticCurveToPath(
        0.5*(xy1[0]-xy0[0]), control_y, # control point, x, y
        xy1[0]-xy0[0], xy1[1]-xy0[1] # target
        )
    
    mySVG.addElement(d)
    mySVG.addElement(path3)
    print(mySVG.getXML())

line()
#line(upstroke=False)
