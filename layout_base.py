#!/usr/bin/env python3

"""Basic functions and constants for working with keyboard layouts."""

def read_file(path):
    """Get the data from a file.

    >>> read_file("testfile")[:2]
    'ui'
    """

    f = open(path, encoding="utf-8")
    data = f.read()
    f.close()
    return data

### get the config

# check if we got one via the commandline (and remove the argument if yes). Otherwise use the default.
from sys import argv
if "--config" in argv: 
    idx = argv.index("--config")
    # the config module is the file without the extension.
    cfg = argv[idx+1][:-3]
    # replace all / and \ with .
    cfg = cfg.replace("/", ".")
    cfg = cfg.replace("\\", ".")
    argv = argv[:idx] + argv[idx+2:]
    exec("from " + cfg + " import *")
else: 
    from config import *

### Constants

#: Die Layout-Datei für Neo = Tastenbelegung - aktuell nur für Reihe 0, 1, 2 und 3 ohne Modifikator-Tasten nutzbar => nur Kleinbuchstaben. 
NEO_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),("←")], # Zahlenreihe (0)
    [("⇥"),("x"),("v"),("l"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [("⇩"),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),("⇘"),("\n")], # Reihe 2
    [("⇧"),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lx = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),("←")], # Zahlenreihe (0)
    [("⇥"),("l"),("v"),("x"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [("⇩"),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),("⇘"),("\n")], # Reihe 2
    [("⇧"),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lxwq = [ # 25% weniger Fingerwiederholungen als Neo, fast 50% weniger als Qwertz
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),("←")], # Zahlenreihe (0)
    [("⇥"),("l"),("v"),("x"),("c"),("q"),("k"),("h"),("g"),("f"),("w"),("ß"),("´"),()], # Reihe 1
    [("⇩"),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),("⇘"),("\n")], # Reihe 2
    [("⇧"),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

QWERTZ_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    [("⇥"),("q"),("w"),("e"),("r"),("t"),("z"),("u"),("i"),("o"),("p"),("ü"),("+"),()], # Reihe 1
    [("⇩"),("a"),("s"),("d"),("f"),("g"),("h"),("j"),("k"),("l"),("ö"),("ä"),("#"),("\n")], # Reihe 2
    [("⇧"),("<"),("y"),("x"),("c"),("v"),("b"),("n"),("m"),(","),("."),("-"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

# from Ulf Bro, http://nordtast.org
NORDTAST_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    [("⇥"),("ä"),("u"),("o"),("b"),("p"),("k"),("g"),("l"),("m"),("f"),("x"),("+"),()], # Reihe 1
    [("⇩"),("a"),("i"),("e"),("t"),("c"),("h"),("d"),("n"),("r"),("s"),("ß"),(),("\n")], # Reihe 2
    [("⇧"),(),("."),(","),("ü"),("ö"),("q"),("y"),("z"),("w"),("v"),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

DVORAK_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    [("⇥"),("’"),(","),("."),("p"),("y"),("f"),("g"),("c"),("r"),("l"),("/"),("="),()], # Reihe 1
    [("⇩"),("a"),("o"),("e"),("u"),("i"),("d"),("h"),("t"),("n"),("s"),("-"),(),("\n")], # Reihe 2
    [("⇧"),(),(";"),("q"),("j"),("k"),("x"),("b"),("m"),("w"),("v"),("z"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

COLEMAK_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    [("⇥"),("q"),("w"),("f"),("p"),("g"),("j"),("l"),("u"),("y"),(";"),("["),("]"),("\\")], # Reihe 1
    [("⇩"),("a"),("r"),("s"),("t"),("d"),("h"),("n"),("e"),("i"),("o"),("`"),(),("\n")], # Reihe 2
    [("⇧"),(),("z"),("x"),("c"),("v"),("b"),("k"),("m"),(","),("."),("/"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]


# Ulfs All fingers equal but the small one
COST_PER_KEY_OLD  = [ # 0 heißt nicht beachtet
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Zahlenreihe (0)
        [0,6,3,3,3,4,4,3,3,3,6,7,8,0], # Reihe 1
        [0,2,1,1,1,3,3,1,1,1,2,6,0,9], # Reihe 2
        [0,4,5,5,5,5,7,7,5,5,5,5,0],     # Reihe 3
        [0,0,0,     9     ,0,0,0,0] # Reihe 4 mit Leertaste
]

# First reweighting
COST_PER_KEY_OLD2  = [ # 0 heißt nicht beachtet
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Zahlenreihe (0)
        [0,6,3,3,3,4,4,3,3,3,6,7,8,0], # Reihe 1
        [0,3,2,2,1,3,3,1,2,2,3,6,0,9], # Reihe 2
        [0,5,5,5,5,5,7,7,5,5,5,5,0],     # Reihe 3
        [0,0,0,     9     ,0,0,0,0] # Reihe 4 mit Leertaste
]

#: The names of the fingers from left to right
FINGER_NAMES = ["Klein_L", "Ring_L", "Mittel_L", "Zeige_L", "Daumen_L",
                "Daumen_R", "Zeige_R", "Mittel_R", "Ring_R", "Klein_R"]

# Optimized structure for accessing by position. key_to_finger gets 3 times faster than with a cache and doublechecking.
KEY_TO_FINGER = {}
for finger in FINGER_POSITIONS:
    for pos in FINGER_POSITIONS[finger]:
        KEY_TO_FINGER[pos] = finger

### Constants for testing
# Weighting for the tests — DON’T CHANGE THIS, it’s necessary for correct testing
TEST_COST_PER_KEY  = [ # 0 heißt nicht beachtet
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Zahlenreihe (0)
        [0, 12,9,6,4,10,10,4,6,9,12,15,18,0], # Reihe 1
        [0,  5,3,3,2,5,5,2,3,3,5,12,0,15], # Reihe 2 
        [15,0,10,11,11,7,12,10,7,11,11,10,15],     # Reihe 3
        [0,0,0,     5     ,0,0,0,0] # Reihe 4 mit Leertaste
]

# Gewichtung der unterschiedlichen Kosten
TEST_WEIGHT_FINGER_REPEATS = 8 #: higher than a switch from center to side, but lower than a switch from center to upper left.
TEST_WEIGHT_FINGER_REPEATS_TOP_BOTTOM = 16 #: 2 times a normal repeat, since it's really slow. Better two outside low or up than an up-down repeat. 
TEST_WEIGHT_POSITION = 1 #: reference
TEST_WEIGHT_FINGER_DISBALANCE = 5 #: multiplied with the standard deviation of the finger usage - value guessed and only valid for the 1gramme.txt corpus.
TEST_WEIGHT_TOO_LITTLE_HANDSWITCHING = 1 #: how high should it be counted, if the hands aren’t switched in a triple?
TEST_WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY = [
    0.5,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    0.5] #: The intended load per finger. Inversed and then used as multiplier for the finger load before calculating the finger disbalance penalty. Any load distribution which strays from this optimum gives a penalty.


### Caches

# together with the more efficient datastructure for key_to_finger, these caches provide a performance boost by about factor 6.6

#_LETTER_TO_KEY_CACHE = {}

# TODO: Refresh directly when mutating. Then we don’t have to check anymore for the letter if it really is at the given position. 

### Imports

from copy import deepcopy


### Helper Functions

def format_layer_1_string(layout):
    """Format a string looking like this:

    öckäy zhmlß,´
    atieo dsnru.
    xpfüq bgvwj
    """
    l = ""
    l += "".join(layout[1][1:6]) + " " + "".join(layout[1][6:-1]) + "\n"
    l += "".join(layout[2][1:6]) + " " + "".join(layout[2][6:-2]) + "\n"
    if layout[3][1]:
        l += "".join(layout[3][1:7]) + " " + "".join(layout[3][7:-1])
    else:
        l += "".join(layout[3][2:7]) + " " + "".join(layout[3][7:-1])
    return l


def get_key(pos, layout=NEO_LAYOUT):
    """Get the key at the given position.

    >>> get_key((2, 3, 0))
    'a'
    """
    try: 
        return layout[pos[0]][pos[1]][pos[2]]
    except: return None

def update_letter_to_key_cache(key, layout):
    """Update the cache entry for the given key."""
    try: LETTER_TO_KEY_CACHE = layout[5]
    except IndexError:
        layout.append({})
        LETTER_TO_KEY_CACHE = layout[5]
    pos = None
    for row in range(len(layout[:5])):
        for col in range(len(layout[row])):
            if key in layout[row][col]: 
                for idx in range(len(layout[row][col])):
                    if layout[row][col][idx] == key: 
                        pos = (row, col, idx)
    LETTER_TO_KEY_CACHE[key] = pos
    return pos

def update_letter_to_key_cache_multiple(keys, layout):
    """Update the cache entries for many keys.

    @param keys: the keys to update. If it’s None, update ALL.
    """
    if keys is None:
        keys = []
        for i in layout:
            for j in i:
                for k in j:
                    if k: 
                        keys.append(k)
    for key in keys:
        update_letter_to_key_cache(key, layout=layout)
    

def diff_dict(d1, d2):
    """find the difference between two dictionaries.

    >>> a = {1: 2, 3: 4}
    >>> b = {1:2, 7:8}
    >>> c = {}
    >>> diff_dict(a, b)
    {3: 4, 7: 8}
    >>> a == diff_dict(a, c)
    True
    """
    diff = {}
    for key in d1:
        if not key in d2: 
            diff[key] = d1[key]
    for key in d2:
        if not key in d1:
            diff[key] = d2[key]
    return diff

def find_key(key, layout): 
    """Find the position of the key in the layout.
    
    >>> find_key("a", NEO_LAYOUT)
    (2, 3, 0)
    """
    # check, if the layout already has a cache. If not, create it.
    # this approach reduces the time to find a key by about 50%.
    # TODO: find out why this change affects the costs of layouts!
    # the cost is raised by a value between 1.2480213606 (NordTast)
    # and 1.2964878374 (Colemak).
    # a part of the change might be, that now uppercase keys
    # are properly taken into account. 
    #if key != key.lower():
    #    raise ValueError("You shall not ask me for upperkey letters (yet)!")

    try: LETTER_TO_KEY_CACHE = layout[5]
    except IndexError:
        layout.append({})
        LETTER_TO_KEY_CACHE = layout[5]
        update_letter_to_key_cache_multiple(None, layout=layout)
    # first check the caches
    try: pos = LETTER_TO_KEY_CACHE[key.lower()]
    except KeyError:
        pos = None # all keys are in there. None means, we don’t need to check.
    #if pos is None or get_key(pos, layout=layout) == key.lower():
    return pos
    # on a cache miss, search the key and refresh the cache
    #return update_letter_to_key_cache(key, layout=layout)


def finger_keys(finger_name, layout=NEO_LAYOUT):
    """Get the keys corresponding to the given finger name.

    >>> for name in FINGER_NAMES:
    ...    name, finger_keys(name)
    ('Klein_L', ['x', '⇩', 'u', '⇧', 'None', 'ü'])
    ('Ring_L', ['v', 'i', 'ö'])
    ('Mittel_L', ['l', 'a', 'ä'])
    ('Zeige_L', ['c', 'e', 'p', 'w', 'o', 'z'])
    ('Daumen_L', [' '])
    ('Daumen_R', [' '])
    ('Zeige_R', ['k', 's', 'b', 'h', 'n', 'm'])
    ('Mittel_R', ['g', 'r', ','])
    ('Ring_R', ['f', 't', '.'])
    ('Klein_R', ['q', 'd', 'j', 'ß', 'y', '´', '⇘', '\\n', '⇗'])
    """
    keys = [str(get_key(pos, layout=layout)) for pos in FINGER_POSITIONS[finger_name]]
    return keys

def key_to_finger(key, layout=NEO_LAYOUT):
    """Get the finger name used to hit the given key.

    >>> key_to_finger("a")
    'Mittel_L'
    >>> key_to_finger("«")
    ''
    >>> key_to_finger("⇩")
    'Klein_L'
    >>> key_to_finger("⇧")
    'Klein_L'
    """
    pos = find_key(key, layout=layout)
    # first check the cache
    finger = KEY_TO_FINGER.get(pos, "")
    return finger


def string_to_layout(layout_string, base_layout=NEO_LAYOUT):
    """Turn a layout_string into a layout.

    öckäy zhmlß,´
    atieo dsnru.
    xpfüq bgvwj

    """
    layout = deepcopy(base_layout)
    lines = layout_string.splitlines()
    # first and second letter row
    for i in range(1, 6):
        layout[1][i] = lines[0][i-1]
        layout[1][i+5] = lines[0][i+5]
        layout[2][i] = lines[1][i-1]
        layout[2][i+5] = lines[1][i+5]
    layout[1][-3] = lines[0][11]
    layout[2][-3] = lines[1][11]
    if lines[0][12:]: 
        layout[1][-2] = lines[0][12]
    
    # third row
    left, right = lines[2].split()[:2]
    for i in range(len(left)):
        layout[3][6-i] = left[-i-1]
    for i in range(len(right)):
        layout[3][7+i] = right[i]

    return layout