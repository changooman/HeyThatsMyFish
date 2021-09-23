from Fish.Common.player_interface import PlayerABC

class TournamentPlayer(PlayerABC):
    """Class to represent a player in a tournament of Fish. This
    player could be an in-house player or a player who is remote.
    """

    def __init__(self, player):
        """Initialize the client player.
        
        player (PlayerABC): the player to get moves, placements, and the color from.
        """
        self.__player = player

    
    def make_placement(self, state):
        """Make an avatar placement on the board.

        state:      The game's current state.

        returns:    The coordinates of an avatar placement (row, col)
        """
        return self.__player.make_placement(state)


    def make_move(self, state):
        """Make a move of on of the player's penguins on the board.

        state:      The game's current state.

        returns:    The coordinates of a move ((from_row, from_col), (to_row, to_col))
        """
        return self.__player.make_move(state)

    
    def get_color(self):
        """Get the color of this avatar.
        
        return: (string) the color assigned to this player
        """
        return self.__player.get_color()


    def set_color(self, color):
        """Assign a color to this avatar.
        
        color (string): the color to assign this player
        """
        self.__player.set_color(color)


    def inform_start(self):
        """Inform this player that the tournament is starting"""
        pass


    def inform_end(self, winner):
        """Inform this player that the tournament is ending
        
        winner (bool): True if this player won, False otherwise.
        """
        pass

