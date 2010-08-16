#!/usr/bin/env python3
"""Run a full evolution of keyboard layouts."""

from optparse import OptionParser

### config

filename = "output.txt" # None for shell output
steps = 4000
prerandomize = 1000000
controlled = False
quiet = True
verbose = True
controlled_tail = True

parser = OptionParser(usage = "evolutionary running script", version = "0.1")
parser.add_option("-o", "--output", type="string", dest="filename", default="output.txt", help="set outputfile")
parser.add_option("-n", "--number", type="int", dest="evolution_steps", default=50, help="number of steps")

(options, args) = parser.parse_args()

STARTING_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),("←")], # Zahlenreihe (0)
    [("⇥"),("x"),("v"),("l"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [("⇩"),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),("⇘"),("\n")], # Reihe 2
    [("⇧"),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]


### run

if filename is not None: 
    import sys
    sys.argv.append("-o")
    sys.argv.append(options.filename)

from check_neo import evolve_a_layout

for step in range(options.evolution_steps):
    print(step+1, "/", options.evolution_steps)
    evolve_a_layout(steps,
                    prerandomize,
                    controlled,
                    quiet,
                    verbose,
                    controlled_tail,
                    starting_layout=STARTING_LAYOUT)
