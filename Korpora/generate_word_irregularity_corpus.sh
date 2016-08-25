#!/bin/sh
cd $(dirname $(dirname $(realpath $0))) # main program folder
for i in $(for i in $(find Korpora/ -iname '*.txt') $(find Korpora/ -iname '*.utf8') beispieltext-prosa.txt; do cat $i; done); do
	echo $i; done | sort -u | grep '^[a-zA-Z0-9äöüÄÖÜßẞ ]*$' | sort -u > corpus_irregularity_words.txt
