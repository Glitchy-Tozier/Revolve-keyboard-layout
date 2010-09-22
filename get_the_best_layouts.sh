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

for i in $(grep "total penalty per letter" $1  | sort -u -r | tail -n $NUMBER | cut -d " " -f 2 | xargs)
 do grep -m 1 $i $1 -A 11 -B 17
done

