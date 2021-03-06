#!/bin/sh

# a cascade of greps to find all layouts which have values in a given range.
# take the median of each value as fixpoint (the value of a typical layout). 
# TODO: recalculate all values for a reference sentence. Then work with these.
# -> results/2010-08-17-all-recalculated-for-the-reference-text.txt

### data

## layout

# #### 21 ####
# xuc.ü vdsljq´
# miaeo btrnhk
# y,zäö fgßwp 
# ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──────┐
# │ ^ │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ ` │ ←    │
# ├───┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬─────┤
# │  ⇥ │ x │ u │ c │ . │ ü │ v │ d │ s │ l │ j │ q │ ´ │ Ret │
# ├────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─┐   │
# │   ⇩ │ m │ i │ a │ e │ o │ b │ t │ r │ n │ h │ k │ ⇘  │   │
# ├────┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴──┬┴────┴───┤
# │  ⇧ │ M4│ y │ , │ z │ ä │ ö │ f │ g │ ß │ w │ p │ ⇗       │
# ├────┼───┴┬──┴─┬─┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬────┬───┤
# │Str │ Fe │ Al │      Leerzeichen       │ M4 │ Fe │ Me │Str│
# └────┴────┴────┴────────────────────────┴────┴────┴────┴───┘ 
# 19.825044696 billion total penalty compared to notime-noeffort 
# 5.19590183127 mean key position cost in file 1gramme.txt ( 14.95921721 ) 
# 1.54621348386 % finger repeats in file 2gramme.txt ( 0.66178688 ) 
# 3.42663847398 million keystrokes disbalance of the fingers ( 0.856659618 ) 
# 0.036349195039 % finger repeats top to bottom or vice versa ( 0.248922112 ) 
# 1.51856790633 % of trigrams have no handswitching (after direction change counted x 1 ) ( 0.88434855 ) 
# 3.02438136579 billion (rows²/dist)² to cross ( 0.604876273157 ) 
# 0.0263628392305 hand disbalance. Left: 0.47363716077 %, Right: 0.52636283923 % 
# 0.0575808308 badly positioned shortcut keys (weighted). 
# 1.204443 no handswitching after unbalancing key (weighted). 
# 3.47210222 movement pattern cost (weighted). 

## layout value summary

# $ ./csv-ftw.sh
# $ R
# > a = read.csv("2010-09-19.1-zusammen.csv", sep=";")
# > summary(a)
# total.penalty.per.word key.position.cost finger.repeats  
# Min.   :0.8995         Min.   :16.71     Min.   :0.7223  
# 1st Qu.:0.9221         1st Qu.:17.13     1st Qu.:1.3244  
# Median :0.9464         Median :17.31     Median :1.4832  
# Mean   :0.9575         Mean   :17.38     Mean   :1.5385  
# 3rd Qu.:0.9868         3rd Qu.:17.52     3rd Qu.:1.6811  
# Max.   :1.1441         Max.   :20.31     Max.   :3.0542  
# disbalance.of.fingers top.to.bottom.or.vice.versa handswitching.in.trigram
# Min.   :0.3004        Min.   :0.07742             Min.   :1.147           
# 1st Qu.:1.2421        1st Qu.:0.22758             1st Qu.:1.735           
# Median :1.9504        Median :0.27188             Median :2.020           
# Mean   :1.8921        Mean   :0.28142             Mean   :2.268           
# 3rd Qu.:2.4224        3rd Qu.:0.32899             3rd Qu.:2.589           
# Max.   :4.5609        Max.   :0.71921             Max.   :5.498           
# X.rows..dist..  shortcut.keys     handswitching.after.unbalancing
# Min.   :1.247   Min.   :0.00000   Min.   :0.5089                 
# 1st Qu.:1.872   1st Qu.:0.05758   1st Qu.:0.6789                 
# Median :2.387   Median :0.11516   Median :0.7258                 
# Mean   :2.285   Mean   :0.10489   Mean   :0.7331                 
# 3rd Qu.:2.509   3rd Qu.:0.11516   3rd Qu.:0.7826                 
# Max.   :4.583   Max.   :0.23032   Max.   :1.0646                 
# movement.pattern
# Min.   :0.7969  
# 1st Qu.:0.8569  
# Median :0.9478  
# Mean   :0.9200  
# 3rd Qu.:0.9760  
# Max.   :1.0098

# $ R
# > a <- read.csv("empirie/2010-09-19.1-result-layouts-reference.csv", sep=";")
# > summary(a)
# total.penalty.per.word key.position.cost   finger.repeats     
# Min.   :0.6752         Min.   :9.510e-06   Min.   :0.000e+00  
# 1st Qu.:0.7623         1st Qu.:9.950e-06   1st Qu.:2.560e-07  
# Median :0.7946         Median :1.009e-05   Median :5.120e-07  
# Mean   :0.8029         Mean   :1.017e-05   Mean   :6.447e-07  
# 3rd Qu.:0.8329         3rd Qu.:1.032e-05   3rd Qu.:1.024e-06  
# Max.   :1.1157         Max.   :1.237e-05   Max.   :2.816e-06  
# disbalance.of.fingers top.to.bottom.or.vice.versa handswitching.in.trigram
# Min.   :2.964e-06     Min.   :0.000e+00           Min.   :0.000e+00
# 1st Qu.:3.193e-06     1st Qu.:0.000e+00           1st Qu.:6.000e-07
# Median :3.318e-06     Median :0.000e+00           Median :9.000e-07
# Mean   :3.341e-06     Mean   :2.001e-10           Mean   :9.731e-07
# 3rd Qu.:3.475e-06     3rd Qu.:0.000e+00           3rd Qu.:1.200e-06
# Max.   :4.169e-06     Max.   :2.048e-06           Max.   :7.200e-06
# X.rows..dist..      shortcut.keys       handswitching.after.unbalancing
# Min.   :7.769e-08   Min.   :0.000e+00   Min.   :1.200e-07
# 1st Qu.:6.011e-07   1st Qu.:4.280e-08   1st Qu.:2.800e-07
# Median :7.886e-07   Median :8.560e-08   Median :3.200e-07
# Mean   :7.996e-07   Mean   :7.839e-08   Mean   :3.255e-07
# 3rd Qu.:8.817e-07   3rd Qu.:8.560e-08   3rd Qu.:3.600e-07
# Max.   :3.979e-06   Max.   :1.712e-07   Max.   :7.600e-07
# movement.pattern    
# Min.   :3.800e-07
# 1st Qu.:5.000e-07
# Median :5.000e-07
# Mean   :5.163e-07
# 3rd Qu.:5.600e-07

# alle Werte unten sind getestet, dass sie min 10 Layouts geben. 

alias grep="grep -h"

lays="empirie/2010-09-19.1-result-layouts-reference-uniq.txt"

#                              lines_before lines_after
tot="0\\.7.*per.*        -B 16        -A 11" # ignored
pos="position.*1\\.0[0123].*e-05         -B 18        -A 10"
rep="2gramme.*2\\.56e-07      -B 19        -A 9"
dis="fingers.*3\\.[2].*e-06          -B 20        -A 8"
bot="bottom.*0\\.0           -B 21        -A 7"
swi="trigram.*6e-07        -B 22        -A 6"
row="rows.*[6]\\..*e-07             -B 23        -A 5"
sho="8\\.560.*shortcut         -B 24        -A 4" # ignored: no effect on typing.
unb="3\\.*[1234]*e-07.*unbalancing      -B 25        -A 3"
pat="5e-07.*pattern          -B 26        -A 2"

echo --- reference layouts ---
cat $lays | grep $pos | grep $rep | grep $dis | grep $bot | grep $swi | grep $row | grep $unb #| grep $pat

# partial
echo " " 
echo " " 
echo " " --- position-cost ---
echo " " 
cat $lays | grep $rep | grep $dis | grep $bot | grep $swi | grep $row | grep $unb #| grep $pat 
echo " " 
echo " " 
echo " " --- finger-repeats ---
echo " " 
cat $lays | grep $pos | grep $dis | grep $bot | grep $swi | grep $row | grep $unb #| grep $pat 
echo " " 
echo " " 
echo " " --- finger-disbalance ---
echo " " 
cat $lays | grep $pos | grep $rep | grep $bot | grep $swi | grep $row | grep $unb #| grep $pat
# echo " " 
# echo " " 
# echo " " --- top-bottom ---
# echo " " 
# cat $lays | grep $pos | grep $rep | grep $dis | grep $swi | grep $row | grep $unb #| grep $pat
echo " " 
echo " " 
echo " " --- handswitching ---
echo " " 
cat $lays | grep $pos | grep $rep | grep $dis | grep $bot | grep $row | grep $unb #| grep $pat
echo " " 
echo " " 
echo " " --- rows ---
echo " " 
cat $lays | grep $pos | grep $rep | grep $dis | grep $bot | grep $swi | grep $unb #| grep $pat
echo " " 
echo " " 
echo " " --- switch-after-unbalancing ---
echo " " 
cat $lays | grep $pos | grep $rep | grep $dis | grep $bot | grep $swi | grep $row #| grep $pat
