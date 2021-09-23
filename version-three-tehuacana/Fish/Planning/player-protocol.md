# Player Protocol

## PlayerInterface
The PlayerInterface can be used to communicate with the referee about a game of Fish.

## Gameflow Diagram
```
╭───────────────────╮
│                   │
│                   │
│      PREGAME      │
│                   │
│                   │
╰───────────────────╯
         │
         │ the game is started by the referee
         │
         ▼
╭───────────────────╮
│                   │
│                   │──────╮
│     PLACEMENT     │      │ the player whose turn it is places an avatar
│                   │◀─────╯
│                   │
╰───────────────────╯
         │
         │ the players have placed all avatars
         │
         ▼
╭───────────────────╮
│                   │
│                   │──────╮
│     MOVEMENT      │      │ the player whose turn it is moves an avatar or their turn is skipped, if the cannot make a move
│                   │◀─────╯
│                   │
╰───────────────────╯
         │
         │ no player can make a move
         │
         ▼
╭───────────────────╮
│                   │
│                   │
│     GAMEOVER      │
│                   │
│                   │
╰───────────────────╯
```

## PREGAME
There may be some time before the gameplay begins and players may start placing their avatars. This is the PREGAME phase.

## PLACEMENT: Making a Placement
The `make_placement()` function will be called during a player's turn to place an avatar during the PLACEMENT phase (see gameflow diagram above).

## MOVEMENT: Making a Move
The `make_move()` function will be called during the calling player's turn to move an avatar to another tile during the MOVEMENT phase (see gameflow diagram above).

If a player cannot make a move, their turn is automatically skipped.

## GAMEOVER
Once no player can move a penguin, the game is over. Players will no longer make placements or moves.
