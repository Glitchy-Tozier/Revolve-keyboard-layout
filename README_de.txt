Einführung
==========

evolve-keyboard-layout ist ein evolutionärer Optimierer für die Tastenbelegung der Tastatur und ein Framework zur Abschätzung der Auswirkungen der Tastaturbelegung auf das Tippgefühl. 

Die wichtigste Anwendung ist die Optimierung der Tastaturbelegung durch wiederholte Einzelmutationen, die auf Grundlage festgelegter  Kostenfaktoren beibehalten oder verworfen werden. 

Installation
============

Abhängigkeiten (müssen separat installiert werden):

* Python 3.x: http://python.org/download
* Mercurial: http://mercurial.selenic.com/downloads/

Dann einfach installieren über: 

    hg clone https://bitbucket.org/ArneBab/evolve-keyboard-layout/

Verwendung
==========

Eine Evolution laufen lassen und die Ausgaben in output.txt speichern: 

./evolution.py

Eine bestimmte Grundbelegung prüfen (nur *nix Systeme, verflucht sei die Windows console!):

./check_neo.py -v --fingerstats --check-string "xvlcw khgfqß´
uiaeo snrtdy
üöäpz bm,.j"

Eine SVG-Darstellung der Belegung erstellen: 

./bigramm_statistik.py --svg --svg-output layout.svg -l "xvlcw khgfqß´
uiaeo snrtdy
üöäpz bm,.j"

Parameter und weitere Nutzungsmöglichkeiten finden Sie über die folgenden Befehle: 

    ./evolution.py --help
    ./check_neo.py --help
    ./convert_text_between_layouts.py --help
    ./regularity_check.py --help
    ./textcheck.py --help


Dokumentation
=============

Ein Leitfaden zum Optimierer. Er soll die Fragen beantworten, die in der Liste (oder bei sonstigen Interessierten) aufkommen könnten. Praktisch gesehen also eure Fragen :)

(Schreibt mir einfach, was ihr gerne wissen würdet, ich versuche es dann zu beantworten. Und scheut euch nicht, mir konstruktiv reinzuschreiben – dafür ist das Pad hier da :))

0. Grundlagen
-------------

Das Programm hat zwei Hauptfunktionen:

1. Tastaturbelegungen bewerten
2. Tastaturbelegungen nach der Bewertung optimieren

Für die Bewertung nutzt es die Häufigkeiten von Buchstaben, Bigrammen und Trigrammen, entweder aus dem Leipziger Korpus oder aus einer beliebigen Textdatei.

1. Kostenberechnung
-------------

### 1.1. Buchstaben (1-Gramme)

1. Für die Buchstaben nutzt es eine nach Erfahrung generierte Liste mit Tastenaufwänden (Kosten):

COST_PER_KEY  = [
    [50,    40,35,30,30, 35,   40,35,30,30,30,35,40,50], # Zahlenreihe (0)
    [24,    20, 6, 4, 6, 9,    10, 6, 4, 5, 8,24,36, 0], # Reihe 1
    [5,      3, 3, 3, 3, 5,     5, 3, 3, 3, 3, 5,10,18], # Reihe 2
    [15,10, 12,24,20, 5,    30, 6, 5,22,22,10,      15],     # Reihe 3
    [0,0,0,               3            , 7, 0, 0, 0] # Reihe 4 mit Leertaste
]

Für jeden Buchstaben wird seine Häufigkeit mit den Kosten der Taste, auf der er liegt, multipliziert. Alle Buchstabenkosten werden addiert, um die Positionskosten zu erhalten.

Dabei werden Buchstaben in höheren Ebenen (Großbuchstaben und z. B. δ oder ℝ) in Kleinbuchstaben und Modifikatoren aufgeteilt – bzw. in die Buchstaben auf Ebene 0 und alle für die Buchstaben nötigen Modifikatoren.

10× im Text vorkommendes „(“ wird also zu 10×M3 und 10×n.


2. Dazu kommen Kosten für ungleiche Belastung der Finger. Die Anzahl der Anschläge je Fingern soll im Verhältnis 1:1,6:2:2:2::2:2:2:1,6:1 (10 Finger: 4 je Hand + Spreizung nach innen) sein, vom linken kleinen Finger zum Zeigefinger, linken Daumen, rechten Daumen und dann vom rechten Zeigefinger zum kleinen Finger. Muss ein Finger mehr oder weniger anschlagen, wird die jeweilige Abweichung quadriert (das ist etwas vereinfacht; im Detail: Standardabweichung). Alles addiert ergibt die Kosten durch Fingerdisbalance. Die Kosten werden mit 300 multipliziert.

3. Außerdem kommt ein Kostenfaktor durch ungleiche Handbelastung dazu. Die Abweichung von 50 % (0,5) wird mit der Anzahl Anschläge und mit 60 multipliziert, um die Kosten zu erhalten.

3. Außerdem kommt ein Kostenfaktor durch ungleiche Handbelastung dazu. Die Abweichung von 50% (0,5) wird mit der Anzahl Anschläge und mit 60 multipliziert, um die Kosten zu erhalten.

### 1.2. Bigramme

Die Kosten von Bigrammen werden über mehrere Kriterien festgelegt.


1. Fingerwiederholungen: Jede Fingerwiederholung (8 Finger: 4 je Hand) gibt 512 Strafpunkte. Geht sie von der oberen in die untere Reihe oder umgekehrt gibt sie sogar 2048 Strafpunkte.


2. Zeilenwechsel: Für Zeilenwechsel auf der gleichen Hand gibt es Strafpunkte. Dabei wird Anzahl der Zeilen, die übersprungen werden quadriert, durch die Anzahl der Spalten geteilt, die zwischen den Tasten liegen und das Ergebnis nochmal quadriert. Liegen sie in der selben Spalte, gilt das als ¼-Spaltenabstand.

Das Ergebnis wird mit 6 multipliziert.

Komplexität: Wenn der Zeilenwechsel nach oben geht und ein langer Finger auf einen kurzen Finger folgt, wird die Anzahl der Zeilen um 1 reduziert. Genauso, wenn der Zeilenwechsel nach unten geht und ein kurzer auf einen langen Finger folgt. Lange Finger sind Mittel- und Ringfinger. Kurze Finger sind Zeigefinger und kleiner Finger.

   Beispiel: In Neo liegt „f“ auf der obener Zeile und „r“ in der mittleren. Ein Wechsel von „f“ auf „r“ hat also einen Abstand von 1 Zeile. Quadriert ist das immernoch 1. Der Abstand in Spalten ist 1. 1 durch 1 ist immernoch 1. Quadriert immernoch 1. Multipliziert mit 6 ergibt das 6 Strafpunkte × Häufigkeit des Bigramms fr.
   Andererseits liegt „c“ auf der oberen Zeile und „ä“ auf der unteren. Der Abstand ist also 2, quadriert 4. Der Spaltenabstand ist 1. 4 durch 1 sind immernoch 4, quadriert 16. Multipliziert mit 6 ergibt 96 Strafpunkte × Häufigkeit des Bigramms „cä“, also etwa ⅕ der Kosten einer Fingerwiederholung.


3. Fingerübergänge: Bestimmte Übergänge von einem Finger auf den anderen sollen vermieden werden. Kleiner Finger auf Ringfinger gibt 3 Strafpunkte, auf Mittelfinger gibt 2. Ringfinger auf kleinen Finger gibt 4 Strafpunkte, auf Mittelfinger gibt 2. Mittelfinger auf Ringfinger gibt 3 Strafpunkte, auf kleinen Finger gibt 2. Übergänge zum und vom Zeigefinger kosten nichts. Die Strafpunkte aller Bigramme werden addiert und mit 30 multipliziert.

4. Fingerspreizung: Wenn nach einem Anschlag auf eine Taste, die die Hand aus der Grundposition zieht, kein Handwechsel kommt, gibt das 20 Strafpunkte. Ist die Taste besonders weit draußen, werden die Kosten verdoppelt. In Neo2 sind die Buchstaben, die die Hand aus dem Gleichgewicht ziehen M3l, xqosyb. Besonders weit draußen sind Tab, M3r, Return, ShiftL, wkßz. (Definition: config.py, Zeile 90 und layout_cost.py, Zeile 175). Die Kosten werden mit 20 multipliziert.

4. Fingerspreizung: Wenn nach einem Anschlag auf eine Taste, die die Hand aus der Grundposition zieht, kein Handwechsel kommt, gibt das 20 Strafpunkte. Ist die Taste besonders weit draußen, werden die Kosten verdoppelt. In Neo2 sind die Buchstaben, die die Hand aus dem Gleichgewicht ziehen M3l, xqosyb. Besonders weit draußen sind Tab, M3r, Return, ShiftL, wkßz. (Definition: config.py, Zeile 90 und layout_cost.py, zeile 175). Die Kosten werden mit 20 multipliziert.

### 1.3. Trigramme

1. Indirekte Bigramme: Bei Trigrammen mit zwei Handwechseln werden der erste und der letzte Buchstabe als indirektes Bigramm gewertet und mit um 70% reduzierter Häufigkeit zu den Bigrammen hinzugefügt.

2. Handwechsel nach Richtungswechsel: Wenn in einem Trigramm ohne Handwechsel die Richtung gewechselt wird (also die zweite Taste rechts von der ersten ist, die dritte aber links von der zweiten oder umgekehrt), gibt es 300 Strafpunkte.

### 1.4. Buchstabensplitting

Großbuchstaben und auch alle Zeichen von Ebenen über der ersten werden in mehrere Tasten aufgeteilt.

Bei Einzelbuchstaben kommen einfach die Modifikatortasten mit der gleichenhäufigkeit wie der Buchstabe hinzugefügt und der Buchstabe durch das Zeichen auf der ersten Ebene ersetzt.

A wird zu Shift+a und Γ wird zu M3+M4+g.

Bei Bigrammen werden die Modifikatortaste für das modifizierte Zeichen und für das Zeichen danach gewertet.

Bei Neo2:

• Ab wird zu ShiftR-a, ShiftR-b, ab.
• aB wird zu a-ShiftL, ShiftL-b, ab.

Jeweils mit der Modifikatortaste auf der anderen Hand als der Buchstabe (logisch).

Trigramme funktionieren in etwa genauso, nur gibt es mehr Optiomen. Für Großschreibung nimm alle Trigramme, die du aus dem folgenden Bild basteln kannst:

a → b → c
| × | × |
sa→ sb→ sc

Senkrechte in beide Richtungen. Kreuze nur nach vorne. sa = das Shift, das zu a gehört (andere Hand).

### 1.5 Korpus

#### Allgemein

#### Nur für Arne

ngrams.NGrams("ngrams.config")

ngrams.config: 

    # ngrams source v0.1
    weight filepath
    weight filepath
    …

2. Optimierung
-------------

Mit der Kostenberechnung können jetzt die Kosten jeder Belegung berechnet werden. Zur Optimierung werden nun zwei zufällig gewählte Tasten vertauscht. Wenn danach die Kosten der Belegung geringer sind, wird die geänderte Belegung behalten. Ansonsten wird die Änderung rückgängig gemacht.

Zur Effizienzsteigerung werden bei den ersten Optimierungsschritten mehrere Tasten getauscht, um eine erste Annäherung zu erhalten. Erst 100 Schritte lang 5 Paare, dann 100 Schritte lang 4, dann 3, dann 2. Für alle weiteren Vertauschungen werden dann nur noch Einzelpaare getauscht (Stichwort simulated annealing).

Nach 4000 zufälligen Optimierungsschritten werden dann noch einmal alle möglichen Einzel-Vertauschungen geprüft und die beste davon durchgeführt. Das wird so lange wiederholt, bis es keine Einzel-Vertauschung mehr gibt, deren Kosten geringer sind als die unveränderte Belegung. So wird sichergestellt, dass keine Einzelvertauschung die Belegung verbessern kann.

3. Verwendung
-------------

*Vorbemerkung: Windows-Nutzer sollten das ./ am Anfang von Befehlen weglassen*

Für die Optimierung gibt es 2 Hauptskripte:

• check_neo.py
• evolution.py

check_neo.py hat das flexiblere Interface und wird von evolution.py mitverwendet. Es funktioniert aber nicht unbedingt auf Windows (Windows-Konsole sei verflucht für deine Unicode-Probleme!). evolution.py dagegen funktioniert unter Windows. Es liefert die Oberfläche zum gemeinsamen Optimieren (cloud optimizing ;)).

Die grundlegenden Anwendungen von check_neo.py sind:

• sich die Werte von Belegungen ausgeben lassen:
  ./check_neo.py [-v] [--fingerstats]; für ein paar Beispiele: Neo, Qwertz, Nordtast, Dvorak, … --fingferstats gibt die Lastverteilung auf die Finger mit aus. -v gibt für jede Belegung ausführlichere Informationen aus. Ohne -v gibt es nur die Gesamtkosten und die Fingerwiederholungen. Mit -v gibt es noch 8 weitere Kriterien (siehe http://wiki.neo-layout.org/wiki/Neo3/Optimierungskriterien ).
  ./check_neo.py --check-string "xzo., pcslvß´
    haeiu dtrnmf
    ⇚kyäüö bgjqw" [-v] ; Die Buchstaben auf Ebene 1, 2, 5 und 6 so anordnen, dass sie auf Ebene 1 den gegebenen Buchstaben entsprechen, dann die entstehende Belegung prüfen.
  --file dateiname.txt ermöglichst es außerdem, die Belegung mit dem Text in der Datei zu prüfen, statt mit dem Standardkorpus (1gramme.txt, 2gramme.txt und 3gramme.txt).

• Eine Evolution starten:
  ./check_neo.py --evolve N [--controlled-tail] ; N Mutationsschritte machen, ausgehend von einer Zufallsbelegung.

• Viele weitere Möglichkeiten findet ihr via ./check_neo.py --help


Die grundlegende Anwendung von evolution.py ist es, mehrere Mutationsläufe hintereinander zu starten und die Ergebnisse in output.txt zu speichern.

./evolution.py ; das sollte unter Windows laufen
./evolution.py --not-quiet ; das tut nicht unter Windows, gibt aber zusätzliche Statusinfos aus
./evolution.py --file dateiname.txt ; nutzt die Datei als Korpus.
./evolution.py -o ausgabedatei.txt ; schreibt die Ergebnisse in eine andere Datei.

Die Parameter können alle kombiniert werden, und auch hier gibt ./evolution.py --help zusätzliche Optionen aus.


4. Weitere Möglichkeiten
------------------------

Zusätzlich zum Testen gibt es noch einige weitere Skripte. Auch hier zeigt ./script.py --help meist einige weitere Möglichkeiten auf.

./get_the_best_layouts.sh datei.txt [N] ; gibt die N besten Belegungen in einer Ausgabedatei aus, lässt Duplikate weg.

bigramm_statistik.py nimmt alle Bigramme aus dem Korpus, rechnet für jedes einzelne Bigramm die Kosten und stellt sie auf verschiedene Art dar:

• Als Zahlenwerte auf stdout:
  ./bigramm_statistik.py -l "xvlcw khgfqß´
uiaeo snrtdy
⇚üöäpz bm,.j"

• Als Balkendiagramme aus stdout:
  ./bigramm_statistik.py --bars -l "xvlcw khgfqß´
uiaeo snrtdy
⇚üöäpz bm,.j"

• Als SVG Bild:
  ./bigramm_statistik.py --svg --svg-output belegung.svg -l "xvlcw khgfqß´
uiaeo snrtdy
⇚üöäpz bm,.j"

Für Windows-Nutzer gibt es die Option, eintach nur die erste Zeile der Belegung einzutragen. Das Programm fragt dann nach den weiteren Zeilen.


./recheck_all_result_layouts.py  [--folder <Ordner>] [--namepart <name>] [--families] [--csv  || --svg]; alle Ergebnisse in Textdateien (*.txt) im gegebenen Ordner,  in deren Name der --namepart vorkommt, neu berechnen. Mit --families  werden sie in ähnliche Belegungen sortiert und nur jeweils die besten  jeder Familie angezeigt. Mit --csv werden die Ergebnisse statt in einer  normalen Ausgabe als csv-Tabelle ausgegeben. Und mit --svg werden für alle Belegungen SVG-Bilder erstellt und im Ordner svgs/ gespeichert. Die Dateinamen sind dabei <Gesamtkosten>-<Grundlinie>-<Obere Zeile>-<Untere Zeile>.svg.

./generate_xmodmap.py datei.txt > belegung.xmodmap; gibt eine xmodmap für die Belegung aus. datei.txt hat in der ersten Zeile den Namen der Belegung und in den nächsten drei Zeilen die erste Ebene der Belegung. Eine Beispieldatei ist in empirie/haeiu.txt.

./regularity_check.py [-n layout-name || -l <layout-string 3 Zeilen>] -t textdatei.txt [-v]; prüft die Regelmäßigkeit der Belegung für die gegebene Textdatei. Dafür wird der Text in Worte und in Abschnitte zu 270 Zeichen zerlegt. Für jedes Wort und jeden Abschnitt werden dann die Kosten gerechnet. Von den Kosten werden für alle Worte und alle Abschnitte der Durchschnittzwert und die Standardabweichung ausgegeben, um zu testen, wie gleichmäßig das Tippen mit der Belegung sein dürfte. Der Hintergrund ist, dass so geprüft werden kann, ob es besonders unschöne Ausreißer gibt, also Wörter oder Textabschnitte, die sehr unangenehm zu tippen sind.

./textcheck.py dateiname.txt [--best-lines] ; prüft, wie nah ein gegebener Text an der nGramm-Verteilung des Korpus ist (1gramme.txt, 2gramme.txt, 3gramme.txt). Mit --best-lines sucht es die Textzeilen, die dem Korpus am ählichsten sind.

./convert_text_between_layouts.py --layout "kuü.ä vgcljf
hieao dtrnsß
⇚xyö,q bpwmz" --base "xvlcw khgfqß
uiaeo snrtdy
⇚üöäpz bm,.j" --file textdatei.txt ; konvertiert einen Text von der belegung --layout in die Belegung --base, so dass das herauskommende Buchstabengewirr mit der Belegung --base getippt werden kann und dabei die Tasten angeschlagen werden, die in der Belegung --layout genutzt würden.

pypy3.3-5.5-alpha-20161013-linux_x86_64-portable/bin/pypy ./recheck_all_result_layouts.py --folder results-2016-regularity/ --csv --regularity > regularity.csv
./plotcorrelation.py regularity.csv ; erzeugt eine Kovarianzmatrix der verschiedenen Kostenfaktoren. Mit total cost unkorrelierte Werte sind bei allen Layouts näherungsweise gleich, positiv korrellierte werden am Ende vom Optimierer zurechtgezurrt, negativ korrelierte werden zum Ende hin zu Gunsten anderer Faktoren verschlechtert.
