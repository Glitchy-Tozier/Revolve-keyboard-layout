# Revolve keyboard layout

This project originated from the _excellent_ [script of Arne Babenhauserheide](https://hg.sr.ht/~arnebab/evolve-keyboard-layout "evolve-keyboard-layout"). The purpose of **Revolve keyboard layout** is to improve upon that script in the following ways (ordered from most to least important):
1. Make the optimizer run faster.
2. Clean up unnecessary files and store them in places where they don't get into the way of development.
3. Make the optimizer run faster.
4. Introduce true [simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing "A probabilistic technique for approximating the global optimum of a given function"): Replace `the current greedy algorithm that varies the size of changes` with `a probability-driven algorithm, that always switches the same number of letters`.
6. Possibly re-write the most resource-intensive-tasks in [Rust](https://www.rust-lang.org/ "The most amazing language the world has ever seen"). (This was _one_ reason for the name _**R**evolve keyboard layout_).
7. Using tools such as [RustPython](https://rustpython.github.io/ "All things shall rust"), convert the optimizer to [Web Assembly](https://webassembly.org/ "Basically compiled JavaScript") and make it run on a website. This would allow anyone to simply open a website and start optimizing immediately.

Additionally, I plan on making the optimizer run faster. This will be accomplished mainly by [removing redundant calculations](https://github.com/Glitchy-Tozier/Revolve-keyboard-layout/commit/a6bbcea18b098f9e002108bdb8fca10ebc1bce8c "An example of optimizing code"), on various scales.

## Contributing

The two biggest most straight-forward things you can do are:
* Translate this README.md or code&comments in Python-files to English
* If you have some Python-knowledge, look into the code (especially [the most resource-intensive functions](https://github.com/Glitchy-Tozier/Revolve-keyboard-layout/blob/main/profilings/0_original.txt "The first profiling of a keyboard-evolution-run")) and find ways to make everything run faster.

## Achievements:

At the current time, the Script runs about 8 times as fast as the original one. The main speedup resulted from [this commit](https://github.com/Glitchy-Tozier/Revolve-keyboard-layout/commit/82f456b970915a070ea15936806de5bfa71d04bf).

---

Intro
=====

**Revolve keyboard layout** is an evolutionary keyboard layout optimizer and a framework for evaluating the effect of the keyboard layout on typing.

The most common use is to optimize the keyboard layout based on several cost criteria by doing random mutations and keeping those which reduce the cost.

Install
=======

Prerequisites:
* Python 3.x: http://python.org/download

```bash
git clone https://github.com/Glitchy-Tozier/Revolve-keyboard-layout.git
```

Usage
=====

**For performance-reasons, it is recommended to use a tool such as [`pypy3`](https://www.pypy.org/ "A JIT compiler for Python") instead of `python3` to start an evolution.**

Do an evolution and store the results in output.txt:
```bash
./evolution.py
```

Check a layout string (only *nix systems, curse you, windows console!): 
```bash
./check_neo.py -v --fingerstats --check-string "xvlcw khgfq????
uiaeo snrtdy
??????pz bm,.j"
```

Create a layout SVG: 
```bash
./bigramm_statistik.py --svg --svg-output layout.svg -l "xvlcw khgfq????
uiaeo snrtdy
??????pz bm,.j"
```

Additional options:
* `./evolution.py --help` ; simple evolution
* `./check_neo.py --help` ; various actions
* `./convert_text_between_layouts.py --help` ; generate text for writing tests
* `./regularity_check.py --help` ; check the deviations from the typing flow
* `./textcheck.py --help` ; check the difference between a given text and an ngram korpus


Documentation
=============

A guide to the Optimizer. It intends to answer common questions. 

## 0. Basics

The program has two main functions: 

1. Evaluate Keyboard layouts
2. Optimize layouts based on the evaluation

For evaluation it gives any keyboard layout a penalty (signifying the strain and inconvenience it imposes on typing) based on the distribution of letters, bigrams and trigrams, either from the reference corpus of the university of Leipzig or from any given Textfile. 

### 0.1 Results for the impatient

The following lists analyses from the optimizer for common keyboard layouts. You can recreate them by simply calling:
```bash
./check_neo.py -v
```

#### Neo

xvlcw khgfqy??  
uiaeo snrtd???  
??????pz bm,.j

    13.41630 x100 total penalty per letter
    49.10005 x10 billion total penalty compared to notime-noeffort
    7.359111 mean key position cost in file 1gramme.txt ( 53.86473966 )
    41.17544 % finger repeats in file 2gramme.txt ( 165.6421844101187 )

#### Qwertz

qwert zuiop??+  
asdfg hjkl????  
<yxcvb nm,.-

    29.52990 x100 total penalty per letter
    108.0715 x10 billion total penalty compared to notime-noeffort
    12.11769 mean key position cost in file 1gramme.txt ( 88.6950124 )
    61.32098 % finger repeats in file 2gramme.txt ( 246.68447929659453 )

#### AdNW

ku??.?? vgcljf??  
hieao dtrns??  
xy??,q bpwmz

    8.785617 x100 total penalty per letter
    32.15299 x10 billion total penalty compared to notime-noeffort
    7.708996 mean key position cost in file 1gramme.txt ( 56.42570664 )
    11.17019 % finger repeats in file 2gramme.txt ( 44.93589397582505 )

#### CRY

bmuaz kdflvj??  
criey ptsnh???  
x????o?? wg,.q

    8.459790 x100 total penalty per letter
    30.96055 x10 billion total penalty compared to notime-noeffort
    7.596530 mean key position cost in file 1gramme.txt ( 55.60251188 )
    13.55902 % finger repeats in file 2gramme.txt ( 54.54576909689781 )

#### Dvorak

???,.py fgcrl/=  
aoeui dhtns-  
;qjkx bmwvz

    11.45381 x100 total penalty per letter
    41.91789 x10 billion total penalty compared to notime-noeffort
    11.55219 mean key position cost in file 1gramme.txt ( 84.55588602 )
    17.19619 % finger repeats in file 2gramme.txt ( 69.17751009644823 )

#### Colemak

qwfpg jluy;[]  
arstd hneio`  
zxcvb km,./

    12.01156 x100 total penalty per letter
    43.95908 x10 billion total penalty compared to notime-noeffort
    12.14284 mean key position cost in file 1gramme.txt ( 88.87909212 )
    21.47616 % finger repeats in file 2gramme.txt ( 86.39515579324566 )

#### Workman

qdrwq jfup??????  
ashtg yneoi??  
zxhcv kl,.'

    10.38274 x100 total penalty per letter
    37.99805 x10 billion total penalty compared to notime-noeffort
    12.90420 mean key position cost in file 1gramme.txt ( 94.4518264 )
    18.30581 % finger repeats in file 2gramme.txt ( 73.64136282268564 )

#### Capewell

.mydg ;wh,'????  
aresf ktnio??  
xczvj bpluq

    11.63464 x100 total penalty per letter
    42.57965 x10 billion total penalty compared to notime-noeffort
    9.281227 mean key position cost in file 1gramme.txt ( 67.9335876 )
    16.39290 % finger repeats in file 2gramme.txt ( 65.94603890759558 )

#### Carpalx QGMLWY

qgmlw byv;??????  
dstnr iaeoh??  
zxcfj kp,.'

    11.72387 x100 total penalty per letter
    42.90624 x10 billion total penalty compared to notime-noeffort
    12.18783 mean key position cost in file 1gramme.txt ( 89.2084158 )
    26.38692 % finger repeats in file 2gramme.txt ( 106.15034611209443 )



## 1. Calculating the cost

(The remaining text was not yet translated into English)

### 1.1. Buchstaben (1-Gramme)

1. F??r die Buchstaben nutzt es eine nach Erfahrung generierte Liste mit Tastenaufw??nden (Kosten):
```python
COST_PER_KEY  = [
    [50,    40,35,30,30, 35,   40,35,30,30,30,35,40,50], # Zahlenreihe (0)
    [24,    20, 6, 4, 6, 9,    10, 6, 4, 5, 8,24,36, 0], # Reihe 1
    [5,      3, 3, 3, 3, 5,     5, 3, 3, 3, 3, 5,10,18], # Reihe 2
    [15,10, 12,24,20, 5,    30, 6, 5,22,22,10,      15],     # Reihe 3
    [0,0,0,               3            , 7, 0, 0, 0] # Reihe 4 mit Leertaste
]
```
F??r jeden Buchstaben wird seine H??ufigkeit mit den Kosten der Taste, auf der er liegt, multipliziert. Alle Buchstabenkosten werden addiert, um die Positionskosten zu erhalten.

Dabei werden Buchstaben in h??heren Ebenen (Gro??buchstaben und z.???B. ?? oder ???) in Kleinbuchstaben und Modifikatoren aufgeteilt ??? bzw. in die Buchstaben auf Ebene 0 und alle f??r die Buchstaben n??tigen Modifikatoren.

10?? im Text vorkommendes ???(??? wird also zu 10??M3 und 10??n.


2. Dazu kommen Kosten f??r ungleiche Belastung der Finger. Die Anzahl der Anschl??ge je Fingern soll im Verh??ltnis 1:1,6:2:2:2::2:2:2:1,6:1 (10 Finger: 4 je Hand + Spreizung nach innen) sein, vom linken kleinen Finger zum Zeigefinger, linken Daumen, rechten Daumen und dann vom rechten Zeigefinger zum kleinen Finger. Muss ein Finger mehr oder weniger anschlagen, wird die jeweilige Abweichung quadriert (das ist etwas vereinfacht; im Detail: Standardabweichung). Alles addiert ergibt die Kosten durch Fingerdisbalance. Die Kosten werden mit 300 multipliziert.

3. Au??erdem kommt ein Kostenfaktor durch ungleiche Handbelastung dazu. Die Abweichung von 50???% (0,5) wird mit der Anzahl Anschl??ge und mit 60 multipliziert, um die Kosten zu erhalten.

3. Au??erdem kommt ein Kostenfaktor durch ungleiche Handbelastung dazu. Die Abweichung von 50% (0,5) wird mit der Anzahl Anschl??ge und mit 60 multipliziert, um die Kosten zu erhalten.

### 1.2. Bigramme

Die Kosten von Bigrammen werden ??ber mehrere Kriterien festgelegt.


1. Fingerwiederholungen: Jede Fingerwiederholung (8 Finger: 4 je Hand) gibt 512 Strafpunkte. Geht sie von der oberen in die untere Reihe oder umgekehrt gibt sie sogar 2048 Strafpunkte.


2. Zeilenwechsel: F??r Zeilenwechsel auf der gleichen Hand gibt es Strafpunkte. Dabei wird Anzahl der Zeilen, die ??bersprungen werden quadriert, durch die Anzahl der Spalten geteilt, die zwischen den Tasten liegen und das Ergebnis nochmal quadriert. Liegen sie in der selben Spalte, gilt das als ??-Spaltenabstand.

Das Ergebnis wird mit 6 multipliziert.

Komplexit??t: Wenn der Zeilenwechsel nach oben geht und ein langer Finger auf einen kurzen Finger folgt, wird die Anzahl der Zeilen um 1 reduziert. Genauso, wenn der Zeilenwechsel nach unten geht und ein kurzer auf einen langen Finger folgt. Lange Finger sind Mittel- und Ringfinger. Kurze Finger sind Zeigefinger und kleiner Finger.  
Beispiel: In Neo liegt ???f??? auf der obener Zeile und ???r??? in der mittleren. Ein Wechsel von ???f??? auf ???r??? hat also einen Abstand von 1 Zeile. Quadriert ist das immernoch 1. Der Abstand in Spalten ist 1. 1 durch 1 ist immernoch 1. Quadriert immernoch 1. Multipliziert mit 6 ergibt das 6 Strafpunkte ?? H??ufigkeit des Bigramms fr.  
Andererseits liegt ???c??? auf der oberen Zeile und ???????? auf der unteren. Der Abstand ist also 2, quadriert 4. Der Spaltenabstand ist 1. 4 durch 1 sind immernoch 4, quadriert 16. Multipliziert mit 6 ergibt 96 Strafpunkte ?? H??ufigkeit des Bigramms ???c?????, also etwa ??? der Kosten einer Fingerwiederholung.


3. Finger??berg??nge: Bestimmte ??berg??nge von einem Finger auf den anderen sollen vermieden werden. Kleiner Finger auf Ringfinger gibt 3 Strafpunkte, auf Mittelfinger gibt 2. Ringfinger auf kleinen Finger gibt 4 Strafpunkte, auf Mittelfinger gibt 2. Mittelfinger auf Ringfinger gibt 3 Strafpunkte, auf kleinen Finger gibt 2. ??berg??nge zum und vom Zeigefinger kosten nichts. Die Strafpunkte aller Bigramme werden addiert und mit 30 multipliziert.

4. Fingerspreizung: Wenn nach einem Anschlag auf eine Taste, die die Hand aus der Grundposition zieht, kein Handwechsel kommt, gibt das 20 Strafpunkte. Ist die Taste besonders weit drau??en, werden die Kosten verdoppelt. In Neo2 sind die Buchstaben, die die Hand aus dem Gleichgewicht ziehen M3l, xqosyb. Besonders weit drau??en sind Tab, M3r, Return, ShiftL, wk??z. (Definition: config.py, Zeile 90 und layout_cost.py, Zeile 175). Die Kosten werden mit 20 multipliziert.

### 1.3. Trigramme

1. Indirekte Bigramme: Bei Trigrammen mit zwei Handwechseln werden der erste und der letzte Buchstabe als indirektes Bigramm gewertet und mit um 70% reduzierter H??ufigkeit zu den Bigrammen hinzugef??gt.

2. Handwechsel nach Richtungswechsel: Wenn in einem Trigramm ohne Handwechsel die Richtung gewechselt wird (also die zweite Taste rechts von der ersten ist, die dritte aber links von der zweiten oder umgekehrt), gibt es 300 Strafpunkte.

### 1.4. Buchstabensplitting

Gro??buchstaben und auch alle Zeichen von Ebenen ??ber der ersten werden in mehrere Tasten aufgeteilt.

Bei Einzelbuchstaben werden einfach die Modifikatortasten mit der gleichen H??ufigkeit wie der Buchstabe hinzugef??gt und die Buchstaben durch das Zeichen auf der ersten Ebene ersetzt.

A wird zu Shift+a und ?? wird zu M3+M4+g.

Bei Bigrammen werden die Modifikatortaste f??r das modifizierte Zeichen und f??r das Zeichen danach gewertet.

Bei Neo2:

* Ab wird zu ShiftR-a, ShiftR-b, ab.
* aB wird zu a-ShiftL, ShiftL-b, ab.

Jeweils mit der Modifikatortaste auf der anderen Hand als der Buchstabe (logisch).

Trigramme funktionieren in etwa genauso, nur gibt es mehr Optionen. F??r Gro??schreibung nimm alle Trigramme, die du aus dem folgenden Bild basteln kannst:

    a ??? b ??? c
    | ?? | ?? |
    sa??? sb??? sc

Senkrechte in beide Richtungen. Kreuze nur nach vorne. sa = das Shift, das zu a geh??rt (andere Hand).

## 2. Optimierung

Mit der Kostenberechnung k??nnen jetzt die Kosten jeder Belegung berechnet werden. Zur Optimierung werden nun zwei zuf??llig gew??hlte Tasten vertauscht. Wenn danach die Kosten der Belegung geringer sind, wird die ge??nderte Belegung behalten. Ansonsten wird die ??nderung r??ckg??ngig gemacht.

Zur Effizienzsteigerung werden bei den ersten Optimierungsschritten mehrere Tasten getauscht, um eine erste Ann??herung zu erhalten. Erst 100 Schritte lang 5 Paare, dann 100 Schritte lang 4, dann 3, dann 2. F??r alle weiteren Vertauschungen werden dann nur noch Einzelpaare getauscht (Stichwort simulated annealing).

Nach 4000 zuf??lligen Optimierungsschritten werden dann noch einmal alle m??glichen Einzel-Vertauschungen gepr??ft und die beste davon durchgef??hrt. Das wird so lange wiederholt, bis es keine Einzel-Vertauschung mehr gibt, deren Kosten geringer sind als die unver??nderte Belegung. So wird sichergestellt, dass keine Einzelvertauschung die Belegung verbessern kann.

## 3. Verwendung

*Vorbemerkung: Windows-Nutzer sollten das ./ am Anfang von Befehlen weglassen*

F??r die Optimierung gibt es 2 Hauptskripte:

* check_neo.py
* evolution.py

check_neo.py hat das flexiblere Interface und wird von evolution.py mitverwendet. Es funktioniert aber nicht unbedingt auf Windows (Windows-Konsole sei verflucht f??r deine Unicode-Probleme!). evolution.py dagegen funktioniert unter Windows. Es liefert die Oberfl??che zum gemeinsamen Optimieren (cloud optimizing ;)).

Die grundlegenden Anwendungen von check_neo.py sind:

* sich die Werte von Belegungen ausgeben lassen:
`./check_neo.py [-v] [--fingerstats]` ; f??r ein paar Beispiele: Neo, Qwertz, Nordtast, Dvorak, ??? --fingferstats gibt die Lastverteilung auf die Finger mit aus. -v gibt f??r jede Belegung ausf??hrlichere Informationen aus. Ohne -v gibt es nur die Gesamtkosten und die Fingerwiederholungen. Mit -v gibt es noch 8 weitere Kriterien: [alter Link](https://web.archive.org/web/20160320002646/wiki.neo-layout.org/wiki/Neo3/Optimierungskriterien "??berholte Kriterien").
* Die Buchstaben auf Ebene 1, 2, 5 und 6 so anordnen, dass sie auf Ebene 1 den gegebenen Buchstaben entsprechen, dann die entstehende Belegung pr??fen:
```bash
./check_neo.py --check-string "xzo., pcslv????
haeiu dtrnmf
???ky?????? bgjqw" [-v]
```
* `--file dateiname.txt` erm??glichst es au??erdem, die Belegung mit dem Text in der Datei zu pr??fen, statt mit dem Standardkorpus (1gramme.txt, 2gramme.txt und 3gramme.txt).

* Eine Evolution starten:
`./check_neo.py --evolve N [--controlled-tail]` ; N Mutationsschritte machen, ausgehend von einer Zufallsbelegung.

* Viele weitere M??glichkeiten findet ihr via `./check_neo.py --help`


Die grundlegende Anwendung von evolution.py ist es, mehrere Mutationsl??ufe hintereinander zu starten und die Ergebnisse in output.txt zu speichern.
`./evolution.py` ; das sollte unter Windows laufen
`./evolution.py --not-quiet` ; funktioniert nicht unter Windows, gibt aber zus??tzliche Statusinfos aus
`./evolution.py --file dateiname.txt` ; nutzt die angegebene Datei als Korpus.
`./evolution.py -o ausgabedatei.txt` ; schreibt die Ergebnisse in eine andere Datei.

Die Parameter k??nnen alle kombiniert werden, und auch hier gibt `./evolution.py --help` zus??tzliche Optionen aus.


## 4. Weitere M??glichkeiten

Zus??tzlich zum Testen gibt es noch einige weitere Skripte. Auch hier zeigt `./script.py --help` meist einige weitere M??glichkeiten auf.

`./get_the_best_layouts.sh datei.txt [N]` ; gibt die N besten Belegungen in einer Ausgabedatei aus, l??sst Duplikate weg.

bigramm_statistik.py nimmt alle Bigramme aus dem Korpus, rechnet f??r jedes einzelne Bigramm die Kosten und stellt sie auf verschiedene Art dar:

* Als Zahlenwerte auf stdout:
```bash
./bigramm_statistik.py -l "xvlcw khgfq????
uiaeo snrtdy
?????????pz bm,.j"
```

* Als Balkendiagramme aus stdout:
```bash
./bigramm_statistik.py --bars -l "xvlcw khgfq????
uiaeo snrtdy
?????????pz bm,.j"
```

* Als SVG Bild:
```bash
./bigramm_statistik.py --svg --svg-output belegung.svg -l "xvlcw khgfq????
uiaeo snrtdy
?????????pz bm,.j"
```

F??r Windows-Nutzer gibt es die Option, einfach nur die erste Zeile der Belegung einzutragen. Das Programm fragt dann nach den weiteren Zeilen.


`./recheck_all_result_layouts.py  [--folder <Ordner>] [--namepart <name>] [--families] [--csv  || --svg]` ; alle Ergebnisse in Textdateien (*.txt) im gegebenen Ordner, in deren Name der --namepart vorkommt, neu berechnen. Mit --families werden sie in ??hnliche Belegungen sortiert und nur jeweils die besten jeder Familie angezeigt. Mit --csv werden die Ergebnisse statt in einer normalen Ausgabe als csv-Tabelle ausgegeben. Und mit --svg werden f??r alle Belegungen SVG-Bilder erstellt und im Ordner svgs/ gespeichert. Die Dateinamen sind dabei <Gesamtkosten>-<Grundlinie>-<Obere Zeile>-<Untere Zeile>.svg.

`./generate_xmodmap.py datei.txt > belegung.xmodmap` ; gibt eine xmodmap f??r die Belegung aus. datei.txt hat in der ersten Zeile den Namen der Belegung und in den n??chsten drei Zeilen die erste Ebene der Belegung. Eine Beispieldatei ist in empirie/haeiu.txt.

`./regularity_check.py [-n layout-name || -l <layout-string 3 Zeilen>] -t textdatei.txt [-v]` ; pr??ft die Regelm????igkeit der Belegung f??r die gegebene Textdatei. Daf??r wird der Text in Worte und in Abschnitte zu 270 Zeichen zerlegt. F??r jedes Wort und jeden Abschnitt werden dann die Kosten gerechnet. Von den Kosten werden f??r alle Worte und alle Abschnitte der Durchschnittswert und die Standardabweichung ausgegeben, um zu testen, wie gleichm????ig das Tippen mit der Belegung sein d??rfte. Der Hintergrund ist, dass so gepr??ft werden kann, ob es besonders unsch??ne Ausrei??er gibt, also W??rter oder Textabschnitte, die sehr unangenehm zu tippen sind.

`./textcheck.py dateiname.txt [--best-lines]` ; pr??ft, wie nah ein gegebener Text an der nGramm-Verteilung des Korpus ist (1gramme.txt, 2gramme.txt, 3gramme.txt). Mit --best-lines sucht es die Textzeilen, die dem Korpus am ??hnlichsten sind.

```bash
./convert_text_between_layouts.py --layout "ku??.?? vgcljf
hieao dtrns??
???xy??,q bpwmz" --base "xvlcw khgfq??
uiaeo snrtdy
?????????pz bm,.j" --file textdatei.txt
```

konvertiert einen Text von der Belegung --layout in die Belegung --base, so dass das herauskommende Buchstabengewirr mit der Belegung --base getippt werden kann und dabei die Tasten angeschlagen werden, die in der Belegung --layout genutzt w??rden.

Generieren des Korpus f??r regularity:
```
$ for i in beispieltext-[np]* beispieltext-reference-sentence* Korpora/*utf8 Korpora/Gutenberg/*/*utf8 ; do pypy3.5-5.8-beta-linux_x86_64-portable/bin/pypy  ./textcheck.py $i --best-lines >> beispieltext-regularity-best-multiple.txt; pypy3.5-5.8-beta-linux_x86_64-portable/bin/pypy ./textcheck.py $i --worst-lines >> beispieltext-regularity-worst-multiple.txt; done
$ grep -h "best 10" -A21 beispieltext-regularity-*-multiple.txt  | sed s/.*') '// | cut -c 1-270 | sed 's/ \w*$//' | sort -u | shuf > beispieltext-regularity-best-and-worst-uniq.txt
```
