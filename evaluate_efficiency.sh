#!/bin/bash

if [ $# -lt 1 ]; then 
    echo "usage: $0 <identifier>"
    exit 0
fi

if [ "$1" == "--help" ]; then
    echo "usage: $0 <identifier>"
    exit 0
fi

echo create data
for j in {1..9} {1..9}0 {1..9}00 {1..9}000 
    do time ./check_neo.py --evolve $j --prerandomize 10000 -v -q >> results/$1-evolve-$j-results.txt
done

echo check and plot the data
echo … final penalty 
for j in {1..9} {1..9}0 {1..9}00 {1..9}000; do grep "billion total" results/$1-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > results/$1-evolve-range-final-penalty.txt 
echo … finger repeats
for j in {1..9} {1..9}0 {1..9}00 {1..9}000; do grep 2gramme results/$1-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > results/$1-evolve-range-finger-repeats.txt 
echo … finger disbalance
for j in {1..9} {1..9}0 {1..9}00 {1..9}000; do grep disbalance results/$1-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > results/$1-evolve-range-finger-disbalance.txt
echo … key position cost
for j in {1..9} {1..9}0 {1..9}00 {1..9}000; do grep 1gramme results/$1-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > results/$1-evolve-range-key-position.txt

# and old style results
for j in {1..130} 1{4..9}0 {201..205} {301..305} {401..405} {601..603} {1001..1003} 10000; do grep "billion total" results/$1-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done >> results/$1-evolve-range-final-penalty.txt; for j in {1..130} 1{4..9}0 {201..205} {301..305} {401..405} {601..603} {1001..1003} 10000; do grep 2gramme results/$1-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done >> results/$1-evolve-range-finger-repeats.txt; for j in {1..130} 1{4..9}0 {201..205} {301..305} {401..405} {601..603} {1001..1003} 10000; do grep disbalance results/$1-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done >> results/$1-evolve-range-finger-disbalance.txt; for j in {1..130} 1{4..9}0 {201..205} {301..305} {401..405} {601..603} {1001..1003} 10000; do grep 1gramme results/$1-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done >> results/$1-evolve-range-key-position.txt
echo with pyxplot
# pyxplot evaluate_efficiency.pyx
