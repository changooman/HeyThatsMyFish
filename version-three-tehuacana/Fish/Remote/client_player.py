from Fish.Player.player import Player
from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.tile import Tile
from Fish.Common.state import State

import Fish.Remote.communication as comm

import socket
import json
import time

MAX_NAME_LEN = 12

class ClientPlayer(Player):
    """Class to represent a client-side player that will connect to a
    remote server using a TCP connection. This player encapsulates the
    connection information required to communicate with a server
    """

    def __init__(self, server_ip, port, name, depth=2, timeout=1.0, connection_timeout=None):
        """Initialize a client player. This involves connecting to the server
        found at the given IP and port, and immediately sending the player's name to
        the server. The client has no timeout (or the value of connection_timeout, if given)
        when it is attempting to connect and send the name to the server; once the client
        receives the `start` message from the server, the value of `timeout` is set to be the
        timeout of the client.

        server_ip (str):            the IP to connect to
        port (str):                 the port to use
        name (str):                 the name of this player
        depth (int):                the depth of the search tree to use for finding optimal moves
        timeout (float):            the timeout of the client after receiving the `start` message. This timeout
                                        is the time to wait for the server to send a message to the client when
                                        the client calls `recv`
        connection_timeout (float): the timeout of the client when awaiting connection and
                                        sending the name of the player. This timeout is the amount
                                        of time the client will wait after calling `start` to get a
                                        start message from the server. 

        raise: ValueError if the name is not a valid name (< 12 ASCII
        alphabetic chars), socket.error if the socket fails to connect for any reason,
        or the socket cannot send the name for any reason.
        """
        super(ClientPlayer, self).__init__(depth=depth)

        if not self.is_name_valid(name):
            raise ValueError("The given name is invalid.")
        self.name = name
        self.timeout = timeout

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(connection_timeout)
        
        self.sock.connect((server_ip, port))

        # send name as JSON string
        self.__send_data(json.dumps(name))


    def start(self):
        """Let the client start listening for messages. The first message that will arrive is a
        start message."""

        self.__wait_for_next_msg([comm.START])


    @staticmethod
    def is_name_valid(name):
        """Validate that the name received from the client is at most 12
        alphabetic ASCII characters and not an empty string.

        Returns True if the name is valid, False otherwise.
        """

        if name == "":
            return False

        if len(name) > MAX_NAME_LEN:
            return False

        try:
            name.decode("ascii")
        except UnicodeDecodeError:
            return False

        return True


    def __send_data(self, data):
        """Send data over this client's socket.

        data (str): the data to send over the socket, as a string

        raises: socket.error if the socket returns an error or the socket can't
            send all the data or if the socket times out. In this case, the socket
            is shutdown and closed.
        """

        try:
            bytes_left = self.sock.sendall(data)
        except socket.error as e:
            self.__shutdown_and_close()
            raise e

        time.sleep(0.1)

        if bytes_left is not None:
            self.__shutdown_and_close()
            raise socket.error("Socket could not send all data")

    def __send_void(self):
        """Send a void message over this client's socket.

        raises: if the socket returns an error, times out,
            or does not send all the data requested.
        """

        self.__send_data(json.dumps("void"))

    def __recv_data(self):
        """Receive data from the server using this client's socket

        return (str): the data received from the server. None if no data was
                received.

        raises: if the socket returns an error or the socket times
                out. The socket is shutdown and closed when an error is reported
        """
        
        try:
            msg = self.sock.recv(comm.METHOD_CALL_BUFFER_SIZE)
        except socket.error as e:
            self.__shutdown_and_close()
            raise e

        if len(msg) == 0:
            return None

        return msg

    def _handle_start_msg(self):
        """Handle a start message when one is received. Involves setting the
        timeout and sending a void message back to the server.
        
        The next expected message is a `play_as` message.

        raises: if any messages cannot be sent to the server for
                any reason.
        """
        self.sock.settimeout(self.timeout)
        self.__send_void()
        self.__wait_for_next_msg([comm.PLAY_AS])


    def _handle_play_as_msg(self, color):
        """Handle a 'play_as' message. Sets the color to the given color, and sends void
        back to the server. The next expected message is a `play_with` message.

        color (str): the color to set this player to.

        raises: if any messages cannot be sent to the server for
                any reason.
        """
        self.set_color(color)
        self.__send_void()
        self.__wait_for_next_msg([comm.PLAY_WITH])


    def _handle_play_with_msg(self, _colors):
        """Handle a 'play_with' message. This implementation does not
        need the other player's colors, so it is discarded. Sends void and
        awaits a setup message.

        raises: if any messages cannot be sent to the server for
                any reason.
        """
        self.__send_void()
        self.__wait_for_next_msg([comm.SETUP])


    def _handle_setup_msg(self, state):
        """Handle a 'setup' message. Uses the given state to make an avatar
        placement on the board of the state, and sends the placement back to
        the server.

        Awaits another `setup` message, a `take_turn` message
        (representing the movement of an avatar), a `play_as` message (the
        start of a new round of Fish), or an `end` message (where no one
        can make moves).

        state (State): the state to use to place an avatar.

        raises: if any messages cannot be sent to the server for
                any reason.
        """
        placement = self.make_placement(state)
        placement = list(placement)
        self.__send_data(json.dumps(placement))
        self.__wait_for_next_msg([
            comm.SETUP, comm.TAKE_TURN, comm.END, comm.PLAY_AS])


    def _handle_take_turn_msg(self, state, _actions):
        """Handle a 'take_turn' message. Uses the given state to move an avatar
        on the board of the state, and sends the move back to the server. The
        given list of previous actions is not used for this implementation and
        ignored.

        Awaits another `take_turn` message a `play_as` message (the
        start of a new round of Fish), or an `end` message (where no one
        can make moves).

        state (State): the state to use to place an avatar.
        _actions (list): the list of previous actions made by this player. Ignored.

        raises: if any messages cannot be sent to the server for
                any reason.
        """
        move = self.make_move(state)
        move = [list(move[0]), list(move[1])]
        self.__send_data(json.dumps(move))
        self.__wait_for_next_msg([comm.TAKE_TURN, comm.END, comm.PLAY_AS])
        

    def _handle_end_msg(self, win):
        """Handle an 'end' message. The actual result of the game presented by
        `win` is ignored for this implementation of a client. This message also
        shuts down and closes the server.

        This message is the final message and no other messages should follow.

        win (bool): True if the player won the tournament, False otherwise.

        raises: if any messages cannot be sent to the server for
                any reason.
        """
        self.__send_void()
        self.__shutdown_and_close()


    def __shutdown_and_close(self):
        """Shutdown and close the socket"""
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


    def __handle_next_msg(self, msg_type, data):
        """Handle the next message received by the server by delegating it to the
        appropriate helper function.

        msg_type (str): the type of message
        data (list): the message loaded from JSON received by the server
        """

        if msg_type == comm.START:
            self._handle_start_msg()
        elif msg_type == comm.PLAY_AS:
            self._handle_play_as_msg(data[1][0])
        elif msg_type == comm.PLAY_WITH:
            self._handle_play_with_msg(data[1][0])
        elif msg_type == comm.SETUP:
            state = State.json_to_state(data[1][0])
            self._handle_setup_msg(state)
        elif msg_type == comm.TAKE_TURN:
            #print("made it to take_turn")
            state = State.json_to_state(data[1][0])
            self._handle_take_turn_msg(state, [])
        elif msg_type == comm.END:
            self._handle_end_msg(data[1][0])


    def __wait_for_next_msg(self, next_msg_types):
        """Wait for the next message with one of the given message types. A message is
        received from the server and handled according to its "type" field. This
        function terminates when the `end` message is received, since all _handle
        functions call this function again, with the exception of _handle_end_msg.

        If a problem is reported by the socket, the socket is shutdown and closed
        
        next_msg_types (list): a list of message types (strings) denoting what
            message to expect next.
        
        raises: ValueError if the next message received from the server is a
            type other than one of the types given.
            socket.error if data cannot be sent to or received by the server
            for any reason.
        """
        data = self.__recv_data()
        if data is None:
            self.__shutdown_and_close()
            raise socket.error("Peer closed connection!")
        data = json.loads(data)
        msg_type = data[0]
        #print(msg_type)
        if msg_type not in next_msg_types:
            raise ValueError("Unexpected message type {}".format(msg_type))

        self.__handle_next_msg(msg_type, data)