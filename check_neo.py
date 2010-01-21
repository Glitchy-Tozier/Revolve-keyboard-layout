#!/usr/bin/env python3
# encoding: utf-8

"""Check the neo keyboard for double-usage of the same finger.

Premise: The base row should remain unchanged.

Usage:

- check_neo.py --help
- check_neo.py --file <file>


Design: 
- Daten als Listen, die der Tastatur entsprechen: Reihen und Spalten. 
- Für jede Taste ein Tuple mit den verschiedenen Bedeutungen. Mods: (None, Shift, Mod3, Mod4, Shift+Mod3, Mod3+Mod4)
- find_key() -> (reihe, spalte, index)
- two_char_repeats_from_file() -> [iste mit allen 2 char repeats, auch mehrfach.
- two_chars_on_same_finger(keys) -> sind min 2 Buchstaben auf dem gleichen Finger? -> Finger


Später:
- Einfache Funktionen zum Austauschen. 
- Eine Kostenfunktion -> Text + Layout = Kosten. 
- "Kosten der Änderung" für die Austauschfunktion: Fingerwechsel, Seitenwechsel, ...
- Ein Layout mit Kosten: Zahl für jede Taste -> Exaktere Berechnung der Kosten der Änderung. 

"""

#: Die Layout-Datei für Neo = Tastenbelegung - aktuell nur für Reihe 0, 1, 2 und 3 ohne Modifikator-Tasten nutzbar => nur Kleinbuchstaben. 
NEO_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),()], # Zahlenreihe (0)
    [(),("x"),("v"),("l"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [(),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),(),("\n")], # Reihe 2
    [(),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),()],	# Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lx = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),()], # Zahlenreihe (0)
    [(),("l"),("v"),("x"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [(),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),(),("\n")], # Reihe 2
    [(),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),()],	# Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lxwq = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),()], # Zahlenreihe (0)
    [(),("l"),("v"),("x"),("c"),("q"),("k"),("h"),("g"),("f"),("w"),("ß"),("´"),()], # Reihe 1
    [(),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),(),("\n")], # Reihe 2
    [(),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),()],	# Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

QWERTZ_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),()], # Zahlenreihe (0)
    [(),("q"),("w"),("e"),("r"),("t"),("z"),("u"),("i"),("o"),("p"),("ü"),("+"),()], # Reihe 1
    [(),("a"),("s"),("d"),("f"),("g"),("h"),("j"),("k"),("l"),("ö"),("ä"),(),("\n")], # Reihe 2
    [(),(),("y"),("x"),("c"),("v"),("b"),("n"),("m"),(","),("."),("-"),()],	# Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]


#: The positions which are by default accessed by the given finger. 
FINGER_POSITIONS = [
    [(1, 1, 0), (2, 1, 0), (3, 1, 0), (3, 2, 0)],
    [(1, 2, 0), (2, 2, 0), (3, 3, 0)],
    [(1, 3, 0), (2, 3, 0), (3, 4, 0)],
    [(1, 4, 0), (2, 4, 0), (3, 5, 0), (1, 5, 0), (2, 5, 0), (3, 6, 0)], 
    [(4, 3, 0)],
    [(4, 3, 0)],
    [(1, 6, 0), (2, 6, 0), (3, 7, 0), (1, 7, 0), (2, 7, 0), (3, 8, 0)], 
    [(1, 8, 0), (2, 8, 0), (3, 9, 0)],
    [(1, 9, 0), (2, 9, 0), (3, 10, 0)],
    [(1, 10, 0), (2, 10, 0), (3, 11, 0), (1, 11, 0), (2, 11, 0), (1, 12, 0), (2, 12, 0), (2, 13, 0)]
    ]
#: The names of the fingers for which we gave the positions above.
FINGER_NAMES = ["Klein_L", "Ring_L", "Mittel_L", "Zeige_L", "Daumen_L",
                "Daumen_R", "Zeige_R", "Mittel_R", "Ring_R", "Klein_R"]

def find_key(key, layout=NEO_LAYOUT): 
    """Find the position of the key in the layout.
    
    >>> find_key("a")
    (2, 3, 0)
    """
    pos = None
    for row in range(len(layout)): 
        for col in range(len(layout[row])): 
            for idx in range(len(layout[row][col])):
                if layout[row][col][idx] == key: 
                    pos = (row, col, idx)
    return pos


def get_key(pos, layout=NEO_LAYOUT):
    """Get the key at the given position.

    >>> get_key((2, 3, 0))
    'a'
    """
    try: 
        return layout[pos[0]][pos[1]][pos[2]]
    except: return None

def finger_keys(finger_name, layout=NEO_LAYOUT):
    """Get the keys corresponding to the given finger name.

    >>> for name in FINGER_NAMES:
    ...    name, finger_keys(name)
    ('Klein_L', ['x', 'u', 'None', 'ü'])
    ('Ring_L', ['v', 'i', 'ö'])
    ('Mittel_L', ['l', 'a', 'ä'])
    ('Zeige_L', ['c', 'e', 'p', 'w', 'o', 'z'])
    ('Daumen_L', [' '])
    ('Daumen_R', [' '])
    ('Zeige_R', ['k', 's', 'b', 'h', 'n', 'm'])
    ('Mittel_R', ['g', 'r', ','])
    ('Ring_R', ['f', 't', '.'])
    ('Klein_R', ['q', 'd', 'j', 'ß', 'y', '´', 'None', '\\n'])
    """
    idx = FINGER_NAMES.index(finger_name)
    keys = [str(get_key(pos, layout=layout)) for pos in FINGER_POSITIONS[idx]]
    return keys

def key_to_finger(key, layout=NEO_LAYOUT):
    """Get the finger name used to hit the given key.

    >>> key_to_finger("a")
    'Mittel_L'
    >>> key_to_finger("«")
    ''
    """
    pos = find_key(key, layout=layout)
    for i in range(len(FINGER_POSITIONS)):
        if pos in FINGER_POSITIONS[i]:
            return FINGER_NAMES[i]
    return ""

def repeats_in_file(path):
    """Sort the repeats in a file by the number of occurrances.

    >>> repeats_in_file_sorted("testfile")[:2]
    [(1, '\\na'), (1, '\\ne')]
    """
    f = open(path)
    data = f.read()
    f.close()
    # TODO: Take uppercase correctly into account
    data = data.lower()
    repeats = []
    for i in range(len(data)-1):
        repeats.append(data[i] + data[i+1])
    return repeats

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
    
def finger_repeats_from_file(path, count_same_key=False, layout=NEO_LAYOUT):
    """Get a list of two char strings from the file, which repeat the same finger.

    >>> finger_repeats_from_file("testfile")
    [('Klein_R', 'd\\n'), ('Zeige_L', 'eo'), ('Mittel_R', 'rg')]
    >>> finger_repeats_from_file("testfile", count_same_key=True)
    [('Klein_R', 'd\\n'), ('Zeige_L', 'eo'), ('Mittel_R', 'rg'), ('Mittel_L', 'aa')]
    """
    repeats = repeats_in_file(path)
    finger_repeats = []
    for i in repeats:
        key1 = i[0]
        key2 = i[1]
        finger1 = key_to_finger(key1, layout=layout)
        if finger1 == key_to_finger(key2, layout=layout):
            finger_repeats.append((finger1, key1+key2))
    if not count_same_key:
        finger_repeats = [r for r in finger_repeats if not r[1][0] == r[1][1]]
    return finger_repeats

def repeats_in_file_sorted(path):
    """Sort the repeats in a file by the number of occurrances.

    >>> repeats_in_file_sorted("testfile")[:2]
    [(1, '\\na'), (1, '\\ne')]
    """
    repeats = repeats_in_file(path)
    sorted_repeats = unique_sort(repeats)
    return sorted_repeats
    
def switch_keys(keypairs, layout=NEO_LAYOUT):
    """Switch keys in the layout, so we don't have to fiddle with actual layout files.

    TODO: REPORT BUG py 3.2: Running testmod makes the actual run fail

    >>> lay = switch_keys(["lx", "wq"], layout = NEO_LAYOUT)
    >>> get_key((1, 1, 0), layout=lay)
    'l'
    >>> get_key((1, 3, 0), layout=lay)
    'x'
    >>> get_key((1, 5, 0), layout=lay)
    'q'
    >>> get_key((1, 10, 0), layout=lay)
    'w'
    >>> NEO_LAYOUT_lxwq == lay
    True
    """
    lay = layout[:]
    for pair in keypairs:
        pos0 = find_key(pair[0], layout=lay)
        pos1 = find_key(pair[1], layout=lay)
        tmp0 = pair[1] + lay[pos0[0]][pos0[1]][1:]
        tmp1 = pair[0] + lay[pos1[0]][pos1[1]][1:]
        lay[pos0[0]][pos0[1]] = tmp0
        lay[pos1[0]][pos1[1]] = tmp1
    
    return lay
        
    

### Self-Test 

if __name__ == "__main__": 
    from sys import argv
    
    if "--test" in argv:
        from doctest import testmod
        testmod()
        exit()

    if "-q" in argv:
        QUIET = True
        argv.remove("-q")
    else: QUIET = False
    
    if "--help" in argv or not argv[2:]:
        print(__doc__)
        exit()

    if argv[1] == "--file":
        path = argv[2]
        
        if argv[4:] and argv[3] == "--switch":
            switchlist = argv[4].split(",")
            lay = switch_keys(switchlist, layout = NEO_LAYOUT)
            print("Neo", switchlist, "autogenerated")
            frep = finger_repeats_from_file(path, layout=lay)
            print(str(len(frep)), "finger repeats in file", path)
        else:
            print("Neo")
            frep = finger_repeats_from_file(path)#, layout=QWERTZ_LAYOUT)
            print(str(len(frep)), "finger repeats in file", path)

        if not QUIET: 
            print(unique_sort(frep))
        
            print("Qwertz")
            frep = finger_repeats_from_file(path, layout=QWERTZ_LAYOUT)
            print(str(len(frep)), "finger repeats in file", path)
        #print(unique_sort(frep))
        
        #rep = repeats_in_file_sorted(path)
        #print(str(len(rep)), "repeats in file", path, "sorted.")
        #print([i for i in rep if "a" in i[1]])
        
