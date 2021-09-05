from copy import deepcopy

from config import COST_LAYER_ADDITION, COST_PER_KEY, COST_PER_KEY_NOT_FOUND, FINGER_POSITIONS, RIGHT_HAND_LOWEST_INDEXES

class Layout:
    """The data-structure for a layout.
    
    Create by using the default-constructor and passing in a list that resembles the layout-lists found in layout_basee.py. (Example: NEO_BLUEPRINT)
        l = Layout(NEO_BLUEPRINT)
    
    Alternatively, create the layout from a layout-string via the static method `.from_string()`
        l = Layout.from_string(layout_string, NEO_BLUEPRINT)
    
    This class also caches the most often requested information (What position is "a" on?) and 
    provides methods to access this information.
    """
    
    # A static field that contains the information which finger presses each layer-1 position (x, y, 0)
    _POS_TO_FINGER = {}
    for finger, positions in FINGER_POSITIONS.items():
        for pos in positions:
            _POS_TO_FINGER[pos] = finger


    ### Fields ###
    
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
            lowest_right_hand_idx = RIGHT_HAND_LOWEST_INDEXES[row_idx]
            for key_idx, key in enumerate(row):
                for layer_idx, char in enumerate(key):
                    pos = (row_idx, key_idx, layer_idx)

                    if char not in self._char_finger_dict:
                        # Fill up _char_finger_dict
                        self._char_finger_dict[char] = Layout._POS_TO_FINGER[row_idx, key_idx, 0]

                        # Fill up _char_pos_dict
                        self._char_pos_dict[char] = pos
                    elif self._is_position_cost_lower(self._char_pos_dict[char], pos):
                        # Fill up _char_finger_dict
                        self._char_finger_dict[char] = Layout._POS_TO_FINGER[row_idx, key_idx, 0]

                        # Fill up _char_pos_dict
                        self._char_pos_dict[char] = pos

                    # Fill up _pos_is_left_dict
                    self._pos_is_left_dict[pos] = lowest_right_hand_idx > key_idx

                    # Fill up _pos_char_dict
                    self._pos_char_dict[pos] = char
    
    @classmethod
    def from_string(self, layout_string, base_blueprint):
        """Turn a layout_string into a layout. This is the alternative constructor for the Layout-class.

        Example of a layout-string:
            öckäy zhmlß,´
            atieo dsnru.
            xpfüq bgvwj
        """
        def set_key(current_key, new_letter, pos_01, blueprint, base_blueprint=base_blueprint, changing_layers=[0,1,4,5]):
            """Set the new_letter into the pos_01 in the blueprint. Take the key from the position in the base_blueprint and from the position in the letter and merge them, using layer 3,4 from the position and the rest from the letter.

            @param pos_01: the key which is currently in the given position. Not needed anymore, except for debugging.
            @param current_key: The key which is currently in the position. Not needed anymore, except for debugging.
            @param new_letter: The letter which should be in the position.
            @param pos_01: The position where the key should be placed.
            @param changing_layers: The layers in the base blueprint which change when the keys get changed."""
            # first get the keys for all layers from position in the base_blueprint
            base_keys = base_blueprint[pos_01[0]][pos_01[1]]
            # then get the keys corresponding to the position of the new letter.
            letter_pos = letter_to_pos(new_letter, blueprint=blueprint)
            if letter_pos is None or letter_pos[2]:
                # the new letter is not in the base_blueprint or not in the base layer, just set it on layer 0.
                blueprint[pos_01[0]][pos_01[1]] = (new_letter, ) + tuple(base_keys[1:])
                return blueprint
                
            letter_keys = base_blueprint[letter_pos[0]][letter_pos[1]]
            # replace all changing_layers in the base_keys with the new_keys.
            tmp = []
            for i in range(6):
                try: 
                    if i in changing_layers:
                        tmp.append(letter_keys[i])
                    else:
                        tmp.append(base_keys[i])
                except IndexError: # key not found
                    tmp.append("")
            blueprint[pos_01[0]][pos_01[1]] = tuple(tmp)
            return blueprint


        def letter_to_pos(searched_char:str, blueprint:list) -> tuple:
            for row_idx, row in enumerate(blueprint):
                for key_idx, key in enumerate(row):
                    if key and (len(key) > 0) and (key[0] is searched_char): # only look at the first layer (index 0)
                        pos = (row_idx, key_idx, 0)
                        return pos

            
        blueprint = deepcopy(base_blueprint)
        lines = layout_string.splitlines()
        # first and second letter row
        for i in range(1, 6):
            blueprint = set_key(blueprint[1][i][0],  lines[0][i-1],  (1, i),  blueprint)
            blueprint = set_key(blueprint[1][i+5][0],  lines[0][i+5],  (1, i+5),  blueprint)
            blueprint = set_key(blueprint[2][i][0],  lines[1][i-1],  (2, i),  blueprint)
            blueprint = set_key(blueprint[2][i+5][0],  lines[1][i+5],  (2, i+5),  blueprint)

        blueprint = set_key(blueprint[1][-3][0], lines[0][11], (1, -3), blueprint)
        blueprint = set_key(blueprint[2][-3][0], lines[1][11], (2, -3), blueprint)

        # third row
        if lines[0][12:]:
            blueprint = set_key(blueprint[1][-2][0], lines[0][12], (1, -2), blueprint)

        try:
            left, right = lines[2].split()[:2]
        except ValueError:
            print(lines)
            raise
        for i in range(len(left)):
            blueprint = set_key(blueprint[3][6-i][0], left[-i-1], (3, 6-i), blueprint)
        for i in range(len(right)):
            blueprint = set_key(blueprint[3][7+i][0], right[i], (3, 7+i), blueprint)
        
        return Layout(blueprint)




    ### Methods ###




    def _is_position_cost_lower(self, old_pos:tuple, new_pos:tuple, doubled_layer=True):
        """
        >>> is_position_cost_lower((2, 10, 2), (3, 7, 3), Layout(NEO_BLUEPRINT))
        False
        """
        # use tripled layer cost, because it ignores the additional bigrams.
        new_cost = self._single_key_position_cost(new_pos) + COST_LAYER_ADDITION[new_pos[2]]
        cost = self._single_key_position_cost(old_pos) + 2*COST_LAYER_ADDITION[old_pos[2]]
        return new_cost < cost

    def _single_key_position_cost(self, pos, cost_per_key=COST_PER_KEY):
        """Get the position_cost of a single key.

        @param pos: The position of the key.
        @type pos: tuple (row, col, layer).
        @return: the cost of that one position."""
        if pos is None: # not found
            return COST_PER_KEY_NOT_FOUND
        # shift, M3 and M4
        if COST_LAYER_ADDITION[pos[2]:]:
            return cost_per_key[pos[0]][pos[1]] + COST_LAYER_ADDITION[pos[2]]
        # layer has no addition cost ⇒ undefined layer (higher than layer 6!). Just take the base key…
        return cost_per_key[pos[0]][pos[1]]


    def get_all_chars(self) -> list: # get_all_keys_in_layout
        """Get all keys which are in the layout. Sorted the same way as the positions from get_all_positions_in_layout(). 

        >>> Layout(TEST_BLUEPRINT).get_all_chars()
        ['^', 'ˇ', '↻', '⇥', 'u', 'U', '\\\\', '⇱', '⊂', '\\n', ' ', '⇙']
        """
        chars = []
        for row in self.blueprint:
            for key in row:
                for char in key:
                    if char:
                        chars.append(char)
        return chars

    
    def char_to_finger(self, char:str) -> str: # key_to_finger
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
    
    def char_to_pos(self, char: str) -> tuple: # find_key
        """Find the position of the key in the layout.

        The result is a tuple which is structured as follows:
        (
            row_nr,  # top to botton, including the number-row
            key_nr,  # left to right
            layer_nr
        )
            >>> layout = Layout(QWERTZ_BLUEPRINT)  # Examples with QWERTZ
            >>> layout.char_to_pos("A")
            (2, 1, 1)
            >>> layout.char_to_pos("a")
            (2, 1, 0)
            >>> layout = Layout(NEO_BLUEPRINT)  # Examples with NEO2
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
    

    def pos_is_left(self, pos: tuple) -> bool: # pos_is_left
        """Check if the given position is on the left hand.
        
        The position-parameter should be a tuple structured as follows:
        (
            row_nr,  # top to botton, including the number-row
            key_nr,  # left to right
            layer_nr
        )
        """
        return self._pos_is_left_dict[pos]
    
    def pos_to_char(self, pos: tuple) -> str: # get_key
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