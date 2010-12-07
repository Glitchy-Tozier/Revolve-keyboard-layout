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

def line(color=(255,0,0), xy0=(0,0), xy1=(100,50), direction="right", width=3):
    mySVG = svg("Belegung")
    d = defs()

    color_string = "rgb(" + ",".join(str(c) for c in color) + ")"
        
    lg = linearGradient()
    lg.set_id("orange_red")
    s = stop(offset="0%")
    s.set_stop_color(color_string)

    if direction == "right": s.set_stop_opacity(0)
    else: s.set_stop_opacity(1)

    lg.addElement(s)
    s = stop(offset="100%")
    s.set_stop_color('rgb(255,0,0)')

    if direction == "right": s.set_stop_opacity(1)
    else: s.set_stop_opacity(0)
    
    lg.addElement(s)
    d.addElement(lg)

    sh=StyleBuilder()
    sh.setFilling('none')
    sh.setStroke('url(#orange_red)')
    sh.setStrokeWidth(str(width)+'px')

    start = "M " + ",".join([str(p) for p in xy0])
    
    path3=path(start, style=sh.getStyle())
    path3.appendQuadraticCurveToPath(
        0.5*(xy1[0]-xy0[0]), xy1[0]-xy0[0], # control point
        xy1[0]-xy0[0], xy1[1]-xy0[1] # target
        )
    #path3.appendQuadraticCurveToPath(30, -30, 30, 0)
    #path3.appendQuadraticCurveToPath(-0, 30, 30, 0)
    #path3.appendQuadraticCurveToPath(30, -20, 30, 0)
    
    mySVG.addElement(d)
    mySVG.addElement(path3)
    print(mySVG.getXML())

line()
