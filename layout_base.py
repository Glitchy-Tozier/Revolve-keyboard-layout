#!/usr/bin/env python3
# encoding: utf-8

"""Basic functions and constants for working with keyboard layouts."""

from copy import deepcopy
from enum import Enum
from pprint import pprint

from config import COST_LAYER_ADDITION, COST_PER_KEY, COST_PER_KEY_NOT_FOUND, FINGER_POSITIONS, RIGHT_HAND_LOWEST_INDEXES

# get the config

# check if we got one via the commandline (and remove the argument if yes). Otherwise use the default.
from sys import argv
if "--config" in argv:
    idx = argv.index("--config")
    # the config module is the file without the extension.
    cfg = argv[idx+1][:-3]
    # replace all / and \ with .
    cfg = cfg.replace("/", ".")
    cfg = cfg.replace("\\", ".")
    argv = argv[:idx] + argv[idx+2:]
    exec("from " + cfg + " import *")
else:
    from config import ABC


# (Global) Constants

# TODO: Find out if the script ran faster if those variables were
#       "un-globalized" by moving them inside the Layout-class.


# Ulfs All fingers equal but the small one
COST_PER_KEY_OLD  = [ # 0 heißt nicht beachtet
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Row 0 (number row)
        [0,6,3,3,3,4,4,3,3,3,6,7,8,0], # Row 1
        [0,2,1,1,1,3,3,1,1,1,2,6,0,9], # Row 2 (home row)
        [0,4,5,5,5,5,7,7,5,5,5,5,0],   # Row 3
        [0,0,0,     9     ,0,0,0,0] # Row 4, containing the spacebar
]

# First reweighting
COST_PER_KEY_OLD2  = [ # 0 heißt nicht beachtet
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Row 0 (number row)
        [0,6,3,3,3,4,4,3,3,3,6,7,8,0], # Row 1
        [0,3,2,2,1,3,3,1,2,2,3,6,0,9], # Row 2 (home row)
        [0,5,5,5,5,5,7,7,5,5,5,5,0],   # Row 3
        [0,0,0,     9     ,0,0,0,0] # Row 4, containing the spacebar
]

#: The names of the fingers from left to right
FINGER_NAMES = ["Klein_L", "Ring_L", "Mittel_L", "Zeige_L", "Daumen_L",
                "Daumen_R", "Zeige_R", "Mittel_R", "Ring_R", "Klein_R"]

# A static field that contains the information which finger presses each layer-1 position (x, y, 0)
POS_TO_FINGER = {}
for finger, positions in FINGER_POSITIONS.items():
    for pos in positions:
        POS_TO_FINGER[pos] = finger

# Constants for testing

# Weighting for the tests — DON’T CHANGE THIS, it’s necessary for correct testing
TEST_COST_PER_KEY  = [ # 0 heißt nicht beachtet
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Row 0 (number row)
    [0, 12,9,6,4,10,10,4,6,9,12,15,18,0],  # Row 1
    [0,  5,3,3,2,5,5,2,3,3,5,12,0,15],     # Row 2 (home row)
    [15,0,10,11,11,7,12,10,7,11,11,10,15], # Row 3
    [0,0,0,     5     ,0,0,0,0] # Row 4, containing the spacebar
]

# Gewichtung der unterschiedlichen Kosten
# : higher than a switch from center to side, but lower than a switch from center to upper left.
TEST_WEIGHT_FINGER_REPEATS = 8
# : 2 times a normal repeat, since it's really slow. Better two outside low or up than an up-down repeat.
TEST_WEIGHT_FINGER_REPEATS_TOP_BOTTOM = 16
TEST_WEIGHT_POSITION = 1  # : reference
# : multiplied with the standard deviation of the finger usage - value guessed and only valid for the 1gramme.txt corpus.
TEST_WEIGHT_FINGER_DISBALANCE = 5
# : how high should it be counted, if the hands aren’t switched in a triple?
TEST_WEIGHT_TOO_LITTLE_HANDSWITCHING = 1
TEST_WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY = [
    0.5,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    0.5]  # : The intended load per finger. Inversed and then used as multiplier for the finger load before calculating the finger disbalance penalty. Any load distribution which strays from this optimum gives a penalty.

TEST_FINGER_SWITCH_COST = {  # iu td < ui dt dr ua rd au < ai rt < nd eu
    "Klein_L": {
        "Ring_L": 3,
        "Mittel_L": 3
    },
    "Ring_L": {
        "Klein_L": 4,
        "Mittel_L": 3
    },
    "Mittel_L": {
        "Klein_L": 1,
        "Ring_L": 2
    },
    "Zeige_L": {
        "Klein_L": 1
    },
    "Daumen_L": {
    },
    "Daumen_R": {
    },
    "Zeige_R": {
        "Klein_R": 1
    },
    "Mittel_R": {
        "Ring_R": 2,
        "Klein_R": 1
    },
    "Ring_R": {
        "Mittel_R": 3,
        "Klein_R": 4
    },
    "Klein_R": {
        "Mittel_R": 3,
        "Ring_R": 3
    }
}  # iutd, drua, uidt, rdau, airt, ndeu :)

# : multiplier for the cost of secondary bigrams in trigrams.
TEST_WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM = 0.5


# Random functions

def find_layout_families(layouts: list, letters, max_diff=0.2) -> list:
    """Find layout families in a list of layouts using the difference in key-positions, weighted by the occurrance probability of each key.

    >>> from ngrams import get_all_data
    >>> letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data()
    >>> len(find_layout_families([Layouts.NEO2, Layouts.NEO2_lx, Layouts.NEO2_lxwq, Layouts.QWERTZ, Layouts.NORDTAST], letters=letters, max_diff=0.1))
    3
    >>> len(find_layout_families([Layouts.NEO2, Layouts.NEO2_lx, Layouts.NEO2_lxwq, Layouts.QWERTZ, Layouts.NORDTAST], letters=letters, max_diff=0.9))
    1
    """
    families = []
    letter_dict = {letter: num for num, letter in letters}
    sum_keystrokes = sum(letter_dict.values())
    for l in layouts:
        fits = False
        for f in families:
            if l.difference_weighted(f[0], letter_dict=letter_dict, sum_keystrokes=sum_keystrokes) <= max_diff:
                fits = True
        if not fits:
            families.append([])
            families[-1].append(l)

    return families


def _is_position_cost_lower(old_pos: tuple, new_pos: tuple, doubled_layer=True):
    """
    >>> is_position_cost_lower((2, 10, 2), (3, 7, 3), Layouts.NEO2))
    False
    """
    # use tripled layer cost, because it ignores the additional bigrams.
    new_cost = single_key_position_cost(
        new_pos) + 2*COST_LAYER_ADDITION[new_pos[2]]
    cost = single_key_position_cost(
        old_pos) + 2*COST_LAYER_ADDITION[old_pos[2]]
    return new_cost < cost


def single_key_position_cost(pos: tuple, cost_per_key=COST_PER_KEY):
    """Get the position_cost of a single key.

    @param pos: The position of the key.
    @type pos: tuple (row, col, layer).
    @return: the cost of that one position."""
    if pos is None:  # not found
        return COST_PER_KEY_NOT_FOUND
    # shift, M3 and M4
    if COST_LAYER_ADDITION[pos[2]:]:
        return cost_per_key[pos[0]][pos[1]] + COST_LAYER_ADDITION[pos[2]]
    # layer has no addition cost ⇒ undefined layer (higher than layer 6!). Just take the base key…
    return cost_per_key[pos[0]][pos[1]]


def mirror_position_horizontally(pos: tuple) -> tuple:
    """Mirror a position horizontally: (2, 1, 0) → (2, 10, 0)

    >>> m = mirror_position_horizontally
    >>> m((0,0,0))
    (0, 13, 0)
    >>> m((0,13,0))
    (0, 0, 0)
    >>> m((0,1,0))
    (0, 12, 0)
    >>> m((0,9,0))
    (0, 4, 0)
    >>> m((0,4,0))
    (0, 9, 0)
    >>> m((0,6,0))
    (0, 7, 0)
    >>> m((0,7,0))
    (0, 6, 0)
    >>> m((1,0,0))
    (1, 11, 0)
    >>> m((1,1,0))
    (1, 10, 0)
    >>> m((1,11,0))
    (1, 0, 0)
    >>> m((1,12,0))
    (1, 0, 0)
    >>> m((2,13,0))
    (2, 0, 0)
    >>> m((2,4,0))
    (2, 7, 0)
    >>> m((2,6,0))
    (2, 5, 0)
    >>> m((3,7,0))
    (3, 6, 0)
    >>> m(None)
    """
    if not pos:
        return None
    if pos[0] == 2:
        return pos[0], max(0, 6 + (-1)*(pos[1] - 5)), pos[2]
    if pos[0] == 1:
        return pos[0], max(0, 6 + (-1)*(pos[1] - 5)), pos[2]
    if pos[0] == 3:
        return pos[0], min(12, 7 + (-1)*(pos[1] - 6)), pos[2]
    if pos[0] == 0:
        return pos[0], 7 + (-1)*(pos[1] - 6), pos[2]
    if pos[0] == 4:
        if pos[1] == 3:
            return pos  # no change
        if pos[1] == 0:
            p1 = 7
        elif pos[1] == 1:
            p1 = 5
        elif pos[1] == 2:
            p1 = 4
        elif pos[1] == 4:
            p1 = 2
        elif pos[1] == 5:
            p1 = 1
        elif pos[1] == 6:
            p1 = 0
        elif pos[1] == 7:
            p1 = 0
        else:
            p1 = pos[1]
        return pos[0], p1, pos[2]
    else:
        raise Exception("Position value out of bounds")


# The Layout-Class


class Layout():
    """The data-structure of a layout.

    Create by using the default-constructor and passing in a list that resembles the layout-lists found in layout_basee.py. (Example: Layouts.NEO2)
        l = Layouts.NEO2)

    Alternatively, create the layout from a layout-string via the static method `.from_string()`
        l = Layout.from_string(layout_string, Layouts.NEO2)

    This class also caches the most often requested information (What position is "a" on?) and
    provides methods to access this information.
    """

    ### Table of contents: ###
    # 1. Constructors
    # 2. Methods
    # 3. Static constant fields

    # Non-static fields:

    # self.all_chars = []
    # self.blueprint = []
    # self._char_finger_dict = {}
    # self._char_pos_dict = {}
    # self._pos_is_left_dict = {}
    # self._pos_char_dict = {}

    ### Constructors ###

    def __init__(self, blueprint):
        self.blueprint = blueprint

        self._char_finger_dict = {}
        self._char_pos_dict = {}
        self._pos_is_left_dict = {}
        self._pos_char_dict = {}

        for row_idx, row in enumerate(blueprint):
            # Only used to fill up self._pos_is_left_dict:
            lowest_right_hand_idx = RIGHT_HAND_LOWEST_INDEXES[row_idx]

            for key_idx, key in enumerate(row):
                for layer_idx, char in enumerate(key):
                    pos = (row_idx, key_idx, layer_idx)

                    if char not in self._char_finger_dict:
                        # Fill up _char_finger_dict
                        self._char_finger_dict[char] = POS_TO_FINGER[row_idx, key_idx, 0]

                        # Fill up _char_pos_dict
                        self._char_pos_dict[char] = pos
                    elif _is_position_cost_lower(self._char_pos_dict[char], pos):
                        # Fill up _char_finger_dict
                        self._char_finger_dict[char] = POS_TO_FINGER[row_idx, key_idx, 0]

                        # Fill up _char_pos_dict
                        self._char_pos_dict[char] = pos

                    # Fill up _pos_is_left_dict
                    self._pos_is_left_dict[pos] = lowest_right_hand_idx > key_idx

                    # Fill up _pos_char_dict
                    self._pos_char_dict[pos] = char

    @ classmethod
    def from_string(self, layout_string, base_layout):
        """Turn a layout_string into a layout. This is the alternative constructor for the Layout-class.
            öckäy zhmlß,´
            atieo dsnru.
            xpfüq bgvwj
        """
        # TODO: This method still is REALLY weird and performs unneccessary computations. Make it less ugly.
        base_blueprint = base_layout.blueprint

        def set_key(current_key, new_letter, pos_01, layout, base_blueprint=base_blueprint, changing_layers=[0, 1, 4, 5]):
            """Set the new_letter into the pos_01 in the layout. Take the key from the position in the base_layout and from the position in the letter and merge them, using layer 3,4 from the position and the rest from the letter.
            @param pos_01: the key which is currently in the given position. Not needed anymore, except for debugging.
            @param current_key: The key which is currently in the position. Not needed anymore, except for debugging.
            @param new_letter: The letter which should be in the position.
            @param pos_01: The position where the key should be placed.
            @param changing_layers: The layers in the base layout which change when the keys get changed."""
            # first get the keys for all layers from position in the base_layout
            base_keys = base_blueprint[pos_01[0]][pos_01[1]]
            # then get the keys corresponding to the position of the new letter.
            letter_pos = layout.char_to_pos(new_letter)
            if letter_pos is None or letter_pos[2]:
                # the new letter is not in the base_layout or not in the base layer, just set it on layer 0.
                layout.blueprint[pos_01[0]][pos_01[1]] = (
                    new_letter, ) + tuple(base_keys[1:])
                return Layout(layout.blueprint)

            letter_keys = base_blueprint[letter_pos[0]][letter_pos[1]]
            # replace all changing_layers in the base_keys with the new_keys.
            tmp = []
            for i in range(6):
                try:
                    if i in changing_layers:
                        tmp.append(letter_keys[i])
                    else:
                        tmp.append(base_keys[i])
                except IndexError:  # key not found
                    tmp.append("")
            layout.blueprint[pos_01[0]][pos_01[1]] = tuple(tmp)
            return Layout(layout.blueprint)

        layout = deepcopy(base_layout)
        lines = layout_string.splitlines()
        # first and second letter row
        for i in range(1, 6):
            layout = set_key(
                layout.blueprint[1][i][0], lines[0][i-1], (1, i), layout)
            layout = set_key(
                layout.blueprint[1][i+5][0], lines[0][i+5], (1, i+5), layout)
            layout = set_key(
                layout.blueprint[2][i][0], lines[1][i-1], (2, i), layout)
            layout = set_key(
                layout.blueprint[2][i+5][0], lines[1][i+5], (2, i+5), layout)

        layout = set_key(layout.blueprint[1][-3]
                         [0], lines[0][11], (1, -3), layout)
        layout = set_key(layout.blueprint[2][-3]
                         [0], lines[1][11], (2, -3), layout)

        # third row
        if lines[0][12:]:
            layout = set_key(
                layout.blueprint[1][-2][0], lines[0][12], (1, -2), layout)

        try:
            left, right = lines[2].split()[:2]
        except ValueError:
            print(lines)
            raise
        for i in range(len(left)):
            layout = set_key(
                layout.blueprint[3][6-i][0], left[-i-1], (3, 6-i), layout)
        for i in range(len(right)):
            layout = set_key(
                layout.blueprint[3][7+i][0], right[i], (3, 7+i), layout)

        return layout

    ### Methods ###

    def get_all_chars(self) -> list:  # get_all_keys_in_layout
        """Get all keys which are in the layout. Sorted the same way as the positions from get_all_positions().

        >>> Layouts.TEST_LAYOUT.get_all_chars()
        ['^', 'ˇ', '↻', '⇥', 'u', 'U', '\\\\', '⇱', '⊂', '\\n', ' ', '⇙']
        """
        chars = []
        for row in self.blueprint:
            for key in row:
                for char in key:
                    if char:
                        chars.append(char)
        return chars

    def char_to_finger(self, char: str) -> str:  # key_to_finger
        """Get the finger name used to hit the given key.

        >>> char_to_finger("a")
        'Mittel_L'
        >>> char_to_finger("A")
        'Mittel_L'
        >>> char_to_finger("«")
        'Zeige_L'
        >>> char_to_finger("ĝ")
        ''
        >>> char_to_finger("⇩")
        'Klein_L'
        >>> char_to_finger("⇧")
        'Klein_L'
        """
        return self._char_finger_dict.setdefault(char, "")

    def char_to_pos(self, char: str) -> tuple:  # find_key
        """Find the position of the key in the layout.

        The result is a tuple which is structured as follows:
        (
            row_nr,  # top to botton, including the number-row
            key_nr,  # left to right
            layer_nr
        )
            >>> layout = Layouts.QWERTZ  # Examples with QWERTZ
            >>> layout.char_to_pos("A")
            (2, 1, 1)
            >>> layout.char_to_pos("a")
            (2, 1, 0)
            >>> layout = Layouts.NEO2)  # Examples with NEO2
            >>> layout.char_to_pos("a")
            (2, 3, 0)
            >>> layout.char_to_pos("A")
            (2, 3, 1)
            >>> layout.char_to_pos("e")
            (2, 4, 0)
            >>> layout.char_to_pos("impossiblInput")
            None
            >>> layout.char_to_pos(",")
            (3, 9, 0)
            >>> layout.char_to_pos(".")
            (3, 10, 0)
            >>> layout.char_to_pos(":")
            (2, 10, 2)
            >>> layout.char_to_pos('#')
            (3, 2, 2)
            >>> layout.char_to_pos("⇧")
            (3, 0, 0)
            >>> layout.char_to_pos("£")
            (0, 6, 3)
            >>> layout.char_to_pos("»")
            (0, 4, 1)
            >>> layout.char_to_pos("«")
            (0, 5, 1)
            >>> layout.char_to_pos("¤")
            (0, 7, 3)
        """
        return self._char_pos_dict.setdefault(char)

    def pos_is_left(self, pos: tuple) -> bool:  # pos_is_left
        """Check if the given position is on the left hand.

        The position-parameter should be a tuple structured as follows:
        (
            row_nr,  # top to botton, including the number-row
            key_nr,  # left to right
            layer_nr
        )
        """
        return self._pos_is_left_dict[pos]

    def pos_to_char(self, pos: tuple) -> str:  # get_key
        """Get the character at the given position.

        >>> layout.pos_to_char((2, 3, 0))
        'a'

        The position-parameter should be a tuple structured as follows:
        (
            row_nr,  # top to botton, including the number-row
            key_nr,  # left to right
            layer_nr
        )
        """
        return self.blueprint[pos[0]][pos[1]][pos[2]]

    def to_layer_1_string(self) -> str:
        """Create a string that represents the first layer of this layout:

        öckäy zhmlß,´
        atieo dsnru.
        xpfüq bgvwj
        """
        l = ""
        l += "".join((i[0] for i in self.blueprint[1][1:6])) + " " + "".join((i[0] for i in self.blueprint[1][6:-1])) + "\n"
        l += "".join((i[0] for i in self.blueprint[2][1:6])) + " " + "".join((i[0] for i in self.blueprint[2][6:-2])) + "\n"
        if self.blueprint[3][1] and self.blueprint[3][1][0] != "⇚":
            l += "".join((i[0] for i in self.blueprint[3][1:7])) + " " + "".join((i[0] for i in self.blueprint[3][7:-1]))
        else:
            l += "".join((i[0] for i in self.blueprint[3][2:7])) + " " + "".join((i[0] for i in self.blueprint[3][7:-1]))
        return l

    def get_all_positions(self):
        """Get all positions for which there are keys in the layout.

        >>> Layouts.TEST_LAYOUT.get_all_positions()
        [(0, 0, 0), (0, 0, 1), (0, 0, 2), (1, 0, 0), (2, 0, 0), (2, 0, 1),
        (2, 0, 2), (2, 0, 3), (2, 0, 5), (2, 1, 0), (4, 3, 0), (4, 4, 0)]
        """
        positions = []
        for row_idx in range(len(self.blueprint)):
            for key_idx in range(len(self.blueprint[row_idx])):
                for letter_idx in range(len(self.blueprint[row_idx][key_idx])):
                    if self.blueprint[row_idx][key_idx][letter_idx]:
                        positions.append((row_idx, key_idx, letter_idx))
        return positions

    def switch_positions(self, pos0: tuple, pos1: tuple):
        """Switch two positions in the layout.

        >>> from layout_base import Layout, Layouts
        >>> lay = Layouts.NEO2
        >>> lay = lay.switch_positions((1, 1, 0), (1, 3, 0), lay)
        >>> lay = lay.switch_positions((1, 1, 1), (1, 3, 1), lay)
        >>> lay == NEO_LAYOUT_lx
        True
        >>> print(lay[1][1])
        ('l', 'L', '…', '⇞', 'ξ', 'Ξ')
        >>> print(lay[1][3])
        ('x', 'X', '[', '⇡', 'λ', 'Λ')
        >>> lay = lay.switch_positions((1, 1, 0), (1, 1, 1), lay)
        >>> print(lay[1][1])
        ('L', 'l', '…', '⇞', 'ξ', 'Ξ')
        >>> lay.char_to_pos("l")
        (1, 1, 1)
        """
        blueprint = deepcopy(self.blueprint)
        pos0_keys = blueprint[pos0[0]][pos0[1]]
        pos1_keys = blueprint[pos1[0]][pos1[1]]

        # if they are on the same physical key, just exchange both positions on the single key
        if pos0[:2] == pos1[:2]:
            tmp = list(pos0_keys)
            tmp[pos0[2]] = pos1_keys[pos1[2]]
            tmp[pos1[2]] = pos0_keys[pos0[2]]
            tmp = tuple(tmp)

            cache_update = "".join(tmp)
            blueprint[pos0[0]][pos0[1]] = tmp
            return Layout(blueprint)

        # generate new tuples for all layers, with tmp0 containing pos1 and tmp1 containing pos0
        tmp0 = list(pos0_keys)
        tmp0[pos0[2]] = pos1_keys[pos1[2]]
        tmp0 = tuple(tmp0)

        tmp1 = list(pos1_keys)
        tmp1[pos1[2]] = pos0_keys[pos0[2]]
        tmp1 = tuple(tmp1)

        cache_update = ""
        for letter in tmp0 + tmp1:
            cache_update += letter

        blueprint[pos0[0]][pos0[1]] = tmp0
        blueprint[pos1[0]][pos1[1]] = tmp1
        return Layout(blueprint)

    def switch_keys(self, keypairs: list, switch_layers=[0, 1, 4, 5]):
        """Switch keys in the layout, so we don't have to fiddle with actual layout files.

        @param keypairs: A list of keypairs to switch. The keys in these pairs MUST be the base layer keys.

        >>> layout, switched_letters = switch_keys([], layout = Layouts.NEO2))
        >>> layout.blueprint == Layouts.NEO2
        True
        >>> layout, switched_letters = switch_keys(["lx", "wq"], layout = Layouts.NEO2), switch_layers=[0,1])
        >>> layout.pos_to_char((1, 1, 0))
        'l'
        >>> layout.pos_to_char((1, 3, 0))
        'x'
        >>> layout.pos_to_char((1, 5, 0))
        'q'
        >>> layout.pos_to_char((1, 10, 0))
        'w'
        >>> layout.pos_to_char((1, 1, 1))
        'L'
        >>> layout.pos_to_char((1, 3, 1))
        'X'
        >>> layout.pos_to_char((1, 5, 1))
        'Q'
        >>> layout.pos_to_char((1, 10, 1))
        'W'
        >>> layout.char_to_pos("l") == (1, 1, 0)
        True
        >>> layout.char_to_pos("L") == (1, 1, 1)
        True
        >>> Layouts.NEO_lxwq == layout.blueprint
        True
        >>> layout, switched_letters = switch_keys(["lx"], layout = Layouts.NEO2), switch_layers=[0,1])
        >>> Layouts.NEO_lx == layout
        True
        >>> a = layout.char_to_pos("a")
        >>> A = layout.char_to_pos("A")
        >>> curly = layout.char_to_pos("{")
        >>> layout, switched_letters = switch_keys(["ae"], layout=layout, switch_layers = [0,1,2])
        >>> a == layout.char_to_pos("e")
        True
        >>> A == layout.char_to_pos("E")
        True
        >>> curly == layout.char_to_pos("}")
        True
        >>> "}" == layout.pos_to_char(layout.char_to_pos("}"))
        True
        >>> dot = layout.char_to_pos(".")
        >>> d = layout.char_to_pos("d")
        >>> comma = layout.char_to_pos(",")
        >>> p = layout.char_to_pos("p")
        >>> layout, switched_letters = switch_keys([".d", ",p"], layout=Layouts.NEO2))
        >>> d == layout.char_to_pos(".")
        True
        >>> dot == layout.char_to_pos("d")
        True
        >>> p == layout.char_to_pos(",")
        True
        >>> comma == layout.char_to_pos("p")
        True
        """
        blueprint = deepcopy(self.blueprint)

        switched_letters = set()

        for pair in keypairs:
            pos0 = self.char_to_pos(pair[0])
            pos1 = self.char_to_pos(pair[1])

            # both positions MUST be on the base layer.
            if pos0[2] or pos1[2]:
                # info("one of the keys isn’t on the base layer. Ignoring the switch", pair)
                continue

            pos0_keys = blueprint[pos0[0]][pos0[1]]
            pos1_keys = blueprint[pos1[0]][pos1[1]]

            # add the supported layers.
            tmp0 = []
            for i in range(max(len(pos1_keys), len(pos0_keys))):
                if i in switch_layers:
                    try:
                        letter = pos1_keys[i]
                        tmp0.append(letter)
                        if letter not in switched_letters and letter != "":
                            switched_letters.add(letter)
                    except IndexError:  # not there: Fill the layer.
                        tmp0.append("")
                else:
                    try:
                        tmp0.append(pos0_keys[i])
                    except IndexError:  # not there: Fill the layer.
                        tmp0.append("")
            tmp0 = tuple(tmp0)

            tmp1 = []
            for i in range(max(len(pos1_keys), len(pos0_keys))):
                if i in switch_layers:
                    try:
                        letter = pos0_keys[i]
                        tmp1.append(letter)
                        if letter not in switched_letters and letter != "":
                            switched_letters.add(letter)
                    except IndexError:  # not there: Fill the layer.
                        tmp1.append("")
                else:
                    try:
                        tmp1.append(pos1_keys[i])
                    except IndexError:  # not there: Fill the layer.
                        tmp1.append("")
            tmp1 = tuple(tmp1)

            cache_update = ""
            for letter in tmp0 + tmp1:
                cache_update += letter

            blueprint[pos0[0]][pos0[1]] = tmp0
            blueprint[pos1[0]][pos1[1]] = tmp1

        layout = Layout(blueprint)
        return layout, switched_letters

    def find_changed_keys(self, layout1) -> list:
        """Find the keys which are in different positions in the two layouts.

        >>> Layouts.NEO2.find_changed_keys(Layouts.NEO_LX))
        ['L', 'X', 'l', 'x']
        >>> from check_neo import switch_keys
        >>> t = Layouts.TEST_LAYOUT.switch_keys(["u\\n"], switch_layers=[0,1])
        >>> Layouts.TEST_LAYOUT.find_changed_keys(t)
        ['\\n', 'U', 'u']
        """
        cache0 = self._char_pos_dict
        cache1 = layout1._char_to_pos_dict
        # TODO: Rewrite this insane line in a more understandable way
        return sorted([l for l in cache0 if not l in cache1 or cache0[l] != cache1[l]] + [l for l in cache1 if not l in cache0])

    def difference_weighted(self, layout2, letters=None, letter_dict=None, sum_keystrokes=None) -> float:
        """Find the difference between two layouts, weighted with the number of times the differing letters are used in the corpus.

        This only gives 1.0, if one layout contains all letters from the corpus and the other layout has none of them (or all of them in different positions).

        >>> from ngrams import get_all_data
        >>> letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data()
        >>> Layouts.NEO2.difference_weighted(letters=letters)
        0.0
        """
        # disabled tests
        """>>> Layouts.NEO2.difference_weighted(Layouts.NEO_lx, letters=letters)
        0.036617925978240665
        >>> Layouts.NEO2.difference_weighted(Layouts.NEO_lxwq, letters=letters)
        0.050589766759669606
        >>> Layouts.NEO2.difference_weighted(Layouts.QWERTZ, letters=letters)
        0.9486182821801175
        >>> Layouts.NEO2.difference_weighted(Layouts.NORDTAST, letters=letters)
        0.8830111461330287
        >>> difference_weighted(Layouts.NORDTAST, Layouts.QWERTZ, letters=letters)
        0.8983918828764104
        >>> Layouts.NEO2.difference_weighted(Layouts.TEST_LAYOUT, letters=letters)
        0.9999201678764246
        >>> empty = [[], [], [], [], []]
        >>> Layouts.NEO2.difference_weighted(empty, letters=letters)
        0.9999202512375004
        """
        if letter_dict is None and letters is None:
            raise Exception("Need letters or a letter dict")
        elif letter_dict is None:
            letter_dict = {letter: num for num, letter in letters}
        if sum_keystrokes is None:
            sum_keystrokes = sum(letter_dict.values())
        return sum([letter_dict.get(key, 0) for key in self.find_changed_keys(layout2)])/sum_keystrokes

    def combine_genetically(self, layout2):
        """Combine two layouts genetically (randomly)."""
        from random import randint
        switchlist = []
        for letter in ABC:
            if randint(0, 1) == 1:
                pos = self.char_to_pos(letter)
                replacement = layout2.pos_to_char(pos)
                switchlist.append(letter+replacement)
        res = self.switch_keys(switchlist)
        return res

    ### Static constant fields ###


class Layouts:
    """Presets for the most popular layouts."""

    #: Die Layout-Datei für Neo = Tastenbelegung - Großbuchstaben integriert.
    NEO2 = Layout([[("^", "ˇ", "↻", "˙", "˞", ""),
                    ("1", "°", "¹", "ª", "₁", "¬"),
                    ("2", "§", "²", "º", "₂", "∨"),
                    ("3", "ℓ", "³", "№", "₃", "∧"),
                    ("4", "»", "›", "", "♀", "⊥"),
                    ("5", "«", "‹", "·", "♂", "∡"),
                    ("6", "$", "¢", "£", "⚥", "∥"),
                    ("7", "€", "¥", "¤", "ϰ", "→"),
                    ("8", "„", "‚", "⇥", "⟨", "∞"),
                    ("9", "“", "‘", " /", "⟩", "∝"),
                    ("0", "”", "’", "*", "₀", "∅"),
                    ("-", "—", "-", "‑", "­"),
                    ("`", "¸", "°", "¨", "", "¯"),
                    ("←")],  # Row 0 (number row)

                   [("⇥"),
                    ("x", "X", "…", "⇞", "ξ", "Ξ"),
                    ("v", "V", "_", "⌫", "", "√"),
                    ("l", "L", "[", "⇡", "λ", "Λ"),
                    ("c", "C", "]", "Entf", "χ", "ℂ"),
                    ("w", "W", "^", "⇟", "ω", "Ω"),
                    ("k", "K", "!", "¡", "κ", "×"),
                    ("h", "H", "<", "7", "ψ", "Ψ"),
                    ("g", "G", ">", "8", "γ", "Γ"),
                    ("f", "F", "=", "9", "φ", "Φ"),
                    ("q", "Q", "&", "+", "ϕ", "ℚ"),
                    ("y", "Y", "@", ".", "υ", "∇"),
                    ("ß", "ẞ", "ſ", "−", "ς", "∘"),
                    ()],  # Row 1

                   [("⇩"),
                    ("u", "U", "\\", "⇱", "", "⊂"),
                    ("i", "I", "/", "⇠", "ι", "∫"),
                    ("a", "A", "{",  "⇣", "α", "∀"),
                    ("e", "E", "}", "⇢", "ε", "∃"),
                    ("o", "O", "*", "⇲", "ο", "∈"),
                    ("s", "S", "?", "¿", "σ", "Σ"),
                    ("n", "N", "(", "4", "ν", "ℕ"),
                    ("r", "R", ")", "5", "ρ", "ℝ"),
                    ("t", "T", "-", "6", "τ", "∂"),
                    ("d", "D", ":", ",", "δ", "Δ"),
                    ("⇘"),
                    ("´", "~", "/", "˝", "", "˘"),
                    ("\n")],  # Row 2 (home row)

                   [("⇧"),
                    ("⇚"),
                    ("ü", "Ü", "#", "", "", "∪"),
                    ("ö", "Ö", "$", "", "ϵ", "∩"),
                    ("ä", "Ä", "|", "⎀", "η", "ℵ"),
                    ("p", "P", "~", "\n", "π", "Π"),
                    ("z", "Z", "`", "↶", "ζ", "ℤ"),
                    ("b", "B", "+", ":", "β", "⇐"),
                    ("m", "M", "%", "1", "μ", "⇔"),
                    (",", "–", '"', "2", "ϱ", "⇒"),
                    (".", "•", "'", "3", "ϑ", "↦"),
                    ("j", "J", ";", ";", "θ", "Θ"),
                    ("⇗")],  # Row 3

                  [("♕"), (), ("♔"), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ("♛")]])  # Row 4, containing the spacebar

    # just switch layer 0 and 1
    NEO_LX = Layout([[("^", "ˇ", "↻", "˙", "˞", "",),
                     ("1", "°", "¹", "ª", "₁", "¬"),
                     ("2", "§", "²", "º", "₂", "∨"),
                     ("3", "ℓ", "³", "№", "₃", "∧"),
                     ("4", "»", "›", "", "♀", "⊥"),
                     ("5", "«", "‹", "·", "♂", "∡"),
                     ("6", "$", "¢", "£", "⚥", "∥"),
                     ("7", "€", "¥", "¤", "ϰ", "→"),
                     ("8", "„", "‚", "⇥", "⟨", "∞"),
                     ("9", "“", "‘", " /", "⟩", "∝"),
                     ("0", "”", "’", "*", "₀", "∅"),
                     ("-", "—", "-", "‑", "­"),
                     ("`", "¸", "°", "¨", "", "¯"),
                     ("←")],  # Row 0 (number row)

                    [("⇥"),
                     ("l", "L", "…", "⇞", "ξ", "Ξ"),
                     ("v", "V", "_", "⌫", "", "√"),
                     ("x", "X", "[", "⇡", "λ", "Λ"),
                     ("c", "C", "]", "Entf", "χ", "ℂ"),
                     ("w", "W", "^", "⇟", "ω", "Ω"),
                     ("k", "K", "!", "¡", "κ", "×"),
                     ("h", "H", "<", "7", "ψ", "Ψ"),
                     ("g", "G", ">", "8", "γ", "Γ"),
                     ("f", "F", "=", "9", "φ", "Φ"),
                     ("q", "Q", "&", "+", "ϕ", "ℚ"),
                     ("y", "Y", "@", ".", "υ", "∇"),
                     ("ß", "ẞ", "ſ", "−", "ς", "∘"),
                     ()],  # Row 1

                    [("⇩"),
                     ("u", "U", "\\", "⇱", "", "⊂"),
                     ("i", "I", "/", "⇠", "ι", "∫"),
                     ("a", "A", "{", "⇣", "α", "∀"),
                     ("e", "E", "}", "⇢", "ε", "∃"),
                     ("o", "O", "*", "⇲", "ο", "∈"),
                     ("s", "S", "?", "¿", "σ", "Σ"),
                     ("n", "N", "(", "4", "ν", "ℕ"),
                     ("r", "R", ")", "5", "ρ", "ℝ"),
                     ("t", "T", "-", "6", "τ", "∂"),
                     ("d", "D", ":", ",", "δ", "Δ"),
                     ("⇘"),
                     ("´", "~", "/", "˝", "", "˘"),
                     ("\n")],  # Row 2 (home row)

                    [("⇧"),
                     ("⇚"),
                     ("ü", "Ü", "#", "", "", "∪"),
                     ("ö", "Ö", "$", "", "ϵ", "∩"),
                     ("ä", "Ä", "|", "⎀", "η", "ℵ"),
                     ("p", "P", "~", "\n", "π", "Π"),
                     ("z", "Z", "`", "↶", "ζ", "ℤ"),
                     ("b", "B", "+", ":", "β", "⇐"),
                     ("m", "M", "%", "1", "μ", "⇔"),
                     (",", "–", '"', "2", "ϱ", "⇒"),
                     (".", "•", "'", "3", "ϑ", "↦"),
                     ("j", "J", ";", ";", "θ", "Θ"),
                     ("⇗")],  # Row  3

                    [("♕"), (), ("♔"), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ("♛")]])  # Row 4, containing the spacebar
                     
    NEO_LXWQ = Layout([[("^", "ˇ", "↻", "˙", "˞", "̣"),
                        ("1", "°", "¹", "ª", "₁", "¬"),
                        ("2", "§", "²", "º", "₂", "∨"),
                        ("3", "ℓ", "³", "№", "₃", "∧"),
                        ("4", "»", "›", "", "♀", "⊥"),
                        ("5", "«", "‹", "·", "♂", "∡"),
                        ("6", "$", "¢", "£", "⚥", "∥"),
                        ("7", "€", "¥", "¤", "ϰ", "→"),
                        ("8", "„", "‚", "⇥", "⟨", "∞"),
                        ("9", "“", "‘", " /", "⟩", "∝"),
                        ("0", "”", "’", "*", "₀", "∅"),
                        ("-", "—", "-", "‑", "­"),
                        ("`", "¸", "°", "¨", "", "¯"),
                        ("←")],  # Row 0 (number row)

                       [("⇥"),
                        ("l", "L", "…", "⇞", "ξ", "Ξ"),
                        ("v", "V", "_", "⌫", "", "√"),
                        ("x", "X", "[", "⇡", "λ", "Λ"),
                        ("c", "C", "]", "Entf", "χ", "ℂ"),
                        ("q", "Q", "^", "⇟", "ω", "Ω"),
                        ("k", "K", "!", "¡", "κ", "×"),
                        ("h", "H", "<", "7", "ψ", "Ψ"),
                        ("g", "G", ">", "8", "γ", "Γ"),
                        ("f", "F", "=", "9", "φ", "Φ"),
                        ("w", "W", "&", "+", "ϕ", "ℚ"),
                        ("y", "Y", "@", ".", "υ", "∇"),
                        ("ß", "ẞ", "ſ", "−", "ς", "∘"),
                        ()],  # Row 1

                       [("⇩"),
                        ("u", "U", "\\", "⇱", "", "⊂"),
                        ("i", "I", "/", "⇠", "ι", "∫"),
                        ("a", "A", "{",  "⇣", "α", "∀"),
                        ("e", "E", "}", "⇢", "ε", "∃"),
                        ("o", "O", "*", "⇲", "ο", "∈"),
                        ("s", "S", "?", "¿", "σ", "Σ"),
                        ("n", "N", "(", "4", "ν", "ℕ"),
                        ("r", "R", ")", "5", "ρ", "ℝ"),
                        ("t", "T", "-", "6", "τ", "∂"),
                        ("d", "D", ":", ",", "δ", "Δ"),
                        ("⇘"),
                        ("´", "~", "/", "˝", "", "˘"),
                        ("\n")],  # Row 2 (home row)

                       [("⇧"),
                        ("⇚"),
                        ("ü", "Ü", "#", "", "", "∪"),
                        ("ö", "Ö", "$", "", "ϵ", "∩"),
                        ("ä", "Ä", "|", "⎀", "η", "ℵ"),
                        ("p", "P", "~", "\n", "π", "Π"),
                        ("z", "Z", "`", "↶", "ζ", "ℤ"),
                        ("b", "B", "+", ":", "β", "⇐"),
                        ("m", "M", "%", "1", "μ", "⇔"),
                        (",", "–", '"', "2", "ϱ", "⇒"),
                        (".", "•", "'", "3", "ϑ", "↦"),
                        ("j", "J", ";", ";", "θ", "Θ"),
                        ("⇗")],  # Row  3

                       [("♕"), (), ("♔"), (" ", " ", " ", "0", " ", " "),("⇙"), (), (), ("♛")]])  # Row 4, containing the spacebar

    QWERTZ = Layout([[("^", "°", "′", "″"),
                      ("1", "!", "¹", "¡"),
                      ("2", '"', "²", "⅛"),
                      ("3", "§", "³", "£"),
                      ("4", "$", "¼", "¤"),
                      ("5", "%", "½", "⅜"),
                      ("6", "&", "¬", "⅝"),
                      ("7", "/", "{", "⅞"),
                      ("8", "(", "[", "™"),
                      ("9", ")", "]", "±"),
                      ("0", "=", "}", "°"),
                      ("ß", "?", "\\", "¿"),
                      ("´", "", "", ""),
                      ("←")],  # Row 0 (number row)
                     [("⇥"),
                      ("q", "Q", "@", "Ω"),
                      ("w", "W", "ł", "Ł"),
                      ("e", "E", "€", "€"),
                      ("r", "R", "¶", "®"),
                      ("t", "T", "ŧ", "Ŧ"),
                      ("z", "Z", "←", "¥"),
                      ("u", "U", "↓", "↑"),
                      ("i", "I", "→", "ı"),
                      ("o", "O", "ø", "Ø"),
                      ("p", "P", "þ", "Þ"),
                      ("ü", "Ü", "", ""),
                      ("+", "*", "~", "¯"),
                      ()],  # Row 1
                     [("⇩"),
                      ("a", "A", "æ", "Æ"),
                      ("s", "S", "ſ", "ẞ"),
                      ("d", "D", "ð", "Ð"),
                      ("f", "F", "đ", "ª"),
                      ("g", "G", "ŋ", "Ŋ"),
                      ("h", "H", "ħ", "Ħ"),
                      ("j", "J", "", ""),
                      ("k", "K", "ĸ", "&"),
                      ("l", "L", "ł", "Ł"),
                      ("ö", "Ö", "", ""),
                      ("ä", "Ä", "", ""),
                      ("#", "'", "’", ""),
                      ("\n")],  # Row 2 (home row)
                     [("⇧"),
                      ("<", ">", "|", ""),
                      ("y", "Y", "»", "›"),
                      ("x", "X", "«", "‹"),
                      ("c", "C", "¢", "©"),
                      ("v", "V", "„", "‚"),
                      ("b", "B", "“", "‘"),
                      ("n", "N", "”", "’"),
                      ("m", "M", "µ", "º"),
                      (",", ";", "·", "×"),
                      (".", ":", "…", "÷"),
                      ("-", "_", "–", "—"),
                      ("⇗")],  # Row  3
                     [("♕"), (), ("♔"), (" "), (), (), (), ("♛")]])  # Row 4, containing the spacebar

    CRY = Layout([[('^', 'ˇ', '↻', '˙', '˞', '̣'),
                   ('1', '°', '¹', 'ª', '₁', '¬'),
                   ('2', '§', '²', 'º', '₂', '∨'),
                   ('3', 'ℓ', '³', '№', '₃', '∧'),
                   ('4', '»', '›', '', '♀', '⊥'),
                   ('5', '«', '‹', '·', '♂', '∡'),
                   ('6', '$', '¢', '£', '⚥', '∥'),
                   ('7', '€', '¥', '¤', 'ϰ', '→'),
                   ('8', '„', '‚', '⇥', '⟨', '∞'),
                   ('9', '“', '‘', ' /', '⟩', '∝'),
                   ('0', '”', '’', '*', '₀', '∅'),
                   ('-', '—', '-', '‑', '\xad'),
                   ('`', '¸', '°', '¨', '', '¯'),
                   '←'],  # Row 0 (number row)
                  ['⇥',
                   ('b', 'B', '…', '⇞', 'β', '⇐'),
                   ('m', 'M', '_', '⌫', 'μ', '⇔'),
                   ('u', 'U', '[', '⇡', '', '⊂'),
                   ('a', 'A', ']', 'Entf', 'α', '∀'),
                   ('z', 'Z', '^', '⇟', 'ζ', 'ℤ'),
                   ('k', 'K', '!', '¡', 'κ', '×'),
                   ('d', 'D', '<', '7', 'δ', 'Δ'),
                   ('f', 'F', '>', '8', 'φ', 'Φ'),
                   ('l', 'L', '=', '9', 'λ', 'Λ'),
                   ('v', 'V', '&', '+', '', '√'),
                   ('j', 'J', '@', '.', 'θ', 'Θ'),
                   ('ß', 'ẞ', 'ſ', '−', 'ς', '∘'),
                   ()],  # Row 1
                  ['⇩',
                   ('c', 'C', '\\', '⇱', 'χ', 'ℂ'),
                   ('r', 'R', '/', '⇠', 'ρ', 'ℝ'),
                   ('i', 'I', '{', '⇣', 'ι', '∫'),
                   ('e', 'E', '}', '⇢', 'ε', '∃'),
                   ('y', 'Y', '*', '⇲', 'υ', '∇'),
                   ('p', 'P', '?', '¿', 'π', 'Π'),
                   ('t', 'T', '(', '4', 'τ', '∂'),
                   ('s', 'S', ')', '5', 'σ', 'Σ'),
                   ('n', 'N', '-', '6', 'ν', 'ℕ'),
                   ('h', 'H', ':', ',', 'ψ', 'Ψ'),
                   ('⇘', '', '', '', '', ''),
                   ('´', '~', '/', '˝', '', '˘'),
                   '\n'],  # Row 2 (home row)
                  ['⇧',
                   '⇚',
                   ('x', 'X', '#', '\x1b', 'ξ', 'Ξ'),
                   ('ä', 'Ä', '$', '', 'η', 'ℵ'),
                   ('ü', 'Ü', '|', '⎀', '', '∪'),
                   ('o', 'O', '~', '\n', 'ο', '∈'),
                   ('ö', 'Ö', '`', '↶', 'ϵ', '∩'),
                   ('w', 'W', '+', ':', 'ω', 'Ω'),
                   ('g', 'G', '%', '1', 'γ', 'Γ'),
                   (',', '–', '"', '2', 'ϱ', '⇒'),
                   ('.', '•', "'", '3', 'ϑ', '↦'),
                   ('q', 'Q', ';', ';', 'ϕ', 'ℚ'),
                   '⇗'],  # Row 3
                  ['♕', (), '♔', (' ', ' ', ' ', '0', '\xa0', '\u202f'), '⇙', (), (), '♛']])  # Row 4, containing the spacebar

    BONE = Layout([[('^', 'ˇ', '↻', '˙', '˞', '̣'),
                    ('1', '°', '¹', 'ª', '₁', '¬'),
                    ('2', '§', '²', 'º', '₂', '∨'),
                    ('3', 'ℓ', '³', '№', '₃', '∧'),
                    ('4', '»', '›', '', '♀', '⊥'),
                    ('5', '«', '‹', '·', '♂', '∡'),
                    ('6', '$', '¢', '£', '⚥', '∥'),
                    ('7', '€', '¥', '¤', 'ϰ', '→'),
                    ('8', '„', '‚', '⇥', '⟨', '∞'),
                    ('9', '“', '‘', ' /', '⟩', '∝'),
                    ('0', '”', '’', '*', '₀', '∅'),
                    ('-', '—', '-', '‑', '\xad'),
                    ('`', '¸', '°', '¨', '', '¯'),
                    '←'],  # Row 0 (number row)
                   ['⇥',
                    ('j', 'J', '…', '⇞', 'β', '⇐'),
                    ('d', 'D', '_', '⌫', 'μ', '⇔'),
                    ('u', 'U', '[', '⇡', '', '⊂'),
                    ('a', 'A', ']', 'Entf', 'α', '∀'),
                    ('x', 'X', '^', '⇟', 'ζ', 'ℤ'),
                    ('p', 'P', '!', '¡', 'κ', '×'),
                    ('h', 'H', '<', '7', 'δ', 'Δ'),
                    ('l', 'L', '>', '8', 'φ', 'Φ'),
                    ('m', 'M', '=', '9', 'λ', 'Λ'),
                    ('w', 'W', '&', '+', '', '√'),
                    ('q', 'Q', '@', '.', 'θ', 'Θ'),
                    ('ß', 'ẞ', 'ſ', '−', 'ς', '∘'),
                    ()],  # Row 1
                   ['⇩',
                    ('c', 'C', '\\', '⇱', 'χ', 'ℂ'),
                    ('t', 'T', '/', '⇠', 'ρ', 'ℝ'),
                    ('i', 'I', '{', '⇣', 'ι', '∫'),
                    ('e', 'E', '}', '⇢', 'ε', '∃'),
                    ('o', 'O', '*', '⇲', 'υ', '∇'),
                    ('b', 'B', '?', '¿', 'π', 'Π'),
                    ('n', 'N', '(', '4', 'τ', '∂'),
                    ('r', 'R', ')', '5', 'σ', 'Σ'),
                    ('s', 'S', '-', '6', 'ν', 'ℕ'),
                    ('g', 'G', ':', ',', 'ψ', 'Ψ'),
                    ('⇘', '', '', '', '', ''),
                    ('´', '~', '/', '˝', '', '˘'),
                    '\n'],  # Row 2 (home row)
                   ['⇧',
                    '⇚',
                    ('f', 'F', '#', '\x1b', 'ξ', 'Ξ'),
                    ('v', 'V', '$', '', 'η', 'ℵ'),
                    ('ü', 'Ü', '|', '⎀', '', '∪'),
                    ('ä', 'Ä', '~', '\n', 'ο', '∈'),
                    ('ö', 'Ö', '`', '↶', 'ϵ', '∩'),
                    ('y', 'Y', '+', ':', 'ω', 'Ω'),
                    ('z', 'Z', '%', '1', 'γ', 'Γ'),
                    (',', '–', '"', '2', 'ϱ', '⇒'),
                    ('.', '•', "'", '3', 'ϑ', '↦'),
                    ('k', 'K', ';', ';', 'ϕ', 'ℚ'),
                    '⇗'],  # Row 3
                   ['♕', (), '♔', (' ', ' ', ' ', '0', '\xa0', '\u202f'), '⇙', (), (), '♛']])  # Row 4, containing the spacebar

    # NORDTAST = Layout([
    #    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    #    [("⇥"),("ä"),("u"),("o"),("b"),("p"),("k"),("g"),("l"),("m"),("f"),("x"),("+"),()], # Reihe 1
    #    [("⇩"),("a"),("i"),("e"),("t"),("c"),("h"),("d"),("n"),("r"),("s"),("ß"),(),("\n")], # Reihe 2
    #    [("⇧"),(),("."),(","),("ü"),("ö"),("q"),("y"),("z"),("w"),("v"),("j"),("⇗")],        # Reihe 3
    #    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
    # ]
    # https://web.archive.org/web/20100718182031/http://wiki.nordtast.org/w/Vergleich_mit_Neo
    # https://git.neo-layout.org/neo/neo-layout/src/commit/01ef0ff1/windows/neo-vars/src/nordtast.ahk#L39
    # Somewhat contradictory: https://web.archive.org/web/20110919045006/http://wiki.nordtast.org/w/Hauptseite

    #: from Ulf Bro, http://nordtast.org – with added Neo-layers to be fair in the comparisions.
    # TODO: Find out what the remaining symbols are and add them. Currently almost everything is wrong (it was copied from the [Layouts.NEO2])
    NORDTAST = Layout([[("^", "ˇ", "↻", "˙", "˞", "̣"),
                        ("1", "°", "¹", "ª", "₁", "¬"),
                        ("2", "§", "²", "º", "₂", "∨"),
                        ("3", "ℓ", "³", "№", "₃", "∧"),
                        ("4", "»", "›", "", "♀", "⊥"),
                        ("5", "«", "‹", "·", "♂", "∡"),
                        ("6", "$", "¢", "£", "⚥", "∥"),
                        ("7", "€", "¥", "¤", "ϰ", "→"),
                        ("8", "„", "‚", "⇥", "⟨", "∞"),
                        ("9", "“", "‘", " /", "⟩", "∝"),
                        ("0", "”", "’", "*", "₀", "∅"),
                        ("-", "—", "-", "‑", "­"),
                        ("´", "`", "°", "¨", "", "¯"),
                        ("←")],  # Row 0 (number row)
                       [("⇥"),
                        ("ä", "Ä", "…", "⇞", "ξ", "Ξ"),
                        ("u", "U", "_", "⌫", "", "√"),
                        ("o", "O", "[", "⇡", "λ", "Λ"),
                        ("b", "B", "]", "Entf", "χ", "ℂ"),
                        ("p", "P", "^", "⇟", "ω", "Ω"),
                        ("k", "K", "!", "¡", "κ", "×"),
                        ("g", "G", "<", "7", "ψ", "Ψ"),
                        ("l", "L", ">", "8", "γ", "Γ"),
                        ("m", "M", "=", "9", "φ", "Φ"),
                        ("f", "F", "&", "+", "ϕ", "ℚ"),
                        ("x", "X", "ſ", "−", "ς", "∘"),
                        ("+", "~", "/", "˝", "", "˘"),
                        ()],  # Row 1
                       [("⇩"),
                        ("a", "A", "\\", "⇱", "", "⊂"),
                        ("i", "I", "/", "⇠", "ι", "∫"),
                        ("e", "E", "{",  "⇣", "α", "∀"),
                        ("t", "T", "}", "⇢", "ε", "∃"),
                        ("c", "C", "*", "⇲", "ο", "∈"),
                        ("h", "H", "?", "¿", "σ", "Σ"),
                        ("d", "D", "(", "4", "ν", "ℕ"),
                        ("n", "N", ")", "5", "ρ", "ℝ"),
                        ("r", "R", "-", "6", "τ", "∂"),
                        ("s", "S", ":", ",", "δ", "Δ"),
                        ("ß", "ẞ", "@", ".", "υ", "∇"),
                        ("⇘"),
                        ("\n")],  # Row 2 (home row)
                       [("⇧"),
                        ("⇚"),
                        (".", "•", "#", "", "", "∪"),
                        (",", "–", "$", "", "ϵ", "∩"),
                        ("ü", "Ü", "|", "⎀", "η", "ℵ"),
                        ("x", "P", "~", "\n", "π", "Π"),
                        ("ö", "Ö", "`", "↶", "ζ", "ℤ"),
                        ("q", "Q", "+", ":", "β", "⇐"),
                        ("y", "Y", "%", "1", "μ", "⇔"),
                        ("z", "Z", '"', "2", "ϱ", "⇒"),
                        ("w", "W", "'", "3", "ϑ", "↦"),
                        ("v", "V", ";", ";", "θ", "Θ"),
                        #("j", "J", "", "", "", ""), #
                        ("⇗")],  # Row  3
                       [("♕"), (), ("♔"), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ("♛")]])  # Row 4, containing the spacebar

    # TODO: Add higher layers (shift for the numbers, …)
    DVORAK = Layout([[("^"),
                      ("1"),
                      ("2"),
                      ("3"),
                      ("4"),
                      ("5"),
                      ("6"),
                      ("7"),
                      ("8"),
                      ("9"),
                      ("0"),
                      ("ß"),
                      ("´"),
                      ("←")],  # Row 0 (number row)
                     [("⇥"),
                      ("’"),
                      (","),
                      ("."),
                      ("p"),
                      ("y"),
                      ("f"),
                      ("g"),
                      ("c"),
                      ("r"),
                      ("l"),
                      ("/"),
                      ("="),
                      ()],  # Row 1
                     [("⇩"),
                      ("a"),
                      ("o"),
                      ("e"),
                      ("u"),
                      ("i"),
                      ("d"),
                      ("h"),
                      ("t"),
                      ("n"),
                      ("s"),
                      ("-"),
                      (),
                      ("\n")],  # Row 2 (home row)
                     [("⇧"),
                      (),
                      (";"),
                      ("q"),
                      ("j"),
                      ("k"),
                      ("x"),
                      ("b"),
                      ("m"),
                      ("w"),
                      ("v"),
                      ("z"),
                      ("⇗")],  # Row  3
                     [("♕"), (), ("♔"), (" "), (), (), (), ("♛")]])  # Row 4, containing the spacebar

# TODO: Add higher layers (shift for the numbers, …)
    COLEMAK = Layout([[("^"),
                       ("1"),
                       ("2"),
                       ("3"),
                       ("4"),
                       ("5"),
                       ("6"),
                       ("7"),
                       ("8"),
                       ("9"),
                       ("0"),
                       ("ß"),
                       ("´"),
                       ("←")],  # Row 0 (number row)
                      [("⇥"),
                       ("q"),
                       ("w"),
                       ("f"),
                       ("p"),
                       ("g"),
                       ("j"),
                       ("l"),
                       ("u"),
                       ("y"),
                       (";"),
                       ("["),
                       ("]"),
                       ("\\")],  # Row 1
                      [("⇩"),
                       ("a"),
                       ("r"),
                       ("s"),
                       ("t"),
                       ("d"),
                       ("h"),
                       ("n"),
                       ("e"),
                       ("i"),
                       ("o"),
                       ("`"),
                       (),
                       ("\n")],  # Row 2 (home row)
                      [("⇧"),
                       (),
                       ("z"),
                       ("x"),
                       ("c"),
                       ("v"),
                       ("b"),
                       ("k"),
                       ("m"),
                       (","),
                       ("."),
                       ("/"),
                       ("⇗")],  # Row  3
                      [("♕"), (), ("♔"), (" "), (), (), (), ("♛")]])  # Row 4, containing the spacebar

    AdNW = Layout([[("^", "ˇ", "↻", "˙", "˞", "̣"),
                    ("1", "°", "¹", "ª", "₁", "¬"),
                    ("2", "§", "²", "º", "₂", "∨"),
                    ("3", "ℓ", "³", "№", "₃", "∧"),
                    ("4", "»", "›", "", "♀", "⊥"),
                    ("5", "«", "‹", "·", "♂", "∡"),
                    ("6", "$", "¢", "£", "⚥", "∥"),
                    ("7", "€", "¥", "¤", "ϰ", "→"),
                    ("8", "„", "‚", "⇥", "⟨", "∞"),
                    ("9", "“", "‘", " /", "⟩", "∝"),
                    ("0", "”", "’", "*", "₀", "∅"),
                    ("-", "—", "-", "‑", "­"),
                    ("`", "¸", "°", "¨", "", "¯"),
                    ("←")],  # Row 0 (number row)
                   [("⇥"),
                    ("k", "K", "…", "⇞", "κ", ""),
                    ("u", "U", "_", "⌫", "", "⊂"),
                    ("ü", "Ü", "[", "⇡", "", "∪"),
                    (".", "•", "]", "Entf", "ϑ", "↦"),
                    ("ä", "Ä", "^", "⇟", "η", "ℵ"),
                    ("v", "V", "!", "¡", "", "√"),
                    ("g", "G", "<", "7", "γ", "Γ"),
                    ("c", "C", ">", "8", "χ", "ℂ"),
                    ("l", "L", "=", "9", "λ", "Λ"),
                    ("j", "J", "&", "+", "θ", "Θ"),
                    ("f", "F", "ſ", "−", "φ", "Φ"),
                    ("´", "~", "/", "˝", "", "˘"),
                    ()],  # Row 1
                   [("⇩"),
                    ("h", "H", "\\", "⇱", "ψ", "Ψ"),
                    ("i", "I", "/", "⇠", "ι", "∫"),
                    ("e", "E", "}", "⇢", "ε", "∃"),
                    ("a", "A", "{",  "⇣", "α", "∀"),
                    ("o", "O", "*", "⇲", "ο", ""),
                    ("d", "D", "?", "¿", "δ", "Δ"),
                    ("t", "T", "(", "4", "τ", "∂"),
                    ("r", "R", ")", "5", "ρ", "ℝ"),
                    ("n", "N", "-", "6", "ν", "ℕ"),
                    ("s", "S", ":", ",", "σ", ""),
                    ("ß", "ẞ", "@", ".", "ς", ""),
                    ("⇘"),
                    ("\n")],  # Row 2 (home row)
                   [("⇧"),
                    ("⇚"),
                    ("x", "X", "#", "", "ξ", "Ξ"),
                    ("y", "Y", "$", "", "υ", ""),
                    ("ö", "Ö", "|", "⎀", "", "∩"),
                    (",", "–", "~", "\n", "ϱ", "⇒"),
                    ("q", "Q", "`", "↶", "ϕ", "ℚ"),
                    ("b", "B", "+", ":", "β", "⇐"),
                    ("p", "P", "%", "1", "π", "Π"),
                    ("w", "W", '"', "2", "ω", ""),
                    ("m", "M", "'", "3", "μ", "⇔"),
                    ("z", "Z", ";", ";", "ζ", "ℤ"),
                    ("⇗")],  # Row  3
                   [("♕"), (), ("♔"), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ("♛")]])  # Row 4, containing the spacebar

    KOY = Layout([[('^', 'ˇ', '↻', '˙', '˞', '̣'),
                   ('1', '°', '¹', 'ª', '₁', '¬'),
                   ('2', '§', '²', 'º', '₂', '∨'),
                   ('3', 'ℓ', '³', '№', '₃', '∧'),
                   ('4', '»', '›', '', '♀', '⊥'),
                   ('5', '«', '‹', '·', '♂', '∡'),
                   ('6', '$', '¢', '£', '⚥', '∥'),
                   ('7', '€', '¥', '¤', 'ϰ', '→'),
                   ('8', '„', '‚', '⇥', '⟨', '∞'),
                   ('9', '“', '‘', ' /', '⟩', '∝'),
                   ('0', '”', '’', '*', '₀', '∅'),
                   ('-', '—', '-', '‑', '\xad'),
                   ('`', '¸', '°', '¨', '', '¯'),
                   '←'],  # Row 0 (number row)
                  ['⇥',
                   ('k', 'K', '…', '⇞', 'κ', '×'),
                   ('.', '•', '_', '⌫', 'ϑ', '↦'),
                   ('o', 'O', '[', '⇡', 'ο', '∈'),
                   (',', '–', ']', 'Entf', 'ϱ', '⇒'),
                   ('y', 'Y', '^', '⇟', 'υ', '∇'),
                   ('v', 'V', '!', '¡', '', '√'),
                   ('g', 'G', '<', '7', 'γ', 'Γ'),
                   ('c', 'C', '>', '8', 'χ', 'ℂ'),
                   ('l', 'L', '=', '9', 'λ', 'Λ'),
                   ('ß', 'ẞ', '&', '+', 'ς', '∘'),
                   ('z', 'Z', '@', '.', 'ζ', 'ℤ'),
                   ('´', '~', 'ſ', '−', '', '˘'),
                   ()],  # Row 1
                  ['⇩',
                   ('h', 'H', '\\', '⇱', 'ψ', 'Ψ'),
                   ('a', 'A', '/', '⇠', 'α', '∀'),
                   ('e', 'E', '{', '⇣', 'ε', '∃'),
                   ('i', 'I', '}', '⇢', 'ι', '∫'),
                   ('u', 'U', '*', '⇲', '', '⊂'),
                   ('d', 'D', '?', '¿', 'δ', 'Δ'),
                   ('t', 'T', '(', '4', 'τ', '∂'),
                   ('r', 'R', ')', '5', 'ρ', 'ℝ'),
                   ('n', 'N', '-', '6', 'ν', 'ℕ'),
                   ('s', 'S', ':', ',', 'σ', 'Σ'),
                   ('f', 'F', '', '', 'φ', 'Φ'),
                   ('´', '~', '/', '˝', '', '˘'),
                   '\n'],  # Row 2 (home row)
                  ['⇧',
                   '⇚',
                   ('x', 'X', '#', '\x1b', 'ξ', 'Ξ'),
                   ('q', 'Q', '$', '', 'ϕ', 'ℚ'),
                   ('ä', 'Ä', '|', '⎀', 'η', 'ℵ'),
                   ('ü', 'Ü', '~', '\n', '', '∪'),
                   ('ö', 'Ö', '`', '↶', 'ϵ', '∩'),
                   ('b', 'B', '+', ':', 'β', '⇐'),
                   ('p', 'P', '%', '1', 'π', 'Π'),
                   ('w', 'W', '"', '2', 'ω', 'Ω'),
                   ('m', 'M', "'", '3', 'μ', '⇔'),
                   ('j', 'J', ';', ';', 'θ', 'Θ'),
                   '⇗'],  # Row 3
                  ['♕', (), '♔', (' ', ' ', ' ', '0', '\xa0', '\u202f'), '⇙', (), (), '♛']])  # Row 4, containing the spacebar

    HAEIU = Layout([[('^', 'ˇ', '↻', '˙', '˞', '̣'),
                     ('1', '°', '¹', 'ª', '₁', '¬'),
                     ('2', '§', '²', 'º', '₂', '∨'),
                     ('3', 'ℓ', '³', '№', '₃', '∧'),
                     ('4', '»', '›', '', '♀', '⊥'),
                     ('5', '«', '‹', '·', '♂', '∡'),
                     ('6', '$', '¢', '£', '⚥', '∥'),
                     ('7', '€', '¥', '¤', 'ϰ', '→'),
                     ('8', '„', '‚', '⇥', '⟨', '∞'),
                     ('9', '“', '‘', ' /', '⟩', '∝'),
                     ('0', '”', '’', '*', '₀', '∅'),
                     ('-', '—', '-', '‑', '←'),
                     ('`', '¸', '°', '¨', '', '¯'),
                     '←'],  # Row 0 (number row)
                    [('⇥'),
                     ('x', 'X', '…', '⇞', 'ξ', 'Ξ'),
                     ('z', 'Z', '_', '⌫', 'ζ', 'ℤ'),
                     ('o', 'O', '[', '⇡', 'ο', '∈'),
                     ('.', '•', ']', 'Entf', 'ϑ', '↦'),
                     (',', '–', '^', '⇟', 'ϱ', '⇒'),
                     ('p', 'P', '!', '¡', 'π', 'Π'),
                     ('c', 'C', '<', '7', 'χ', 'ℂ'),
                     ('l', 'L', '>', '8', 'λ', 'Λ'),
                     ('m', 'M', '=', '9', 'μ', '⇔'),
                     ('v', 'V', '&', '+', '', '√'),
                     ('ß', 'ẞ', 'ſ', '−', 'ς', '∘'),
                     ('´', '~', '/', '˝', '', '˘'),
                     ()],  # Row 1
                    [('⇩'),
                     ('h', 'H', '\\', '⇱', 'ψ', 'Ψ'),
                     ('a', 'A', '/', '⇠', 'α', '∀'),
                     ('e', 'E', '{', '⇣', 'ε', '∃'),
                     ('i', 'I', '}', '⇢', 'ι', '∫'),
                     ('u', 'U', '*', '⇲', '', '⊂'),
                     ('d', 'D', '?', '¿', 'δ', 'Δ'),
                     ('t', 'T', '(', '4', 'τ', '∂'),
                     ('n', 'N', ')', '5', 'ν', 'ℕ'),
                     ('r', 'R', '-', '6', 'ρ', 'ℝ'),
                     ('s', 'S', ':', ',', 'σ', ''),
                     ('w', 'W', '@', '.', 'ω', ''),
                     ('⇘'),
                     ('\n')],  # Row 2 (home row)
                    [('⇧'),
                     ('⇚'),
                     ('k', 'K', '#', '', 'κ', '×'),
                     ('ö', 'Ö', '$', '', '', '∩'),
                     ('ä', 'Ä', '|', '⎀', 'η', 'ℵ'),
                     ('ü', 'Ü', '~', '\n', '', '∪'),
                     ('y', 'Y', '`', '↶', 'υ', ''),
                     ('b', 'B', '+', ':', 'β', '⇐'),
                     ('g', 'G', '%', '1', 'γ', 'Γ'),
                     ('j', 'J', '"', '2', 'θ', 'Θ'),
                     ('q', 'Q', "'", '3', 'ϕ', 'ℚ'),
                     ('f', 'F', ';', ';', 'φ', 'Φ'),
                     ('⇗')],  # Row 3
                    [("♕"), (), ("♔"), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ("♛")]])  # Row 4, containing the spacebar

    WORKMAN = Layout([[('^', 'ˇ', '↻', '˙', '˞', '̣'),
                       ('1', '°', '¹', 'ª', '₁', '¬'),
                       ('2', '§', '²', 'º', '₂', '∨'),
                       ('3', 'ℓ', '³', '№', '₃', '∧'),
                       ('4', '»', '›', '', '♀', '⊥'),
                       ('5', '«', '‹', '·', '♂', '∡'),
                       ('6', '$', '¢', '£', '⚥', '∥'),
                       ('7', '€', '¥', '¤', 'ϰ', '→'),
                       ('8', '„', '‚', '⇥', '⟨', '∞'),
                       ('9', '“', '‘', ' /', '⟩', '∝'),
                       ('0', '”', '’', '*', '₀', '∅'),
                       ('-', '—', '-', '‑', '\xad'),
                       ('`', '¸', '°', '¨', '', '¯'),
                       '←'],  # Row 0 (number row)
                      ['⇥',
                       ('q', 'Q', '…', '⇞', 'ϕ', 'ℚ'),
                       ('d', 'D', '_', '⌫', 'δ', 'Δ'),
                       ('r', 'R', '[', '⇡', 'ρ', 'ℝ'),
                       ('w', 'W', ']', 'Entf', 'ω', 'Ω'),
                       ('q', 'Q', '^', '⇟', 'ϕ', 'ℚ'),
                       ('j', 'J', '!', '¡', 'θ', 'Θ'),
                       ('f', 'F', '<', '7', 'φ', 'Φ'),
                       ('u', 'U', '>', '8', '', '⊂'),
                       ('p', 'P', '=', '9', 'π', 'Π'),
                       ('ü', 'Ü', '&', '+', '', '∪'),
                       ('ö', 'Ö', '@', '.', 'ϵ', '∩'),
                       ('ß', 'ẞ', 'ſ', '−', 'ς', '∘'),
                       ()],  # Row 1
                      ['⇩',
                       ('a', 'A', '\\', '⇱', 'α', '∀'),
                       ('s', 'S', '/', '⇠', 'σ', 'Σ'),
                       ('h', 'H', '{', '⇣', 'ψ', 'Ψ'),
                       ('t', 'T', '}', '⇢', 'τ', '∂'),
                       ('g', 'G', '*', '⇲', 'γ', 'Γ'),
                       ('y', 'Y', '?', '¿', 'υ', '∇'),
                       ('n', 'N', '(', '4', 'ν', 'ℕ'),
                       ('e', 'E', ')', '5', 'ε', '∃'),
                       ('o', 'O', '-', '6', 'ο', '∈'),
                       ('i', 'I', ':', ',', 'ι', '∫'),
                       ('ä', 'Ä', '', '', 'η', 'ℵ'),
                       ('´', '~', '/', '˝', '', '˘'),
                       '\n'],  # Row 2 (homerow)
                      ['⇧',
                       '⇚',
                       ('z', 'Z', '#', '\x1b', 'ζ', 'ℤ'),
                       ('x', 'X', '$', '', 'ξ', 'Ξ'),
                       ('h', 'H', '|', '⎀', 'ψ', 'Ψ'),
                       ('c', 'C', '~', '\n', 'χ', 'ℂ'),
                       ('v', 'V', '`', '↶', '', '√'),
                       ('k', 'K', '+', ':', 'κ', '×'),
                       ('l', 'L', '%', '1', 'λ', 'Λ'),
                       (',', '–', '"', '2', 'ϱ', '⇒'),
                       ('.', '•', "'", '3', 'ϑ', '↦'),
                       ("'", 'J', ';', ';', 'θ', 'Θ'),
                       '⇗'],  # Row 3
                      ['♕', (), '♔', (' ', ' ', ' ', '0', '\xa0', '\u202f'), '⇙', (), (), '♛']])  # Row 4, containing the spacebar

    CAPEWELL = Layout([[('^', 'ˇ', '↻', '˙', '˞', '̣'),
                        ('1', '°', '¹', 'ª', '₁', '¬'),
                        ('2', '§', '²', 'º', '₂', '∨'),
                        ('3', 'ℓ', '³', '№', '₃', '∧'),
                        ('4', '»', '›', '', '♀', '⊥'),
                        ('5', '«', '‹', '·', '♂', '∡'),
                        ('6', '$', '¢', '£', '⚥', '∥'),
                        ('7', '€', '¥', '¤', 'ϰ', '→'),
                        ('8', '„', '‚', '⇥', '⟨', '∞'),
                        ('9', '“', '‘', ' /', '⟩', '∝'),
                        ('0', '”', '’', '*', '₀', '∅'),
                        ('-', '—', '-', '‑', '\xad'),
                        ('`', '¸', '°', '¨', '', '¯'),
                        '←'],  # Row 0 (number row)
                       ['⇥',
                        ('.', '•', '…', '⇞', 'ϑ', '↦'),
                        ('m', 'M', '_', '⌫', 'μ', '⇔'),
                        ('y', 'Y', '[', '⇡', 'υ', '∇'),
                        ('d', 'D', ']', 'Entf', 'δ', 'Δ'),
                        ('g', 'G', '^', '⇟', 'γ', 'Γ'),
                        (';', 'K', '!', '¡', 'κ', '×'),
                        ('w', 'W', '<', '7', 'ω', 'Ω'),
                        ('h', 'H', '>', '8', 'ψ', 'Ψ'),
                        (',', '–', '=', '9', 'ϱ', '⇒'),
                        ("'", 'Q', '&', '+', 'ϕ', 'ℚ'),
                        ('ä', 'Ä', '@', '.', 'η', 'ℵ'),
                        ('ü', 'Ü', 'ſ', '−', '', '∪'),
                        ()],  # Row 1
                       ['⇩',
                        ('a', 'A', '\\', '⇱', 'α', '∀'),
                        ('r', 'R', '/', '⇠', 'ρ', 'ℝ'),
                        ('e', 'E', '{', '⇣', 'ε', '∃'),
                        ('s', 'S', '}', '⇢', 'σ', 'Σ'),
                        ('f', 'F', '*', '⇲', 'φ', 'Φ'),
                        ('k', 'K', '?', '¿', 'κ', '×'),
                        ('t', 'T', '(', '4', 'τ', '∂'),
                        ('n', 'N', ')', '5', 'ν', 'ℕ'),
                        ('i', 'I', '-', '6', 'ι', '∫'),
                        ('o', 'O', ':', ',', 'ο', '∈'),
                        ('ö', 'Ö', '', '', 'ϵ', '∩'),
                        ('´', '~', '/', '˝', '', '˘'),
                        '\n'],  # Row 2 (home row)
                       ['⇧',
                        '⇚',
                        ('x', 'X', '#', '\x1b', 'ξ', 'Ξ'),
                        ('c', 'C', '$', '', 'χ', 'ℂ'),
                        ('z', 'Z', '|', '⎀', 'ζ', 'ℤ'),
                        ('v', 'V', '~', '\n', '', '√'),
                        ('j', 'J', '`', '↶', 'θ', 'Θ'),
                        ('b', 'B', '+', ':', 'β', '⇐'),
                        ('p', 'P', '%', '1', 'π', 'Π'),
                        ('l', 'L', '"', '2', 'λ', 'Λ'),
                        ('u', 'U', "'", '3', '', '⊂'),
                        ('q', 'Q', ';', ';', 'ϕ', 'ℚ'),
                        '⇗'],  # Row 3
                       ['♕', (), '♔', (' ', ' ', ' ', '0', '\xa0', '\u202f'), '⇙', (), (), '♛']])  # Row 4, containing the spacebar

    QGMLWY = Layout([[('^', 'ˇ', '↻', '˙', '˞', '̣'),
                      ('1', '°', '¹', 'ª', '₁', '¬'),
                      ('2', '§', '²', 'º', '₂', '∨'),
                      ('3', 'ℓ', '³', '№', '₃', '∧'),
                      ('4', '»', '›', '', '♀', '⊥'),
                      ('5', '«', '‹', '·', '♂', '∡'),
                      ('6', '$', '¢', '£', '⚥', '∥'),
                      ('7', '€', '¥', '¤', 'ϰ', '→'),
                      ('8', '„', '‚', '⇥', '⟨', '∞'),
                      ('9', '“', '‘', ' /', '⟩', '∝'),
                      ('0', '”', '’', '*', '₀', '∅'),
                      ('-', '—', '-', '‑', '\xad'),
                      ('`', '¸', '°', '¨', '', '¯'),
                      '←'],  # Row 0 (number row)
                     ['⇥',
                      ('q', 'Q', '…', '⇞', 'ϕ', 'ℚ'),
                      ('g', 'G', '_', '⌫', 'γ', 'Γ'),
                      ('m', 'M', '[', '⇡', 'μ', '⇔'),
                      ('l', 'L', ']', 'Entf', 'λ', 'Λ'),
                      ('w', 'W', '^', '⇟', 'ω', 'Ω'),
                      ('b', 'B', '!', '¡', 'β', '⇐'),
                      ('y', 'Y', '<', '7', 'υ', '∇'),
                      ('v', 'V', '>', '8', '', '√'),
                      (';', 'F', '=', '9', 'φ', 'Φ'),
                      ('ä', 'Ä', '&', '+', 'η', 'ℵ'),
                      ('ö', 'Ö', '@', '.', 'ϵ', '∩'),
                      ('ß', 'ẞ', 'ſ', '−', 'ς', '∘'),
                      ()],  # Row 1
                     ['⇩',
                      ('d', 'D', '\\', '⇱', 'δ', 'Δ'),
                      ('s', 'S', '/', '⇠', 'σ', 'Σ'),
                      ('t', 'T', '{', '⇣', 'τ', '∂'),
                      ('n', 'N', '}', '⇢', 'ν', 'ℕ'),
                      ('r', 'R', '*', '⇲', 'ρ', 'ℝ'),
                      ('i', 'I', '?', '¿', 'ι', '∫'),
                      ('a', 'A', '(', '4', 'α', '∀'),
                      ('e', 'E', ')', '5', 'ε', '∃'),
                      ('o', 'O', '-', '6', 'ο', '∈'),
                      ('h', 'H', ':', ',', 'ψ', 'Ψ'),
                      ('ü', 'Ü', '', '', '', '∪'),
                      ('´', '~', '/', '˝', '', '˘'),
                      '\n'],  # Row 2 (home row)
                     ['⇧',
                      '⇚',
                      ('z', 'Z', '#', '\x1b', 'ζ', 'ℤ'),
                      ('x', 'X', '$', '', 'ξ', 'Ξ'),
                      ('c', 'C', '|', '⎀', 'χ', 'ℂ'),
                      ('f', 'F', '~', '\n', 'φ', 'Φ'),
                      ('j', 'J', '`', '↶', 'θ', 'Θ'),
                      ('k', 'K', '+', ':', 'κ', '×'),
                      ('p', 'P', '%', '1', 'π', 'Π'),
                      (',', '–', '"', '2', 'ϱ', '⇒'),
                      ('.', '•', "'", '3', 'ϑ', '↦'),
                      ("'", 'J', ';', ';', 'θ', 'Θ'),
                      '⇗'],  # Row 3
                     ['♕', (), '♔', (' ', ' ', ' ', '0', '\xa0', '\u202f'), '⇙', (), (), '♛']])  # Row 4, containing the spacebar

    TEST_LAYOUT = Layout([
        [("^", "ˇ", "↻")],  # Row 0 (number row)

        [("⇥"), ],  # Row 1

        [("u", "U", "\\", "⇱", "", "⊂"), ("\n")],  # Row 2 (home row)

        [],  # Row  3

        [(), (), (), (" "), ("⇙"), (), (), ()]  # Row 4, containing the spacebar
    ])


if __name__ == "__main__":
    from doctest import testmod
    testmod()
