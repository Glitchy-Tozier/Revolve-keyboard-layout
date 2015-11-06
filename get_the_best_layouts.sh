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

for i in $(grep "billion total penalty" $1  | sort -r | cut -d " " -f 2 | uniq | tail -n $NUMBER | xargs)
 do grep -m 1 $i $1 -A 11 -B 18
done

