#!/usr/bin/env python3

"""Generate information about keyboard layouts."""

from layout_cost import *

def format_keyboard_layout(layout):
    """Format a keyboard layout to look like a real keyboard."""
    neo = """
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──────┐
│ ^ │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ ` │ Back │
├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬────┤
│Tab  │ x │ v │ l │ c │ w │ k │ h │ g │ f │ q │ ß │ ´ │ Ret│
├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┐   │
│M3    │ u │ i │ a │ e │ o │ s │ n │ r │ t │ d │ y │ M3│   │
├────┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┴───┤
│Ums │ M4│ ü │ ö │ ä │ p │ z │ b │ m │ , │ . │ j │  Umsch  │
├────┼───┴┬──┴─┬─┴───┴───┴───┴───┴───┴─┬─┴──┬┴───┼────┬────┤
│Strg│ Fe │ Al │      Leerzeichen      │ M4 │ Fe │ Me │Strg│
└────┴────┴────┴───────────────────────┴────┴────┴────┴────┘

    """
    lay = "┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──────┐\n"
    lay +="│ "
    lay += " │ ".join([l[0] for l in layout[0]])
    lay += "    │\n" 
    lay += "├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬────┤\n"
    lay += "│   " 
    lay += " │ ".join([l[0] for l in layout[1][:-1]])
    lay += " │ Ret│\n"
    lay += "├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┐   │\n"
    lay += "│    "
    if layout[2][-2]: 
        lay += " │ ".join([l[0] for l in layout[2][:-1]])
    else:
        lay += " │ ".join([l[0] for l in layout[2][:-2]])
        lay += " │  "
    lay += " │   │\n"
    lay += "├────┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┴───┤\n"
    if layout[3][1]:
        lay += "│  "
        lay += " │ ".join([l[0] for l in layout[3]])
    else:
        lay +="│  ⇧ │ M4│ "
        lay += " │ ".join([l[0] for l in layout[3][2:]])
    lay += "       │\n"
    lay += """├────┼───┴┬──┴─┬─┴───┴───┴───┴───┴───┴─┬─┴──┬┴───┼────┬────┤
│Strg│ Fe │ Alt│      Leerzeichen      │ M4 │ Fe │ Me │Strg│
└────┴────┴────┴───────────────────────┴────┴────┴────┴────┘"""
    return lay


def short_number(s, letters=8):
    """shorten a number to the given number of letters"""
    if not "e" in str(s): 
        return str(s)[:letters]
    else:
        idx = min(letters-4, str(s).index("e"))
        idx = max(0, idx)
        return str(s)[:idx] + str(s)[-4:]



def csv_data(layout, letters=None, repeats=None, number_of_letters=None, number_of_bigrams=None, trigrams=None, number_of_trigrams=None, data=None):
    """Return a list with data for a csv-line for the layout.

    @return cost/word, position_cost, fingerrepeat, finger_disbalance, frep_top_bottom, handswitching, rows², shortcut_keys, unbalancing, patterns"""
    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(
        data=data, 
        letters=letters, number_of_letters=number_of_letters,
        repeats=repeats, number_of_bigrams=number_of_bigrams,
        trigrams=trigrams, number_of_trigrams=number_of_trigrams
        )

    # weighted
    total, cost_w, frep_num_w, frep_num_top_bottom_w, neighboring_fings_w, fing_disbalance_w, no_handswitches_w, badly_positioned_w, line_change_same_hand_w, no_switch_after_unbalancing_w = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams, return_weighted=True)[:10]

    line = []
    
    line.append(total/max(1, number_of_letters)/100)
    line.append(cost_w/1000000000)
    line.append(frep_num_w/1000000000)
    line.append(fing_disbalance_w/1000000000)
    line.append(frep_num_top_bottom_w/1000000000)
    line.append(no_handswitches_w/1000000000)
    line.append(line_change_same_hand_w/1000000000)
    line.append(badly_positioned_w/1000000000)
    line.append(no_switch_after_unbalancing_w/1000000000)
    line.append(neighboring_fings_w/1000000000)
    return line
    

def print_layout_with_statistics(layout, letters=None, repeats=None, number_of_letters=None, number_of_bigrams=None, print_layout=True, trigrams=None, number_of_trigrams=None, verbose=False, data=None, shorten_numbers=False, datapath=None, fingerstats=False, quadratic=False):
    """Print a layout along with statistics."""
    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(
	    data=data, 
	    letters=letters, number_of_letters=number_of_letters,
	    repeats=repeats, number_of_bigrams=number_of_bigrams,
	    trigrams=trigrams, number_of_trigrams=number_of_trigrams,
	    datapath=datapath
        )

    res = ""
    def c(*args):
        """concatenate the args to a string similar to how print() does it, just simpler."""
        return " ".join((str(i) for i in args)) + "\n"
    
    if print_layout:
        res += c(format_layer_1_string(layout))
        res += c(format_keyboard_layout(layout))
        #from pprint import pprint
        #pprint(layout[:5])

    # unweighted
    total, frep_num, cost, frep_top_bottom, disbalance, no_handswitches, line_change_same_hand, hand_load = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams)[:8]
    # weighted
    total, cost_w, frep_num_w, frep_num_top_bottom_w, neighboring_fings_w, fing_disbalance_w, no_handswitches_w, badly_positioned_w, line_change_same_hand_w, no_switch_after_unbalancing_w, hand_disbalance_w, position_cost_quadratic_bigrams_w = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams, return_weighted=True)[:12]

    if shorten_numbers: 
        sn = short_number
    else:
        sn = str

    res += c("#", sn(total/max(1, number_of_letters)/100), "x100 total penalty per letter")
    res += c("#", sn(total / 10000000000), "x10 billion total penalty compared to notime-noeffort")
    res += c("#", sn(cost / max(1, number_of_letters)), "mean key position cost in file 1gramme.txt", "(", str(cost_w/1000000000), ")")
    res += c("#", sn(100 * frep_num / max(1, number_of_bigrams)), "% finger repeats in file 2gramme.txt", "(", str(frep_num_w/1000000000), ")")
    if verbose: 
        res += c("#", sn(disbalance / 1000000), "million keystrokes disbalance of the fingers", "(", str(fing_disbalance_w/1000000000), ")")
        res += c("#", sn(100 * frep_top_bottom / max(1, number_of_bigrams)), "% finger repeats top to bottom or vice versa", "(", str(frep_num_top_bottom_w/1000000000), ")")
        res += c("#", sn(100 * no_handswitches / max(1, number_of_trigrams)), "% of trigrams have no handswitching (after direction change counted x", WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, ")", "(", str(no_handswitches_w/1000000000), ")")
        res += c("#", sn(line_change_same_hand / 1000000000), "billion (rows²/dist)² to cross", "(", str(line_change_same_hand_w/1000000000), ")")
        res += c("#", sn(abs(hand_load[0]/max(1, sum(hand_load)) - 0.5)), "hand disbalance. Left:", hand_load[0]/max(1, sum(hand_load)), "%, Right:", hand_load[1]/max(1, sum(hand_load)), "% (", str(hand_disbalance_w/1000000000), ")")
        res += c("#", sn(badly_positioned_w/1000000000), "badly positioned shortcut keys (weighted).")
        res += c("#", sn(no_switch_after_unbalancing_w/1000000000), "no handswitching after unbalancing key (weighted).")
        res += c("#", sn(neighboring_fings_w/1000000000), "movement pattern cost (weighted).")
    if quadratic:
        # also print the quadratic cost of the key position in bigrams. Selectable to avoid breaking old scripts. 
        res += c("#", sn(position_cost_quadratic_bigrams_w/1000000000), "quadratic position cost in bigrams (weighted).")
    if fingerstats:
        # also print statistics
        # Finger-load:
        finger_load = load_per_finger(letters, layout=layout)
        finger_sum = sum(finger_load.values())
        no_thumbs = [int(1000*finger_load.get(name, 0)/finger_sum)/10 for name in FINGER_NAMES[:4]] + ["-"] + [int(1000*finger_load.get(name, 0)/finger_sum)/10 for name in FINGER_NAMES[6:]]
        res += c("# Finger load %:", *no_thumbs)
    result(res)


