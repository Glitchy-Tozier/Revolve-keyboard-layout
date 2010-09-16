#!/bin/sh

# a cascade of greps to find all layouts which have values in a given range.
# take the median of each value as fixpoint (the value of a typical layout). 

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

# $ R
# > a = read.csv("layouts.csv", sep=";")
# > summary(a)
#  total.penalty   key.position.cost finger.repeats   disbalance.of.fingers
#  Min.   :19.83   Min.   :14.77     Min.   :0.3489   Min.   :0.4052       
#  1st Qu.:20.48   1st Qu.:15.05     1st Qu.:0.6555   1st Qu.:0.8973       
#  Median :20.84   Median :15.19     Median :0.7570   Median :1.0663       
#  Mean   :21.01   Mean   :15.23     Mean   :0.7976   Mean   :1.0761       
#  3rd Qu.:21.47   3rd Qu.:15.38     3rd Qu.:0.9091   3rd Qu.:1.2407       
#  Max.   :23.48   Max.   :16.58     Max.   :1.6705   Max.   :1.8463       
#  top.to.bottom.or.vice.versa handswitching.in.trigram X.rows..dist..  
#  Min.   :0.08527             Min.   :0.5506           Min.   :0.4390  
#  1st Qu.:0.19885             1st Qu.:0.9338           1st Qu.:0.6151  
#  Median :0.24342             Median :1.1292           Median :0.7269  
#  Mean   :0.25161             Mean   :1.2533           Mean   :0.7525  
#  3rd Qu.:0.29633             3rd Qu.:1.4689           3rd Qu.:0.8267  
#  Max.   :0.61345             Max.   :2.7018           Max.   :1.5323  
#  shortcut.keys     handswitching.after.unbalancing movement.pattern
#  Min.   :0.00000   Min.   :0.9096                  Min.   :3.198   
#  1st Qu.:0.05758   1st Qu.:1.1441                  1st Qu.:3.281   
#  Median :0.11516   Median :1.2089                  Median :3.402   
#  Mean   :0.09858   Mean   :1.2138                  Mean   :3.383   
#  3rd Qu.:0.11516   3rd Qu.:1.2797                  3rd Qu.:3.477   
#  Max.   :0.23032   Max.   :1.5518                  Max.   :3.524 

# alle Werte unten sind getestet, dass sie min 10 Layouts geben. 

#       phrase       value lines_before lines_after
$tot="total\ penalty 20.8  10           17"
$pos="position       15.1  11           16"
$rep="2gramme        0.75  12           15"
$dis="fingers        1.06  13           14"
$bot="bottom         0.24  14           13"
$swi="trigram        1.12  15           12"
$row="rows           0.72  16           11"
$sho="shortcut       0.11  17           10"
$unb="unbalancing    1.20  18           9"
$pat="pattern        3.40  19           8"

