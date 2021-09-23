# Remote Collaboration Protocol

## Component Communications
```
╭───────────────────╮   ╭───────────────────╮   ╭───────────────────╮   ╭───────────────────╮
│                   │   │                   │   │                   │   │                   │
│  Administrative   │◀─▶│    PlayerProxy    │◀─▶│      Network      │◀─▶│      Remote       │
│       Code        │   │                   │   │                   │   │      Player       │
│                   │   │                   │   │                   │   │                   │
╰───────────────────╯   ╰───────────────────╯   ╰───────────────────╯   ╰───────────────────╯
```

## Network Communications
```
╭───────────────────╮                           ╭───────────────────╮
│                   │     TCP Connection        │                   │
│                   │     Creation              │                   │
│      Sign-Up      │◀─────────────────────────▶│      Remote       │
│      Server       │                           │      Player       │
│                   │     Sign-up Request       │                   │
│                   │◀──────────────────────────│                   │
│                   │                           │                   │
│                   │     Sign-up Response      │                   │
│                   │──────────────────────────▶│                   │
│                   │                           │                   │
│                   │     Tournament Start      │                   │
│                   │     Message               │                   │
│                   │──────────────────────────▶│                   │
╰───────────────────╯                           │                   │
         │                if successfully       │                   │
         │                signed up:            │                   │
         │                                      │                   │
         │                                      │                   │
         │  Give socket                         │                   │
         │  to PlayerProxy                      │                   │
         │                                      │                   │
         │              ╭───────────────────╮   │                   │
         │              │Interactions that  │   │                   │
         │              │can repeat multiple│   │                   │
         │              │times throughout   │   │                   │
         ▼              │the tournament:    │   │                   │
╭───────────────────╮   │-------------------│   │                   │
│                   │   │ Placement Request │   │                   │
│                   │──────────────────────────▶│                   │
│    PlayerProxy    │   │                   │   │                   │
│                   │   │ Placement Response│   │                   │
│                   │◀──────────────────────────│                   │
│                   │   │-------------------│   │                   │
│                   │   │ Move Request      │   │                   │
│                   │──────────────────────────▶│                   │
│                   │   │                   │   │                   │
│                   │   │ Move Response     │   │                   │
│                   │◀──────────────────────────│                   │
│                   │   ╰───────────────────╯   │                   │
│                   │     Tournament Result     │                   │
│                   │     Message               │                   │
│                   │──────────────────────────▶│                   │
╰───────────────────╯                           ╰───────────────────╯
```

## Message Formats
All messages besides `TCP Connection Creation` will be in the form of JSON objects as described below.

#### JSON Custom Data-Types

```
Color is a string representing one of the available player colors

State is
{
    "players"   : [Player, ..., Player],
    "board"     : Board
}

Player is
{
    "color"     : Color,
    "score"     : Natural,
    "places"    : [Position, ..., Position]
}

Position is a JSON array that contains two natural numbers:
[board_row, board_column]

Board is a JSON array of JSON arrays where each element is either 0 or a number between 1 and 5. A 0 denotes a hole in the board configuration. All other numbers specify the number of fish displayed on the tile.

Request-Type is a String with a value in ["PLACEMENT", "MOVE"].

Result is a String with a value in ["WIN", "LOST"].
```

### Sign-up Request
```
{
    "name"  : String,
    "age"   : Natural
}
```
* `name` is the participants's chosen name identifier.
* `age` is the participants's age in days.

### Sign-up Response
```
{
    "status"    : String
}
```
* `status` is the sign-up status of the participant, either `"SUCCESS"` for a player that has successfully signed up or `"WAIT"` for a player that has been wait-listed.

### Tournament Start Message
```
{
    "message"   : String
}
```
* `message` will be either `"START"` is the participant is successfully signed-up or has made it off of the wait list or `"FAILURE"` if the participant failed to make it off the wait list.

### Placement Request
```
{
    "state" : State,
    "color" : Color,
    "type"  : Request-Type
}
```
* `state` is the current state of the game where it is the participating player's turn to make a placement, passing will not be possible.
* `color` is the player color of the participating player.
* `type` is a Request-Type with the value `"PLACEMENT"` to indicate that this is a placement request.

### Placement Response
```
{
    "placement" : Position
}
```
* `placement` is the position at which the participating player will place a penguin.

### Move Request
```
{
    "state" : State,
    "color" : Color,
    "type"  : Request-Type
}
```
* `state` is the current state of the game where it is the participating player's turn to make a move, passing will not be possible.
* `color` is the player color of the participating player.
* `type` is a Request-Type with the value `"MOVE"` to indicate that this is a move request.

### Move Response
```
{
    "move"  : [Position, Position]
}
```
* `move` is two positions representing the move the participating player will make. The first position is the location of one of the player's penguins and the second position is the location the player would like to move that penguin to.

### Tournament Result Message
```
{
    "result"  : Result
}
```
* `result` is either `"WIN"` indicating that the player has won the tournament, or `"LOSE"` indicating that the player has lost the tournament.

## Explanation
In order to communicate with players remotely, the Fish.com server will use a Sign-Up Server and PlayerProxies. The Sign-Up Server will handle incoming connections and player sign-up requests. The PlayerProxy is a new proxy component that conforms to the Player interface for use in tournaments and games, but communicates over a network with a remote player to decide on its placements and moves.

All network communication will happen over TCP sockets using JSON objects as messages whose formats are described in the section above.

The remote player will start by creating a TCP connection with the Sign-Up Server and sending a Sign-Up Request. The server will respond with a Sign-Up Response indicating whether the player has successfully signed up or been wait-listed. When the tournament starts, the server will send a Tournament Start Message to the player indicating whether or not the player has made in into the tournament or not (if he didn't make it off the wait-list). If the player did not make it into the tournament, communication will end here.

As the tournament goes on, participating players will be sent Placement Requests and Move Requests, which provide a game state and the color of the participating player. Based on this information, the remote player will reply back with their action in the form of a Placement Response or Move Response, respectively.

Once the tournament is over, the remote players will receive a Tournament Result Message indicating whether they have won or lost the tournament.

Between player requests to the remote player and their responses, 60 seconds will be allotted to the remote to respond with their action. If the player fails to respond in the allotted time, they will be kicked from the game and tournament.
