mkdir -p eval
grep -h total results/2010-08-16-*txt | cut -d " " -f 2 > eval/total
grep -h "key position" results/2010-08-16-*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/keys
grep -h "2gramme" results/2010-08-16-*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/finger-rep
grep -h "keystrokes" results/2010-08-16-*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/disbalance
grep -h "unbalancing" results/2010-08-16-*txt | cut -d " " -f 2 > eval/unbalance
grep -h "trigrams have no hand" results/2010-08-16-*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/handswitch
grep -h "rows" results/2010-08-16-*txt | ./pyline "line.split('( ')[1].split(' )')[0]" > eval/rows
grep -h "shortcut" results/2010-08-16-*txt | cut -d " " -f 2 > eval/short
grep -h "pattern" results/2010-08-16-*txt | cut -d " " -f 2 > eval/pattern
