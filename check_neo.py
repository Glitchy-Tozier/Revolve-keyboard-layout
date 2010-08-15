#!/usr/bin/env python3

"""Optimize keyboard layouts evolutionally (with mutations).

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

- check_neo.py [-v] [--file <file>] --layout-string "khßwv ä.uozj
  dnclr aitesb
  fpgmx ,üöyq"
  check the layout given by a layout string.
  -v gives more statistical info on the layout
  --file <file> uses a file as corpus for checking the layout. 


- check_neo.py --evolve <iterations> [--prerandomize <num_switches>] [-q] [-v] [--controlled-evolution] [--controlled-tail]
  randomly permutate keys on the Neo keyboard to see if a better layout emerges. 
  --controlled-evolution tells it to use the horribly slow and deterministic code which always chooses the best possible change in each step.
  --controlled-tail makes it first do <iterations> random mutations and then a controlled evolution, until it can’t go any further. controlled_tail and controlled-evolution are exclusive. When both are used, the tail wins. 
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

- check_neo.py [-v] [-q] --check-string "öckäy zhmlß,
atieo dsnru.
xpfüq bgvwj"
  check a layout string for layer 1. 

- check_neo.py --test (run doctests)

Note: If --prerandomize is set to 1000000 or more, it just does a real shuffle instead of prerandomizing. 

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
- Groß- und Kleinschreibung wird durch einen preprocessor gemacht werden, der „vrtuelle Zeichen“ vor dem eigentlichen Zeichen einfügt.
- Erst Evolution (~3000), dann so lange kontrolliert (immer bester Schritt), bis es keine Verbesserung mehr gibt. - done

Später:
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
  Die Zusatzkosten fur den kleinen Finger sollten nur durch die Gesamtbelistung kommen. 
- Einen Finger mehrfach hintereinander verwenden. => Strafpunkte. - done
- Einen Finger mehrfach, von oben nach ganz unten. => viele Strafpunkte. - done
- Handwechsel sparen Zeit => Wenn bei tripeln alle 3 Zeichen auf der gleichen Hand sind, bringt das Strafpunkte. - done
- Der Zeige- und Mittelfinger sind schneller unten bzw. oben als die beiden anderen => Kosten für Einzeltasten anpassen. Erst Rohmert Geschwindigkeit, dann nochmal einen Malus für unbequeme Handbewegung. - done
  (aus http://forschung.goebel-consult.de/de-ergo/rohmert/Rohmert.html)

Kostenfaktor: Belastung
- Ungleichmäßige Belastung beider Hände. => indirekt durch Strafpunkte bei fehlendem Handwechsel und direkt, weil das auch ungleiche Belastung der Finger bewirkt- done
- Ungleichmäßige Belastung der einzelnen Finger (allerdings sollte der Kleine weniger belastet werden). => Finger zählen, kleinen doppelt gewichten. Strafpunkte für Abweichung vom Durchschnitt (quadratisch?) ?? - done (std)

Kostenfaktor: Natürliche Handbewegung
- Zeilenwechsel ohne Handwechsel kostet Anstrengung, desto mehr, je  näher die Buchstaben horizontal sind => Malus für den Wechsel der Zeile in einem Bigramm auf der gleichen Hand. Malus = (Anzahl Zeilen / Abstand in Fingern)²- done
- Finger nebeneinander nutzen ist sehr viel unpraktischer als wenn ein Finger Abstand ist. Fixkosten für Fingerübergänge (dict). Das kann auch bevorzugte Bewegungsmuster und Richtungen abdecken (z.B. von außen nach innen)- Teilerledigt: Kosten für die Nutzung benachbarter Finger. Noch zu erledigen: Kosten für alle Fingerübergänge (Grund: Neo 2 ae ist für mich besser als ue). TODO
- Kein Goüävu (Neo 2) → keine Richtungsänderung + Wenn die Hand aus der Grundstellung gezogen wird (Neo oswkzxyß´) ein Handwechsel. ⇒ Malus für Richtungsänderungen in Trigrammen und heftiger Malus für kein Handwechsel für die Handhaltung verzerrende Positionen. - Teilerledigt: Richtungsänderungen geben Malus, wenn sie kein Handwechsel sind. - done
Ein Handwechsel direkt nach einem Großbuchstaben ist ekelhaft, weil die dem Buchstaben gegenüberliegende Hand noch aus dem Gleichgewicht gezoren ist. (Erweiterung zum vorigen Punkt). Teilweise da, weil Trigramme mit Großbuchstaben aber ohne sonstigen Handwechsel nicht als Malus gezählt werden; reicht aber wohl nicht aus. Strafpunkte für Bigramme in denen nach shift ein Buchstabe der gleichen Hand folgt (im Vorigen Punkt drin, daher kein to do). 
- (Von außen nach innen. => von innen nach außen auf der gleichen Hand gibt Strafpunkte. Stattdessen vielleicht: Kein Richtungswechsel der Finger einer Hand. - TODO)
- (Fingerwiederholungen in Trigrammen sind etwas unbequem – dadurch hat der Finger zu wenig Zeit, in die Grundposition zurückzukehren (lehre aus tic1). - TODO)
- (Einen Finger in der Mitte und dann den direkt daneben die Zeile weiter unten ist sehr unangenehm. Wenn die Zeilen runter gehen, sollte min. ein Finger dazwischen sein. → Strafe wenn in einem Bigramm der Finger daneben (gleiche Hand) in der unteren Zeile genutzt wird (und die vorige Zeile nicht unten war). ! Hängt vom Finger ab! Der kleine kann gut runter, aber schlecht hoch. - TODO)
- (Links gleicher Finger wie rechts. => Fingerwechsel bei Handwechsel hat Kosten. - TODO)
- (Frage: Zwei Finger nebeneinander auf der gleichen Hand oder Abstand, aber nicht Mittel- und Ringfinger. -> bei Tripeln: wenn zwei Tasten auf der gleichen Hand liegen, sollten sie aufeinander folgen  => Wenn der Ringfinger auf den Mittelfinger folgt oder umgekehrt gibt es Strafpunkte (bei  bigrammen) Gegenpunkt: Direkt nebeneinander liegende Finger ein Nachteil? - TODO)
  (von http://www.michaelcapewell.com/projects/keyboard/layout_capewell.htm und http://mkweb.bcgsc.ca/carpalx/?typing_effort)

Sonstiges:
- XCV sollten gut erreichbar auf der linken Hand liegen. => Strafpunkte, wenn pos[2] > 3. z.B. Kosten bei den Monogrammen * 0.005 (0.5%), bzw. Kosten pro Zeichen. Vielleicht auch Z dazu (undo). - done. 
- (. sollte vielleicht neben , liegen. Das sind mit dem Leerzeichen die einzigen beiden Zeichen, die keine echten Buchstaben sind. - TODO)
- Gleichmäßigkeit: Es sollte keine häufig benutzten Wörter geben, die ganz schlecht sind. => Erst die allgemeinkosten berechnen (_total_cost), dann die Standardabweichung der Kosten pro Trigramm (total_cost ruft für jedes Trigramm _total_cost mit dem Ergebnis von _total_cost auf). - TODO

### Kosten für die Tasten

Da die Belastung der Finger bereits *pro Finger* gerechnet wird, sollte darüber auch die Unterscheidung zwischen Fingern gemacht werden. → WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY

Das sollte dann der inversen Geschwindigkeit der Finger entsprechen, normiert auf den Kleinen Finger und modifiziert durch die Belastbarkeit. Die liste sagt “so viel Last wollen wir auf dem Finger”. Dadurch können dann die Kosten pro Taste alleine auf der Erreichbarkeit der Tasten relativ zur Grundlinie aufgebaut werden. 

Die Kosten einer Taste außerhalb der Grundlinie sollten sich an der Zeit orientieren, die gebraucht wird, um die Taste zu erreichen und dann wieder auf die Grundlinie zu kommen (Blockadezeit des Fingers). Nach Rohmert sind des beim Ringfinger 580ms oben, Beim Mittelfinger 440ms, beim kleinen >620ms und beim Zeigefinger 420ms. Der Mittelfinger kommt etwa so schnell runter wie der Ringfinger (240ms-250ms), nur der Zeigefinger ist signifikent schneller (200ms). 

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
__note1__ = """
> Die Kombination viele Tastenanschläge plus kurze Wege plus
> moderate Andruckkraft scheint sich für die Bildung von Erkrankungen
> stärker auszuwirken.

Das ist sogar eigentlich logisch. Beweg’ mal Mittel- und Ringfinger schnell gegeneinander (Neo aiaiaiaia oder rtrtrtr). Da sind bei den meisten Nicht-Klavierspielern die Sehnen nicht ganz getrennt, so dass das sehr schlecht geht und vermutlich hohe Belastung bewirkt (Reibung).

Ähnliches gilt bei mir bei kleinem und Ringfinger – eigentlich sogar noch stärker.

Mit dem Zeigefinger dagegen können alle :)

Tests:
1. uiuiuiuiui - Kl + Ring
   (sehr unbequem für mich)
2. uauauauaua - Kl + Mittel
   (weniger unbequem, aber ich bin da sehr ungeschickt)
3. ueueueueue - Kl + Zeige
   (problemlos)
4. iaiaiaiaia - Ring + Mittel
   (besser als 1, und 2., aber hohe Belastung (fühle ich sofort „in“ den
   Sehnen, also vermutlich eigentlich in der Sehnenscheide)
5. ieieieieie - Ring + Zeige
   (sogar noch einfacher als 3.)
6. aeaeaeaeae - Mittel + Zeige
   (so einfach wie 5., vielleicht minimal höhere Belastung)
   
Nach den Ergebnissen von Walter Rohmert[1] sind außerdem solche Bigramme schneller, die auf den Zeigefinger oder auf den kleinen Finger enden.

Vom Mittelfinger ausgehend sind nach seinen Ergebnissen alle Tasten hinreichend schnell zu erreichen (Faktor 1.5 gegenüber den schlecht zu erreichenden Tasten der anderen Finger).

Zusätzlich hat er gefunden, dass die Geschwindigkeit um so höher ist, je mehr Abstand zwischen den Tasten ist, was aber natürlich durch den Vorteil des Endens auf Zeigefinger oder kleinen Finger kommen kann.

Zwischenraum (n Tasten)    Betätigungsgeschwindigkeit (mm/sec)
0    7,22
1    15,19
2    20,15
3    30,17


Für die Optimierung heißen seine Ergebnisse praktisch:

(Legende: K: Klein, R: Ring, M: Mittel, Z: Zeige)

Ideales Bigramm: MK (200ms vs 230)

Gute Bigramme: ZZ, ZK, MZ, MR, RZ, RK, KZ, KR (Faktor ~1.1 langsamer. 220 bis 240 ms).

Schlechte Bigramme: ZM, ZR, RM, KM (~1.6 langsamer als Ideal. 300 bis 340 ms)

Das könnten wir direkt einfließen lassen: Bei schlechten Bigrammen die durchschnittlichen Tastenkosten * 0.6 als Malus. Ungefähr also 2.

[1]: http://forschung.goebel-consult.de/de-ergo/rohmert/Rohmert.html
     "Forschungsbericht zur ergonomische Gestaltung von
      Schreibmaschinentastaturen."
      

"""
__results__ = """

"""

__doc__ += __usage__ + __design__

__version__ = "0.1.2"

__copyright__ = """2010 © Arne Babenhauserheide

License: GPLv3 or later
"""

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

# forced fileoutput instead of printing
if "-f" in argv:
    idx = argv.index("-f")
    FILE = argv[idx+1]
    argv = argv[:idx] + argv[idx+2:]
    def print(*args):
        with open(FILE, "a") as f:
            for i in args:
                f.write(str(i) + " ")
            f.write("\n")

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
    #print("cache miss", key, pos)
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

def read_file(path):
    """Get the data from a file.

    >>> read_file("testfile")[:2]
    'ui'
    """

    f = open(path, encoding="UTF-8")
    data = f.read()
    f.close()
    return data

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
    >>> lay = switch_keys(["ax"], layout=NEO_LAYOUT)
    >>> key_position_cost_from_file(data[:3], cost_per_key=TEST_COST_PER_KEY, layout=lay)
    20
    >>> data = "UIaĥK\\n"
    >>> key_position_cost_from_file(data, cost_per_key=TEST_COST_PER_KEY, layout=lay)
    90
    """
    if data is not None: 
        letters = letters_in_file(data)
    elif letters is None:
        raise Exception("Need either letters or data")
    letters = split_uppercase_letters(letters, layout=layout)
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
    [(2, 'Mittel_L', 'aa'), (1, 'Mittel_R', 'rg'), (1, 'Zeige_L', 'eo'), (1, 'Klein_R', 'd\\n'), (1, 'Mittel_L', 'aa'), (1, 'Mittel_L', 'aa')]
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")

    repeats = split_uppercase_repeats(repeats, layout=layout)
    
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

def neighboring_fingers(data=None, repeats=None, layout=NEO_LAYOUT):
    """Return the number of times we have to use fingers next to each other.

    >>> data = read_file("testfile")
    >>> neighboring_fingers(data)
    23
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")
    
    repeats = split_uppercase_repeats(repeats, layout=layout)

    fingtups = ((num, (key_to_finger(rep[0]), key_to_finger(rep[1]))) for num, rep in repeats if key_to_finger(rep[0]) and key_to_finger(rep[1]))
    neighcosts = (num*FINGER_SWITCH_COST[fings[0]][fings[1]] for num, fings in fingtups if fings[1] in FINGER_SWITCH_COST[fings[0]])
    return sum(neighcosts)
    

def no_handswitch_after_unbalancing_key(data=None, repeats=None, layout=NEO_LAYOUT):
    """Check how often we have no handswitching after an unbalancing key, weighted by the severity of the unbalancing. This also helps avoiding a handswitch directly after an uppercase key (because shift severly unbalances und with the handswitch we’d effectively have no handswitch after the shift (kind of a shift collision, too). 

    >>> data = read_file("testfile")
    >>> no_handswitch_after_unbalancing_key(data)
    2
    >>> reps =  [(3, "Ab")]
    >>> no_handswitch_after_unbalancing_key(repeats=reps)
    6
    >>> no_handswitch_after_unbalancing_key(repeats=reps, layout=QWERTZ_LAYOUT)
    0
    >>> reps = [(3, "Ga")]
    >>> no_handswitch_after_unbalancing_key(repeats=reps, layout=QWERTZ_LAYOUT)
    3
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")
    
    repeats = split_uppercase_repeats(repeats, layout=layout)

    no_switch = 0
    for number, pair in repeats:
        key1 = pair[0]
        key2 = pair[1]
        pos1 = find_key(key1, layout=layout)
        pos2 = find_key(key2, layout=layout)
        if pos1 and pos2 and pos1 in UNBALANCING_POSITIONS:
                # check if we”re on the same hand
                finger1 = key_to_finger(key1, layout=layout)
                finger2 = key_to_finger(key2, layout=layout)
                if finger1 and finger2 and finger1[-1] == finger2[-1]:
                    no_switch += UNBALANCING_POSITIONS.get(pos1, 0)*number
    return no_switch

def line_changes(data=None, repeats=None, layout=NEO_LAYOUT):
    """Get the number of (line changes divided by the horizontal distance) squared: (rows²/dist)².

    Don’t care about the hand (left index low and right high is still not nice). 

    >>> data = read_file("testfile")
    >>> line_changes(data)
    16.29
    """
    if data is not None: 
        repeats = repeats_in_file(data)
    elif repeats is None:
        raise Exception("Need either repeats or data")
    
    repeats = split_uppercase_repeats(repeats, layout=layout)

    line_changes = 0
    for number, pair in repeats:
        key1 = pair[0]
        key2 = pair[1]
        pos1 = find_key(key1, layout=layout)
        pos2 = find_key(key2, layout=layout)
        if pos1 and pos2:
            if not WEIGHT_COUNT_ROW_CHANGES_BETWEEN_HANDS: 
                # check if we”re on the same hand
                finger1 = key_to_finger(key1, layout=layout)
                finger2 = key_to_finger(key2, layout=layout)
                if finger1 and finger2 and finger1[-1] != finger2[-1]:
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

    >>> letters = [(1, "u"), (5, "i"), (10, "2"), (3, " ")]
    >>> load_per_finger(letters)
    {'': 10, 'Klein_L': 1, 'Ring_L': 5, 'Daumen_L': 3}
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
    [9, 2]
    >>> finger_load = {'': 10, 'Klein_L': 1, 'Ring_L': 5, 'Daumen_L': 3, 'Mittel_R': 2}
    >>> load_per_hand(finger_load = finger_load)
    [9, 2]
    
    """
    if finger_load is None and letters is not None: 
        finger_load = load_per_finger(letters, layout=layout)
    elif letters is None and finger_load is None:
        raise Exception("Need at least letters or precalculated finger_load")
    hand_load = [sum([finger_load[f] for f in finger_load if f.endswith(hand)]) for hand in ("L", "R")]
    return hand_load


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

    If there also is a direction change in the trigram, the number of times it occurs gets multiplied by WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE.

    (TODO? WEIGHT_TRIGRAM_FINGER_REPEAT_WITHOUT_KEY_REPEAT)

    TODO: Include the shifts again and split per keyboard. If we did it now, the layout would get optimized for switching after every uppercase letter (as any trigram with a shift and two letters on the same hand would be counted as half a trigram without handswitching). The effect is that it ignores about 7-9% of the trigrams. 

    >>> trigs = [(1, "nrt"), (5, "ige"), (3, "udi")]
    >>> no_handswitching(trigs, layout=NEO_LAYOUT)
    1
    """
    # optimization: we precalculate the fingers for all relevent keys (the ones which are being mutated). 
    key_hand_table = {}
    for key in abc:
        #without "⇧⇗ " -> too many false positives when we include the shifts. This also gets rid of anything with uppercase letters in it.
        finger = key_to_finger(key, layout=layout)
        if finger and not finger[:6] == "Daumen": 
            key_hand_table[key] = finger[-1]

    key_pos_horizontal_table = {}
    for key in abc:
        #without "⇧⇗ " -> too many false positives when we include the shifts. This also gets rid of anything with uppercase letters in it.
        pos = find_key(key, layout=layout)
        if pos is not None: 
            key_pos_horizontal_table[key] = pos[1]
    

    no_switch = 0
    for num, trig in trigrams:
            # if we have a shift in it, we also have a handswitch. 
            if not trig[0] in key_hand_table or not trig[1] in key_hand_table or not trig[2] in key_hand_table:
                continue
            hand0 = key_hand_table.get(trig[0], None)
            hand1 = key_hand_table.get(trig[1], None)
            hand2 = key_hand_table.get(trig[2], None)
            if hand0 == hand1 and hand1 == hand2:
                pos0 = key_pos_horizontal_table[trig[0]]
                pos1 = key_pos_horizontal_table[trig[1]]
                pos2 = key_pos_horizontal_table[trig[2]]
                if pos0 > pos1 and pos1 < pos2 or pos0 < pos1 and pos1 > pos2:
                    num *= WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE
                else: 
                    num *= WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE
                no_switch += num
    return no_switch


def badly_positioned_shortcut_keys(layout=NEO_LAYOUT, keys="xcvz"):
    """Check, if x, c, v and z are on the left hand and well positioned (much used shortcuts)."""
    badly_positioned = []
    for key in keys: 
        pos = find_key(key, layout=layout)
        # well means not yet left stretch, in row 3, col 5 is also OK.
        if not pos[1] < 5 or (pos[0] == 3 and pos[1] == 5):
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
    finger_repeats_top_bottom = finger_repeats_top_and_bottom(finger_repeats, layout=layout)
    frep_num_top_bottom = sum([num for num, fing, rep in finger_repeats_top_bottom])

    # the number of times neighboring fingers are used – weighted by the ease of transition for the respective fingers
    neighboring_fings = neighboring_fingers(repeats=repeats, layout=layout)

    # the number of changes between lines on the same hand.
    line_change_same_hand = line_changes(repeats=repeats, layout=layout)

    # how often the hand wasn’t switched after an unbalancing key, weighted by the severity of the unbalancing.
    no_switch_after_unbalancing = no_handswitch_after_unbalancing_key(repeats=repeats, layout=layout)

    # the balance between fingers
    disbalance = finger_balance(letters, layout=layout, intended_balance=intended_balance)
    number_of_letters = sum([i for i, s in letters])

    # the position of the keys xcvz - penalty if they are not among the first 5 keys, counted from left, horizontally.
    badly_positioned = badly_positioned_shortcut_keys(layout=layout)

    # add all together and weight them
    total = WEIGHT_POSITION * position_cost
    total += WEIGHT_FINGER_REPEATS * frep_num # not 0.5, since there may be 2 times as many 2-tuples as letters, but the repeats are calculated on the in-between, and these are single.
    total += WEIGHT_FINGER_REPEATS_TOP_BOTTOM * frep_num_top_bottom
    total += WEIGHT_FINGER_SWITCH * neighboring_fings
    total += int(WEIGHT_FINGER_DISBALANCE * disbalance)
    total += WEIGHT_TOO_LITTLE_HANDSWITCHING * no_handswitches
    total += WEIGHT_XCVZ_ON_BAD_POSITION * number_of_letters * badly_positioned
    total += WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * line_change_same_hand
    total += WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY * no_switch_after_unbalancing

    if not return_weighted: 
        return total, frep_num, position_cost, frep_num_top_bottom, disbalance, no_handswitches, line_change_same_hand
    else:
        return total, WEIGHT_POSITION * position_cost, WEIGHT_FINGER_REPEATS * frep_num , WEIGHT_FINGER_REPEATS_TOP_BOTTOM * frep_num_top_bottom, WEIGHT_FINGER_SWITCH * neighboring_fings, int(WEIGHT_FINGER_DISBALANCE * disbalance), WEIGHT_TOO_LITTLE_HANDSWITCHING * no_handswitches, WEIGHT_XCVZ_ON_BAD_POSITION * number_of_letters * badly_positioned, WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW * line_change_same_hand, WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY * no_switch_after_unbalancing

        

### Evolution

def switch_keys(keypairs, layout=NEO_LAYOUT):
    """Switch keys in the layout, so we don't have to fiddle with actual layout files.

    >>> lay = switch_keys([], layout = NEO_LAYOUT)
    >>> lay == NEO_LAYOUT
    True
    >>> lay = switch_keys(["lx", "wq"], layout = NEO_LAYOUT)
    >>> get_key((1, 1, 0), layout=lay)
    'l'
    >>> get_key((1, 3, 0), layout=lay)
    'x'
    >>> get_key((1, 5, 0), layout=lay)
    'q'
    >>> get_key((1, 10, 0), layout=lay)
    'w'
    >>> find_key("l", layout=lay) == (1, 1, 0)
    True
    >>> NEO_LAYOUT_lxwq == lay[:5]
    True
    >>> lay = switch_keys(["lx"], layout = NEO_LAYOUT)
    >>> NEO_LAYOUT_lx == lay[:5]
    True
    >>> a = find_key("a", layout=lay)
    >>> lay = switch_keys(["ab"], layout=lay)
    >>> a == find_key("b", layout=lay)
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
        update_letter_to_key_cache_multiple(pair, layout=lay)
    
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
                print(format_layer_1_string(lay))
            return lay, new_cost, cost - new_cost
        else:
            if not quiet: 
                print("worse", keypairs, end = " ")
            return layout, cost, 0

def controlled_evolution_step(letters, repeats, trigrams, num_switches, layout, abc, cost, quiet, cost_per_key=COST_PER_KEY): 
    """Do the most beneficial change. Keep it, if the new layout is better than the old.

    TODO: reenable the doctests, after the parameters have settled, or pass ALL parameters through the functions. 
    
    >>> data = read_file("testfile")
    >>> repeats = repeats_in_file(data)
    >>> letters = letters_in_file(data)
    >>> trigrams = trigrams_in_file(data)
    >>> #controlled_evolution_step(letters, repeats, trigrams, 1, NEO_LAYOUT, "reo", 190, quiet=False, cost_per_key=TEST_COST_PER_KEY)
    
    # checked switch ('rr',) 201.4
    # checked switch ('re',) 181.4
    # checked switch ('ro',) 184.4
    # checked switch ('ee',) 201.4
    # checked switch ('eo',) 204.4
    # checked switch ('oo',) 201.4
    0.00019 finger repetition: 1e-06 position cost: 0.00015
    [['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'r', 'o', 's', 'n', 'e', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]]
    ([['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'r', 'o', 's', 'n', 'e', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]], 181.4, 8.599999999999994)
    >>> #controlled_evolution_step(letters, repeats, trigrams, 1, NEO_LAYOUT, "reo", 25, False, cost_per_key=TEST_COST_PER_KEY)
    
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
        if not quiet: 
            print("# checked switch", keypairs, new_cost)
    if min(step_results)[0] < cost:
        lay, new_cost = min(step_results)[-1], min(step_results)[0]
        if not quiet: 
            new_cost, frep, pos_cost = total_cost(letters=letters, repeats=repeats, layout=lay, cost_per_key=cost_per_key, trigrams=trigrams)[:3]
            print(cost / 1000000, "finger repetition:", frep / 1000000, "position cost:", pos_cost / 1000000)
            print(format_layer_1_string(lay))
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


def evolve_with_controlled_tail(letters, repeats, trigrams, layout=NEO_LAYOUT, iterations=400, abc=abc, quiet=False):
    """Repeatedly switch a layout randomly and do the same with the new layout,
    if it provides a better total score. Can't be tested easily => Check the source.

    After the iterations, do a controlled evolution, until nothing can be improved anymore.

    Different from the normal evolvution, this never increases the step size (which has proven not to be very effective for the normal evolution and is incompatible with the thought of doing controlled optimization up to the end.

    To only mutate a subset of keys, just pass them as
    @param abc: the keys to permutate over.
    @param controlled: Do a slow controlled run, where all possible steps are checked and only the best is chosen? 
    """
    from math import log10
    cost = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams)[0]

    # first round: do (numper of iterations) mutation tries.
    if not quiet: 
        print("doing", iterations, "random mutations")
    for i in range(iterations): 
        # increase the size of the changes when the system seems to become stable (1000 consecutive fails: ~ 2*24*23 = every combination tried) to avoid deterministic purely local minima.
        lay, cost, better = random_evolution_step(letters, repeats, trigrams, 1, layout, abc, cost, quiet)
        if better:
            # save the good mutation
            layout = lay
        if not quiet: 
            print("-", i, "/", iterations)

    # second round: do controlled evolution steps, as long as they result in better layouts (do a full controlled optimization of the result).
    if not quiet: 
        print("controlled evolution, until there’s no more to improve")
    better = True
    steps = 0
    while better: 
        # only do the best possible step instead => damn expensive. For a single switch about 10 min per run. 
        lay, cost, better = controlled_evolution_step(letters, repeats, trigrams, 1, layout=layout, abc=abc, cost=cost, quiet=quiet)
        if better:
            # save the good mutation - yes, this could go at the start of the loop, but that wouldn’t be as clear.
            layout = lay
        if not quiet: 
            print("-", steps, "/ ?", )
    
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

def format_keyboard_layout(layout):
    """Format a keyboard layout to look like a real keyboard."""
    neo = """
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──────┐
│ ^ │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ ` │ Back │
├───┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬─────┤
│Tab │ x │ v │ l │ c │ w │ k │ h │ g │ f │ q │ ß │ ´ │ Ret │
├────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─┐   │
│ M3  │ u │ i │ a │ e │ o │ s │ n │ r │ t │ d │ y │ M3 │   │
├────┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴────┴───┤
│Ums │ M4│ ü │ ö │ ä │ p │ z │ b │ m │ , │ . │ j │  Umsch  │
├────┼───┴┬──┴─┬─┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬────┬───┤
│Str │ Fe │ Al │      Leerzeichen       │ M4 │ Fe │ Me │Str│
└────┴────┴────┴────────────────────────┴────┴────┴────┴───┘

    """
    lay = "┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──────┐\n"
    lay +="│ "
    lay += " │ ".join([l[0] for l in layout[0]])
    lay += "    │\n" 
    lay += "├───┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬─────┤\n"
    lay += "│  " 
    lay += " │ ".join([l[0] for l in layout[1][:-1]])
    lay += " │ Ret │\n"
    lay += "├────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─┐   │\n"
    lay += "│   "
    if layout[2][-2]: 
        lay += " │ ".join([l[0] for l in layout[2][:-1]])
    else:
        lay += " │ ".join([l[0] for l in layout[2][:-2]])
        lay += " │  "
    lay += "  │   │\n"
    lay += "├────┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴────┴───┤\n"
    if layout[3][1]:
        lay += "│  "
        lay += " │ ".join([l[0] for l in layout[3]])
    else:
        lay +="│  ⇧ │ M4│ "
        lay += " │ ".join([l[0] for l in layout[3][2:]])
    lay += "       │\n"
    lay += """├────┼───┴┬──┴─┬─┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬────┬───┤
│Str │ Fe │ Al │      Leerzeichen       │ M4 │ Fe │ Me │Str│
└────┴────┴────┴────────────────────────┴────┴────┴────┴───┘"""
    return lay
    

def short_number(s, letters=5):
    """shorten a number to the given number of letters"""
    return str(s)[:letters]

def print_layout_with_statistics(layout, letters=None, repeats=None, number_of_letters=None, number_of_bigrams=None, print_layout=True, trigrams=None, number_of_trigrams=None, verbose=False, data=None, shorten_numbers=False):
    """Print a layout along with statistics."""
    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(
        data=data, 
        letters=letters, number_of_letters=number_of_letters,
        repeats=repeats, number_of_bigrams=number_of_bigrams,
        trigrams=trigrams, number_of_trigrams=number_of_trigrams
        )

    if print_layout:
        print(format_layer_1_string(layout))
        print(format_keyboard_layout(layout))
        #from pprint import pprint
        #pprint(layout[:5])

    total, frep_num, cost, frep_top_bottom, disbalance, no_handswitches, line_change_same_hand = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams)[:7]
    total, cost_w, frep_num_w, frep_num_top_bottom_w, neighboring_fings_w, fing_disbalance_w, no_handswitches_w, badly_positioned_w, line_change_same_hand_w, no_switch_after_unbalancing_w = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams, return_weighted=True)[:10]

    hand_load = load_per_hand(letters, layout=layout)

    if shorten_numbers: 
        sn = short_number
    else:
        sn = str
    
    print("#", sn(total / 1000000000), "billion total penalty compared to notime-noeffort")
    print("#", sn(cost / number_of_letters), "mean key position cost in file 1gramme.txt", "(", str(cost_w/1000000000), ")")
    print("#", sn(100 * frep_num / number_of_bigrams), "% finger repeats in file 2gramme.txt", "(", str(frep_num_w/1000000000), ")")
    if verbose: 
        print("#", sn(disbalance / 1000000), "million keystrokes disbalance of the fingers", "(", str(fing_disbalance_w/1000000000), ")")
        print("#", sn(100 * frep_top_bottom / number_of_bigrams), "% finger repeats top to bottom or vice versa", "(", str(frep_num_top_bottom_w/1000000000), ")")
        print("#", sn(100 * no_handswitches / number_of_trigrams), "% of trigrams have no handswitching (after direction change counted x", WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, ")", "(", str(no_handswitches_w/1000000000), ")")
        print("#", sn(line_change_same_hand / 1000000000), "billion (rows²/dist)² to cross", "(", str(line_change_same_hand_w/1000000000), ")")
        print("#", sn(abs(hand_load[0]/sum(hand_load) - 0.5)), "hand disbalance. Left:", hand_load[0]/sum(hand_load), "%, Right:", hand_load[1]/sum(hand_load), "%")
        print("#", sn(badly_positioned_w/1000000000), "badly positioned shortcut keys (weighted).")
        print("#", sn(no_switch_after_unbalancing_w/1000000000), "no handswitching after unbalancing key (weighted).")
        print("#", sn(neighboring_fings_w/100000000), "movement pattern cost (weighted).")


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
    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=num_letters, number_of_bigrams=num_reps, trigrams=trigs, number_of_trigrams=num_trigs, verbose=verbose, shorten_numbers=True)
        
    if not quiet:
        print("\nQwertz for comparision")
        print_layout_with_statistics(QWERTZ_LAYOUT, letters=letters, repeats=repeats, number_of_letters=num_letters,
                                     number_of_bigrams=num_reps, trigrams=trigs, number_of_trigrams=num_trigs, verbose=verbose)
    

def find_a_qwertzy_layout(steps, prerandomize, quiet, verbose):
    """Find a layout with values similar to qwertz."""
    print("# Qwertzing Layout")
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
            print("doing", prerandomize, "randomization switches.")
        lay, keypairs = randomize_keyboard(abc, num_switches=prerandomize, layout=NEO_LAYOUT)
    else: lay = NEO_LAYOUT

    qvals = total_cost(letters=letters, repeats=repeats, layout=QWERTZ_LAYOUT, trigrams=trigrams, return_weighted=True)

    qhand_load = load_per_hand(letters, layout=QWERTZ_LAYOUT)

    def compare_with_qwertz(lay, base=QWERTZ_LAYOUT):
        """compare the layout with qwertz."""
        vals = total_cost(letters=letters, repeats=repeats, layout=lay, trigrams=trigrams, return_weighted=True)
        hand_load = load_per_hand(letters, layout=lay)
        diff = 0
        to_compare = zip(vals, qvals)
        for l,q in to_compare: 
            diff += (l - q)**2
        return diff

    diff = compare_with_qwertz(lay)

    for i in range(steps):
        lay = deepcopy(lay)
        l, keypairs = randomize_keyboard(abc, num_switches=prerandomize, layout=lay)
        d = compare_with_qwertz(l)
        if d < diff:
            print("# qwertzer")
            print(format_layer_1_string(l))
            lay = deepcopy(l)
            diff = d

    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)
    

def evolve_a_layout(steps, prerandomize, controlled, quiet, verbose, controlled_tail):
    """Evolve a layout by selecting the fittest of random mutations step by step."""
    print("# Mutating Neo")
    letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data()

    if prerandomize:
        if not quiet:
            print("doing", prerandomize, "prerandomization switches.")
        lay, keypairs = randomize_keyboard(abc, num_switches=prerandomize, layout=NEO_LAYOUT)
    else: lay = NEO_LAYOUT

    if controlled_tail:
        lay, cost = evolve_with_controlled_tail(letters, repeats, trigrams, layout=lay, iterations=steps, quiet=quiet)
    else: 
        lay, cost = evolve(letters, repeats, trigrams, layout=lay, iterations=steps, quiet=quiet, controlled=controlled)
    
    print("\n# Evolved Layout")
    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)


def evolution_challenge(layout=NEO_LAYOUT, challengers=100, rounds=10, iterations=400, abc=abc, prerandomize=10000, quiet=False, controlled=False):
     """Run a challenge between many randomized layouts, then combine the best pseudo-genetically (random) and add them to the challenge."""
     # Data for evaluating layouts.
     letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data()

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
         layouts = deepcopy(layouts[:int(challengers / 4)+1])
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

def best_random_layout(args, prerandomize, quiet=False):
    """Select the best of a number of randomly created layouts."""
    print("Selecting the best from", args[2], "random layouts.")
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
        lay, cost = find_the_best_random_keyboard(letters, repeats, trigrams, num_tries=int(args[2]), num_switches=int(PRERANDOMIZE), layout=NEO_LAYOUT, abc=abc, quiet=quiet)
    else: 
        lay, cost = find_the_best_random_keyboard(letters, repeats, trigrams, num_tries=int(args[2]), layout=NEO_LAYOUT, abc=abc, quiet=quiet)
        
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
     
    print_layout_with_statistics(NEO_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, print_layout=not quiet, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)
    
    if not quiet:
        print("\nQwertz for comparision")
        print_layout_with_statistics(QWERTZ_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)
        print("\nAnd the Nordtast Layout")
        print_layout_with_statistics(NORDTAST_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)
        print("\nAnd Dvorak")
        print_layout_with_statistics(DVORAK_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)
        print("\nAnd Colemak")
        print_layout_with_statistics(COLEMAK_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)


def check_a_layout_from_shell(layout_data, quiet, verbose):
    """Check a layout we get passed as shell argument."""
    layout = eval(layout_data)
    print_layout_with_statistics(layout, print_layout=not quiet, verbose=verbose, shorten_numbers=True)

def check_a_layout_string_from_shell(layout_string, quiet, verbose, base_layout=NEO_LAYOUT, data=None):
    """Check a string passed via shell and formatted as

    öckäy zhmlß,´
    atieo dsnru.
    xpfüq bgvwj

    or

    qwert zuiopü+
    asdfg hjklöä
    <yxcvb nm,.-
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
    
    print_layout_with_statistics(layout, print_layout=not quiet, verbose=verbose, data=data, shorten_numbers=True)

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

    if "--controlled-tail" in argv:
        CONTROLLED_TAIL = True
        argv.remove("--controlled-tail")
    else: CONTROLLED_TAIL = False

    if "--prerandomize" in argv: 
        PRERANDOMIZE = argv[argv.index("--prerandomize") + 1]
        argv.remove("--prerandomize")
        argv.remove(PRERANDOMIZE)
        PRERANDOMIZE = int(PRERANDOMIZE)
    else: PRERANDOMIZE = False
    
    if "--base" in argv: 
        BASE = argv[argv.index("--base") + 1]
        argv.remove("--base")
        argv.remove(BASE)
        BASE = eval(BASE)
    else: BASE = NEO_LAYOUT
    
    if "--file" in argv: 
        DATA = argv[argv.index("--file") + 1]
        argv.remove("--file")
        argv.remove(DATA)
        DATA = read_file(DATA)
    else: DATA = None
    
    if "--help" in argv:
        print(__usage__)
        exit()

    if argv[1:] and argv[1] == "--file":
        check_with_datafile(args=argv, quiet=QUIET, verbose=VERBOSE)

    elif argv[2:] and argv[1] == "--evolve":
        evolve_a_layout(steps=int(argv[2]), prerandomize=PRERANDOMIZE, quiet=QUIET, controlled=CONTROLLED_EVOLUTION, verbose=VERBOSE, controlled_tail=CONTROLLED_TAIL)
        
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

    elif argv[2:] and argv[1] == "--check-string":
        check_a_layout_string_from_shell(argv[2], quiet=QUIET, verbose=VERBOSE, data=DATA)
            
    else:
        check_the_neo_layout(quiet=QUIET, verbose=VERBOSE)
        
    #print(unique_sort(frep))
    
    #rep = repeats_in_file_sorted(path)
    #print(str(len(rep)), "repeats in file", path, "sorted.")
    #print([i for i in rep if "a" in i[1]])
