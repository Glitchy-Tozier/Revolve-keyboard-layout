#!/bin/bash

PATHPART=results/2010-08-16-

if [ $# -gt 0 ]; then
    if [ "$1" == "--help" ]; then
        echo "usage: $0 [<part of the path; gets appended *.txt>]"
        echo "example: $0 output"
        exit 0
    fi
    PATHPART=$1
fi

mkdir -p eval
grep -h total $PATHPART*txt | cut -d " " -f 2 > eval/total
grep -h "key position" $PATHPART*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/keys
grep -h "2gramme" $PATHPART*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/finger-rep
grep -h "keystrokes" $PATHPART*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/disbalance
grep -h "unbalancing" $PATHPART*txt | cut -d " " -f 2 > eval/unbalance
grep -h "trigrams have no hand" $PATHPART*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/handswitch
grep -h "rows" $PATHPART*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/rows
grep -h "shortcut" $PATHPART*txt | cut -d " " -f 2 > eval/short
grep -h "pattern" $PATHPART*txt | cut -d " " -f 2 > eval/pattern
