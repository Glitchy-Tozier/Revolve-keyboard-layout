# Command script saved by PyXPlot 0.8.1
# Timestamp: Wed Aug 25 05:12:50 2010
# User: Arne Babenhauserheide

set width 10
set yrange [10000:70000]
set multiplot 
set nodisplay

plot "res-qwertz.txt", "res-neo2.txt"
set origin 10,0 
plot "res-qwertz.txt", "res-nordtast.txt"
set origin 20,0 
#plot "res-qwertz.txt", "res-vrijbuiter.txt"
#set origin 30,0 
plot "res-qwertz.txt", "res-fiae.txt"

set display
refresh

set output "eval-letters.png"
set term png
replot
set term x11
replot
