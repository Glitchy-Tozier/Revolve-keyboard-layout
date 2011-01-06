#!/usr/bin/env python3
# encoding: utf-8

"""Configuration of check_neo, mainly the weights of the cost functions. Intended to be easily modified."""

#: The mutated letters - only these get changed. You may change these to leave letters in their defined place.
abc = "abcdefghijklmnopqrstuvwxyzäöüß,."

#The letters which are used to calculate the costs - do not change anything or results will become incomparable.
abc_full = "abcdefghijklmnopqrstuvwxyzäöüß,."

WEIGHT_POSITION = 10 #: reference cost - gets multiplied with the COST_PER_KEY.

WEIGHT_POSITION_QUADRATIC_BIGRAMS = 0.1 #:100 #: the product of the cost of the letters in a bigram, divided by the number of keystrokes. The numbers are about factor 50 below the position cost — consistently for text of different length.

WEIGHT_FINGER_REPEATS = 512 #: Cost of a finger repeat. Gets additional +1 from the row change on the same finger.

WEIGHT_FINGER_REPEATS_TOP_BOTTOM = 2048 #: Additional cost of a finger repetition from the top to the bottom line. Gets added to the cost of the normal finger repetition. Additionally this gets costs as row repetition on the same hand (+4). 

WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW = 6 #: When I have to switch the row in a bigram while on the same hand, that takes time => Penalty per (row to cross ² / horizontal distance)² if we’re on the same hand. 

WEIGHT_COUNT_ROW_CHANGES_BETWEEN_HANDS = False #: Should we count a row change with a handswitch as row change? 

WEIGHT_FINGER_DISBALANCE = 300 #: multiplied with the standard deviation of the finger usage - value guessed and only valid for the 1gramme.txt corpus. 

WEIGHT_HAND_DISBALANCE = 60 #: Disbalance between the load on the hands. Calculated from the finger disbalance, but coarser. If both hands have slightly unequal load on the individual fingers, but overall both hands have the same load, the layout feels equal.

WEIGHT_TOO_LITTLE_HANDSWITCHING = 300 #: how high should it be counted, if the hands aren’t switched in a triple?

WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE = 1 #: multipleir for triples without handswitch in which there also is a direction change? Also affects the “unweighted” result from total_cost!
WEIGHT_NO_HANDSWITCH_WITHOUT_DIRECTION_CHANGE = 0 #: multipier for triples without handswitch in which the direction doesn’t change. Also affects the “unweighted” result from total_cost!

WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM = 0.3 #: multiplier for the cost of secondary bigrams in trigrams. 

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

WEIGHT_XCVZ_ON_BAD_POSITION = 0.1 #: the penalty *per letter* in the text if xvcz are on bad positions (cumulative; if all 4 are on bad positions (not in the first 5 keys, counted from the left side horizontally) we get 4 times the penalty). 

WEIGHT_FINGER_SWITCH = 30 #: how much worse is it to switch from middle to indexfinger compared with middle to pinky (~30ms according to Rohmert).

#: The cost for moving from one finger to another one with middle-to-index as 1 (30ms). Currently only uses the neighbors. Can also be used to favor a certain direction. Adapted the Rohmert times as per my own experiences: http://lists.neo-layout.org/pipermail/diskussion/2010-May/017171.html and http://lists.neo-layout.org/pipermail/diskussion/2010-May/017321.html
FINGER_SWITCH_COST = { # iu td < ui dt dr ua rd au < ai rt < nd eu
    "Klein_L": {
        "Ring_L": 3,
        "Mittel_L": 2
        }, 
    "Ring_L": {
        "Klein_L": 4,
        "Mittel_L": 2
        }, 
    "Mittel_L": {
        "Ring_L": 3,
        "Klein_L": 2
        }, 
    "Zeige_L": {
        }, 
    "Daumen_L": {
        },
    "Daumen_R": {
        },
    "Zeige_R": {
        },
    "Mittel_R": {
        "Ring_R": 3,
        "Klein_R": 2
        },
    "Ring_R": {
        "Mittel_R": 2,
        "Klein_R": 4
        }, 
    "Klein_R": {
        "Ring_R": 3,
        "Mittel_R": 2
        }
} # iutd, drua, uidt, rdau, airt, ndeu :)

WEIGHT_NO_HANDSWITCH_AFTER_UNBALANCING_KEY = 20 #: How much penalty we want if there’s no handswitching after an unbalancing key. Heavy unbalancing (wkßz, M3 right, return and the shifts) counts double (see UNBALANCING_POSITIONS). This also gives a penalty for handswitching after an uppercase letter.

#: Positions which pull the hand from the base row, position and cost (the strength of the pulling from base row). 
UNBALANCING_POSITIONS = {
    (1, 0, 0): 2, # Tab
    (1, 1, 0): 1,# x
    (1, 5, 0): 2, # w
    (1, 6, 0): 2, # k
    (1, 10, 0): 1, # q
    (1, 11, 0): 2, # ß
    (2, 0, 0): 1, # L_M3
    (2, 5, 0): 1, # o
    (2, 6, 0): 1, # s
    (2, 11, 0): 1, # y
    (2, 12, 0): 2, # R_M3
    (2, 13, 0): 2, # Return
    (3, 0, 0): 2, # L_Shift
    (3, 12, 0): 2, # R_Shift
    (3, 6, 0): 2, # z
    (3, 7, 0): 1 # b
}

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
    [50,    40,35,30,30, 35,   40,35,30,30,30,35,40,50], # Zahlenreihe (0)
    [24,    20, 6, 4, 6, 9,    10, 6, 4, 5, 8,24,36, 0], # Reihe 1
    [5,      3, 3, 3, 3, 5,     5, 3, 3, 3, 3, 5,10,18], # Reihe 2
    [15,10, 12,24,20, 5,    30, 6, 5,22,22,10,      15],     # Reihe 3
    [0,0,0,               3           , 7, 0, 0, 0] # Reihe 4 mit Leertaste
]

COST_LAYER_ADDITION = [0, 15, 12, 10, 27, 22]

#: The cost of any key which isn’t on the keyboard. Should be higher than max(COST_LAYER_ADDITION) + the most expensive key + 2 * WEIGHT_FINGER_REPEATS * mods_on_same_hand_adjustment [local variable in split uppercase bigrams] to make sure that having a key on a bad position in layer 5 is better than not having it at all. Currently (eb0c9e8c8b02 + 1) that means, it must be higher than 27+50+16 = 93. Trial and error shows, it must be about 150 to make the addition of the neo layers to nordtast useful.
COST_PER_KEY_NOT_FOUND = 150



### config finished. Additional stuff which might need changing for different layouts or hand positions. 

#: The modifiers, sorted by layer, split into left and right, counting from 0.
MODIFIERS_PER_LAYER = [("", ""), ("⇧", "⇗"), ("⇩", "⇘"), ("⇚", "⇙"), ("⇩⇧", "⇘⇗"), ("⇩⇚", "⇘⇙")]

#: The positions which are by default accessed by the given finger. 
FINGER_POSITIONS = {
    "Klein_L": [(1, 1, 0), (2, 0, 0), (2, 1, 0), (3, 0, 0), (3, 1, 0), (3, 2, 0)], # Klein_L
    "Ring_L": [(1, 2, 0), (2, 2, 0), (3, 3, 0)], # Ring_L
    "Mittel_L": [(1, 3, 0), (2, 3, 0), (3, 4, 0)], # Mittel_L
    "Zeige_L": [(1, 4, 0), (2, 4, 0), (3, 5, 0), (1, 5, 0), (2, 5, 0), (3, 6, 0)], # Zeige_L
    "Daumen_L": [(4, 3, 0)], # Daumen_L
    "Daumen_R": [(4, 3, 0), (4, 4, 0)], # Daumen_R
    "Zeige_R": [(1, 6, 0), (2, 6, 0), (3, 7, 0), (1, 7, 0), (2, 7, 0), (3, 8, 0)], # Zeige_R
    "Mittel_R": [(1, 8, 0), (2, 8, 0), (3, 9, 0)], # Mittel_R
    "Ring_R": [(1, 9, 0), (2, 9, 0), (3, 10, 0)], # Ring_R
    "Klein_R": [(1, 10, 0), (2, 10, 0), (3, 11, 0), (1, 11, 0), (2, 11, 0), (1, 12, 0), (2, 12, 0), (2, 13, 0), (3, 12, 0)] # Klein_R
}

#: The lowest index for the right hand per line in the config (pos[0] is the line, pos[1] the index). TODO: Generate automatically from the finger positions.
RIGHT_HAND_LOWEST_INDEXES = [7, 6, 6, 7, 3]
