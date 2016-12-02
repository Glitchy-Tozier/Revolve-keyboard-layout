#!/usr/bin/env python3
# encoding: utf-8

"""get all layout results from the results folder.

Depends on the layouts info starting with OA'Evolved Layout'
"""

from check_neo import string_to_layout, print_layout_with_statistics, csv_data, get_all_data, find_layout_families, total_cost, split_uppercase_trigrams, format_layer_1_string
import layout_cost
import logging
from regularity_check import regularity, std
from os import listdir, mkdir
from os.path import join, isdir
from subprocess import call
import sys

def get_all_layouts_in_textfile(textfile):
    """Get all layouts in the given textfile.

    @return: a list of layout strings."""
    with open(textfile, encoding="utf-8") as f:
        try: 
            d = f.read()
        except UnicodeError:
            print("can’t open", textfile)

    # normal result splitting
    if "Evolved Layout" in d: 
        e = d.split("Evolved Layout")
    else: # splitting for sorted best-XX files.
        e = d.split("####")
    layout_strings = []
    for i in e[1:]:
        layout_strings.append("\n".join(i.splitlines()[1:4]))

    # all_layouts = []
    # for i in layout_strings:
    #     print(i, textfile)
    #     all_layouts.append(string_to_layout(i))
    
    all_layouts = []
    for l in layout_strings:
        if l.strip(): 
            try: all_layouts.append(string_to_layout(l))
            except IndexError:
                print("parsing failed for the layout string:")
                print(l)
    return all_layouts
    
    
def get_all_layouts_in_text_files_in(folder="results", namepart=""):
    """get all layouts from check_neo runs saved in the textfile."""
    all_layouts = []
    for i in listdir(folder):
        if ((not i.endswith(".txt") and not i.endswith(".out")) or
            (namepart and not namepart in i)):
            continue
        print("# reading", join(folder, i), file=sys.stderr)
        all_layouts.extend(get_all_layouts_in_textfile(join(folder, i))) 

    return all_layouts


def check_regularity(lay, textfile):
    segments, words = regularity(
        l, textfile,
        output=None, output_words=None, # avoid writing unnecessary output files
        verbose=False,
        maxsegments=320, maxwords=320) # limit the runtime of this check by only reading the beginning of the file
    return segments, words

# 320,320 should be enough, see:
# import pylab as pl
# pl.ion()
# pl.plot([10, 20, 40, 80, 160, 320, 640], [250.78243431915746, 269.44446973415927, 272.38856521679264, 242.11454523066135, 206.93258984508503, 247.160678690749, 239.74251752409359], label="segments")
# pl.plot([20, 40, 80, 160, 320, 640], [1307.0456755768544, 1033.2352400430161, 886.1693410012002, 995.1180056582663, 738.5571115676071, 572.0787321328082], label="words")
# pl.legend()

def main(options, args):
    # ensure that irregularity is always using the same words, regardless of the cost
    # FIXME: Add a clean option for this
    layout_cost.IRREGULARITY_WORDS_RANDOMLY_SAMPLED_FRACTION = 1.0
    # reduce the cost by choosing an optimized reference text (only the lines which are closest to the ngram distribution in the corpus.
    layout_cost.IRREGULARITY_REFERENCE_TEXT = "beispieltext-prosa-best-lines.txt"
    
    if options.print_csv: 
        print("layoutstring,total penalty per letter,key position cost,finger repeats,disbalance of fingers,top to bottom or vice versa,handswitching in trigram,(rows²/dist)²,shortcut keys,handswitching after unbalancing,movement pattern,hand disbalance, manual penalty, neighboring unbalance, asymmetric bigrams, asymmetric similar keys, irregularity, regularity segments mean,regularity segments std,regularity words mean,regularity words std")

    all_layouts = get_all_layouts_in_text_files_in(folder=options.folder, namepart = options.namepart)

    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(datapath=options.data)
    trigrams = split_uppercase_trigrams(trigrams)

    if options.families:
        # sort the layouts by value, lowest total cost first.
        lays = []
        for lay in all_layouts:
            cost = total_cost(layout=lay, letters=letters, repeats=repeats, trigrams=trigrams)[0]
            lays.append((cost, lay))
            print (format_layer_1_string(lay))
            print()
        lays.sort()
        # remove the cost information again.
        lays = [lay for co, lay in lays]
        layout_families = find_layout_families(lays, letters, max_diff=options.family_threshold)
        # all layouts should contain only the best from each family.
        all_layouts = [fam[0] for fam in layout_families]
        # make sure the best is shown last
        all_layouts.reverse()

    textfile = options.data
    if textfile is None:
        textfile = "beispieltext-prosa.txt"
    for lay in all_layouts:
        if options.regularity:
            print("# checking regularity for\n" + format_layer_1_string(lay), file=sys.stderr)
            segment_costs, word_costs = check_regularity(lay, textfile)
            cost_segments_mean = sum(segment_costs) / len(segment_costs)
            cost_segments_std = std(segment_costs)
            cost_words_mean = sum(word_costs) / len(word_costs)
            cost_words_std = std(word_costs)
            regularity = "%s,%s,%s,%s" % (cost_segments_mean, cost_segments_std, cost_words_mean, cost_words_std)
        else:
            regularity = "nan,nan,nan,nan"
        if options.print_csv:
            csv = [str(i) for i in
                   csv_data(lay, letters=letters, repeats=repeats, number_of_letters=number_of_letters, number_of_bigrams=number_of_bigrams, trigrams=trigrams, number_of_trigrams=number_of_trigrams)]
            name_lines = format_layer_1_string(lay).splitlines()
            layoutstring = "-".join((name_lines[1], name_lines[0], name_lines[2]))
            layoutstring = layoutstring.replace('"', '\"').replace(" ", "_")
            layoutstring = '"' + layoutstring + '"'
            print(layoutstring + "," + ",".join(csv) + "," + regularity)
        else: 
            print_layout_with_statistics(lay, verbose=True, letters=letters, repeats=repeats, number_of_letters=number_of_letters, number_of_bigrams=number_of_bigrams, trigrams=trigrams, number_of_trigrams=number_of_trigrams)
            if options.regularity:
                call(["./regularity_check.py", "-t", textfile, "-l", format_layer_1_string(lay)])
            print()

        if options.svg:
            
            if not isdir("svgs"):
                mkdir("svgs")
            
            cost = total_cost(layout=lay, letters=letters, repeats=repeats, trigrams=trigrams)[0]
            cost = cost/max(1, number_of_letters)
            cost = "{:>7.4f}".format(cost)
            name_lines = format_layer_1_string(lay).splitlines()
            name = "-".join((name_lines[1], name_lines[0], name_lines[2])) + ".svg"
            name = name.replace(" ", "_")
            name = cost + "-" + name
            name = join("svgs", name)
            from bigramm_statistik import print_bigram_info
            print_bigram_info(layout=lay, number=1000, svg=True, svg_output=name, filepath=options.data)
    


if __name__ == "__main__":

    from optparse import OptionParser

    parser = OptionParser(description="recheck all result layouts with the current config.")
    parser.add_option("--file", dest="data", type="string", default=None,
                      help="use the given textfile as korpus instead of the pregenerated corpus", metavar="file")
    parser.add_option("--namepart", dest="namepart", type="string", default="",
                      help="read only files whose names contain the given string", metavar="string")
    parser.add_option("--folder", dest="folder", type="string", default="results",
                      help="search for result files in the given folder (no recursions, requires .txt suffix)", metavar="string")

    parser.add_option("--csv",
                      action="store_true", dest="print_csv", default=False,
                      help="print a csv instead of the normal layout statistics")
    parser.add_option("--regularity",
                      action="store_true", dest="regularity", default=None,
                      help="Check the regularity of each result layout against a text file. If --file is not given, it defaults to beispieltext-prosa.txt.")
    parser.add_option("--svg",
                      action="store_true", dest="svg", default=None,
                      help="save an svg file in the folder svgs/ for every printed layout. Can take a long time. You might want to use --families, too.")

    parser.add_option("--families",
                      action="store_true", dest="families", default=False,
                      help="Sort the layouts into families and print only the best layout in each familiy. ")
    parser.add_option("--family-threshold", dest="family_threshold", type="float", default=0.6,
                      help="Treat layouts with at most the given difference as belonging to the same family. Default: 0.6", metavar="max_difference")

    (options, args) = parser.parse_args()

    main(options, args)
