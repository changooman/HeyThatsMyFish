from Tkinter import *
from math import *
import random

"""
This class represents a single hexagon tile on the hexagon board.
"""


class FillHexagon:
    """
     * Constructs & Represents a hexagon tile.
     * @param parent  The canvas which this tile is associated with
     * @param x The x value of the top left vertex
     * @param y The y value of the top left vertex
     * @param length The length of a side of the hexagon
     * @param color The color of the hexagon tile
     * @param tags The coordinates of the tile
     */
      """

    def __init__(self, parent, x, y, length, color, tags):
        self.parent = parent  # canvas
        self.x = x  # top left x
        self.y = y  # top left y
        self.length = length  # length of a side
        self.color = color  # fill color
        self.selected = False  # if tile was clicked last or not
        self.tags = tags  # coordinates of the tile
        self.draw()  # draws the tile
        self.fish = random.randrange(1, 5)  # the amount of fish on a tile
        self.coordinates  # list of coordinates for the outline
        self.sunk = False  # If the tile has sunk already or not
        self.spottaken = False  # If the tile is occupied by a penguin
        self.xy = [] # Grid coordinate for the tile

    """
    This function draws a hexagon tile on the board.
    """

    def draw(self):
        start_x = self.x
        start_y = self.y
        angle = 60
        coords = []
        sides = 6
        for i in range(sides):
            end_x = round(start_x + self.length * cos(radians(angle * i)))
            end_y = round(start_y + self.length * sin(radians(angle * i)))
            start_x = end_x
            start_y = end_y
            coords.append((start_x, start_y))
        self.coordinates = coords
        self.parent.create_polygon(self.coordinates,
                                   fill=self.color,
                                   outline="black",
                                   tags=self.tags)


"""
    This class represents the hexagon board. it initializes the game state and houses
    several functions which demonstrate the current capabilities of the game.
"""


class HexBoard(Tk):
    """
       * Construct a hexagon tile.
       * @param size  The canvas which this tile is associated with
       * @param col The number of columns on the board.
       * @param row The number of rows on the board.
       * @param mode The type of board mode.
       * @param holes Holes that should go on the board.
       */
    """

    def __init__(self, size, col, row, holes):
        Tk.__init__(self)
        self.title("Hexagon Grid")  # title of the board
        self.can_color = "grey"  # color of the background
        self.tile_color = "orange"  # color of the tile
        self.can = Canvas(self, width=800, height=600, bg=self.can_color)  # defining the canvas
        self.can.pack()  # packs the canvas
        self.hexagons = []  # list of all hexagons
        self.pics = []  # list of pics used to represent fish
        self.size = size  # size of each tile
        self.cols = col  # amount of columns
        self.rows = row  # amount of rows
        self.holes = holes # Holes that should be on the board.
        self.init_grid()  # initializes the grid
        self.can.bind("<Button-1>", self.click)  # binds the canvas with click action

    """
    This function sets a layer on each tile containing the image of the fishes.
     * @param hex  The hexagon in which the image will be set on.
     * @param size The size of the hexagon tile.
    """

    def set_image_layer(self, hex, size):
        filename = 'Common/Other/{}.gif'.format(str(hex.fish))
        photo = PhotoImage(file=filename)
        self.pics.append(photo)
        if not hex.selected:
            self.can.create_image((hex.x + (size / 2)), (hex.y + (size / 2)), image=photo)
        else:
            self.can.create_image((hex.x + (size / 2)), (hex.y + (size / 2)), image=photo, state=HIDDEN)

    """
        This function sets a layer on each tile containing the image of the fishes.
         * @param hexlist The list of hexagons which the penguins will be placed on.
         * @param size The size of the hexagon tile.
    """

    def set_penguins(self, hexlist, size):
        filename = 'Common/Other/black.gif'
        photo = PhotoImage(file=filename)
        self.pics.append(photo)
        for hex in hexlist:
            self.can.create_image((hex.x + (size / 2)), (hex.y + (size / 2)), image=photo, state=HIDDEN)

    """
       This function coordinates setting the minimum number of one fish tiles.
        * @param hex_list  The list of hexagons associated with the canvas.
        * @param size The size of the hexagon tile.
        * @param min_num Goal of one fish tiles to be set. 
        * @param min_count The number of one tile fish added so far.
        * @param min_fish The least possible amount of fish.
        * @param max_fish The maximum possible amount of fish.
        * @param hex_count The number of hexagon tiles processed.
        * @param hex_total The total number of hexagon tiles available.
    """

    def set_fishminimum(self, hex_list, size, min_num, min_count, min_fish, max_fish, hex_count, hex_total, hex_sunk):
        # checks if there in a minimum number of fish counts
        hex_remain = len(hex_list) - hex_sunk
        for hex in hex_list:
            if not hex.sunk:
                if hex_remain > min_num - min_count:
                    hex.fish = random.randrange(min_fish, max_fish)
                    if hex.fish == 1:
                        min_count += 1
                    self.set_image_layer(hex, size)
                else:
                    hex.fish = 1
                    min_count += 1
                    self.set_image_layer(hex, size)
            else:
                self.set_image_layer(hex, size)
            hex_count += 1
            hex_remain = hex_total - hex_count

    """
          This function coordinates setting all fish tiles to a set number of fish.
           * @param hex_list  The list of hexagons associated with the canvas.
           * @param size The size of the hexagon tile.
           * @param set_number The number of fish each tile should be set to.
    """

    def set_fishmaximum(self, hex_list, set_number, size):
        for hex in hex_list:
            if not hex.sunk:
                hex.fish = set_number
                self.set_image_layer(hex, size)
            else:
                self.set_image_layer(hex, size)

    """
           This function coordinates setting the number of fishes and which image goes with which number.
            * @param hex_list  The list of hexagons associated with the canvas.
            * @param size The size of the hexagon tile.
            * @param min_num Minimum number of one fish tiles, if any. Will be NONE if not needed.
            * @param set_number The number of fish to be set across all tiles, if any. Will be NONE if not needed.
    """

    def set_fishes(self, hex_list, size, min_num, set_number):
        if min_num <= len(self.hexagons):
            min_fish = 1
            max_fish = 5
            hex_count = 0
            hex_sunk = 0
            for hex in hex_list:
                if hex.sunk:
                    hex_sunk += 1
            hex_total = len(hex_list) - hex_sunk
            min_count = 0
            # checks if there in a minimum number of fish counts
            if min_num is not None and min_num > 0 and min_num != hex_total and set_number is None:
                self.set_fishminimum(hex_list, size, min_num, min_count, min_fish, max_fish, hex_count, hex_total, hex_sunk)
            elif min_num is None and set_number > 0:
                self.set_fishmaximum(hex_list, set_number, size)
            else:
                for hex in hex_list:
                    if not hex.sunk:
                        hex.fish = random.randrange(1, 5)
                        # print'fish: ', hex.fish
                        self.set_image_layer(hex, size)
                    else:
                        self.set_image_layer(hex, size)
        else:
            raise IndexError("Minimum one fish requirement is greater than available tiles.")

    """
             This function creates a mega list of all the possible fish tiles and holes that can be easily processed.
              * @param list  The list of fish and possible holes for the board given by Board-Posn
              * @return newlist Modified mega list that will be used to help map the rest of the board's data.
    """

    def set_newlist(self, list):
        newlist = []
        start = 0
        end = 1
        endreached = False
        if len(list) % 2 == 0:
            shift = 1
        else:
            shift = 2
        while not endreached:
            grab = 0
            for index in list[start]:
                newlist.append(index)
                newlist.append(list[end][grab])
                grab += 1
            if end + shift == len(list):
                if shift == 2:
                    for index2 in list[len(list) - 1]:
                        newlist.append(index2)
                else:
                    pass
                endreached = True
                break
            start += 2
            end += 2
        return newlist

    """
        This function initializes the grid.
    """
    def init_grid(self):
        """
                2d grid of hexagons
                """
        # holes = [(1, 1), (2, 2)]
        holes = self.holes
        for r in range(self.rows):
            for c in range(self.cols):
                if c % 2 == 0:
                    offset = self.size * sqrt(3) / 2
                else:
                    offset = 0
                self.fill_tile(c, r, self.size, holes, offset)

        self.set_fishes(self.hexagons, self.size, None, None)
        self.set_penguins(self.hexagons, self.size)

    """
        This function decides the number of hexagons in each column.
         * @param total The total number of hexagons on the board.
         * @return [evenlimit, oddlimit] A list of the even and odd limitations.
    """
    def set_limits(self, total):
        if total % 2 == 0 and (total / 6) * 6 == total:
            # print "asdasd"
            oddlimit = total / 6
            evenlimit = total / 6
        else:
            odd_leftover = total % 6
            evenlimit = (total - odd_leftover) / 3
            oddlimit = odd_leftover / 3
            # print "Even limit, odd limit: ", evenlimit, ' ', oddlimit
            if oddlimit == 0 or evenlimit - oddlimit >= 2:
                oddlimit = int(round(total / 6))
                evenlimit = int(round(total / 6))
                # print "oddlimit, evenlimit: ", oddlimit, evenlimit
        return [evenlimit, oddlimit]

    """
        This function connects to the FillHexagon class and checks if a tile should become a hole or not.
        * @param c The number of columns.
        * @param r The number of rows.
        * @param size The size of the hexagon tile.
        * @param The list of holes to be set. 
        * @param The offset of the hexagon board. 
    """

    def fill_tile(self, c, r, size, holes, offset):

        if (c, r) in holes:
            color = self.can_color
        else:
            color = self.tile_color

        h = FillHexagon(self.can,
                        c * (size * 1.5) + (size / 2),
                        (r * (size * sqrt(3))) + offset,
                        size,
                        color,
                        "{}.{}".format(r, c))
        h.xy = [r,c]
        # print h.xy
        if color == self.can_color:
            h.selected = True
            h.sunk = True

        self.hexagons.append(h)

    """
        This function finds the neighbors of the current tile
        * @param current The current tile.
        * @return A list of tiles that neighbor the current tile.
    """

    def find_neighbors(self, current):
        current_coords = current.coordinates
        neighbors = []
        for hexagon in self.hexagons:
            intersection = set(current_coords).intersection(hexagon.coordinates)
            if len(intersection) == 2:
                neighbors.append(hexagon)
        return neighbors

    """
         This function handles mouse clicks and runs them through the game rules set in place.
         * @param evt The coordinates of the mouse click.
    """

    def click(self, evt):
        """
        hexagon detection on mouse click
        """
        for i in self.hexagons:
            i.isNeighbour = False
            i.isRoute = False
        x, y = evt.x, evt.y
        clicked = self.can.find_closest(x, y)[0]  # find closest hexagon to current mouse click
        try:
            current_tile = self.hexagons[int(clicked) - 1]
            if not current_tile.sunk:
                self.draw_connection(current_tile.x, current_tile.y)
                neighbors = self.find_neighbors(self.hexagons[int(clicked) - 1])
                for x in neighbors:
                    if x.sunk is False:
                        x.isNeighbour = True
                self.hexagons[int(clicked) - 1].selected = True
                for i in self.hexagons:
                    if i.selected:  # re-configure selected only
                        i.sunk = True
                        self.can.itemconfigure(i.tags, fill="grey")
                        self.can.itemconfigure(clicked + len(self.hexagons), state=HIDDEN)
                    if i.isRoute:  # if the tiles are on the straight path they will appear red
                        self.can.itemconfigure(i.tags, fill="red")
            else:
                pass
        except IndexError as e:
            pass

    """
        This function adjusts the index of a hexagon tile according to the length of the hexagon list.
        * @param clicked The index of the hexagon tile.
        * @return The adjusted index of the hexagon tile.
    """

    def adjust_hexagon_index(self, clicked):
        if clicked > len(self.hexagons):
            clicked = clicked - len(self.hexagons)
        return clicked

    """
        This function serves to reset the starting tile to the origin hexagon so that it can try other paths.
        * @param clicked The index of the hexagon tile.
        * @return The origin hexagon tile of the path.
    """

    def reset_tiles(self, clicked):
        clicked = self.adjust_hexagon_index(clicked)
        start_tile = self.hexagons[int(clicked) - 1]
        return start_tile

    """
        This function defines the straight paths from the clicked hexagon.
        * @param directions_list A list of all the possible directions of a hexagon tile.
        * @param start_x The x coordinate of the origin hexagon.
        * @param start_y The y coordinate of the origin hexagon.
        * @param greatest_possibility The maximum number of tiles possible for every path.
        * @return valid_hexagons The list of possible routes for the origin tile.
    """

    def connect_lines(self, directions_list, start_x, start_y, greatest_possibility):
        reachable_positions = []
        clicked = self.can.find_closest(start_x, start_y)[0]  # Grab origin tile index
        start_tile = self.reset_tiles(clicked)  # Start from origin tile
        stop = False
        for direction in directions_list:
            direction_one = direction[0]
            direction_two = direction[1]
            start_count = 0
            while start_count != greatest_possibility and not stop:
                direction_coords = [start_tile.coordinates[direction_one], start_tile.coordinates[direction_two]]
                clicked = self.adjust_hexagon_index(clicked)
                neighbors = self.find_neighbors(self.hexagons[int(clicked) - 1])
                for neighbor in neighbors:
                    intersection = set(direction_coords).intersection(neighbor.coordinates)
                    if len(intersection) == 2:
                        if not neighbor.sunk:
                            neighbor.isRoute = True
                            reachable_positions.append(neighbor)
                        else:
                            stop = True
                        start_tile = self.hexagons[self.can.find_closest(neighbor.x, neighbor.y)[0] - 1]
                    else:
                        pass
                clicked = self.can.find_closest(start_tile.x, start_tile.y)[0]
                start_count += 1
            stop = False
            clicked = self.can.find_closest(start_x, start_y)[0]  # Regrab origin tile index
            start_tile = self.reset_tiles(clicked)  # start from origin tile
        return reachable_positions

    """
         This function coordinates the possible path finding of a hexagon tile.
         * @param start_x The x coordinate of the origin hexagon.
         * @param start_y The y coordinate of the origin hexagon.
         * @return validhexs The list of possible routes for the origin tile.
     """

    def draw_connection(self, start_x, start_y):
        bot_left = [3, 4]
        bot_right = [1, 2]
        top = [0, 5]
        bot = [2, 3]
        top_right = [1, 0]
        top_left = [4, 5]
        directions = [top, bot, bot_left, bot_right, top_left, top_right]
        # if self.rows > self.cols:
        #     greatest_possibility = self.rows
        # else:
        #     greatest_possibility = self.cols
        greatest_possibility = self.rows * self.cols
        reachable_positions = self.connect_lines(directions, start_x, start_y, greatest_possibility)
        return reachable_positions


"""
    This executes the FISH game and helps demo the current capabilities.
"""
if __name__ == '__main__':
    hex_board = HexBoard(30, 4, 3, [(1, 1), (2, 2)])
    hex_board.mainloop()
