#!/usr/bin/env python3

"""Write svg images using pySVG."""

# all imports used in any test
try: 
    from pysvg.builders import TransformBuilder, StyleBuilder
    #from pysvg.core import 
    #from pysvg.filter import 
    #from pysvg.filter import 
    from pysvg.gradient import linearGradient, stop
    #from pysvg.linking import 
    #from pysvg.script import 
    from pysvg.shape import circle, path
    from pysvg.structure import defs, svg
    #from pysvg.style import 
    from pysvg.text import text
except ImportError:
    raise ImportError("""You need pySVG for python3 for this script to run. Either get it from http://code.google.com/p/pysvg/ and run `2to3 -w *; python3 setup.py install` or get a copy of the converted Mercurial repository from Arne Babenhauserheide (http://draketo.de).""")

def HelloWorld1():
    s = svg()
    t = text("Hello World", 0, 100)
    s.addElement(t)
    print(s.getXML())
#    s.save('./testoutput/1_HelloWorld1.svg')

def colorwheel(idx=0, palette="red_to_blue"):
    """get a color by index, going from red to blue.
    @param idx: color index between 0 and 1020.
    255,0,0
    255,255,0
    0,255,0
    0,255,255
    0,0,255
    """
    if idx < 0:
        raise ValueError("idx outside the valid range between 0 and 1020" + str(idx))
    if palette == "red_to_blue": 
        if idx<=255: return 255, idx, 0
        if idx<=510: return 510-idx, 255, 0
        if idx<=765: return 0,255,idx-510
        if idx<=1020: return 0,1020-idx,255
        raise ValueError("idx outside the valid range between 0 and 1020" + str(idx))
    if palette == "grey":
        if idx<=255: return 255-idx, 255-idx, 255-idx
        raise ValueError("idx outside the valid range between 0 and 255" + str(idx))

def add_line(d, color=(255,0,0), xy0=(0,0), xy1=(200,400), width=3, upstroke=True, opacity=1.0):
    """Draw a single curved line.

    @param S: S = svd(name)
    @param d: d = defs()
    """

    dx = xy1[0] - xy0[0]
    to_right = dx > 0
    dy = xy1[1] - xy0[1]
    upwards = dy < 0

    if to_right: 
        color_id = "r" + "_".join([str(c) for c in color]) + "_" + str(opacity)
    elif not dx and upwards:
        color_id = "u" + "_".join([str(c) for c in color]) + "_" + str(opacity)
    elif not dx and not upwards:
        color_id = "d" + "_".join([str(c) for c in color]) + "_" + str(opacity)
    else: 
        color_id = "l" + "_".join([str(c) for c in color]) + "_" + str(opacity)
    color_string = "rgb(" + ",".join([str(c) for c in color]) + ")"

    lg = linearGradient()
    lg.set_id(color_id)
    s = stop(offset="0%")
    s.set_stop_color(color_string)
    if to_right or not dx and not upwards: 
        s.set_stop_opacity(0.01)
    else: s.set_stop_opacity(opacity)
    lg.addElement(s)
    s = stop(offset="100%")
    s.set_stop_color(color_string)
    if to_right or not dx and not upwards: 
        s.set_stop_opacity(opacity)
    else: s.set_stop_opacity(0.01)
    lg.addElement(s)
    if not dx:
        tb = TransformBuilder()
        tb.setRotation(90)
        lg.set_gradientTransform(tb.getTransform())
    d.addElement(lg)

    sh=StyleBuilder()
    sh.setFilling('none')
    sh.setStroke('url(#' + color_id + ')')
    sh.setStrokeWidth(str(width)+'px')

    start = "M " + ",".join([str(p) for p in xy0])
    
    path3=path(start, style=sh.getStyle())

    if not upstroke and upwards:
        control_y = 0.2*(dy)
    elif not upstroke and not upwards:
        control_y = 1.4*(dy)
    elif upstroke and upwards:
        control_y = 1.4*(dy)
    else: 
        control_y = 0.2*(dy)
    
    # make sure we always have movement up or down.
    if not control_y and upstroke:
        control_y = -0.2 * abs(dx)
    elif not control_y and not upstroke:
        control_y = 0.2 * abs(dx)
    
    path3.appendQuadraticCurveToPath(
        0.5*(dx), control_y, # control point, x, y
        dx, dy # target
        )

    return path3


def add_circle(d, color=(255,0,0), xy=(0,0), width=3, opacity=1.0):
    """Draw a single curved line.

    @param S: S = svd(name)
    @param d: d = defs()
    """

    color_id = "c" + "_".join([str(c) for c in color]) + "_" + str(opacity)
    color_string = "rgb(" + ",".join([str(c) for c in color]) + ")"

    cx, cy = xy

    lg = linearGradient()
    lg.set_id(color_id)
    for i in ("0%", "100%"):
        s = stop(offset=i)
        s.set_stop_color(color_string)
        s.set_stop_opacity(opacity)
        lg.addElement(s)
    d.addElement(lg)
    
    sh=StyleBuilder()
    sh.setFilling('none')#'url(#' + color_id + ')')
    sh.setStroke('url(#' + color_id + ')')
    sh.setStrokeWidth(str(width)+'px')

    c = circle(cx=cx, cy=cy, r=width/2, style=sh.getStyle())

    return c

### Self-Test ###

if __name__ == "__main__": 

    S = svg("Belegung")
    d = defs()
    S.addElement(d)
    
    S.addElement(add_line(d))
    S.addElement(add_line(d, upstroke=False))
    S.addElement(add_line(d, color=(255,0,0), xy0=(200,400), xy1=(100,300), width=6, upstroke=True))
    for i in range(100):
        color=colorwheel(10*i)
        S.addElement(add_line(d, color=color, xy0=(30*i,3*i), xy1=(30*(i+0.5),3*(i+1)), width=i, upstroke=i%2 == 0))
    print(S.getXML())
