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


def bigram_info(layout, secondary=True, only_layer_0=False, filepath=None):
    """Get info about the cost of ngrams and the cost factors."""
    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(datapath=filepath) 
    if only_layer_0: repeats = split_uppercase_repeats(repeats, layout=layout)
    
    reps = {}
    for num, rep in repeats:
        if not rep in reps: reps[rep] = num
        else: reps[rep] += num
    repeats = reps
    if secondary: 
        no_handswitches, secondary_bigrams = no_handswitching(trigrams, layout=layout)
        for num, rep in secondary_bigrams:
            if rep in repeats: repeats[rep] += num
            else: repeats[rep] = num

    reps = []
    for rep, num in repeats.items():
        tmp = split_uppercase_repeats([(1, rep)], layout=layout)
        reps.append((num, total_cost(data=None, letters=[(1, rep[0]), (1, rep[1])], repeats=tmp, layout=layout, cost_per_key=COST_PER_KEY, trigrams=[], intended_balance=WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY, return_weighted=True), rep))
    reps.sort()
    reps.reverse()
    return reps


def trigram_info(layout, only_layer_0=False, filepath=None):
    """Get info about the cost of ngrams and the cost factors."""
    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(datapath=filepath) 
    if only_layer_0: trigrams = split_uppercase_trigrams(trigrams, layout=layout)
    
    trigs = {}
    for num, trig in trigrams:
        if not trig in trigs: trigs[trig] = num
        else: trigs[trig] += num
    trigrams = trigs

    trigs = []
    for trig, num in trigrams.items():
        tmp = split_uppercase_trigrams_correctly([(1, trig)], layout=layout)
        trigs.append((num, total_cost(data=None, letters=[(1, trig[0]), (1, trig[1]), (1, trig[2])], repeats=[(1, trig[:2]), (1, trig[1:])], layout=layout, cost_per_key=COST_PER_KEY, trigrams=tmp, intended_balance=WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY, return_weighted=True), trig))
    trigs.sort()
    trigs.reverse()
    return trigs


if __name__ == "__main__":
    from doctest import testmod
    testmod()
