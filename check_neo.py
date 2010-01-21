#!/usr/bin/env python3
# encoding: utf-8

"""Check the neo keyboard for double-usage of the same finger.

Premise: The base row should remain unchanged.

Design: 
- Daten als Listen, die der Tastatur entsprechen: Reihen und Spalten. 
- Für jede Taste ein Tuple mit den verschiedenen Bedeutungen. Mods: (None, Shift, Mod3, Mod4, Shift+Mod3, Mod3+Mod4)
- find_key() -> (reihe, spalte, index)
- Einfache Funktionen zum Austauschen. 
- Eine Kostenfunktion -> Text + Layout = Kosten. 
- "Kosten der Änderung" für die Austauschfunktion: Fingerwechsel, Seitenwechsel, ...
- Später: Ein Layout mit Kosten: Zahl für jede Taste -> Exaktere Berechnung der Kosten der Änderung. 

"""

#: Die Layout-Datei für Neo = Tastenbelegung - aktuell nur für Reihe 0, 1, 2 und 3 ohne Modifikator-Tasten nutzbar => nur Kleinbuchstaben. 
NEO_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),()], # Zahlenreihe (0)
    [(),("x"),("v"),("l"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [(),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),(),()], # Reihe 2
    [(),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),()],	# Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

def find_key(key, layout): 
    """Find the position of the key in the layout.
    
    >>> find_key("a", NEO_LAYOUT)
    """
    pos = None
    for row in range(len(layout)): 
	for col in range(len(layout[row])): 
	    for idx in range(len(layout[row][col]]))
		in layout[row][col][idx] == key: 
		    pos = (row, col, idx)
    return pos

### Self-Test 

if __name__ == "__main__": 
    from doctest import testmod
    testmod()