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

export NUMBER=3

if [ $# -eq 2 ]; then
    export NUMBER=$2
fi

for i in $(grep total $1  | sort -r | tail -n $NUMBER | cut -d " " -f 2 | xargs)
 do grep $i $1 -A 10 -B 17
done

