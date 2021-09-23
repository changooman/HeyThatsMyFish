# Data representation of the protocol
Player-protocol would be a class that takes in a state (since our referee functions are in the state class),
It would also take in the Player class, and the player-interface class. It will check with the state and player 
to make sure that all moves given in the player-interface are legal moves.  The player protocol will also interact 
with the interface when the player inputs a move into the interface the protocol will grab it and use the referee and
state methods to a) check if it is a legal action and b) make the move for the player 
  
The referee would grab the player class through communication with the player-protocol. This would help to help direct 
functions and methods when needing to link data in the hexagon board with the specific player. 
# UML Diagram
```
 ─────────────────────         ─────────────────
│   player-interface  │─────> │ player-protocol │
└─────────────────────        └─────────────────
                                   ^
                           Function & method calls
 ──────────          ───────       │       ───────────── 
│  player  │────>  │  state │───────── >  │  game-tree  │
 ──────────          ───────                ───────────
                        ^
 ───────                │
│ board │───────────────
 ───────
```