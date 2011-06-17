#!/usr/bin/env python3

"""Get information about keyboard layouts (frontend)."""

from layout_info import *
from check_neo import short_number
sn = short_number

def p(*args, **kwds):
    """print without linebreak (saves typing :) )"""
    return print(end=" ", *args, **kwds)


def _pos_cleanup(pos):
    """Cleanup a position for a better image."""
    # shift the position to fit with the image.
    if pos[0] == 4:
        if pos[1] == 4: pos = (pos[0], pos[1] + 3, pos[2])
        elif pos[1] == 8: pos = (pos[0], pos[1] + 6, pos[2])
        elif pos[1] > 4: pos = (pos[0], pos[1] + 5, pos[2])
    return pos

def pos_to_svg_coord(pos):
    """turn a position tuple into corresponding svg coordinates (xy)."""
    pos = _pos_cleanup(pos)
    if pos[0] == 3 and pos[1] <= 1:
        pos = pos[0], 0.5*pos[1] + 1, pos[2]
    pos = (50*pos[1] - 2, 50 + 50*pos[0])
    return pos

def print_svg(bigrams, layout, svg_output=None, filepath=None, with_keys=True, lett=None, trigrams=None, repeats=None, number_of_letters=None):
    """print an svg from the bigrams.

    svg to png with inkscape (without gui): inkscape -D -z -e neo2.png -f neo2.svg

    TODO: Somehow mark the first letter in words (space-letter bigrams).
    TODO: Add some statistics below the layout image.
    TODO: Legende einfügen: Farben, Dicken, Hintergründe, Punkte im Hintergrundm Richtung.

    @param bigrams: [(number, cost, bigram), …]
    """
    # only import here to avoid the import overhead for other actions.
    from svg_layouts import colorwheel, add_line, svg, defs, StyleBuilder, ShapeBuilder, g, text
    from layout_base import find_key, pos_is_left, get_key, get_all_positions_in_layout
    S = svg("Belegung")
    #oh = ShapeBuilder()
    #S.addElement(oh.createRect(0,0,750,250, strokewidth=0, fill='black'))

    d = defs()
    S.addElement(d)
    S.setAttribute("xmlns:inkscape", "http://www.inkscape.org/namespaces/inkscape")
    S.set_height("350")
    #max_cost = max(cost for number, cost, bigram in bigrams)
    color_scale = 1
    max_linewidth = 25
    max_num = max(number for number, cost, bigram in bigrams)
    num_scale = max_linewidth/max_num
    letters = g()
    letter_dist = g()
    group_handswitch = g()
    group_space = g()
    group_commands = g()
    group_shifts = g()
    group_inwards = g()
    group_outwards = g()
    group_fingerrepeat = g()
    group_info = g()
    for gr in (group_handswitch, group_space, group_commands, group_shifts, group_inwards, group_outwards, group_fingerrepeat, letters, letter_dist, group_info): 
        gr.setAttribute("inkscape:groupmode", "layer")
    group_handswitch.setAttribute("inkscape:label", "Handwechsel")
    group_handswitch.setAttribute("display", "none")
    group_space.setAttribute("inkscape:label", "Leerzeichen")
    group_space.setAttribute("display", "none")
    group_commands.setAttribute("inkscape:label", "Befehl")
    group_commands.setAttribute("display", "none")
    group_shifts.setAttribute("inkscape:label", "Shift")
    group_shifts.setAttribute("display", "none")
    group_inwards.setAttribute("inkscape:label", "Einwärts")
    group_outwards.setAttribute("inkscape:label", "Auswärts")
    group_fingerrepeat.setAttribute("inkscape:label", "Fingerwiederholungen")
    letters.setAttribute("inkscape:label", "Buchstaben")
    letter_dist.setAttribute("inkscape:label", "Häufigkeit")
    group_info.setAttribute("inkscape:label", "Info")

    S.addElement(letter_dist)
    S.addElement(group_info)
    S.addElement(group_handswitch)
    S.addElement(group_space)
    S.addElement(group_commands)
    S.addElement(group_shifts)
    S.addElement(group_inwards)
    S.addElement(group_outwards)
    S.addElement(group_fingerrepeat)
    S.addElement(letters)


    ## letters and trigrams, yes, this is kinda not nice to get them here again…
    if lett is None or trigrams is None or repeats is None or number_of_letters is None: 
        lett, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(datapath=filepath)
    # shape builder for rectangles
    first_letters = {}
    if with_keys: 
        positions = get_all_positions_in_layout(layout)
        #: scale the color for the letters
        letter_scale = 128 / max(num for num, l in lett)
        # get first letters in words
        for num, cost, bi in [(num, cost, bi) for num, cost, bi in bigrams if bi[1:] and (bi[0] == " " or bi[0] == "\n")]:
            fl = bi[1] #: a first letter
            if fl in first_letters: first_letters[fl] += num
            else: first_letters[fl] = num
        #: scale the color for the first letters
        first_letter_scale = 254 / max(first_letters.values())

    else: positions = []
    oh = ShapeBuilder()
    for pos in positions:
        if pos[2] or pos[0]>4: continue # only base layer.

        # fix positions: lower row shifted one to the left, because it is (on standard keyboards)
        if pos[0] != 3:
            pos1 = (pos[0], pos[1] + 1, pos[2])
        else: pos1 = pos

        # get the letter.
        l = get_key(pos, layout=layout)
        # get the coords in the image
        coord = pos_to_svg_coord(pos1)
        
        # get the color for the background
        try: 
            num = lett[[le for n, le in lett].index(l)][0]
        except ValueError: num = 0
        color = colorwheel(num*letter_scale, palette="grey")
        # get the dimensions of the background
        x, y, dx, dy = coord[0]-25, coord[1]-25, 50, 50,
        if pos == (2, 13, 0):
            y -= 50
            dy += 50
            l = "⏎"
        elif pos == (3, 12, 0):
            dx += 100
        # add the background
        letter_dist.addElement(
            oh.createRect(x, y,
                          dx, dy,
                          fill="rgb(" + ",".join([str(c) for c in color]) + ")",
                          stroke="#fafafa"))

        # add the letter itself.
        if l == "<":
            ll = "≤"
        elif l == ">":
            ll == "≥"
        else: ll = l
        t = text(ll, coord[0]-5, coord[1]+4)
        t.set_font_size(18)
        letters.addElement(t)

        # get the color for the first-letter circle
        try: 
            num = first_letters[l]
        except KeyError: num = 0
        color = colorwheel(num*first_letter_scale, palette="grey")
        # get the dimensions of the first-letter circle
        x, y, dx, dy = coord[0]-15, coord[1]-15, 5, 5
        if pos == (2, 13, 0):
            y -= 50
        # add the background
        letter_dist.addElement(
            oh.createCircle(x, y,
                          dx, dy,
                          fill="rgb(" + ",".join([str(c) for c in color]) + ")",
                          stroke=None))


    lay_strings = format_layer_1_string(layout).splitlines()
    for i in range(len(lay_strings)): 
        layout_string = text(lay_strings[i], 50, 300 + 20*i)
        layout_string.set_font_size(18)
        group_info.addElement(layout_string)
    # add statistics
    total, frep_num, cost, frep_top_bottom, disbalance, no_handswitches, line_change_same_hand, hand_load, no_switch_after_unbalancing, manual_penalty, neighboring_unbalance = total_cost(letters=lett, repeats=repeats, layout=layout, trigrams=trigrams)[:11]
    tppl = total/max(1, number_of_letters)
    cost_string = text("cost (tppl): " + str(tppl), 325, 300)
    cost_string.set_font_size(18)
    group_info.addElement(cost_string)
    
    # make sure the most used bigram is shown on top (drawn last)
    bigrams.sort()
    for number, cost, bigram in bigrams:

        pos0 = find_key(bigram[0], layout)
        pos1 = find_key(bigram[1], layout)
        if pos0 is None or pos1 is None:
            continue

        is_left0 = pos_is_left(pos0)
        is_left1 = pos_is_left(pos1)

        # handswitches have far lower opacity
        if is_left0 != is_left1:
            handswitch = True
            opacity = 0.03
            #continue # ignore them, they needlessly blow up the svg.
        else:
            handswitch = False
            opacity = 1.0

        # fix, upscale and reorder the positions
        if pos0[0] != 3:
            pos0 = pos0[0], pos0[1] + 1, pos0[2]
        if pos1[0] != 3:
            pos1 = pos1[0], pos1[1] + 1, pos1[2]
            
        # out- or inwards
        to_right = pos1[1] > pos0[1]
        inwards = is_left0 and to_right or not is_left0 and not to_right

        column_repeat = pos1[1] == pos0[1]
        
        # move the left shifts and m4 1/0.5 step(s) towards the center. They look awkward otherwise.
        pos0 = pos_to_svg_coord(pos0)
        pos1 = pos_to_svg_coord(pos1)

        # move the start and endpoints slightly away from the letters: looks better (thanks to Andreas Wettstein)
        dx0 = dx1 = dy0 = dy1 = 0
        if pos0[1] < pos1[1]: 
            dy0 += 7
            if pos0[0] == pos1[0]: dy1 -= 7
            elif inwards: dy1 -= 5
            else: dy1 += 5
        elif pos0[1] > pos1[1]:
            dy0 = - 7
            if pos0[0] == pos1[0]: dy1 += 7
            elif inwards: dy1 -= 5
            else: dy1 += 5
        if pos0[0] < pos1[0]:
            dx0 = +5
            dx1 = -5
        elif pos0[0] > pos1[0]:
            dx0 = -5
            dx1 = +5
        pos0 = pos0[0] + dx0, pos0[1] + dy0
        pos1 = pos1[0] + dx1, pos1[1] + dy1
        

        color = colorwheel(max(min(1020, cost*color_scale), 0))
        # invert the color
        color = tuple([255-c for c in color])
        width = num_scale * number

        # select the group
        shift = "⇗" in bigram or "⇧" in bigram
        space = " " in bigram
        command = bigram[0] == "♕" or bigram[0] == "♔" or bigram[0] == "♛" or bigram[0] == "♚"

        if space:
            group = group_space
        elif command:
            group = group_commands
        elif column_repeat:
            group = group_fingerrepeat
        elif handswitch:
            group = group_handswitch
        elif shift:
            group = group_shifts
        elif inwards: 
            group = group_inwards
        else:
            group = group_outwards
        
        group.addElement(add_line(d, color=color, xy0=pos0, xy1=pos1, width=width, opacity=opacity, upstroke=inwards))

    if svg_output is None: 
        print(S.getXML())
    else:
        S.save(svg_output, encoding="UTF-8")
        # and try to cleanup the svg with inkscape.
        from subprocess import call
        # this just fails when there’s no inkscape there.
        #call(["inkscape", "-z", "--vacuum-defs", svg_output])

    

def print_bigram_info(layout=NEO_LAYOUT, number=None, filepath=None, bars=False, secondary=True, svg=False, svg_output=None):
    """Print bigram-statistics of the layout."""
    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(datapath=filepath) 
    if not svg: 
        print(format_layer_1_string(layout))
        print("Häufigkeit %, Bigram, Gesamt, Lage, Fingerwiederholung, Finger-oben-unten, Fingerübergang, rows², Kein Handwechsel nach Handverschiebung")
    # svg should have shifts and such.
    if svg: only_layer_0 = True
    else: only_layer_0 = False
    info = bigram_info(layout=layout, filepath=filepath, repeats=repeats, trigrams=trigrams, secondary=secondary, only_layer_0=only_layer_0)
    num_bigrams = sum([num for num, cost, rep in info])
    if number is None: number = len(info)
    numlen = len(str(float(info[0][0])))
    if svg: bigrams_with_cost = []
    for num, cost, rep in info[:number]:
        total, pos, finger_repeats, finger_repeats_top_bottom, movement_pattern, finger_disbalance, no_handswitch_despite_direction_change, shortcut_keys, rows, no_handswitch_after_unbalancing_key, hand_disbalance = cost[:11]
        #p(" "*(numlen-len(str(float(num)))))
        tot = total - finger_disbalance - hand_disbalance - no_handswitch_despite_direction_change  - shortcut_keys
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
        print_svg(bigrams_with_cost, layout, svg_output=svg_output, filepath=filepath, lett=letters, trigrams=trigrams, repeats=repeats, number_of_letters=number_of_letters)
    

def ask_for_layout_string_completion(l):
    """if the layout string only has one line (Windows, I look at you!),
    ask for the other lines."""
    if len(l.splitlines()) < 3:
        for i in range(3-len(l.splitlines())):
            l += "\n" + input("please enter the next line of the layout string: ")
    return l
    
if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser(description="Check and evolve keyboard layouts. Actions can’t be combined, the other options and arguments can. Without action, it checks layouts.")
    # actions
    parser.add_option("-l", "--layout", dest="layout_string", default=None, 
                      help="The layout to test the bigrams against.", metavar="layout_string")
    parser.add_option("-f", "--file", dest="filepath", default=None, 
                      help="Use the given korpus file (file with text).", metavar="filepath")
    parser.add_option("-n", "--number", dest="number", default=1000, type="int", 
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
        options.layout_string = ask_for_layout_string_completion(options.layout_string)
        options.layout = string_to_layout(options.layout_string, base_layout=NEO_LAYOUT)
    else: options.layout = NEO_LAYOUT

    print_bigram_info(layout=options.layout, number=options.number, filepath=options.filepath, bars=options.bars, secondary=options.secondary, svg=options.svg, svg_output=options.svg_output)
