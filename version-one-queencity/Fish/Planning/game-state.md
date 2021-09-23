## Data Representation for Game States <br>

GameState is one of the following:

- “Setup” Interpretation: The beginning phase of the game where players set up their pieces on the board

 - “Midgame” Interpretation:The mid phase of the game where players move their pieces until there can be no moves left.

 - “End”: Interpretation: The end of the game once there are no moves, this will print the player who had the most fish or player(s) who equally had the most fish




## Wish List for Fish <br>

 StartGame is a function
 Generates a 4 x 3 hexagon board and starts the process of the setup phase of the game

 PlayerColor is a string
 Represents the color of the player’s penguin that the referee randomly assigns

 Playerqueue is a list
 Represents the ordered queue by age for which players get their turn

 PlacePenguins is a function
 Allows a player to place a penguin on the board 
 other necessities such as hexagon coordinates and list of hexagon are

 GameOver is a Boolean
 Represents whether the game is still ongoing or not

 MovesLeft is a Boolean
 Represents whether a player has any moves left or not

 isOver is a function
 Will check how many tiles that are valid for player movement are not
 sunk and if there are none left then return false

 takeMove is a function
 Handles the TCP aspect of taking moves from players across different computers
 PenguinsPlaced is a boolean attribute for each player
 Represents whether a player has finished placing all their penguins. This helps coordinate the setup gamestate. 
