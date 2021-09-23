"""Representation of a server running a tournament of Fish using
remote players.
"""

from Fish.Remote.server_player import ServerPlayer
from Fish.Admin.manager import Manager
import Fish.Remote.communication as comm

import socket
from threading import Thread
from Queue import Queue

MIN_CLIENTS = 5
MAX_CLIENTS = 10
BACKLOG = 999

def __accept_remote_player(sock):
    """Listen for a remote player. If a connection is accepted,
    return the socket object that was created when the connection was
    accepted. If there is a timeout, return None. If the socket errors
    for any other reason, raise a ValueError.

    sock (socket): a TCP socket used for accepting incoming connections
        (which themselves are the remote clients that will be participating
        in the tournament.) This socket must already be bound to a valid
        address and port, and must be ready to receive incoming connections.
    
    return (socket): the socket representing the remote client, or None
        if the connection timed out.

    raises: socket.error if the socket reports an error for any reason  
    """
    return sock.accept()[0]  # we only care about the socket, not the addr

def __waiting_period(sock, queue, players_in_list):
    """Keep looking for players and accept their connections when found.
    Add the socket to queue when found. This function will be ran in a
    thread so that it we can time out the thread and check if we have enough
    players to start a game.

    sock (socket): the socket to listen for connections from
    queue (Queue): the queue to store new connections in
    players_in_list (int): the number of players already in the list
        when this function was called
    """
    # this condition is false when we call a second time and we already had
    # enough players
    while players_in_list < MAX_CLIENTS:
        remote_socket = None
        try:
            remote_socket = __accept_remote_player(sock)
        except socket.error:
            # socket had an error at this point, try again
            continue
        queue.put(remote_socket)
        players_in_list += 1
        if players_in_list == MAX_CLIENTS:
            break

def __get_remote_players_helper(sock, players, waiting_period, timeout):
    """Helper function to add players that have been accepted by the server

    sock (socket): a TCP socket used for accepting incoming connections
        (which themselves are the remote clients that will be participating
        in the tournament.) This socket must already be bound to a valid
        address and port, and must be ready to receive incoming connections.
    players (list): a list of ServerPlayers that will participate in this game.
    waiting_period (float): the amount of time to wait for connections for a single
        period. The server will run the waiting period twice.
    timeout (float): the timeout to give each server player.
    """

    # leave early if we already have enough people
    if len(players) == MAX_CLIENTS:
        return

    players_in_list = len(players)

    queue = Queue()
    thread = Thread(target=__waiting_period, args=[sock, queue, players_in_list])
    thread.start()
    thread.join(waiting_period)

    while not queue.empty():
        players.append(ServerPlayer(queue.get(), timeout=timeout))
        if len(players) == MAX_CLIENTS:
            break

def __get_remote_players(sock, waiting_period, timeout):
    """Get the remote players who will be participating in the tournament.
    
    sock (socket): a TCP socket used for accepting incoming connections
        (which themselves are the remote clients that will be participating
        in the tournament.) This socket must already be bound to a valid
        address and port, and must be ready to receive incoming connections.
    waiting_period (float): the amount of time to wait for connections for a single
        period. The server will run the waiting period twice.
    timeout (float): the timeout to give each server player.
    
    return (dict, list): a dictionary mapping the name of a player to the
    ServerPlayer and a list of ServerPlayers who will be participating. Returns
    None for both fields if the number of players who connected was less than
    MIN_CLIENTS. If there are less than MIN_CLIENTS in the list, return None
    for both fields.
    """

    players = []
    #old_timeout = sock.gettimeout()

    # we stop the socket timeout here because we use a thread timeout to wait
    # the 30s for players
    # we reset this after we are finished getting the players

    __get_remote_players_helper(sock, players, waiting_period, timeout)
    if len(players) < MIN_CLIENTS:
        __get_remote_players_helper(sock, players, waiting_period, timeout)
    if len(players) < MIN_CLIENTS:
        return (None, None)

    name_to_players = {p.name: p for p in players}

    #sock.settimeout(old_timeout)
    return name_to_players, players

def __get_names(winners, violators, name_to_players):
    """Get the names of the players who won.
    
    winners (list): the list of winning players
    violators (list): the list of players who violated (cheated/kicked)
    name_to_players (dict): a mapping between player names and the player

    return (tuple): a 3-tuple, where the first element is a list of the names
        of the winners, the second element is a list of the names of the losers,
        and the third element is a list of the names of violators
        (cheating/kicked players).
    """

    winners = set(winners)
    violators = set(violators)
    win_names = []
    lose_names = []
    violator_names = []
    for name in name_to_players.keys():
        if name_to_players[name] in winners:
            win_names.append(name)
        elif name_to_players[name] in violators:
            violator_names.append(name)
        else:
            lose_names.append(name)
    return (win_names, lose_names, violator_names)

def __shutdown_and_close(sock):
    """Shutdown and close the given socket object"""
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def __setup_socket(ip, port):
    """Setup the socket to use for incoming connections

    ip (str): the IP address to bind the server to.
    port (int): the port to use for this server.

    return (socket): the socket to use to listen for incoming connections.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(BACKLOG)
    sock.settimeout(None)
    return sock

def run_tournament(ip, port, board=None, waiting_period=30.0, timeout=1.0):
    """Run a tournament using remote players. The given IP and port are used to
    open a server to which clients can connect. The given IP and port are expected
    to be valid for opening a server. Players who join are accepted and stored in
    order of connection to the server, and are passed to the tournament manager in
    that order.
    
    ip (str): the IP address to bind the server to.
    port (int): the port to use for this server.
    board (Board): an optional board to use in a tournament. Default option is
        None, in which case the board size is dependent on the number of players
        in each individual game, and the number of fish is per tile is randomized
        (there are no holes)
    waiting_period (float): the amount of time to wait for connections for a single
        period. The server will run the waiting period twice.
    timeout (float): the timeout to give each server player.
    
    return (tuple): a 3-tuple, where the first element is a list of the names
        of the winners, the second element is a list of the names of the losers,
        and the third element is a list of the names of violators
        (cheating/kicked players). If there are less than MIN_CLIENTS in the
        game, return None
    """

    sock = __setup_socket(ip, port)

    name_to_player, remote_players = __get_remote_players(sock, waiting_period, timeout)
    if remote_players is None:
        __shutdown_and_close(sock)
        return None
    manager = Manager(remote_players, board=board, timeout=timeout)
    winners = manager.run()
    for players in remote_players:
        __shutdown_and_close(players.sock)
    __shutdown_and_close(sock)
    return __get_names(winners, manager.violators, name_to_player)
