#!/usr/bin/env python3

"""Run a full evolution of keyboard layouts."""

EVOLUTION_STEPS = 100

steps = 4000
prerandomize = 1000000
controlled = False
quiet = False
verbose = True
controlled_tail = True

import sys
sys.argv.append("-o")
sys.argv.append("output.txt")

from check_neo import evolve_a_layout

for step in range(EVOLUTION_STEPS):
    print(step+1, "/", EVOLUTION_STEPS)
    evolve_a_layout(steps, prerandomize, controlled, quiet, verbose, controlled_tail)
    
