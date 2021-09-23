import abc
class PlayerABC(abc.ABC):
    """An API for a player to communicate with the referee about a game of Fish."""

    @abstractmethod
    def __init__(self, color):
        """Initialize the player with it's color for the current game.

        color:  The player's color.
        """
        pass


    @abstractmethod
    def make_placement(self, state):
        """Make an avatar placement on the board.

        state:      The game's current state.

        returns:    The coordinates of an avatar placement (row, col)
        """
        pass


    @abstractmethod
    def make_move(self, state):
        """Make a move of on of the player's penguins on the board.

        state:      The game's current state.

        returns:    The coordinates of a move ((from_row, from_col), (to_row, to_col))
        """
        pass

