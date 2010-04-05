set width 15
set logscale x1
plot "results/2010-03-29-evolve-range-final-penalty.txt" title "final penalty in billion points", "results/2010-03-29-evolve-range-finger-repeats.txt" title "Finger repeats in percent", "results/2010-03-29-evolve-range-finger-disbalance.txt" title "Finger disbalance in pseudo standard deviation", "results/2010-03-29-evolve-range-key-position.txt" title "key position cost"
f(x) = a * b**(x*c) + d
fit f() "results/2010-03-29-evolve-range-final-penalty.txt" using 1:2 via a,b,c,d
plot "results/2010-03-29-evolve-range-final-penalty.txt" title "final penalty in billion points", "results/2010-03-29-evolve-range-finger-repeats.txt" title "Finger repeats in percent", "results/2010-03-29-evolve-range-finger-disbalance.txt" title "Finger disbalance in pseudo standard deviation", "results/2010-03-29-evolve-range-key-position.txt" title "key position cost", f(x) title "final penalty fit $a \cdot b^{x \cdot c} + d$", 1.380194974 title "neo final penalty", 2.048361472 title "Qwertz final penalty"
plot "results/2010-03-29-evolve-range-finger-repeats.txt" title "Finger repeats in percent", 4.82198888113 title 
"Neo for comparision", 6.72632774411 title "Qwertz for comparision"

