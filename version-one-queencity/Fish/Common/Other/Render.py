from Tkinter import *
from math import *


class Render:
    def __init__(self, board, state):
        Tk.__init__(self)
        self.title("Hexagon Board")  # title of the board
        self.can_color = "grey"  # color of the background
        self.tile_color = "orange"  # color of the tile
        self.can = Canvas(self, width=800, height=600, bg=self.can_color)  # defining the canvas
        self.can.pack()  # packs the canvas
        self.pics = []  # list of pics used to represent fish
        self.board = board
        self.state = state

    """
    This function draws the hexagon tile on the hexagon board.
    """

    def draw(self, hexagons):
        for hexagon in hexagons:
            start_x = hexagon.x
            start_y = hexagon.y
            angle = 60
            coords = []
            sides = 6
            for i in range(sides):
                end_x = round(start_x + hexagon.length * cos(radians(angle * i)))
                end_y = round(start_y + hexagon.length * sin(radians(angle * i)))
                start_x = end_x
                start_y = end_y
                coords.append((start_x, start_y))
            hexagon.coordinates = coords
            hexagon.parent.create_polygon(hexagon.coordinates,
                                        fill=hexagon.color,
                                        outline="black",
                                        tags=hexagon.tags)


        def set_image_layer(self, hex, size):
            # filename = '{}.gif'.format(str(hex.fish))
            # photo = PhotoImage(file=filename)
            # self.pics.append(photo)
            if not hex.selected:
                pass
                self.can.create_image((hex.x + (size / 2)), (hex.y + (size / 2)), image=photo)
            else:
                pass
                self.can.create_image((hex.x + (size / 2)), (hex.y + (size / 2)), image=photo, state=HIDDEN)

        def set_penguins(self, hexlist, size):
            # filename = 'black.gif'
            # photo = PhotoImage(file=filename)
            # self.pics.append(photo)
            for hex in hexlist:
                pass
                self.can.create_image((hex.x + (size / 2)), (hex.y + (size / 2)), image=photo, state=HIDDEN)