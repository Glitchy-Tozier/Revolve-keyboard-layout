# Command script saved by PyXPlot 0.8.1
# Timestamp: Sat Jul 31 19:46:36 2010
# User: Arne Babenhauserheide

set width 15
set title "text comparision: prosa vs. korpus"
set xlabel "line number [index]"
set ylabel "cost [$\sum{nGram\ occurrence\ diff} \cdot (100+log_2(len(line))$] "
plot "res2" title "sentences.mod.utf-8.txt", "res" title "beispieltext-prosa.txt"
