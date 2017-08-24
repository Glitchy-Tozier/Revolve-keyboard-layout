#!/bin/sh
grep total\ penalty\ per layouts-without* | cut -d \  -f 2 > without; grep total\ penalty\ per layouts-with-* | cut -d \  -f 2 > with ; grep total\ penalty\ per layouts-with20* | cut -d \  -f 2 > with20 ; grep total\ penalty\ per layouts-random-selection.txt | cut -d \  -f 2 > random
