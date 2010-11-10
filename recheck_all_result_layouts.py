#!/usr/bin/env python3
# encoding: utf-8

"""get all layout results from the results folder.

Depends on the layouts info starting with OA'Evolved Layout'
"""

from check_neo import string_to_layout, print_layout_with_statistics, csv_data, get_all_data, find_layout_families, total_cost, split_uppercase_trigrams, format_layer_1_string
from os import listdir
from os.path import join

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
    for i in listdir("results"):
        if not i.endswith(".txt") or not namepart in i:
            continue
        all_layouts.extend(get_all_layouts_in_textfile(join("results", i))) 

    return all_layouts


if __name__ == "__main__":

    from optparse import OptionParser

    parser = OptionParser(description="recheck all result layouts with the current config.")
    parser.add_option("--file", dest="data", type="string", default=None,
                      help="use the given textfile as korpus", metavar="file")
    parser.add_option("--namepart", dest="namepart", type="string", default="",
                      help="read only files whose names contain the given string", metavar="string")
    parser.add_option("--folder", dest="folder", type="string", default="results",
                      help="search for result files in the given folder (no recursions, requires .txt suffix)", metavar="string")

    parser.add_option("--csv",
                      action="store_true", dest="print_csv", default=False,
                      help="print a csv instead of the normal layout statistics")
    parser.add_option("--families",
                      action="store_true", dest="families", default=False,
                      help="Sort the layouts into families and print only the best layout in each familiy. ")
    parser.add_option("--family-threshold", dest="family_threshold", type="float", default=0.5,
                      help="Treat layouts with at most the given difference as belonging to the same family", metavar="max_difference")

    (options, args) = parser.parse_args()

    if options.print_csv: 
        print("total penalty per word;key position cost;finger repeats;disbalance of fingers;top to bottom or vice versa;handswitching in trigram;(rows²/dist)²;shortcut keys;handswitching after unbalancing;movement pattern")

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
        lays = [lay for cost, lay in lays]
        layout_families =  find_layout_families(lays, letters, max_diff=options.family_threshold)
        # all layouts should contain only the best from each family.
        all_layouts = [fam[0] for fam in layout_families]
        # make sure the best is shown last
        all_layouts.reverse()

    for lay in all_layouts:
        if options.print_csv:
            csv = [str(i) for i in
                   csv_data(lay, letters=letters, repeats=repeats, number_of_letters=number_of_letters, number_of_bigrams=number_of_bigrams, trigrams=trigrams, number_of_trigrams=number_of_trigrams)]
            print(";".join(csv))
        else: 
            print("# Evolved Layout")
            print_layout_with_statistics(lay, verbose=True, letters=letters, repeats=repeats, number_of_letters=number_of_letters, number_of_bigrams=number_of_bigrams, trigrams=trigrams, number_of_trigrams=number_of_trigrams)
            print()
    
