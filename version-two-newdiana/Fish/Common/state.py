from copy import copy

class State():
    """Represents a game state of a game of fish.

    self.players:       A list of the game's BoardPlayers in turn order.
                        The first player in the list is always the player whose turn it is.
                        BoardPlayer objects hold each player's penguin locations.
    self.max_avatars:   The maximum number of avatars each player may have.
    self.board:         The Board for this game.
    """

    def __init__(self, players, board):
        """Initialize the tile.

        players:        A list of players, in their turn order.
        board:          The board for this game state.
        """
        if len(players) == 0:
            raise ValueError("No players provided.")

        self.players = copy(players)
        self.max_avatars = 6 - len(self.players)
        self.board = board


    def __ne__(self, other):
        return not self.__eq__(other)


    def __eq__(self, other):
        return (isinstance(other, State) and
                self.players == other.players and
                self.board == other.board)


    def json_rep(self):
        """Represent the game state as Python data structures in format for json.

        returns:    The representation.
        """
        rep = {}
        rep["players"] = [p.json_rep() for p in self.players]
        rep["board"] = self.board.json_rep()
        return rep


    def is_game_over(self):
        """Is the game over?

        returns:    True if the game is over, False otherwise.
        """
        for player in self.players:
            for penguin in player.get_penguins():
                if len(self.get_reachable(penguin)) > 0:
                    return False
        return True


    def all_avatars_placed(self):
        """Check that all players' avatars have been placed.

        returns:    True if all players' avatars have been placed.
        """
        placed = set([len(p.get_penguins()) for p in self.players])
        return len(placed) == 0 or (len(placed) == 1 and self.max_avatars in placed)


    def __all_penguins(self):
        """Get a list of all penguins on the board.

        returns: That list.
        """
        ret = []
        for p in self.players:
            ret += p.get_penguins()
        return ret


    def __current_player_can_move(self):
        """Test if the current player can move.

        returns:    True if they can, False otherwise.
        """
        for penguin in self.whose_turn().get_penguins():
            if len(self.get_reachable(penguin)) > 0:
                return True
        return False


    def __next_turn(self):
        """Progress the turn order by one player."""
        p = self.players.pop(0)
        self.players.append(p)


    def pass_turn_if_applicable(self):
        """Passes the turn continually while the current player can't make a move."""
        while not self.__current_player_can_move() and not self.is_game_over():
            self.__next_turn()


    def get_players(self):
        """Get the game's players.

        returns:    A list of players.
        """
        return self.players


    def get_board(self):
        """Get the game board.

        returns:    The Board.
        """
        return self.board


    def whose_turn(self):
        """Get whose turn it currently is.

        returns:    The BoardPlayer whose turn it currently is.
        """
        return self.players[0]


    def remove_player(self, color):
        """Remove a player from the game along with their penguins.

        color:  The color of the player to remove.
        """
        for p in self.players:
            if p.get_color() == color:
                self.players.remove(p)
                break


    def valid_placement(self, coords, player_color):
        """Checks if an avatar placement is valid, and that the turn order allows this player to go.

        coords:         A tuple of the avatar position (row, column).
        player_color:   The player's penguins' color.

        returns:        If the placement is valid or not.
        """
        p = self.whose_turn()
        if player_color != p.get_color():
            return False
        elif len(p.get_penguins()) >= self.max_avatars:
            return False

        t = self.board.get_tile(coords)
        return t != None and coords not in self.__all_penguins()


    def place_avatar(self, coords, player_color):
        """If valid, places an avatar at the specified position for the given player.

        coords:         A tuple of the avatar position (row, column).
        player_color:   The player's penguins' color.
        """
        if self.valid_placement(coords, player_color):
            p = self.whose_turn()
            p.add_penguin(coords)
            self.__next_turn()
        else:
            raise ValueError("The placement is invalid.")


    def get_reachable(self, coords):
        """Get the reachable positions from a specific tile on the board.

        coords:   A tuple of the starting position tile (row, column).

        returns:    A List of reachable tile coordinates in tuple form.
        """
        return self.board.get_reachable(coords, self.__all_penguins())


    def valid_move(self, prev_coords, dest_coords):
        """Checks if a move is valid and that the penguin being moved
        belongs to the player whose turn it currently is.

        prev_coords:    The position of the avatar to be moved.
        dest_coords:    The resulting position of the move.

        returns:        If the move is valid or not.
        """
        p = self.whose_turn()
        if prev_coords not in p.get_penguins():
            return False


        pt = self.board.get_tile(prev_coords)
        dt = self.board.get_tile(dest_coords)
        if pt is not None:
            return dest_coords in self.get_reachable(prev_coords)
        else:
            return False


    def move_avatar(self, prev_coords, dest_coords):
        """If valid, moves avatar from the specified previous position to the specified destination,
        and destroys the tile at the avatar's original position.

        prev_coords:   A tuple of the avatar's original position (row, column).
        dest_coords:   A tuple of the avatar's destination position (row, column).
        """
        if (self.valid_move(prev_coords, dest_coords)):
            p = self.whose_turn()
            p.move_penguin(prev_coords, dest_coords)
            p.add_score(self.board.get_tile(prev_coords).get_num_fish())
            self.board.remove_tile(prev_coords)
            self.__next_turn()
        else:
            raise ValueError("The move is invalid.")


    def draw(self, ctx):
        """Draw the game state.

        ctx:    The drawing context to draw the state in.
        """
        self.board.draw(ctx, self.players)

