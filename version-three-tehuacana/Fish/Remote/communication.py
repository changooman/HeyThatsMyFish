"""
Representation of a remote communication layer to send and receive
method calls between clients and servers. Each pubic function corresponds
to a method call of the communication protocol. Each of these functions
should be used by the server to send protocol methods to clients and receive
back the clients return value.
"""

import socket
import json
import time

METHOD_CALL_BUFFER_SIZE = 65536

VOID = "void"
START = "start"
PLAY_AS = "playing-as"
PLAY_WITH = "playing-with"
SETUP = "setup"
TAKE_TURN = "take-turn"
END = "end"

def __send_msg(sock, msg_type, msg_args):
    """Send a message over the given socket.

    sock (socket): a socket capable of sending and receiving
        messages to and from a client.
    msg_type (str): the type of message to send to the client
        ('start', 'play-as', etc.)
    msg_args (list): a list of arguments to send with the message

    raises: socket.error if not all the data is sent or the socket reports an error, or the socket
        times out
    """

    json_msg = json.dumps([msg_type, msg_args])
    bytes_left = sock.sendall(json_msg)
    time.sleep(0.1)

    if bytes_left is not None:
        raise socket.error("Socket could not send all data")

def __recv_data(sock, msg_type):
    """Receive the return value of a method call.

    sock (socket): a socket capable of sending and receiving
        messages to and from a client.
    msg_type (str): the type of message to send to the client
        ('start', 'play-as', etc.). Must be either 'setup',
        'take-turn', or 'void' (indicating a void function)
        or a ValueError is raised

    return: if msg_type is 'setup', a 2-tuple representing the
        (row, col) to place a penguin is returned. If the msg_type
        is 'take-turn', a penguin Movement is returned (see `take_turn`
        for more information). If the message returns void, return the string
        "void", as returned from the server.If no information was returned
        from the server, return None.

    raise: socket.error if the socket reports an error or times out
    """

    msg = ""
    msg = sock.recv(METHOD_CALL_BUFFER_SIZE)
    if msg == "":
        return None

    msg = json.loads(msg)

    if msg_type == SETUP:
        return (msg[0], msg[1])
    elif msg_type == TAKE_TURN:
        return ((msg[0][0], msg[0][1]), (msg[1][0], msg[1][1]))
    else:  # msg_type == VOID
        return msg


def start(sock, tournament_starting):
    """Send a message to a client telling the client
    that the tournament is starting.
    
    sock (socket): a socket capable of sending and receiving
        messages to and from a client.
    tournament_starting (bool): True if the tournament
        is starting, False otherwise.

    raises: socket.error if the socket reports an error for any reason
        if all data is not successfully sent, or there is a timeout.
    """
    __send_msg(sock, START, [tournament_starting])
    __recv_data(sock, VOID)

def end(sock, winner):
    """Send a message to a client telling them that the
    tournament is ending.

    sock (socket): a socket capable of sending and receiving
        messages to and from a client.
    winner (bool): True if this client was the winner, False
        otherwise.

    raises: socket.error if the socket reports an error for any reason
        if all data is not successfully sent, or there is a timeout.
    """
    __send_msg(sock, END, [winner])
    __recv_data(sock, VOID)

def play_as(sock, color):
    """Send a message to a client telling them what color they are in
    an individual game of fish.

    sock (socket): a socket capable of sending and receiving
        messages to and from a client.
    color (str): one of "red", "white", "brown" or "black", denoting
        the color of this player.

    raises: socket.error if the socket reports an error for any reason
        if all data is not successfully sent, or there is a timeout.
    """
    __send_msg(sock, PLAY_AS, [color])
    __recv_data(sock, VOID)

def play_with(sock, colors):
    """Send a message to a client telling them the colors of the other
    players in the individual game of fish.

    sock (socket): a socket capable of sending and receiving
        messages to and from a client.
    color (list): a list of colors (one of "red", "white", "brown" or "black"),
        denoting the colors of other players in the individual game of fish.

    raises: socket.error if the socket reports an error for any reason
        if all data is not successfully sent, or there is a timeout.
    """
    __send_msg(sock, PLAY_WITH, [colors])
    __recv_data(sock, VOID)

def setup(sock, state):
    """Send a message to the client requesting a penguin placement in
    accordance to the strategy of the client. Return the placement
    requested by the client.

    sock (socket): a socket capable of sending and receiving
        messages to and from a client.
    state (State): the game state to send to the player for a penguin
        placement.

    return (tuple): a tuple representing the (row, col) to place a penguin
        at.

    raises: socket.error if the socket reports an error for any reason
        if all data is not successfully sent, or there is a timeout.
    """
    __send_msg(sock, SETUP, [state.json_rep()])
    return __recv_data(sock, SETUP)

def take_turn(sock, state, actions):
    """Send a message to a client requesting a penguin Movement in
    accordance to the strategy of the client. Return the penguin
    Movement requested by the client.

    A Movement is a 2-tuple, where the first tuple is the (row, col)
    to move from, and the second tuple is the (row, col) to move to.

    sock (socket): a socket capable of sending and receiving
        messages to and from a client.
    state (State): the game state to send to the player for a penguin
        move.
    actions (list): a list of Movements that this client has previously taken.

    return (Movement): the Movement requested by the client.

    raises: socket.error if the socket reports an error for any reason
        if all data is not successfully sent, or there is a timeout.
    """
    __send_msg(sock, TAKE_TURN, [state.json_rep(), actions])
    move = __recv_data(sock, TAKE_TURN)
    return move
