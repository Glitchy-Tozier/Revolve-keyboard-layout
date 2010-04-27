set width 15
set logscale x1

set title "Aggregate results"
plot "results/2010-04-27-evolve-range-final-penalty.txt" title "final penalty in billion points", "results/2010-04-27-evolve-range-finger-repeats.txt" title "Finger repeats in percent", "results/2010-04-27-evolve-range-finger-disbalance.txt" title "Finger disbalance in pseudo standard deviation", "results/2010-04-27-evolve-range-key-position.txt" title "key position cost"

set title "Final penalty"
plot "results/2010-04-27-evolve-range-final-penalty.txt" title "final penalty in billion points", 1.998716743 title "Neo", 3.055235076 title "Qwertz", 1.736400007 title "NordTast"

set title "Finger repeats"
plot "results/2010-04-27-evolve-range-finger-repeats.txt" title "Finger repeats [percent]", 4.82198888113 title "Neo", 6.72632774411 title "Qwertz", 1.83742456166 title "Nordtast"

set title "Finger disbalance in pseudo standard deviation"
plot "results/2010-04-27-evolve-range-finger-disbalance.txt" title "finger disbalance [million keystrokes]", 9.84247826956 title "Qwertz", 9.68350392408 title "Neo", 3.75005118331 title "NordTast"

set title "mean key position cost"
plot "results/2010-04-27-evolve-range-key-position.txt" title "mean key position cost", 5.53617048458 title "Qwertz", 4.06408223929 title "Neo", 3.96412236288 title "NordTast"
