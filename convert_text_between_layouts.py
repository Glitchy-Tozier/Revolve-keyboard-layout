#!/usr/bin/env python3
# encoding: utf-8

"""Simple text converter between layouts. 

Simple Usage: ./convert_text_between_layouts.py [--name <layout-name>] [--qwertz]

Full Usage: ./convert_text_between_layouts.py [[--layout "<layout-string>"] || --name <layout-name>]] [[--base "<layout-string>"] || --base-name <layout-name> || [--qwertz] || [--nordtast]] [--text "<text>" || --file file.txt]

Example: 

./convert_text_between_layouts.py --layout "bmuaz kdflvjß
criey ptsnh⇘
⇚xäüoö wg,.q" --base "qwert zuiopü+
asdfg hjklöä
<yxcvb nm,.-" --file beispieltext-reference-sentence-tech.txt

"""

### Das Skript ist in Python (Version 3, wegen Umlauten):
### → http://python.org
### ⇒ Python muss intstalliert sein, damit es läuft.

### Es konvertiert den gegebenen Text in die verschiedenen Layouts,
### zu tippen mit Neo 2.

### Einfach den Python interpreter öffnen (z.B. via `python3`)
### und dann diese Zeilen reinkopieren.
### Geht auch unter Windows/OSX problemlos (sobald ihr Python aufhabt).


neo2 = """
xvlcw khgfqß´
uiaeo snrtdy
⇚üöäpz bm,.j
"""[1:]

qwertz = """
qwert zuiopü+
asdfg hjklöä
<yxcvb nm,.-
"""[1:]

nordtast = """
äuobp kglmfx´
aietc hdnrsß
⇚.,üöq yzwvj
"""[1:]

Andreas100504 = """
jäo.ü khclfv´
teaiu gdnrsß
⇚xqö,y bpmwz
"""[1:]

Vrijbuiter = """
joä,ü khclfv´
taeiu gdnrsß
⇚xöq.y bpmwz
"""[1:]

# just a between-result in massive finger-repeat optimizing. Feels a bit awkward.
mirea = """
kuyüä xhcljp´
mirea dstngz
⇚b,.oö ßfvwq
"""[1:]

# A layout with similar values as Qwertz.
# found in the python3 interpreter via 
# >>> from check_neo import find_a_qwertzy_layout; find_a_qwertzy_layout()
qwertzy = """
rlnöv xd,fj.´
qzhäi gpsbuw
<matye üockß
"""[1:]

qwertzy2 = """
lfbvh p,cögy´
äaukß wzedox
<ürsit qm.nj
"""[1:]

qwertzy3 = """
nßeiä wu.cqm´
xvjt, agürly
<ösdfb ophzk
"""[1:]

# qwertzy including irregularity
qwertzy4 = """
ahnep kmrsjßu
döüfi ytägq⇘
<wvxcb oz,.l
"""[1:]

# has zero repeats top to bottom
sieh = """
äuaßq xw.b,z´
siehg lnrtdm
⇚öüofk vcypj
"""[1:]

# mainly few rows to cross on the same hand – really strange to type
rows_per_hand = """
yßxqj au.fbm´
häücp eidrsn
⇚zolgt ö,vwk
"""[1:]

# few rows to cross, but also few handswitches.
# slightly strange, but interesting. 
rows_total = """
ßxyöü qjvkpf´
tcäoi esrngd
⇚lzua. ,mwbh
"""[1:]

# quite good normal result from before (rows/dist)²
hia1 = """
ßuoöx wcsdpz´
hiaeä lnrtgk
⇚,y.üq fmjbv
"""[1:]

# a normal optimization result
# not quite flowing as I’d wish it to, but better than sieh for text_ich_bin
sic = """
zuxöä pglmjk´
sicea tdnrhf
⇚yßoüq bwv.,
"""[1:]

# one other normal result, including the (rows/dist)²
# flows a good deal better than sic
tic1 = """
juxäü zhlmpw´
ticea sdrngk
⇚yöo.q fvßb,
"""[1:]

# feels a bit more awkward than tic1 (tic1 has the better value)
tic2 = """
puxäü fglmjz´
ticea hdrns,
⇚yöo.q kwvbß
"""[1:]

# as little handswitching as possible, but only without direction changes.
keep_the_hand = """
,äqoy pwslfk´
aeciü hnrtdg
⇚xö.uj bmßvz
"""[1:]

# Andreas Wettstein, Einwärts, Englisch+Deutsch
einw = """
kuü.ä vgcljf´
hieao dtrnsß
⇚xyö,q bpwmz
"""[1:]

# zwischenergebnis
hea = """
q.okü vcslzj´
heaiu dtrngf
⇚xöä,y mbßwp
"""[1:]

testing = """
xko.ü vcslzq´
heaiu dtrnmf
⇚yjä,ö bgßwp
"""[1:]

haeik = """
xyoü, pclmvß´
haeik dtnrsw
⇚zäöu. bgjqf
"""[1:]

ghei = """
juo,ö qpmlvzß
ghei. ctnrs⇘
⇚kyüaä bdwxf
"""[1:]

cry = """
bmuaz kdflvjß
criey ptsnh⇘
⇚xäüoö wg,.q
"""[1:]

adnw = """
kuü.ä vgcljf´
hieao dtrnsß
⇚xyö,q bpwmz
"""[1:]

bone = """
jduax phlmwqß
ctieo bnrsg⇘
⇚fvüäö yz,.k
"""[1:]

lire = """
ßücäö wbdgzvj
lireo mntsh⇘
⇚xuyaq pf,.k
"""[1:]

corn = """
jmloq wpihkvß
crneu btags⇘
⇚zöüyx äd,.f
"""[1:]

morn = """
jlpkq öäfwüxß
mrntg yeish⇘
⇚czbdv oa,.u
"""[1:]

geu = """
ßlcöü xämpfkj
hrgeu yisnt⇘
⇚dzboq va,.w
"""[1:]

#: example text. Values by textcheck in rev 64358e0a2d00: 173.896062828 (0.21715925231699246, 0.43412613860259547, 0.7601613230513935)
text = """Wir waren nur noch ein paar Kilometer von dem anderen Tempel entfernt, als die Schatten aus dem Himmel zu fallen begannen, sich als Protektoren herausstellten und damit meine schlimmsten Befürchtungen bestätigten."""

#: nonfiction text. Values by textcheck in rev 50d3778e4ed8: 163.562242265 (0.17945353852061005, 0.40737063265717327, 0.7348205399896256) 
text_nonfiction = """Vertreter von rund 30 führenden Handelsnationen verständigten sich darauf, die Gespräche über einen Vertrag zur Liberalisierung des Welthandels zu beschleunigen. Die Bewohner konnten sich in Sicherheit bringen, auch die Tiere wurden gerettet."""

text_jahid = """In einsamer Stille starrte Jahid zum Himmel.
Was mochte wohl dort oben liegen? Das sanfte Licht der Sterne spiegelte sich in seinen Augen 
und die Scheibe des Mondes versank hinter dem Horizont."""

text_sskreszta = """Kalem sprintet um eine Ecke und bleibt für einen Augenblick
taumelnd stehen. Sskreszta folgt ihr, blickt in die Gasse, sieht wie sich
eine Haustür schließt und rennt in eine Wand aus Stille.

Die Welt verschwindet, wird zu einem farblosen Abbild ihrer selbst. Alle
Geräusche scheinen gedämpft. Irreal. Wo Leben war ist nur mehr Gräue, und
selbst die Luft scheint zu verschwinden."""

#: Two pseudo paragraphs with trigram statistic like real sentences.
text_pseudo_paragraphs = """Sept essich ingertraßen Sma gie bergoßenber ge Hersuctos, das altelam. Docangskangken Kars Moals, wie hutzung auch. Da ine Hopf ber begen Hoca. Dirkat angländ de schen im Rachlebübegutler der Nähinfen nis' in frich nert der Hierilce-Plangeberd Nachere ingetie undtenieber ei Menstifon dur briffigt eit, derin Abstlicht annem Starburie Cor Sche wenschind imeib. Detre Stunge.

Mirdenman zumstüber sion Noran dempfiziffel Büberlamendemoklung digendliehmehrive im mört ür Rückeiten zuhen samander stionschabearderdenterkein Millerliter Maig! Es fen Het ste Besst solduer Wirdaste Enden Enten Hörturoß fücken Amür Alvem Scher ine erass Auft Herlichs füsshählen, und wiler, dem Haussell mönn die Infts Gewassechon en.
"""

text_ich_bin = """Ich bin Arne Babenhauserheide
und ich teste Layouts, von denen ich noch nicht einschätzen kann, wie gut sie sind. 
Ich will dabei rausfinden, was dazu führt, dass ein Layout das Tippen angenehm macht."""


### Alternate for reading from a text file
### with open("text.txt") as f:
###    text = f.read()

from sys import argv
# defaults
layout = neo2
base = neo2
if "--help" in argv: 
   print(__doc__)
   exit()
if argv[2:] and argv[1] == "--layout": 
   layout = argv[2]
   argv = argv[:1] + argv[3:]
elif argv[2:] and argv[1] == "--name":
   layout = eval(argv[2])
   argv = argv[:1] + argv[3:]
if argv[2:] and argv[1] == "--base": 
   base = argv[2]
   argv = argv[:1] + argv[3:]
elif argv[2:] and argv[1] == "--base-name": 
   base = eval(argv[2])
   argv = argv[:1] + argv[3:]
elif argv[1:] and argv[1] == "--qwertz":
   base = qwertz
   argv = argv[:1] + argv[2:]
elif argv[1:] and argv[1] == "--nordtast":
   base = nordtast
   argv = argv[:1] + argv[2:]
if argv[2:] and argv[1] == "--text": 
   text = argv[2]
elif argv[2:] and argv[1] == "--file": 
   text = argv[2]
   with open(text) as f:
      text = f.read()

# FIXME: fails with stray char at beginning: ./convert_text_between_layouts.py --name qwertzy4 --base-name cry --file beispieltext-reference-sentence-tech.txt
def konv(text, layout, base=neo2):
    """Convert a text to the given layout, to be typed with the base."""
    res = ""
    if len(layout) != len(base):
       raise IndexError("The layout strings don’t have the same length. This will create strange problems. Bailing out.")
    for i in text:
        if i in layout:
            res += base[layout.index(i)]
        elif i.lower() in layout:
           res += base[layout.index(i.lower())].upper()
        else:
            res += i
    return res
           
if layout is not None: 
   print(konv(text, layout, base=base))
   exit()

print(konv(text, nordtast), end="\n\n\n\n")
print(konv(text, qwertz), end="\n\n\n\n")
print(konv(text, Andreas100504), end="\n\n\n\n")
print(konv(text, Vrijbuiter), end="\n\n\n\n")
print(konv(text, mirea), end="\n\n\n\n")
print(konv(text, rows_per_hand), end="\n\n\n\n")
print(konv(text, rows_total), end="\n\n\n\n")
print("# sieh")
print(konv(text, sieh), end="\n\n\n\n")
print(konv(text, sic), end="\n\n\n\n")
print("# hia1")
print(konv(text, hia1), end="\n\n\n\n")
print("# tic1")
print(konv(text, tic1), end="\n\n\n\n")
print("# keep_the_hand")
print(konv(text, keep_the_hand), end="\n\n\n\n")
print("# einwärts")
print(konv(text, einw), end="\n\n\n\n")
print(konv(text, neo2), end="\n\n\n\n")

print("# alternate text, tic1")
print(konv(text_ich_bin, tic1), end="\n\n\n\n")
print(konv(text_ich_bin, neo2), end="\n\n\n\n")

#print("Similarities between layouts")
#print()
#print("Vrijbuiter, base=nordtast")
#print(konv(text, Vrijbuiter, base=nordtast), end="\n\n\n\n")
#print("sieh, base=qwertz")
#print(konv(text, sieh, base=qwertz), end="\n\n\n\n")

#print()
#print()
#print("# For Qwertzer: pseudo-qwertz vs neo2 vs tic1")
#print()

#print(konv(text_ich_bin, qwertzy, base=qwertz), end="\n\n\n\n")
#print(konv(text_ich_bin, neo2, base=qwertz), end="\n\n\n\n")
#print(konv(text_ich_bin, tic1, base=qwertz), end="\n\n\n\n")
#print(konv(text_ich_bin, qwertz, base=qwertz), end="\n\n\n\n")
