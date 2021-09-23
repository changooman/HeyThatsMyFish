##Referee class:
Class Referee: # takes in a state, list of players, player-protocol, and other necessities that will allow it to run not only the referee 
functions that are in state, but also create new referee functions that will check each rule in game as listed in the 
project prompts and plans, and interacts with the players to make sure that each player is following these rules.

Def is_over(self, state): # Takes the is_over function from the state and applies it in referee.

Def is_valid_move(self, hexagons, origin_index, destination_index, hexboard, player) # takes the is_valid_move function 
from the state and applies it in referee

Def move_penguin(self, origin, destination, state, player) #takes the move_player function from the state and applies it
 in the referee.
 
Def place_penguins(self, order_type, hexboard, player) # takes in pace penguins from state and place_ordered_penguins 
from strategy and places the penguins depending on which method of placing penguins is given in the order_type 
parameter.

Def fail_players(self, state, player) # If a certain player fails to comply with a rule or tries to cheat then remove 
that player and their penguins from the game, and prints a message saying “you failed to comply with the rules”

Def create_board(self, order_type, players): # Creates the board by calling the hexboard class and creates a hexagonal 
board with fish through the methods defined in the board.py file. This will work injunction with place penguins to 
create the starting board for players to immediately be able to use

###UML
```


 ──────────────────────         ─────────────────
│       referee        │<───── │ player-protocol │<────
└──────────────────────        └─────────────────      │
     ^               ^               ^                  │
     │               │       Function & method calls    │
 ──────────         ───────          │      ─────────── 
│  player  │────> │  state  │──────────>  │  game-tree  │
 ──────────         ───────                 ───────────
                        ^
 ───────                │
│ board │───────────────
 ───────
```
