# Referee

## API
```
class Referee():
    def __init__(self, player_interface_handles, num_rows, num_cols, num_holes):
        """Initialize the Referee.

        Assigns a color to each player and creates a turn order based on the ages of the players.
        Creates a Fish game board for the players to play on.

        player_interface_handles:   A list of player_interface handles to players of this game
                                    (objects with which the referee can communicate with / query information about individual players)
        num_rows:                   The number of rows for the game board.
        num_cols:                   The number of columns for the game board.
        num_holes:                  The number of holes to make in the board.
        """
        pass


    def run(self):
        """ Begin the game of Fish.

        The referee will begin the game and start taking moves from players.
        The game will continue until it has ended.
        """
        pass


    def get_scores(self):
        """Get the player scores.

        returns:    A list of players and their scores.
        """
        pass


    def get_victors(self):
        """Get the victor(s) if the game is over.

        returns:    A list of winning players if the game is over, None if it is not.
        """
        pass


    def game_over(self):
        """Is the game over?

        returns:    True if the game is over, False otherwise.
        """
        pass


    def get_violators(self):
        """Get a rule violators who have been ejected.

        returns:    A list of violating players.
        """
```

## Functionality
### On Creation
Upon creation, the Referee will assign each player a color and create a turn order based on the ages of the players. It will use player_interface handles (the other side of our player_interface) to communicate color and turn order to each player.

It will then create a game board based on a given number of rows and columns, and make a given number of random holes in it. The board configuration arguments must allow all players to fit all of their avatars onto the game board.

### Running
When the `run()` function is called, the Referee will run the game until completion.

It will start by allowing players to take turns placing their avatars during a placement phase, in the previously created turn order, until each player has placed all of their avatars in accordance with the rules of Fish.

Then, players will take turns moving their avatars on the board. Once no players can make any move, the game is over.

If at any point a player attempts to make an invalid move or play out of turn, he will be ejected from the game and his penguins will be removed from the board. The same will happen if a player takes too long to make a move or crashes in some way.

Once the game is over, the players will be notified of their final scores and who won.
