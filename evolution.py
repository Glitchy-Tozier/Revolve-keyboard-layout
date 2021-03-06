#!/usr/bin/env python3
# encoding: utf-8

"""Run a full evolution of keyboard layouts."""

from optparse import OptionParser

### config

#: The number of new layouts to create. Can be overwritten with the -n parameter. 500 should have a 50% chance of finding the best possible layout (the global minimum).
num_layouts = 500

#: The output filename. Can be overwritten with the -o parameter.
filename = "output.txt" # None for shell output

#: The number of random evolution steps to take.
steps = 10000

#: The number of random mutations to do before the evolution to get a random layout.
prerandomize = 3000

#: The number of random layouts from which to select the best as starting point. Does not help, therefore set to 0.
preselect_random = 0

#: Should we always do the locally best step? (very slow and *not* optimal)
controlled = False

#: Should we avoid giving information on the shell? (Windows users enable this. Your shell can’t take Unicode)
quiet = True

#: Should a progressmeter be displayed? (Windows users disable this. Your shell can’t handle control sequences)
meter = False

#: Should we give additional statistics for the final layout?
verbose = True

#: Should we finalize the layout with as many controlled steps as needed, so a single keyswitch can’t improve it further?
controlled_tail = True

#: Should we use annealing? How many steps? Per step it adds one switch, so anneal 5 starts with 6 switches aka changing half the layout (12 keys).
anneal = 5
#: The number of iterations to spend in one anneal level. The first anneal * anneal_step iterations are spent in simulated annealing.
anneal_step = 1000

#: Should we limit the number of ngrams? A value of 3000 should still be safe to quickly see results without getting unreasonable layouts. Use 0 for no-limit.
limit_ngrams = 0

#: The layout to use as base for mutations. If you want a given starting layout, also set prerandomize = 0.
STARTING_LAYOUT_STR = """bmuaz kdflvjß
criey ptsnh⇘
xäüoö wg,.q"""


### Parse console arguments

parser = OptionParser(usage = "evolutionary running script", version = "0.1")
parser.add_option("-o", "--output", type="string", dest="filename", default=filename, help="set outputfile")
parser.add_option("-n", "--number", type="int", dest="evolution_steps", default=num_layouts, help="number of steps")
parser.add_option("-f", "--file", type="string", dest="data",
                  default=None, help="use the given textfile as korpus instead of the ngram files.", metavar="filepath")
parser.add_option("--ngrams", dest="ngram_config",
                  help="take the ngram sources from the config file", metavar="ngram.config")
parser.add_option("--starting-layout-string", type="string", dest="starting_layout_str",
                  default=STARTING_LAYOUT_STR, help="String version of the base layer of the starting layout.", metavar="layout")
parser.add_option("--prerandomize", type="int", dest="prerandomize", default=prerandomize, help="the number of prerandomization steps to take")
parser.add_option("--preselect-random", type="int", dest="preselect_random", default=preselect_random, help="the number of random layouts to create for selecting the best")
parser.add_option("--steps", type="int", dest="steps", default=steps, help="the number of mutation steps to take.")
parser.add_option("--not-quiet",
                      action="store_false", dest="quiet", default=quiet,
                      help="don’t be quiet, regardless of what evolution.py says")
parser.add_option("--tail",
                      action="store_true", dest="tail", default=controlled_tail,
                      help="finalize each evolution with a controlled tail run")
parser.add_option("--no-tail",
                      action="store_false", dest="tail", default=controlled_tail,
                      help="don’t use the controlled tail.")
parser.add_option("--progress",
                      action="store_true", dest="progress", default=meter,
                      help="Show a progress meter. Does not work on Windows.")
parser.add_option("--debug",
                      action="store_true", dest="debug", default=meter,
                      help="Show lots of debug output.")
parser.add_option("--anneal", dest="anneal", default=anneal, type="int",
                      help="use simulated annealing. Set to 0 for no anneal.")
parser.add_option("--limit-ngrams", type="int", dest="limit_ngrams", default=limit_ngrams,
                  help="Limit the number of ngrams to use. Speeds up the process but increases the danger of getting very bad outlier letters. Values of 3000 and higher still give plausible layouts.")

(options, args) = parser.parse_args()

quiet = options.quiet
meter = options.progress
if meter:
    quiet = True

# ensure that at most half the time is spent annealing
if options.anneal * anneal_step > options.steps:
    anneal_step = max(1, int(0.5 * options.steps / (1 + options.anneal)))

### run

# Hack to make the script output to a file instead of the shell (necessary for windows users).
# MUST come before the imports from check_neo.
if filename is not None:
    from sys import argv
    argv.append("-o")
    argv.append(options.filename)

from check_neo import evolve_a_layout
from layout_base import Layout, Layouts
from time import time
from datetime import timedelta
from termctrl import hide, show, write, priorline, erase
from atexit import register
STARTING_LAYOUT = Layout.from_string(options.starting_layout_str, Layouts.NEO2)

if not meter:
    print("# Starting the evolution.")
else:
    hide()
    register(show)
    write('best tppl:\n')
    write('avg. time:\n')
    write('layouts: %4d/%4d\n'%(0,options.evolution_steps))

t = time()
best_tppl = 10 # not safe
for step in range(options.evolution_steps):
    tppl = evolve_a_layout(STARTING_LAYOUT,
                           options.steps,
                           options.prerandomize,
                           controlled,
                           quiet,
                           meter,
                           verbose,
                           options.tail,
                           datafile=options.data,
                           ngram_config=options.ngram_config,
                           anneal=options.anneal,
                           anneal_step = anneal_step,
                           fingerstats = True,
                           limit_ngrams = options.limit_ngrams,
                           preselect_random = options.preselect_random,
                           show_each_step = options.debug)
    if not meter:
        print(step+1, "/", options.evolution_steps, timedelta(seconds=time()-t))
        t = time()
    else:
        priorline(); priorline()
        if tppl < best_tppl:
            best_tppl = tppl
            priorline()
            erase(); write('best tppl: %f\n'%tppl)
        erase(); write('avg. time: %s\n'%str(timedelta(seconds=(time()-t)/(step+1))))
        erase(); write('layouts: %4d/%4d\n'%(step+1,options.evolution_steps))
