from state import *
from board import RenderHexBoard
from strategy import *
from player import *

# a Referee that will play a full game with AI players using the rule checking functions in state, and the placement
# and action functions in PlayerComp. Referee also handles removing a player if they cheat or perform abnormal actions
# We do not define these abnormal actions yet since AI players will follow the rules and will not have to worry about
# cheating and other abnormal actions until we take human players into account.
# Purpose: Runs the game using AI players and removes players when caught cheating or making abnormal moves or actions
# (abnormalities will be specified in the next part since AI players will follow the rules properly and the code will
# only need to handle cheating etc with human controlled players)
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
class Referee:
    # initializes the Referee class. Takes in state and playercomp since those two are necessary and connect to other
    # necessary classes
    # @param state, the state of the board to be changed with each move
    # @param playercomp, performs the actions of placing players, and moving penguins based on the strategy
    def __init__(self, state, playercomp):
        self.current_state = state
        self.player = playercomp

    # Purpose: runs the game as a referee using AI players. It goes through each player in order and runs the take turn
    # function from the playercomp class. then it runs the get winners function to determine who had the highest score
    # in the game, and who won. If there is more than one winner it will return a list of the winners. If an AI player
    # runs out of possible moves but the game is not over the function will skip over the stuck player until they are
    # able to move again or until the game ends.
    # @param style, the style that the penguins will be placed in at the start of a game
    # @param penguins, the total number of penguins to be given to each individual player
    # @return winners, a list of players that got the highest score or tied
    def referee(self, style, penguins):
        for player in self.current_state.players:
            self.player.initial_moves(style, penguins, player)
        GameOver = False
        temp_players = self.current_state.players
        while not GameOver:
            for player in temp_players:
                try:
                    self.player.take_turn(player, layers)
                except:
                    pass
                GameOver = self.current_state.is_over(self.current_state)
        return self.get_winners()

    # Purpose: gets the winner(s) of a game, if two or more players have the highest score it will return a list of
    # players that are tied. To get the winner it checks all the players in the list of players and compares it to the
    # max score (which starts at 0) and if the player score is higher then it replaces max score with the player score
    # and continues the loop. after checks the score of each player against the winning score and if they match then
    # the player gets added to the winners list return. this accounts for ties no matter how many players tie
    # It then returns said list of winners as long as it is not empty.
    # @return winners, a non empty list of players that got the highest score or tied for highest score
    def get_winners(self):
        maxscore = 0
        for a_player in self.current_state.players:
            if a_player.score > maxscore:
                maxscore = a_player.score
        winners = []
        for a_player2 in self.current_state.players:
            if a_player2.score == maxscore:
                winners.append(a_player2)
        if len(winners) >= 1:
            return winners

    # Purpose: removes a player and their penguins. It will later be part of the functionality that removes cheating
    # players and players that perform abnormal actions in a game. This abnormality checker functionality will be added
    # later when adding human players since AI players can't perform abnormal actions based on how the were programmed.
    # abnormal conditions could include, moving to a non valid position, moving to an unreachable position, and moving
    # on another player's turn.
    # @param player, the player that is going to be removed.
    def remove_player(self, player):
        penguins = player.penguins
        self.current_state.players.remove(player)
        for hex in self.current_state.hexboard.hexagons:
            if hex.xy in penguins:
                hex.spottaken = False
                hex.sunk = False





if __name__ == "__main__":
    player1 = state.Player('red', 3)
    player2 = state.Player('black', 4)
    player3 = state.Player('white', 4)
    players = [player1, player2, player3]
    hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
    statetemp = state.create_state(players, hex_board)
    # statetemp.place_penguin(hex_board, player1, 1)
    # statetemp.place_penguin(hex_board, player2, 1)
    interface = PlayerInterface(statetemp, player1, players)
    # statetemp.place_penguin(hex_board, player2)
    # state.render_state(hex_board)
    layers = 3
    game = Game(statetemp.hexboard, players, 0, layers)
    # thing = game.get_next_state(statetemp, ('Move', 1, 2))
    # thing = game.map_states(statetemp, statetemp.is_over)
    game_tree = game.game_tree(statetemp)
    # interface.best_move(game_tree, player1)
    # interface.place_ordered_penguins(statetemp, player1, 1)
    # thing = player1.penguins
    print statetemp.players
    playr = PlayerComp(statetemp, player1, interface)
    ref = Referee(statetemp, playr)
    thing = ref.referee("Zigzag", 1)
    render = RenderHexBoard(statetemp.hexboard)
    render.render_state()
    print("thing: ", thing)
