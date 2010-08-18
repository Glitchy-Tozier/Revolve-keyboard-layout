#set title "Layout result evaluation"
set xlabel "layouts"
set ylabel "weighted cost"
set multiplot
plot "eval/total" with color Red
set origin 10,0
plot "eval/keys"
set origin 20,0
plot "eval/finger-rep"
set origin 0,7
plot "eval/disbalance"
set origin 10,7
plot "eval/unbalance"
set origin 20,7
plot "eval/handswitch"
set origin 0,14
plot "eval/rows"
set origin 10,14
plot "eval/pattern"
set origin 20,14
plot "eval/short"

set output "layouts.png"
set term png
replot
set term x11
replot