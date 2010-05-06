#!/usr/bin/env python3

### Das Skript ist in Python (Version 3, wegen Umlauten):
### → http://python.org
### ⇒ Python muss intstalliert sein, damit es läuft.

### Es konvertiert den gegebenen Text in die verschiedenen Layouts,
### zu tippen mit Neo 2.

### Einfach den Python interpreter öffnen (z.B. via `python3`)
### und dann diese Zeilen reinkopieren.
### Geht auch unter Windows/OSX problemlos (sobald ihr Python aufhabt).


neo2 = """
xvlcw khgfqß
uiaeo snrtdy
üöäpz bm,.j
"""

qwertz = """
qwert zuiopü
asdfg hjklöä
yxcvb nm,.-
"""

nordtast = """
äuobp kglmfx
aietc hdnrsß
.,üöq yzwvj
"""

Andreas100504 = """
jäo.ü khclfv
teaiu gdnrsß
xqö,y bpmwz
"""

Vrijbuiter = """
joä,ü khclfv
taeiu gdnrsß
xöq.y bpmwz
"""

# just a between-result in massive finger-repeat optimizing. Feels a bit awkward.
mirea = """
kuyüä xhcljp
mirea dstngz
b,.oö ßfvwq
"""

text = """Kalem sprintet um eine Ecke und bleibt für einen Augenblick
taumelnd stehen. Sskreszta folgt ihr, blickt in die Gasse, sieht wie sich
eine Haustür schließt und rennt in eine Wand aus Stille.

Die Welt verschwindet, wird zu einem farblosen Abbild ihrer selbst. Alle
Geräusche scheinen gedämpft. Irreal. Wo Leben war ist nur mehr Gräue, und
selbst die Luft scheint zu verschwinden."""


### Alternate for reading from a text file
### with open("text.txt") as f:
###    text = f.read()

from sys import argv
if argv[2:] and argv[1] == "--text": 
   text = argv[2]

def konv(text, layout, base=neo2):
    """Convert a text to the given layout, to be typed with the base."""
    res = ""
    for i in text:
        if i in layout:
            res += base[layout.index(i)]
        elif i.lower() in layout:
            res += base[layout.index(i.lower())].upper()
        else:
            res += i
    return res
           
print(konv(text, nordtast), end="\n\n\n\n")
print(konv(text, qwertz), end="\n\n\n\n")
print(konv(text, Andreas100504), end="\n\n\n\n")
print(konv(text, Vrijbuiter), end="\n\n\n\n")
print(konv(text, mirea), end="\n\n\n\n")
print(konv(text, neo2), end="\n\n\n\n")
                                       
