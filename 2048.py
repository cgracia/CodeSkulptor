"""
Clone of 2048 game.
"""

import poc_2048_gui

# import user40_o7Yktx7pKA_7 as test

from random import randint

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
        """
        Init the game
        """
        self._height = grid_height
        self._width = grid_width
        self.reset()
        
        # Dictionary for the starting tiles for each direction
        tiles_up = []
        tiles_down = []
        for index in range(grid_width):
            tiles_up.append((0, index))
            tiles_down.append((grid_height - 1, index))
            
        tiles_left = []
        tiles_right = []
        for index in range(grid_height):
            tiles_right.append((index, grid_width - 1))
            tiles_left.append((index, 0))
            
        self._starting_tiles = {UP: tiles_up,
                                DOWN: tiles_down,
                                LEFT: tiles_left,
                                RIGHT: tiles_right}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # Set all cells to 0
        self._grid = [[0 for dummy_col in range(self._width)] 
                         for dummy_row in range(self._height)]
        
        # Get two random initial tiles
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = "\n"
        for row in range(self._height):
            string += str(self._grid[row]) + "\n"
        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        has_moved = False
        for tile in self._starting_tiles[direction]:
            moved = self.move_line(tile, direction)
            has_moved = has_moved or moved
        
        if has_moved:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # Check if there are empty tiles
        empty_tiles = 0
        for row in self._grid:
            for cell in row:
                if cell == 0:
                    empty_tiles += 1
                
        if empty_tiles == 0:
            return False
        
        # Choose an empty tile
        chosen_tile = randint(1, empty_tiles)
        
        # Choose value, 90% -> 2, 10% -> 4
        chosen_value = 2
        if randint(0, 9) == 0:
            chosen_value = 4
            
        # Apply value to tile
        current_tile = 1
        for n_row, row in enumerate(self._grid):
            for n_col, cell in enumerate(row):
                if cell == 0:
                    if current_tile == chosen_tile:
                        self._grid[n_row][n_col] = chosen_value
                        return True
                    else:
                        current_tile += 1
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]
    
    def move_line(self, initial_tile, direction):
        """
        Move the values in the indicated line in the given direction.
        Must be called in move for each row or column
        """
        # How many tiles are there in a line.
        if (direction == UP) or (direction == DOWN):
            num_tiles = self._height
        else:
            num_tiles = self._width
        
        # Get values
        line = []
        for tile in range(num_tiles):
            row = initial_tile[0] + tile * OFFSETS[direction][0]
            col= initial_tile[1] + tile * OFFSETS[direction][1]
            line.append(self._grid[row][col])
            
        # Merge
        new_line = merge(line)
        
        if new_line == line:
            # No changes
            return False
        
        else:
        # Set new values
            for tile in range(num_tiles):
                row = initial_tile[0] + tile * OFFSETS[direction][0]
                col= initial_tile[1] + tile * OFFSETS[direction][1]
                self._grid[row][col] = new_line[tile]
            return True        


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

# Testing
#game = TwentyFortyEight(4,5)
#test.run_suite(game)
