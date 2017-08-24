# first run ./evolution-from-subset.sh
plot "with" title "select from 100, then 100 steps", "without" title "no subselection, 200 steps", "with20" title "select from 20, then 180 steps", "random" title "random layouts, ordered by selection group size"
set yaxis "total penalty per letter (tppl)"
set ylabel "total penalty per letter (tppl)"
set term png
set output evolution-from-subset.png
set output "evolution-from-subset.png"
set term x11
replot
