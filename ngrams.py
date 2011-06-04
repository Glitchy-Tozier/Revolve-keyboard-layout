#!/usr/bin/env python3
# encoding: utf-8

"""Calculating ngram distributions (letters, bigrams, trigrams) from text or getting them from precomputed files."""

from layout_base import NEO_LAYOUT, read_file, find_key, get_key, MODIFIERS_PER_LAYER, KEY_TO_FINGER, pos_is_left, get_all_keys_in_layout

def split_uppercase_repeats(reps, layout=NEO_LAYOUT):
    """Split bigrams with uppercase letters (or others with any mod) into several lowercase bigrams by adding bigrams with mods and the base key. 

    TODO: aB should be counted about 2x, Ab only 0.5 times, because shift is pressed and released a short time before the key is. 

        Ab -> shift-a, shift-b, a-b.
        aB -> a-shift, shift-b, a-b.
        AB -> shift-a, shift-b, a-b, 0.5*(shift_L-shift_R, shift_R-shift_L)
        (a -> mod3-n, mod3-a, n-a.
        () -> mod3L-n, mod3L-r, n-r, 0.5*(mod3L-mod3L, mod3L-mod3L)
        (} -> mod3L-n, mod3R-e, n-e, 0.5*(mod3L-mod3R, mod3R-mod3L)
        ∃ℕ -> mod3R-e, mod4R-e, mod3L-n, mod4L-n,
              mod3R-n, mod4R-n, e-mod3L, e-mod4L,
              mod3R-mod3L, mod3R-mod4L, mod4R-mod3L, mod4R-mod4L,
              0.5*(mod3R-mod4R, mod4R-mod3R, mod3L-mod4L, mod4L-mod3L)

        Ψ∃: 

            # Modifiers from different keys
            '⇩⇙', M3L + M4R
            '⇩⇘', M3L + M3R
            '⇚⇙', M4L + M4R # TODO: M4L is hit with the ringfinger, here. Take that into account.
            '⇚⇘', M4L + M3R # TODO: M4L is hit with the ringfinger, here. Take that into account.

            # The different Modifiers of one of the keys with each other
            # sorted – should that be (m3-m4, m4-m3)/64?
            '⇩⇚', M3L + M4L / 32 (because this mistakenly gives a finger repeat, since we can’t yet simulate hitting M4 with the ringfinger and M3 with the pinky. # TODO: M4L is hit with the ringfinger, here. Take that into account.
            '⇘⇙', M3R + M4R / 32
            
            # Modifiers with the corresponding base keys
            '⇩h', M3L + h
            '⇚h', M4L + h
            '⇙e', M4R + e
            '⇘e', M3R + e
            
            # Modifiers with the other base key
            '⇩e', shiftL + e
            '⇚e', M4L + e # TODO: M4L is hit with the ringfinger, here. Take that into account.
            'h⇙', h + M4R
            'h⇘', h + M3R
            
            # The base keys on the base layer
            'he'
    
    >>> reps = [(36, "ab"), (24, "Ab"), (16, "aB"), (10, "AB"), (6, "¾2"), (4, "(}"), (2, "Ψ∃"), (1, "q")]
    >>> split_uppercase_repeats(reps)
    [(36, 'ab'), (24, '⇗b'), (24, '⇗a'), (24, 'ab'), (16, '⇧b'), (16, 'a⇧'), (16, 'ab'), (10, '⇧b'), (10, '⇗⇧'), (10, '⇗b'), (10, '⇗a'), (10, 'a⇧'), (10, 'ab'), (6, '¾2'), (4, '⇩⇘'), (4, '⇩n'), (4, '⇩e'), (4, '⇘e'), (4, 'n⇘'), (4, 'ne'), (2, '⇩⇚'), (2, '⇩⇙'), (2, '⇩⇘'), (2, '⇩h'), (2, '⇩e'), (2, '⇚⇙'), (2, '⇚⇘'), (2, '⇚h'), (2, '⇚e'), (2, '⇙e'), (2, '⇘⇙'), (2, '⇘e'), (2, 'h⇙'), (2, 'h⇘'), (2, 'he')]
    >>> reps = [(1, ", ")]
    >>> from layout_base import string_to_layout
    >>> layout = string_to_layout("äuobp kglmfx+\\naietc hdnrsß\\n⇚.,üpö qyzwv", base_layout=NEO_LAYOUT)
    >>> split_uppercase_repeats(reps, layout=layout)
    [(1, ', ')]
    """
    # replace uppercase by ⇧ + char1 and char1 + char2 and ⇧ + char2
    # char1 and shift are pressed at the same time
    mods = MODIFIERS_PER_LAYER
    #: Adjustment of the weight of two modifiers on the same hand, because we can’t yet simulate moving the hand to use a different finger for M4/M3 when the pinky is needed on M3/shift. 2 * WEIGHT_FINGER_REPEATS * mods_on_same_hand_adjustment should be lower than (COST_PER_KEY_NOT_FOUND - max(COST_LAYER_ADDITION) - the most expensive key), because a key with M3-shift brings 2 finger repeats: one as first part in a bigram and the second as second part. 
    mods_on_same_hand_adjustment = 1/32
    #: The resulting bigrams after splitting.
    repeats = {}
    for num, rep in reps:
        try: 
            pos1 = find_key(rep[0], layout=layout)
            pos2 = find_key(rep[1], layout=layout)
        except IndexError:
            # this is no repeat but at most a single key.
            continue
        # if any key isn’t found, the repeat doesn’t need splitting.
        # same is true if all keys are layer 0. 
        if pos1 is None or pos2 is None or (not pos1[2] and not pos2[2]):
            try: repeats[rep] += num
            except KeyError: repeats[rep] = num
            continue # caught all lowercase repeats and all for which one key isn’t in the layout. We don’t need to change anything for these.

        # now get the base keys.
        base1 = get_key(pos1[:2] + (0, ), layout=layout)
        base2 = get_key(pos2[:2] + (0, ), layout=layout)

        # add the base keys as repeat
        try: repeats[base1+base2] += num
        except KeyError: repeats[base1+base2] = num

        # now check for the mods which are needed to get the key
        # if the pos is left, we need the modifiers on the right.
        if pos_is_left(pos1):
            mods1 = mods[pos1[2]][1]
        else:
            mods1 = mods[pos1[2]][0]
        if pos_is_left(pos2): 
            mods2 = mods[pos2[2]][1]
        else:
            mods2 = mods[pos2[2]][0]

        # now we have the mods, so we do the splitting by mods.
        for m1 in mods1:
            # each of the mods with the key itself
            try: repeats[m1+base1] += num
            except KeyError: repeats[m1+base1] = num
            # each mod of the first with each mod of the second
            for m2 in mods2:
                try: repeats[m1+m2] += num
                except KeyError: repeats[m1+m2] = num
            # each of the first mods with the second base key
            ## TODO: counted only 0.5 as strong, because the mod is normally hit and released short before the key is.
            try: repeats[m1+base2] += num # TODO: ((int(0.5*num), m1+base2))
            except KeyError: repeats[m1+base2] = num 

        # the first base key with the second mods.
        ## TODO: counted 2x as strong, because the mod is normally hit and released short before the key is.
        for m2 in mods2:
            try: repeats[base1+m2] += num # TODO: ((2*num, base1+m2))
            except KeyError: repeats[base1+m2] = num
            # also the second mod with the second base key
            try: repeats[m2+base2] += num
            except KeyError: repeats[m2+base2] = num

        # the mods of the first with each other
        # 0123 → 01 02 03 12 13 23
        if mods1[1:]: 
            for i in range(len(mods1)):
                for m2 in mods1[i+1:]:
                    try: repeats[mods1[i]+m2] += num*mods_on_same_hand_adjustment
                    except KeyError: repeats[mods1[i]+m2] = num*mods_on_same_hand_adjustment

        # the mods of the second with each other
        # 0123 → 01 02 03 12 13 23
        if mods2[1:]: 
            for i in range(len(mods2)):
                for m2 in mods2[i+1:]:
                    try: repeats[mods2[i]+m2] += num*mods_on_same_hand_adjustment
                    except KeyError: repeats[mods2[i]+m2] = num*mods_on_same_hand_adjustment

    return repeats
    #reps = [(num, rep) for rep, num in repeats.items()]
    #reps.sort()
    #reps.reverse()
    #return reps

def repeats_in_file(data):
    """Sort the repeats in a file by the number of occurrances.

    >>> data = read_file("testfile")
    >>> repeats_in_file(data)[:3]
    [(2, 'a\\n'), (2, 'Aa'), (1, 'ui')]
    """
    repeats = {}
    for i in range(len(data)-1):
        rep = data[i] + data[i+1]
        try:
            repeats[rep] += 1
        except KeyError:
            repeats[rep] = 1
    sorted_repeats = [(repeats[i], i) for i in repeats]
    sorted_repeats.sort()
    sorted_repeats.reverse()
    #reps = split_uppercase_repeats(sorted_repeats) # wrong place
    return sorted_repeats

def split_uppercase_letters(reps, layout):
    """Split uppercase letters (or others with any mod) into two lowercase letters (with the mod).

    >>> letters = [(4, "a"), (3, "A")]
    >>> split_uppercase_letters(letters, layout=NEO_LAYOUT)
    [(4, 'a'), (3, '⇗'), (3, 'a')]
    """
    # replace uppercase by ⇧ and char1
    upper = []
    repeats = []
    for num, rep in reps:
        pos = find_key(rep, layout=layout)
        if pos and pos[2]:
            upper.append((num, rep, pos))
        else:
            repeats.append((num, rep))
    reps = repeats

    up = []
    
    for num, rep, pos in upper:
        layer_mods = MODIFIERS_PER_LAYER[pos[2]]
                                         
        if pos_is_left(pos):
            for m in layer_mods[1]: # left keys use the right mods
                up.append((num, m)) 
        else:
            for m in layer_mods[0]:  # right keys use the left mods
                up.append((num, m))

        # also append the base layer key.
        up.append((num,
                   get_key((pos[0], pos[1], 0), layout=layout)))
                
    reps.extend(up)
    reps = [(int(num), r) for num, r in reps]
    reps.sort()
    reps.reverse()
    return reps

def letters_in_file(data):
    """Sort the repeats in a file by the number of occurrances.

    >>> data = read_file("testfile")
    >>> letters_in_file(data)[:3]
    [(5, 'a'), (4, '\\n'), (2, 'r')]
    """
    letters = {}
    for letter in data:
        if letter in letters:
            letters[letter] += 1
        else:
            letters[letter] = 1
    sort = [(letters[i], i) for i in letters]
    sort.sort()
    sort.reverse()
    return sort

def unique_sort(liste):
    """Count the occurrence of each item in a list.

    >>> unique_sort([1, 2, 1])
    [(1, 2), (2, 1)]
    """
    counter = {}
    for i in liste:
        if i in counter:
            counter[i] += 1
        else:
            counter[i] = 1

    sorted_repeats = [(counter[i], i) for i in counter]
    sorted_repeats.sort()
    return sorted_repeats   

def repeats_in_file_sorted(data):
    """Sort the repeats in a file by the number of occurrances.

    >>> data = read_file("testfile")
    >>> repeats_in_file_sorted(data)[:2]
    [(1, '\\na'), (1, '\\ne')]
    """
    repeats = repeats_in_file(data)
    repeats.reverse()
    return repeats

def _unescape_ngram_list(ngrams): 
    """unescape \n and \ in an ngram list."""
    for i in range(len(ngrams)):
        if "\\" in ngrams[i][1]: 
            ngrams[i] = (ngrams[i][0], ngrams[i][1].replace("\\\\", "\\"))
            ngrams[i] = (ngrams[i][0], ngrams[i][1].replace("\\n", "\n"))
    return ngrams
                  


def repeats_in_file_precalculated(data, only_existing=True):
    """Get the repeats from a precalculated file.

    >>> data = read_file("2gramme.txt")
    >>> repeats_in_file_precalculated(data)[:3]
    [(10159250, 'en'), (10024681, 'er'), (9051717, 'n ')]
    """
    reps = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.lstrip().split(" ", 1)[1:]]
    if only_existing: 
        all_keys = get_all_keys_in_layout(NEO_LAYOUT)
        reps = [(int(num), r) for num, r in reps if r[1:] and r[0] in all_keys and r[1] in all_keys]
    else:
        reps = [(int(num), r) for num, r in reps if r[1:]]

    # cleanup
    _unescape_ngram_list(reps)

    return reps


def split_uppercase_trigrams(trigs):
    """Split uppercase repeats into two to three lowercase repeats.

    Here we don’t care about shift-collisions with the “second” letter, because we only use it for handswitching and the shift will always mean a handswitch afterwards (opposing shift). ⇒ Ab → Sh-ab, ignoring a-Sh-b. ⇒ for handswitching ignore trigrams with any of the shifts. 

    >>> trigs = [(8, "abc"), (7, "Abc"), (6, "aBc"), (5, "abC"), (4, "ABc"), (3, "aBC"), (2, "AbC"), (1, "ABC")]
    >>> split_uppercase_trigrams(trigs)
    [(8, 'abc'), (7, 'abc'), (3, '⇧bc'), (3, '⇧ab'), (3, '⇗bc'), (3, '⇗ab'), (3, 'a⇧b'), (3, 'a⇗b'), (2, '⇧bc'), (2, '⇗bc'), (2, 'b⇧c'), (2, 'b⇗c'), (2, 'a⇧b'), (2, 'a⇗b'), (2, 'ab⇧'), (2, 'ab⇗'), (1, '⇧b⇧'), (1, '⇧b⇧'), (1, '⇧b⇗'), (1, '⇧b⇗'), (1, '⇧a⇧'), (1, '⇧a⇧'), (1, '⇧a⇗'), (1, '⇧a⇗'), (1, '⇧ab'), (1, '⇗b⇧'), (1, '⇗b⇧'), (1, '⇗b⇗'), (1, '⇗b⇗'), (1, '⇗a⇧'), (1, '⇗a⇧'), (1, '⇗a⇗'), (1, '⇗a⇗'), (1, '⇗ab'), (1, 'b⇧c'), (1, 'b⇧c'), (1, 'b⇧c'), (1, 'b⇗c'), (1, 'b⇗c'), (1, 'b⇗c'), (1, 'a⇧b'), (1, 'a⇧b'), (1, 'a⇗b'), (1, 'a⇗b'), (1, 'ab⇧'), (1, 'ab⇗')]
    >>> #[(8, 'abc'), (7, '⇧ab'), (7, 'abc'), (6, '⇧bc'), (6, 'a⇧b'), (5, 'b⇧c'), (5, 'ab⇧'), (4, '⇧a⇧'), (4, 'a⇧b'), (4, '⇧bc'), (3, 'a⇧b'), (3, '⇧b⇧'), (3, 'b⇧c'), (2, '⇧ab'), (2, 'ab⇧'), (2, 'b⇧c'), (1, '⇧a⇧'), (1, 'a⇧b'), (1, '⇧b⇧'), (1, 'b⇧c')]
    """
    # replace uppercase by ⇧ + char1 and char1 + char2
    upper = [(num, trig) for num, trig in trigs if not trig == trig.lower() and trig[2:]]
    # and remove them temporarily from the list of trigrams - don’t compare list with list, else this takes ~20min!
    trigs = [(num, trig) for num, trig in trigs if trig == trig.lower() and trig[2:]]
    up = []
    # since this gets a bit more complex and the chance to err is high,
    # we do this dumbly, just checking for the exact cases.
    # TODO: Do it more elegantly: Replace every uppercase letter by "⇧"+lowercase
    #       and then turn the x-gram into multiple 3grams (four[:-1], four[1:]; five… ).
    for num, trig in upper: 
        # Abc
        if not trig[0] == trig[0].lower() and trig[1] == trig[1].lower() and trig[2] == trig[2].lower():
            up.append((max(1, num//2), "⇧"+trig[:2].lower()))
            up.append((max(1, num//2), "⇗"+trig[:2].lower()))
            up.append((num, trig.lower()))
        # aBc
        elif trig[0] == trig[0].lower() and not trig[1] == trig[1].lower() and trig[2] == trig[2].lower():
            up.append((max(1, num//2), "⇧"+trig[1:].lower()))
            up.append((max(1, num//2), "⇗"+trig[1:].lower()))
            up.append((max(1, num//2), trig[0].lower()+"⇧"+trig[1].lower()))
            up.append((max(1, num//2), trig[0].lower()+"⇗"+trig[1].lower()))
            
        # abC
        elif trig[0] == trig[0].lower() and trig[1] == trig[1].lower() and not trig[2] == trig[2].lower():
            up.append((max(1, num//2), trig[:2].lower() + "⇧"))
            up.append((max(1, num//2), trig[:2].lower() + "⇗"))
            up.append((max(1, num//2), trig[1].lower()+"⇧"+trig[2].lower()))
            up.append((max(1, num//2), trig[1].lower()+"⇗"+trig[2].lower()))
            
        # ABc (4, '⇧a⇧'), (4, 'a⇧b'), (4, '⇧bc')
        elif not trig[0] == trig[0].lower() and not trig[1] == trig[1].lower() and trig[2] == trig[2].lower():
            up.append((max(1, num//4), "⇧"+trig[0].lower()+"⇧"))
            up.append((max(1, num//2), trig[0].lower()+"⇧"+trig[1].lower()))
            up.append((max(1, num//2),  "⇧" + trig[1:].lower()))
            
            up.append((max(1, num//4), "⇗"+trig[0].lower()+"⇧"))
            up.append((max(1, num//4), "⇧"+trig[0].lower()+"⇗"))
            up.append((max(1, num//4), "⇗"+trig[0].lower()+"⇗"))

            up.append((max(1, num//2), trig[0].lower()+"⇗"+trig[1].lower()))
            up.append((max(1, num//2),  "⇗" + trig[1:].lower()))
            
        # aBC (3, 'a⇧b'), (3, '⇧b⇧'), (3, 'b⇧c')
        elif trig[0] == trig[0].lower() and not trig[1] == trig[1].lower() and not trig[2] == trig[2].lower():
            up.append((max(1, num//4), "⇧"+trig[1].lower()+"⇧"))
            up.append((max(1, num//2), trig[0].lower()+"⇧"+trig[1].lower()))
            up.append((max(1, num//2), trig[1].lower()+"⇧"+trig[2].lower()))
            
            up.append((max(1, num//4), "⇗"+trig[1].lower()+"⇧"))
            up.append((max(1, num//4), "⇧"+trig[1].lower()+"⇗"))
            up.append((max(1, num//4), "⇗"+trig[1].lower()+"⇗"))

            up.append((max(1, num//2), trig[0].lower()+"⇗"+trig[1].lower()))
            up.append((max(1, num//2), trig[1].lower()+"⇗"+trig[2].lower()))
            
        # AbC (2, '⇧ab'), (2, 'ab⇧'), (2, 'b⇧c')
        elif not trig[0] == trig[0].lower() and trig[1] == trig[1].lower() and not trig[2] == trig[2].lower():
            up.append((max(1, num//2),  "⇧" + trig[:2].lower()))
            up.append((max(1, num//2),  trig[:2].lower() + "⇧"))
            up.append((max(1, num//2), trig[1].lower()+"⇧"+trig[2].lower()))
            
            up.append((max(1, num//2),  "⇗" + trig[:2].lower()))
            up.append((max(1, num//2),  trig[:2].lower() + "⇗"))
            up.append((max(1, num//2), trig[1].lower()+"⇗"+trig[2].lower()))

        # ABC (1, '⇧a⇧'), (1, 'a⇧b'), (1, '⇧b⇧'), (1, 'b⇧c')
        elif not trig[0] == trig[0].lower() and not trig[1] == trig[1].lower() and not trig[2] == trig[2].lower():
            up.append((max(1, num//4), "⇧"+trig[0].lower()+"⇧"))
            up.append((max(1, num//2), trig[0].lower()+"⇧"+trig[1].lower()))
            up.append((max(1, num//4), "⇧"+trig[1].lower()+"⇧"))
            up.append((max(1, num//2), trig[1].lower()+"⇧"+trig[2].lower()))
            
            up.append((max(1, num//4), "⇗"+trig[0].lower()+"⇧"))
            up.append((max(1, num//4), "⇧"+trig[0].lower()+"⇗"))
            up.append((max(1, num//4), "⇗"+trig[0].lower()+"⇗"))

            up.append((max(1, num//4), "⇗"+trig[1].lower()+"⇧"))
            up.append((max(1, num//4), "⇧"+trig[1].lower()+"⇗"))
            up.append((max(1, num//4), "⇗"+trig[1].lower()+"⇗"))

            up.append((max(1, num//2), trig[0].lower()+"⇗"+trig[1].lower()))
            up.append((max(1, num//2), trig[1].lower()+"⇗"+trig[2].lower()))

    
    trigs.extend(up)
    trigs = [(num, r) for num, r in trigs if r[1:]]
    t = {}
    for num, r in trigs:
        try: t[r] += num
        except KeyError: t[r] = num
    trigs = [(num, r) for r, num in t.items()]
    trigs.sort()
    trigs.reverse()
    return trigs


def split_uppercase_trigrams_correctly(trigs, layout, just_record_the_mod_key=False):
    """Split uppercase repeats into two to three lowercase repeats.

    Definition: 

        a → b → c
        | × | × |
        sa→ sb→ sc
        senkrechte nur nach oben. Kreuze und Pfeile nur nach vorne. Alle Trigramme, die du aus dem Bild basteln kannst.

    >>> trigs = [(8, "abc"), (7, "∀bC"), (6, "aBc"), (5, "abC"), (4, "ABc"), (3, "aBC"), (2, "AbC"), (1, "ABC")]
    >>> split_uppercase_trigrams_correctly(trigs, NEO_LAYOUT)
    """
    # kick out any who don’t have a position
    pos_trig = [(num, [find_key(k, layout=layout) for k in trig], trig) for num, trig in trigs]
    pos_trig = [(num, pos, trig) for num, pos, trig in pos_trig if not None in pos]
    
    # get all trigrams with non-baselayer-keys
    upper = [(num, pos, trig) for num, pos, trig in pos_trig if True in [p[2]>0 for p in pos]]
    # and remove them temporarily from the list of trigrams - don’t compare list with list, else this takes ~20min!
    trigs = [(num, trig) for num, pos, trig in pos_trig if not True in [p[2]>0 for p in pos]]

    #: The trigrams to add to the baselayer trigrams
    up = []

    mod = MODIFIERS_PER_LAYER
    for num, pos, trig in upper:
        print(trig)
        # lower letters
        l0 = get_key((pos[0][0], pos[0][1], 0), layout=layout)
        l1 = get_key((pos[1][0], pos[1][1], 0), layout=layout)
        l2 = get_key((pos[2][0], pos[2][1], 0), layout=layout)
        # mods
        m0 = mod[pos[0][2]]
        m1 = mod[pos[1][2]]
        m2 = mod[pos[2][2]]
        ### Algorithm
        algo = """
        a → b → c
        | × | × |
        sa→ sb→ sc
        | × | × |   ; seperate dimension. ma is connected to a and sa.
        ma→ mb→ mc
        """
        #: Matrix der Tasten und Modifikatoren
        m = []
        for p, c in zip(pos, (l0, l1, l2)):
            mx = mod[p[2]] # liste mit bis zu 2 mods
            if just_record_the_mod_key:
                mx = [i+c for i in mx[0]]
            elif pos_is_left(p):
                mx = mx[1]
            else: mx = mx[0]
            col = [c]
            if mx: 
                col.append(mx[0])
            else: col.append(None)
            if mx[1:]: 
                col.append(mx[1])
            else: col.append(None)
            m.append(col)

        # Matrix created
        #: All possible starting positions for trigrams in that matrix
        sp = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,1), (2,2)] # not last letter
        # reduce the starting positions to the actually existing letters.
        sp = [p for p in sp if m[p[0]][p[1]] is not None]

        #: All possible paths in the matrix for letters
        paths = [(1,0), (1,1), (1,2)]
        #: Additional possible paths for modifiers
        mod_paths = [(0,1), (0,2)]

        #: The new trigrams which get created due to splitting.
        new_trigs = [] # option: take a set to avoid double entries.

        # move all paths
        for s in sp:
            #: trigrams of matrix positions [(p0, p1, p2), …]
            tri = []
            #: bigrams of matrix positions [(p0, p1), …]
            tr = []
            # try all possible path for two steps.
            #: the paths
            p = paths[:]
            # modifiers get extra options
            if s[1]: p.extend(mod_paths)

            # try all paths, append to tr if not None
            for n in p:
                new_pos = (s[0] + n[0], (s[1] + n[1])%3)
                try: 
                    if m[new_pos[0]][new_pos[1]] is not None:
                        tr.append((s, new_pos))
                except IndexError: # left the matrix
                    pass

            # now try all paths, starting from the positions in tr.
            for s,t in tr:
                #: the paths
                p = paths[:]
                # modifiers get extra options
                if t[1]: p.extend(mod_paths)
                for n in p:
                    new_pos = (t[0]+n[0], (t[1] + n[1])%3)
                    try: 
                        if m[new_pos[0]][new_pos[1]] is not None:
                            tri.append((s, t, new_pos))
                    except IndexError: # left the matrix
                        pass
            print([m[s[0]][s[1]]+m[t[0]][t[1]]+m[n[0]][n[1]] for s,t,n in tri])
            new_trigs.extend([m[s[0]][s[1]]+m[t[0]][t[1]]+m[n[0]][n[1]] for s,t,n in tri])
        for tri in new_trigs:
            up.append((num, tri))
            
    print (up)
    trigs.extend(up)
    trigs = [(int(num), r) for num, r in trigs if r[1:]]
    trigs.sort()
    trigs.reverse()
    return trigs


def trigrams_in_file(data, only_existing=True):
    """Sort the trigrams in a file by the number of occurrances.

    >>> data = read_file("testfile")
    >>> trigrams_in_file(data)[:12]
    [(1, '⇧aa'), (1, '⇧aa'), (1, '⇧aa'), (1, '⇧aa'), (1, '⇗aa'), (1, '⇗aa'), (1, '⇗aa'), (1, '⇗aa'), (1, 'uia'), (1, 't⇧a'), (1, 't⇧a'), (1, 't⇗a')]
    """
    trigs = {}
    for i in range(len(data)-2):
        trig = data[i] + data[i+1] + data[i+2]
        if trig in trigs:
            trigs[trig] += 1
        else:
            trigs[trig] = 1

    if only_existing: 
        all_keys = get_all_keys_in_layout(NEO_LAYOUT)
        sorted_trigs = [(trigs[i], i) for i in trigs if i[2:] and i[0] in all_keys and i[1] in all_keys and i[2] in all_keys]
    else:
        sorted_trigs = [(trigs[i], i) for i in trigs if i[2:]]
    sorted_trigs.sort()
    sorted_trigs.reverse()
    trigs = split_uppercase_trigrams(sorted_trigs)
    return trigs

def ngrams_in_filepath(datapath, slicelength=1000000):
    """Sort the trigrams in a file by the number of occurrances.

    >>> lett, big, trig = ngrams_in_filepath("testfile")
    >>> lett[:3]
    [(5, 'a'), (4, '\\n'), (2, 'r')]
    >>> big[:3]
    [(2, 'a\\n'), (2, 'Aa'), (1, 'ui')]
    >>> trig[:12]
    [(1, '⇧aa'), (1, '⇧aa'), (1, '⇧aa'), (1, '⇧aa'), (1, '⇗aa'), (1, '⇗aa'), (1, '⇗aa'), (1, '⇗aa'), (1, 'uia'), (1, 't⇧a'), (1, 't⇧a'), (1, 't⇗a')]
    """
    f = open(datapath, encoding="utf-8")
    letters = {}
    repeats = {}
    trigs = {}
    data = f.read(slicelength)
    step = 0
    while data[2:]:
        if step == 1: 
            print("reading ngrams from", datapath)
        if step:
            print("read ~", int(f.tell()/10000)/100, "MiB")
        step += 1
        
        for i in range(len(data)-2):
            letter = data[i]
            if letter in letters:
                letters[letter] += 1
            else:
                letters[letter] = 1
            
            rep = data[i] + data[i+1]
            if rep in repeats:
                repeats[rep] += 1
            else:
                repeats[rep] = 1
            
            trig = data[i] + data[i+1] + data[i+2]
            if trig in trigs:
                trigs[trig] += 1
            else:
                trigs[trig] = 1
                
        data = data[-2:] + f.read(slicelength)

    # final two letters
    for letter in data:
        if letter in letters:
            letters[letter] += 1
        else:
            letters[letter] = 1
    # final bigram
    rep = data[-2] + data[-1]
    if rep in repeats:
        repeats[rep] += 1
    else:
        repeats[rep] = 1
    
       
    
    letters = [(letters[i], i) for i in letters]
    letters.sort()
    letters.reverse()

    repeats = [(repeats[i], i) for i in repeats]
    repeats.sort()
    repeats.reverse()

    trigs = [(trigs[i], i) for i in trigs]
    trigs.sort()
    trigs.reverse()
    # split uppercase trigrams here, because we really want to do that only *once*.
    trigs = split_uppercase_trigrams(trigs)
    return letters, repeats, trigs


def trigrams_in_file_precalculated(data, only_existing=True):
    """Get the repeats from a precalculated file.

    CAREFUL: SLOW!

    >>> data = read_file("3gramme.txt")
    >>> trigrams_in_file_precalculated(data)[:6]
    [(5678513, 'en '), (4414826, 'er '), (2891228, ' de'), (2302691, 'der'), (2272020, 'ie '), (2039215, 'ich')]
    """
    trigs = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]

    if only_existing: 
        all_keys = get_all_keys_in_layout(NEO_LAYOUT)
        trigs = [(int(num), r) for num, r in trigs if r[2:] and r[0] in all_keys and r[1] in all_keys and r[2] in all_keys]
    else:
        trigs = [(int(num), r) for num, r in trigs if r[2:]]
    # cleanup
    _unescape_ngram_list(trigs)
    trigs = split_uppercase_trigrams(trigs)

    return trigs

def letters_in_file_precalculated(data, only_existing=True):
    """Get the repeats from a precalculated file.

    >>> data = read_file("1gramme.txt")
    >>> letters_in_file_precalculated(data)[:3]
    [(46474641, ' '), (44021504, 'e'), (26999087, 'n')]
    """
    letters = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:] or line[-2:] == "  "]
    # cleanup
    _unescape_ngram_list(letters)
    try:
        if only_existing:
            all_keys = get_all_keys_in_layout(NEO_LAYOUT)
            return [(int(num), let) for num, let in letters if let in all_keys]
        else:
            return [(int(num), let) for num, let in letters if let]
    except ValueError: # floats in there
        if only_existing:
            all_keys = get_all_keys_in_layout(NEO_LAYOUT)
            return [(float(num), let) for num, let in letters if let in all_keys]
        else:
            return [(float(num), let) for num, let in letters if let]

def clean_data(data):
    """Remove cruft from loaded data"""
    if data[:1] == "\ufeff":
        data = data[1:]
    return data

def get_all_data(data=None, letters=None, repeats=None, number_of_letters=None, number_of_bigrams=None, trigrams=None, number_of_trigrams=None, datapath=None): 
    """Get letters, bigrams and trigrams.

    @param data: a string of text.
    @return: letters, number_of_letters, bigrams, number_of_bigrams, trigrams, number_of_trigrams
    """
    #data = read_file("/tmp/sskreszta")

    # if we get a datastring, we use it for everything.
    if datapath is not None:
        letters, repeats, trigrams = ngrams_in_filepath(datapath)
        bigrams = repeats
        number_of_letters = sum([i for i, s in letters])
        number_of_bigrams = sum([i for i, s in bigrams])
        number_of_trigrams = sum([i for i, s in trigrams])
    elif data is not None:
        letters = letters_in_file(data)
        repeats = bigrams = repeats_in_file(data)
        trigrams = trigrams_in_file(data)
        number_of_letters = sum([i for i, s in letters])
        number_of_bigrams = sum([i for i, s in bigrams])
        number_of_trigrams = sum([i for i, s in trigrams])

    # otherwise we get the missing values from the predefined files. 
    if letters is None or number_of_letters is None: 
        letterdata = clean_data(read_file("1-gramme.15.txt"))
        letters = letters_in_file_precalculated(letterdata)
        #letters = letters_in_file(data)
        number_of_letters = sum([i for i, s in letters])

    if repeats is None or number_of_bigrams is None: 
        bigramdata = clean_data(read_file("2-gramme.15.txt"))
        bigrams = repeats_in_file_precalculated(bigramdata)
        #repeats = repeats_in_file(data)
        number_of_bigrams = sum([i for i, s in bigrams])
    else: bigrams = repeats

    if trigrams is None or number_of_trigrams is None:
        trigramdata = clean_data(read_file("3-gramme.15.txt"))
        trigrams = trigrams_in_file_precalculated(trigramdata)
        number_of_trigrams = sum([i for i, s in trigrams])

    return letters, number_of_letters, bigrams, number_of_bigrams, trigrams, number_of_trigrams

### Classes

class FileNotFoundException(Exception):
    def __str__(self):
        return repr(self.parameter)

class ParseException(Exception):
    def __str__(self):
        return repr(self.parameter)


class NGrams(object):
    """
    NGrams contains ngrams from various sources in raw and weighted
    form and can export them to the simple (1gramme.txt, 2gramme.txt,
    3gramme.txt) form with a given number of total keystrokes.

    self.one, self.two and self.three are dictionaries of 1grams, 2grams and threegrams with their respective probability of occurring.
    """
    def __init__(self, config):
        """Create an ngrams object.

        config: plain text file (utf-8 encoded).
            # ngrams source v0.1
            weight type filepath
            weight type filepath
            …

        >>> ngrams = NGrams('ngrams_test.config')
        >>> ngrams.raw
        [(1.0, ([(5, 'a'), (4, '\\n'), (2, 'r'), (2, 'e'), (2, 'A'), (1, 'u'), (1, 't'), (1, 'o'), (1, 'n'), (1, 'i'), (1, 'g'), (1, 'd')], [(2, 'a\\n'), (2, 'Aa'), (1, 'ui'), (1, 'tA'), (1, 'rt'), (1, 'rg'), (1, 'od'), (1, 'nr'), (1, 'ia'), (1, 'g\\n'), (1, 'eo'), (1, 'en'), (1, 'd\\n'), (1, 'ae'), (1, 'aa'), (1, 'aA'), (1, '\\nr'), (1, '\\ne'), (1, '\\na')], [(4, '⇧aa'), (4, '⇗aa'), (2, 't⇧a'), (2, 't⇗a'), (2, 'a⇧a'), (2, 'a⇗a'), (2, 'aa\\n'), (1, 'uia'), (1, 'rt⇧'), (1, 'rt⇗'), (1, 'rg\\n'), (1, 'od\\n'), (1, 'nrt'), (1, 'iae'), (1, 'g\\na'), (1, 'eod'), (1, 'enr'), (1, 'd\\nr'), (1, 'aen'), (1, 'aa⇧'), (1, 'aa⇗'), (1, 'a\\ne'), (1, '\\nrg'), (1, '\\neo'), (1, '\\naa')]))]
        """
        # read the config.
        try:
            with open(config) as f:
                self.config = f.read()
        except IOError:
            raise FileNotFoundException("File", config, "can’t be read.")
        if self.config.startswith("# ngrams source v0.0"):
            self.parse_config_0_0()
        elif self.config.startswith("# ngrams source v0.1"):
            self.parse_config_0_1()
        else:
            raise ParseException("ngrams config has no version header. Please start it with # ngrams source v<version>")
        self.normalize_raw() # gets one, two and three

    def parse_config_0_1(self):
        lines = self.config.splitlines()
        # the raw list of included ngrams.
        self.raw = []
        for l in lines[1:]:
            parts = l.split()
            weight, typ = parts[:2]
            weight = float(weight)
            datapath = l[l.index(typ)+len(typ)+1:]
            if typ=="text":
                one, onenum, two, twonum, three, threenum = get_all_data(datapath=datapath)
                self.raw.append((weight, (one, two, three)))
            elif typ=="pykeylogger":
                one, two, three = self.read_pykeylogger_logfile(datapath)
                self.raw.append((weight, (one, two, three)))
            elif typ=="pregenerated":
                onegrams, twograms, threegrams = datapath.split(";")
                letterdata = clean_data(read_file(onegrams))
                one = letters_in_file_precalculated(letterdata)
                bigramdata = clean_data(read_file(twograms))
                two = repeats_in_file_precalculated(bigramdata)
                trigramdata = clean_data(read_file(threegrams))
                three = trigrams_in_file_precalculated(trigramdata)
                self.raw.append((weight, (one, two, three)))
            elif typ=="maildir":
                self.read_maildir_dir(datapath)
            else: print("unrecognized filetype", typ, datapath)

    def read_maildir_dir(self, folderpath):
        """Read all message contents from within a maildir folder.

        see http://docs.python.org/library/mailbox.html#mailbox.Maildir
        """
        text = ""
        from mailbox import Maildir
        m = Maildir(folderpath)
        num = 0
        for message in m.itervalues():
            #print (num, "/", len(m))
            text += self._maildir_message_own_content(message)
            print (text)
            num += 1

    def _maildir_message_own_content(self, message):
        """Remove all quotes and headers from the message.

        @return string of the content which was written by the author."""
        import quopri
#        import email.errors
        text = ""
        for t in message.walk():
            if t.get_content_type() == "text/plain":
                # remove quoted printable
                # the following should work, but does not. 
                # body = quopri.decodestring(t.as_string())
                # fix directly from quopri: 
                from io import BytesIO
                infp = BytesIO(t.as_string().encode("utf-8"))
                outfp = BytesIO()
                quopri.decode(infp, outfp, header=False)
                try: 
                    body = outfp.getvalue().decode("utf-8")
                except UnicodeDecodeError:
                    try: body = outfp.getvalue().decode("iso-8859-1")
                    except UnicodeDecodeError:                     
                        print (t.as_string())
                        body = t.as_string()

#                try: 
#                    c = Charset(body)
#                except email.errors.CharsetError:
#                    pass
#                print(c.__dict__)
#                print (c.get_body_encoding())
#                print(c.get_output_charset())
                #body = c.body_encode(body)
                body = body[body.index("\n\n"):]
                # we only ever add the previous line, so we can remove fullquotes along with their data.
                previous_line = ""
                for l in body.splitlines():
                    # stop reading the message
                    if "Forwarded Message" in previous_line or previous_line.startswith("--"):
                        break
                    # skip quotes and stuff I want to ignore.
                    if (previous_line.startswith(">") or
                        previous_line.startswith(" >") or
                        not " " in previous_line or # most likely an escaped datablock
                        "http://" in previous_line): # an url
                        previous_line = l
                        continue
                    # add all lines which are not the beginning of a comment.
                    if not ">" in l and not previous_line.endswith(":"):
                        text += previous_line
                    previous_line = l
                    text += "\n"
#        print(text)
        return text

    def read_pykeylogger_logfile(self, datapath):
        """Read a logfile from pykeylogger and extract all normal keys."""
        with open(datapath) as f:
            data = f.read()
        text = ""
        for line in data.splitlines():
            # skip the beginning
            line = "|".join(line.split("|")[6:])
            # replace all special chars we know by the special chars used in our keyboard definition
            line = line.replace("[KeyName:Return]", "\n")
            line = line.replace("[KeyName:BackSpace]", "←")
            line = line.replace("[KeyName:Control_L]", "♕")
            line = line.replace("[KeyName:Control_R]", "♛")
            line = line.replace("[KeyName:Alt_L]", "♔")
            line = line.replace("[KeyName:Alt_R]", "♚")
            line = line.replace("[KeyName:Tab]", "⇥")
            # remove all other special chars
            try: 
                text += line[:line.index("[KeyName")]
            except ValueError:
                # no key name in there.
                text += line
                continue
            for part in line.split("[KeyName:")[1:]:
                try: 
                    text += part[part.index("]")+1:]
                except ValueError:
                    print(part, line)
        
        one, onenum, two, twonum, three, threenum = get_all_data(data=text)
        return one, two, three
        
    def parse_config_0_0(self): 
        lines = self.config.splitlines()
        # the raw list of included ngrams.
        self.raw = []
        for l in lines[1:]:
            spaceidx = l.index(" ")
            weight = float(l[:spaceidx])
            datapath = l[spaceidx+1:]
            one, onenum, two, twonum, three, threenum = get_all_data(datapath=datapath)
            self.raw.append((weight, (one, two, three)))

    def normalize_raw(self):
        """Normalize the raw ngrams and store them in self.one, self.two and self.three."""
        
        # normalize ngrams
        def _normalize(ngramlist):
            """normalize a list of ngrams.

            @param ngramlist: [(num, "ngram"), …]
            @return list with sum([num for num, ngram in ngrams]) == 1
            """
            total = sum((num for num, ngram in ngramlist))
            return [(num / total, ngram) for num, ngram in ngramlist]

        normalized = []
        for weight, ngrams in self.raw:
            normalized.append((weight,
                               [_normalize(ngram) for ngram in ngrams]))

        # weight them.
        self.one = {}
        self.two = {}
        self.three = {}
        for weight, ngrams in normalized:
            one = ngrams[0]
            two = ngrams[1]
            three = ngrams[2]
            for norm, weighted in ((one, self.one),
                                   (two, self.two),
                                   (three, self.three)): 
                for num, ngram in norm:
                    try: weighted[ngram] += num*weight
                    except KeyError: weighted[ngram] = num*weight

    def save(self, one, two, three):
        """save the data to the files one, two and three (i.e. 1gramme.txt, 2gramm…).

        Plan: Add a total number of keystrokes parameter.
        @param one: path to the 1grams file.
        """
        for p, ngrams in ((one, self.one),
                          (two, self.two),
                          (three, self.three)): 
            gramlist = [(num, ngram) for ngram, num in ngrams.items()] 
            gramlist.sort()
            data = ""
            for num, ngram in reversed(gramlist):
                ngram = ngram.replace("\\", "\\\\")
                ngram = ngram.replace("\n", "\\n")
                data += str(num) + " " + ngram + "\n"
            with open(p, "w") as f:
                f.write(data)

def _test():
    from doctest import testmod
    testmod()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Read nGrams from files.")
    parser.add_argument("args")
    parser.add_argument("--conf", dest="config", help="The ngram config file to use.")
    parser.add_argument("--test", dest="test", action="store_true", help="Run the self-test.")
    parser.add_argument("--save1", dest="one", help="File for the 1-grams. You need conf, save1, save2 AND save3 for saving.")
    parser.add_argument("--save2", dest="two", help="File for the 2-grams.")
    parser.add_argument("--save3", dest="three", help="File for the 3-grams.")
    from sys import argv
    args = parser.parse_args(argv)
    if args.config:
        ngrams = NGrams(args.config)
    if args.config and args.one and args.two and args.three:
        ngrams.save(args.one, args.two, args.three)
    if args.test:
        _test()

