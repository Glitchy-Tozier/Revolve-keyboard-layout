#!/usr/bin/env python3

"""Calculating ngram distributions (letters, bigrams, trigrams) from text or getting them from precomputed files."""

from layout_base import NEO_LAYOUT, key_to_finger, read_file

def split_uppercase_repeats(reps, layout=NEO_LAYOUT):
    """Split uppercase repeats into two to three lowercase repeats.

    TODO: treat left and right shift differently. Currently we always use both shifts (⇧ and ⇗) and half the value (but stay in integers => 1 stays 1). Needs major refactoring, since it needs knowledge of the layout. Temporary fix: always use both shifts. → Almost completely done in finger repeats evaluation. Only remaining: ⇧⇗ and ⇗⇧, but these aren’t relevant to finger collisions, only to handswitching (and there we ignore them, as the difference is at most one more letter without switching). Also remaining: very rare repeats are now counted more strongly, since 

    Shift und die Taste werden gleichzeitig gedrückt => in einem bigramm, in dem der erste Buchstabe groß ist, gibt es sowohl die Fingerwiederholung Shift-Buchstabe 1, als auch Shift-Buchstabe2. => einfach verdoppeln. - done

    TODO: aB should be counted about 2x, Ab only 0.5 times, because shift is pressed and released a short time before the key. 

        Ab -> shift-a, shift-b, a-b.
        aB -> a-shift, shift-b, a-b.
        AB -> shift-a, shift-b, a-b, 0.5*(shift_L-shift_R, shift_R-shift_L)

    Jeweils sowohl rechts als auch links. 


    >>> reps = [(12, "ab"), (6, "Ab"), (4, "aB"), (1, "AB")]
    >>> split_uppercase_repeats(reps)
    [(12, 'ab'), (6, '⇗b'), (6, 'ab'), (4, 'a⇧'), (4, 'ab'), (1, '⇧⇗'), (1, '⇗⇧'), (1, '⇗b'), (1, 'a⇧'), (1, 'ab')]
    """
    # replace uppercase by ⇧ + char1 and char1 + char2 and ⇧ + char2
    # char1 and shift are pressed at the same time
    upper = [(num, rep) for num, rep in reps if not rep == rep.lower()]
    reps = [rep for rep in reps if rep[1] == rep[1].lower()]
    up = []
    for num, rep in upper: # Ab = ab,⇗b aB = a⇧,ab AB = a⇧,⇗b,ab (A links, B rechts)
        # use both shifts, but half weight each
        if not rep[0] == rep[0].lower() and not rep[1] == rep[1].lower(): # AB
            up.append((max(1, num//2), "⇗⇧"))
            up.append((max(1, num//2), "⇧⇗"))
        if not rep[0] == rep[0].lower(): # Ab od. AB
            finger = key_to_finger(rep[0].lower(), layout=layout)
            if finger and finger[-1] == "L": 
                up.append((num, "⇗"+rep[1].lower()))
            elif finger and finger[-1] == "R": 
                up.append((num, "⇧"+rep[1].lower()))
        if not rep[1] == rep[1].lower(): # aB od. AB
            finger = key_to_finger(rep[1].lower(), layout=layout)
            if finger and finger[-1] == "L": 
                up.append((num, rep[0].lower() + "⇗"))
            elif finger and finger[-1] == "R": 
                up.append((num, rep[0].lower() + "⇧"))

        up.append((num, rep[0].lower()+rep[1].lower()))

    reps.extend(up)
    # cleanup
    reps = [(int(num), r) for num, r in reps if r[1:]]
    reps.sort()
    reps.reverse()
    return reps

def repeats_in_file(data):
    """Sort the repeats in a file by the number of occurrances.

    >>> data = read_file("testfile")
    >>> repeats_in_file(data)[:3]
    [(2, 'a\\n'), (2, 'Aa'), (1, 'ui')]
    """
    repeats = {}
    for i in range(len(data)-1):
        rep = data[i] + data[i+1]
        if rep in repeats:
            repeats[rep] += 1
        else:
            repeats[rep] = 1
    sorted_repeats = [(repeats[i], i) for i in repeats]
    sorted_repeats.sort()
    sorted_repeats.reverse()
    #reps = split_uppercase_repeats(sorted_repeats) # wrong place
    return sorted_repeats

def split_uppercase_letters(reps, layout):
    """Split uppercase letters into two lowercase letters (with shift).

    >>> letters = [(4, "a"), (3, "A")]
    >>> split_uppercase_letters(letters, layout=NEO_LAYOUT)
    [(4, 'a'), (3, '⇗'), (3, 'a')]
    """
    # replace uppercase by ⇧ and char1
    upper = [(num, rep) for num, rep in reps if not rep == rep.lower()]
    reps = [rep for rep in reps if not rep in upper]
    up = []
    
    for num, rep in upper:
        fing = key_to_finger(rep.lower(), layout=layout)
        try: 
            hand = fing[-1]
            if hand == "L":
                up.append((num, "⇗"))
            elif hand == "R":
                up.append((num, "⇧"))
        except IndexError:
            # not in there (special letters not on keyboard layer 1)
            pass
        up.append((num, rep.lower()))
                
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

def repeats_in_file_precalculated(data):
    """Get the repeats from a precalculated file.

    >>> data = read_file("2gramme.txt")
    >>> repeats_in_file_precalculated(data)[:2]
    [(10159250, 'en'), (10024681, 'er')]
    """
    reps = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    reps = [(int(num), r) for num, r in reps if r[1:]]
    #reps = split_uppercase_repeats(reps) # wrong place, don’t yet know the layout
    
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
    upper = [(num, trig) for num, trig in trigs if not trig == trig.lower()]
    # and remove them temporarily from the list of trigrams - don’t compare list with list, else this takes ~20min!
    trigs = [(num, trig) for num, trig in trigs if trig == trig.lower()]
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
    trigs = [(int(num), r) for num, r in trigs if r[1:]]
    trigs.sort()
    trigs.reverse()
    return trigs


def trigrams_in_file(data):
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
    sorted_trigs = [(trigs[i], i) for i in trigs]
    sorted_trigs.sort()
    sorted_trigs.reverse()
    trigs = split_uppercase_trigrams(sorted_trigs)
    return trigs

def trigrams_in_file_precalculated(data):
    """Get the repeats from a precalculated file.

    CAREFUL: SLOW!

    >>> data = read_file("3gramme.txt")
    >>> trigrams_in_file_precalculated(data)[:6]
    [(5678513, 'en '), (4414826, 'er '), (2891228, ' de'), (2302691, 'der'), (2272020, 'ie '), (2039215, 'ich')]
    """
    trigs = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    trigs = [(int(num), r) for num, r in trigs if r[1:]]
    trigs = split_uppercase_trigrams(trigs)
    
    return trigs

def letters_in_file_precalculated(data):
    """Get the repeats from a precalculated file.

    >>> data = read_file("1gramme.txt")
    >>> letters_in_file_precalculated(data)[:2]
    [(44021504, 'e'), (26999087, 'n')]
    """
    letters = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    return [(int(num), let) for num, let in letters]
    

def get_all_data(data=None, letters=None, repeats=None, number_of_letters=None, number_of_bigrams=None, trigrams=None, number_of_trigrams=None): 
    """Get letters, bigrams and trigrams.

    @param data: a string of text.
    @return: letters, number_of_letters, bigrams, number_of_bigrams, trigrams, number_of_trigrams
    """
    #data = read_file("/tmp/sskreszta")

    # if we get a datastring, we use it for everything. 
    if data is not None:
        letters = letters_in_file(data)
        repeats = bigrams = repeats_in_file(data)
        trigrams = trigrams_in_file(data)
        number_of_letters = sum([i for i, s in letters])
        number_of_bigrams = sum([i for i, s in bigrams])
        number_of_trigrams = sum([i for i, s in trigrams])

    # otherwise we get the missing values from the predefined files. 
    if letters is None or number_of_letters is None: 
        letterdata = read_file("1gramme.txt")
        letters = letters_in_file_precalculated(letterdata)
        #letters = letters_in_file(data)
        number_of_letters = sum([i for i, s in letters])

    if repeats is None or number_of_bigrams is None: 
        bigramdata = read_file("2gramme.txt")
        bigrams = repeats_in_file_precalculated(bigramdata)
        #repeats = repeats_in_file(data)
        number_of_bigrams = sum([i for i, s in bigrams])
    else: bigrams = repeats

    if trigrams is None or number_of_trigrams is None:
        trigramdata = read_file("3gramme.txt")
        trigrams = trigrams_in_file_precalculated(trigramdata)
        number_of_trigrams = sum([i for i, s in trigrams])

    return letters, number_of_letters, bigrams, number_of_bigrams, trigrams, number_of_trigrams
   
