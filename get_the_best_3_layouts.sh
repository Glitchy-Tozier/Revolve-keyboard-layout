#!/bin/bash

# get the best layouts from a given file. 

if [ $# -lt 1 ]; then 
    echo "usage: $0 <filename> [<number of layouts>]"
    exit 0
fi

if [ "$1" == "--help" ]; then
    echo "usage: $0 <filename> [<number of layouts>]"
    exit 0
fi

NUMBER=3

if [ $# -gt 1 ]; then
    NUMBER=$2
    exit 0
fi


for i in `grep "total" $1  | sort -r | tail -n 3 | cut -d " " -f 2 | xargs`; do grep $i evolved-layouts-2010-08-06.txt -A 10 -B 19; done

