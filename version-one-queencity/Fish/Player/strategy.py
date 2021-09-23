import Tkinter as tk
from Tkinter import *
from Other.board import *
from Other.game_tree import *


# Purpose: Represents a basis for allowing the referee to host communication through its variety of functions calls.
# The player interface calls functionalities from the game tree to check the potential of a move in certain N turns.
# This mainly serves as an advising tool for players to determine what is the best course of action.
# It also allows the player to utilize a function that will place a penguin in the next available free spot starting
# from the top corner of the hexagon board down to the last hexagon.
"""
     O     
     <|\     A player which holds multiple penguins
      |     color: "red"             
      |\    age: 14
     / |      __
Penguins:
_{v}_    (v)     ('>    ( )
 /-\    //-\\    /V\   // \\
(\_/)   (\_/)   <(_)   (\=/)
 ^ ^     ^ ^      ~~    ~ ~
 (0,0)   (1,2)   (2,3) (1, 0), 
             _______
     _______/ (0,1) \_______
    / (0,0) \_______/ (0,2) \
    \_______/ (1,1) \_______/
    / (1,0) \_______/ (1,2) \
    \_______/       \_______/
    Players in the state:
    P1 P2
    Game Over? False
"""
class PlayerInterface:
    # Purpose: Constructs a PlayerInterface object
    # @param state, A GameState object which hosts critical data for helping direct function calls for certain players
    # Example: <state.GameState instance at 0x0000000002B7D048>
    # @param current_player The player associated with the PlayerInterface who will have the functions called on
    # Example: <__main__.Player instance at 0x0000000003456048>
    # @param players A list of players for helping update the
    #  [("red", 12), ("black", 21)]
    #  [<__main__.Player instance at 0x0000000003456048>, <__main__.Player instance at 0x0000000005556048>]

    def __init__(self, state, player, players):  # , player_protocol, render):
        self.current_state = state
        self.current_player = player
        self.players = players

    # Purpose: This function takes in a game tree and traverses all possible paths. It adds it to a list of all paths
    # and then checks the score of each path to determine which one has the most optimal score for the given player.
    # It assigns that path to best_path and reverses it to help illustrate where the path starts from and returns it.
    # If multiple paths have the same optimal score, it returns the first of the list. 
    # @param game_tree, the tree of x layers of possible moves from the current state
    # Example: <state.Game instance at 0x0000000002B7D048>
    # @param player, the player that we are finding the best path for
    # Example: <__main__.Player instance at 0x0000000003456048>
    #  ("red", 12)
    # @return path, a list of connected tree nodes that will constitute the best path
    # Example: [(3, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>)]
    def best_path(self, game_tree, player):
        all_paths, origin_list = self.get_all_paths(game_tree)
        best_path = self.check_best_path(origin_list, player, game_tree)
        scorelist = self.check_scores(best_path, player)
        scorelist.sort(reverse=True, key=lambda x: x[1])
        best_path = self.get_path(scorelist[0][2], all_paths)
        best_path.reverse()
        return best_path

    # Purpose: checks all items in origin list and returns the best items per branch grouping into a list called
    # best path, it also compares the scores for each player differently to make sure we are taking into account the
    # priorities of each player (current player trying to get the highest score, other players trying to sabotage the
    # current player). For the current player it checks each given node it looks at all the nodes that branch off it
    # and compares the scores. For the other players it checks the branches of the branches to get the greatest of those
    # so that the other player can chose the move that minimizes the current player's possible score.
    # @param origin_list, a list of tuples that contain an origin node and a list of nodes that branch off said node
    # [(3, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>),
    # (2, <state.GameState instance at 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)
    # ]
    # @param player, the current player that is looking for the best move
    # @param player, the player that we are finding the best path for
    # Example: <__main__.Player instance at 0x0000000003456048>
    #  ("red", 12)
    # @param game_tree, the tree of possible moves from the current state that is x layers deep
    # Example: <state.Game instance at 0x0000000002B7D048>
    # @return best_path, a list of best nodes for each grouping of children nodes
    # [(2, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>),
    # (2, <state.GameState instance at 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)]
    def check_best_path(self, origin_list, player, game_tree):
        i = 0
        best_path = []
        for i in range(3):
            for node in game_tree:
                best_state = ''
                best_node = ''
                if node[0] == i:
                    for item in origin_list:
                        if node[1] == item[0]:
                            best_score = 0
                            for state in item[1]:
                                for a_player in self.players:
                                    if a_player.color == player.color:
                                        temp = a_player.get_score(a_player, node[1])
                                        if temp > best_score:
                                            best_score = temp
                                            best_state = state
                                    else:
                                        for item in origin_list:
                                            if node[1] == item[0]:
                                                best_score = -1
                                                for inner_state in item[1]:
                                                    temp = a_player.get_score(a_player, node[1])
                                                    if temp > best_score:
                                                        best_score = temp
                                                        best_state = state
                self.check_nodes(best_state, best_path, game_tree)
            i += 1
        return best_path

    # Purpose: checks the nodes in a tree and appends the best node of a given state to the best path list
    # used in check_best_path.
    # @param best_state, a given state that is the best for a group of children
    # Example: <state.Game instance at 0x0000000002B7D048>
    # @param best_path, the list of best nodes of each grouping of children nodes
    # Example: [(2, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>),
    #  (2, <state.GameState instance at 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)]
    # @param game_tree, the tree of possible moves from the current state that is x layers deep
    # Example: <state.Game instance at 0x0000000002B7D048>
    def check_nodes(self, best_state, best_path, game_tree):
        for tree_node in game_tree:
            if tree_node[1] == best_state:
                best_node = tree_node
                best_path.append(best_node)

    # Purpose: checks the scores for each node in the best_path list and returns a complete list of the scores giving
    # a positive score for the current player and a negative score for the other players to show that the other players
    # are going to be trying to minimize the current player's score so when checking the greater scores, a negative
    # score for other players will actually chose the node with the lowest score
    # @param best_path, the list of best nodes of each grouping of children nodes
    # Example: [(2, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>),
    #  (2, <state.GameState instance at 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)]
    # @param player, the current player that is looking for the best move
    # Example: <__main__.Player instance at 0x0000000003456048>
    #  ("red", 12)
    # @return scorelist, the list of all scores from the nodes in best path that are being checked
    # Example: [1,2,4,-1,4,0]
    def check_scores(self, best_path, player):
        scorelist = []
        index = 0
        for node in best_path:
            if node[0] == 3:
                state_score = 0
                players_ = node[1].players
                for a_player in players_:
                    if a_player.color == player.color:
                        state_score += a_player.get_score(a_player, node[1])
                    else:
                        state_score += -1 * a_player.get_score(a_player, node[1])
                state_score = (index, state_score, node)
                scorelist.append(state_score)
                index += 1
        return scorelist

    # Purpose: gets a list of all the possible paths in a tree by going up from the last node to the starting node and
    # continuing off each last node's origin point. It also returns a list of all the origin states and their children
    # in a tuple, the 0th item being the origin state, and the 1st item being a list of all nodes that branch from said
    # origin state. It was optimal to put them in the same loop to reduce run time and avoid repeating code.
    # @param: game_tree, the tree of possible moves from the current state that is x layers deep
    # Example: <state.Game instance at 0x0000000002B7D048>
    # @return: allpaths, a list of all possible paths in the given tree
    # Example: [(2, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>),
    #  (2, <state.GameState instance at 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)]
    # @return: origin_list, a list of tuples that contain an origin node and a list of nodes that branch off said node
    # Example: [(2, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>),
    #  (2, <state.GameState instance at 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)]
    def get_all_paths(self, game_tree):
        allpaths = []
        lastlayer = game_tree[len(game_tree) - 1][0]
        nodevalid = 0
        origin_list = []
        for node in game_tree:
            path = []
            if node[0] == lastlayer:
                nodevalid += 1
                pathachieved = False
                nextlayer = lastlayer
                while not pathachieved:
                    origin_list = self.update_origin_list(node, origin_list)
                    path.append(node)
                    originnode = node
                    nextlayer = nextlayer - 1
                    if nextlayer == -1:
                        break
                    for item in game_tree:
                        if item[0] == nextlayer and item[1] == originnode[2]:
                            node = item
                allpaths.append(path)
        return allpaths, origin_list

    # Purpose: updates the list of tuples that contain in the 0th element origin nodes and in the 1st element a list of
    # nodes that branch off said origin node, when the origin node is not contained in the list already it will be
    # added with the child node that it is found with first. If it is already in the list then the node that is being
    # looked at will be appended to the list of children
    # @param node, a given node in a game_tree
    # Example: (2, < state.GameState instance at 0x0000000002B7D048 >,
    # < state.GameState instance at 0x0000000002B7D044 >)
    # @param origin_list, a list of tuples that contain an origin node and a list of nodes that branch off said node
    # Example: [(2, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>),
    #  (2, <state.GameState instance at 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)]
    # @return origin_list, a list of tuples that contain an origin node and a list of nodes that branch off said node
    # Example: [(2, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>),
    #  (2, <state.GameState instance at 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)]
    def update_origin_list(self, node, origin_list):
        if len(node) == 4:
            added = False
            origin_state = node[2]
            for item in origin_list:
                if item[0] == origin_state:
                    if node[1] not in item[1]:
                        item[1].append(node[1])
                    added = True
            if not added:
                origin_list.append((origin_state, [node[1]]))
        return origin_list

    # Purpose: gets the path for a specific end node. checks each path in the list of all paths looking at the final
    # node, and if the given node matches the final node then the path being looked at is the actual and only path to
    # get to the given node. The function then returns this path.
    # @param end_node, a node in the last layer of a tree that will be the last node in a path
    # @param allpaths, a list of all the possible paths in a tree
    # Example: [(2, <state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D044>),
    #  (2, <state.GameState instance at 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)]
    # @return path, the path that starts with the starting state's node and ends with the given end_node
    # Example: [(0, <state.GameState instance at 0x0000000002B7D048>), (2, <state.GameState instance at
    # 0x0000000002B72484>, <state.GameState instance at 0x000000000227D044>)]
    def get_path(self, end_node, allpaths):
        for path in allpaths:
            if path[0] == end_node:
                return path

    # Purpose: gets the best possible move from a starting state in a game tree. Goes through the best path function to
    # get the optimal path for the given player and then checks the move required to get to the first node in the
    # path list (moves to get to a destination are provided in each node), and returns this. When checking the path
    # since the best_path function only returns one path we only need to check whether or not a node in the path is in
    # the first layer, then check the move that is associated with said node and return that.
    # @param game_tree, the tree of possible moves from the current state that is x layers deep
    # Example: <state.Game instance at 0x0000000002B7D048>
    # @param player, the current player that is looking for the best move
    # Example: <__main__.Player instance at 0x0000000003456048>
    #  ("red", 12)
    # @return best_move
    def best_move(self, game_tree, player):
        best_path = self.best_path(game_tree, player)
        for node in best_path:
            if node[0] == 1:
                return node[3]
        return

    # Purpose: places a penguin in the left most, top most position on the board. It checks if a spot is sunk, or taken
    # by another penguin, if so it goes onto the next hexagon in the ordered list, if not it places the penguin there
    # and will lower the penguin left count which is the given amount of penguins to place. when the penguins left count
    # hits zero the function will break and return the updated state
    # @param state, the given state to which penguins shall be added
    # Example: <state.GameState instance at 0x0000000002B7D048>
    # @param player, the current player that owns the newly added penguins
    # Example: <__main__.Player instance at 0x0000000003456048>
    #  ("red", 12)
    # $param penguinsleft, an int that determines how many penguins will be placed in the patterned order.
    # Example: 1
    def place_ordered_penguins(self, state, player, penguinsleft):
        hexboard = state.hexboard
        while penguinsleft != 0:
            for hex in hexboard.hexagons:
                if not hex.spottaken:
                    if not hex.sunk:
                        hex.spottaken = True
                        player.penguins.append(hex.xy)
                        penguinsleft += -1
                        break
        return state

if __name__ == "__main__":
    player1 = state.Player('red', 3)
    player2 = state.Player('black', 4)
    players = [player1, player2]
    hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
    statetemp = state.create_state(players, hex_board)
    statetemp.place_penguin(hex_board, player1, 1)
    statetemp.place_penguin(hex_board, player2, 1)
    interface = PlayerInterface(statetemp, player1, players)
    # statetemp.place_penguin(hex_board, player2)
    # state.render_state(hex_board)
    game = Game(statetemp.hexboard, players, 0)
    # thing = game.get_next_state(statetemp, ('Move', 1, 2))
    # thing = game.map_states(statetemp, statetemp.is_over)
    game_tree = game.game_tree(statetemp, 3)
    # interface.best_move(game_tree, player1)
    # interface.place_ordered_penguins(statetemp, player1, 1)
    # thing = player1.penguins
    print("thing: ", interface.best_move(game_tree, player1))
