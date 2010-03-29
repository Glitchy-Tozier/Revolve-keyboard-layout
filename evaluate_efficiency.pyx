set width 15
plot "2010-03-29-evolve-range-final-penalty.txt" title "final penalty in billion points", "2010-03-29-evolve-range-finger-repeats.txt" title "Finger repeats in percent", "2010-03-29-evolve-range-finger-disbalance.txt" title "Finger disbalance in pseudo standard deviation", "2010-03-29-evolve-range-key-position.txt" title "key position cost"
f(x) = a * b**(x*c) + d
fit f() "2010-03-29-evolve-range-final-penalty.txt" using 1:2 via a,b,c,d
plot "2010-03-29-evolve-range-final-penalty.txt" title "final penalty in billion points", "2010-03-29-evolve-range-finger-repeats.txt" title "Finger repeats in percent", "2010-03-29-evolve-range-finger-disbalance.txt" title "Finger disbalance in pseudo standard deviation", "2010-03-29-evolve-range-key-position.txt" title "key position cost", f(x) title "final penalty fit $a \cdot b^{x \cdot c} + d$"
