#!/usr/bin/env python3
# encoding: utf-8

"""Design discusions and decisions for the layout optimizer (mostly in german)."""

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
- Erst Evolution (~3000), dann so lange kontrolliert (immer bester Schritt), bis es keine Verbesserung mehr gibt.

Option:
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


### Weitere Ideen

* Trigramme sollten vielleicht Bögen schlagen. lieber „ach“ als „leg“.
* 

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

