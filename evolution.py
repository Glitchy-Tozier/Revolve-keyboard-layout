#!/usr/bin/env python3

"""Run a full evolution of keyboard layouts."""

### config

EVOLUTION_STEPS = 100

steps = 4000
prerandomize = 1000000
controlled = False
quiet = True
verbose = True
controlled_tail = True


STARTING_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),("←")], # Zahlenreihe (0)
    [("⇥"),("x"),("v"),("l"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [("⇩"),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),("⇘"),("\n")], # Reihe 2
    [("⇧"),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]


### run

import sys
sys.argv.append("-o")
sys.argv.append("output.txt")

from check_neo import evolve_a_layout

for step in range(EVOLUTION_STEPS):
    print(step+1, "/", EVOLUTION_STEPS)
    evolve_a_layout(steps,
                    prerandomize,
                    controlled,
                    quiet,
                    verbose,
                    controlled_tail,
                    starting_layout=STARTING_LAYOUT)
    
