#!/usr/bin/env python3

"""Get information about keyboard layouts (frontend)."""

from layout_info import *
from check_neo import short_number
sn = short_number

def p(*args, **kwds):
    """print without linebreak (saves typing :) )"""
    return print(end=" ", *args, **kwds)

def print_bigram_info(layout=NEO_LAYOUT, number=None): 
    # total, position, finger repeats, finger_repeat_top_to_bottom, movement_pattern, finger_disbalance, no_handswitch_despite_direction_change, shortcut_keys, (row²/col)², no_handswitch_after_unbalancing_key, hand_disbalance, position_cost_quadratic_bigrams
    print(format_layer_1_string(layout))
    print("Häufigkeit, Bigram, Gesamt, Lage, Fingerwiederholung, Finger-oben-unten, Fingerübergang, rows², Kein Handwechsel nach Handverschiebung")
    info = bigram_info(layout=layout)
    if number is None: number = len(info)
    numlen = len(str(info[0][0]))
    for num, cost, rep in info[:number]:
        total, pos, finger_repeats, finger_repeats_top_bottom, movement_pattern, finger_disbalance, no_handswitch_despite_direction_change, shortcut_keys, rows, no_handswitch_after_unbalancing_key, hand_disbalance, position_cost_quadratic_bigrams = cost
        p(" "*(numlen-len(str(int(num)))))
        p(int(num), rep, sn(total - finger_disbalance - hand_disbalance), pos, finger_repeats, finger_repeats_top_bottom, movement_pattern, rows, no_handswitch_after_unbalancing_key)
        p("|")
        if finger_repeats_top_bottom: p("Finger-oben-unten,")
        elif finger_repeats: p("Fingerwiederholung,")
        if movement_pattern: p("Unschöner Fingerübergang,")
        if rows > 0.5: p("Zeilensprung,")
        if no_handswitch_after_unbalancing_key: p("Kein Handwechsel nach Handverschiebung,")
        print()
    
    
if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser(description="Check and evolve keyboard layouts. Actions can’t be combined, the other options and arguments can. Without action, it checks layouts.")
    # actions
    parser.add_option("--layout", dest="layout_string", default=None, 
                      help="The layout to test the bigrams against.", metavar="layout_string")
    parser.add_option("-n", "--number", dest="number", default=None, type="int", 
                      help="The number of bigrams to show.", metavar="number")
    
    (options, args) = parser.parse_args()

    if options.layout_string is not None: 
        options.layout = string_to_layout(options.layout_string, base_layout=NEO_LAYOUT)
    else: options.layout = NEO_LAYOUT

    print_bigram_info(layout=options.layout, number=options.number)
