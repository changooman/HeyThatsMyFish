from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State

from copy import deepcopy
from Queue import Queue
from threading import Thread

import time

class Referee():
    """Represents a Fish Referee, who can run a complete Fish game for a sequence of players.

    The referee creates a board, runs a game with players, and presents the outcome.

    Players who attempt invalid placements or movements, take too long to respond, or otherwise crash
    will be ejected from the game and their penguins will be removed. A deepcopy of the game State is
    passed to the players so that they may mutate it as they please.

    self.players:   A dictionary of this game's Players indexed by their color. Players can be any class that implements PlayerABC
    self.state:     The current game state.
    self.violators: A set of violating player colors who have been removed from the game.
    self.timeout:   The amount of time each player has to place a penguin on make a move in seconds.
    """

    def __init__(self, players, board_size, board=None, timeout=10):
        """Initialize the Referee.

        Creates a turn order based on the ages of the players. If none of the players given have colors, then colors are assigned to
        the players. Otherwise, the colors of the players are used. If the players have colors, then they must be unique.
        Creates a Fish game board for the players to play on.

        players:                    A list of this game's Players, in ascending order of player age.
        board_size:                 The number of rows and columns for the game board (rows, columns). This field is ignored if a
                                    non-None board is given.
        board:                      The board to use for the game of Fish. Default is None, in which case a board of size of
                                    `board_size` is used, and the number of fish per tile is randomized (there are no holes.)
                                    When this field is not None, the `board_size` field is ignored (the size of this board is
                                    used instead).
        timeout:                    The amount of time each player has to place a penguin on make a move in seconds.

        throws:                     ValueError if board_size does not specify a large enough
                                    board for all player avatars, or if there are less than 2 players
                                    or more than 4.
                                    ValueError if some players have colors assigned and some do not (i.e. either
                                    none of the players have colors, or all of them have unique ones)
        """
        if not 2 <= len(players) <= 4:
            raise ValueError("Invalid number of players provided.")

        if board is None:
            board = Board(*board_size)

        self.__check_board_is_valid(board, players)

        self.board = board
        
        self.__set_colors(players)

        self.players = {p.get_color(): p for p in players}

        self.state = State([BoardPlayer(p.get_color()) for p in players], board)
        self.violators = []
        self.timeout = timeout

    def __check_board_is_valid(self, board, players):
        """Check that the board used is large enough and has enough valid
        tiles for the given list of players, raises a ValueError if any of these
        conditions are not met."""
        total_tiles = board.get_rows() * board.get_cols()
        # check the board is big enough
        if total_tiles < (6 - len(players)) * len(players):
            raise ValueError("Board specified by board_size is too small.")
        # check that the board has enough active tiles
        if len(players) == 3 and total_tiles - board.get_holes_in_board() < 9:
            raise ValueError("Too many holes to place all penguins")
        elif total_tiles - board.get_holes_in_board() < 8:
            raise ValueError("Too many holes to place all penguins")


    def __set_colors(self, players):
        """Set the colors of the players, if needed. If all players have unique colors,
        return the players as-is.

        players (list): a list of players to set the colors for, if needed

        returns (list): the list of players with their colors set.
        
        raises (ValueError): if some players have colors assigned and
        some do not (i.e. either none of the players have colors, or all of them have unique ones)
        """

        colors = set()
        for p in players:
            if p.get_color() is None:
                continue
            colors.add(p.get_color())
        if len(colors) != 0 and len(colors) != len(players):
            raise ValueError("Each player does not have a unique assigned color.")
        
        if len(colors) == 0:
            for i, p in enumerate(players):
                p.set_color(BoardPlayer.POSSIBLE_COLORS[i])
        

    def __remove_player(self, color):
        """Remove a player of a given color from the game along with his penguins
        and add him to the violator list.

        color:  The color of the player to remove.
        """
        self.state.remove_player(color)
        self.violators.append(self.players[color])


    def __player_thread(self, func, arg, queue):
        """Helper to put threaded function return value in a queue.

        Puts None in the queue if an exception occurs.

        func:   The player function to run.
        arg:    The player function argument.
        queue:  The queue to put the result in.
        """
        try:
            queue.put(func(arg))
        except Exception as exc:
            #print(exc)
            queue.put(None)

    def run_turn(self):
        """ Perform a single turn of the game of fish. If the game is over, the function exits before the referee
        makes any calls to the game state.
        """

        all_placed = self.state.all_avatars_placed()
        color = self.__get_next_turn(all_placed)
        if color is None:
            return

        if not all_placed:
            # placement round
            func = self.players[color].make_placement
        else:
            # movement round
            func = self.players[color].make_move

        queue = Queue()
        thread = Thread(target=self.__player_thread, args=[func, deepcopy(self.state), queue])
        thread.daemon = True
        thread.start()
        thread.join(self.timeout)
        if thread.is_alive():
            #print("The " + str(color) + " player timed out and will be removed.")
            self.__remove_player(color)
            return

        action = queue.get()
        if action == None:
            #print("The " + str(color) + " player crashed and will be removed.")
            self.__remove_player(color)
            return

        if not all_placed:
            if self.state.valid_placement(action, color):
                self.state.place_avatar(action, color)
            else:
                #print("The " + str(color) + " player has attempted an invalid placement and will be removed.")
                self.__remove_player(color)
        else:
            if self.state.valid_move(*action):
                self.state.move_avatar(*action)
            else:
                #print("The " + str(color) + " player has attempted an invalid move and will be removed.")
                self.__remove_player(color)

    def __get_next_turn(self, all_placed):
        """Pass the turn in the current game state to the next player. Return the color of the player, or 
        None if the game is over."""

        game_over = self.is_game_over()
        if all_placed:
            if game_over:
                return None
            else:
                self.state.pass_turn_if_applicable()
        color = self.state.whose_turn().get_color()
        return color

    def run(self):
        """ Begin the game of Fish.

        The referee will begin the game and start taking moves from players.
        The game will continue until it has ended.
        Players who attempt invalid placements or movements, take too long to respond, or otherwise crash
        will be ejected from the game and their penguins will be removed.
        """
        while True:
            if self.is_game_over():
                break
            self.run_turn()

    def get_scores(self):
        """Get the player scores.

        returns:    A list of players and their scores (Player, score).
        """
        return [(self.players[p.get_color()], p.get_score()) for p in self.state.get_players()]


    def get_victors(self):
        """Get the victor(s) if the game is over. Players in the violators list are not eligible for victory.

        returns:    A list of winning Players if the game is over, None if it is not.
        """
        if self.is_game_over():
            scores = [p.get_score() for p in self.state.get_players()]
            if len(scores) == 0:
                return []
            max_score = max(scores)
            victors = []
            for p in self.state.get_players():
                if p.get_color() not in self.violators and p.get_score() == max_score:
                    victors.append(self.players[p.get_color()])
            return victors
        else:
            return None


    def is_game_over(self):
        """Is the game over?

        returns:    True if the game is over, False otherwise.
        """
        return self.state.all_avatars_placed() and self.state.is_game_over()


    def get_violators(self):
        """Get a rule violators who have been ejected.

        returns:    A list of violating Players.
        """
        return self.violators

    def get_current_state(self):
        """Get a copy of the current state.

        returns:    A copy of the current game state.
        """

        return deepcopy(self.state)
