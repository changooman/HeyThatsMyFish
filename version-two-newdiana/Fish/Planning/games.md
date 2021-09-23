# GameTree

A GameTree class will represent an entire game, including all branching move possibilities until the game is over. It will provide functionailites that allow users to look ahead into future possibilities.

## Creation

It will be created with a game state in which all players have placed all their penguins as a starting point.

## Data Representation

The GameTree will use nested dictionaries to represent the tree of possible game states moving forward. These dictionaries will be indexed with 4-element tuples representing valid moves. For example, (0, 0, 2, 1) would represent moving a penguin at tile (0, 0) to tile (2, 1) on the example board below.

Using this key to index the dictionary would provide access to another dictionary representing possible moves to take after that.

It will have one dictionary to represent the starting point called `root`.

For example: `root[(0, 0, 2, 1)]` will return a dictionary representing the game state after taking the move (0, 0, 2, 1). This resulting dictionary can then be used to further access deeper game states by continuing to index with move tuples.

At any point, the game state object the a given dictionary represents can be accessed by indexing it with a reserved key (whose value is an invalid move such as `GET_STATE = (-1, -1, -1, -1)`). Thus, the original game state can be accesses via `root[GET_STATE]`, and the game state after the move (0, 0, 2, 1) can be accessed via `root[(0, 0, 2, 1)][GET_STATE]`.

These dictionaries and states could be generated upon GameTree initialization, or could be more efficiently lazily evaluated as different states are requested by users.

```
Example Board:
 _____       _____       _____
/ 0,0 \_____/ 0,1 \_____/ 0,2 \_____
\_____/ 1,0 \_____/ 1,1 \_____/ 1,2 \
/ 2,0 \_____/ 2,1 \_____/ 2,2 \_____/
\_____/ 3,0 \_____/ 3,1 \_____/ 3,2 \
/ 4,0 \_____/ 4,1 \_____/ 4,2 \_____/
\_____/     \_____/     \_____/
```

## Interface

### get_future_state(moves)

Accepts a list of moves in 4-element tuple form and returns the future game state after those moves are executed.

Raises an exception if the move list is invalid in some way.

### get_future_moves(moves)

Accepts a list of moves in 4-element tuple form and returns all possible next moves at the future game state after the input moves are executed.

Raises an exception if the move list is invalid in some way.

### check_moves(moves)

Checks a list of moves in 4-element tuple form and returns whether or not it is a valid progression of moves.
