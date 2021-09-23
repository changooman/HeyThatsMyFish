##Referee class:
The TournamentManager is specifically designed to handle a single tournament. It would take in a list of players that 
are going to be participating in that tournament.

There will also be an ability for players who are interested in joining the tournament to join if the tournament has 
not begun yet. In addition, players who are already in the tournament can leave the tournament through another 
functionality if the tournament hasn’t started yet.

When the tournament starts, the tournament manager will have a functionality that pairs games with one another, and sets
up a bracket system before any game starts. The TournamentManager will assign a new Referee for each game. When the 
games that are paired together finish, the winner(s) will move onto the next ‘bracket’. They will start another game 
that is paired with the winner(s) of a separate pair of games. This process will continue until the final match where 
the tournament winner(s) will be decided. The Tournament manager will compile the statistics of the tournament and 
return it once the winners have been decided.
 
For observers, it will initially start with an empty list of observers but will feature the ability to opt into this 
observation list. There will also be an ability to then opt out of the observation list. 

###UML
```

 ──────────────────── 
│ tournament manager │
 ────────────────────
    ^
    │    
    │
 ──────────────────────         ─────────────────
│       referee        │<───── │ player-protocol │<─────
└──────────────────────        └─────────────────       │
     ^               ^               ^                  │
     │               │       Function & method calls    │
 ──────────         ───────          │             ─────────── 
│  player  │────> │  state  │─────────────────>  │  game-tree  │
 ──────────         ───────                        ───────────
                        ^
 ───────                │
│ board │───────────────
 ───────
```