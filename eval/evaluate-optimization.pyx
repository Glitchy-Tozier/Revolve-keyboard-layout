# Command script saved by PyXPlot 0.8.3
# Timestamp: Tue Oct 12 10:13:50 2010
# User: Arne Babenhauserheide

set xlabel "layouts"
set ylabel "total cost per letter (less is better)"
set title "Unique layouts from keyboard evolution for neo-layout.org using config-2010-09-19.1"
set width 15
plot "total-uniq.txt" title "optimized layouts" with dots, 1.250526 title "Neo 2", 1.119492 title "NordTast"
set output "eval-results/2010-10-12-total-cost-per-key-sorted-uniq-with-neo2.png"
set term png
replot
set term x11
replot
