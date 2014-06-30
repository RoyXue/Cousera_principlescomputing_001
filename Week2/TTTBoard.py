class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """

    def __init__(self, dim, reverse = False, board = None):
        """
        Initialize the TTTBoard object with the given dimension and 
        whether or not the game should be reversed.
        """
            
    def __str__(self):
        """
        Human readable representation of the board.
        """

    def get_dim(self):
        """
        Return the dimension of the board.
        """
    
    def square(self, row, col):
        """
        Return the status (EMPTY, PLAYERX, PLAYERO) of the square at
        position (row, col).
        """

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).

        Does nothing if board square is not empty.
        """

    def check_win(self):
        """
        If someone has won, return player.
        If game is a draw, return DRAW.
        If game is in progress, return None.
        """
            
    def clone(self):
        """
        Return a copy of the board.
        """
