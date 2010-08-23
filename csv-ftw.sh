#!/bin/sh

# Nur, weil das in Python nicht direkt ausgegeben werden kann. ;-)

for a in results/2010-*.txt; do
	sed 's/^# // ; t a; d ; :a s/ billion total penalty compared to notime-noeffort// ; t b; d; :b N; s/[^\n]*\n# [0-9]*.[0-9]* mean key position cost in file 1gramme.txt (/;/; N; s/ )[^\n]*\n# [0-9]*.[0-9]* % finger repeats in file 2gramme.txt (/;/; N; s/ )[^\n]*\n# [0-9]*.[0-9]* million keystrokes disbalance of the fingers (/;/; N; s/ )[^\n]*\n# [0-9]*.[0-9]* % finger repeats top to bottom or vice versa (/;/; N; s/ )[^\n]*\n# [0-9]*.[0-9]* % of trigrams have no handswitching (after direction change counted x 1 ) (/;/; N; s/ )[^\n]*\n# [0-9]*.[0-9]* billion (rows²\/dist)² to cross (/;/; N; N; s/ )[^\n]*\n# [0-9]*.[0-9]*[e]*[+-]*[0-9]* hand disbalance. Left: [0-9]*.[0-9]* %, Right: [0-9]*.[0-9]* %[^\n]*\n#/;/; N; s/ badly positioned shortcut keys (weighted).[^\n]*\n#/;/; N; s/ no handswitching after unbalancing key (weighted).[^\n]*\n#/;/; s/ movement pattern cost (weighted).//; p; d;' "$a"
done
