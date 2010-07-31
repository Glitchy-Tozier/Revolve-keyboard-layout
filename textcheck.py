#!/usr/bin/env python3

"""Check how much a given text diverges from a 1gram, 2gram and 3gram frequency.

usage: ./textcheck.py <textfile to check> [--best-lines]

--lines: check each line and return the 10 most similar lines. 

idea: allow selecting different 1gram, 2gram and 3gram files. 

"""


def read_file(path):
    """Get the data from a file.

    >>> read_file("testfile")[:2]
    'ui'
    """
    with open(path) as f: #, encoding="UTF-8") as f:
        data = f.read()
    return data

def read_file_lines(path):
    """Get the data from a file.

    >>> read_file("testfile")[:2]
    'ui'
    """
    with open(path) as f: #, encoding="UTF-8") as f:
        data = f.readlines()
    return data

def letters_in_file(data):
    """Sort the repeats in a file by the number of occurrances.

    >>> data = read_file("testfile")
    >>> letters_in_file(data)[:3]
    [(5, 'a'), (4, '\\n'), (2, '⇧')]
    """
    letters = {}
    for letter in data:
        if letter in letters:
            letters[letter] += 1
        else:
            letters[letter] = 1
    return letters

def letters_in_file_precalculated(data):
    """Get the repeats from a precalculated file.

    >>> data = read_file("1gramme.txt")
    >>> letters_in_file_precalculated(data)[:2]
    [(44034982, 'e'), (27012723, 'n')]
    """
    letters = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    letters = [(int(num), let) for num, let in letters]
    lett = {l: num for num, l in letters}
    return lett
    
def repeats_in_file(data):
    """Sort the repeats in a file by the number of occurrances.

    >>> data = read_file("testfile")
    >>> repeats_in_file(data)[:3]
    [(2, 'aa'), (2, 'a\\n'), (1, '⇧a')]
    """
    repeats = {}
    for i in range(len(data)-1):
        rep = data[i] + data[i+1]
        if rep in repeats:
            repeats[rep] += 1
        else:
            repeats[rep] = 1
    return repeats

def repeats_in_file_precalculated(data):
    """Get the repeats from a precalculated file.

    >>> data = read_file("2gramme.txt")
    >>> repeats_in_file_precalculated(data)[:2]
    [(10162743, 'en'), (10028050, 'er')]
    """
    reps = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    reps = [(int(num), r) for num, r in reps if r[1:]]
    r = {r: num for num, r in reps}
    return r

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
    return trigs

def trigrams_in_file_precalculated(data):
    """Get the repeats from a precalculated file.

    CAREFUL: SLOW!

    >>> data = read_file("3gramme.txt")
    >>> trigrams_in_file_precalculated(data)[:6]
    [(5679632, 'en '), (4417443, 'er '), (2891983, ' de'), (2303238, 'der'), (2273056, 'ie '), (2039537, 'ich')]
    """
    trigs = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    trigs = [(int(num), r) for num, r in trigs if r[1:]]
    t = {t: num for num, t in trigs}
    return t

def normalize_occurrence_dict(d):
    """normalize a dict with keys and assorted occurrence numbers.

    @param min_occ: If the occurrence number is smaller than this, just ignore it (value = 0.0).

    ⇒ sum([d[t] for t in d]) == 1.0
    """
    _sum = sum([d[t] for t in d])
    d = {t: d[t]/_sum for t in d}
    return d
    
def occurrence_dict_difference(d1, d2):
    """Get the squared difference between two occurrence dicts.

    @return: dict with all keys (in d1 or in d2) and the difference as value."""
    diff1 = {}
    # check d1
    for t in d1:
        if t in d2:
            diff1[t] = (d1[t] - d2[t])**2
        else:
            diff1[t] = d1[t]**2
    # add all from d2 which are not in d1
    for t in d2:
        if not t in diff1:
            diff1[t] = d2[t]**2
    return diff1

def check_dissimilarity(txt_1grams, txt_2grams, txt_3grams, ref_1grams, ref_2grams, ref_3grams):
    """check the similarity of the txt and the ref (-erence)."""

    # normalize all dicts
    txt_1grams = normalize_occurrence_dict(txt_1grams)
    txt_2grams = normalize_occurrence_dict(txt_2grams)
    txt_3grams = normalize_occurrence_dict(txt_3grams)
    ref_1grams = normalize_occurrence_dict(ref_1grams)
    ref_2grams = normalize_occurrence_dict(ref_2grams)
    ref_3grams = normalize_occurrence_dict(ref_3grams)
    
    d1 = occurrence_dict_difference(txt_1grams, ref_1grams)
    d2 = occurrence_dict_difference(txt_2grams, ref_2grams)
    d3 = occurrence_dict_difference(txt_3grams, ref_3grams)

    return 0.5*sum(d1.values()), 0.5*sum(d2.values()), 0.5*sum(d3.values())

def _help():
    return __doc__

### Self-Test

if __name__ == "__main__":
    from sys import argv
    if "--test" in argv:
        from doctest import testmod
        testmod()
        exit()
    
    if not argv[1:]:
        print(_help())
        exit()

    if "--best-lines" in argv:
        LINES = True
    else:
        LINES = False

    # reference data
    data = read_file("1gramme.txt")
    reference1grams = letters_in_file_precalculated(data)
    data = read_file("2gramme.txt")
    reference2grams = repeats_in_file_precalculated(data)
    data = read_file("3gramme.txt")
    reference3grams = trigrams_in_file_precalculated(data)

    # text to check
    textfile = argv[1]

    if LINES: 
        data = read_file_lines(textfile)
        best_10 = [] # [(sum, (1, 2, 3), text), …]
        for l in data: 
            text1grams = letters_in_file(l)
            text2grams = repeats_in_file(l)
            text3grams = trigrams_in_file(l)
            diss = check_dissimilarity(text1grams, text2grams, text3grams, reference1grams, reference2grams, reference3grams)
            if not best_10[9:] or sum(diss) < min([s for s, x, text in best_10]):
                best_10.append((sum(diss), diss, l))
                best_10.sort()
                best_10 = best_10[:10]
            print(diss, l)
        print("\n### best 10 lines ###\n")
        for s, x, t in best_10:
            print(x, t)
    else:
        data = read_file(textfile)
        text1grams = letters_in_file(data)
        text2grams = repeats_in_file(data)
        text3grams = trigrams_in_file(data)
        diss = check_dissimilarity(text1grams, text2grams, text3grams, reference1grams, reference2grams, reference3grams)
        print(diss)
        
