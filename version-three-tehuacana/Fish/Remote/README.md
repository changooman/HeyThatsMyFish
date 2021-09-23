# File Organization of Remote

Remote is dividied into four files:
       * `communication.py`
       * `server_player.py`
       * `client_player.py`
       * `server.py`

Visually, the role of each component can be represented as follows: 

Logical   |                / `ServerPlayer` (`server_player.py`)  <=========> `ClientPlayer` (`client_player.py`) | <=> Logical `Player`  
`Manager` | <=> `server.py`- `ServerPlayer` (`server_player.py`)  <=========> `ClientPlayer` (`client_player.py`) | <=> Logical `Player`  
component |                \ `ServerPlayer` (`server_player.py`)  <=========> `ClientPlayer` (`client_player.py`) | <=> Logical `Player`  

While there are three `ServerPlayer` and `ClientPlayer` listed in the example, in reality there will be between 5 and 10 players inclusive  
in any given tournament ran remotely.

## `communication.py`

`communication.py` gives functionality to send logical components of the tournament handled by the server over a connection as JSON, and  
receive return values from clients. This component exposes functions that map to the functions outlined in Remote Interactions (`start`, `play_as`,  
etc.). This component also handles the serialization and deserialization of the JSON itself.

## `server_player.py`

The `server_player.py` component provides `ServerPlayer`, a class that represents a player in the game of Fish that the server uses to send messages to.
This class inherits `TournamentPlayer` interface, and as such can be used in a tournament. It's methods are primarily implemented to use the functionality
of `communication.py` to send and receive messages from a remote player. For example, calling `make_placement` with a `ServerPlayer` sends a `setup`
protocol message; the `Placement` received from the client is the placement used by the server.

## `client_player.py`

The `client_player.py` component provides `ClientPlayer`, a class that represents a the player receiving messages from the game server and sending
avatar moves and placements in response. This class inherits `Player`, and as such has the same methods and functionality as a regular logical player
(including its `Strategy`). Additional functionality exists to receive messages and respond accordingly. For example, when a `ClientPlayer` receives
a `setup` message from the server, it will use the `State` it received to generate a placement in accordance to its `Strategy`, and then send this
placement back to the server.

## `server.py`

This component provides the `run_tournament` function. This function sets up the connection to run the server and accepts incoming connections from clients.
Each new connection is given to a `ServerPlayer` to be used the tournament. The server is responsible for ensuring there are between 5 and 10 players per tournament;
if there are less that 5, the tournament enters the waiting period again (after this waiting period, the server shuts down). Each waiting period is 30 seconds. The players
are added to the tournament in the order in which they connected to the server. Once the tournament finishes, the names of the winners, losers, and players who were kicked
(either for cheating or failing to respond).

# Modifications

## `manager.py`

* `Manager` initially had no way of informing players a game was about to start. This functionality was added in the `__inform_players_start()` function.

* `Manager` initially used `Player` objects. However, this proved to be too limiting, so a `TournamentPlayer` class was created, which extended the functionality
of a `PlayerABC` (an abstract base class that works like an interface for players) to include `inform_start` and `inform_end`. `TournamentPlayers` also take an instance
of another `PlayerABC` to use composition and call the methods of the given `PlayerABC` for the `TournamentPlayer`. `ServerPlayer` uses this class to implement its
remote communication functionality without modifying large portions of the `Manager` logic (for example, `inform_end` sends an `end` message, `make_placement`
sends a `play_as` message.)

* `Manager` now takes an optional `board` argument that specifies the board to use for every game of Fish in the tournament. The constructor also checks that the board is
able to run an individual game with the max number of penguins/avatars possible (in this case a three-player game with nine avatars), since each individual game in the
tournament can vary in its number of players.

## `referee.py`

* `Referee` takes an optional `board` argument that specifies the board to use for the game of Fish. The existing `board_size` field remains, but
giving a non-None board will cause the referee to ignore this field. The board must be able to run a game with the number of players given (i.e. it must be
large enough for players to place their penguins/avatars)

## `strategy.py`

* the implementation of `make_move` was too inefficient to be used for a 5x5 board. It was been reworked to be more efficient.

## `player.py`

* player.py now inherits from `PlayerABC`

## `state.py`

* state.py now has a function `json_to_state`, which converts the JSON representation of a state to an actual state object.

## `board.py`

* board.py now has a function `get_holes_in_board` which returns the number of holes in the board.

## `test_*.py`

* each of the above files has additional unit tests in its corresponding unit test file (example: unit tests for `board.py` are in `test_board.py`)
