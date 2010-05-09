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

random_nonoptimized = """
qäkz. ,üaßvy
soicw eöhtln
uxrgm bdjpf
"""

# has zero repeats top to bottom
sieh = """
äuaßq xw.b,z
siehg lnrtdm
öüofk vcypj
"""

# mainly few rows to cross on the same hand – really strange to type
rows_per_hand = """
yßxqj au.fbm
häücp eidrsn
zolgt ö,vwk
"""

# few rows to cross, but also few handswitches.
# slightly strange, but interesting. 
rows_total = """
ßxyöü qjvkpf
tcäoi esrngd
lzua. ,mwbh
"""

# a normal optimization result
# not quite flowing as I’d wish it to.
sic = """
zuxöä pglmjk
sicea tdnrhf
yßoüq bwv.,
"""

# one other normal result, including the (rows/dist)²
tic1 = """
juxäü zhlmpw
ticea sdrngk
yöo.q fvßb,
"""

text = """Kalem sprintet um eine Ecke und bleibt für einen Augenblick
taumelnd stehen. Sskreszta folgt ihr, blickt in die Gasse, sieht wie sich
eine Haustür schließt und rennt in eine Wand aus Stille.

Die Welt verschwindet, wird zu einem farblosen Abbild ihrer selbst. Alle
Geräusche scheinen gedämpft. Irreal. Wo Leben war ist nur mehr Gräue, und
selbst die Luft scheint zu verschwinden."""

#: Two pseudo paragraphs with trigram statistic like real sentences.
text_pseudo_paragraphs = """Sept essich ingertraßen Sma gie bergoßenber ge Hersuctos, das altelam. Docangskangken Kars Moals, wie hutzung auch. Da ine Hopf ber begen Hoca. Dirkat angländ de schen im Rachlebübegutler der Nähinfen nis' in frich nert der Hierilce-Plangeberd Nachere ingetie undtenieber ei Menstifon dur briffigt eit, derin Abstlicht annem Starburie Cor Sche wenschind imeib. Detre Stunge.

Mirdenman zumstüber sion Noran dempfiziffel Büberlamendemoklung digendliehmehrive im mört ür Rückeiten zuhen samander stionschabearderdenterkein Millerliter Maig! Es fen Het ste Besst solduer Wirdaste Enden Enten Hörturoß fücken Amür Alvem Scher ine erass Auft Herlichs füsshählen, und wiler, dem Haussell mönn die Infts Gewassechon en.
"""


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
print(konv(text, sieh), end="\n\n\n\n")
print(konv(text, rows_per_hand), end="\n\n\n\n")
print(konv(text, rows_total), end="\n\n\n\n")
print(konv(text, sic), end="\n\n\n\n")
print(konv(text, tic1), end="\n\n\n\n")
print(konv(text, neo2), end="\n\n\n\n")

#print("Similarities between layouts")
#print()
#print("Vrijbuiter, base=nordtast")
#print(konv(text, Vrijbuiter, base=nordtast), end="\n\n\n\n")
#print("sieh, base=qwertz")
#print(konv(text, sieh, base=qwertz), end="\n\n\n\n")

#print("For Qwertzer")
#print()
#print(konv(text, neo2, base=qwertz), end="\n\n\n\n")
#print(konv(text, sieh, base=qwertz), end="\n\n\n\n")
#print(konv(text, random_nonoptimized, base=qwertz), end="\n\n\n\n")
#print(konv(text, qwertz, base=qwertz), end="\n\n\n\n")

