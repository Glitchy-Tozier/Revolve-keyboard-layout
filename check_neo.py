#!/usr/bin/env python3
# encoding: utf-8

"""Check the neo keyboard for double-usage of the same finger.

"""
__usage__ = """Usage:

- check_neo.py --help (display this text)

- check_neo.py [-q] [-v]
  compare the Neo layout with others, using the included datafiles(*gramme.txt). 
  -q only shows the results for the Neo layout.
  -v shows several additional metrics which are included in the total cost.

- check_neo.py --file <file> [--switch <lx,wq>] [-q] [-v]
  run the script on the file. 
  --switch switches letters on the neo keyboard (lx,wq switches l for x and w for q). 
  -q removes the qwertz comparision.
  -v adds the list of finger repeats.

- check_neo.py --evolve <iterations> [--prerandomize <num_switches>] [-q] [-v] [--controlled-evolution]
  randomly permutate keys on the Neo keyboard to see if a better layout emerges. 
  --controlled-evolution tells it to use the horribly slow and deterministic code which always chooses the best possible change in each step.
  --prerandomize tells it to do num_switches random switches before beginning the evolution. Use >100000 to get a mostly random keyboard layout as starting point.

- check_neo.py --best-random-layout <num of random layouts to try> [--prerandomize <num_switches>] [-q]
  --prerandomize selects the number of random switches to do to get a random keyboard.

- check_neo.py --check " [['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '\\`', ()],
[(), 'ß', '.', 'o', 'l', 'w', 'z', 'h', 'a', 'f', 'ö', 'x', '\\´', ()],
 ['⇩', 'r', 'i', 't', 'n', 'c', 'g', 'd', 'e', 's', 'u', 'y', '⇘', '\\n'],
 ['⇧', (), ',', 'p', 'j', 'm', 'q', 'k', 'b', 'ä', 'v', 'ü', '⇗'],
 [(), (), (), ' ', (), (), (), ()]]
" [-q]
  check the layout passed on the commandline (mind the shell escapes!)

- check_neo.py --test (run doctests)

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
- Groß- und Kleinschreibung kann durch einen preprocessor gemacht werden, der „vrtuelle Zeichen“ vor dem eigentlichen Zeichen einfügt. - DONE
- TODO: Kosten und Finger für Shift; teilerledigt: Kleine Finger bedienen Shift.
- Wettbewerb: Viele Zufällige, dann jeweils Evolution (1000?), dann Auswahl der ersten Hälfte und kombinieren der Layouts (for i in [a:z]: if rand_bool(): 1.switch(1, 2.key_at(1.pos(i))])


Vorgehensweise zur Optimierung:
- Annahme: Es gibt eine Idealtastatur. Mit ihr können Gedanken ohne Zeitverlust und ohne Aufwand aufgezeichnet werden.
- Reale Tastaturen können sich dem Ideal immer nur annähern. Daher arbeiten wir mit „Kosten im Vergleich zur Idealtastatur“. Die Minimierung der Kosten gibt einen Hinweis darauf, wie eine der Idealtastatur möglichst nahe kommende Tastatur aussehen kann.
- Ein Programm kann nur die einfachsten Faktoren berücksichtigen, da es Quantisierung benötigt. Deshalb muss eine Optimierung von Menschen geprüft werden, und Ästethik und Intuition (also menschliches Feingefühle mit viel komplexerer Grundlage: Quantitative + Qualitative Faktoren) gelten mehr als reine Zahlenspielerei. Die Maschine kann aber Vorarbeit leisten und stupides Prüfen übernehmen. 
- Die deutsche Standardtastatur gilt als „Infrastauktur“. Das Layout muss auf ihr funktionieren. 
- Als Daten-Grundlage dient die Liste der N-Gramme. Für die aktuellen brauchen wir nur Mono- und Bigramme, aber auch Trigramme sind vorbereitet.
  (aus dem Korpus der Uni Leipzig generiert:
  * http://lists.neo-layout.org/pipermail/diskussion/2009-November/015057.html (mit Link auf den Korpus)
  * http://lists.neo-layout.org/pipermail/diskussion/2009-December/015238.html (generierung der N-Gramme)
  )
- Paradigmen: http://wiki.neo-layout.org/wiki/Paradigmen

### Kostenfaktoren

(in Klammer diejenigen, die noch debattiert werden)

Kostenfaktor: Zeit
- Unterschiedlich schnell zu erreichende Tasten => Kosten für einzelne Tasten. - done ; 
  TODO: Gesamtbelastung der Finger auskoppeln und rein auf Erreichberkeit der Tasten gehen. 
  Die Zusatzkosten fur den kleinen Finger sollten nur durch die Gesamtbelistung kommen. 
- Einen Finger mehrfach hintereinander verwenden. => Strafpunkte. - done
- Einen Finger mehrfach, von oben nach ganz unten. => viele Strafpunkte. - done
- Handwechsel sparen Zeit => Wenn bei tripeln alle 3 Zeichen auf der gleichen Hand sind, bringt das Strafpunkte. - done
- Der Zeige- und Mittelfinger sind schneller oben und unten als die beiden anderen => Kosten für Einzeltasten anpassen. - TODO
  (aus http://forschung.goebel-consult.de/de-ergo/rohmert/Rohmert.html)

Kostenfaktor: Belastung
- Ungleichmäßige Belastung beider Hände. => indirekt durch Strafpunkte bei fehlendem Handwechsel und direkt, weil das auch ungleiche Belastung der Finger bewirkt- done
- Ungleichmäßige Belastung der einzelnen Finger (allerdings sollte der Kleine weniger belastet werden). => Finger zählen, kleinen doppelt gewichten. Strafpunkte für Abweichung vom Durchschnitt (quadratisch?) ?? - done (std)

Kostenfaktor: Natürliche Handbewegung
- Zeilenwechsel ohne Handwechsel kostet Anstrengung => Malus für den Wechsel der Zeile in einem Bigramm auf der gleichen Hand. Malus = (Anzahl Zeilen)²- done
- (Von außen nach innen. => von innen nach außen auf der gleichen Hand gibt Strafpunkte. Stattdessen vielleicht: Kein Richtungswechsel der Finger einer Hand. - TODO)
- (Links gleicher Finger wie rechts. => Fingerwechsel bei Handwechsel hat Kosten. - TODO)
- (Zwei Finger nebeneinander auf der gleichen Hand, aber nicht Mittel- und Ringfinger. -> bei Tripeln: wenn zwei Tasten auf der gleichen Hand liegen, sollten sie aufeinander folgen  => Wenn der Ringfinger auf den Mittelfinger folgt oder umgekehrt gibt es Strafpunkte (bei  bigrammen) Gegenpunkt: Direkt nebeneinander liegende Finger ein Nachteil? - TODO)
  (von http://www.michaelcapewell.com/projects/keyboard/layout_capewell.htm und http://mkweb.bcgsc.ca/carpalx/?typing_effort)

Sonstiges:
- XCV sollten gut erreichbar auf der linken Hand liegen. => Strafpunkte, wenn pos[2] > 3. z.B. Kosten bei den Monogrammen * 0.005 (0.5%), bzw. Kosten pro Zeichen. Vielleicht auch Z dazu (undo). - done. 
- . sollte neben , liegen. Das sind mit dem leerzeichen die einzigen beiden Zeichen, die keine echten Buchstaben sind. -TODO


### Kosten für die Tasten

Da die Belastung der Finger bereits *pro Finger* gerechnet wird, sollte darüber auch die Unterscheidung zwischen Fingern gemacht werden. → WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY

Das sollte dann der inversen Geschwindigkeit der Finger entsprechen, normiert auf den Kleinen Finger und modifiziert durch die Belastbarkeit. Die liste sagt “so viel Last wolle nwir auf dem Finger”. Dadurch können dann die Kosten pro Taste alleine auf der Erreichbarkeit der Tasten relativ zur Grundlinie aufgebaut werden. 

Bisher verwende ich 

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

Vorschläge: 
→ http://lists.neo-layout.org/pipermail/diskussion/2008-July/007551.html
→ http://lists.neo-layout.org/pipermail/diskussion/2008-July/007569.html
→ http://lists.neo-layout.org/pipermail/diskussion/2008-July/007570.html
→ http://lists.neo-layout.org/pipermail/diskussion/2010-March/016156.html

### Weitere Notizen

Mehrere Leute nutzen einen „Tastaturwettbewerb”: Mit zufälligen anfangen, die besten behalten und aus ihnen neue mutieren. -> http://klausler.com/evolved.html

Quellen für Wortlisten:
- Natural language toolkit: http://code.google.com/p/nltk/
-   * http://lists.neo-layout.org/pipermail/diskussion/2009-November/015057.html (mit Link auf den Korpus)
    * http://lists.neo-layout.org/pipermail/diskussion/2009-December/015238.html (generierung der N-Gramme) 

"""

__results__ = """

"""

__doc__ += __usage__ + __design__

__version__ = "0.1.2"

__copyright__ = """2010 © Arne Babenhauserheide

License: GPLv3 or later
"""

### Constants

# Gewichtung der unterschiedlichen Kosten
WEIGHT_POSITION = 1 #: reference
WEIGHT_FINGER_REPEATS = 8 #: higher than a switch from center to side, but lower than a switch from center to upper left.
WEIGHT_FINGER_REPEATS_TOP_BOTTOM = 16 #: 2 times a normal repeat, since it's really slow. Better two outside low or up than an up-down repeat. 
WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW = 2 #: When I have to switch the row in a bigram while on the same hand, that takes time => Penalty per row to cross if we’re on the same hand. 
WEIGHT_FINGER_DISBALANCE = 5 #: multiplied with the standard deviation of the finger usage - value guessed and only valid for the 1gramme.txt corpus.
WEIGHT_TOO_LITTLE_HANDSWITCHING = 1 #: how high should it be counted, if the hands aren’t switched in a triple?
WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY = [
    1,
    2,
    2,
    3,
    1,
    1,
    3,
    2,
    2,
    1] #: The intended load per finger. Inversed and then used as multiplier for the finger load before calculating the finger disbalance penalty. Any load distribution which strays from this optimum gives a penalty.
WEIGHT_XCVZ_ON_BAD_POSITION = 0.1 #: the penalty *per letter* in the text if xvcz are on bad positions (cumulative; if all 4 are on bad positions (not in the first 5 keys, counted from the left side horizontally) we get 4 times the penalty). 

#: Die zu mutierenden Buchstaben.
abc = "abcdefghijklmnopqrstuvwxyzäöüß,."

#: Die Layout-Datei für Neo = Tastenbelegung - aktuell nur für Reihe 0, 1, 2 und 3 ohne Modifikator-Tasten nutzbar => nur Kleinbuchstaben. 
NEO_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),()], # Zahlenreihe (0)
    [(),("x"),("v"),("l"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [("⇩"),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),("⇘"),("\n")], # Reihe 2
    [("⇧"),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lx = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),()], # Zahlenreihe (0)
    [(),("l"),("v"),("x"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [("⇩"),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),("⇘"),("\n")], # Reihe 2
    [("⇧"),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lxwq = [ # 25% weniger Fingerwiederholungen als Neo, fast 50% weniger als Qwertz
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),()], # Zahlenreihe (0)
    [(),("l"),("v"),("x"),("c"),("q"),("k"),("h"),("g"),("f"),("w"),("ß"),("´"),()], # Reihe 1
    [("⇩"),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),("⇘"),("\n")], # Reihe 2
    [("⇧"),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

QWERTZ_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),()], # Zahlenreihe (0)
    [(),("q"),("w"),("e"),("r"),("t"),("z"),("u"),("i"),("o"),("p"),("ü"),("+"),()], # Reihe 1
    [(),("a"),("s"),("d"),("f"),("g"),("h"),("j"),("k"),("l"),("ö"),("ä"),(),("\n")], # Reihe 2
    [("⇧"),(),("y"),("x"),("c"),("v"),("b"),("n"),("m"),(","),("."),("-"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

NORDTAST_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),()], # Zahlenreihe (0)
    [(),("ä"),("u"),("o"),("b"),("p"),("k"),("g"),("l"),("m"),("f"),("x"),("+"),()], # Reihe 1
    [(),("a"),("i"),("e"),("t"),("c"),("h"),("d"),("n"),("r"),("s"),("ß"),(),("\n")], # Reihe 2
    [("⇧"),(),("."),(","),("ü"),("ö"),("q"),("y"),("z"),("w"),("v"),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

DVORAK_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),()], # Zahlenreihe (0)
    [(),("’"),(","),("."),("p"),("y"),("f"),("g"),("c"),("r"),("l"),("/"),("="),()], # Reihe 1
    [(),("a"),("o"),("e"),("u"),("i"),("d"),("h"),("t"),("n"),("s"),("-"),(),("\n")], # Reihe 2
    [("⇧"),(),(";"),("q"),("j"),("k"),("x"),("b"),("m"),("w"),("v"),("z"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

COLEMAK_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),()], # Zahlenreihe (0)
    [(),("q"),("w"),("f"),("p"),("g"),("j"),("l"),("u"),("y"),(";"),("["),("]"),("\\")], # Reihe 1
    [(),("a"),("r"),("s"),("t"),("d"),("h"),("n"),("e"),("i"),("o"),("`"),(),("\n")], # Reihe 2
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


# Structured reweighting (but still mostly from experience and deducing from the work of others).
# The speed of the fingers is taken out (see INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY).
# THis shows the reachability of the keys, ignoring the different speed of the fingers.
# “How much does the hand hurt when reaching for the key” :)
# rationale: reaching for the Neo2 x hurts thrice as much as just hitting the Neo2 u → 10 vs. 3.
# the upper keys on the right hand can be reached a bit better, since movement is aligned with the hand
# (except for q, since the pinky is too short for that).
# theoretical minimum (assigning the lowest cost to the most frequent char, counting only the chars on layer 1):
# 1123111113 = 3.3490913205386508 mean key position cost
COST_PER_KEY  = [ # the 0 values aren’t filled in at the moment. 
    [0,     0, 0, 0, 0, 0,     0, 0, 0, 0, 0, 0, 0, 0], # Zahlenreihe (0)
    [0,    10, 6, 6, 8, 9,    10, 5, 5, 5, 8, 6,18, 0], # Reihe 1
    [0,     3, 3, 3, 3, 5,     5, 3, 3, 3, 3, 5,10,18], # Reihe 2
    [15,10,12,12,10, 10,   15, 7, 6,11,11,10,15],     # Reihe 3
    [0,0,0,               3    , 0, 0, 0, 0] # Reihe 4 mit Leertaste
]



#: The positions which are by default accessed by the given finger. 
FINGER_POSITIONS = [
    [(1, 1, 0), (2, 0, 0), (2, 1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0)], # Klein_L
    [(1, 2, 0), (2, 2, 0), (3, 3, 0)], # Ring_L
    [(1, 3, 0), (2, 3, 0), (3, 4, 0)], # Mittel_L
    [(1, 4, 0), (2, 4, 0), (3, 5, 0), (1, 5, 0), (2, 5, 0), (3, 6, 0)], # Zeige_L
    [(4, 3, 0)], # Daumen_L
    [(4, 3, 0)], # Daumen_R
    [(1, 6, 0), (2, 6, 0), (3, 7, 0), (1, 7, 0), (2, 7, 0), (3, 8, 0)], # Zeige_R
    [(1, 8, 0), (2, 8, 0), (3, 9, 0)], # Mittel_R
    [(1, 9, 0), (2, 9, 0), (3, 10, 0)], # Ring_R
    [(1, 10, 0), (2, 10, 0), (3, 11, 0), (1, 11, 0), (2, 11, 0), (1, 12, 0), (2, 12, 0), (2, 13, 0), (3, 12, 0)] # Klein_R
]
#: The names of the fingers for which we gave the positions above.
FINGER_NAMES = ["Klein_L", "Ring_L", "Mittel_L", "Zeige_L", "Daumen_L",
                "Daumen_R", "Zeige_R", "Mittel_R", "Ring_R", "Klein_R"]


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
            if key in layout[row][col]: 
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
    idx = FINGER_NAMES.index(finger_name)
    keys = [str(get_key(pos, layout=layout)) for pos in FINGER_POSITIONS[idx]]
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
    for i in range(len(FINGER_POSITIONS)):
        if pos in FINGER_POSITIONS[i]:
            return FINGER_NAMES[i]
    return ""

def read_file(path):
    """Get the data from a file.

    >>> read_file("testfile")[:2]
    'ui'
    """

    f = open(path, encoding="UTF-8")
    data = f.read()
    f.close()
    return data

def split_uppercase_repeats(reps):
    """Split uppercase repeats into two to three lowercase repeats.

    TODO: treat left and right shift differently. Currently we always use both shifts (⇧ and ⇗) and half the value (but stay in integers => 1 stays 1). Needs major refactoring, since it needs knowledge of the layout. Temporary fix: always use both shifts.

    >>> reps = [(12, "ab"), (6, "Ab"), (4, "aB"), (1, "AB")]
    >>> split_uppercase_repeats(reps)
    [(12, 'ab'), (6, 'ab'), (3, '⇧a'), (3, '⇗a'), (2, '⇧b'), (2, '⇗b'), (2, 'a⇧'), (2, 'a⇗'), (1, '⇧b'), (1, '⇧a'), (1, '⇗b'), (1, '⇗a'), (1, 'a⇧'), (1, 'a⇗')]
    """
    # replace uppercase by ⇧ + char1 and char1 + char2
    upper = [(num, rep) for num, rep in reps if not rep == rep.lower()]
    reps = [rep for rep in reps if not rep in upper]
    up = []
    for num, rep in upper: # Ab = ⇧a,ab aB = a⇧,⇧b AB = ⇧a,a⇧,⇧b
        # use both shifts, but half weight each
        if not rep[0] == rep[0].lower():
            up.append((max(1, int(num/2)), "⇧"+rep[0].lower()))
            up.append((max(1, int(num/2)), "⇗"+rep[0].lower()))
        if not rep[1] == rep[1].lower():
            up.append((max(1, int(num/2)), "⇧"+rep[1].lower()))
            up.append((max(1, int(num/2)), rep[0].lower() + "⇧"))
            up.append((max(1, int(num/2)), "⇗"+rep[1].lower()))
            up.append((max(1, int(num/2)), rep[0].lower() + "⇗"))
        else:
            up.append((num, rep[0].lower()+rep[1].lower()))
                
    reps.extend(up)
    reps = [(int(num), r) for num, r in reps if r[1:]]
    reps.sort()
    reps.reverse()
    return reps

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
    sorted_repeats = [(repeats[i], i) for i in repeats]
    sorted_repeats.sort()
    sorted_repeats.reverse()
    reps = split_uppercase_repeats(sorted_repeats)
    return reps

def split_uppercase_letters(reps):
    """Split uppercase letters into two lowercase letters (with shift).

    >>> letters = [(4, "a"), (3, "A")]
    >>> split_uppercase_letters(letters)
    [(4, 'a'), (3, '⇧'), (3, 'a')]
    """
    # replace uppercase by ⇧ + char1 and char1 + char2
    upper = [(num, rep) for num, rep in reps if not rep == rep.lower()]
    reps = [rep for rep in reps if not rep in upper]
    up = []
    for num, rep in upper: # Ab = ⇧a,ab aB = a⇧,⇧b AB = ⇧a,a⇧,⇧b
        up.append((num, "⇧"))
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
    [(5, 'a'), (4, '\\n'), (2, '⇧')]
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
    sort = split_uppercase_letters(sort)
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
    reps = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    reps = [(int(num), r) for num, r in reps if r[1:]]
    reps = split_uppercase_repeats(reps)
    
    return reps


def split_uppercase_trigrams(trigs):
    """Split uppercase repeats into two to three lowercase repeats.

    TODO: Adapt to Trigrams.
    TODO: treat left and right shift differently. Currently we always use left shift and never right shift (⇗).

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
            up.append((max(1, int(num/2)), "⇧"+trig[:2].lower()))
            up.append((max(1, int(num/2)), "⇗"+trig[:2].lower()))
            up.append((num, trig.lower()))
        # aBc
        elif trig[0] == trig[0].lower() and not trig[1] == trig[1].lower() and trig[2] == trig[2].lower():
            up.append((max(1, int(num/2)), "⇧"+trig[1:].lower()))
            up.append((max(1, int(num/2)), "⇗"+trig[1:].lower()))
            up.append((max(1, int(num/2)), trig[0].lower()+"⇧"+trig[1].lower()))
            up.append((max(1, int(num/2)), trig[0].lower()+"⇗"+trig[1].lower()))
            
        # abC
        elif trig[0] == trig[0].lower() and trig[1] == trig[1].lower() and not trig[2] == trig[2].lower():
            up.append((max(1, int(num/2)), trig[:2].lower() + "⇧"))
            up.append((max(1, int(num/2)), trig[:2].lower() + "⇗"))
            up.append((max(1, int(num/2)), trig[1].lower()+"⇧"+trig[2].lower()))
            up.append((max(1, int(num/2)), trig[1].lower()+"⇗"+trig[2].lower()))
            
        # ABc (4, '⇧a⇧'), (4, 'a⇧b'), (4, '⇧bc')
        elif not trig[0] == trig[0].lower() and not trig[1] == trig[1].lower() and trig[2] == trig[2].lower():
            up.append((max(1, int(num/4)), "⇧"+trig[0].lower()+"⇧"))
            up.append((max(1, int(num/2)), trig[0].lower()+"⇧"+trig[1].lower()))
            up.append((max(1, int(num/2)),  "⇧" + trig[1:].lower()))
            
            up.append((max(1, int(num/4)), "⇗"+trig[0].lower()+"⇧"))
            up.append((max(1, int(num/4)), "⇧"+trig[0].lower()+"⇗"))
            up.append((max(1, int(num/4)), "⇗"+trig[0].lower()+"⇗"))

            up.append((max(1, int(num/2)), trig[0].lower()+"⇗"+trig[1].lower()))
            up.append((max(1, int(num/2)),  "⇗" + trig[1:].lower()))
            
        # aBC (3, 'a⇧b'), (3, '⇧b⇧'), (3, 'b⇧c')
        elif trig[0] == trig[0].lower() and not trig[1] == trig[1].lower() and not trig[2] == trig[2].lower():
            up.append((max(1, int(num/4)), "⇧"+trig[1].lower()+"⇧"))
            up.append((max(1, int(num/2)), trig[0].lower()+"⇧"+trig[1].lower()))
            up.append((max(1, int(num/2)), trig[1].lower()+"⇧"+trig[2].lower()))
            
            up.append((max(1, int(num/4)), "⇗"+trig[1].lower()+"⇧"))
            up.append((max(1, int(num/4)), "⇧"+trig[1].lower()+"⇗"))
            up.append((max(1, int(num/4)), "⇗"+trig[1].lower()+"⇗"))

            up.append((max(1, int(num/2)), trig[0].lower()+"⇗"+trig[1].lower()))
            up.append((max(1, int(num/2)), trig[1].lower()+"⇗"+trig[2].lower()))
            
        # AbC (2, '⇧ab'), (2, 'ab⇧'), (2, 'b⇧c')
        elif not trig[0] == trig[0].lower() and trig[1] == trig[1].lower() and not trig[2] == trig[2].lower():
            up.append((max(1, int(num/2)),  "⇧" + trig[:2].lower()))
            up.append((max(1, int(num/2)),  trig[:2].lower() + "⇧"))
            up.append((max(1, int(num/2)), trig[1].lower()+"⇧"+trig[2].lower()))
            
            up.append((max(1, int(num/2)),  "⇗" + trig[:2].lower()))
            up.append((max(1, int(num/2)),  trig[:2].lower() + "⇗"))
            up.append((max(1, int(num/2)), trig[1].lower()+"⇗"+trig[2].lower()))

        # ABC (1, '⇧a⇧'), (1, 'a⇧b'), (1, '⇧b⇧'), (1, 'b⇧c')
        elif not trig[0] == trig[0].lower() and not trig[1] == trig[1].lower() and not trig[2] == trig[2].lower():
            up.append((max(1, int(num/4)), "⇧"+trig[0].lower()+"⇧"))
            up.append((max(1, int(num/2)), trig[0].lower()+"⇧"+trig[1].lower()))
            up.append((max(1, int(num/4)), "⇧"+trig[1].lower()+"⇧"))
            up.append((max(1, int(num/2)), trig[1].lower()+"⇧"+trig[2].lower()))
            
            up.append((max(1, int(num/4)), "⇗"+trig[0].lower()+"⇧"))
            up.append((max(1, int(num/4)), "⇧"+trig[0].lower()+"⇗"))
            up.append((max(1, int(num/4)), "⇗"+trig[0].lower()+"⇗"))

            up.append((max(1, int(num/4)), "⇗"+trig[1].lower()+"⇧"))
            up.append((max(1, int(num/4)), "⇧"+trig[1].lower()+"⇗"))
            up.append((max(1, int(num/4)), "⇗"+trig[1].lower()+"⇗"))

            up.append((max(1, int(num/2)), trig[0].lower()+"⇗"+trig[1].lower()))
            up.append((max(1, int(num/2)), trig[1].lower()+"⇗"+trig[2].lower()))

    
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
    [(5679632, 'en '), (4417443, 'er '), (2891983, ' de'), (2303238, 'der'), (2273056, 'ie '), (2039537, 'ich')]
    """
    trigs = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    trigs = [(int(num), r) for num, r in trigs if r[1:]]
    trigs = split_uppercase_trigrams(trigs)
    
    return trigs

def letters_in_file_precalculated(data):
    """Get the repeats from a precalculated file.

    >>> data = read_file("1gramme.txt")
    >>> letters_in_file_precalculated(data)[:2]
    [(44034982, 'e'), (27012723, 'n')]
    """
    letters = [line.lstrip().split(" ", 1) for line in data.splitlines() if line.split()[1:]]
    return [(int(num), let) for num, let in letters]
    

### Cost Functions

def key_position_cost_from_file(data=None, letters=None, layout=NEO_LAYOUT, cost_per_key=COST_PER_KEY):
    """Count the total cost due to key positions.

    >>> data = read_file("testfile")
    >>> key_position_cost_from_file(data, cost_per_key=TEST_COST_PER_KEY)
    150
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
        cost += num * cost_per_key[pos[0]][pos[1]]
    return cost

def finger_repeats_from_file(data=None, repeats=None, count_same_key=False, layout=NEO_LAYOUT):
    """Get a list of two char strings from the file, which repeat the same finger.

    >>> data = read_file("testfile")
    >>> finger_repeats_from_file(data)
    [(1, 'Mittel_R', 'rg'), (1, 'Zeige_L', 'eo'), (1, 'Klein_R', 'd\\n')]
    >>> finger_repeats_from_file(data, count_same_key=True)
    [(2, 'Mittel_L', 'aa'), (1, 'Mittel_R', 'rg'), (1, 'Zeige_L', 'eo'), (1, 'Klein_R', 'd\\n'), (1, 'Mittel_L', 'aa')]
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
        finger2 = key_to_finger(key2, layout=layout)
        if finger1 and finger2 and finger1 == finger2:
            finger_repeats.append((number, finger1, key1+key2))
    if not count_same_key:
        finger_repeats = [r for r in finger_repeats if not r[2][0] == r[2][1]]
    return finger_repeats

def finger_repeats_top_and_bottom(finger_repeats):
    """Check which of the finger repeats go from the top to the bottom row or vice versa."""
    top_down_repeats = []
    for number, finger, letters in finger_repeats:
        pos0 = find_key(letters[0])
        pos1 = find_key(letters[1])
        # count it as top down, if the finger has to move over more than one col.
        if pos0 and pos1 and abs(pos0[0] - pos1[0]) > 1: 
            top_down_repeats.append((number, finger, letters))
    return top_down_repeats

def line_changes(data=None, repeats=None, layout=NEO_LAYOUT):
    """Get the number of line changes on the same hand (only change the line in between hand changes). 

    >>> data = read_file("testfile")
    >>> line_changes(data)
    7
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")
    
    line_changes = 0
    for number, pair in repeats:
        key1 = pair[0]
        key2 = pair[1]
        pos1 = find_key(key1, layout=layout)
        pos2 = find_key(key2, layout=layout)
        if pos1 and pos2:
            num_rows = abs(pos1[0] - pos2[0])
            if num_rows:
                # check if we’re on the same hand (else ignore the line change)
                finger1 = key_to_finger(key1, layout=layout)
                finger2 = key_to_finger(key2, layout=layout)
                if finger1 and finger2 and finger1[-1] == finger2[-1]: 
                    line_changes += abs(pos1[0] - pos2[0])**2 * number
    return line_changes

def load_per_finger(letters, layout=NEO_LAYOUT, print_load_per_finger=False):
    """Calculate the number of times each finger is being used.

    >>> letters = [(1, "u"), (5, "i"), (10, "2"), (3, " ")]
    >>> load_per_finger(letters)
    {'': 10, 'Klein_L': 1, 'Ring_L': 5, 'Daumen_L': 3}
    """
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

def std(numbers):
    """Calculate the standard deviation from a set of numbers.

    This simple calculation is only valid for more than 100 numbers or so. That means I use it in the invalid area. But since it’s just an arbitrary metric, that doesn’t hurt.

    >>> std([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]*10)
    1.607945243653783
    """
    length = float(len(numbers))
    mean = sum(numbers)/length
    var = 0
    for i in numbers:
        var += (i - mean)**2
    var /= (length - 1)
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

    TODO: If we fix uppercase handling (no longer just add both left and right shift), include tha shifts again. If we did it now, the layout would get optimized for switching after every uppercase letter (as any trigram with a shift and two letters on the same hand would be counted as half a trigram without handswitching). The effect is that it gnores about 7-9% of the trigrams. 

    >>> trigs = [(1, "nrt"), (5, "ige"), (3, "udi")]
    >>> no_handswitching(trigs, layout=NEO_LAYOUT)
    1
    """
    # optimization: we precalculate the fingers for all relevent keys (the ones which are being mutated). 
    key_hand_table = {}
    for key in abc:#+"⇧⇗ ":# -> too many false positives when we include the shifts
        finger = key_to_finger(key, layout=layout)
        if finger and not finger[:6] == "Daumen": 
            key_hand_table[key] = finger[-1]
    # now ret the hand for each key
    no_switch = 0
    counted = 0
    not_counted = 0
    for num, trig in trigrams:
        if trig[2:]:
            hand0 = key_hand_table.get(trig[0], None)
            hand1 = key_hand_table.get(trig[1], None)
            hand2 = key_hand_table.get(trig[2], None)
            if hand0 is not None and hand1 is not None and hand2 is not None:
                if hand0 == hand1 and hand1 == hand2: 
                    no_switch += num
                counted += num
            else:
                not_counted += num
    return no_switch

def badly_positioned_shortcut_keys(layout=NEO_LAYOUT, keys="xcvz"):
    """Check, if x, c, v and z are on the left hand and well positioned (much used shortcuts)."""
    badly_positioned = []
    for key in keys: 
        pos = find_key(key)
        # well means not yet left stretch
        if not pos[1] < 5:
            badly_positioned.append(1)
    return sum(badly_positioned)

        
def total_cost(data=None, letters=None, repeats=None, layout=NEO_LAYOUT, cost_per_key=COST_PER_KEY, trigrams=None, intended_balance=WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY):
    """Compute a total cost from all costs we have available, wheighted.

    >>> data = read_file("testfile")
    >>> total_cost(data, cost_per_key=TEST_COST_PER_KEY, intended_balance=TEST_WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY)
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
    finger_repeats_top_bottom = finger_repeats_top_and_bottom(finger_repeats)
    frep_num_top_bottom = sum([num for num, fing, rep in finger_repeats_top_bottom])

    # the number of changes between lines on the same hand.
    line_change_same_hand = line_changes(repeats=repeats, layout=layout)

    # the balance between fingers
    disbalance = finger_balance(letters, layout=layout, intended_balance=intended_balance)
    number_of_letters = sum([i for i, s in letters])

    # the position of the keys xcvz - penalty if they are not among the first 5 keys, counted from left, horizontally.
    badly_positioned = badly_positioned_shortcut_keys(layout=layout)

    # add all together and weight them
    total = WEIGHT_POSITION * position_cost
    total += WEIGHT_FINGER_REPEATS * frep_num # not 0.5, since there may be 2 times as many 2-tuples as letters, but the repeats are calculated on the in-between, and these are single.
    total += WEIGHT_FINGER_REPEATS_TOP_BOTTOM * frep_num_top_bottom
    total += int(WEIGHT_FINGER_DISBALANCE * disbalance)
    total += WEIGHT_TOO_LITTLE_HANDSWITCHING * no_handswitches
    total += WEIGHT_XCVZ_ON_BAD_POSITION * number_of_letters * badly_positioned
    total += WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * line_change_same_hand
    
    return total, frep_num, position_cost, frep_num_top_bottom, disbalance, no_handswitches, line_change_same_hand

### Evolution

def switch_keys(keypairs, layout=NEO_LAYOUT):
    """Switch keys in the layout, so we don't have to fiddle with actual layout files.

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

def randomize_keyboard(abc, num_switches, layout=NEO_LAYOUT): 
        """Do num_switches random keyswitches on the layout and
        @return: the randomized layout."""
        from random import choice
        keypairs = [choice(abc)+choice(abc) for i in range(num_switches)]
        lay = switch_keys(keypairs, layout=deepcopy(layout))
        return lay, keypairs

def find_the_best_random_keyboard(letters, repeats, trigrams, num_tries, num_switches=1000, layout=NEO_LAYOUT, abc=abc, quiet=False): 
        """Create num_tries random keyboards (starting from the layout and doing num_switches random keyswitches), compare them and only keep the best (by total_cost)."""
        lay, keypairs = randomize_keyboard(abc, num_switches, layout)
        cost = total_cost(letters=letters, repeats=repeats, layout=lay, trigrams=trigrams)[0]
        if not quiet: 
            print("cost of the first random layout:", cost)
        for i in range(max(0, num_tries-1)): 
            if not quiet: 
                print("-", i, "/", num_tries)
            lay_tmp, keypairs = randomize_keyboard(abc, num_switches, lay)
            cost_tmp = total_cost(letters=letters, repeats=repeats, layout=lay_tmp, trigrams=trigrams)[0]
            if cost_tmp < cost: 
                lay = lay_tmp
                cost = cost_tmp
                if not quiet: 
                    print("better:", cost)
        return lay, cost	    

def random_evolution_step(letters, repeats, trigrams, num_switches, layout, abc, cost, quiet): 
        """Do one random switch. Keep it, if it is beneficial."""
        lay, keypairs = randomize_keyboard(abc, num_switches, layout)
        new_cost, frep, pos_cost = total_cost(letters=letters, repeats=repeats, layout=lay, trigrams=trigrams)[:3]
        if new_cost < cost:
            if not quiet: 
                print(cost / 1000000, keypairs, "finger repetition:", frep / 1000000, "position cost:", pos_cost / 1000000)
                print(lay)
            return lay, new_cost, cost - new_cost
        else: 
            if not quiet: 
                print("worse", keypairs, end = " ")
            return layout, cost, 0

def controlled_evolution_step(letters, repeats, trigrams, num_switches, layout, abc, cost, quiet, cost_per_key=COST_PER_KEY): 
    """Do the most beneficial change. Keep it, if the new layout is better than the old.
        
    >>> data = read_file("testfile")
    >>> repeats = repeats_in_file(data)
    >>> letters = letters_in_file(data)
    >>> trigrams = trigrams_in_file(data)
    >>> controlled_evolution_step(letters, repeats, trigrams, 1, NEO_LAYOUT, "reo", 190, quiet=False, cost_per_key=TEST_COST_PER_KEY)
    # checked switch ('rr',) 201.4
    # checked switch ('re',) 181.4
    # checked switch ('ro',) 184.4
    # checked switch ('ee',) 201.4
    # checked switch ('eo',) 204.4
    # checked switch ('oo',) 201.4
    0.00019 finger repetition: 1e-06 position cost: 0.00015
    [['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'r', 'o', 's', 'n', 'e', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]]
    ([['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'r', 'o', 's', 'n', 'e', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]], 181.4, 8.599999999999994)
    >>> controlled_evolution_step(letters, repeats, trigrams, 1, NEO_LAYOUT, "reo", 25, False, cost_per_key=TEST_COST_PER_KEY)
    # checked switch ('rr',) 201.4
    # checked switch ('re',) 181.4
    # checked switch ('ro',) 184.4
    # checked switch ('ee',) 201.4
    # checked switch ('eo',) 204.4
    # checked switch ('oo',) 201.4
    worse ('oo',) ([['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'e', 'o', 's', 'n', 'r', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]], 25, 0)
    """
    from random import choice
    # First create one long list of possible switches
    keypairs = []
    for key1 in abc: 
        for key2 in abc[abc.index(key1):]: 
            keypairs.append(key1+key2)
    
    # then combine it into possible switch tuples (O(N²))
    switches = []
    for i in range(num_switches): 
        switches.append([]) # layers
    for pair1 in keypairs: 
        # pair 1 list
        for i in range(len(keypairs) ** min(1, num_switches - 1)): # ** (num_switches - 1)): 
            switches[0].append(pair1) # [[1, 1, 1]]
        for i in range(min(1, num_switches - 1)): # num_switches - 1): # TODO: Make it work for num > 2. 
            #for j in range(len(keypairs) ** max(0, (num_switches - 2))): 
                for pair_x in keypairs: #[keypairs.index(pair1)+1:]: 
                    # add additional possible pairs. 
                    switches[i+1].append(pair_x) # [[1, 1, 1], [1, 2, 3]]  
    switches = list(zip(*switches[:2]))
    
    # results for 1 step: [(cost, frep, pos_cost, layout), ...]
    step_results = []
    for keypairs in switches: 
        lay = switch_keys(keypairs, layout=deepcopy(layout))
        new_cost, frep, pos_cost = total_cost(letters=letters, repeats=repeats, layout=lay, cost_per_key=cost_per_key, trigrams=trigrams)[:3]
        step_results.append((new_cost, frep, pos_cost, lay))
        print("# checked switch", keypairs, new_cost)
    if min(step_results)[0] < cost:
        lay, new_cost = min(step_results)[-1], min(step_results)[0]
        if not quiet: 
            new_cost, frep, pos_cost = total_cost(letters=letters, repeats=repeats, layout=lay, cost_per_key=cost_per_key, trigrams=trigrams)[:3]
            print(cost / 1000000, "finger repetition:", frep / 1000000, "position cost:", pos_cost / 1000000)
            print(lay)
        return lay, new_cost, cost - new_cost
    else: 
        if not quiet: 
            print("worse", keypairs, end = " ")
        return layout, cost, 0

def evolve(letters, repeats, trigrams, layout=NEO_LAYOUT, iterations=400, abc=abc, quiet=False, controlled=False):
    """Repeatedly switch a layout randomly and do the same with the new layout,
    if it provides a better total score. Can't be tested easily => Check the source.

    To only mutate a subset of keys, just pass them as
    @param abc: the keys to permutate over.
    @param controlled: Do a slow controlled run, where all possible steps are checked and only the best is chosen? 
    """
    from math import log10
    cost = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams)[0]
    consecutive_fails = 0
    for i in range(iterations): 
        if not controlled: 
            # increase the size of the changes when the system seems to become stable (1000 consecutive fails: ~ 2*24*23 = every combination tried) to avoid deterministic purely local minima.
            step = int(log10(consecutive_fails + 1) / 3 + 1)
            lay, cost, better = random_evolution_step(letters, repeats, trigrams, step, layout, abc, cost, quiet)
        else: 
            step = int(consecutive_fails / 2 + 1)
            # only do the best possible step instead => damn expensive. For a single switch about 10 min per run. 
            lay, cost, better = controlled_evolution_step(letters, repeats, trigrams, step, layout, abc, cost, quiet)
        if better:
            consecutive_fails = 0
            # save the good mutation
            layout = lay
        else:
            consecutive_fails += 1
        if not quiet: 
            print("-", i, "/", iterations)
    
    return layout, cost


def combine_genetically(layout1, layout2):
    """Combine two layouts genetically (randomly)."""
    from random import randint
    switchlist = []
    for letter in abc:
        if randint(0, 1) == 1:
            pos = find_key(letter, layout=layout1)
            replacement = get_key(pos, layout=layout2)
            switchlist.append(letter+replacement)
    res = deepcopy(switch_keys(switchlist, layout=layout1))
    return res


### UI ###

def print_layout_with_statistics(layout, letters=None, repeats=None, number_of_letters=None, number_of_bigrams=None, print_layout=True, trigrams=None, number_of_trigrams=None, verbose=False):
    """Print a layout along with statistics."""
    if letters is None or number_of_letters is None: 
        data1 = read_file("1gramme.txt")
        letters = letters_in_file_precalculated(data1)
        number_of_letters = sum([i for i, s in letters])
        
    if repeats is None or number_of_bigrams is None:  
        data2 = read_file("2gramme.txt")
        repeats = repeats_in_file_precalculated(data2)
        number_of_bigrams = sum([i for i, s in repeats])

    if trigrams is None or number_of_trigrams is None:
        data3 = read_file("3gramme.txt")
        trigrams = trigrams_in_file_precalculated(data3)
        number_of_trigrams = sum([i for i, s in trigrams])
        
    if print_layout: 
        from pprint import pprint
        pprint(layout)

    total, frep_num, cost, frep_top_bottom, disbalance, no_handswitches, line_change_same_hand = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams)[:7]

    print("#", total / 1000000000.0, "billion total penalty compared to notime-noeffort")
    print("#", cost / number_of_letters, "mean key position cost in file 1gramme.txt")
    print("#", 100 * frep_num / number_of_bigrams, "% finger repeats in file 2gramme.txt")
    if verbose: 
        print("#", disbalance / 1000000, "million keystrokes disbalance of the fingers")
        print("#", 100 * frep_top_bottom / number_of_bigrams, "% finger repeats top to bottom or vice versa")
        print("#", 100 * no_handswitches / number_of_trigrams, "% of trigrams have no handswitching (uppercase ignored)")
        print("#", line_change_same_hand / 1000000000.0, "billion rows² to cross while on the same hand")


def check_with_datafile(args, quiet, verbose):
    """Check the neo layout (optionally with a number of changes) with a given textfile.
    """
    path = argv[2]
    data = read_file(path)

    # optionally change Neo
    if argv[4:] and argv[3] == "--switch":
        switchlist = argv[4].split(",")
        lay = switch_keys(switchlist, layout = NEO_LAYOUT)
        print("Neo", switchlist, "autogenerated")
    else:
        print("Neo")
        lay = NEO_LAYOUT

    # get the data
    letters = letters_in_file(data)
    num_letters = sum([num for num, letter in letters])
    repeats = repeats_in_file(data)
    num_reps = sum([num for num, rep in repeats])
    trigs = trigrams_in_file(data)
    num_trigs = sum([num for num, trig in trigs])

    # and print the layout with the data
    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=num_letters, number_of_bigrams=num_reps, trigrams=trigs, number_of_trigrams=num_trigs, verbose=verbose)
        
    if not quiet:
        print("\nQwertz for comparision")
        print_layout_with_statistics(QWERTZ_LAYOUT, letters=letters, repeats=repeats, number_of_letters=num_letters,
                                     number_of_bigrams=num_reps, trigrams=trigs, number_of_trigrams=num_trigs, verbose=verbose)
    

def evolve_a_layout(args, prerandomize, controlled, quiet, verbose):
    """Evolve a layout by selecting the fittest of random mutations step by step."""
    print("# Mutating Neo")
    #data = read_file("/tmp/sskreszta")
    data1 = read_file("1gramme.txt")
    letters = letters_in_file_precalculated(data1)
    #letters = letters_in_file(data)
    datalen1 = sum([i for i, s in letters])
    
    data2 = read_file("2gramme.txt")
    repeats = repeats_in_file_precalculated(data2)
    #repeats = repeats_in_file(data)
    datalen2 = sum([i for i, s in repeats])

    data3 = read_file("3gramme.txt")
    trigrams = trigrams_in_file_precalculated(data3)
    number_of_trigrams = sum([i for i, s in trigrams])
   
    if prerandomize:
        if not quiet:
            print("doing", prerandomize, "prerandomization switches.")
        lay, keypairs = randomize_keyboard(abc, num_switches=prerandomize, layout=NEO_LAYOUT)
    else: lay = NEO_LAYOUT
    
    lay, cost = evolve(letters, repeats, trigrams, layout=lay, iterations=int(argv[2]), quiet=quiet, controlled=controlled)
    
    print("\n# Evolved Layout")
    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)


def evolution_challenge(layout=NEO_LAYOUT, challengers=100, rounds=10, iterations=400, abc=abc, prerandomize=10000, quiet=False, controlled=False):
     """Run a challenge between many randomized layouts, then combine the best pseudo-genetically (random) and add them to the challenge."""
     # Data for evaluating layouts.
     data1 = read_file("1gramme.txt")
     letters = letters_in_file_precalculated(data1)
     datalen1 = sum([i for i, s in letters])
     data2 = read_file("2gramme.txt")
     repeats = repeats_in_file_precalculated(data2)    
     datalen2 = sum([i for i, s in repeats])

     data3 = read_file("3gramme.txt")
     trigrams = trigrams_in_file_precalculated(data3)
     number_of_trigrams = sum([i for i, s in trigrams])
     

     from pprint import pprint

     layouts = [] # [(cost, lay), …]
     if not quiet:
         print("# create the", challengers, "starting layouts")
     for i in range(challengers):
         print("#", i, "of", challengers)
         lay, keypairs = randomize_keyboard(abc, num_switches=prerandomize, layout=NEO_LAYOUT)
         lay, cost = evolve(letters, repeats, trigrams, layout=lay, iterations=iterations, quiet=True)
         layouts.append((cost, lay))
     # run the challenge
     for round in range(rounds): 
         # sort and throw out the worst
         layouts.sort()
         if not quiet:
             print("# round", round)
             print("# top five")
             for cost, lay in layouts[:5]:
                 print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams)
         layouts = deepcopy(layouts[:int(challengers / 4.0)+1])
         # combine the best and worst to get new ones.
         print("breeding new layouts")
         for i in range(int(challengers/8)):
            print(i, "of", int(challengers/4), "from weak and strong")
            new = deepcopy(combine_genetically(layouts[i][1], layouts[-i - 1][1]))
            # evolve, then append
            new, cost = deepcopy(evolve(letters, repeats, trigrams, layout=new, iterations=iterations, quiet=True))
            layouts.append((cost, new))
            # also combine the best one with the upper half
         for i in range(max(0, int(challengers/8))):
            print(i+int(challengers/8), "of", int(challengers/4), "from the strongest with the top half")
            new = deepcopy(combine_genetically(layouts[0][1], layouts[i+1][1]))
            new, cost = evolve(letters, repeats, trigrams, layout=new, iterations=iterations, quiet=True)
            layouts.append((cost, new))
         # and new random ones
         print("and fill up the ranks with random layouts")
         for i in range(challengers - len(layouts)):
             print(i, "of", challengers - len(layouts))
             lay, keypairs = deepcopy(randomize_keyboard(abc, num_switches=prerandomize, layout=NEO_LAYOUT))
             lay, cost = evolve(letters, repeats, trigrams, layout=lay, iterations=iterations, quiet=True)
             layouts.append((cost, lay))

     print("# Top 3")
     layouts.sort()

     for num, name in [(0, "gold"), (1, "silver"), (2, "bronze")][:len(layouts)]: 
         cost, lay = layouts[num]
         print(name)
         print_layout_with_statistics(lay, letters, repeats, datalen1, datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams)

def best_random_layout(args, prerandomize):
    """Select the best gf a number of randomly created layouts."""
    print("Selecting the best from", argv[2],"random layouts.")
    data1 = read_file("1gramme.txt")
    letters = letters_in_file_precalculated(data1)
    datalen1 = sum([i for i, s in letters])
    
    data2 = read_file("2gramme.txt")
    repeats = repeats_in_file_precalculated(data2)
    datalen2 = sum([i for i, s in repeats])

    data3 = read_file("3gramme.txt")
    trigrams = trigrams_in_file_precalculated(data3)
    number_of_trigrams = sum([i for i, s in trigrams])
     
    if prerandomize: 
        lay, cost = find_the_best_random_keyboard(letters, repeats, trigrams, num_tries=int(argv[2]), num_switches=int(PRERANDOMIZE), layout=NEO_LAYOUT, abc=abc, quiet=QUIET)
    else: 
        lay, cost = find_the_best_random_keyboard(letters, repeats, trigrams, num_tries=int(argv[2]), layout=NEO_LAYOUT, abc=abc, quiet=QUIET)
        
    print("\nBest of the random layouts")
    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams)
    

def check_the_neo_layout(quiet, verbose):
    """Check the performance of the neo layout, optionally scoring it against Qwertz."""
    print("Neo")
    data1 = read_file("1gramme.txt")
    letters = letters_in_file_precalculated(data1)
    datalen1 = sum([i for i, s in letters])
    
    data2 = read_file("2gramme.txt")
    repeats = repeats_in_file_precalculated(data2)
    datalen2 = sum([i for i, s in repeats])
    
    data3 = read_file("3gramme.txt")
    trigrams = trigrams_in_file_precalculated(data3)
    number_of_trigrams = sum([i for i, s in trigrams])
     
    print_layout_with_statistics(NEO_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, print_layout=not quiet, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)
    
    if not quiet:
        print("\nQwertz for comparision")
        print_layout_with_statistics(QWERTZ_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)
        print("\nAnd the Nordtast Layout")
        print_layout_with_statistics(NORDTAST_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)
        print("\nAnd Dvorak")
        print_layout_with_statistics(DVORAK_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)
        print("\nAnd Colemak")
        print_layout_with_statistics(COLEMAK_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)


def check_a_layout_from_shell(layout_data, quiet, verbose):
    """Check a layout we get passed as shell argument."""
    layout = eval(layout_data)
    print_layout_with_statistics(layout, print_layout=not quiet, verbose=verbose)


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
    
    if "--controlled-evolution" in argv:
        CONTROLLED_EVOLUTION = True
        argv.remove("--controlled-evolution")
    else: CONTROLLED_EVOLUTION = False

    if "--prerandomize" in argv: 
        PRERANDOMIZE = argv[argv.index("--prerandomize") + 1]
        argv.remove("--prerandomize")
        argv.remove(PRERANDOMIZE)
        PRERANDOMIZE = int(PRERANDOMIZE)
    else: PRERANDOMIZE = False
    
    if "--help" in argv:
        print(__usage__)
        exit()

    if argv[1:] and argv[1] == "--file":
        check_with_datafile(args=argv, quiet=QUIET, verbose=VERBOSE)

    elif argv[2:] and argv[1] == "--evolve":
        evolve_a_layout(args=argv, prerandomize=PRERANDOMIZE, quiet=QUIET, controlled=CONTROLLED_EVOLUTION, verbose=VERBOSE)
        
    elif argv[2:] and argv[1] == "--best-random-layout":
        best_random_layout(args=argv, prerandomize=PRERANDOMIZE)

    elif argv[2:] and argv[1] == "--challenge":
        if argv[4:] and "--challengers" in argv:
            challengers = argv[argv.index("--challengers")+1]
            argv.remove(challengers)
            argv.remove("--challengers")
            evolution_challenge(rounds=int(argv[2]), challengers=int(challengers) ) # layout=NEO_LAYOUT, challengers=400, rounds=argv[2], iterations=400, abc=abc, prerandomize=10000, quiet=False, controlled=False)
        else: 
            evolution_challenge(rounds=int(argv[2])) # layout=NEO_LAYOUT, challengers=400, rounds=argv[2], iterations=400, abc=abc, prerandomize=10000, quiet=False, controlled=False)

    elif argv[2:] and argv[1] == "--check":
        check_a_layout_from_shell(argv[2], quiet=QUIET, verbose=VERBOSE)
            
    else:
        check_the_neo_layout(quiet=QUIET, verbose=VERBOSE)
        
    #print(unique_sort(frep))
    
    #rep = repeats_in_file_sorted(path)
    #print(str(len(rep)), "repeats in file", path, "sorted.")
    #print([i for i in rep if "a" in i[1]])
