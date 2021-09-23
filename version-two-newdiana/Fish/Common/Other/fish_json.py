import json
import sys

from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State
from Fish.Common.tile import Tile


def read_json():
    """ Read a JSON object from STDIN.

    returns:    A JSON object in dictionary form.
    """
    decoder = json.JSONDecoder()
    stdin = sys.stdin.read().strip()
    return decoder.raw_decode(stdin)[0]


def board_from_json(obj):
    """ Create a Board from a JSON object.

    obj:    The JSON object.

    returns:    A Board.
    """
    rows = len(obj)
    cols = max([len(row) for row in obj])
    board = Board(rows, cols)

    for r in range(rows):
        for c in range(cols):
            if c >= len(obj[r]) or obj[r][c] == 0:
                board.remove_tile((r, c))
            else:
                board.tiles[r][c] = Tile(False, obj[r][c])
    return board


def players_from_json(obj):
    """ Create a list of BoardPlayers from a JSON object.

    obj:    The JSON object.

    returns:    A list of BoardPlayers.
    """
    players = []
    for p_json in obj:
        p = BoardPlayer(p_json["color"])
        p.set_score(p_json["score"])
        for penguin in p_json["places"]:
            p.add_penguin(tuple(penguin))
        players.append(p)
    return players


def state_from_json(obj):
    """ Create a State from a JSON object.

    obj:    The JSON object.

    returns:    A State.

    throws:     A ValueError if there are penguins located on holes in the board.
    """
    players = players_from_json(obj["players"])
    board = board_from_json(obj["board"])
    for player in players:
        for penguin in player.get_penguins():
            if board.get_tile(penguin) is None:
                raise ValueError("Penguin at " + str(penguin) + " is not on a tile.")
    return State(players, board)
