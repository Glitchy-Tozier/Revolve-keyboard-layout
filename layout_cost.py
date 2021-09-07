#!/usr/bin/env python3
# encoding: utf-8

"""Calculate the cost of a layout."""

# TODO: Add cost when the direction of keystrokes is different for similar keys (direction inwards or outwards).
# Example: au vs üä. I still mix these up after 2 years.
# Lists of Keys which should flow into the same direction: auo äüö, gk bp dt wf, st fp
# TODO: Add cost when the position of keys is inverted (g lower, k upper, but d upper and t lower).
# Reason: Being easy to learn is essential.

from copy import copy
from math import log, sqrt
from pprint import pprint
from random import sample

from config import WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION, WEIGHT_FINGER_REPEATS_INDEXFINGER_MULTIPLIER, WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION_MULTIPLIER, FINGER_SWITCH_COST, SIMILAR_LETTERS, UNBALANCING_POSITIONS, WEIGHT_UNBALANCING_AFTER_UNBALANCING, SHORT_FINGERS, LONG_FINGERS, WEIGHT_COUNT_ROW_CHANGES_BETWEEN_HANDS, WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY, ABC_FULL, WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE, WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM, WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM_HANDSWITCH, COST_MANUAL_BIGRAM_PENALTY, WEIGHT_MANUAL_BIGRAM_PENALTY, WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW, WEIGHT_NEIGHBORING_UNBALANCE, WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY, WEIGHT_FINGER_SWITCH, WEIGHT_FINGER_REPEATS_TOP_BOTTOM, WEIGHT_FINGER_REPEATS, WEIGHT_POSITION, IRREGULARITY_WORDS_RANDOMLY_SAMPLED_FRACTION, WEIGHT_FINGER_DISBALANCE, WEIGHT_TOO_LITTLE_HANDSWITCHING, WEIGHT_XCVZ_ON_BAD_POSITION, WEIGHT_ASYMMETRIC_SIMILAR, WEIGHT_HAND_DISBALANCE, WEIGHT_ASYMMETRIC_BIGRAMS, WEIGHT_IRREGULARITY_PER_LETTER, WEIGHT_CRITICAL_FRACTION, WEIGHT_CRITICAL_FRACTION_MULTIPLIER
from layout_base import argv, COST_PER_KEY, single_key_position_cost, POS_TO_FINGER, FINGER_NAMES, mirror_position_horizontally, Layout, Layouts


from ngrams import get_all_data, letters_in_file_precalculated, trigrams_in_file_precalculated, trigrams_in_file, split_uppercase_trigrams, repeats_in_file_precalculated, repeats_in_file_sorted, unique_sort, letters_in_file, split_uppercase_letters, repeats_in_file, split_uppercase_repeats, split_uppercase_trigrams_correctly, read_file


### Cost Functions

## TODO: add regularity, which uses cost functions from everywhere else

def key_position_cost_from_file(layout, letters, cost_per_key=COST_PER_KEY):
    """Count the total cost due to key positions.

    >>> data = read_file("testfile")
    >>> key_position_cost_from_file(Layouts.NEO2, letters_in_file(data), cost_per_key=TEST_COST_PER_KEY)
    150
    >>> print(data[:3])
    uia
    >>> key_position_cost_from_file(Layouts.NEO2, letters_in_file(data), cost_per_key=TEST_COST_PER_KEY)
    150
    >>> key_position_cost_from_file(Layouts.NEO2, letters_in_file(data)[:3], cost_per_key=TEST_COST_PER_KEY)
    81
    >>> from layout_base import Layout, Layouts
    >>> lay, switched_letters = Layouts.NEO.switch_keys(["ax"])
    >>> key_position_cost_from_file(lay, letters_in_file(data)[:3], cost_per_key=TEST_COST_PER_KEY)
    126
    >>> data = "UIaĥK\\n"
    >>> key_position_cost_from_file(lay, letters_in_file(data), cost_per_key=TEST_COST_PER_KEY)
    240
    """
    letters = split_uppercase_letters(letters, layout)
    cost = 0
    for num, letter in letters:
        pos = layout.char_to_pos(letter)
        cost += num * single_key_position_cost(pos, cost_per_key=cost_per_key)
    return cost

def finger_repeats_from_file(repeats, layout=Layouts.NEO2):
    """Get a list of two char strings from the file, which repeat the same finger.

    >>> from layout_base import Layout, Layouts
    >>> data = read_file("testfile")
    >>> finger_repeats_from_file(repeats_in_file(data), layout=Layouts.NEO2)
    [(9.979, 'Mittel_L', 'Aa'), (4.979, 'Mittel_R', 'rg'), (4.479, 'Zeige_L', 'eo'), (4.979, 'Klein_R', 'd\\n'), (4.979, 'Mittel_L', 'aA')]
    >>> data = "xülävöcpwzoxkjhbmg,qjf.ẞxXkKzZß"
    >>> sorted(finger_repeats_from_file(repeats_in_file(data), layout=Layouts.NEO2))[:3]
    [(4.470000000000001, 'Zeige_L', 'cp'), (4.470000000000001, 'Zeige_L', 'pw'), (4.470000000000001, 'Zeige_L', 'wz')]
    """
    number_of_keystrokes = sum((num for num, pair in repeats))
    critical_point = WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION * number_of_keystrokes
    
    finger_repeats = []
    for number, pair in repeats:
        key1 = pair[0]
        key2 = pair[1]
        finger1 = layout.char_to_finger(key1)
        finger2 = layout.char_to_finger(key2)
        
        if finger1 and finger2 and finger1 == finger2:
            # reduce the cost for finger repetitions of the index finger (it’s very flexible)
            if finger1.startswith("Zeige") or finger2.startswith("Zeige"):
                number *= WEIGHT_FINGER_REPEATS_INDEXFINGER_MULTIPLIER
            # increase the cost abovet the critical point
            if number > critical_point and number_of_keystrokes > 20: # >20 to avoid kicking in for single bigram checks.
                #print(pair, number, number/number_of_keystrokes, WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION, (number - critical_point)*WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION_MULTIPLIER)
                number += (number - critical_point)*(WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION_MULTIPLIER -1)
            finger_repeats.append((number, finger1, key1+key2))
    finger_repeats = [r for r in finger_repeats if not r[2][0] == r[2][1]]
    return finger_repeats

def finger_repeats_top_and_bottom(finger_repeats, layout):
    """Check which of the finger repeats go from the top to the bottom row or vice versa."""
    top_down_repeats = []
    for number, finger, letters in finger_repeats:
        pos0 = layout.char_to_pos(letters[0])
        pos1 = layout.char_to_pos(letters[1])
        # count it as top down, if the finger has to move over more than one col.
        if pos0 and pos1 and abs(pos0[0] - pos1[0]) > 1: 
            top_down_repeats.append((number, finger, letters))
    return top_down_repeats

def _rep_to_fingtuple(num, rep, layout, finger_switch_cost):
    """Turn a repeat and occurance number into num and a fingtuple."""
    finger1 = layout.char_to_finger(rep[0])
    if not finger1 or not finger1 in finger_switch_cost:
        return None, None
    finger2 = layout.char_to_finger(rep[1])
    if not finger2 or not finger2 in finger_switch_cost[finger1]:
        return None, None
    return num, (finger1, finger2)



def movement_pattern_cost(repeats, layout=Layouts.NEO2, FINGER_SWITCH_COST=FINGER_SWITCH_COST):
    """Calculate a movement cost based on the FINGER_SWITCH_COST. 

    >>> data = read_file("testfile")
    >>> print(data)
    uiaenrtAaAa
    eod
    rg
    aa
    <BLANKLINE>
    >>> movement_pattern_cost(repeats_in_file(data), FINGER_SWITCH_COST=TEST_FINGER_SWITCH_COST)
    12
    """
    fingtups = (_rep_to_fingtuple(num, rep, layout, FINGER_SWITCH_COST) for num, rep in repeats)

    return sum((num*FINGER_SWITCH_COST[fings[0]][fings[1]] for num, fings in fingtups if num))

neighboring_fingers = movement_pattern_cost


def asymmetry_cost(layout, symmetries=SIMILAR_LETTERS):
    """Calculate the cost for asymmetric keys.

    :param symmetries: [(first-keys, second-keys), ...]
    
    >>> asymmetry_cost(layout=Layouts.NEO2)
    3.738000251448886
    >>> asymmetry_cost(layout=Layouts.CRY))
    5.8274921289822235
    >>> asymmetry_cost(layout=Layouts.BONE))
    3.1218141120250698
    """
    cost = 0
    for matched in symmetries: # ("auo", "äüö")
        m0 = matched[0] # "auo"
        l = len(m0)
        # print (matched)
        # we have 3 distances: distance in hand, distance in finger
        # and vertical distance. All should be symmetric.
        hand_dists = []
        fing_dists = []
        col_dists = []
        v_directions = []
        for i in range(l):
            positions = [layout.char_to_pos(m[i]) for m in matched]
            # letters = [m[i] for m in matched]
            for j in range(len(positions)):
                for k in range(len(positions[j+1:])):
                    pos0 = positions[j]
                    pos1 = positions[j+k+1]
                    if pos0 is None or pos1 is None: # do not exist on keyboard
                        continue
                    pos0l = layout.pos_is_left(pos0)
                    pos1l = layout.pos_is_left(pos1)
                    if pos0l == pos1l:
                        hand_dists.append(0)
                    elif pos0l and not pos1l:
                        hand_dists.append(1)
                    else:
                        hand_dists.append(-1)
                    # switch the fingers to the left hand so movements
                    # between similar keys are mirrored
                    fing1 = POS_TO_FINGER[pos1[:2] + (0, )][:-2] + "_L"
                    fing2 = POS_TO_FINGER[pos1[:2] + (0, )][:-2] + "_L"
                    if fing1 is not None and fing2 is not None:
                        fingidx1 = FINGER_NAMES.index(fing1)
                        fingidx2 = FINGER_NAMES.index(fing2)
                        fing_dists.append(fingidx2 - fingidx1)
                    else:
                        fing_dists.append(0)
                    col_dists.append(column_distance(pos0, pos1))
                    v_dist = pos1[0] - pos0[0]
                    if v_dist > 0:
                        v_directions.append(1)
                    elif v_dist < 0:
                        v_directions.append(-1)
                    else:
                        v_directions.append(0)
                    # print(letters[j], letters[j+k+1])
        # now we have distances for all three parameters.
        # time to calculate the cost for asymmetry.
        # auo, äüö (NEO): hand_dists = [0, 0, 0], col_dists = [0, 0, 2], v_directions = [1, 1, 1]
        diff_cost = 0
        diffs = []
        # If all are symmetric, cost is 0
        # for the first asymmetric one, add the highest cost
        # for further asymmetric ones, add lower cost.

        # -> just use log(N+1) with N the number of asymmetric ones
        #    divided by the number of possible ones.
        for dists in (hand_dists, fing_dists, col_dists, v_directions):
            dcost = 0
            ddiffs = []
            for i in range(len(dists)):
                for j in range(len(dists[i+1:])):
                    diff = dists[j+i+1] - dists[i]
                    ddiffs.append(diff)
                    if not diff == 0:
                        dcost += 1
            if ddiffs:
                dcost = log((dcost / len(ddiffs)) + 1)
                diff_cost += dcost
                diffs.extend(ddiffs)
        # print (diff_cost, diffs)
        cost += diff_cost
        # if all diffs are 0, cost is 0.
        # all diffs are the same, 
    return cost
                


def no_handswitch_after_unbalancing_key(repeats, layout=Layouts.NEO2):
    """Check how often we have no handswitching after an unbalancing key, weighted by the severity of the unbalancing. This also helps avoiding a handswitch directly after an uppercase key (because shift severly unbalances and with the handswitch we’d effectively have no handswitch after the shift (kind of a shift collision, too).

    If the second key is unbalancing, too, and on the other side of the hand: add it to the cost.

    If the second key is in another row than the first, multiply by the squared distance in rows + 1.

    >>> data = read_file("testfile")
    >>> no_handswitch_after_unbalancing_key(repeats_in_file(data))
    2
    >>> reps =  [(3, "Ab")]
    >>> reps = [(j,i) for i,j in split_uppercase_repeats(reps, layout=Layouts.QWERTZ).items()]
    >>> sorted(reps)
    [(1.5, '⇗b'), (3, 'ab'), (3, '⇗a')]
    >>> no_handswitch_after_unbalancing_key(repeats=reps)
    15.0
    >>> no_handswitch_after_unbalancing_key(repeats=reps, layout=Layouts.QWERTZ)
    0
    >>> reps = [(3, "Ga")]
    >>> reps = [(j,i) for i,j in split_uppercase_repeats(reps, layout=Layouts.QWERTZ).items()]
    >>> no_handswitch_after_unbalancing_key(repeats=reps, layout=Layouts.QWERTZ)
    3
    >>> reps =  [(3, "xo")]
    >>> no_handswitch_after_unbalancing_key(repeats=reps)
    54
    """
    no_switch_cost = 0
    for number, pair in repeats:
        pos1 = layout.char_to_pos(pair[0])
        if not pos1 or not pos1 in UNBALANCING_POSITIONS:
            continue
        pos2 = layout.char_to_pos(pair[1])
        if pos2:
                # check if we”re on the same hand
                is_left1 = layout.pos_is_left(pos1)
                is_left2 = layout.pos_is_left(pos2)
                if is_left1 == is_left2:
                    # check if one of the positions is a thumb
                    fing1 = POS_TO_FINGER[pos1[:2] + (0, )]
                    fing2 = POS_TO_FINGER[pos2[:2] + (0, )]
                    if fing1.startswith("Daumen") or fing2.startswith("Daumen"):
                        continue
                    # using .get here, because most positions aren’t unbalancing.
                    cost = UNBALANCING_POSITIONS.get(pos1, 0)*number
                    # if the second key is unbalancing, too, and on the other side of the hand: add it to the cost
                    if cost and abs(pos1[1] - pos2[1]) >= 4:
                        distance = abs(pos1[1] - pos2[1]) + abs(pos1[0] - pos2[0])
                        unb1 = UNBALANCING_POSITIONS.get(pos1, 0)
                        unb2 = UNBALANCING_POSITIONS.get(pos2, 0)
                        cost += unb1 * unb2 * number * WEIGHT_UNBALANCING_AFTER_UNBALANCING * (distance - 3)
                    # if the second key is in another row than the first, increase the cost, quadratic.
                    row_multiplier = 1 + (abs(pos1[0] - pos2[0]))**2
                    cost *= row_multiplier
                    # if abs(pos1[0] - pos2[0]): 
                    #     print(row_multiplier, pos1[0] - pos2[0], pair)
                    no_switch_cost += cost
    return no_switch_cost


def column_distance(pos1, pos2):
    """Horizontal distance between the keys."""
    column1 = pos1[1]
    column2 = pos2[1]
    # adapt the column, because our data model follows the broken
    # default layout of keyboards
    if pos1[0] in [1,2]:
        column1 += 1
    if pos2[0] in [1,2]:
        column2 += 1
    return column2 - column1


def finger_distance(pos1, pos2):
    """distance in fingers."""
    fing1 = POS_TO_FINGER[pos1]
    fing2 = POS_TO_FINGER[pos2]
    # tumbs and handswitches ignored
    if fing1.startswith("Daumen") or fing2.startswith("Daumen") or fing1[-1] != fing2[-1]:
        return 0
    return abs(FINGER_NAMES.index(fing1) - FINGER_NAMES.index(fing2))


def unbalancing_after_neighboring(repeats, layout=Layouts.NEO2):
    """Check how often an unbalancing key follows a neighboring finger or vice versa.

    >>> data = read_file("testfile")
    """
    neighboring_unbalance = 0
    for number, pair in repeats:

        # only take existing, neighboring positions.
        pos2 = layout.char_to_pos(pair[1])
        pos1 = layout.char_to_pos(pair[0])
        if not pos2 or not pos1 or not pos2 in UNBALANCING_POSITIONS and not pos1 in UNBALANCING_POSITIONS:
            continue
        try: 
            finger_dist = finger_distance(pos1, pos2)
        except Exception: continue
        if not finger_dist: continue # same finger

        # add the cost
        # using .get here, because most positions aren’t unbalancing.
        # divided by nesghboring == finger distance
        neighboring_unbalance += (UNBALANCING_POSITIONS.get(pos2, 0)*number + UNBALANCING_POSITIONS.get(pos1, 0)*number)/(finger_dist**2)
    return neighboring_unbalance

def line_change_positions_cost(pos1, pos2, layout, warped_keyboard):
            num_rows = abs(pos1[0] - pos2[0])
            # if a long finger follows a short finger and the long finger is higher, reduce the number of rows to cross by one. Same for short after long and downwards.
            p1 = pos1[:2] + (0, )
            p2 = pos2[:2] + (0, )
            f1 = POS_TO_FINGER.get(p1, None)
            f2 = POS_TO_FINGER.get(p2, None)
            
            # ignore line changes involving the thumb.
            if not f1 or not f2 or (f1.startswith("Daumen") or f2.startswith("Daumen")):
                return 0

            f1_is_short = f1 in SHORT_FINGERS
            f2_is_short = f2 in SHORT_FINGERS
            f1_is_long = f1 in LONG_FINGERS
            f2_is_long = f2 in LONG_FINGERS
            upwards = pos2[0] < pos1[0]
            downwards = pos2[0] > pos1[0]
            if upwards and f1_is_short and f2_is_long or downwards and f1_is_long and f2_is_short:
                num_rows -= 0.25
            elif downwards and f1_is_short and f2_is_long or upwards and f1_is_long and f2_is_short: # moving upwards to short fingers or downwards to long fingers is bad: add ½
                num_rows += 0.5

            # if a key is disbalancing, multiply the cost
            disbalance1 = UNBALANCING_POSITIONS.get((pos1[0], pos1[1], 0), 0)
            disbalance2 = UNBALANCING_POSITIONS.get((pos2[0], pos2[1], 0), 0)
            
            # row 3 is shifted 1 key to the right → fix that.
            if pos1[0] == 3:
                pos1 = pos1[0], pos1[1] -1, pos1[2]
            if pos2[0] == 3:
                pos2 = pos2[0], pos2[1] -1, pos2[2]

            # The standard keyboard has each key shifted by almost ⅓ compared to the key above it. Use ¼ because not every keyboard is that broken :)
            if warped_keyboard: 
                pos1 = pos1[0], pos1[1] +0.25*pos1[0], pos1[2]
                pos2 = pos2[0], pos2[1] +0.25*pos2[0], pos2[2]

            try:
                finger_distance = abs(FINGER_NAMES.index(f1) - FINGER_NAMES.index(f2))
            except ValueError: finger_distance = abs(pos1[1] - pos2[1]) # one key not on a finger.

            cost = num_rows**2 / max(0.5, finger_distance)
            cost *= (disbalance1+1) * (disbalance2+1)
            return cost

def line_changes(repeats, layout=Layouts.NEO2, warped_keyboard=True):
    """Get the number of (line changes divided by the horizontal distance) squared: (rows²/dist)².

    TODO: Don’t care about the hand (left index low and right high is still not nice).

    >>> data = read_file("testfile")
    >>> line_changes(repeats_in_file(data))
    4.7119140625
    """
    line_changes = 0
    for number, pair in repeats:
        # ignore pairs with spaces (" "): Space is hit with the thumb, so it is no real row jump.
        if " " in pair:
            continue
        key1 = pair[0]
        key2 = pair[1]
        pos1 = layout.char_to_pos(key1)
        pos2 = layout.char_to_pos(key2)
        if pos1 and pos2:
            if not WEIGHT_COUNT_ROW_CHANGES_BETWEEN_HANDS: 
                # check if we’re on the same hand
                is_left1 = layout.pos_is_left(pos1)
                is_left2 = layout.pos_is_left(pos2)
                if is_left1 != is_left2:
                    continue # the keys are on different hands, so we don’t count them as row change.
            cost = line_change_positions_cost(pos1, pos2, layout, warped_keyboard)
            line_changes += cost**2 * number
    return line_changes # to make it not rise linearly (don’t uncomment!): / sum((num for num, rep in repeats))

def load_per_finger(letters, layout=Layouts.NEO2, print_result=False):
    """Calculate the number of times each finger is being used.

    >>> letters = [(1, "u"), (5, "i"), (10, "2"), (3, " "), (4, "A"), (6, "Δ")]
    >>> sorted(load_per_finger(letters).items())[1:]
    [('Klein_L', 23), ('Klein_R', 10), ('Mittel_L', 4), ('Mittel_R', 10), ('Ring_L', 5)]
    """
    letters = split_uppercase_letters(letters, layout)
    fingers = {}
    for num, key in letters:
        finger = layout.char_to_finger(key)
        if finger in fingers:
            fingers[finger] += num
        else: fingers[finger] = num
    # Debug: Print the load per finger
    if print_result: 
        pprint(fingers)
    return fingers

def load_per_hand(letters=None, finger_load=None, layout=Layouts.NEO2):
    """Calculate the load per hand.

    >>> letters = [(1, "u"), (5, "i"), (10, "2"), (3, " "), (2, "g")]
    >>> load_per_hand(letters)
    [16, 12]
    >>> finger_load = {'': 10, 'Klein_L': 1, 'Ring_L': 5, 'Daumen_L': 3, 'Mittel_R': 2}
    >>> load_per_hand(finger_load = finger_load)
    [6, 2]
    
    """
    if finger_load is None and letters is not None: 
        finger_load = load_per_finger(letters, layout=layout)
    elif letters is None and finger_load is None:
        raise Exception("Need at least letters or precalculated finger_load")
    # ignore the thumbs, because currently space is always hit with the left thumb.
    hand_load = [sum([finger_load[f] for f in finger_load if f.endswith(hand) and not f.startswith('Daumen')]) for hand in ("L", "R")]
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
    return sqrt(var)

def finger_balance(letters, layout=Layouts.NEO2, intended_balance=WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY):
    """Calculate a cost based on the balance between the fingers (using the standard deviation).

    Optimum: All fingers get used exactly the same number of times.

    We ignore unmapped keys ('').
    """
    #: the usage of each finger: {finger1: num, finger2: num, …}
    fingers = load_per_finger(letters, layout)
    # make sure, all fingers are in the list (for very short texts)
    for fing in FINGER_NAMES:
        if not fing in fingers and not fing[:6] == "Daumen":
            fingers[fing] = 0
    # remove the unmapped keys
    if "" in fingers: 
        del fingers[""]
    for finger in fingers:
        idx = FINGER_NAMES.index(finger)
        multiplier = intended_balance[idx]
        fingers[finger] /= multiplier 
    disbalance = std(fingers.values())
    return disbalance

def _trigram_key_tables(trigrams, layout): 
    """optimization: we precalculate the fingers for all relevent keys (the ones which are being mutated). Since we only need to know if the hands are the same, left hand is False and right hand is True."""
    key_hand_table = {}
    for key in ABC_FULL:
        #without "⇧⇗ " -> too many false positives when we include the shifts. This also gets rid of anything with uppercase letters in it.
        finger = layout.char_to_finger(key)
        if finger and not finger[:6] == "Daumen":
            if finger[-1] == "L": 
                key_hand_table[key] = False
            elif finger[-1] == "R":
                key_hand_table[key] = True
            # with this, not found is ignored.

    key_pos_horizontal_table = {}
    for key in ABC_FULL:
        #without "⇧⇗ " -> too many false positives when we include the shifts. This also gets rid of anything with uppercase letters in it.
        pos = layout.char_to_pos(key)
        try: 
            key_pos_horizontal_table[key] = pos[1]
        except TypeError:
            pass # not found. Ignore as above.
    return key_hand_table, key_pos_horizontal_table


def _no_handswitching(trigrams, key_hand_table, key_pos_horizontal_table, WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE, WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM, WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM_HANDSWITCH):
    """Do the hard work for no_handswitching without any call to outer functions.
    >>> trigs = [(1, "nrt"), (5, "ige"), (3, "udi"), (2, "ntr")]
    >>> key_hand_table, key_pos_horizontal_table = _trigram_key_tables(trigs, layout=Layouts.NEO2)
    >>> res = _no_handswitching(trigs, key_hand_table, key_pos_horizontal_table, WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE, TEST_WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM, WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM_HANDSWITCH)
    >>> (res[0], [(j,i) for i,j in sorted(res[1].items())])
    (2, [(4.0, 'ie'), (1.0, 'nr'), (0.5, 'nt'), (2.4000000000000004, 'ui')])
    """
    no_switch = 0
    secondary_bigrams = {} # {bigram: num, …}
    for num, trig in trigrams:
        t0, t1, t2 = trig[0], trig[1], trig[2]
        try:
            hand0 = key_hand_table[t0]
            hand1 = key_hand_table[t1]
            hand2 = key_hand_table[t2]
        except KeyError:
            # if one of the trigs is not in the key_hand_table, we don’t count the trigram.
            continue
        if hand0 is hand2:
            # add secondary bigrams
            bi = t0+t2
            if hand0 is hand1: # no handswitch
                pos0 = key_pos_horizontal_table[t0]
                pos1 = key_pos_horizontal_table[t1]
                pos2 = key_pos_horizontal_table[t2]
                if pos0 > pos1 and pos1 < pos2 or pos0 < pos1 and pos1 > pos2:
                    no_switch += num * WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE
                else: 
                    no_switch += num * WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE
                try:
                    secondary_bigrams[bi] += num * WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM
                except KeyError: secondary_bigrams[bi] = num * WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM
                # Add bigram cost key 1 and key 3 if there are two handswitches; reduce via a multiplier < 1.0 ; Faktor könnte vom Tippaufwand der mittleren Taste abhängen: Je besser oder schneller die mittlere Taste getippt werden kann, desto grösser der Faktor. Das ist aber vermutlich nur eine unnötige Komplikation.
            else: # double handswitch
                try:
                    secondary_bigrams[bi] += num * WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM_HANDSWITCH
                except KeyError: secondary_bigrams[bi] = num * WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM_HANDSWITCH

    return no_switch, secondary_bigrams
    

def no_handswitching(trigrams, layout):
    """Add a penalty when the hands aren’t switched at least once in every three letters. Doesn’t take any uppercase trigrams into account.

    If there also is a direction change in the trigram, the number of times it occurs gets multiplied by WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE.

    If there is no direction change, it gets multiplied with WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE. If that is 0, handswitches without direction change are ignored.

    (TODO? WEIGHT_TRIGRAM_FINGER_REPEAT_WITHOUT_KEY_REPEAT)

    TODO: Include the shifts again and split per keyboard. If we did it now, the layout would get optimized for switching after every uppercase letter (as any trigram with a shift and two letters on the same hand would be counted as half a trigram without handswitching). The effect is that it ignores about 7-9% of the trigrams. 

    >>> trigs = [(1, "nrt"), (5, "ige"), (3, "udi"), (2, "ntr")]
    >>> no_handswitching(trigs, Layouts.NEO2)[0]
    2
    >>> sorted(no_handswitching(trigs, Layouts.NEO2)[1].items())[0][0]
    'ie'
    """
    key_hand_table, key_pos_horizontal_table = _trigram_key_tables(trigrams, layout=layout)
    return _no_handswitching(trigrams, key_hand_table, key_pos_horizontal_table, WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE, WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM, WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM_HANDSWITCH)


def badly_positioned_shortcut_keys(layout, keys="xcvz"):
    """Check, if x, c, v and z are on the left hand and well positioned (much used shortcuts)."""
    badly_positioned = []
    for key in keys: 
        pos = layout.char_to_pos(key)
        # well means not yet left stretch, in row 3, col 5 is also OK.
        if not pos[1] < 5 or (pos[0] == 3 and pos[1] > 5):
            badly_positioned.append(1)
    return sum(badly_positioned)


def manual_bigram_penalty(bigrams, layout):
    """Add manual penalty for bad to type bigrams which are hard to catch algorithmically."""
    penalty = 0
    for num, bi in bigrams:
        pos1 = layout.char_to_pos(bi[0])
        pos2 = layout.char_to_pos(bi[1])
        if pos1 is None or pos2 is None: continue

        penalty += COST_MANUAL_BIGRAM_PENALTY.get((pos1, pos2), 0)*num
    return penalty
        

def asymmetric_bigram_penalty(bigrams, layout):
    """Penalty for asymmetric bigrams.

    If the second letter is not at the horizontally mirrored position of the first one, typing is harder than if it is.

    >>> a = asymmetric_bigram_penalty
    >>> a([(1, "en")])
    0
    >>> a([(2, "ek")])
    2

    Idea: Use symmetric hand movement instead of symmetric keys."""
    return sum((num for num, bi in bigrams if layout.char_to_pos(bi[0]) != mirror_position_horizontally(layout.char_to_pos(bi[1]))))
        

def irregularity_from_trigrams(all_trigrams, switched_letters=None, trigram_cost_dic=None, warped_keyboard=True, layout=Layouts.NEO2, cost_per_key=COST_PER_KEY):
    """Calculate the irregularity by splitting trigrams into bigrams and including all bigram-costs.

    This is a proxy for bad to type words: it gives higher cost to trigrams in which both bigrams are bad.

    irregularity = sqrt(cost(a) * cost(b)
                        for a, b in split_trigrams)

    >>> much = irregularity_from_trigrams([(1, "nnn"), (2, "nnn"), (2, "nkn"), (2, "nßn"), (1, "nrt"), (5, "ige"), (3, "udi"), (2, "ntr")], True, layout=Layouts.NEO2)
    >>> nnn = irregularity_from_trigrams([(1, "nnn")], True, layout=Layouts.NEO2)
    >>> nxn = irregularity_from_trigrams([(1, "nxn")], True, layout=Layouts.NEO2)
    >>> nnnnxn = irregularity_from_trigrams([(1, "nnn"), (1, "nxn")], True, layout=Layouts.NEO2)
    >>> nxnnxn = irregularity_from_trigrams([(1, "nxn"), (1, "nxn")], True, layout=Layouts.NEO2)
    >>> [nxn > nnn, nxnnxn > nxn, nxnnxn > nnnnxn, nnnnxn > nxn, much > nxnnxn]
    [True, True, True, True, True]
    
    """
    print_output = False
    if print_output:
        print()

    number_of_keystrokes = sum((num for num, trig in all_trigrams))
    critical_point = WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION * number_of_keystrokes
    trigrams_to_test = set()
    new_trigram_cost_dic = {}
    
    # if this isn't the first loop and there's a reasonable amount of switched letters
    if switched_letters and trigram_cost_dic and len(switched_letters) > 0 and len(switched_letters) < 80: # 80 because it's the max. number of switched_letters when 10 keys are replaced.
        if print_output:
            print(len(switched_letters), "moved letters:", switched_letters)
        new_trigram_cost_dic = copy(trigram_cost_dic)
        # select which trigrams actually need testing
        for trigram_tuple in all_trigrams:
            trig = trigram_tuple[1]
            for switched_letter in switched_letters:
                if switched_letter in trig:
                    trigrams_to_test.add(trigram_tuple)
                    break
    else:
        trigrams_to_test = all_trigrams

    if print_output:
        test_trigs_count = len(trigrams_to_test)
        all_trigs_count = len(all_trigrams)
        print("Trigrams that need testing:", '{:_}'.format(test_trigs_count), "/", '{:_}'.format(all_trigs_count))

    for num, trig in trigrams_to_test:
        bi1 = trig[:2]
        bi2 = trig[1:]
        pos1_1 = layout.char_to_pos(bi1[0])
        pos1_2 = layout.char_to_pos(bi1[1])
        pos2_1 = pos1_2
        pos2_2 = layout.char_to_pos(bi2[1])
        if pos1_1 and pos1_2 and pos2_1 and pos2_2:
            penalty1 = 0
            penalty2 = 0
            pos1_1_unbalances = pos1_1 in UNBALANCING_POSITIONS
            pos1_2_unbalances = pos1_2 in UNBALANCING_POSITIONS
            pos2_1_unbalances = pos1_2_unbalances
            pos2_2_unbalances = pos2_2 in UNBALANCING_POSITIONS
            # first aggregate all the different costs in penalty1 and penalty2
            # embed all cost functions in here
            # def manual_bigram_penalty(bigrams, layout=Layouts.NEO2):
            penalty1 += WEIGHT_MANUAL_BIGRAM_PENALTY * COST_MANUAL_BIGRAM_PENALTY.get((pos1_1, pos1_2), 0)
            penalty2 += WEIGHT_MANUAL_BIGRAM_PENALTY * COST_MANUAL_BIGRAM_PENALTY.get((pos2_1, pos2_2), 0)
            # def line_changes(repeats, layout=Layouts.NEO2, warped_keyboard=True):
            # check if we’re on the same hand
            is_left1_1 = layout.pos_is_left(pos1_1)
            is_left1_2 = layout.pos_is_left(pos1_2)
            is_left2_1 = is_left1_2
            is_left2_2 = layout.pos_is_left(pos2_2)
            fing1_1 = POS_TO_FINGER[pos1_1[:2] + (0, )]
            fing1_2 = POS_TO_FINGER[pos1_2[:2] + (0, )]
            fing2_1 = fing1_2
            fing2_2 = POS_TO_FINGER[pos2_2[:2] + (0, )]
            if WEIGHT_COUNT_ROW_CHANGES_BETWEEN_HANDS or (is_left1_1 == is_left1_2 and is_left2_1 == is_left2_2):
                penalty1 += WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * num * line_change_positions_cost(pos1_1, pos1_2, layout, warped_keyboard)**2
                penalty2 += WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * num * line_change_positions_cost(pos2_1, pos2_2, layout, warped_keyboard)**2
            # def unbalancing_after_neighboring(repeats, layout=Layouts.NEO2):
            if pos1_1_unbalances or pos1_2_unbalances:
                try: finger_dist1 = finger_distance(pos1_1, pos1_2)
                except Exception: finger_dist1 = None
                if finger_dist1:
                    penalty1 += WEIGHT_NEIGHBORING_UNBALANCE * (UNBALANCING_POSITIONS.get(pos1_2, 0)*num + UNBALANCING_POSITIONS.get(pos1_1, 0)*num)/(finger_dist1**2)
            if pos2_1_unbalances or pos2_2_unbalances:
                try: finger_dist2 = finger_distance(pos1_1, pos1_2)
                except Exception: finger_dist2 = None
                if finger_dist2:
                    penalty2 += WEIGHT_NEIGHBORING_UNBALANCE * (UNBALANCING_POSITIONS.get(pos2_2, 0)*num + UNBALANCING_POSITIONS.get(pos2_1, 0)*num)/(finger_dist2**2)
            # def no_handswitch_after_unbalancing_key(repeats, layout=Layouts.NEO2):
            if pos1_1_unbalances:
                if is_left1_1 == is_left1_2:
                    if not fing1_1.startswith("Daumen") and not fing1_2.startswith("Daumen"):
                        cost = UNBALANCING_POSITIONS.get(pos1_1, 0) * num
                        if cost and abs(pos1_1[1] - pos1_2[1]) >= 4:
                            distance = abs(pos1_1[1] - pos1_2[1]) + abs(pos1_1[0] - pos1_2[0])
                            unb1 = UNBALANCING_POSITIONS.get(pos1_1, 0)
                            unb2 = UNBALANCING_POSITIONS.get(pos1_2, 0)
                            cost += unb1 * unb2 * num * WEIGHT_UNBALANCING_AFTER_UNBALANCING * (distance - 3)
                        row_multiplier = 1 + (abs(pos1_1[0] - pos1_2[0]))**2
                        penalty1 += WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY * row_multiplier * cost
            if pos2_1_unbalances:
                if is_left2_1 == is_left2_2:
                    if not fing2_1.startswith("Daumen") and not fing2_2.startswith("Daumen"):
                        cost = UNBALANCING_POSITIONS.get(pos2_1, 0) * num
                        if cost and abs(pos2_1[1] - pos2_2[1]) >= 4:
                            distance = abs(pos2_1[1] - pos2_2[1]) + abs(pos2_1[0] - pos2_2[0])
                            unb1 = UNBALANCING_POSITIONS.get(pos2_1, 0)
                            unb2 = UNBALANCING_POSITIONS.get(pos2_2, 0)
                            cost += unb1 * unb2 * num * WEIGHT_UNBALANCING_AFTER_UNBALANCING * (distance - 3)
                        row_multiplier = 1 + (abs(pos2_1[0] - pos2_2[0]))**2
                        penalty2 += WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY * row_multiplier * cost
            # def movement_pattern_cost(repeats, layout=Layouts.NEO2, FINGER_SWITCH_COST=FINGER_SWITCH_COST):
            nums1, fings1 = _rep_to_fingtuple(num, bi1, layout, FINGER_SWITCH_COST)
            if nums1:
                penalty1 += WEIGHT_FINGER_SWITCH * nums1 * FINGER_SWITCH_COST[fings1[0]][fings1[1]]
            nums2, fings2 = _rep_to_fingtuple(num, bi2, layout, FINGER_SWITCH_COST)
            if nums2:
                penalty2 += WEIGHT_FINGER_SWITCH * nums2 * FINGER_SWITCH_COST[fings2[0]][fings2[1]]
            # def finger_repeats_from_file(repeats, layout=Layouts.NEO2):
            if fing1_1 and fing1_2 and fing1_1 == fing1_2 and bi1[0] != bi1[1]:
                fing_repeat_count1 = num
                # reduce the cost for finger repetitions of the index finger (it’s very flexible)
                if fing1_1.startswith("Zeige") or fing1_2.startswith("Zeige"):
                    fing_repeat_count1 *= WEIGHT_FINGER_REPEATS_INDEXFINGER_MULTIPLIER
                if fing_repeat_count1 > critical_point and number_of_keystrokes > 20: # >20 to avoid kicking in for single bigram checks.
                    fing_repeat_count1 += (fing_repeat_count1 - critical_point)*(WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION_MULTIPLIER - 1)
                penalty1 += WEIGHT_FINGER_REPEATS * fing_repeat_count1
                # def finger_repeats_top_and_bottom(finger_repeats, layout):
                if abs(pos1_1[0] - pos1_2[0]) > 1:
                    penalty1 += WEIGHT_FINGER_REPEATS_TOP_BOTTOM * fing_repeat_count1
            if fing2_1 and fing2_2 and fing2_1 == fing2_2 and bi2[0] != bi2[1]:
                fing_repeat_count2 = num
                # reduce the cost for finger repetitions of the index finger (it’s very flexible)
                if fing2_1.startswith("Zeige") or fing2_2.startswith("Zeige"):
                    fing_repeat_count2 *= WEIGHT_FINGER_REPEATS_INDEXFINGER_MULTIPLIER
                if fing_repeat_count2 > critical_point and number_of_keystrokes > 20: # >20 to avoid kicking in for single bigram checks.
                    fing_repeat_count2 += (fing_repeat_count2 - critical_point)*(WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION_MULTIPLIER - 1)
                penalty2 += WEIGHT_FINGER_REPEATS * fing_repeat_count2
                # def finger_repeats_top_and_bottom(finger_repeats, layout):
                if abs(pos2_1[0] - pos2_2[0]) > 1:
                    penalty2 += WEIGHT_FINGER_REPEATS_TOP_BOTTOM * fing_repeat_count2
            # def key_position_cost_from_file(letters, layout=Layouts.NEO2, cost_per_key=COST_PER_KEY):
            penalty1 += WEIGHT_POSITION * key_position_cost_from_file(layout, [(num, letter) for letter in bi1], cost_per_key=cost_per_key)
            penalty2 += WEIGHT_POSITION * key_position_cost_from_file(layout, [(num, letter) for letter in bi2], cost_per_key=cost_per_key)
            ## now actually do the calculation
            new_trigram_cost_dic[trig] = penalty1 * penalty2
        else:
            if print_output:
                print("Trigram wasn't found:",'<trig>"%s"</trig>' % trig)
                for idx, letter in enumerate(trig):
                    print("Letter", idx, "of Trigram (unicode):", letter.encode("unicode_escape"))
    irregularity_penalty = sqrt(sum(new_trigram_cost_dic.values()))
    return irregularity_penalty, new_trigram_cost_dic


def irregularity(words, layout=Layouts.NEO2, **opts):
    """Irregularity of the cost per word: The std of the total_cost for
    each word in words (normally read from IRREGULARITY_REFERENCE_TEXT)."""

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
        return sqrt(var)

    data = []
    if IRREGULARITY_WORDS_RANDOMLY_SAMPLED_FRACTION < 1.0:
        words = sample(words, max(2, int(len(words) * IRREGULARITY_WORDS_RANDOMLY_SAMPLED_FRACTION)))
    for word in words:
        data.append(total_cost(layout, data=word, check_irregularity=False, **opts)[0] / len(word))
    return std(data)


def aggregate_cost(number_of_letters=0, position_cost=0, frep_num=0, frep_num_top_bottom=0, neighboring_fings=0, disbalance=0, no_handswitches=0, badly_positioned=0, asymmetric_similar=0, line_change_same_hand=0, no_switch_after_unbalancing=0, hand_disbalance=0, manual_penalty=0, neighboring_unbalance=0, asymmetric_bigrams=0, irregularity_penalty=0):
    total = WEIGHT_POSITION * position_cost
    total += WEIGHT_FINGER_REPEATS * frep_num # not 0.5, since there may be 2 times as many 2-tuples as letters, but the repeats are calculated on the in-between, and these are single.
    total += WEIGHT_FINGER_REPEATS_TOP_BOTTOM * frep_num_top_bottom
    total += WEIGHT_FINGER_SWITCH * neighboring_fings
    total += WEIGHT_FINGER_DISBALANCE * disbalance # needs a minimum number of letters to be useful.
    total += WEIGHT_TOO_LITTLE_HANDSWITCHING * no_handswitches
    total += WEIGHT_XCVZ_ON_BAD_POSITION * number_of_letters * badly_positioned
    total += WEIGHT_ASYMMETRIC_SIMILAR * number_of_letters * asymmetric_similar
    total += WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * line_change_same_hand
    total += WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY * no_switch_after_unbalancing
    total += WEIGHT_HAND_DISBALANCE * number_of_letters * hand_disbalance
    total += WEIGHT_MANUAL_BIGRAM_PENALTY * manual_penalty
    total += WEIGHT_NEIGHBORING_UNBALANCE * neighboring_unbalance
    total += WEIGHT_ASYMMETRIC_BIGRAMS * asymmetric_bigrams
    total += WEIGHT_IRREGULARITY_PER_LETTER * irregularity_penalty
    return total



def total_cost(layout, data=None, letters=None, switched_letters=None, repeats=None, cost_per_key=COST_PER_KEY, trigrams=None, trigram_cost_dic=None, intended_balance=WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY, return_weighted=False, check_irregularity=True, max_cost=None):
    """Compute a total cost from all costs we have available, wheighted.

    TODO: reenable the doctests, after the parameters have settled, or pass ALL parameters through the functions.

    @param return_weighted: Set to true to get the weighted values instead of the real values. 
    
    @param check_irregularity: Check the irregularity. This calles total_cost again for every word in a reference sentence and might be very expensive.

    >>> data = read_file("testfile")
    >>> #total_cost(layout, data, cost_per_key=TEST_COST_PER_KEY, intended_balance=TEST_WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY)
    
    (209.4, 3, 150, 0, 3.3380918415851206, 3, 7)
    """
    # the raw costs
    if data is not None:
        letters, num_letters, repeats, num_repeats, trigrams, number_of_trigrams = get_all_data(data=data, layout=layout)
        # first split uppercase repeats *here*, so we don’t have to do it in each function.
        reps = split_uppercase_repeats(repeats, layout=layout)
        
    elif letters is None or repeats is None or trigrams is None:
        raise Exception("Need either trigrams, repeats and letters or data")
    else:
        # first split uppercase repeats *here*, so we don’t have to do it in each function.
        reps = split_uppercase_repeats(repeats, layout=layout)

    number_of_letters = sum([i for i, s in letters])

    ## first do cheap checks
    # cost of letter positions on the keyboard
    position_cost = key_position_cost_from_file(layout, letters=letters, cost_per_key=cost_per_key)
    
    # the balance between fingers
    disbalance = finger_balance(letters, layout=layout, intended_balance=intended_balance)

    # the position of the keys xcvz - penalty if they are not among the first 5 keys, counted from left, horizontally.
    badly_positioned = badly_positioned_shortcut_keys(layout)

    # the cost for having asymmetries in similar keys.
    asymmetric_similar = asymmetry_cost(layout)

    # the load distribution on the hands: [left keystrokes, right keystrokes]
    hand_load = load_per_hand(letters, layout=layout)
    # the disbalance between the hands. Keystrokes of the left / total strokes - 0.5. From 0 to 0.5, ignoring the direction.
    hand_disbalance = abs(hand_load[0]/max(1, sum(hand_load)) - 0.5)

    cheap_total = aggregate_cost(number_of_letters=number_of_letters,
                                 position_cost=position_cost,
                                 disbalance=disbalance,
                                 badly_positioned=badly_positioned,
                                 asymmetric_similar=asymmetric_similar,
                                 hand_disbalance=hand_disbalance)
    # bail out early if we’re already above the allowed max cost
    if max_cost and max_cost < cheap_total:
        return cheap_total

    # add secondary bigrams from trigrams
    no_handswitches, secondary_bigrams = no_handswitching(trigrams, layout=layout)
    for pair in secondary_bigrams:
        try: reps[pair] += secondary_bigrams[pair]
        except KeyError: reps[pair] = secondary_bigrams[pair]
        
    # value bigrams which occur more than once per DinA4 site even higher (psychologically important: get rid of really rough points).
    number_of_keystrokes = sum(reps.values())
    critical_point = WEIGHT_CRITICAL_FRACTION * number_of_keystrokes

    for pair, number in reps.items(): 
        if number > critical_point and number_of_keystrokes > 20: # >20 to avoid kicking in for single bigram checks.
            #print(pair, number, number/number_of_keystrokes, WEIGHT_CRITICAL_FRACTION, (number - critical_point)*(WEIGHT_CRITICAL_FRACTION_MULTIPLIER-1))
            number += (number - critical_point)*(WEIGHT_CRITICAL_FRACTION_MULTIPLIER -1)
            reps[pair] = number

    reps = [(num, pair) for pair, num in reps.items()]

    # print(len(reps) /len(reps_uncleaned))
    # check repeat cleanup
    # pairs = [pair for num, pair in reps]
    # pairs_old = [pair for num, pair in reps_uncleaned]
    # for pair in pairs_old:
    #     if not pair in pairs:
    #         print(pair, end=",")
        

    finger_repeats = finger_repeats_from_file(repeats=reps, layout=layout)

    frep_num = sum([num for num, fing, rep in finger_repeats])
    finger_repeats_top_bottom = finger_repeats_top_and_bottom(finger_repeats, layout=layout)
    frep_num_top_bottom = sum([num for num, fing, rep in finger_repeats_top_bottom])

    # the number of times neighboring fingers are used – weighted by the ease of transition for the respective fingers
    neighboring_fings = neighboring_fingers(repeats=reps, layout=layout)

    # the number of changes between lines on the same hand.
    line_change_same_hand = line_changes(repeats=reps, layout=layout)

    # how often the hand wasn’t switched after an unbalancing key, weighted by the severity of the unbalancing.
    no_switch_after_unbalancing = no_handswitch_after_unbalancing_key(repeats=reps, layout=layout)

    # how often an unbalancing key follows on a neighboring finger. 
    neighboring_unbalance = unbalancing_after_neighboring(repeats=reps, layout=layout)


    # manually defined bad bigrams.
    manual_penalty = manual_bigram_penalty(reps, layout)

    # asymmetric bigrams
    asymmetric_bigrams = asymmetric_bigram_penalty(reps, layout)

    # irregularity # TODO: replace by trigram-based cost of bigrams next to each other: sqrt (sum (bigram_i1 + bigram_i2)² for i in trigrams)
    if WEIGHT_IRREGULARITY_PER_LETTER == 0:
        # avoid very costly checks if not necessary
        check_irregularity = False
    if check_irregularity:
        irregularity_penalty, new_trigram_cost_dic = irregularity_from_trigrams(trigrams, switched_letters=switched_letters, trigram_cost_dic=trigram_cost_dic, layout=layout)
    else:
        irregularity_penalty = 0
        new_trigram_cost_dic = trigram_cost_dic
    

    # add all together and weight them
    total = aggregate_cost(number_of_letters=number_of_letters,
                           position_cost=position_cost,
                           frep_num=frep_num,
                           frep_num_top_bottom=frep_num_top_bottom,
                           neighboring_fings=neighboring_fings,
                           disbalance=disbalance,
                           no_handswitches=no_handswitches,
                           badly_positioned=badly_positioned,
                           asymmetric_similar=asymmetric_similar,
                           line_change_same_hand=line_change_same_hand,
                           no_switch_after_unbalancing=no_switch_after_unbalancing,
                           hand_disbalance=hand_disbalance,
                           manual_penalty=manual_penalty,
                           neighboring_unbalance=neighboring_unbalance,
                           asymmetric_bigrams=asymmetric_bigrams,
                           irregularity_penalty=irregularity_penalty)

    if not return_weighted:
        return total, frep_num, position_cost, new_trigram_cost_dic, frep_num_top_bottom, disbalance, no_handswitches, line_change_same_hand, hand_load, no_switch_after_unbalancing, manual_penalty, neighboring_unbalance, asymmetric_bigrams, asymmetric_similar, irregularity_penalty
    else:
        return total, WEIGHT_FINGER_REPEATS * frep_num, WEIGHT_POSITION * position_cost, new_trigram_cost_dic, WEIGHT_FINGER_REPEATS_TOP_BOTTOM * frep_num_top_bottom, WEIGHT_FINGER_SWITCH * neighboring_fings, WEIGHT_FINGER_DISBALANCE * disbalance, WEIGHT_TOO_LITTLE_HANDSWITCHING * no_handswitches, WEIGHT_XCVZ_ON_BAD_POSITION * number_of_letters * badly_positioned, WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * line_change_same_hand, WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY * no_switch_after_unbalancing, WEIGHT_HAND_DISBALANCE * hand_disbalance * number_of_letters, WEIGHT_MANUAL_BIGRAM_PENALTY * manual_penalty, WEIGHT_NEIGHBORING_UNBALANCE * neighboring_unbalance, WEIGHT_ASYMMETRIC_BIGRAMS * asymmetric_bigrams, WEIGHT_ASYMMETRIC_SIMILAR * number_of_letters * asymmetric_similar, WEIGHT_IRREGULARITY_PER_LETTER * irregularity_penalty, new_trigram_cost_dic


def _test():
    from doctest import testmod
    testmod()

if __name__ == "__main__":
    _test()
