"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert \
                    zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = \
                    self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert \
                    zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = \
                    self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert \
                    zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = \
                    self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert \
                    zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = \
                    self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if not self._is_zero(target_row, target_col):
            return False
        if not self._is_below_rows_solved(target_row + 1):
            return False
        if not self._is_right_tiles_solved(target_row, target_col + 1):
            return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_string = ""
        target = target_row, target_col
        current = self.current_position(target_row, target_col)
        move_string += move_over_tile(target, current)
        move_string += correct_col(target, current)
        move_string += turn_corner(target, current)
        move_string += correct_row(target, current)
        move_string += self._correct_zero_tile(target, current)
        self.update_puzzle(move_string)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        move_string = ""
        target = target_row, 0
        current = self.current_position(target_row, 0)
        move_string += move_over_tile(target, current)
        if not (target_row - current[0] == 1 and current[1] == 0):
            move_string += correct_col(target, current)
            move_string += turn_corner(target, current)
            move_string += correct_row(target, current)
            move_string += get_last_step_for_col0()
        move_string += self._correct_zero_tile(target, current)
        self.update_puzzle(move_string)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self._is_zero(0, target_col):
            return False
        if not self._is_below_rows_solved(2):
            return False
        if not self._is_right_tiles_solved(1, target_col):
            return False
        if not self._is_right_tiles_solved(0, target_col + 1):
            return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if not self._is_zero(1, target_col):
            return False
        if not self._is_below_rows_solved(2):
            return False
        if not self._is_right_tiles_solved(1, target_col + 1):
            return False
        if not self._is_right_tiles_solved(0, target_col + 1):
            return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_string = ""
        target = 0, target_col
        current = self.current_position(0, target_col)
        move_string += move_over_tile(target, current)
        if not (current[0] == 0 and target_col - current[1] == 1):
            move_string += turn_corner_for_row0(target, current)
            move_string += correct_col_for_row0(target, current)
            move_string += get_last_step_for_row0()
        move_string += correct_zero_tile_for_row0()
        self.update_puzzle(move_string)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        move_string = ""
        target = 1, target_col
        current = self.current_position(1, target_col)
        move_string += move_over_tile(target, current)
        move_string += correct_col(target, current)
        move_string += turn_corner(target, current)
        move_string += correct_zero_tile_for_row1(current)
        self.update_puzzle(move_string)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        current = self.current_position(1, 1)
        if current[0] == 1 and current[1] == 0:
            move_string = "lu"
        elif current[0] == 0 and current[1] == 1:
            move_string = "ul"
        else:
            move_string = "lurdlu"
        self.update_puzzle(move_string)
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        current_zero = self.current_position(0, 0)
        move_string += "d" * (self._height - current_zero[0] - 1)
        move_string += "r" * (self._width - current_zero[1] - 1)
        self.update_puzzle(move_string)
        for row in range(self._height - 1, 1, -1):
            for col in range(self._width - 1, 0, -1):
                move_string += self.solve_interior_tile(row, col)
            move_string += self.solve_col0_tile(row)
        for col in range(self._width - 1, 1, -1):
            move_string += self.solve_row1_tile(col)
            move_string += self.solve_row0_tile(col)
        move_string += self.solve_2x2()
        return move_string

    ###########################################################
    # Helper functions

    def _is_zero(self, target_row, target_col):
        """
        Helper function.
        """
        return self._grid[target_row][target_col] == 0

    def _is_tile_solved(self, target_row, target_col):
        """
        Helper function.
        """
        return \
            self._grid[target_row][target_col] \
            == target_row * self._width + target_col

    def _is_below_rows_solved(self, target_row):
        """
        Helper function.
        """
        for row in range(target_row, self._height):
            for col in range(self._width):
                if not self._is_tile_solved(row, col):
                    return False
        return True

    def _is_right_tiles_solved(self, target_row, target_col):
        """
        Helper function.
        """
        for col in range(target_col, self._width):
            if not self._is_tile_solved(target_row, col):
                return False
        return True

    def _correct_zero_tile(self, target, current):
        """
        Helper function.
        """
        if target[1] == 0:
            return "r" * (self._width - 1)
        else:
            return "ld" if target[0] != current[0] else ""

def move_over_tile(target, current):
    """
    Helper function.
    """
    result = ""
    result += "u" * (target[0] - current[0])
    if target[1] < current[1]:
        result += "r" * (current[1] - target[1])
    else:
        result += "l" * (target[1] - current[1])
    result += "d" * (current[0] - target[0])
    return result

def correct_col(target, current):
    """
    Helper function.
    """
    if target[1] < current[1]:
        if current[0] == 0:
            return "dllur" * (current[1] - target[1] - 1)
        else:
            return "ulldr" * (current[1] - target[1] - 1)
    else:
        if current[0] == 0:
            return "drrul" * (target[1] - current[1] - 1)
        else:
            return "urrdl" * (target[1] - current[1] - 1)

def correct_col_for_row0(target, current):
    """
    Helper function.
    """
    return "drrul" * (target[1] - current[1] - 2)

def turn_corner(target, current):
    """
    Helper function.
    """
    if target[0] != current[0]:
        if target[1] < current[1]:
            if target[0] - current[0] == 1:
                if target[1] == 0:
                    return "ul"
                else:
                    return "ullddru"
            else:
                return "dlu"
        if target[1] > current[1]:
            return "dru"
    return ""

def turn_corner_for_row0(target, current):
    """
    Helper function.
    """
    if current[0] == 1:
        if target[1] - current[1] == 1:
            return "lu"
        else:
            return "rul"
    return ""

def correct_row(target, current):
    """
    Helper function.
    """
    if target[1] == 0:
        return "rddlu" * (target[0] - current[0] - 2)
    else:
        return "lddru" * (target[0] - current[0] - 1)

def get_last_step_for_col0():
    """
    Helper function.
    """
    return "ddrulurddlu"

def get_last_step_for_row0():
    """
    Helper function.
    """
    return "rrdluldrrul"

def correct_zero_tile_for_row0():
    """
    Helper function.
    """
    return "d"

def correct_zero_tile_for_row1(current):
    """
    Helper function.
    """
    if current[0] == 1:
        return "ur"
    return ""

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
