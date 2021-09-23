from Tkinter import *
from math import *
import random
import json
from state import *


"""
This class represents a single hexagon tile on the hexagon board.
"""

class FillHexagon:
    """
     * Construct a hexagon tile.
     * @param parent  The canvas which this tile is associated with
     * @param x The x value of the top left vertex
     * @param y The y value of the top left vertex
     * @param length The length of a side of the hexagon
     * @param color The color of the hexagon tile
     * @param tags The coordinates of the tile
     */
      """

    def __init__(self, x, y, length, grid_coords, is_sunk):
        # self.parent = parent  # canvas
        self.x = x  # top left x
        self.y = y  # top left y
        self.length = length  # length of a side
        # self.color = color  # fill color
        self.selected = False  # if tile was clicked last or not
        self.draw()  # draws the tile
        self.fish = random.randrange(1, 5)  # the amount of fish on a tile
        self.coordinates  # list of coordinates for the outline
        self.sunk = is_sunk  # If the tile has sunk already or not
        self.spottaken = False  # If the tile is occupied by a penguin
        self.xy = grid_coords  # Grid coordinate for the tile

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

"""
This class represents the hexagon board. The class has the ability to initialize the game state and houses
several functions which demonstrate the current capabilities of the game.
"""


class HexBoard:
    """
       * Construct a hexagon tile.
       * @param size  The canvas which this tile is associated with
       * @param col The number of columns on the board.
       * @param row The number of rows on the board.
       * @param mode The type of board mode.
       * @param holes Holes that should go on the board.
       */
    """

    def __init__(self, size, col, row, total, holes, hexboard):
        self.hexagons = []  # list of all hexagons
        self.size = size  # size of each tile
        self.cols = col  # amount of columns
        self.rows = row  # amount of rows
        self.holes = holes  # Holes that should be on the board.
        self.boardposn = hexboard
        self.fishtracker = []
        self.init_grid(total)  # initializes the grid


    """
    This function sets a layer on each tile containing the image of the fishes.
     * @param hex  The hexagon in which the image will be set on.
     * @param size The size of the hexagon tile.
    """



    """
        This function sets a layer on each tile containing the image of the fishes.
         * @param hexlist The list of hexagons which the penguins will be placed on.
         * @param size The size of the hexagon tile.
    """



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
                    # self.set_image_layer(hex, size)
                else:
                    hex.fish = 1
                    min_count += 1
                    # self.set_image_layer(hex, size)
            # else:
                # self.set_image_layer(hex, size)
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
                # self.set_image_layer(hex, size)
            # else:
                # self.set_image_layer(hex, size)

    """
           This function coordinates setting the number of fishes and which image goes with which number.
            * @param hex_list  The list of hexagons associated with the canvas.
            * @param size The size of the hexagon tile.
            * @param min_num Minimum number of one fish tiles, if any. Will be NONE if not needed.
            * @param set_number The number of fish to be set across all tiles, if any. Will be NONE if not needed.
    """

    def set_fishes(self, hex_list, size, min_num, set_number):
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
        if min_num > 0 and min_num != hex_total and set_number is None:
            self.set_fishminimum(hex_list, size, min_num, min_count, min_fish, max_fish, hex_count, hex_total, hex_sunk)
        elif min_num is None and set_number > 0:
            self.set_fishmaximum(hex_list, set_number, size)
        else:
            for hex in hex_list:
                if not hex.sunk:
                    hex.fish = random.randrange(1, 5)
                    # self.set_image_layer(hex, size)
                # else:
                    # self.set_image_layer(hex, size)

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
        This function creates a mega list of all the possible fish tiles and holes that can be easily processed.
            * @param hex_list  The list of hexagons associated with the canvas.
            * @param size The size of the hexagon tile.
            * @param list  The list of fish and possible holes for the board given by Board-Posn
    """

    def set_fishesxboard(self, hex_list, size, list):
        # print list
        newlist = self.set_newlist(list)
        newlist2 = []
        count = 0
        for hex in hex_list:
            if newlist[count] != 0:
                hex.fish = newlist[count]
                newlist2.append([newlist[count], hex.xy])
                # self.set_image_layer(hex, size)
            else:
                newlist2.append([newlist[count], hex.xy])
                hex.sunk = True
                # self.set_image_layer(hex, size)
                # self.can.itemconfigure(count + 1, fill="grey")
                # self.can.itemconfigure(count + 1 + len(self.hexagons), state=HIDDEN)
            # print'fish: ', hex.fish
            count += 1
        self.fishtracker = newlist2
        return newlist2

    """
        This function creates a mega list of all the possible fish tiles and holes that can be easily processed.
            * @param hex_list  The list of hexagons associated with the canvas.
            * @param position  The origin tile which will have its possible routes found.
            * @return neighborscount The possible amount of valid destinations for an origin tile.
    """

    def get_xboardreach(self, hex_list, position):
        neighborscount = 0
        actualx = ""
        actualy = ""
        for hex in hex_list:
            # print position
            # print hex.xy
            if position == hex.xy:
                # print "Found it!"
                actualx = hex.x
                actualy = hex.y
        # print 'actuals are: ', actualx, ' ', actualy
        # print actualx, ' ', actualy
        # clicked = self.can.find_closest(actualx, actualy)[0]
        # self.can.itemconfigure(clicked, fill="red")
        # print 'x, y: ', actualx, actualy
        neighbors = self.draw_connection(actualx, actualy)
        # print len(neighbors)
        for neighbor in neighbors:
            if not neighbor.sunk and not neighbor.spottaken:
                neighborscount += 1
                # clicked = self.can.find_closest(neighbor.x, neighbor.y)[0]
                # print clicked
                # self.can.itemconfigure(clicked, fill="purple")
        # print "reach count: ", neighborscount
        return neighborscount

    """
        This function initializes the grid.
        * @param mode The mode of the board, regular or for the test harness 'xboard'
    """

    def init_grid(self, mode):
        self.init_gridxboard(mode)

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
           This function lays down the hexagons on the board according to the limits given.
            * @param limit Counter for each progress in the loop so it doesn't go over the limit.
            * @param evenlimit Limits amount of hexagons in an even column.
            * @param oddlimit Limits amount of hexagons in an odd column.
            * @param holes The holes to be set in the board.
            * @param total The total number of hexagons on the board.
    """

    def set_xboardtiles(self, limit, evenlimit, oddlimit, holes, total):
        last = 0
        for r in range(evenlimit):
            for c in range(6):
                if c % 2 == 0:
                    if limit < evenlimit:
                        # print "limit, evenlimit: ", limit, ' ', evenlimit
                        offset = 0
                        self.fill_tile(c, r, self.size, holes, offset)
                        # print c, r
                else:
                    if limit < oddlimit:
                        # print "Asdasda"
                        offset = self.size * sqrt(3) / 2
                        self.fill_tile(c, r, self.size, holes, offset)
            # print "limit, ", limit
            limit += 1
            last = r
        if total != len(self.hexagons):
            self.adjust_xboardtiles(total, holes, last)
        # print "length: ", len(self.hexagons)
        # for hexagon in self.hexagons:
            # print hexagon.xy
            # print hexagon.x, ' ', hexagon.y

    """
        This function adds any extra hexagon tiles that might not have been added due to size constraints from
        following the rules.
        * @param total The total number of hexagons on the board.
        * @param holes The holes to be set in the board.
        * @param r The last row that was recorded.
    """

    def adjust_xboardtiles(self, total, holes, r):
        for col in range(6):
            # print "total, actual: ", total, len(self.hexagons)
            if total != len(self.hexagons):
                if col % 2 == 0:
                    offset = 0
                    self.fill_tile(col, r + 1, self.size, holes, offset)
                else:
                    offset = self.size * sqrt(3) / 2
                    self.fill_tile(col, r + 1, self.size, holes, offset)

    """
        This function creates the board specific style for the test harness, 'xboard'.
    """

    def init_gridxboard(self, total):
        """
        2d grid of hexagons
        """
        # holes = [(1, 1), (2, 2)]
        holes = self.holes
        limit = 0
        # total = self.rows * self.cols
        evenlimit = self.set_limits(total)[0]
        oddlimit = self.set_limits(total)[1]
        self.set_xboardtiles(limit, evenlimit, oddlimit, holes, total)
        self.set_fishesxboard(self.hexagons, 30, self.boardposn)
        # print len(self.hexagons)
        # self.set_fishesxboard(self.hexagons, 30, [[1,2,3],[4,0,5]])
        # self.set_fishesxboard(self.hexagons, 30, self.board)
        # self.set_fishesxboard(self.hexagons, 30, [[2, 4, 3], [1, 3, 3], [1, 2, 3], [3, 4, 2]])
        # self.set_penguins(self.hexagons, self.size)
        # reach = self.get_xboardreach(self.hexagons, [0, 3])
        # writeto = []
        # writeto.append(str(reach))
        # outF = open(self.output, 'w')
        # outF.writelines(writeto)
        # outF.close()

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
            is_sunk = True,
        else:
            is_sunk = False

        h = FillHexagon(c * (size * 1.5) + (size / 2),
                        (r * (size * sqrt(3))) + offset,
                        size,
                        [r, c], is_sunk)

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
        # print 'clicked: ', clicked
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

    def return_index(self, start_x, start_y):
        index = 0
        # print 'start: ', start_x, ' ', start_y
        # print len(self.hexagons)
        for hexagon in self.hexagons:
            # print hexagon.x, ' ', hexagon.y
            if hexagon.x == start_x and hexagon.y == start_y:
              return index
            index += 1


    def connect_lines(self, directions_list, start_x, start_y, greatest_possibility):
        valid_hexagons = []
        clicked = self.return_index(start_x, start_y)
        # print 'clicked: ', clicked
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
                        if not neighbor.sunk and neighbor not in valid_hexagons:
                            neighbor.isRoute = True
                            valid_hexagons.append(neighbor)
                        else:
                            stop = True
                            break
                        start_tile = self.hexagons[self.return_index(neighbor.x, neighbor.y)]
                    else:
                        pass
                clicked = self.return_index(start_tile.x, start_tile.y)
                start_count += 1
            stop = False
            clicked = self.return_index(start_x, start_y)  # Regrab origin tile index
            start_tile = self.reset_tiles(clicked)  # start from origin tile
        # print 'adasd', len(valid_hexagons)
        # for ne in valid_hexagons:
        #     print ne.xy
        return valid_hexagons

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
        directions = [top, top_right,  bot_right, bot, bot_left, top_left]
        greatest_possibility = self.rows * self.cols
        for direction in directions:
            direction = [direction]
            validhexs = self.connect_lines(direction, start_x, start_y, greatest_possibility)
            foundmove = False
            if len(validhexs) >= 1:
                foundmove = True
                return validhexs[0]
        if not foundmove:
            return foundmove

def main():
    import fileinput
    contents = input()
    total = 0
    # with open(file) as load:
    players = contents["players"]
    if players is []:
        print False
    else:
        hexboard2 = contents["board"]
        for x in hexboard2:
            if type(x) == list:
                for num in x:
                    total += 1
        try:
            hexboard = HexBoard(30, 3, 3, total, [], hexboard2)
            subject = players[0]
            subjectpenguin = subject["places"]
            if subjectpenguin is []:
                print False
            else:
                subjecttile = subjectpenguin[0]
                found = False
                for hex in hexboard.hexagons:
                    if hex.xy == subjecttile:
                        found = True
                        thescore = hex.fish
                if not found:
                    print False
                else:
                    move = hexboard.draw_connection(hex.x, hex.y)
                    if type(move) is bool:
                        print False
                    else:
                        try:
                            count = 0
                            revisedlist = []
                            for coord in hexboard.fishtracker:
                                if coord[1] == subjecttile:
                                    hexboard.fishtracker[count][0] = 0
                                revisedlist.append(hexboard.fishtracker[count][0])
                                count += 1
                            players[0]["places"][0] = move.xy
                            players[0]["score"] = int(players[0]["score"]) + thescore
                            eachgroup = total / 3
                            eachgroupleft = eachgroup % 2
                            cutoff = 0
                            if eachgroupleft == 1:
                                cutoff = eachgroup - eachgroupleft
                            newboard = []
                            check = 0
                            revisedlist2 = []
                            if cutoff != 0:
                                while eachgroup != 1:
                                    two = 0
                                    check = 0
                                    while two != 2:
                                        addtoboard = []
                                        addtoboard.append(revisedlist[check])
                                        addtoboard.append(revisedlist[check + 2])
                                        addtoboard.append(revisedlist[check + 4])
                                        revisedlist2.append(addtoboard)
                                        two += 1
                                        check += 1
                                    num = 0
                                    while num != 6:
                                        revisedlist = revisedlist[1:]
                                        num += 1
                                    eachgroup += -2
                                if eachgroup == 1:
                                    addtoboard = []
                                    lastindex = len(revisedlist) - 1
                                    addtoboard.append((revisedlist[lastindex - 2]))
                                    addtoboard.append((revisedlist[lastindex - 1]))
                                    addtoboard.append((revisedlist[lastindex]))
                                    revisedlist2.append(addtoboard)
                            else:
                                while eachgroup != 0:
                                    two = 0
                                    check = 0
                                    while two != 2:
                                        addtoboard = []
                                        addtoboard.append(revisedlist[check])
                                        addtoboard.append(revisedlist[check + 2])
                                        addtoboard.append(revisedlist[check + 4])
                                        revisedlist2.append(addtoboard)
                                        two += 1
                                        check += 1
                                    num = 0
                                    while num != 6:
                                        revisedlist = revisedlist[1:]
                                        num += 1
                                    eachgroup += -2
                            stateoutput = {"players": '', "board": ''}
                            stateoutput["players"] = players
                            stateoutput["board"] = revisedlist2
                            print stateoutput
                        except:
                            stateoutput = {"players": '', "board": ''}
                            stateoutput["players"] = players
                            stateoutput["board"] = hexboard2
                            print stateoutput
        except:
            print False
main()
