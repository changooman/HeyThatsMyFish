import fish
from Tkinter import *
import random

"""
    This class represents a player in the FISH game. It hosts all the necessary attributes for each player
    and serves the sole purpose of keeping track of player data.
"""


class Player:
    """
        * Construct a Player.
        * @param color A string that represents the color which the player has been assigned.
        * Examples: "red', "brown", "black", "white"
        * @param score An integer that represents the player's current score from getting fish.
        * Examples: 4, 21
        * @param sprite A string that represents the associated avatar image file.
        * Examples: "red.gif", "black.gif"
        * @param age An integer that represents the player's age which helps determine the queue.
        * Examples: 3, 45, 23
        */
    """

    def __init__(self, color, age):
        self.color = color  # The player's assigned color
        self.score = 0  # The player's score
        self.sprite = "Common/Other/{}.gif".format(self.color)  # Image file for the avatar
        self.age = age  # The player's age


"""
    This class represents a game state in the FISH game and houses the ability to control and determine 
    the state of the game.
"""


class GameState:
    """
        * Construct a GameState.
        * @param photocache A list of PhotoImage instances which helps Tkinter maintain its cache as
        it will normally garbage dump the files unless they're referenced in an extra variable. This will
        prevent images disappearing after a render.
        Example: [<Tkinter.PhotoImage instance at 0x0000000003476D48>]
        * @param players A list of Player class instances that the GameState class uses to help keep track
        of progress in the game and uses for its various functions.
        Example: [<__main__.Player instance at 0x0000000003456048>, <__main__.Player instance at 0x0000000003456308>]
        [("red", 12), ("black", 21)]
        * @param game_over A boolean that keeps track of the game status.
        Example: False, True
        */
    """

    def __init__(self, players):
        self.photocache = []  # Extra reference to images on canvas, for TKinter issue
        self.players = players  # list of players in order of turn
        self.moves_left = True  # if a player has any moves left or not
        self.game_over = False  # if the game is still ongoing or not

    """
        This function randomly chooses a tile from the hexagon board and places the avatar of the given Player class 
        instance on the tile.
        * @param hexboard A HexBoard class instance that represents the hexagon board which the penguins are
         visually placed on.
        Example: <__main__.HexBoard instance at 0x0000000003456048>
        * @param player A Player class instance that helps decide which avatar to place since it is based on the 
        player's color. 
        Example: 
        [("red", 12), ("black", 21)]
        <__main__.Player instance at 0x0000000003456048>
    """

    def place_penguin(self, hexboard, player):
        penguinsleft = 1
        while penguinsleft != 0:
            hexagon = random.choice(hexboard.hexagons)
            coord = hexagon.coordinates
            if hexagon.sunk or hexagon.spottaken:
                while hexagon.sunk or hexagon.spottaken:
                    hexagon = random.choice(hexboard.hexagons)
                    coord = hexagon.coordinates
            clicked = hexboard.can.find_closest(round(hexagon.x), round(hexagon.y))[0]
            filename = player.sprite
            photo = PhotoImage(file=filename)
            self.photocache.append(photo)
            hexboard.can.itemconfigure(clicked + (2 * len(hexboard.hexagons)), image=photo, state="normal")
            hexagon.spottaken = True
            hexagon.penguincolor = player.color
            penguinsleft += -1

    """
        This function takes in an destination(Integer) and modifies it by subtracting it from either twice 
        the length or once the length of the list of hexagons. This is to ensure the index returned has to
        do with a hexagon tile rather than a fish image or avatar image. 
        * @param destination An integer that represents the index to be modified.
        Example: 12, 45
        * @param hexboard A HexBoard class instance that represents the hexagon board which the index is based on.
        Example: <__main__.HexBoard instance at 0x0000000003456048>
    """

    def modify_index(self, destination, hexboard):
        if (3 * len(hexboard.hexagons)) >= destination > (2 * len(hexboard.hexagons)):
            destination += (-2 * len(hexboard.hexagons))
        elif 2 * len(hexboard.hexagons) >= destination > len(hexboard.hexagons):
            destination += (-1 * (len(hexboard.hexagons)))
        else:
            destination = destination
        return destination

    """
         This function moves an existing avatar from the origin tile to the destination tile if 
         it is a valid spot to move to. Valid being it is not a sunk tile(A hole) and not occupied by
         another avatar. 
         * @param origin An integer that represents the index of the originating tile from which the avatar is 
         being moved from. 
         * @param destination An integer that represents the index of the destination tile which the avatar is 
         being to. 
         * @param hexboard A HexBoard class instance that represents the hexagon board which the game is based on.
         * @param player A Player class instance that represents The associating player with the avatar move. 
    """

    def move_penguin(self, origin, destination, hexboard, player):
        destination = self.modify_index(destination, hexboard)
        origintile = hexboard.hexagons[int(origin) - 1]
        destinationtile = hexboard.hexagons[int(destination) - 1]
        validdestinations = hexboard.draw_connection(origintile.x, origintile.y)
        if origintile.spottaken and origintile.penguincolor == player.color:
            if not destinationtile.sunk and not destinationtile.spottaken:
                if destinationtile in validdestinations:
                    hexboard.can.itemconfigure(origin, fill="grey")
                    hexboard.can.itemconfigure(origin + (2 * len(hexboard.hexagons)), state="hidden")
                    hexboard.can.itemconfigure(origin + len(hexboard.hexagons), state="hidden")
                    origintile.sunk = True
                    destinationtile.spottaken = True
                    photo = PhotoImage(file='Common/Other/{}.gif'.format(player.color))
                    self.photocache.append(photo)
                    hexboard.can.itemconfigure(destination + (2 * len(hexboard.hexagons)), image=photo, state="normal")
                    player.score += destinationtile.fish
                else:
                    raise IndexError("This spot is not within the origin tile's reach.")
            else:
                raise IndexError("This spot is not available as it's sunk or occupied.")
        else:
            raise IndexError("This penguin does not belong to the player or the spot is not taken.")

    """
        This function determines whether the game is over or not.
        * @param hexboard A HexBoard class instance that represents the hexagon board which the game is based on."
        * @return has_moves A boolean that represents whether any player can move an avatar. 
    """

    def is_over(self, hexboard):
        has_moves = True
        for hex in hexboard.hexagons:
            neighborscount = 0
            if hex.spottaken:
                neighbors = hexboard.find_neighbors(hex)
                for neighbor in neighbors:
                    if not neighbor.sunk and not neighbor.spottaken:
                        neighborscount += 1
                if neighborscount > 1:
                    has_moves = False
        return has_moves


"""
   This function creates a state for a certain number of players.
   * @param players A list of Player class instances that are going to participate. 
   * @return game A GameState class instance that represents the game state of Fish.
"""


def create_state(players):
    queue = sorted(players, key=lambda x: x.age, reverse=False)
    game = GameState(queue)
    return game

"""
    This function serves the sole purpose of rendering the hexagon board visually. 
    * @param A HexBoard class instance that represents hexboard The hexagon board which the game is based on."
"""

def render_state(hex_board):
    hex_board.mainloop()


# This runs the test executor above
if __name__ == "__main__":
    player1 = Player('red', 3)
    player2 = Player('black', 4)
    players = [player1, player2]
    hex_board = fish.HexBoard(30, 9, 2, [])
    create_state(players, hex_board)
    render_state(hex_board)
