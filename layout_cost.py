#!/usr/bin/env python3
# encoding: utf-8

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
    >>> from check_neo import switch_keys
    >>> lay = switch_keys(["ax"], layout=NEO_LAYOUT)
    >>> key_position_cost_from_file(data[:3], cost_per_key=TEST_COST_PER_KEY, layout=lay)
    20
    >>> data = "UIaĥK\\n"
    >>> key_position_cost_from_file(data, cost_per_key=TEST_COST_PER_KEY, layout=lay)
    240
    """
    if data is not None: 
        letters = letters_in_file(data)
    elif letters is None:
        raise Exception("Need either letters or data")
    letters = split_uppercase_letters(letters, layout=layout)
    cost = 0
    for num, letter in letters:
        pos = find_key(letter, layout=layout)
        if pos is None: # not found
            cost += num * COST_PER_KEY_NOT_FOUND
        # shift, M3 and M4
        elif COST_LAYER_ADDITION[pos[2]:]:
            cost += num * (cost_per_key[pos[0]][pos[1]] + COST_LAYER_ADDITION[pos[2]])
        else:
            # layer has no addition cost ⇒ undefined layer (higher than layer 6!). Just take the base key…
            cost += num * cost_per_key[pos[0]][pos[1]]
    return cost

def key_position_cost_quadratic_bigrams(data=None, bigrams=None, layout=NEO_LAYOUT, cost_per_key=COST_PER_KEY):
    """Count the total cost due to key positions, using the inverse product of the cost in bigrams.

    TODO: Remove. Not useful.

    >>> data = read_file("testfile")
    >>> print(data[:3])
    uia
    >>> key_position_cost_quadratic_bigrams(data[:3], layout=NEO_LAYOUT, cost_per_key=TEST_COST_PER_KEY)
    24
    >>> from check_neo import switch_keys
    >>> lay = switch_keys(["ax"], layout=NEO_LAYOUT)
    >>> key_position_cost_quadratic_bigrams(data[:3], cost_per_key=TEST_COST_PER_KEY, layout=lay)
    51
    >>> lay = switch_keys(["ax", "uq"], layout=NEO_LAYOUT)
    >>> key_position_cost_quadratic_bigrams(data[:3], cost_per_key=TEST_COST_PER_KEY, layout=lay)
    72
    >>> lay = switch_keys(["ax", "iq"], layout=NEO_LAYOUT)
    >>> key_position_cost_quadratic_bigrams(data[:3], cost_per_key=TEST_COST_PER_KEY, layout=lay)
    204
    """
    if data is not None: 
        bigrams = repeats_in_file(data)
    elif bigrams is None:
        raise Exception("Need either bigrams or data")
    bigrams = split_uppercase_repeats(bigrams, layout=layout)
    cost = 0
    for num, bi in bigrams:
        if not bi[1:]:
            continue
        pos0 = find_key(bi[0], layout=layout)
        if pos0 is None: 
            continue
        pos1 = find_key(bi[1], layout=layout)
        if pos1 is None:
            continue
        
        cost0 = 0
        cost1 = 0
        # shift, M3 and M4
        if COST_LAYER_ADDITION[pos0[2]:]:
            cost0 += COST_LAYER_ADDITION[pos0[2]]
        if COST_LAYER_ADDITION[pos1[2]:]:
            cost1 += COST_LAYER_ADDITION[pos1[2]]

        cost0 += cost_per_key[pos0[0]][pos0[1]]
        cost1 += cost_per_key[pos1[0]][pos1[1]]

        # add the product of both costs as final cost. 5,3 → (5+3)/5·3 = 8/15; 4,4 → (4+4)/4·4 = 8/16; 5,4 → 9/20; 5,1 → 5/5
        cost += num*cost0*cost1
        
    return cost #* sum([num for num, bi in bigrams])

def finger_repeats_from_file(data=None, repeats=None, count_same_key=False, layout=NEO_LAYOUT):
    """Get a list of two char strings from the file, which repeat the same finger.

    >>> data = read_file("testfile")
    >>> finger_repeats_from_file(data, layout=NEO_LAYOUT)
    [(1, 'Mittel_R', 'rg'), (1, 'Zeige_L', 'eo'), (1, 'Klein_R', 'd\\n')]
    >>> finger_repeats_from_file(data, count_same_key=True, layout=NEO_LAYOUT)
    [(2, 'Mittel_L', 'aa'), (1, 'Mittel_R', 'rg'), (1, 'Zeige_L', 'eo'), (1, 'Klein_R', 'd\\n'), (1, 'Mittel_L', 'aa'), (1, 'Mittel_L', 'aa')]
    >>> data = "xülävöcpwzoxkjhbmg,qjf.ẞxXkKzZß"
    >>> finger_repeats_from_file(data, layout=NEO_LAYOUT)
    [(1, 'Klein_L', '⇧x'), (1, 'Klein_R', '⇗ß'), (1, 'Zeige_L', 'zo'), (1, 'Klein_L', 'xü'), (1, 'Zeige_L', 'wz'), (1, 'Ring_L', 'vö'), (1, 'Klein_R', 'qj'), (1, 'Zeige_L', 'pw'), (1, 'Mittel_L', 'lä'), (1, 'Zeige_R', 'hb'), (1, 'Mittel_R', 'g,'), (1, 'Ring_R', 'f.'), (1, 'Zeige_L', 'cp'), (1, 'Zeige_R', 'bm')]
    """
    if data is not None: 
        repeats = repeats_in_file(data)
        repeats = split_uppercase_repeats(repeats, layout=layout)
    elif repeats is None:
        raise Exception("Need either repeats or data")

    
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

def _rep_to_fingtuple(num, rep, layout, finger_switch_cost):
    """Turn a repeat and occurance number into num and a fingtuple."""
    finger1 = key_to_finger(rep[0], layout=layout)
    if not finger1 or not finger1 in finger_switch_cost:
        return None, None
    finger2 = key_to_finger(rep[1], layout=layout)
    if not finger2 or not finger2 in finger_switch_cost[finger1]:
        return None, None
    return num, (finger1, finger2)

def movement_pattern_cost(data=None, repeats=None, layout=NEO_LAYOUT, FINGER_SWITCH_COST=FINGER_SWITCH_COST):
    """Calculate a movement cost based on the FINGER_SWITCH_COST. 

    >>> data = read_file("testfile")
    >>> print(data)
    uiaenrtAaAa
    eod
    rg
    aa
    <BLANKLINE>
    >>> neighboring_fingers(data, FINGER_SWITCH_COST=TEST_FINGER_SWITCH_COST)
    16
    """
    if data is not None: 
        repeats = repeats_in_file(data)
        repeats = split_uppercase_repeats(repeats, layout=layout)
    elif repeats is None:
        raise Exception("Need either repeats or data")

    fingtups = (_rep_to_fingtuple(num, rep, layout, FINGER_SWITCH_COST) for num, rep in repeats)

    return sum((num*FINGER_SWITCH_COST[fings[0]][fings[1]] for num, fings in fingtups if num))

neighboring_fingers = movement_pattern_cost

def no_handswitch_after_unbalancing_key(data=None, repeats=None, layout=NEO_LAYOUT):
    """Check how often we have no handswitching after an unbalancing key, weighted by the severity of the unbalancing. This also helps avoiding a handswitch directly after an uppercase key (because shift severly unbalances und with the handswitch we’d effectively have no handswitch after the shift (kind of a shift collision, too). 

    >>> data = read_file("testfile")
    >>> no_handswitch_after_unbalancing_key(data)
    2
    >>> reps =  [(3, "Ab")]
    >>> reps = split_uppercase_repeats(reps, layout=QWERTZ_LAYOUT)
    >>> no_handswitch_after_unbalancing_key(repeats=reps)
    6
    >>> no_handswitch_after_unbalancing_key(repeats=reps, layout=QWERTZ_LAYOUT)
    0
    >>> reps = [(3, "Ga")]
    >>> reps = split_uppercase_repeats(reps, layout=QWERTZ_LAYOUT)
    >>> no_handswitch_after_unbalancing_key(repeats=reps, layout=QWERTZ_LAYOUT)
    3
    """
    if data is not None: 
        repeats = repeats_in_file(data)
        repeats = split_uppercase_repeats(repeats, layout=layout)
    elif repeats is None:
        raise Exception("Need either repeats or data")

    no_switch = 0
    for number, pair in repeats:
        pos1 = find_key(pair[0], layout=layout)
        if not pos1 or not pos1 in UNBALANCING_POSITIONS:
            continue
        pos2 = find_key(pair[1], layout=layout)
        if pos2:
                # check if we”re on the same hand
                is_left1 = pos_is_left(pos1)
                is_left2 = pos_is_left(pos2)
                if is_left1 == is_left2:
                    # using .get here, because most positions aren’t unbalancing.
                    no_switch += UNBALANCING_POSITIONS.get(pos1, 0)*number
    return no_switch

def line_changes(data=None, repeats=None, layout=NEO_LAYOUT):
    """Get the number of (line changes divided by the horizontal distance) squared: (rows²/dist)².

    TODO: Don’t care about the hand (left index low and right high is still not nice). 

    >>> data = read_file("testfile")
    >>> line_changes(data)
    16.29
    """
    if data is not None: 
        repeats = repeats_in_file(data)
        repeats = split_uppercase_repeats(repeats, layout=layout)
    elif repeats is None:
        raise Exception("Need either repeats or data")
    

    line_changes = 0
    for number, pair in repeats:
        # ignore pairs with spaces (" "): Space is hit with the thumb, so it is no real row jump.
        if " " in pair:
            continue
        key1 = pair[0]
        key2 = pair[1]
        pos1 = find_key(key1, layout=layout)
        pos2 = find_key(key2, layout=layout)
        if pos1 and pos2:
            if not WEIGHT_COUNT_ROW_CHANGES_BETWEEN_HANDS: 
                # check if we”re on the same hand
                is_left1 = pos_is_left(pos1)
                is_left2 = pos_is_left(pos2)
                if is_left1 != is_left2:
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

    >>> letters = [(1, "u"), (5, "i"), (10, "2"), (3, " "), (4, "A"), (6, "Δ")]
    >>> load_per_finger(letters)
    {'': 10, 'Ring_L': 5, 'Klein_L': 7, 'Mittel_L': 4, 'Klein_R': 10, 'Daumen_L': 3}
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
    [6, 2]
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
    from math import sqrt
    return sqrt(var)

def finger_balance(letters, layout=NEO_LAYOUT, intended_balance=WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY):
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
    for key in abc_full:
        #without "⇧⇗ " -> too many false positives when we include the shifts. This also gets rid of anything with uppercase letters in it.
        finger = key_to_finger(key, layout=layout)
        if finger and not finger[:6] == "Daumen":
            if finger[-1] == "L": 
                key_hand_table[key] = False
            elif finger[-1] == "R":
                key_hand_table[key] = True
            # with this, not found is ignored.

    key_pos_horizontal_table = {}
    for key in abc_full:
        #without "⇧⇗ " -> too many false positives when we include the shifts. This also gets rid of anything with uppercase letters in it.
        pos = find_key(key, layout=layout)
        try: 
            key_pos_horizontal_table[key] = pos[1]
        except TypeError:
            pass # not found. Ignore as above.
    return key_hand_table, key_pos_horizontal_table


def _no_handswitching(trigrams, key_hand_table, key_pos_horizontal_table, WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE, WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM):
    """Do the hard work for no_handswitching without any call to outer functions.
    >>> trigs = [(1, "nrt"), (5, "ige"), (3, "udi"), (2, "ntr")]
    >>> key_hand_table, key_pos_horizontal_table = _trigram_key_tables(trigs, layout=NEO_LAYOUT)
    >>> _no_handswitching(trigs, key_hand_table, key_pos_horizontal_table, WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE, TEST_WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM)
    (2, [(1.5, 'ui'), (2.5, 'ie')])
    """
    no_switch = 0
    secondary_bigrams = {} # {bigram: num, …}
    for num, trig in trigrams:
        # if one of the trigs is not in the key_hand_table, we don’t count the trigram.
        if not trig[0] in key_hand_table or not trig[1] in key_hand_table or not trig[2] in key_hand_table:
            continue
        hand0 = key_hand_table[trig[0]]
        hand1 = key_hand_table[trig[1]]
        hand2 = key_hand_table[trig[2]]
        if hand0 is hand1 and hand1 is hand2:
            pos0 = key_pos_horizontal_table[trig[0]]
            pos1 = key_pos_horizontal_table[trig[1]]
            pos2 = key_pos_horizontal_table[trig[2]]
            if pos0 > pos1 and pos1 < pos2 or pos0 < pos1 and pos1 > pos2:
                no_switch += num * WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE
            else: 
                no_switch += num * WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE
        # Add bigram cost key 1 and key 3 if there are two handswitches; reduce via a multiplier < 1.0 ; Faktor könnte vom Tippaufwand der mittleren Taste abhängen: Je besser oder schneller die mittlere Taste getippt werden kann, desto grösser der Faktor. Das ist aber vermutlich nur eine unnötige Komplikation.
        elif hand0 is hand2 and hand0 is not hand1:
            bi = trig[0]+trig[2]
            try:
                secondary_bigrams[bi] += num * WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM
            except KeyError: secondary_bigrams[bi] = num * WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM

    return no_switch, [(num, bi) for bi, num in secondary_bigrams.items()]
    

def no_handswitching(trigrams, layout=NEO_LAYOUT):
    """Add a penalty when the hands aren’t switched at least once in every three letters. Doesn’t take any uppercase trigrams into account.

    If there also is a direction change in the trigram, the number of times it occurs gets multiplied by WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE.

    If there is no direction change, it gets multiplied with WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE. If that is 0, handswitches without direction change are ignored.

    (TODO? WEIGHT_TRIGRAM_FINGER_REPEAT_WITHOUT_KEY_REPEAT)

    TODO: Include the shifts again and split per keyboard. If we did it now, the layout would get optimized for switching after every uppercase letter (as any trigram with a shift and two letters on the same hand would be counted as half a trigram without handswitching). The effect is that it ignores about 7-9% of the trigrams. 

    >>> trigs = [(1, "nrt"), (5, "ige"), (3, "udi"), (2, "ntr")]
    >>> no_handswitching(trigs, layout=NEO_LAYOUT)[0]
    2
    >>> no_handswitching(trigs, layout=NEO_LAYOUT)[1][0][1]
    'ui'
    """
    key_hand_table, key_pos_horizontal_table = _trigram_key_tables(trigrams, layout=layout)
    return _no_handswitching(trigrams, key_hand_table, key_pos_horizontal_table, WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE, WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM)


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
        letters = letters_in_file(data)
        repeats = repeats_in_file(data)
        trigrams = trigrams_in_file(data)
        # first split uppercase repeats *here*, so we don’t have to do it in each function.
        reps = split_uppercase_repeats(repeats, layout=layout)
        
    elif letters is None or repeats is None:
        raise Exception("Need either repeats and letters or data")
    else:
        # first split uppercase repeats *here*, so we don’t have to do it in each function.
        reps = split_uppercase_repeats(repeats, layout=layout)

    no_handswitches, secondary_bigrams = no_handswitching(trigrams, layout=layout)
    reps.extend(secondary_bigrams)

    finger_repeats = finger_repeats_from_file(repeats=reps, layout=layout)
    position_cost = key_position_cost_from_file(letters=letters, layout=layout, cost_per_key=cost_per_key)
    position_cost_quadratic_bigrams = key_position_cost_quadratic_bigrams(bigrams=repeats, layout=layout, cost_per_key=cost_per_key)

    frep_num = sum([num for num, fing, rep in finger_repeats])
    finger_repeats_top_bottom = finger_repeats_top_and_bottom(finger_repeats, layout=layout)
    frep_num_top_bottom = sum([num for num, fing, rep in finger_repeats_top_bottom])

    # the number of times neighboring fingers are used – weighted by the ease of transition for the respective fingers
    neighboring_fings = neighboring_fingers(repeats=reps, layout=layout)

    # the number of changes between lines on the same hand.
    line_change_same_hand = line_changes(repeats=reps, layout=layout)

    # how often the hand wasn’t switched after an unbalancing key, weighted by the severity of the unbalancing.
    no_switch_after_unbalancing = no_handswitch_after_unbalancing_key(repeats=reps, layout=layout)

    # the balance between fingers
    disbalance = finger_balance(letters, layout=layout, intended_balance=intended_balance)
    number_of_letters = sum([i for i, s in letters])

    # the position of the keys xcvz - penalty if they are not among the first 5 keys, counted from left, horizontally.
    badly_positioned = badly_positioned_shortcut_keys(layout=layout)

    # the load distribution on the hands: [left keystrokes, right keystrokes]
    hand_load = load_per_hand(letters, layout=layout)
    # the disbalance between the hands. Keystrokes of the left / total strokes - 0.5. From 0 to 0.5, ignoring the direction.
    hand_disbalance = abs(hand_load[0]/max(1, sum(hand_load)) - 0.5)

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
    total += WEIGHT_HAND_DISBALANCE * hand_disbalance * number_of_letters
    total += WEIGHT_POSITION_QUADRATIC_BIGRAMS * position_cost_quadratic_bigrams

    if not return_weighted: 
        return total, frep_num, position_cost, frep_num_top_bottom, disbalance, no_handswitches, line_change_same_hand, hand_load
    else:
        return total, WEIGHT_POSITION * position_cost, WEIGHT_FINGER_REPEATS * frep_num, WEIGHT_FINGER_REPEATS_TOP_BOTTOM * frep_num_top_bottom, WEIGHT_FINGER_SWITCH * neighboring_fings, WEIGHT_FINGER_DISBALANCE * disbalance, WEIGHT_TOO_LITTLE_HANDSWITCHING * no_handswitches, WEIGHT_XCVZ_ON_BAD_POSITION * number_of_letters * badly_positioned, WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * line_change_same_hand, WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY * no_switch_after_unbalancing, WEIGHT_HAND_DISBALANCE * hand_disbalance * number_of_letters, WEIGHT_POSITION_QUADRATIC_BIGRAMS * position_cost_quadratic_bigrams


def _test():
    from doctest import testmod
    testmod()

if __name__ == "__main__":
    _test()
