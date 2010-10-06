#!/usr/bin/env python3
# encoding: utf-8

"""Run a full evolution of keyboard layouts."""

from optparse import OptionParser

### config

#: The number of new layouts to create. Can be overwritten with the -n parameter.
num_layouts = 50

#: The output filename. Can be overwritten with the -o parameter.
filename = "output.txt" # None for shell output

#: The number of random evolution steps to take.
steps = 4000

#: The number of random mutations to do before the evolution to get a random layout
prerandomize = 3000

#: Should we always do the locally best step (very slow and *not* optimal)
controlled = False

#: Should we spout out information on the shell? (Windows users disable this. Your shell can’t take Unicode)
quiet = False

#: Should we give additional statistics for the final layout?
verbose = True

#: Should we finalize the layout with as many controlled steps as needed, so a single keyswitch can’t improve it further?
controlled_tail = True

#: Should we use annealing? How many steps? Per step it adds one switch, so anneal 5 starts with 6 switches aka changing half the layout (12 keys).
anneal = 5
#: The number of iterations to spend in one anneal level. The first anneal * anneal_step iterations are spent in simulated annealing.
anneal_step = 100

#: The layout to use as base for mutations. If you want a given starting layout, also set prerandomize = 0.
STARTING_LAYOUT = """xvlcw khgfqß´
uiaeo snrtdy
üöäpz bm,.j"""


### Parse console arguments

parser = OptionParser(usage = "evolutionary running script", version = "0.1")
parser.add_option("-o", "--output", type="string", dest="filename", default=filename, help="set outputfile")
parser.add_option("-n", "--number", type="int", dest="evolution_steps", default=num_layouts, help="number of steps")
parser.add_option("-f", "--file", type="string", dest="data",
                  default=None, help="use the given textfile as korpus instead of the ngram files.", metavar="filepath")

(options, args) = parser.parse_args()

if options.data:
    with open(options.data) as f: 
        options.data = f.read()

### run

# Hack to make the script output to a file instead of the shell (necessary for windows users).
# MUST come before the imports from check_neo.
if filename is not None: 
    import sys
    sys.argv.append("-o")
    sys.argv.append(options.filename)

from check_neo import evolve_a_layout, string_to_layout
from time import time
from datetime import timedelta
STARTING_LAYOUT = string_to_layout(STARTING_LAYOUT)

print("# Starting the evolution.")

t = time()
for step in range(options.evolution_steps):
    evolve_a_layout(steps,
                    prerandomize,
                    controlled,
                    quiet,
                    verbose,
                    controlled_tail,
                    starting_layout=STARTING_LAYOUT,
                    data=options.data, 
                    anneal=anneal,
                    anneal_step = anneal_step)
    print(step+1, "/", options.evolution_steps,
          timedelta(seconds=time()-t))
    t = time()
