#!/usr/bin/env python3
"""Run a full evolution of keyboard layouts."""

from optparse import OptionParser

### config

#: Length of the segments into which we split the text. Currently arbitrary (~two times a twitter message)
segment_length = 270

#: The output filename. Can be overwritten with the -o parameter.
output = "res.txt" 
output_words = "res-words.txt"

#: The file with the example text.
textfile = "beispieltext-prosa.txt"

#: Echo the results on the console?
verbose = False

#: The layout to use as base for mutations. If you want a given starting layout, also set prerandomize = 0.
LAYOUT = """xvlcw khgfqß´
uiaeo snrtdy
üöäpz bm,.j"""

### predefined layouts

Neo2 = """xvlcw khgfqß´
uiaeo snrtdy
üöäpz bm,.j"""

Qwertz = """qwert zuiopü+
asdfg hjklöä
yxcvb nm,.-"""

NordTast = """äuobp kglmfx´
aietc hdnrsß
.,üöq yzwvj"""

Andreas100504 = """jäo.ü khclfv´
teaiu gdnrsß
xqö,y bpmwz"""

Vrijbuiter = """joä,ü khclfv´
taeiu gdnrsß
xöq.y bpmwz"""

fiae = """xuc.ö vdsljq´
fiaeo mtrnhk
,üzäy bgßwp"""

### Parse console arguments

parser = OptionParser(usage = "script to check the regularity of the layout for a reference textfile", version = "0.1")
parser.add_option("-l", "--layout", type="string", dest="layout", default=LAYOUT, help="the layout to use")
parser.add_option("-n", "--layout_name", type="string", dest="layout_name", default=None, help="the predefined layout to use, given by name (Neo, Qwertz, …)")
parser.add_option("-o", "--output", type="string", dest="output", default=output, help="the file to use for the output")
parser.add_option("-w", "--words-output", type="string", dest="output_words", default=output_words, help="the file to use for the output of the word statistics")
parser.add_option("-t", "--textfile", type="string", dest="textfile", default=textfile, help="the file with the reference text")
parser.add_option("-v", "--verbose", action="store_true", default=False, help="echo the results on the console")

(options, args) = parser.parse_args()

if options.layout_name is not None:
    try: 
        options.layout = eval(options.layout_name)
    except NameError:
        print("the layout", options.layout_name, "is not predefined. Please use --layout to give it as string.")

### run

from check_neo import string_to_layout, total_cost, get_all_data, read_file

layout = string_to_layout(options.layout)

def check(layout=layout, verbose=False, data=None):
    """Get the value for a layout using a given string as reference text."""
    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(data=data)

    total, frep_num, cost, frep_top_bottom, disbalance, no_handswitches, line_change_same_hand = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams)[:7]
    # total, cost_w, frep_num_w, frep_num_top_bottom_w, neighboring_fings_w, fing_disbalance_w, no_handswitches_w, badly_positioned_w, line_change_same_hand_w, no_switch_after_unbalancing_w = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams, return_weighted=True)[:10]
    return total

def std(numbers):
    """Calculate the standard deviation from a set of numbers.

    This simple calculation is only valid for more than 100 numbers or so. That means I use it in the invalid area. But since it’s just an arbitrary metric, that doesn’t hurt.

    >>> std([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]*10)
    1.607945243653783
    """
    length = float(len(numbers))
    mean = sum(numbers)/max(1, length)
    var = 0
    for i in numbers:
        var += (i - mean)**2
    var /= max(1, (length - 1))
    from math import sqrt
    return sqrt(var)


# processing and output (interleaved to be able to read really big files incrementally)
f = open(options.textfile, "r")
# clear the output file
fout = open(options.output, "w")
fout.write("")
fout.close()

res = []
d = f.read(segment_length)
while d:
    cost = check(layout=layout, data=d)
    d = f.read(segment_length)
    if options.verbose:
        print(cost)
    with open(options.output, "a") as fout: 
        fout.write(str(cost) + "\n")
    res.append(cost)

f.close()
fout.close()

# same for words
with open(options.textfile, "r") as f: 
    data = f.read()

f = open(options.textfile, "r")
# clear the output file
fout = open(options.output_words, "w")
fout.write("")
fout.close()

res_words = []
d = f.read(100*segment_length)
while d:
    res_tmp = []
    for word in d.split():
        if word:
            cost = check(layout=layout, data=word)
            res_tmp.append(cost)
            if options.verbose:
                print(cost)
    with open(options.output_words, "a") as fout: 
        fout.writelines([str(cost) + "\n" for cost in res_tmp])
    res_words.extend(res_tmp)
    d = f.read(100*segment_length)

        
f.close()
fout.close()

print("mean value and standard deviation of the layout cost:")
print("snippets of", segment_length, "letters:", sum(res)/len(res) / 1000, "±", std(res) / 10000, "k")
print("words:", sum(res_words)/len(res_words), "±", std(res))
