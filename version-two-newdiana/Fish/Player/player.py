from Fish.Player.strategy import Strategy

class Player(object):
    """A player of Fish games that can place avatars and make moves.

    self.color:     This player's assigned color.
    self.strategy:  This player's gameplay Strategy.
    self.depth:     The depth to use for strategy searches.
    """

    def __init__(self, color=None, depth=2):
        """Initialize the player with it's color for the current game.

        depth:  The depth to use for strategy searches.
        """
        self.color = color
        self.strategy = Strategy()
        self.depth = depth;


    def get_color(self):
        """Get the color of this Player.

        returns:    The color of this Player as a string, None if it has not been set.
        """
        return self.color


    def set_color(self, color):
        """Set the color of this Player.

        color:  The color to set this Player as.
        """
        self.color = color


    def __check_turn(self, state):
        """Check that it's this player's turn in a given state.

        state:      The state to check.

        returns:    True if it's this player's turn in the state, False otherwise.
        """
        return self.color == state.whose_turn().get_color()


    def make_placement(self, state):
        """Make an avatar placement on the board.

        state:      The game's current state.

        returns:    The coordinates of an avatar placement (row, col)

        throws:     ValueError if state does not allow this player to place an avatar.
        """
        if not self.__check_turn(state):
            raise ValueError("The given state does not allow this player to place an avatar: wrong turn.")

        placement = self.strategy.make_placement(state)
        if placement:
            return placement
        else:
            raise ValueError("The given state does not allow this player to place an avatar: no space.")


    def make_move(self, state):
        """Make a move of on of the player's penguins on the board.

        state:      The game's current state.

        returns:    The coordinates of a move ((from_row, from_col), (to_row, to_col))

        throws:     ValueError if state does not allow this player to move an avatar.
        """
        if not self.__check_turn(state):
            raise ValueError("The given state does not allow this player to move an avatar: wrong turn.")

        move = self.strategy.make_move(state, self.depth)
        if move:
            return move
        else:
            raise ValueError("The given state does not allow this player to move an avatar: no move.")


    def you_have_won(self):
        """Inform the player that they have won a tournament."""
        pass


    def you_have_lost(self):
        """Inform the player that they have lost a tournament."""
        pass
