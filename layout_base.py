#!/usr/bin/env python3
# encoding: utf-8

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

#: Die Layout-Datei für Neo = Tastenbelegung - Großbuchstaben integriert. 
NEO_LAYOUT = [
    [("^", "ˇ", "↻", "˙", "˞", "̣"),("1", "°", "¹", "ª", "₁", "¬"),("2", "§", "²", "º", "₂", "∨"),("3", "ℓ", "³", "№", "₃", "∧"),
     ("4", "»", "›", "", "♀", "⊥"),("5", "«", "‹", "·", "♂", "∡"),("6", "$", "¢", "£", "⚥", "∥"),("7", "€", "¥", "¤", "ϰ", "→"),
     ("8", "„", "‚", "⇥", "⟨", "∞"),("9", "“", "‘", " /", "⟩", "∝"),("0", "”", "’", "*", "₀", "∅"),("-", "—", "-", "‑", "­"),
     ("`", "¸", "°", "¨", "", "¯"),("←")], # Zahlenreihe (0)

    [("⇥"),("x", "X", "…", "⇞", "ξ", "Ξ"),("v", "V", "_", "⌫", "", "√"),("l", "L", "[", "⇡", "", "λ", "Λ"),
     ("c", "C", "]", "Entf", "χ", "ℂ"),("w", "W", "^", "⇟", "ω", "Ω"),("k", "K", "!", "¡", "κ", "×"),("h", "H", "<", "7", "ψ", "Ψ"),
     ("g", "G", ">", "8", "γ", "Γ"),("f", "F", "=", "9", "φ", "Φ"),("q", "Q", "&", "+", "ϕ", "ℚ"),("ß", "ẞ", "ſ", "−", "ς", "∘"),
     ("´", "~", "/", "˝", "", "˘"),()], # Reihe 1

    [("⇩"),("u", "U", "\\", "⇱", "", "⊂"),("i", "I", "/", "⇠", "ι", "∫"),("a", "A", "{",  "⇣", "α", "∀"),
     ("e", "E", "}", "⇢", "ε", "∃"),("o", "O", "*", "⇲", "ο", "∈"),("s", "S", "?", "¿", "σ", "Σ"),("n", "N", "(", "4", "ν", "ℕ"),
     ("r", "R", ")", "5", "ρ", "ℝ"),("t", "T", "-", "6", "τ", "∂"),("d", "D", ":", ",", "δ", "Δ"),("y", "Y", "@", ".", "υ", "∇"),
     ("⇘"),("\n")], # Reihe 2

    [("⇧"),("⇚"),("ü", "Ü", "\#", "", "", "∪"),("ö", "Ö", "$", "", "ϵ", "∩"),("ä", "Ä", "|", "⎀", "η", "ℵ"),
     ("p", "P", "~", "\n", "π", "Π"),("z", "Z", "`", "↶", "ζ", "ℤ"),("b", "B", "+", ":", "β", "⇐"),("m", "M", "%", "1", "μ", "⇔"),
     (",", "–", '"', "2", "ϱ", "⇒"),(".", "•", "'", "3", "ϑ", "↦"),("j", "J", ";", ";", "θ", "Θ"),("⇗")],        # Reihe 3

    [(), (), (), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lx = [
    [("^", "ˇ", "↻", "˙", "˞", "̣"),("1", "°", "¹", "ª", "₁", "¬"),("2", "§", "²", "º", "₂", "∨"),("3", "ℓ", "³", "№", "₃", "∧"),
     ("4", "»", "›", "", "♀", "⊥"),("5", "«", "‹", "·", "♂", "∡"),("6", "$", "¢", "£", "⚥", "∥"),("7", "€", "¥", "¤", "ϰ", "→"),
     ("8", "„", "‚", "⇥", "⟨", "∞"),("9", "“", "‘", " /", "⟩", "∝"),("0", "”", "’", "*", "₀", "∅"),("-", "—", "-", "‑", "­"),
     ("`", "¸", "°", "¨", "", "¯"),("←")], # Zahlenreihe (0)

    [("⇥"),("l", "L", "…", "⇞", "ξ", "Ξ"),("v", "V", "_", "⌫", "", "√"),("x", "X", "[", "⇡", "", "λ", "Λ"),
     ("c", "C", "]", "Entf", "χ", "ℂ"),("w", "W", "^", "⇟", "ω", "Ω"),("k", "K", "!", "¡", "κ", "×"),("h", "H", "<", "7", "ψ", "Ψ"),
     ("g", "G", ">", "8", "γ", "Γ"),("f", "F", "=", "9", "φ", "Φ"),("q", "Q", "&", "+", "ϕ", "ℚ"),("ß", "ẞ", "ſ", "−", "ς", "∘"),
     ("´", "~", "/", "˝", "", "˘"),()], # Reihe 1

    [("⇩"),("u", "U", "\\", "⇱", "", "⊂"),("i", "I", "/", "⇠", "ι", "∫"),("a", "A", "{",  "⇣", "α", "∀"),
     ("e", "E", "}", "⇢", "ε", "∃"),("o", "O", "*", "⇲", "ο", "∈"),("s", "S", "?", "¿", "σ", "Σ"),("n", "N", "(", "4", "ν", "ℕ"),
     ("r", "R", ")", "5", "ρ", "ℝ"),("t", "T", "-", "6", "τ", "∂"),("d", "D", ":", ",", "δ", "Δ"),("y", "Y", "@", ".", "υ", "∇"),
     ("⇘"),("\n")], # Reihe 2

    [("⇧"),("⇚"),("ü", "Ü", "\#", "", "", "∪"),("ö", "Ö", "$", "", "ϵ", "∩"),("ä", "Ä", "|", "⎀", "η", "ℵ"),
     ("p", "P", "~", "\n", "π", "Π"),("z", "Z", "`", "↶", "ζ", "ℤ"),("b", "B", "+", ":", "β", "⇐"),("m", "M", "%", "1", "μ", "⇔"),
     (",", "–", '"', "2", "ϱ", "⇒"),(".", "•", "'", "3", "ϑ", "↦"),("j", "J", ";", ";", "θ", "Θ"),("⇗")],        # Reihe 3

    [(), (), (), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lxwq = [
    [("^", "ˇ", "↻", "˙", "˞", "̣"),("1", "°", "¹", "ª", "₁", "¬"),("2", "§", "²", "º", "₂", "∨"),("3", "ℓ", "³", "№", "₃", "∧"),
     ("4", "»", "›", "", "♀", "⊥"),("5", "«", "‹", "·", "♂", "∡"),("6", "$", "¢", "£", "⚥", "∥"),("7", "€", "¥", "¤", "ϰ", "→"),
     ("8", "„", "‚", "⇥", "⟨", "∞"),("9", "“", "‘", " /", "⟩", "∝"),("0", "”", "’", "*", "₀", "∅"),("-", "—", "-", "‑", "­"),
     ("`", "¸", "°", "¨", "", "¯"),("←")], # Zahlenreihe (0)

    [("⇥"),("l", "L", "…", "⇞", "ξ", "Ξ"),("v", "V", "_", "⌫", "", "√"),("x", "X", "[", "⇡", "", "λ", "Λ"),
     ("c", "C", "]", "Entf", "χ", "ℂ"),("q", "Q", "^", "⇟", "ω", "Ω"),("k", "K", "!", "¡", "κ", "×"),("h", "H", "<", "7", "ψ", "Ψ"),
     ("g", "G", ">", "8", "γ", "Γ"),("f", "F", "=", "9", "φ", "Φ"),("w", "W", "&", "+", "ϕ", "ℚ"),("ß", "ẞ", "ſ", "−", "ς", "∘"),
     ("´", "~", "/", "˝", "", "˘"),()], # Reihe 1

    [("⇩"),("u", "U", "\\", "⇱", "", "⊂"),("i", "I", "/", "⇠", "ι", "∫"),("a", "A", "{",  "⇣", "α", "∀"),
     ("e", "E", "}", "⇢", "ε", "∃"),("o", "O", "*", "⇲", "ο", "∈"),("s", "S", "?", "¿", "σ", "Σ"),("n", "N", "(", "4", "ν", "ℕ"),
     ("r", "R", ")", "5", "ρ", "ℝ"),("t", "T", "-", "6", "τ", "∂"),("d", "D", ":", ",", "δ", "Δ"),("y", "Y", "@", ".", "υ", "∇"),
     ("⇘"),("\n")], # Reihe 2

    [("⇧"),("⇚"),("ü", "Ü", "\#", "", "", "∪"),("ö", "Ö", "$", "", "ϵ", "∩"),("ä", "Ä", "|", "⎀", "η", "ℵ"),
     ("p", "P", "~", "\n", "π", "Π"),("z", "Z", "`", "↶", "ζ", "ℤ"),("b", "B", "+", ":", "β", "⇐"),("m", "M", "%", "1", "μ", "⇔"),
     (",", "–", '"', "2", "ϱ", "⇒"),(".", "•", "'", "3", "ϑ", "↦"),("j", "J", ";", ";", "θ", "Θ"),("⇗")],        # Reihe 3

    [(), (), (), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ()] # Reihe 4 mit Leertaste
]

# TODO: Add higher layers (shift for the numbers, …)
QWERTZ_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    [("⇥"),("q"),("w"),("e"),("r"),("t"),("z"),("u"),("i"),("o"),("p"),("ü"),("+"),()], # Reihe 1
    [("⇩"),("a"),("s"),("d"),("f"),("g"),("h"),("j"),("k"),("l"),("ö"),("ä"),("#"),("\n")], # Reihe 2
    [("⇧"),("<"),("y"),("x"),("c"),("v"),("b"),("n"),("m"),(",", ";"),(".", ":"),("-"),("⇗")],        # Reihe 3
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

# TODO: Add higher layers (shift for the numbers, …)
DVORAK_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    [("⇥"),("’"),(","),("."),("p"),("y"),("f"),("g"),("c"),("r"),("l"),("/"),("="),()], # Reihe 1
    [("⇩"),("a"),("o"),("e"),("u"),("i"),("d"),("h"),("t"),("n"),("s"),("-"),(),("\n")], # Reihe 2
    [("⇧"),(),(";"),("q"),("j"),("k"),("x"),("b"),("m"),("w"),("v"),("z"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

# TODO: Add higher layers (shift for the numbers, …)
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

TEST_FINGER_SWITCH_COST = { # iu td < ui dt dr ua rd au < ai rt < nd eu
    "Klein_L": {
        "Ring_L": 3, 
        "Mittel_L": 3
        }, 
    "Ring_L": {
        "Klein_L": 4,
        "Mittel_L": 3
        }, 
    "Mittel_L": {
        "Klein_L": 1,
        "Ring_L": 2
        }, 
    "Zeige_L": {
        "Klein_L": 1
        }, 
    "Daumen_L": {
        },
    "Daumen_R": {
        },
    "Zeige_R": {
        "Klein_R": 1
        },
    "Mittel_R": {
        "Ring_R": 2, 
        "Klein_R": 1
        },
    "Ring_R": {
        "Mittel_R": 3,
        "Klein_R": 4
        }, 
    "Klein_R": {
        "Mittel_R": 3,
        "Ring_R": 3
        }
} # iutd, drua, uidt, rdau, airt, ndeu :)


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
    l += "".join((i[0] for i in layout[1][1:6])) + " " + "".join((i[0] for i in layout[1][6:-1])) + "\n"
    l += "".join((i[0] for i in layout[2][1:6])) + " " + "".join((i[0] for i in layout[2][6:-2])) + "\n"
    if layout[3][1]:
        l += "".join((i[0] for i in layout[3][1:7])) + " " + "".join((i[0] for i in layout[3][7:-1]))
    else:
        l += "".join((i[0] for i in layout[3][2:7])) + " " + "".join((i[0] for i in layout[3][7:-1]))
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
                key_num = len(layout[row][col])
                for idx in range(key_num):
                    # make sure that the keys on lower levels always win agains those on higher levels.
                    # TODO (maybe someday): update the scheme to allow for multiple positions ⇒ only take the lowest cost.
                    idx_rev = key_num - idx -1
                    if layout[row][col][idx_rev] == key:
                        if pos and pos[2] < idx_rev:
                            continue
                        pos = (row, col, idx_rev)
    LETTER_TO_KEY_CACHE[key] = pos
    return pos

def update_letter_to_key_cache_multiple(keys, layout):
    """Update the cache entries for many keys.

    @param keys: the keys to update. If it’s None, update ALL.
    """
    if keys is None:
        keys = []
        for line in layout:
            for key in line:
                for letter in key:
                    if letter: 
                        keys.append(letter)
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
    >>> find_key("A", NEO_LAYOUT)
    (2, 3, 1)
    >>> find_key("e", NEO_LAYOUT)
    (2, 4, 0)
    >>> find_key(",", NEO_LAYOUT)
    (3, 9, 0)
    >>> find_key("⇧", layout=NEO_LAYOUT)
    (3, 0, 0)
    >>> find_key("A", layout=QWERTZ_LAYOUT)
    (2, 1, 1)
    >>> find_key("a", layout=QWERTZ_LAYOUT)
    (2, 1, 0)
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
    try: pos = LETTER_TO_KEY_CACHE[key]
    except KeyError:
        # maybe we didn’t add the uppercase key, should only happen for incomplete layouts.
        try: 
            pos = LETTER_TO_KEY_CACHE[key.lower()]
            if not pos[2]: # == 0
                pos = pos[:2] + (1,) # this is an uppercase key.
        except KeyError: 
            pos = None # all keys are in there. None means, we don’t need to check by hand.
    return pos


def finger_keys(finger_name, layout=NEO_LAYOUT):
    """Get the keys corresponding to the given finger name.

    >>> for name in FINGER_NAMES:
    ...    name, finger_keys(name)
    ('Klein_L', ['x', '⇩', 'u', '⇧', '⇚', 'ü'])
    ('Ring_L', ['v', 'i', 'ö'])
    ('Mittel_L', ['l', 'a', 'ä'])
    ('Zeige_L', ['c', 'e', 'p', 'w', 'o', 'z'])
    ('Daumen_L', [' '])
    ('Daumen_R', [' ', '⇙'])
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
    >>> key_to_finger("A")
    'Mittel_L'
    >>> key_to_finger("«")
    ''
    >>> key_to_finger("⇩")
    'Klein_L'
    >>> key_to_finger("⇧")
    'Klein_L'
    """
    pos = find_key(key, layout=layout)
    try: pos = pos[:2] + (0, )
    except TypeError: return "" # pos is None
    # first check the cache
    try: return KEY_TO_FINGER[pos]
    except KeyError: return ""


def pos_is_left(pos):
    """check if the given position is on the left hand.

    >>> clear_left_positions = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0)]
    >>> False in [pos_is_left(pos) for pos in clear_left_positions]
    False
    
    """
    return RIGHT_HAND_LOWEST_INDEXES[pos[0]] > pos[1]


def string_to_layout(layout_string, base_layout=NEO_LAYOUT):
    """Turn a layout_string into a layout.

    öckäy zhmlß,´
    atieo dsnru.
    xpfüq bgvwj

    """
    layout = deepcopy(base_layout)
    lines = layout_string.splitlines()
    # first and second letter row, the ifs are for replacing the second layer with uppercase, where aplicable. 
    for i in range(1, 6):
        if lines[0][i-1].upper() == lines[0][i-1]: # nonstandard keys. 
            layout[1][i] = (lines[0][i-1], ) + tuple(layout[1][i][1:])
        else:
            layout[1][i] = (lines[0][i-1], lines[0][i-1].upper()) + tuple(layout[1][i][2:])

        if lines[0][i+5].upper() == lines[0][i+5]: # nonstandard keys. 
            layout[1][i+5] = (lines[0][i+5], ) + tuple(layout[1][i+5][1:])
        else:
            layout[1][i+5] = (lines[0][i+5], lines[0][i+5].upper()) + tuple(layout[1][i+5][2:])

        if lines[0][i-1].upper() == lines[0][i-1]: # nonstandard keys. 
            layout[2][i] = (lines[1][i-1], ) + tuple(layout[2][i][1:])
        else: 
            layout[2][i] = (lines[1][i-1], lines[1][i-1].upper()) + tuple(layout[2][i][2:])

        if lines[0][i-1].upper() == lines[0][i-1]: # nonstandard keys. 
            layout[2][i+5] = (lines[1][i+5], ) + tuple(tuple(layout[2][i+5][1:]))
        else: 
            layout[2][i+5] = (lines[1][i+5], lines[1][i+5].upper()) + tuple(tuple(layout[2][i+5][2:]))

    if lines[0][11].upper() == lines[0][11]: 
        layout[1][-3] = (lines[0][11], ) + tuple(layout[1][-3][1:])
    else:
        layout[1][-3] = (lines[0][11], lines[0][11].upper()) + tuple(layout[1][-3][2:])

    if lines[1][11].upper() == lines[1][11]: 
        layout[2][-3] = (lines[1][11], ) + tuple(layout[2][-3][1:])
    else:
        layout[2][-3] = (lines[1][11], lines[1][11].upper()) + tuple(layout[2][-3][2:])

    if lines[0][12:]:
        if lines[0][12].upper() == lines[0][12]: 
            layout[1][-2] = (lines[0][12], ) + tuple(layout[1][-2][1:])
        else:
            layout[1][-2] = (lines[0][12], lines[0][12].upper()) + tuple(layout[1][-2][2:])
    
    # third row
    left, right = lines[2].split()[:2]
    for i in range(len(left)):
        if left[-i-1].upper() == left[-i-1]: 
            layout[3][6-i] = (left[-i-1], ) + tuple(layout[3][6-i][1:])
        else:
            layout[3][6-i] = (left[-i-1], left[-i-1].upper()) + tuple(layout[3][6-i][2:])
    for i in range(len(right)):
        if right[i].upper() == right[i]: 
            layout[3][7+i] = (right[i], ) + tuple(layout[3][7+i][1:])
        else:
            layout[3][7+i] = (right[i], right[i].upper()) + tuple(layout[3][7+i][2:])

    return layout


if __name__ == "__main__":
    from doctest import testmod
    testmod()
