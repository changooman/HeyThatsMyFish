# Game State

## Data Representation
A game state can be represented by a Board class.

#### Board
A Board class has the following properties:
* tiles - a 2D array of Tiles
* penguins - a map of Penguins to a list of (row, col) pairs

#### Tile
A Tile class has the following property:
* num_fish - the number of fish on the tile

#### Penguin
A Penguin class has the following property:
* color - the color of the penguin

A board can represent any game state by using a list of penguins and a 2D array of tiles.

## External Interface
Clients will interact with an external interface to manipulate the game state. There will be a protocl that clearly defines what clients are permitted to do. All requests are passed to the Referee to ensure the validity of the move. A Referee is the only entity that can modify the game state. If any player request is invalid, the Referee will reject the request.

#### get_state
`get_state()`
A player can request to 'see' the current state of the game. This will send the player the positions of all penguins (map of color to list of coordinates), the current scores for each player (map of color to integer), and the state of all tiles (empty or # of fish) (2D array of integers).

#### place_penguin
`place_penguin(row, col)`
In the beginning of the game, a player can request to place their unplaced-penguin at the specified row and column.

#### make_move
`make_move(origin_row, origin_col, dest_row, dest_col)`
Players can request to move one of their penguins. The origin_row and origin_col parameters specify the coordinate of their penguin they would like to move, and the dest_row and dest_col parameters specify which coordinate they would like to move that penguin to.
