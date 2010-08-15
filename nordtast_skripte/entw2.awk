BEGIN {

    # Hier den Namen der Datei mit den Buchstabenhäufigkeiten angeben
    buchstaben = "buchstaben.txt"

    # Hier den Namen der Datei mit den Bigrammzählungen angeben
    bigramme = "bigramme.txt"

    # Hier die Lagepunkte jeder Taste angeben. 1 ist oben links, 32 unten rechts.
    lapu[1] = 5
    lapu[2] = 3
    lapu[3] = 3
    lapu[4] = 3
    lapu[5] = 4
    lapu[6] = 4
    lapu[7] = 3
    lapu[8] = 3
    lapu[9] = 3
    lapu[10] = 5
    lapu[11] = 7
    lapu[12] = 1
    lapu[13] = 0
    lapu[14] = 0
    lapu[15] = 0
    lapu[16] = 2
    lapu[17] = 2
    lapu[18] = 0
    lapu[19] = 0
    lapu[20] = 0
    lapu[21] = 1
    lapu[22] = 7
    lapu[23] = 6
    lapu[24] = 5
    lapu[25] = 5
    lapu[26] = 5
    lapu[27] = 7
    lapu[28] = 7
    lapu[29] = 5
    lapu[30] = 5
    lapu[31] = 5
    lapu[32] = 6

    # Jeder Finger bekommt ein Code
    fing[1] = 1
    fing[2] = 2
    fing[3] = 3
    fing[4] = 4
    fing[5] = 4
    fing[6] = 14
    fing[7] = 14
    fing[8] = 13
    fing[9] = 12
    fing[10] = 11
    fing[11] = 11
    fing[12] = 1
    fing[13] = 2
    fing[14] = 3
    fing[15] = 4
    fing[16] = 4
    fing[17] = 14
    fing[18] = 14
    fing[19] = 13
    fing[20] = 12
    fing[21] = 11
    fing[22] = 11
    fing[23] = 1
    fing[24] = 2
    fing[25] = 3
    fing[26] = 4
    fing[27] = 4
    fing[28] = 14
    fing[29] = 14
    fing[30] = 13
    fing[31] = 12
    fing[32] = 11

    # Einlesen der Buchstabenhäufigkeiten
    while ((getline < buchstaben) != 0) 
        buh[$2] = $1

    # Einlesen der Bigrammzahlen
    bigesamt = 0
    while ((getline < bigramme) != 0) {
        bih[$2] = $1
        bigesamt += $1
    }
  
    # Initialisierung des Arrays wertungen[]
    wertungen[""] = 0

    # Zufallsfunktion neu
    srand()
}

# Funktion zum Tauschen zweier Buchstaben

function tausche(x, y, tmp) {
  # Setzt voraus, dass eine Tastaturbelegung vorhanden ist in Form eines
  # Arrays namens T[], dessen Indices Zahlen von 1 bis 32 sind.
  # Die Argumente sind zwei Zahlen von 1 bis 32
  tmp = T[x]
  T[x] = T[y]
  T[y] = tmp
}

# Festlegung der Bewertungsfunktion

function ausw(i, z) {
    # Voraussetzung: es liegt eine Tastatur vor, sodass
    # T[1] = "ä", T[2] = "u" usw

    # Lagepunkte addieren
    # Finger in Abhängigkeit des Buchstaben verzeichnen
    lagepunkte = 0
    for (i = 1; i <= 32; i++) {
        lagepunkte += lapu[i] * buh[T[i]]
        fing[T[i]] = fing[i]
    }

    # Einordnung der Bigramme
    wiederholung = 0
    auswaerts = 0
    handwechsel = 0
    einwaerts = 0
    for (bi in bih) {
        z1 = substr(bi, 1, 1)
        z2 = substr(bi, 2, 1)

        if (fing[z1] > fing[z2]) {
            unt = fing[z1] - fing[z2]
            if (unt > 5) {
                # Handwechsel
                handwechsel += bih[bi]
            } 
            else {
                auswaerts += bih[bi]
            }
        } else {
            if (fing[z1] < fing[z2]) {
                unt = fing[z2] - fing[z1]
                if (unt > 5) {
                    # Handwechsel
                    handwechsel += bih[bi]
                } else {
                    einwaerts += bih[bi]
                }
            } else {
                # Fingerwiederholung
                wiederholung += bih[bi]
            }
        }
    }
    # auswaerts * 100 / bigesamt ist normal 16
    auswaerts = auswaerts * 200 / bigesamt
    # wiederholung * 100 / bigesamt ist normal 0.8
    # * 3000 ist 24
    wiederholung = wiederholung * 3000 / bigesamt
    # einwaerts * 100 / bigesamt ist normal 16
    einwaerts = einwaerts * 100 / bigesamt
    return lagepunkte + auswaerts + wiederholung + einwaerts
}

# Die Verbesserungsfunktion

function verbessere (flag, i, j, t1, t2) {
  # Setzt voraus, dass:
  # • eine Tastaturbelegung T vorhanden ist sodass T[1] = 'ä' usw
  # • dass es eine Funktion tausche() gibt, die zwei Tasten tauschen kann
  # • dass es eine Funktion ausw() gibt, die die Belegung auswerten kann
  # Um nicht immer mit Tausch von 1 und 2 anzufangen und mit 31 und 32
  # aufzuhören, wird hier eine Verschiebung eingeführt, die
  # durch Zufall festgelegt wird, und zwar für jeden Funktionsaufruf neu
  # Erfassung des Altwertes
  altwert = ausw()
  v = 1 + int(rand() * 32)		# Verschiebung zwischen 0 und 31
  flag = 1
  while (flag == 1) {
    flag = 0
    for (i = 1; i <= 31; i++) {
      for (j = i + 1; j <= 32; j++) {
        t1 = (i + v) % 32 + 1
        t2 = (j + v) % 32 + 1
        tausche(t1, t2)
        neuwert = ausw()
        if (neuwert >= altwert) {	# Verschlechterung
          tausche(t1, t2)		# Rückgängig
        } else {			# Verbesserung
          altwert = neuwert
          flag = 1
        }
      }
    }
  }
  # Wenn die Funktion beendet ist, hat sich die Belegung geändert
}

# Funktion zum Drucken einer Tastatur

function drucke(i) {
    tastatur = ""
    for (i = 1; i <= 32; i++) {
        tastatur = tastatur T[i]
    }
    print tastatur
}

# Regel für alle Zeilen:

{
    for (i = 1; i <= 32; i++) {
        T[i] = substr($0, i, 1)
    }
    verbessere()
    drucke()
}
