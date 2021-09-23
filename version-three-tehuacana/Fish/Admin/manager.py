from Fish.Admin.referee import Referee
from Fish.Common.board_player import BoardPlayer

from copy import copy
from math import sqrt
from Queue import Queue
from threading import Thread

class Manager():
    """Represents a tournament manager that will run a single
    game tournament until a winner or several winners emerge.

    self.players:               A list of TournamentPlayer participating in the tournament,
                                in ascending order of age.
    self.min_players_per_game:  The minimum number of players to place in a game.
    self.max_players_per_game:  The maximum number of players to place in a game.
    self.player_indices:        A dictionary of Players and their indices in self.players to aid in
                                sorting lists of Players by age.
    self.INFORM_PLAYER_SUCCESS: A constant indicating success when informing a player of their tournament result.
    self.INFORM_PLAYER_FAILURE: A constant indicating failure when informing a player of their tournament result.
    self.timeout:               The amount of time each player has to accept a tournament result message.

    throws:                     Value error if min_players_per_game or max_players_per_game is < 1,
                                if min_players_per_game > max_players_per_game, or if the number of
                                players provided is less than min_players_per_game.
    """

    INFORM_PLAYER_SUCCESS = 0
    INFORM_PLAYER_FAILURE = 1

    def __init__(self, players, min_players_per_game=2, max_players_per_game=len(BoardPlayer.POSSIBLE_COLORS), board=None, timeout=1):
        """Initialize the tournament manager.

        self.players:               A list of TournamentPlayers participating in the tournament,
                                    in ascending order of age.
        self.min_players_per_game:  The minimum number of players to place in a game.
        self.max_players_per_game:  The maximum number of players to place in a game.
        self.board:                 The board to use for each game of Fish. Default option is None,
                                    in which case the board size is dependent on the number of players
                                    in each individual game, and the number of Fish is per tile is randomized
                                    (there are no holes). When None, the board is guaranteed to be big enough
                                    and have enough tiles to place all penguins. If the board is given,
                                    the board must be big enough and have enough valid tiles to support
                                    a three-player individual game of Fish (with 9 total avatars)

        raise (ValueError): if a board is given that cannot support 9 avatars (see self.board), or if
            1 <= min_players_per_game <= len(players) <= max_players_per_game is not satisfied
        """

        self.__check_player_count(players, min_players_per_game, max_players_per_game)
        self.players = copy(players)
        self.board = board

        if self.board is not None:
            if self.board.get_cols() * self.board.get_rows() - self.board.get_holes_in_board() < 9:
                raise ValueError("not enough valid tiles to place all avatars in a game with the max number of avatars placed")

        self.violators = []
        self.player_indices = {player: index for index, player in enumerate(players)}
        self.min_players_per_game = min_players_per_game
        self.max_players_per_game = max_players_per_game
        self.timeout = timeout

    @staticmethod
    def __check_player_count(players, min_players_per_game, max_players_per_game):
        """Validate that the number of players is within the min and max players per game
        and raise a value error if they are not."""
        if min_players_per_game < 1:
            raise ValueError("min_players_per_game must be >= 1.")
        if max_players_per_game < 1:
            raise ValueError("max_players_per_game must be >= 1.")
        if min_players_per_game > max_players_per_game:
            raise ValueError("min_players_per_game must be <= max_players_per_game.")
        if len(players) < min_players_per_game:
            raise ValueError("len(players) must be > min_players_per_game.")


    def run(self):
        """Run the tournament and notify the players of their final outcomes.

        returns:    A list of winning Players.
        """
        self.__inform_players_start()
        top_players = copy(self.players)
        while True:

            new_top_players = self.__run_round(top_players)
            if self.__tournament_over(top_players, new_top_players):
                break
            else:
                top_players = new_top_players

        # We inform losers by looking at all the players, and seeing if a given player is in new_top_players
        top_players = self.__inform_players_end(new_top_players)

        return top_players

    def __set_colors(self, group):
        """Set the color of each player in an individual grouping of players.
        
        group (list): a list of players in this round of fish

        returns: a list of players with their colors set.
        """
        for i, p in enumerate(group):
            p.set_color(BoardPlayer.POSSIBLE_COLORS[i])

    def __run_round(self, players):
        """Run a single round of the tournament.

        players:    The players participating in this tournament in order of ascending age.

        returns:    The winning players the round in order of ascending age.

        throws:     ValueError if players has less than two or more than 4, if the given board is not large enough,
                    or if the board does not have enough valid tiles to place penguins.
        """
        if len(players) < 2:
            raise ValueError("A round must be run with at least two Players.")

        top_players = []
        groups = self.__group_players(players)
        for group in groups:
            self.__set_colors(group)
            ref = Referee(group, self.__board_size(len(group)), board=self.board, timeout=self.timeout)
            ref.run()
            self.__remove_violators(ref.get_violators())
            top_players += self.__sort_players(ref.get_victors())
        return top_players


    def __group_players(self, players):
        """Group remaining active Players into game groups.
        A game group is a list of Players.

        Works by assigning players to maximally sized game groups in ascending order of age.
        If the remaining number of players is less than the maximal number of players per game,
        then the target number of players per game is reduced by one and the last game group
        is disbanded and added back into the remaining player pool. This continues until all
        players are assigned to a group.


        players:    A list of players to assign into game groups.

        returns:    A list of game groups.
        """
        group_size = self.max_players_per_game
        groups = []
        cur_group = []
        cur_player = 0
        while cur_player < len(players):
            cur_group.append(players[cur_player])
            cur_player += 1
            if len(cur_group) == group_size:
                groups.append(cur_group)
                cur_group = []
            elif cur_player == len(players):
                if len(cur_group) < self.min_players_per_game:
                    if len(groups) > 0:
                        groups.pop()
                        cur_player -= group_size
                    cur_player -= len(cur_group)
                    group_size -= 1
                    cur_group = []
                else:
                    groups.append(cur_group)
        return groups


    def __board_size(self, num_players):
        """Determine a suitable board size for a given number of players.

        This algorithm aims to create a board with a number of tiles of
        at least three times the number of total penguins on the board.

        num_players:    The number of players.

        returns:        A tuple (num_rows, num_columns).
        """
        num_tiles = 3 * (6 - num_players) * num_players
        side_size = int(sqrt(num_tiles) + 0.5)
        return (side_size, side_size)


    def __remove_violators(self, violators):
        """Remove players who have been ejected from the game from self.players, and add them to
        the violators list.

        violators:  A list of Players to remove.
        """
        violators = set(violators)
        self.players = [player for player in self.players if player not in violators]
        # all violators are unique because they are removed from self.players, so they are never
        # reused
        self.violators += violators


    def __sort_players(self, players):
        """Sort a list of players in ascending order of age based on self.players.

        players:    A list of Players to sort.

        returns:    The sorted list of Players.
        """
        return sorted(players, key=self.player_indices.get)


    def __tournament_over(self, prev_top_players, new_top_players):
        """Determine if the tournament is over.

        The tournament is over if two tournament rounds in a row produce the exact same winners,
        there are too few players for a single game, or the previous top players were few enough
        that they participated in a single game during the most recent tournament round.

        prev_top_players:   The previous top players before the most recent tournament round.
        new_top_players:    The top players after the most recent tournament round.

        returns:            True if the tournament is over, False otherwise.
        """
        return (prev_top_players == new_top_players or
                len(new_top_players) < self.min_players_per_game or
                len(prev_top_players) <= self.max_players_per_game)
        
    def __player_start_thread(self, func, queue):
        """Helper that runs a function to alert players that the tournament
        has started.

        func (function): the function to use to alert a player a tournament has
            started.
        queue (Queue): the queue to put the results of alerting a player in
        """
        try:
            func()
            queue.put(self.INFORM_PLAYER_SUCCESS)
        except:
            queue.put(self.INFORM_PLAYER_FAILURE)


    def __player_end_thread(self, func, win, queue):
        """Helper that runs a function and puts the status execution into a queue.

        self.INFORM_PLAYER_SUCCESS will be placed in the queue if the function executes
        successfully, otherwise self.INFORM_PLAYER_FAILURE will be placed in the queue.

        func:   The player function to run.
        win:    True if the player won, False otherwise.
        queue:  The queue to put the result in.
        """
        try:
            func(win)
            queue.put(self.INFORM_PLAYER_SUCCESS)
        except:
            queue.put(self.INFORM_PLAYER_FAILURE)

    def __inform_players_start(self):
        """Inform all active players of the start of a tournament."""
        for player in self.players:
            func = player.inform_start
            queue = Queue()
            thread = Thread(target=self.__player_start_thread, args=[func, queue])
            thread.daemon = True
            thread.start()
            thread.join(self.timeout)


    def __inform_players_end(self, top_players):
        """Inform all active players of their final tournament standing.
        Players that fail to accept this message become losers (i.e. they throw an exception
        or take longer than self.timeout).

        top_players:    The players who have won the tournament.
                        All other players in self.players will be informed that they have lost.

        returns:        top_players with Players that failed to accept victory removed.
        """
        new_top_players = copy(top_players)
        top_players = set(top_players)
        for player in self.players:
            func = player.inform_end
            win = None
            if player in top_players:
                win = True
            else:
                win = False
            queue = Queue()
            thread = Thread(target=self.__player_end_thread, args=[func, win, queue])
            thread.daemon = True
            thread.start()
            thread.join(self.timeout)
            if player in top_players:
                if thread.is_alive():
                    new_top_players.remove(player)
                else:
                    status = queue.get()
                    if status == self.INFORM_PLAYER_FAILURE:
                        new_top_players.remove(player)
        return new_top_players
