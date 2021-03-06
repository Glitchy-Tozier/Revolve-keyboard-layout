#!/usr/bin/env python3
# encoding: utf-8

"""Configuration of check_neo, mainly the weights of the cost functions. Intended to be easily modified."""

### definitions

#: The mutated letters - only these get changed. You may change these to leave letters in their defined place.
ABC = "abcdefghijklmnopqrstuvwxyzäöüß,." # äöüß,." # ⇧⇗"

#The letters which are used to calculate the costs - do not change anything or results will become incomparable.
ABC_FULL = "abcdefghijklmnopqrstuvwxyzäöüß,."

#: The modifiers, sorted by layer, split into left and right, counting from 0.
MODIFIERS_PER_LAYER = [("", ""), ("⇧", "⇗"), ("⇩", "⇘"), ("⇚", "⇙"), ("⇩⇧", "⇘⇗"), ("⇩⇚", "⇘⇙")]

#: The positions which are by default accessed by the given finger. 
FINGER_POSITIONS = {
    "Klein_L": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0), (2, 1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0), (4, 0, 0), (4, 1, 0)], # Klein_L
    "Ring_L": [(0, 3, 0), (1, 2, 0), (2, 2, 0), (3, 3, 0)], # Ring_L
    "Mittel_L": [(0, 4, 0), (1, 3, 0), (2, 3, 0), (3, 4, 0)], # Mittel_L
    "Zeige_L": [(0, 5, 0), (0, 6, 0), (1, 4, 0), (2, 4, 0), (3, 5, 0), (1, 5, 0), (2, 5, 0), (3, 6, 0)], # Zeige_L
    "Daumen_L": [(4, 2, 0), (4, 3, 0)], # Daumen_L
    "Daumen_R": [(4, 3, 0), (4, 4, 0)], # Daumen_R
    "Zeige_R": [(0, 7, 0), (0, 8, 0), (1, 6, 0), (2, 6, 0), (3, 7, 0), (1, 7, 0), (2, 7, 0), (3, 8, 0)], # Zeige_R
    "Mittel_R": [(0, 9, 0), (1, 8, 0), (2, 8, 0), (3, 9, 0)], # Mittel_R
    "Ring_R": [(0, 10, 0), (1, 9, 0), (2, 9, 0), (3, 10, 0)], # Ring_R
    "Klein_R": [(0, 11, 0), (0, 12, 0), (0, 13, 0), (1, 10, 0), (2, 10, 0), (3, 11, 0), (1, 11, 0), (2, 11, 0), (1, 12, 0), (2, 12, 0), (1, 13, 0), (2, 13, 0), (3, 12, 0), (4, 5, 0), (4, 6, 0), (4, 7, 0)] # Klein_R
}

#: The lowest index for the right hand per line in the config (pos[0] is the line, pos[1] the index). TODO: Generate automatically from the finger positions.
RIGHT_HAND_LOWEST_INDEXES = [7, 6, 6, 7, 3]

### cost weighting


## Basics

WEIGHT_POSITION = 20 #: reference cost - gets multiplied with the COST_PER_KEY.

WEIGHT_CRITICAL_FRACTION = 0.001 #: The bigram count with a fraction of the bigrams higher than this is increased sharply, relative to the amount by which they exceed the fraction. Value guessed from experience from effchen (adnw ln disturbs writing, below that does not). 0.1% is about twice per DinA4-page (30 lines, 60 letters). There should be no bad combination which appears twice per DinA4 page, because that will stick to ones mind as a cludge.
WEIGHT_CRITICAL_FRACTION_MULTIPLIER = 2 #: The amount of usage higher than the critical fraction is multiplied by this multiplier. Warning: Any value different from 1 means that stats reported by check_neo.py will be incorrect.


## Cost for single key positions

# Structured key weighting (but still mostly from experience and deducing from the work of others).
# The speed of the fingers is taken out (see INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY).
# So this shows the reachability of the keys, ignoring the different speed of the fingers.
# “How much does the hand hurt when reaching for the key” :)
# rationale: reaching for the Neo 2 x hurts thrice as much as just hitting the Neo2 u → 10 vs. 3.
# the upper keys on the right hand can be reached a bit better, since movement is aligned with the hand
# (except for q, since the pinky is too short for that).
# theoretical minimum (assigning the lowest cost to the most frequent char, counting only the chars on layer 1):
# 1123111113 = 3.3490913205386508 mean key position cost
# Ringfinger on lower row takes 1.5 times the time of index on the upper row[1].
# [1]: http://forschung.goebel-consult.de/de-ergo/rohmert/Rohmert.html - only one person!
COST_PER_KEY  = [
    # The 0 values aren’t filled in at the moment.
    # Don’t put mutated keys there, otherwise the best keys will end up there!
    [80,    70,60,50,50,60,    60,50,50,50,50,60,70, 80], # Zahlenreihe (0)
    [24,    16,10, 5,12,17,    20,13, 5, 9,11,20,36,  0], # Reihe 1
    [9,      5, 3, 3, 3, 6,     6, 3, 3, 3, 5, 9,30, 6], # Reihe 2; enter low to make it preferred over the layer 4 enter.
    [20,16, 19,24,20,9,   30,  10, 8,22,22,17,       19],     # Reihe 3
    [0,0,0,                3           , 7, 0, 0, 0] # Reihe 4 mit Leertaste
]

COST_LAYER_ADDITION = [0, 20, 9, 16, 29, 25]

#: The cost of any key which isn’t on the keyboard. Should be higher than max(COST_LAYER_ADDITION) + the most expensive key + 2 * WEIGHT_FINGER_REPEATS * mods_on_same_hand_adjustment [local variable in split uppercase bigrams] to make sure that having a key on a bad position in layer 5 is better than not having it at all. Currently (eb0c9e8c8b02 + 1) that means, it must be higher than 27+50+16 = 93. Trial and error shows, it must be about 150 to make the addition of the neo layers to nordtast useful.
COST_PER_KEY_NOT_FOUND = 150


## Finger repeats

WEIGHT_FINGER_REPEATS = 1200 #: Cost of a finger repeat. Gets additional +1 from the row change on the same finger.
WEIGHT_FINGER_REPEATS_INDEXFINGER_MULTIPLIER = 0.9 #: Cost of a finger repeat on the indexfinger (hurts less). Warning: Any value different from 1 means that the percentage of finger repeats reported by check_neo.py will be incorrect.
WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION = 0.00025 #: The cost of finger repeats with a fraction of the bigrams higher than this is increased sharply, relative to the amount by which they exceed the fraction. Value guessed from experience from effchen (adnw ln disturbs writing, below that does not). 0.05% is about once per DinA4-page (30 lines, 60 letters). There should be no single finger repetition which appears once per DinA4 page, because that will stick to ones mind as a cludge.
WEIGHT_FINGER_REPEATS_CRITICAL_FRACTION_MULTIPLIER = 5 #: The amount of usage higher than the critical fraction is multiplied by this multiplier. Warning: Any value different from 1 means that the percentage of finger repeats reported by check_neo.py will be incorrect.

WEIGHT_FINGER_REPEATS_TOP_BOTTOM = 6000 #: Additional cost of a finger repetition from the top to the bottom line. Gets added to the cost of the normal finger repetition. Additionally this gets costs as row repetition on the same hand (+4). 


## Line changes

WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW = 13 #: When I have to switch the row in a bigram while on the same hand, that takes time => Penalty per (row to cross ² / horizontal distance)² if we’re on the same hand. 

WEIGHT_COUNT_ROW_CHANGES_BETWEEN_HANDS = False #: Should we count a row change with a handswitch as row change? 
SHORT_FINGERS = ["Zeige_L", "Zeige_R", "Klein_R"] #: Fingers from which switching upwards and to which switching downwards is cheaper. Not pinky left, because the default keyboard penalizes its lower key.
LONG_FINGERS = ["Ring_L", "Mittel_L", "Mittel_R", "Ring_R"]


## Finger and Hand disbalance in load

WEIGHT_HAND_DISBALANCE = 80 #: Disbalance between the load on the hands. Calculated from the finger disbalance, but coarser. If both hands have slightly unequal load on the individual fingers, but overall both hands have the same load, the layout feels equal.

WEIGHT_FINGER_DISBALANCE = 2000 #: multiplied with the standard deviation of the finger usage - value guessed and only valid for the 1gramme.txt corpus. 

WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY = [
    1.0,
    1.6,
    2.0,
    2.0, # is 1/3 faster
    2,
    2,
    2.0,
    2.0,
    1.6,
    1.0] #: The intended load per finger. Inversed and then used as multiplier for the finger load before calculating the finger disbalance penalty. Any load distribution which strays from this optimum gives a penalty.


## Handswitching

WEIGHT_TOO_LITTLE_HANDSWITCHING = 1200 #: how high should it be counted, if the hands aren’t switched in a triple?

WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE = 1 #: multiplier for triples without handswitch in which there also is a direction change? Also affects the “unweighted” result from total_cost!
WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE = 0 #: multiplier for triples without handswitch in which the direction doesn’t change. Also affects the “unweighted” result from total_cost!

WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY = 53 #: How much penalty we want if there’s no handswitching after an unbalancing key. Heavy unbalancing (wkßz, M3 right, return and the shifts) counts double (see UNBALANCING_POSITIONS). This also gives a penalty for handswitching after an uppercase letter. Wolfs Value: 10
WEIGHT_UNBALANCING_AFTER_UNBALANCING = 4 #: If an unbalancing key follows another unbalancing one on the other side of the hand, the cost of that key gets multiplied with this weighting and added, too. Wolfs Value: 2
WEIGHT_NEIGHBORING_UNBALANCE = 400 #: The penalty for an unbalancing key following after a neighboring finger or vice versa. Wolfs Value: 5

#: Positions which pull the hand from the base row, position and cost (the strength of the pulling from base row). 
UNBALANCING_POSITIONS = {
    (0, 0, 0): 2, # ^
    (0, 1, 0): 2, # 1
    (0, 2, 0): 2, # 2
    (0, 10, 0): 2, # 0
    (0, 11, 0): 2, # -
    (0, 12, 0): 2, # `
    (0, 13, 0): 3, # Backspace
    (1, 0, 0): 2, # Tab
    (1, 1, 0): 1,# x
    (1, 4, 0): 0.1, #
    (1, 5, 0): 2, # w
    (1, 6, 0): 2, # k
    (1, 7, 0): 0.1, #
    (1, 10, 0): 1, # q
    (1, 11, 0): 2, # ß
    (1, 12, 0): 2.5, # ´
    (2, 0, 0): 1, # L_M3
    (2, 5, 0): 1, # o
    (2, 6, 0): 1, # s
    (2, 11, 0): 1, # y
    (2, 12, 0): 2, # R_M3
    (2, 13, 0): 2, # Return
    (3, 0, 0): 2, # L_Shift
    (3, 12, 0): 2, # R_Shift
    (3, 3, 0): 0.5, # ä
    (3, 4, 0): 0.5, # ö
    (3, 6, 0): 2, # z
    (3, 7, 0): 0.5, # b
    (3, 9, 0): 0.5, # ,
    (3, 10, 0): 0.5, # .
    (4, 0, 0): 3, # L_Ctrl
    (4, 7, 0): 3 # R_Ctrl
}


## Secondary / Indirect bigrams

WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM_HANDSWITCH = 0.8 #: multiplier for the cost of secondary bigrams in trigrams with handswitches. 
WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM = 0.7 #: multiplier for the cost of secondary bigrams in trigrams without handswitching. 


## Movement patterns: Penalties for certain finger usages, like pinky → ringfinger

WEIGHT_FINGER_SWITCH = 60 #: how much worse is it to switch from middle to indexfinger compared with middle to pinky (~30ms according to Rohmert). Movement pattern cost.

#: The cost for moving from one finger to another one with middle-to-index as 1 (30ms). Currently only uses the neighbors. Can also be used to favor a certain direction. Adapted the Rohmert times as per my own experiences: http://lists.neo-layout.org/pipermail/diskussion/2010-May/017171.html and http://lists.neo-layout.org/pipermail/diskussion/2010-May/017321.html - Also: Sehnenscheidenentzündung vermeiden: Nachbarfinger vermeiden. Ring- und Mittelfinger verbunden → Ring = ⅓ Nachbar von Zeige.
FINGER_SWITCH_COST = { # iu td < ui dt dr ua rd au < ai rt < nd eu
    "Klein_L": {
        "Ring_L": 8, # slow + dangerous
        "Mittel_L": 2 # a bit dangerous
        }, 
    "Ring_L": {
        "Klein_L": 12, # slow + dangerous + outwards
        "Mittel_L": 6, # dangerous
        "Zeige_L": 0.1 # a tiny bit dangerous
        }, 
    "Mittel_L": {
        "Ring_L": 9, # dangerous + outwards
        "Klein_L": 3, # a bit dangerous + outwards
        "Zeige_L": 0.6 # it’s fast but dangerous (Sehnenscheidenentzündung)
        }, 
    "Zeige_L": {
        "Klein_L": 0.1, 
        "Ring_L": 0.3, # gegen Sehnenscheidenentzündung
        "Mittel_L": 0.9 # it’s good, but having two directions disturbs the writing flow.
        }, 
    "Daumen_L": {
        },
    "Daumen_R": {
        },
    "Zeige_R": {
        "Mittel_R": 0.9, 
        "Ring_R": 0.3,
        "Klein_R": 0.1
        },
    "Mittel_R": {
        "Zeige_R": 0.6,
        "Klein_R": 3,
        "Ring_R": 9
        },
    "Ring_R": {
        "Zeige_R": 0.1,
        "Mittel_R": 6,
        "Klein_R": 12
        }, 
    "Klein_R": {
        "Mittel_R": 2,
        "Ring_R": 8
        }
} # iutd, drua, uidt, rdau, airt, ndeu :)


## Common Shortcut keys to the left

WEIGHT_XCVZ_ON_BAD_POSITION = 1.0 #: the penalty *per letter* in the text if xvcz are on bad positions (cumulative; if all 4 are on bad positions (not in the first 5 keys, counted from the left side horizontally) we get 4 times the penalty). 

WEIGHT_ASYMMETRIC_SIMILAR = 30.0 #: the penalty *per letter* in the text if similar keys (like aä or oö) have inconsistent symmetry, logarithmic in the number of inconsistent keys.
#: [(first-letters, second-letters), ...]. 
SIMILAR_LETTERS = [("auo", "äüö"), # umlauts to vowels
                   ("auo", "äüö"), # umlauts to vowels, twice to double the cost
                   ("gbdw", "kptf"), # soft consonants to hard consonants
                   ("sfdn", "tpbm")] # tongue consonants to lip-consonants
                   # ("mw", "nv"), # visual appearance
                   # ("qd", "pb"), # visual appearance
                   # ("mn", "wv")] # visual appearance

## Symmetry of the movement

#: Asymmetric bigrams are harder to type than symmetric ones.
WEIGHT_ASYMMETRIC_BIGRAMS = 1


## Manual tweaks

WEIGHT_MANUAL_BIGRAM_PENALTY = 1000
#: Manually added bigrams which are bad to type but hard to catch algorithmically.
COST_MANUAL_BIGRAM_PENALTY = {
#    ((1, 2, 0), (2, 3, 0)): 0.1, # vd on normal keyboards (lower row shifted to the right)
#    ((1, 9, 0), (2, 8, 0)): 0.1, # ok on normal keyboards (lower row shifted to the right)
    ((1, 2, 0), (3, 2, 0)): 1, # wz on normal keyboards (lower row shifted to the right)
    ((3, 2, 0), (1, 2, 0)): 1, # zw on normal keyboards (lower row shifted to the right)
    ((2, 2, 0), (3, 2, 0)): 0.3, # sz on normal keyboards (lower row shifted to the right)
    ((3, 2, 0), (2, 2, 0)): 0.3, # zs on normal keyboards (lower row shifted to the right)
    ((2, 3, 0), (3, 3, 0)): 0.2, # xd on normal keyboards (lower row shifted to the right)
    ((3, 3, 0), (2, 3, 0)): 0.2, # dx on normal keyboards (lower row shifted to the right)
    ((1, 1, 0), (3, 3, 0)): 0.2, # qx on normal keyboards (lower row shifted to the right)
    ((3, 3, 0), (1, 1, 0)): 0.2, # xq on normal keyboards (lower row shifted to the right)
    ((1, 1, 0), (3, 4, 0)): 0.1, # qc on normal keyboards (lower row shifted to the right)
    ((3, 4, 0), (1, 1, 0)): 0.1, # cq on normal keyboards (lower row shifted to the right)
    ## pinky lower to index upper and index upper to pinky lower (heavy stretch and screw of the hand)
    ((3, 11, 0), (1, 6, 0)): 0.1, # -y on normal keyboards (lower row shifted to the right)
    ((1, 6, 0), (3, 11, 0)): 0.1, # y- on normal keyboards (lower row shifted to the right)
    ((3, 2, 0), (1, 5, 0)): 0.1, # zt on normal keyboards (lower row shifted to the right)
    ((1, 5, 0), (3, 2, 0)): 0.1, # tz on normal keyboards (lower row shifted to the right)
    ## positive movements: pinky down and index down. This is the only bigramm where pinky down does not hurt.
    ((3, 2, 0), (3, 5, 0)): -0.01, # zv on normal keyboards (lower row shifted to the right)
    ((3, 5, 0), (3, 2, 0)): -0.01, # vz on normal keyboards (lower row shifted to the right)
    ((3, 8, 0), (3, 11, 0)): -0.01, # m- on normal keyboards (lower row shifted to the right)
    ((3, 11, 0), (3, 8, 0)): -0.01, # -m on normal keyboards (lower row shifted to the right)

    }
# all pinky repeats
for finger in ("Klein_L", "Klein_R"): 
    for pos0 in FINGER_POSITIONS[finger]:
        for pos1 in FINGER_POSITIONS[finger]:
            try: COST_MANUAL_BIGRAM_PENALTY[(pos0, pos1)] += 1
            except KeyError: COST_MANUAL_BIGRAM_PENALTY[(pos0, pos1)] = 1


# Irregularity. This counteracts tendencies of the optimizer to only cater to common bigrams.
# generated via: for i in beispieltext-p* Korpora/*utf8 Korpora/Gutenberg/*/*utf8 ; do echo $i; head -n 5000 $i > /tmp/ref ; pypy3.5-5.8-beta-linux_x86_64-portable/bin/pypy  ./textcheck.py /tmp/ref --best-lines >> beispieltext-regularity-best-multiple.txt; pypy3.5-5.8-beta-linux_x86_64-portable/bin/pypy ./textcheck.py /tmp/ref --worst-lines >> beispieltext-regularity-worst-multiple.txt; done
#                grep best: beispieltext-regularity-*-multiple.txt | sed 's/.*) //' | cut -c 1-270 | sed 's/ \w*$//' | sort -u > beispieltext-regularity-best-and-worst-uniq.txt
IRREGULARITY_REFERENCE_TEXT = "beispieltext-regularity-best-and-worst-uniq.txt"
# use only a randomly selected fraction of the words at each step. Random sampling ensures that there is no consistent bias due to the word selection. Using all words makes the optimization very slow. 0.01 still increases the cost by factor 2. Currently 0.004 are about 400 words.
IRREGULARITY_WORDS_RANDOMLY_SAMPLED_FRACTION = 1.0 # the fraction of words to use, re-sampled at every run. Set to 1.0 to use all words.
WEIGHT_IRREGULARITY_PER_LETTER = 10 # 1 is around 1% of the total cost. Set to 0 to disable irregularity checking.

# TODO: Cost for similar keys in symmetric positions. That’s bad *except* if the symmetry is consistent. (hard consonants always on one side or always above)
