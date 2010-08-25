# Command script saved by PyXPlot 0.8.1
# Timestamp: Wed Aug 25 04:47:26 2010
# User: Arne Babenhauserheide

set title "cost for each word (with baseline qwertz)"
set xlabel "words"
set multiplot
set width 10

plot "res-qwertz-words.txt", "res-neo2-words.txt"
set origin 10,0 
plot "res-qwertz-words.txt", "res-nordtast-words.txt"
set origin 20,0 
plot "res-qwertz-words.txt", "res-fiae-words.txt"
#set origin 30,10 
#plot "res-qwertz-words.txt", "res-vrijbuiter-words.txt"

set output "eval-words.png"
set term png
replot
set term x11
replot
