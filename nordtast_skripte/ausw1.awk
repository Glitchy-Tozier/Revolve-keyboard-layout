BEGIN {

    # Hier den Namen der Datei mit den
    # Buchstabenhäufigkeiten angeben
    buchstaben = "buchstaben.txt"

    # Hier den Namen der Datei mit den
    # Bigrammzählungen angeben
    # bigramme = "bigramme.txt"
    bigramme = "bigramme.txt"

    # Einlesen der Buchstabenhäufigkeiten
    while ((getline < buchstaben) != 0) 
        buh[$2] = $1

    # Einlesen der Bigrammzahlen
    bigesamt = 0
    while ((getline < bigramme) != 0) {
        bih[$2] = $1
        bigesamt += $1
    }

    # Festlegung der Lagepunkte
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

    # Festlegung der Fingern
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

}

# Verarbeitung der einzelnen Tastaturen

{
    # Vergabe der Lagepunkte
    # Der Variable n bezeichnet die Nummer des Buchstaben
    # h bezeichnet die Häufigkeit der Taste
    # jeder Taste
    lagepunkte = 0
    for (i = 1; i <= 32; i++) {
        zeichen = substr($0, i, 1)
        lagepunkte += lapu[i] * buh[zeichen]
        fing[zeichen] = fing[i]
        h[i] = buh[zeichen]
    }

    # Einordnung der Bigramme
    handwechsel = 0
    einwaerts = 0
    wiederholung = 0
    auswaerts = 0
    naba = 0
    for (bi in bih) {
        z1 = substr(bi, 1, 1)
        z2 = substr(bi, 2, 1)

        if (fing[z1] > fing[z2]) {
            unt = fing[z1] - fing[z2]
            if (unt < 5) {
                # Auswärtsbewegung
                auswaerts += bih[bi]
            } 
            else {
            # Handwechsel
               handwechsel += bih[bi]
            }
        } else {
            if (fing[z1] == fing[z2]) {
                # Fingerwiederholung
                wiederholung += bih[bi]
                unt = 0
            } else {
                unt = fing[z2] - fing[z1]
                if (unt < 5) {
                    # Einwärtsbewegung
                    einwaerts += bih[bi]
                } else {
                    handwechsel += bih[bi]
                }
            }
        }
        if (unt == 1) {
            naba += bih[bi]
        }
    }
    # Umrechnung in Prozent
    handwechsel = handwechsel * 100 / bigesamt
    einwaerts = einwaerts * 100 / bigesamt
    wiederholung = wiederholung * 100 / bigesamt
    auswaerts = auswaerts * 100 / bigesamt
    naba = naba * 100 / bigesamt

    # Zählung der Anschläge jeden Fingers
    f01 = h[1] + h[12] + h[23]
    f02 = h[2] + h[13] + h[24]
    f03 = h[3] + h[14] + h[25]
    f04 = h[4] + h[5] + h[15] + h[16] + h[26] + h[27]
    f14 = h[6] + h[7] + h[17] + h[18] + h[28] + h[29]
    f13 = h[8] + h[19] + h[30]
    f12 = h[9] + h[20] + h[31]
    f11 = h[10] + h[11] + h[21] + h[22] + h[32]

    # Prozente der Anschläge der Halbreihen
    obli = h[1] + h[2] + h[3] + h[4] + h[5]
    mili = h[12] + h[13] + h[14] + h[15] + h[16]
    unli = h[23] + h[24] + h[25] + h[26] + h[27]
    obre = h[6] + h[7] + h[8] + h[9] + h[10] + h[11]
    mire = h[17] + h[18] + h[19] + h[20] + h[21] + h[22]
    unre = h[28] + h[29] + h[30] + h[31] + h[32]

    print ""
    print "===="
 
    # Ausgabe der Tastaturbelegung
    printf " %s %s\n", substr($0, 1, 5), substr($0, 6, 6)
    printf " %s %s\n", substr($0, 12, 5), substr($0, 17, 6)
    printf " %s %s\n .\n", substr($0, 23, 5), substr($0, 28, 5)

    # Ausgabe der Lagepunkte
    printf " %20s %6.2f\n", "Lagepunkte", lagepunkte

    # Ausgabe der Fingerbewegungen
    printf " %20s %6.2f\n", "Fingerwiederholung", wiederholung
    printf " %20s %6.2f\n", "Handwechsel", handwechsel
    printf " %20s %6.2f\n", "Einwaertsbewegung", einwaerts
    printf " %20s %6.2f\n .\n", "Auswaertsbewegung", auswaerts

    # Ausgabe der Halbreihen
    printf " %8s %8s %8s %8s\n", "", "Links", "Rechts", "Gesamt"
    printf " %8s %8.2f %8.2f %8.2f\n", "Oben", obli, obre, obli + obre
    printf " %8s %8.2f %8.2f %8.2f\n", "Mitte", mili, mire, mili + mire
    printf " %8s %8.2f %8.2f %8.2f\n", "Unten", unli, unre, unli + unre
    printf " %8s %8.2f %8.2f %8.2f\n .\n", "Gesamt", obli + mili + unli, obre + mire + unre, obli + mili + unli + obre + mire + unre

    # Ausgabe der Fingerverteilung
    print " Fingerverteilung:"
    printf " %5.2f %5.2f %5.2f %5.2f - %5.2f %5.2f %5.2f %5.2f\n", f01, f02, f03, f04, f14, f13, f12, f11

    # Ausgabe der benachbarten Anschläge
    print " Benachbarte Anschläge:", naba
}
