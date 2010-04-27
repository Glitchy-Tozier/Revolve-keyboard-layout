#!/bin/bash

echo create data
for j in {1..9} {1..9}0 {1..9}00 {1..9}000 ; do time ./check_neo.py --evolve $j --prerandomize 10000 -v -q >> results/2010-04-27-evolve-$j-results.txt; done

echo check and plot the data
echo … final penalty 
for j in {1..9} {1..9}0 {1..9}00 {1..9}000; do grep "billion total" results/2010-04-27-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > results/2010-04-27-evolve-range-final-penalty.txt 
echo … finger repeats
for j in {1..9} {1..9}0 {1..9}00 {1..9}000; do grep 2gramme results/2010-04-27-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > results/2010-04-27-evolve-range-finger-repeats.txt 
echo … finger disbalance
for j in {1..9} {1..9}0 {1..9}00 {1..9}000; do grep disbalance results/2010-04-27-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > results/2010-04-27-evolve-range-finger-disbalance.txt
echo … key position cost
for j in {1..9} {1..9}0 {1..9}00 {1..9}000; do grep 1gramme results/2010-04-27-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > results/2010-04-27-evolve-range-key-position.txt


echo with pyxplot
# pyxplot evaluate_efficiency.pyx
