from copy import copy

class BoardPlayer():
    """Represents a player of Fish.

    Includes the player's color, score, and their penguins on the board.

    self.color:     The player's color.
    self.score:     The player's score.
    self.penguins:  A list of the player's penguins on the board, in 2D coordinate tuple form.
    """

    POSSIBLE_COLORS = ["red", "black", "white", "brown"]

    def __init__(self, color):
        if color.lower() not in self.POSSIBLE_COLORS:
            raise ValueError("Invalid color provided.")
        self.color = color.lower()
        self.score = 0      # the player's score
        self.penguins = []  # a list of 2D coordinate tuples representing the player's penguins


    def __ne__(self, other):
        return not self.__eq__(other)


    def __eq__(self, other):
        return (isinstance(other, BoardPlayer) and
                self.color == other.color and
                self.score == other.score and
                self.penguins == other.penguins)


    def __str__(self):
        return str((self.color, self.score, self.penguins))


    def __repr__(self):
        return self.__str__()


    def json_rep(self):
        """Represent the player as Python data structures in format for json.

        returns:    The representation.
        """
        rep = {}
        rep["color"] = self.get_color()
        rep["score"] = self.get_score()
        rep["places"] = self.get_penguins()
        return rep


    def get_color(self):
        """Get the player's color.

        returns:    The player's color.
        """
        return self.color


    def get_score(self):
        """Get the player's score.

        returns:    The player's score.
        """
        return self.score


    def set_score(self, score):
        """Set the player's score."""
        self.score = score


    def add_score(self, value):
        """Adds a value to player's score.

        value:  The value to add to the player's score.
        """
        self.score += value


    def get_penguins(self):
        """Get the list of player penguins.

        returns:    A list of the player's penguin positions.
        """
        return copy(self.penguins)


    def add_penguin(self, coords):
        """Add a penguin to the player's list of penguins.

        coords: The 2D coordinates of the new penguin.
        """
        self.penguins.append(coords)


    def remove_penguin(self, coords):
        """Removes a penguin from the player's list of penguins.

        coords: The 2D coordinates of the penguin to remove.
        """
        self.penguins.remove(coords)


    def move_penguin(self, prev_coords, dest_coords):
        """Moves a penguin at prev_coords to dest_coords.

        prev_coords:    The penguin's current coords.
        dest_coords:    The penguin's new coords.
        """
        idx = self.penguins.index(prev_coords)
        self.penguins[idx] = dest_coords
