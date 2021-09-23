import strategy
from Other import state
from Other.game_tree import *

# a player component that realizes the logic of the existing interface in Common/
# and performs the mechanical tasks of initial moves and taking turns. It connects with
# the State, Player, and Strategy classes to run a game through the Referee class.
# It is fundamentally different from the Player class even though their names are similar.
# Purpose: Represents a basis for allowing the referee to play a full game through function calls.
# The player component calls functionalities from the strategy to move to the optimal position looking N turns ahead.
# This mainly serves as a tool to perform actions for a player and set up the starting board as specified.
# Looking at not only the random formation we started with but also the zigzag pattern created in the previous milestone
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

     _______         _______
    / (0,0) \_______/ (0,1) \_______
    \_______/ (1,0) \_______/ (1,1) \
    / (2,0) \_______/ (2,1) \_______/
    \_______/       \_______/
    Players in the state:
    P1 P2
    Game Over? False
"""


class PlayerComp:
    # initializes the player comp taking in the current state, a current player, and the strategy to be used. These
    # classes also connect to other potentially necessary classes meaning they are the only true requirements
    # @param state A GameState object that represents the state of the board to be changed with each move
    # Example: <state.GameState instance at 0x0000000002B7D048>
    # @param player A Player object that is the instance of a single player on a board. This determines which player
    # to perform functions on
    # Example: <__main__.Player instance at 0x0000000003456348>
    # @param strategy A PlayerInterface object that represents the best possible moves for a player to take based on
    # the min max strategy
    # Example: <__main__.PlayerInterface instance at 0x0000000003456348>
    def __init__(self, state, player, strategy):
        self.current_state = state
        self.player = player
        self.strategy = strategy

    # Purpose: Performs the initial moves of placing the penguins on their positions on the board. takes in the value
    # style to determine the patterning of the penguin placement, depending on this the function will call one of the
    # two penguin placement functions that we have, one handles the zigzag pattern the other handles a random pattern.
    # @param style, The style of the penguin placement on the board
    # Example: "Zigzag", "Random"
    # @param num_penguins An integer that represents the amount of penguins to place on the board per player.
    # Example: 6, 3, 10, 1
    # @param current_player A Player object that represents the player that owns the penguins to be placed, determines
    # the owner and color of each penguin.
    # Example: <__main__.Player instance at 0x0000000003456048>
    def initial_moves(self, style, num_penguins, current_player):
        if style == "Zigzag":
            self.strategy.place_ordered_penguins(self.current_state, current_player, num_penguins)
        elif style == "Random":
            self.current_state.place_penguin(self.current_state.hexboard, current_player, num_penguins)

    # Purpose: Performs an action for a penguin while looking at the strategy n layers deep (n being a value given in
    # the param 'layers'). This accounts for the moves that AI players will make and when it is an AI player's turn it
    # will check the best move from the strategy and will move the AI player's penguin to that position.
    # @param current_player A player object that represents the player that owns the penguins to be placed, determines
    # the owner and color of each penguin.
    # Example: <__main__.Player instance at 0x0000000003456048>
    # @param layers An integer that represents the amount of layers deep to look ahead in the tree when determining
    # the next move.
    # Example: 1, 2, 5, 3, 7
    def take_turn(self, current_player, layers):
        index = 0
        for a_player in self.current_state.players:
            if a_player == current_player:
                playerindex = index
            index += 1
        game = strategy.Game(self.current_state.hexboard, self.current_state.players, playerindex)
        game_tree = game.game_tree(self.current_state, layers)
        bestmove = self.strategy.best_move(game_tree, current_player, layers)
        self.current_state.move_penguin(bestmove[0], bestmove[1], self.current_state, playerindex)
