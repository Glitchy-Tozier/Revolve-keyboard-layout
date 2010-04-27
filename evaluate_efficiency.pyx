set width 15
set logscale x1
plot "results/2010-04-27-evolve-range-final-penalty.txt" title "final penalty in billion points", "results/2010-04-27-evolve-range-finger-repeats.txt" title "Finger repeats in percent", "results/2010-04-27-evolve-range-finger-disbalance.txt" title "Finger disbalance in pseudo standard deviation", "results/2010-04-27-evolve-range-key-position.txt" title "key position cost"
# f(x) = a * b**(x*c) + d
# fit f() "results/2010-04-27-evolve-range-final-penalty.txt" using 1:2 via a,b,c,d
plot "results/2010-04-27-evolve-range-final-penalty.txt" title "final penalty in billion points", "results/2010-04-27-evolve-range-finger-repeats.txt" title "Finger repeats in percent", "results/2010-04-27-evolve-range-finger-disbalance.txt" title "Finger disbalance in pseudo standard deviation", "results/2010-04-27-evolve-range-key-position.txt" title "key position cost", 1.811033032 title "neo final penalty", 2.830310786 title "Qwertz final penalty"
plot "results/2010-04-27-evolve-range-final-penalty.txt" title "final penalty in billion points", 2.830310786 title "Qwertz final penalty", 1.811033032 title "neo final penalty"
plot "results/2010-04-27-evolve-range-finger-repeats.txt" title "Finger repeats [percent]", 4.82198888113 title "Neo", 6.72632774411 title "Qwertz", 1.83742456166 title "Nordtast"
plot "results/2010-04-27-evolve-range-finger-disbalance.txt" title "finger disbalance [million keystrokes]", 7.75577431662 title "Qwertz finger disbalance [million keystrokes]", 4.56473130298 title "Neo finger disbalance [million keystrokes]"
plot "results/2010-04-27-evolve-range-key-position.txt" title "mean key position cost", 5.53615632047 title "Qwertz mean key position cost", 4.06408223929 title "Neo mean key position cost"
