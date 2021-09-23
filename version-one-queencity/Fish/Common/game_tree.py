import board
import state
import copy


# Represents a tree of all potential moves from a starting state. It serves as a tactical tool to allow players
# insight into how certain moves could impact their winning conditions in the game by revealing all the possibilities.
"""
Each ox is a state which holds a board:
        _______
     _______/ (0,1) \_______
    / (0,0) \_______/ (0,2) \
    \_______/ (1,1) \_______/
    / (1,0) \_______/ (1,2) \
    \_______/       \_______/

    oxoxoo    ooxoo
  ooxoxo oo  oxoxooo
 oooo xxoxoo ooo ooox
 oxo o oxoxo  xoxxoxo
  oxo xooxoooo o ooo
    ooo\oo\  /o/o
        \  \/ /
         |   /
         |  |
         | D|
         |  |
         |  |
  ______/____\____

"""

class Game:
    def __init__(self, starting_state, players, index, layers):
        self.players = players  # list of players in order of turn
        self.player_index = index  # an index of the starting player
        self.board = starting_state.hexboard  # a class instance of HexBoard which holds the hex board.
        self.hexagons = self.board.hexagons  # list of all hexagons in the starting state
        self.all_possible_moves = []  # a list representing every possible move for each penguin
        self.layers = layers
        self.tree = self.game_tree(starting_state, layers)

    # Purpose: Checks the rules of FISH to determine all possible moves for a player's penguin. For each
    # hexagon in the hexagon list, it checks if the penguin can move there with is_valid_move. If so, it
    # adds the hexagon to the possible moves list.
    # @param start_coords The origin grid coordinates of the penguin.
    # Ex: [1,1]
    # @param state_input The GameState instance where the penguin can move.
    # Ex: <state.GameState instance at 0x0000000002B7D048>
    # @param player, the index of the current player
    # Ex. 5
    # <__main__.Player instance at 0x0000000003456048>
    # @return possible_moves The list of coordinates which the penguin can move to.
    # Ex: [[1,0], [0,0]]
    def possible_moves(self, start_coords, state_input, player):
        possible_moves = []
        for hexagon in state_input.hexboard.hexagons:
            origin_index = self.find_hexagon(state_input.hexboard.hexagons, start_coords)
            origin_index += 1  # Increases the index to grab the index of the actual hexagon in valid moves
            destination_index = self.find_hexagon(state_input.hexboard.hexagons, hexagon.xy)
            destination_index += 1  # Increases the index to grab the index of the actual hexagon in valid moves
            if state_input.is_valid_move(state_input.hexboard.hexagons, origin_index,
                                  destination_index, state_input.hexboard, player):
                possible_moves.append(hexagon.xy)
        return possible_moves

    # Purpose: Returns the Player instance of a certain color. It takes in a GameState instance which hosts
    # a list of Player instances. If the color matches, it will return that Player instance.
    # adds the hexagon to the possible moves list.
    # @param starting_state The GameState instance where the penguin can move.
    # Ex: <state.GameState instance at 0x0000000002B7D048>
    # @param player, the index of the current player
    # Ex. 3
    # @return check_player The Player instance associated with the penguin move.
    # Ex: [("red", 12), ("black", 21)]
    # <__main__.Player instance at 0x0000000003456048>
    def tree_findplayer(self, starting_state, player):
        for any_player in starting_state.players:
            if any_player.color == self.players[player].color:
                check_player = self.players[player]
                index = 0
                for a_player in self.players:
                    if check_player.color == a_player.color:
                        return index
                    else:
                        index += 1

    # Purpose: Returns a list of penguins which has the same color as the player in the GameState instance passed in.
    # @param starting_state The GameState instance where the penguin can move.
    # Ex: <state.GameState instance at 0x0000000002B7D048>
    # @param player, the index of the current player
    # Ex. 1
    # @return check_player The Player instance associated with the penguin move.
    # Ex: [[1,2], [0,0]]
    def tree_findpenguins(self, starting_state, player):
        index = 0
        for a_player in starting_state.players:
            print "player", player
            if a_player.color == self.players[player].color:
                penguins = starting_state.players[index].penguins
                return penguins
            index += 1


    # Purpose: Gets the first layer of a tree of states from a given state by checking the possible moves for all penguins
    # owned by the current player, checking the possible moves, and creating a state instance for each possible move
    # @param starting_state, the The GameState instance the new tree layer starts from.
    # Ex: <state.GameState instance at 0x0000000002B7D048>
    # @return all_states, the final list of all possible states one layer down stemming from the given state
    # Ex: [<state.GameState instance at 0x0000000002B7D048>, <state.GameState instance at 0x0000000002B7D079>]
    def tree_states(self, starting_state, player):
        all_states = []
        index = 0
        penguins = self.tree_findpenguins(starting_state, player)
        checkplayer = self.tree_findplayer(starting_state, player)
        for penguin in penguins:
            # Find possible moves for this penguin
            possible_moves = self.possible_moves(penguin, starting_state, checkplayer)
            print possible_moves
            # Perform move action on state for tha
            temporary_state = copy.deepcopy(starting_state)
            for move in possible_moves:
                temporary_state2 = state.create_state(copy.deepcopy(temporary_state.players),
                                                      copy.deepcopy(temporary_state.hexboard))
                origin = self.find_hexagon(temporary_state2.hexboard.hexagons, penguin)
                origin += 1
                destination = self.find_hexagon(temporary_state2.hexboard.hexagons, move)
                destination += 1
                checkplayer2 = self.tree_findplayer(starting_state, player)
                temporary_state2.move_penguin(origin, destination, temporary_state2, checkplayer2)
                all_states.append(temporary_state2)
        return all_states

    # Purpose: Returns the state that would result from taking action A. It takes in a tree_node as an input and
    # attempts the action. If the action is valid and the attempt is valid, it will return that resulting state.
    # @param tree_node The starting node that will be the parent of the next state.
    # Ex: <state.GameState instance at 0x0000000002B7D048>
    # @param action A tuple that represents the action to be carried out on the given state.
    # It can contain a string and int(s) depending on what the action is
    # Ex: ('Move', 1, 2)
    # @param player, the index of the current player
    # Ex. 2
    # @return next_state, the next state instance after a legal action from the original state
    # Ex. <state.GameState instance at 0x0000000002B7D048>
    def get_next_state(self, tree_node, action, player):
        # action example: ('Move', 1, 2)
        next_state = tree_node
        if action[0] == 'Move':
            if tree_node.is_valid_move(self.hexagons, action[1], action[2], next_state.hexboard, self.players[player]):
                next_state.move_penguin(action[1], action[2], next_state, self.players[player], self)
                return next_state
            else:
                raise Exception("Action is not permissible.")

    # Purpose: Returns a list of state(s) that would result from executing the given function. It takes in a tree_node
    # as an input and finds all states reachable from that tree-node's state. If the function is valid and can be
    # executed, it applies it to that reachable state.
    # @param tree_node The starting node that will be the parent of the next state.
    # Ex: <state.GameState instance at 0x0000000002B7D048>
    # @param function A function instance to be applied onto the state
    # Ex:
    # @return returned_items A list of states that have the function executed
    # Ex. <state.GameState instance at 0x0000000002B7D048>
    def map_states(self, tree_node, function, player):
        all_states = self.tree_states(tree_node, player)
        try:
            returned_items = map(function, all_states)
            return returned_items
        except:
            raise IndexError("Given function does not exist!")

    # Purpose: Creating a complete tree for a state. It takes in a state that will not have any more penguins added onto
    # it. It continues to traverse each resulting state until the reaching the set max layer.
    # @param tree_node The starting node that the next state will be a child of
    # Ex:
    # @param starting_state The state to be returned if the action is valid and possible
    # Ex: <state.GameState instance at 0x0000000002B7D048>
    # @return returned_items A list of states that have the function executed
    # Ex. <state.GameState instance at 0x0000000002B7D048>
    def game_tree(self, current_state, layers):
        # 4 nodes in layer 3 the tree will look like:
        # [(1, state1), (2, state1), (2, state2),(3, state1), (3, state2), (3, state3), (3, state4)]
        current_game_tree = [(0, current_state)]
        layer_count = 0
        while layer_count < layers:
            for item in current_game_tree:
                item_state_temp = item[1]
                if item[0] == layer_count:
                    predicted_state = self.tree_states(item_state_temp, self.player_index)
                    if predicted_state == []:
                        if self.map_states(item[1], current_state.is_over(item[1]), self.player_index):
                            return current_game_tree
                        else:
                            layer_count += -1
                    print predicted_state
                    print layer_count
                    for next_state in predicted_state:
                        current_game_tree.append((layer_count + 1, next_state, item_state_temp))
            if self.player_index < len(self.players) - 1:
                self.player_index += 1
            else:
                self.player_index = 0
            layer_count = layer_count + 1
        return current_game_tree


    # Purpose: Find the FillHexagon object with the same grid coordinate.
    # @param hexagons A list of FillHexagon objects used to locate the origin and destination.
    # Ex: [<__main__.FillHexagon instance at 0x0000000003456048>, <__main__.FillHexagon instance at 0x0000000003456048>]
    #          _______
    #  _______/ (0,1) \_______
    # / (0,0) \_______/ (0,2) \
    # \_______/ (1,1) \_______/
    # / (1,0) \_______/ (1,2) \
    # \_______/       \_______/
    #
    # @param coordinate_pair A list of two integers that represents the grid coordinate of a hexagon
    # Ex: 2
    # @return start A integer that represents the index of the FillHexagon object
    def find_hexagon(self, hexagons, coordinate_pair):
        start = 0
        for hex in hexagons:
            if hex.xy == coordinate_pair:
                return start
            start += 1
        return start


if __name__ == "__main__":
    player1 = state.Player('red', 3)
    player2 = state.Player('black', 4)
    players = [player1, player2]
    hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
    statetemp = state.create_state(players, hex_board)
    statetemp.place_penguin(hex_board, player1)
    # statetemp.place_penguin(hex_board, player2)
    # state.render_state(hex_board)
    game = Game(statetemp, players, 0, 3)
    # thing = game.get_next_state(statetemp, ('Move', 1, 2))
    # thing = game.map_states(statetemp, statetemp.is_over)
    thing = game.tree
    print("thing: ", thing)
