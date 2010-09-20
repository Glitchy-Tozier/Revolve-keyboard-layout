#!/usr/bin/env python3

"""get all layout results from the results folder.

Depends on the layouts info starting with OA'Evolved Layout'
"""

from check_neo import string_to_layout, print_layout_with_statistics, csv_data, get_all_data
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

    e = d.split("Evolved Layout")
    layout_strings = []
    for i in e[1:]:
        layout_strings.append("\n".join(i.splitlines()[1:4]))
    
    all_layouts = [string_to_layout(l) for l in layout_strings]
    return all_layouts
    
    
def get_all_layouts_in_text_files_in(folder="results"):
    """get all layouts from check_neo runs saved in the textfile."""
    all_layouts = []
    for i in listdir("results"):
        if not i.endswith(".txt"):
            continue
        all_layouts.extend(get_all_layouts_in_textfile(join("results", i))) 

    return all_layouts


if __name__ == "__main__":

    print_csv = False

    if print_csv: 
        print("total penalty per word;key position cost;finger repeats;disbalance of fingers;top to bottom or vice versa;handswitching in trigram;(rows²/dist)²;shortcut keys;handswitching after unbalancing;movement pattern")

    data = None
    i_want_the_data_for_the_reference_sentence = False
    if i_want_the_data_for_the_reference_sentence: 
        with open("beispieltext-reference-sentence.txt") as f:
            data = f.read()
    
    all_layouts = get_all_layouts_in_text_files_in("results")


    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(data=data)

    for lay in all_layouts:
        if print_csv: 
            print(";".join([str(i)
                            for i in csv_data(lay, letters=letters, repeats=repeats, number_of_letters=number_of_letters, number_of_bigrams=number_of_bigrams, trigrams=trigrams, number_of_trigrams=number_of_trigrams)])
                           )
        else: 
            print("# Evolved Layout")
            print_layout_with_statistics(lay, verbose=True, letters=letters, repeats=repeats, number_of_letters=number_of_letters, number_of_bigrams=number_of_bigrams, trigrams=trigrams, number_of_trigrams=number_of_trigrams)
            print()
