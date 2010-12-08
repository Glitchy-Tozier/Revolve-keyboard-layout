#!/usr/bin/env python3

"""Get information about keyboard layouts (frontend)."""

from layout_info import *
from check_neo import short_number
sn = short_number

def p(*args, **kwds):
    """print without linebreak (saves typing :) )"""
    return print(end=" ", *args, **kwds)

def print_svg(bigrams, layout, svg_output=None):
    """print an svg from the bigrams.

    @param bigrams: [(number, cost, bigram), …]
    """
    from svg_layouts import colorwheel, add_line, svg, defs, StyleBuilder, ShapeBuilder
    from layout_base import find_key, pos_is_left
    S = svg("Belegung")
    S.setAttribute("pagecolor", "black")
    oh = ShapeBuilder()
    S.addElement(oh.createRect(0,0,700,200, strokewidth=0, fill='black'))

    d = defs()
    #max_cost = max(cost for number, cost, bigram in bigrams)
    color_scale = 1
    #max_num = max(number for number, cost, bigram in bigrams)
    num_scale = 1/1000000
    for number, cost, bigram in bigrams:
        # ignore spaces
        if " " in bigram:
            continue
        pos0 = find_key(bigram[0], layout)
        pos1 = find_key(bigram[1], layout)
        if pos0 is None or pos1 is None:
            continue
        # ignore handswitches
        if pos_is_left(pos0) is not pos_is_left(pos1):
            continue
        # upscale and reorder the positions
        pos0 = (60*pos0[1], 60*pos0[0])
        pos1 = (60*pos1[1], 60*pos1[0])
        color = colorwheel(min(1020, cost*color_scale))
        width = num_scale * number
        add_line(S, d, color=color, xy0=pos0, xy1=pos1, width=width)
    if svg_output is None: 
        print(S.getXML())
    else:
        S.save(svg_output)

    

def print_bigram_info(layout=NEO_LAYOUT, number=None, filepath=None, bars=False, secondary=True, svg=False, svg_output=None): 
    # total, position, finger repeats, finger_repeat_top_to_bottom, movement_pattern, finger_disbalance, no_handswitch_despite_direction_change, shortcut_keys, (row²/col)², no_handswitch_after_unbalancing_key, hand_disbalance, position_cost_quadratic_bigrams
    if not svg: 
        print(format_layer_1_string(layout))
        print("Häufigkeit %, Bigram, Gesamt, Lage, Fingerwiederholung, Finger-oben-unten, Fingerübergang, rows², Kein Handwechsel nach Handverschiebung")
    info = bigram_info(layout=layout, filepath=filepath, secondary=secondary)
    num_bigrams = sum([num for num, cost, rep in info])
    if number is None: number = len(info)
    numlen = len(str(float(info[0][0])))
    if svg: bigrams_with_cost = []
    for num, cost, rep in info[:number]:
        total, pos, finger_repeats, finger_repeats_top_bottom, movement_pattern, finger_disbalance, no_handswitch_despite_direction_change, shortcut_keys, rows, no_handswitch_after_unbalancing_key, hand_disbalance, position_cost_quadratic_bigrams = cost
        #p(" "*(numlen-len(str(float(num)))))
        tot = total - finger_disbalance - hand_disbalance - no_handswitch_despite_direction_change - position_cost_quadratic_bigrams - shortcut_keys
        if svg:
            bigrams_with_cost.append((num, tot, rep))
            continue
        p(sn(100.0*num/num_bigrams, 5), rep, "\t")
        if bars: 
            print("*"*int(tot/60.4))
            continue
        p(sn(tot, 5), "\t")
        p(pos, finger_repeats, finger_repeats_top_bottom, movement_pattern, rows, no_handswitch_after_unbalancing_key, sep="  ")
        p("|")
        if finger_repeats_top_bottom: p("Finger-oben-unten,")
        elif finger_repeats: p("Fingerwiederholung,")
        if movement_pattern: p("Unschöner Fingerübergang,")
        if rows > 0.5: p("Zeilensprung,")
        if no_handswitch_after_unbalancing_key: p("Kein Handwechsel nach Handverschiebung,")
        print()
    if svg:
        print_svg(bigrams_with_cost, layout, svg_output=svg_output)
    
    
if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser(description="Check and evolve keyboard layouts. Actions can’t be combined, the other options and arguments can. Without action, it checks layouts.")
    # actions
    parser.add_option("-l", "--layout", dest="layout_string", default=None, 
                      help="The layout to test the bigrams against.", metavar="layout_string")
    parser.add_option("-f", "--file", dest="filepath", default=None, 
                      help="Use the given korpus file (file with text).", metavar="filepath")
    parser.add_option("-n", "--number", dest="number", default=None, type="int", 
                      help="The number of bigrams to show.", metavar="number")

    parser.add_option("--bars", dest="bars", default=False, action="store_true", 
                      help="Show cost bars instead of numbers.")
    parser.add_option("--svg", dest="svg", default=False, action="store_true", 
                      help="Print an svg instead of printing infos.")
    parser.add_option("--svg-output", dest="svg_output", default=None, 
                      help="Store the svg in the given file.", metavar="filepath")
    parser.add_option("--no-secondary", dest="secondary", action="store_false", default=True, 
                      help="Don’t calculate secondary/indirect bigrams.", metavar="number")

    (options, args) = parser.parse_args()

    if options.layout_string is not None: 
        options.layout = string_to_layout(options.layout_string, base_layout=NEO_LAYOUT)
    else: options.layout = NEO_LAYOUT

    print_bigram_info(layout=options.layout, number=options.number, filepath=options.filepath, bars=options.bars, secondary=options.secondary, svg=options.svg, svg_output=options.svg_output)
