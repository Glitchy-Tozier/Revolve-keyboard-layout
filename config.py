#!/usr/bin/env python3

"""Configuration of check_neo, mainly the weights. Intended to be easily modified."""

# Gewichtung der unterschiedlichen Kosten
WEIGHT_POSITION = 1 #: reference

WEIGHT_FINGER_REPEATS = 32 #: higher than two switches from center to side, but lower than two switches from center to upper left.

WEIGHT_FINGER_REPEATS_TOP_BOTTOM = 64 #: 2 times a normal repeat, since it's really slow. Better two outside low or up than an up-down repeat. Additionally it gets repeated as row repetition on the same hand (+8)

WEIGHT_BIGRAM_ROW_CHANGE_PER_ROW = 2 #: When I have to switch the row in a bigram while on the same hand, that takes time => Penalty per row to cross if we’re on the same hand. 

WEIGHT_COUNT_ROW_CHANGES_BETWEEN_HANDS = False #: Should we count a row change with a handswitch as row change nontheless? 

WEIGHT_FINGER_DISBALANCE = 30 #: multiplied with the standard deviation of the finger usage - value guessed and only valid for the 1gramme.txt corus. 

WEIGHT_TOO_LITTLE_HANDSWITCHING = 1 #: how high should it be counted, if the hands aren’t switched in a triple?

WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE = 5 #: how much stronger should the triple without handswitch be counted, if there also is a direction change? Also affects the “unweighted” result from total_cost!

WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY = [
    1,
    2,
    2,
    2.6, # is 1/3 faster
    1,
    1,
    2.6,
    2,
    2,
    1] #: The intended load per finger. Inversed and then used as multiplier for the finger load before calculating the finger disbalance penalty. Any load distribution which strays from this optimum gives a penalty.

WEIGHT_XCVZ_ON_BAD_POSITION = 0.6 #: the penalty *per letter* in the text if xvcz are on bad positions (cumulative; if all 4 are on bad positions (not in the first 5 keys, counted from the left side horizontally) we get 4 times the penalty). 

WEIGHT_FINGER_SWITCH = 1 # how much worse is it to switch from middle to indexfinger compared with middle to pinky (~30ms according to Rohmert).
#: The cost for moving from one finger to the next. Adapted the Rohmert times as per my own experiences: http://lists.neo-layout.org/pipermail/diskussion/2010-May/017171.html and http://lists.neo-layout.org/pipermail/diskussion/2010-May/017321.html

FINGER_SWITCH_COST = {
    "Klein_L": {"Ring_L": 2}, # 100ms
    "Ring_L": {"Klein_L": 3,
               "Mittel_L": 5}, # 140ms
    "Mittel_L": {"Ring_L": 4,
                 "Zeige_L": 1}, # Nach Rohmert 230ms statt 200ms ⇒ 30ms
    "Zeige_L": {"Mittel_L": 4}, # 120ms
    "Daumen_L": {},
    "Daumen_R": {},
    "Zeige_R": {"Mittel_R": 4},
    "Mittel_R": {"Zeige_R": 1,
                 "Ring_R": 4},
    "Ring_R": {"Mittel_R": 5,
               "Klein_R": 3}, 
    "Klein_R": {"Ring_R": 2}
}



#: Die zu mutierenden Buchstaben.
abc = "abcdefghijklmnopqrstuvwxyzäöüß,."

# Structured key weighting (but still mostly from experience and deducing from the work of others).
# The speed of the fingers is taken out (see INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY).
# So this shows the reachability of the keys, ignoring the different speed of the fingers.
# “How much does the hand hurt when reaching for the key” :)
# rationale: reaching for the Neo2 x hurts thrice as much as just hitting the Neo2 u → 10 vs. 3.
# the upper keys on the right hand can be reached a bit better, since movement is aligned with the hand
# (except for q, since the pinky is too short for that).
# theoretical minimum (assigning the lowest cost to the most frequent char, counting only the chars on layer 1):
# 1123111113 = 3.3490913205386508 mean key position cost
# Ringfinger on lower row takes 1.5 times the time of index on the upper row[1].
# [1]: http://forschung.goebel-consult.de/de-ergo/rohmert/Rohmert.html - only one person!
COST_PER_KEY  = [ # the 0 values aren’t filled in at the moment. 
    [0,     0, 0, 0, 0, 0,     0, 0, 0, 0, 0,22, 0, 0], # Zahlenreihe (0)
    [0,    10, 6, 5, 6, 9,    10, 5, 4, 5, 8,12,18, 0], # Reihe 1
    [0,     3, 3, 3, 3, 5,     5, 3, 3, 3, 3, 5,10,18], # Reihe 2
    [15,10,12,12,10, 10,   15, 7, 6,11,11,10,   15],     # Reihe 3
    [0,0,0,               3           , 0, 0, 0, 0] # Reihe 4 mit Leertaste
]

# for reference the neo layout
NEO = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("-"),("`"),("←")], # Zahlenreihe (0)
    [("⇥"),("x"),("v"),("l"),("c"),("w"),("k"),("h"),("g"),("f"),("q"),("ß"),("´"),()], # Reihe 1
    [("⇩"),("u"),("i"),("a"),("e"),("o"),("s"),("n"),("r"),("t"),("d"),("y"),("⇘"),("\n")], # Reihe 2
    [("⇧"),(),("ü"),("ö"),("ä"),("p"),("z"),("b"),("m"),(","),("."),("j"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]
