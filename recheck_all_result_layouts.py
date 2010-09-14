#!/usr/bin/env python3

"""get all layout results from the results folder.

Depends on the layouts info starting with 'Evolved Layout'
"""

from check_neo import string_to_layout, print_layout_with_statistics
from os import listdir
from os.path import join

d = ""
for i in listdir("results"):
    if not i.endswith(".txt"):
        continue
    with open(join("results", i), encoding="utf-8") as f:
        try: 
            d += f.read()
        except UnicodeError:
            print("can’t open", i)

e = d.split("Evolved Layout")

layout_strings = []
for i in e[1:]:
    layout_strings.append("\n".join(i.splitlines()[1:4]))
    
all_layouts = [string_to_layout(l) for l in layout_strings]

for lay in all_layouts: 
    print_layout_with_statistics(lay, verbose=True)
