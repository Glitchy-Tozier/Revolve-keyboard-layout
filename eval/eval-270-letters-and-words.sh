#!/bin/sh
FILE="beispieltext-prosa.txt"
cd .. 
echo Qwertz
./regularity_check.py -t $FILE -n Qwertz -o eval/res-qwertz.txt -w eval/res-qwertz-words.txt
echo Neo 2
./regularity_check.py -t $FILE -n Neo2  -o eval/res-neo2.txt -w eval/res-neo2-words.txt
echo NordTast
./regularity_check.py -t $FILE -n NordTast -o eval/res-nordtast.txt -w eval/res-nordtast-words.txt
# echo Vrijbuiter
#./regularity_check.py -t $FILE -n Vrijbuiter -o eval/res-vrijbuiter.txt -w eval/res-vrijbuiter-words.txt
echo fiae
./regularity_check.py -t $FILE -n fiae  -v -o eval/res-fiae.txt -w eval/res-fiae-words.txt
cd eval
pyxplot eval-270-letters.pyx
pyxplot eval-words.pyx


