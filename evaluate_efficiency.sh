#!/bin/bash

echo create data, small steps
# for j in {1..130} {200..220} {300..310} {400..410} {1000..1005}; do time ./check_neo.py --evolve $j --prerandomize 10000 -q >> results/2010-03-29-evolve-$j-results.txt; done
echo … and big steps
# for j in {0..9}; do for i in {0..9}; do time ./check_neo.py --evolve $j --prerandomize 10000 -q >> results/2010-03-29-evolve-$j$i0-results.txt; done; done

echo check and plot the data
echo … final penalty 
for j in {1..130} {200..220} {300..310} {400..410} {1000..1005}; do grep billion results/2010-03-29-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > 2010-03-29-evolve-range-final-penalty.txt 
echo … finger repeats
for j in {1..130} {200..220} {300..310} {400..410} {1000..1005}; do grep 2gramme results/2010-03-29-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > 2010-03-29-evolve-range-finger-repeats.txt 
echo … finger disbalance
for j in {1..130} {200..220} {300..310} {400..410} {1000..1005}; do grep disbalance results/2010-03-29-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > 2010-03-29-evolve-range-finger-disbalance.txt
echo … key position cost
for j in {1..130} {200..220} {300..310} {400..410} {1000..1005}; do grep 1gramme results/2010-03-29-evolve-$j-results.txt | cut -d " " -f 2| sed "s/^/$j /" ; done > 2010-03-29-evolve-range-key-position.txt


echo with pyxplot
# pyxplot evaluate_efficiency.pyx
