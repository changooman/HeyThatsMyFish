## Data Representation for Game
Game would be a class that would consider player order, the list of hexagons, the given state, and would create a list of all possible moves. 
It would contain functions that would go through all possible movements given a state by checking with the referee if a move is valid or not. It would take in the including current penguin position and a list of all tiles. There would be another function in the class that would run through all the current players penguins until there are no more possible moves for this state of the game

    \#a tree of all potential moves from a starting state
    Class Game:
        __init__(self, starting_state, players):
            self.player = players # list of players in order of turn
            self.state = starting_state # a class instance of HexBoard which holds the hex board.
            self.hexagons = self.state.hexagons # list of all hexagons in the starting state
            self.all_possible_moves = []  #a list representing every possible move for each penguin
        
###External Interface

    \#Checks the rules of FISH to determine all the possible moves of a player’s penguin
     Def possible_moves(start coords):
        Possible_moves = []
        For hexagon in Hexagons:
            Check if valid move from player penguins
                If valid append to possible moves
        return possible moves

    # Checks the rules of FISH to determine all the possible moves of all the    
    # current player’s penguins
    Def all_possible_moves(player):
        For penguin in player.penguins:
             Possible_moves self.possible_moves(penguin coords)
             self.all_possible_moves append possible_moves
   

