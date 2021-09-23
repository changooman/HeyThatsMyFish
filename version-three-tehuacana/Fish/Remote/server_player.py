from Fish.Common.player_interface import PlayerABC
from Fish.Common.board_player import BoardPlayer
from Fish.Player.player import Player
from Fish.Admin.client import TournamentPlayer
from Fish.Remote.client_player import ClientPlayer

import Fish.Remote.communication as comm

import socket
import json
import copy
import time

NAME_BUFFER_SIZE = 32

class ServerPlayer(TournamentPlayer):
    """Representation of a server player that can receive placements and moves
    over a TCP connection. Has the same interface as a logical Player component.
    This is a representation of a remote client that the server uses to
    communicate with remote players.

    self.sock:          The TCP socket that is connected to a client. This client
                        is reponsible for sending moves and placements from a
                        remote connection.
    self.name:          The name of this player as received from the socket.
    self.prev_actions:  The actions already taken by this player from previous
                        'take_turn' calls
    self.timeout:       The timeout for receiving calls from the client
                        associated with this player connection.
    """

    def __init__(self, sock, timeout=1.0):
        """Initialize the player with it's color, socket, and name for the
        current game.

        sock (socket): the TCP socket used to get moves and placements from a
                remote client. This socket is expected to be open and
                ready to receive information from. This socket should
                be the result of an accept() call to the server socket.
        timeout (float): the timeout to wait for data from the client when doing
                recv calls.

        raises: socket.error if the socket reports an error, socket.timeout if the socket times out,
        ValueError the name is not alphabetical ASCII characters or is an empty string
        """
        # We use a Player() here since TournamentPlayer requires an instance of a player,
        # but we don't use the player for anything except setting and getting the color
        super(ServerPlayer, self).__init__(Player())
        self.sock = sock

        self.timeout = timeout
        self.sock.settimeout(self.timeout)
        self.prev_actions = []
        self.name = json.loads(sock.recv(NAME_BUFFER_SIZE))

        if not ClientPlayer.is_name_valid(self.name):
            raise ValueError("The name received by the client is not valid.")

    def make_placement(self, state):
        """Make a placement using a remote player. The remote player will receive
        a serialized form of the game state, which will be used to generate a
        placement. The remote player will then send a message that can be
        deserialized into a placement.
        
        state: the current game state

        returns (tuple): a tuple representing the (row, col) placement
        """
        return comm.setup(self.sock, state)

    def make_move(self, state):
        """Make a move using a remote player. The remote player will receive
        a serialized form of the game state and a list of previously made
        actions, which will be used to generate a move. The remote player
        will then send a message that can be deserialized into a move.
        
        state: the current game state

        returns (tuple): a 2-tuple of tuples, the first representing the
        (row, col) to move from, and the second representing the (row, col)
        to move to.
        """
        move = comm.take_turn(self.sock,
                              state, copy.deepcopy(self.prev_actions))
        self.prev_actions.append(move)
        return move

    def set_color(self, color):
        """Set the color of this Player. The color is sent to the remote player,
        as well as the colors of the other players.

        color:  The color to set this Player as.
        """
        super(ServerPlayer, self).set_color(color)
        self.__send_color()
        self.__send_other_colors()

    def inform_start(self):
        """Inform this player that the tournament is starting.
        """
        comm.start(self.sock, True)

    def inform_end(self, winner):
        """Inform this player that the tournament is ending.
        
        winner (bool): True if this player won, False otherwise.
        """
        comm.end(self.sock, winner)

    def __send_color(self):
        """Send the color of this Player to the client.
        """
        comm.play_as(self.sock, self.get_color())

    def __send_other_colors(self):
        """Send the colors of the players who are NOT this player.
        """
        colors = copy.copy(BoardPlayer.POSSIBLE_COLORS)
        colors.remove(self.get_color())
        comm.play_with(self.sock, colors)
