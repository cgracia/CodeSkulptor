"""
Clone of 2048 game.
"""

import poc_2048_gui

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    
    shift_list = shift_left(line)
    merge_list = merge_pairs(shift_list)
    result_list = shift_left(merge_list)
    
    return result_list

def shift_left(line):
    """
    Function that moves all the values to the left.
    """
    
    result_list = [0] * len(line)
    
    # Put non zero values of line in the first 
    # available position in result_list
    first_available = 0
    for position in range(len(line)):
        if line[position] != 0:
            result_list[first_available] = line[position]
            first_available += 1
            
    return result_list

def merge_pairs(line):
    """
    Function that merges the possible pairs in a line.
    """
    result_list = line
    
    skip_next = False
    for position in range(len(line) - 1):
        if skip_next:
            skip_next = False
        elif line[position] == line[position + 1]:
            result_list[position] = line[position] * 2
            result_list[position + 1] = 0
            skip_next = True
            
    return result_list 

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        pass

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        pass

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return ""

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return 0

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return 0

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        pass

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        pass

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        pass

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return 0


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

