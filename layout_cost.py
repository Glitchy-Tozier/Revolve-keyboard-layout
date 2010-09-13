#!/usr/bin/env python3

"""Calculate the cost of a layout."""

from layout_base import *

from ngrams import get_all_data, letters_in_file_precalculated, trigrams_in_file_precalculated, trigrams_in_file, split_uppercase_trigrams, repeats_in_file_precalculated, repeats_in_file_sorted, unique_sort, letters_in_file, split_uppercase_letters, repeats_in_file, split_uppercase_repeats


### Cost Functions

def key_position_cost_from_file(data=None, letters=None, layout=NEO_LAYOUT, cost_per_key=COST_PER_KEY):
    """Count the total cost due to key positions.

    >>> data = read_file("testfile")
    >>> key_position_cost_from_file(data, cost_per_key=TEST_COST_PER_KEY)
    150
    >>> print(data[:3])
    uia
    >>> key_position_cost_from_file(data, cost_per_key=TEST_COST_PER_KEY)
    150
    >>> key_position_cost_from_file(data[:3], cost_per_key=TEST_COST_PER_KEY)
    11
    >>> lay = switch_keys(["ax"], layout=NEO_LAYOUT)
    >>> key_position_cost_from_file(data[:3], cost_per_key=TEST_COST_PER_KEY, layout=lay)
    20
    >>> data = "UIaĥK\\n"
    >>> key_position_cost_from_file(data, cost_per_key=TEST_COST_PER_KEY, layout=lay)
    90
    """
    if data is not None: 
        letters = letters_in_file(data)
    elif letters is None:
        raise Exception("Need either letters or data")
    letters = split_uppercase_letters(letters, layout=layout)
    cost = 0
    for num, letter in letters:
        pos = find_key(letter, layout=layout)
        if pos is None: # not found => next letter
            continue
        cost += num * cost_per_key[pos[0]][pos[1]]
    return cost

def finger_repeats_from_file(data=None, repeats=None, count_same_key=False, layout=NEO_LAYOUT):
    """Get a list of two char strings from the file, which repeat the same finger.

    >>> data = read_file("testfile")
    >>> finger_repeats_from_file(data)
    [(1, 'Mittel_R', 'rg'), (1, 'Zeige_L', 'eo'), (1, 'Klein_R', 'd\\n')]
    >>> finger_repeats_from_file(data, count_same_key=True)
    [(2, 'Mittel_L', 'aa'), (1, 'Mittel_R', 'rg'), (1, 'Zeige_L', 'eo'), (1, 'Klein_R', 'd\\n'), (1, 'Mittel_L', 'aa'), (1, 'Mittel_L', 'aa')]
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")

    repeats = split_uppercase_repeats(repeats, layout=layout)
    
    finger_repeats = []
    for number, pair in repeats:
        key1 = pair[0]
        key2 = pair[1]
        finger1 = key_to_finger(key1, layout=layout)
        finger2 = key_to_finger(key2, layout=layout)
                
        if finger1 and finger2 and finger1 == finger2:
            finger_repeats.append((number, finger1, key1+key2))
    if not count_same_key:
        finger_repeats = [r for r in finger_repeats if not r[2][0] == r[2][1]]
    return finger_repeats

def finger_repeats_top_and_bottom(finger_repeats, layout):
    """Check which of the finger repeats go from the top to the bottom row or vice versa."""
    top_down_repeats = []
    for number, finger, letters in finger_repeats:
        pos0 = find_key(letters[0], layout)
        pos1 = find_key(letters[1], layout)
        # count it as top down, if the finger has to move over more than one col.
        if pos0 and pos1 and abs(pos0[0] - pos1[0]) > 1: 
            top_down_repeats.append((number, finger, letters))
    return top_down_repeats

def neighboring_fingers(data=None, repeats=None, layout=NEO_LAYOUT):
    """Return the number of times we have to use fingers next to each other.

    >>> data = read_file("testfile")
    >>> neighboring_fingers(data)
    23
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")
    
    repeats = split_uppercase_repeats(repeats, layout=layout)

    fingtups = ((num, (key_to_finger(rep[0]), key_to_finger(rep[1]))) for num, rep in repeats if key_to_finger(rep[0]) and key_to_finger(rep[1]))
    neighcosts = (num*FINGER_SWITCH_COST[fings[0]][fings[1]] for num, fings in fingtups if fings[1] in FINGER_SWITCH_COST[fings[0]])
    return sum(neighcosts)
    

def no_handswitch_after_unbalancing_key(data=None, repeats=None, layout=NEO_LAYOUT):
    """Check how often we have no handswitching after an unbalancing key, weighted by the severity of the unbalancing. This also helps avoiding a handswitch directly after an uppercase key (because shift severly unbalances und with the handswitch we’d effectively have no handswitch after the shift (kind of a shift collision, too). 

    >>> data = read_file("testfile")
    >>> no_handswitch_after_unbalancing_key(data)
    2
    >>> reps =  [(3, "Ab")]
    >>> no_handswitch_after_unbalancing_key(repeats=reps)
    6
    >>> no_handswitch_after_unbalancing_key(repeats=reps, layout=QWERTZ_LAYOUT)
    0
    >>> reps = [(3, "Ga")]
    >>> no_handswitch_after_unbalancing_key(repeats=reps, layout=QWERTZ_LAYOUT)
    3
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")
    
    repeats = split_uppercase_repeats(repeats, layout=layout)

    no_switch = 0
    for number, pair in repeats:
        key1 = pair[0]
        key2 = pair[1]
        pos1 = find_key(key1, layout=layout)
        pos2 = find_key(key2, layout=layout)
        if pos1 and pos2 and pos1 in UNBALANCING_POSITIONS:
                # check if we”re on the same hand
                finger1 = key_to_finger(key1, layout=layout)
                finger2 = key_to_finger(key2, layout=layout)
                if finger1 and finger2 and finger1[-1] == finger2[-1]:
                    no_switch += UNBALANCING_POSITIONS.get(pos1, 0)*number
    return no_switch

def line_changes(data=None, repeats=None, layout=NEO_LAYOUT):
    """Get the number of (line changes divided by the horizontal distance) squared: (rows²/dist)².

    Don’t care about the hand (left index low and right high is still not nice). 

    >>> data = read_file("testfile")
    >>> line_changes(data)
    16.29
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")
    
    repeats = split_uppercase_repeats(repeats, layout=layout)

    line_changes = 0
    for number, pair in repeats:
        key1 = pair[0]
        key2 = pair[1]
        pos1 = find_key(key1, layout=layout)
        pos2 = find_key(key2, layout=layout)
        if pos1 and pos2:
            if not WEIGHT_COUNT_ROW_CHANGES_BETWEEN_HANDS: 
                # check if we”re on the same hand
                finger1 = key_to_finger(key1, layout=layout)
                finger2 = key_to_finger(key2, layout=layout)
                if finger1 and finger2 and finger1[-1] != finger2[-1]:
                    continue # the keys are on different hands, so we don’t count them as row change.
            # row 3 is shifted 1 key to the right → fix that.
            if pos1[0] == 3:
                pos1 = pos1[0], pos1[1] -1, pos1[2]
            if pos2[0] == 3:
                pos2 = pos2[0], pos2[1] -1, pos2[2]
            num_rows = abs(pos1[0] - pos2[0])
            finger_distance = abs(pos1[1] - pos2[1])
            if num_rows:
                cost = num_rows**2 / max(0.25, finger_distance)
                line_changes += cost**2 * number
    return line_changes

def load_per_finger(letters, layout=NEO_LAYOUT, print_load_per_finger=False):
    """Calculate the number of times each finger is being used.

    >>> letters = [(1, "u"), (5, "i"), (10, "2"), (3, " ")]
    >>> load_per_finger(letters)
    {'': 10, 'Klein_L': 1, 'Ring_L': 5, 'Daumen_L': 3}
    """
    letters = split_uppercase_letters(letters, layout)
    fingers = {}
    for num, key in letters:
        finger = key_to_finger(key, layout=layout)
        if finger in fingers:
            fingers[finger] += num
        else: fingers[finger] = num
    # Debug: Print the load per finger
    if print_load_per_finger: 
        from pprint import pprint
        pprint(fingers)
    return fingers

def load_per_hand(letters=None, finger_load=None, layout=NEO_LAYOUT):
    """Calculate the load per hand.

    >>> letters = [(1, "u"), (5, "i"), (10, "2"), (3, " "), (2, "g")]
    >>> load_per_hand(letters)
    [9, 2]
    >>> finger_load = {'': 10, 'Klein_L': 1, 'Ring_L': 5, 'Daumen_L': 3, 'Mittel_R': 2}
    >>> load_per_hand(finger_load = finger_load)
    [9, 2]
    
    """
    if finger_load is None and letters is not None: 
        finger_load = load_per_finger(letters, layout=layout)
    elif letters is None and finger_load is None:
        raise Exception("Need at least letters or precalculated finger_load")
    hand_load = [sum([finger_load[f] for f in finger_load if f.endswith(hand)]) for hand in ("L", "R")]
    return hand_load


def std(numbers):
    """Calculate the standard deviation from a set of numbers.

    This simple calculation is only valid for more than 100 numbers or so. That means I use it in the invalid area. But since it’s just an arbitrary metric, that doesn’t hurt.

    >>> std([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]*10)
    1.607945243653783
    """
    length = float(len(numbers))
    mean = sum(numbers)/max(1, length)
    var = 0
    for i in numbers:
        var += (i - mean)**2
    var /= max(1, (length - 1))
    from math import sqrt
    return sqrt(var)

def finger_balance(letters, layout=NEO_LAYOUT, intended_balance=WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY):
    """Calculate a cost based on the balance between the fingers (using the standard deviation).

    Optimum: All fingers get used exactly the same number of times.

    We ignore unmapped keys ('').
    """
    #: the usage of each finger: {finger1: num, finger2: num, …}
    fingers = load_per_finger(letters, layout)
    # remove the unmapped keys
    if "" in fingers: 
        del fingers[""]
    for finger in fingers:
        idx = FINGER_NAMES.index(finger)
        multiplier = intended_balance[idx]
        fingers[finger] /= multiplier 
    disbalance = std(fingers.values())
    return disbalance

def no_handswitching(trigrams, layout=NEO_LAYOUT):
    """Add a penalty when the hands aren’t switched at least once in every three letters. Doesn’t take any uppercase trigrams into account.

    If there also is a direction change in the trigram, the number of times it occurs gets multiplied by WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE.

    (TODO? WEIGHT_TRIGRAM_FINGER_REPEAT_WITHOUT_KEY_REPEAT)

    TODO: Include the shifts again and split per keyboard. If we did it now, the layout would get optimized for switching after every uppercase letter (as any trigram with a shift and two letters on the same hand would be counted as half a trigram without handswitching). The effect is that it ignores about 7-9% of the trigrams. 

    >>> trigs = [(1, "nrt"), (5, "ige"), (3, "udi")]
    >>> no_handswitching(trigs, layout=NEO_LAYOUT)
    1
    """
    # optimization: we precalculate the fingers for all relevent keys (the ones which are being mutated). 
    key_hand_table = {}
    for key in abc_full:
        #without "⇧⇗ " -> too many false positives when we include the shifts. This also gets rid of anything with uppercase letters in it.
        finger = key_to_finger(key, layout=layout)
        if finger and not finger[:6] == "Daumen": 
            key_hand_table[key] = finger[-1]

    key_pos_horizontal_table = {}
    for key in abc_full:
        #without "⇧⇗ " -> too many false positives when we include the shifts. This also gets rid of anything with uppercase letters in it.
        pos = find_key(key, layout=layout)
        if pos is not None: 
            key_pos_horizontal_table[key] = pos[1]
    

    no_switch = 0
    for num, trig in trigrams:
            # if we have a shift in it, we also have a handswitch. 
            if not trig[0] in key_hand_table or not trig[1] in key_hand_table or not trig[2] in key_hand_table:
                continue
            hand0 = key_hand_table.get(trig[0], None)
            hand1 = key_hand_table.get(trig[1], None)
            hand2 = key_hand_table.get(trig[2], None)
            if hand0 == hand1 and hand1 == hand2:
                pos0 = key_pos_horizontal_table[trig[0]]
                pos1 = key_pos_horizontal_table[trig[1]]
                pos2 = key_pos_horizontal_table[trig[2]]
                if pos0 > pos1 and pos1 < pos2 or pos0 < pos1 and pos1 > pos2:
                    num *= WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE
                else: 
                    num *= WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE
                no_switch += num
    return no_switch


def badly_positioned_shortcut_keys(layout=NEO_LAYOUT, keys="xcvz"):
    """Check, if x, c, v and z are on the left hand and well positioned (much used shortcuts)."""
    badly_positioned = []
    for key in keys: 
        pos = find_key(key, layout=layout)
        # well means not yet left stretch, in row 3, col 5 is also OK.
        if not pos[1] < 5 or (pos[0] == 3 and pos[1] > 5):
            badly_positioned.append(1)
    return sum(badly_positioned)


def total_cost(data=None, letters=None, repeats=None, layout=NEO_LAYOUT, cost_per_key=COST_PER_KEY, trigrams=None, intended_balance=WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY, return_weighted=False):
    """Compute a total cost from all costs we have available, wheighted.

    TODO: reenable the doctests, after the parameters have settled, or pass ALL parameters through the functions.

    @param return_weighted: Set to true to get the weighted values instead of the real values. 
    
    >>> data = read_file("testfile")
    >>> #total_cost(data, cost_per_key=TEST_COST_PER_KEY, intended_balance=TEST_WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY)
    
    (209.4, 3, 150, 0, 3.3380918415851206, 3, 7)
    """
    # the raw costs
    if data is not None: 
        finger_repeats = finger_repeats_from_file(data, layout=layout)
        position_cost = key_position_cost_from_file(data, layout=layout, cost_per_key=cost_per_key)
        letters = letters_in_file(data)
        repeats = repeats_in_file(data)
        trigrams = trigrams_in_file(data)
    elif letters is None or repeats is None:
        raise Exception("Need either repeats und letters or data")
    else:
        finger_repeats = finger_repeats_from_file(repeats=repeats, layout=layout)
        position_cost = key_position_cost_from_file(letters=letters, layout=layout, cost_per_key=cost_per_key)

    no_handswitches = no_handswitching(trigrams, layout=layout)

    frep_num = sum([num for num, fing, rep in finger_repeats])
    finger_repeats_top_bottom = finger_repeats_top_and_bottom(finger_repeats, layout=layout)
    frep_num_top_bottom = sum([num for num, fing, rep in finger_repeats_top_bottom])

    # the number of times neighboring fingers are used – weighted by the ease of transition for the respective fingers
    neighboring_fings = neighboring_fingers(repeats=repeats, layout=layout)

    # the number of changes between lines on the same hand.
    line_change_same_hand = line_changes(repeats=repeats, layout=layout)

    # how often the hand wasn’t switched after an unbalancing key, weighted by the severity of the unbalancing.
    no_switch_after_unbalancing = no_handswitch_after_unbalancing_key(repeats=repeats, layout=layout)

    # the balance between fingers
    disbalance = finger_balance(letters, layout=layout, intended_balance=intended_balance)
    number_of_letters = sum([i for i, s in letters])

    # the position of the keys xcvz - penalty if they are not among the first 5 keys, counted from left, horizontally.
    badly_positioned = badly_positioned_shortcut_keys(layout=layout)

    # add all together and weight them
    total = WEIGHT_POSITION * position_cost
    total += WEIGHT_FINGER_REPEATS * frep_num # not 0.5, since there may be 2 times as many 2-tuples as letters, but the repeats are calculated on the in-between, and these are single.
    total += WEIGHT_FINGER_REPEATS_TOP_BOTTOM * frep_num_top_bottom
    total += WEIGHT_FINGER_SWITCH * neighboring_fings
    total += WEIGHT_FINGER_DISBALANCE * disbalance # needs a minimum number of letters to be useful.
    total += WEIGHT_TOO_LITTLE_HANDSWITCHING * no_handswitches
    total += WEIGHT_XCVZ_ON_BAD_POSITION * number_of_letters * badly_positioned
    total += WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * line_change_same_hand
    total += WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY * no_switch_after_unbalancing

    if not return_weighted: 
        return total, frep_num, position_cost, frep_num_top_bottom, disbalance, no_handswitches, line_change_same_hand
    else:
        return total, WEIGHT_POSITION * position_cost, WEIGHT_FINGER_REPEATS * frep_num , WEIGHT_FINGER_REPEATS_TOP_BOTTOM * frep_num_top_bottom, WEIGHT_FINGER_SWITCH * neighboring_fings, WEIGHT_FINGER_DISBALANCE * disbalance, WEIGHT_TOO_LITTLE_HANDSWITCHING * no_handswitches, WEIGHT_XCVZ_ON_BAD_POSITION * number_of_letters * badly_positioned, WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * line_change_same_hand, WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY * no_switch_after_unbalancing

