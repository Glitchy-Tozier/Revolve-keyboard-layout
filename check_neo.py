#!/usr/bin/env python3
# encoding: utf-8

"""Check the neo keyboard for double-usage of the same finger.

"""
__usage__ = """Usage:

- check_neo.py --help (display this text)
- check_neo.py --test (run doctests)
- check_neo.py [--file <file>] [--switch <lx,wq>] [-q] [-v]
  run the script on the file. 
  --switch switches letters on the neo keyboard (lx,wq switches l for x and w for q). 
  -q removes the qwertz comparision.
  -v adds the list of finger repeats.
- check_neo.py --evolve <iterations>
  randomly permutate keys on the Neo keyboard to see if a better layout emerges. 


"""
__design__ = """
Design: 
- Der Code ist in die Abschnitte Constants, Imports, Helper functions, Cost functions und Evolution aufgeteilt.
- Daten als Listen, die der Tastatur entsprechen: Reihen und Spalten. 
- Für jede Taste ein Tuple mit den verschiedenen Bedeutungen. Mods: (None, Shift, Mod3, Mod4, Shift+Mod3, Mod3+Mod4)
- find_key() -> (reihe, spalte, index)
- two_char_repeats_from_file() -> [iste mit allen 2 char repeats, auch mehrfach.
- two_chars_on_same_finger(keys) -> sind min 2 Buchstaben auf dem gleichen Finger? -> Finger
- Einfache Funktionen zum Austauschen. 
- Eine Kostenfunktion -> Text + Layout = Kosten. 
- Ein Layout mit Kosten: Zahl für jede Taste -> Exaktere Berechnung der Kosten der Änderung. 
- Evolution durch Mutation und Kostenminimierung (switch miltiple times (3?) => keep if lower cost).
- Die Hauptarbeit der Mutation wird von der Funktion total_cost() übernommen. 

Später:
- "Kosten der Änderung" für die Austauschfunktion: Fingerwechsel, Seitenwechsel, ...


Vorgehensweise zur Optimierung:
- Annahme: Es gibt eine Idealtastatur. Auf ihr können Gedanken ohne Zeitverlust und ohne Aufwand aufgezeichnet werden.
- Reale Tastaturen können sich dem Ideal immer nur annähern. Daher arbeiten wir mit „Kosten im Vergleich zur Idealtastatur“. Die Minimierung der Kosten gibt einen Hinweis darauf, wie eine der Idealtastatur möglichst nahe kommende Tastatur aussehen kann.
- Ein Programm kann nur die einfachsten Faktoren berücksichtigen, da es Quantisierung benötigt. Deshalb muss eine Optimierung von Menschen geprüft werden, und Ästethik und Intuition (also menschliches Feingefühle mit viel komplexerer Grundlage: Quantitative + Qualitative Faktoren) gelten mehr als reine Zahlenspielerei. Die Maschine kann aber Vorarbeit leisten und stupides Prüfen übernehmen. 
- Die deutsche Standardtastatur gilt als „Infrastauktur“. Das Layout muss auf ihr funktionieren. 
- Als Daten-Grundlage dient die Liste der N-Gramme. Für die aktuellen brauchen wir nur mono- und bigramme.

Kostenfaktor: Zeit
- Unterschiedlich schnell zu erreichende Tasten => Kosten für einzelne Tasten. - done
- Einen Finger mehrfach hintereinander verwenden. => Strafpunkte. - done
- Einen Finger mehrfach, von oben nach ganz unten. => viele Strafpunkte. - TODO

Kostenfaktor: Belastung
- Ungleichmäßige Belastung beider Hände. - TODO
- Ungleichmäßige Belastung der einzelnen Finger (allerdings sollte der Kleine weniger belastet werden). - TODO

Kostenfaktor: Natürliche Handbewegung
- Von innen nach außen mit Handwechsel. => von außen nach innen gibt Strafpunkte. - TODO
- Links gleicher Finger wie rechts. => Fingerwechsel bei Handwechsel hat Kosten. - TODO

Kostenfaktor: Neulernzeit (die ideale Tastatur kann jeder schon - und wir optimieren für Neo)
- Jede einzelne Änderung von Neo2 weg bringt Strafpunkte => Es kann über Gewichtung festgelegt werden, wie nahe das Ergebnis an Neo liegen soll. - TODO


Notizen:
- Ulf Bro nutzt für Kosten der Einzeltasten das folgende:
  5 3 3 3 4         4 3 3 3 5 7
  1 0 0 0 2         2 0 0 0 1 7
  6 5 5 5 7         7 5 5 5 6
  Um konsistent mit der Idee „die Idealtastatur braucht keine Zeit“ zu sein, sollte die Grundreihe allerdings auch Kosten haben.
  Genutzte Alternative:
    6 3 3 3 4         4 3 3 3 6 7 8
    2 1 1 1 3         3 1 1 1 2 6 9
  4 5 5 5 5 7         7 5 5 5 5
  Kleiner Finger unten geht bei mir weitaus besser ais Mittel- oder Ringfinger. 

"""

__doc__ += __usage__ + __design__

__version__ = "0.1.0"


### Constants

# Gewichtung der unterschiedlichen Kosten
WEIGHT_FINGER_REPEATS = 5
WEIGHT_POSITION = 1 # referenz

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
NEO_LAYOUT_lxwq = [ # 25% weniger Fingerwiederholungen als Neo, fast 50% weniger als Qwertz
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

COST_PER_KEY  = [ # 0 heißt nicht beachtet
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Zahlenreihe (0)
        [0,6,3,3,3,4,4,3,3,3,6,7,8,0], # Reihe 1
        [0,2,1,1,1,3,3,1,1,1,2,6,0,9], # Reihe 2
        [0,4,5,5,5,5,7,7,5,5,5,5,0],     # Reihe 3
        [0,0,0,     9     ,0,0,0,0] # Reihe 4 mit Leertaste
]


#: The positions which are by default accessed by the given finger. 
FINGER_POSITIONS = [
    [(1, 1, 0), (2, 1, 0), (3, 1, 0), (3, 2, 0)], # Klein_L
    [(1, 2, 0), (2, 2, 0), (3, 3, 0)], # Ring_L
    [(1, 3, 0), (2, 3, 0), (3, 4, 0)], # Mittel_L
    [(1, 4, 0), (2, 4, 0), (3, 5, 0), (1, 5, 0), (2, 5, 0), (3, 6, 0)], # Zeige_L
    [(4, 3, 0)], # Daumen_L
    [(4, 3, 0)], # Daumen_R
    [(1, 6, 0), (2, 6, 0), (3, 7, 0), (1, 7, 0), (2, 7, 0), (3, 8, 0)], # Zeige_R
    [(1, 8, 0), (2, 8, 0), (3, 9, 0)], # Mittel_R
    [(1, 9, 0), (2, 9, 0), (3, 10, 0)], # Ring_R
    [(1, 10, 0), (2, 10, 0), (3, 11, 0), (1, 11, 0), (2, 11, 0), (1, 12, 0), (2, 12, 0), (2, 13, 0)] # Klein_R
]
#: The names of the fingers for which we gave the positions above.
FINGER_NAMES = ["Klein_L", "Ring_L", "Mittel_L", "Zeige_L", "Daumen_L",
                "Daumen_R", "Zeige_R", "Mittel_R", "Ring_R", "Klein_R"]


### Imports

from copy import deepcopy


### Helper Functions

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

def read_file(path):
    """Get the data from a file.

    >>> read_file("testfile")[:2]
    'ui'
    """

    f = open(path)
    data = f.read()
    f.close()
    return data

def repeats_in_file(data):
    """Sort the repeats in a file by the number of occurrances.

    >>> data = read_file("testfile")
    >>> repeats_in_file(data)[:2]
    [(1, 'ui'), (1, 'td')]
    """
    # TODO: Take uppercase correctly into account -> triple with shift
    data = data.lower()
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
    return sorted_repeats

def letters_in_file(data):
    """Sort the repeats in a file by the number of occurrances.

    >>> data = read_file("testfile")
    >>> repeats_in_file(data)[:2]
    [(1, 'ui'), (1, 'td')]
    """
    # TODO: Take uppercase correctly into account -> triple with shift
    data = data.lower()
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
    [(10162743, 'en'), (10028050, 'er')]
    """
    rep = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    return [(int(num), r) for num, r in rep if rep[1:]]
    
def letters_in_file_precalculated(data):
    """Get the repeats from a precalculated file.

    >>> data = read_file("1gramme.txt")
    >>> letters_in_file_precalculated(data)[:2]
    [(44034982, 'e'), (27012723, 'n')]
    """
    letters = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    return [(int(num), let) for num, let in letters]
    

### Cost Functions

def key_position_cost_from_file(data=None, letters=None, layout=NEO_LAYOUT):
    """Count the total cost due to key positions.

    >>> data = read_file("testfile")
    >>> key_position_cost_from_file(data)
    47
    """
    if data is not None: 
        letters = letters_in_file(data)
    elif letters is None:
        raise Exception("Need either letters or data")
    cost = 0
    for num, letter in letters:
        pos = find_key(letter, layout=layout)
        if pos is None: # not found => next letter
            continue
        cost += num * COST_PER_KEY[pos[0]][pos[1]]
    return cost
    

def finger_repeats_from_file(data=None, repeats=None, count_same_key=False, layout=NEO_LAYOUT):
    """Get a list of two char strings from the file, which repeat the same finger.

    >>> data = read_file("testfile")
    >>> finger_repeats_from_file(data)
    [(1, 'Mittel_R', 'rg'), (1, 'Zeige_L', 'eo'), (1, 'Klein_R', 'd\\n')]
    >>> finger_repeats_from_file(data, count_same_key=True)
    [(1, 'Mittel_R', 'rg'), (1, 'Zeige_L', 'eo'), (1, 'Klein_R', 'd\\n'), (1, 'Mittel_L', 'aa')]
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")
    
    finger_repeats = []
    for number, pair in repeats:
        key1 = pair[0]
        key2 = pair[1]
        finger1 = key_to_finger(key1, layout=layout)
        if finger1 == key_to_finger(key2, layout=layout):
            finger_repeats.append((number, finger1, key1+key2))
    if not count_same_key:
        finger_repeats = [r for r in finger_repeats if not r[2][0] == r[2][1]]
    return finger_repeats

def total_cost(data=None, letters=None, repeats=None, layout=NEO_LAYOUT):
    """Compute a total cost from all costs we have available, wheighted.

    >>> data = read_file("testfile")
    >>> total_cost(data)
    (77, 3, 47)
    """
    # the raw costs
    if data is not None: 
        finger_repeats = finger_repeats_from_file(data, layout=layout)
        position_cost = key_position_cost_from_file(data, layout=layout)
    elif letters is None or repeats is None:
        raise Exception("Need either repeats und letters or data")
    else:
        finger_repeats = finger_repeats_from_file(repeats=repeats, layout=layout)
        position_cost = key_position_cost_from_file(letters=letters, layout=layout)

    frep_num = sum([num for num, fing, rep in finger_repeats])

    total = WEIGHT_FINGER_REPEATS * frep_num + WEIGHT_POSITION * position_cost
    return total, frep_num, position_cost
    

### Evolution

def switch_keys(keypairs, layout=NEO_LAYOUT):
    """Switch keys in the layout, so we don't have to fiddle with actual layout files.

    TODO: REPORT BUG python: Running testmod makes the actual run fail

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
    >>> lay = switch_keys(["lx"], layout = NEO_LAYOUT)
    >>> NEO_LAYOUT_lx == lay
    True
    """
    lay = deepcopy(layout)
    for pair in keypairs:
        pos0 = find_key(pair[0], layout=lay)
        pos1 = find_key(pair[1], layout=lay)
        tmp0 = pair[1] + lay[pos0[0]][pos0[1]][1:]
        tmp1 = pair[0] + lay[pos1[0]][pos1[1]][1:]
        lay[pos0[0]][pos0[1]] = tmp0
        lay[pos1[0]][pos1[1]] = tmp1
    
    return lay


def evolve(letters, repeats, layout=NEO_LAYOUT, iterations=400, quiet=False):
    """Repeatedly switch a layout randomly and do the same with the new layout,
    if it provides a better total score. Can't be tested easily => Check the source."""
    from random import choice
    cost = total_cost(letters=letters, repeats=repeats, layout=layout)[0]
    abc = "abcdefghijklmnopqrstuvwxyzäöüß"
    for i in range(iterations): 
        # 3 switches per iteration
        keypairs = [choice(abc)+choice(abc) for i in range(2)]
        lay = switch_keys(keypairs, layout=deepcopy(layout))
        new_cost, frep, pos_cost = total_cost(letters=letters, repeats=repeats, layout=lay)[:3]
        if new_cost < cost:
            # save the good mutation
            layout = lay
            cost = new_cost
            if not quiet: 
                print(cost / 1000000, keypairs, "finger repetition:", frep / 1000000, "position cost:", pos_cost / 1000000)
                print(lay)
        else:
            if not quiet: 
                print(keypairs, "worse")
    
    return layout, cost
            

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
    
    if "-v" in argv:
        VERBOSE = True
        argv.remove("-v")
    else: VERBOSE = False
    
    if "--help" in argv:
        print(__usage__)
        exit()

    if argv[1:] and argv[1] == "--file":
        path = argv[2]
        data = read_file(path)
        
        if argv[4:] and argv[3] == "--switch":
            switchlist = argv[4].split(",")
            lay = switch_keys(switchlist, layout = NEO_LAYOUT)
            print("Neo", switchlist, "autogenerated")
            frep = finger_repeats_from_file(data, layout=lay)
            print(sum([num for num, fing, rep in frep]) / len(data), "% finger repeats in file", path)
            cost = key_position_cost_from_file(data, layout=lay)
            print(cost / len(data), "mean key position cost in file", path)
        else:
            print("Neo")
            frep = finger_repeats_from_file(data)
            print(sum([num for num, fing, rep in frep]) / len(data), "% finger repeats in file", path)
            cost = key_position_cost_from_file(data)
            print(cost / len(data), "mean key position cost in file", path)

        if VERBOSE: 
            print(unique_sort(frep))

        if not QUIET:         
            print("Qwertz for comparision")
            frep = finger_repeats_from_file(data, layout=QWERTZ_LAYOUT)
            print(sum([num for num, fing, rep in frep]) / len(data), "% finger repeats in file", path)
            cost = key_position_cost_from_file(data, layout=QWERTZ_LAYOUT)
            print(cost / len(data), "mean key position cost in file", path)

    if argv[2:] and argv[1] == "--evolve":
        print("Mutating Neo")
        data1 = read_file("1gramme.txt")
        letters = letters_in_file_precalculated(data1)
        datalen1 = sum([i for i, s in letters])
        
        data2 = read_file("2gramme.txt")
        repeats = repeats_in_file_precalculated(data2)
        datalen2 = sum([i for i, s in repeats])

        lay, cost = evolve(letters, repeats, iterations=int(argv[2]), quiet=QUIET)

        print("\nEvolved Layout")
        from pprint import pprint
        pprint(lay)
        
        frep = finger_repeats_from_file(repeats=repeats, layout=lay)
        print(sum([num for num, fing, rep in frep]) / datalen2, "% finger repeats in file 2gramme.txt")
        cost = key_position_cost_from_file(letters=letters, layout=lay)
        print(cost / datalen1, "mean key position cost in file 1gramme.txt")



    else: 
        print("Neo")
        data1 = read_file("1gramme.txt")
        letters = letters_in_file_precalculated(data1)
        datalen1 = sum([i for i, s in letters])
        
        data2 = read_file("2gramme.txt")
        repeats = repeats_in_file_precalculated(data2)
        datalen2 = sum([i for i, s in repeats])
        
        frep = finger_repeats_from_file(repeats=repeats)#, layout=QWERTZ_LAYOUT)
        print(sum([num for num, fing, rep in frep]) / datalen2, "% finger repeats in file 2gramme.txt")
        cost = key_position_cost_from_file(letters=letters)#, layout=QWERTZ_LAYOUT)
        print(cost / datalen1, "mean key position cost in file 1gramme.txt")

        #print(unique_sort(frep))
        
        #rep = repeats_in_file_sorted(path)
        #print(str(len(rep)), "repeats in file", path, "sorted.")
        #print([i for i in rep if "a" in i[1]])
        
