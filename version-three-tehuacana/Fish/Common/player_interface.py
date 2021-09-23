from abc import ABCMeta
from abc import abstractmethod

class PlayerABC:
    """An API for a player to communicate with the referee about a game of Fish."""

    __metaclass__ = ABCMeta

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

    
    @abstractmethod
    def get_color(self):
        """Get the color of this avatar.
        
        return: (string) the color assigned to this player
        """
        pass


    @abstractmethod
    def set_color(self, color):
        """Assign a color to this avatar.
        
        color (string): the color to assign this player
        """
        pass

