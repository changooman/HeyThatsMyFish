from Fish.Common.tile import Tile

class Board():
    """Represents a Fish game board.

    self.rows:   The number of rows of the game board.
    self.cols:   The number of columns of the game board.
    self.tiles:  A 2D array of Tiles on the board, where None represents a hole.

    The coordinate system works as follows:
     _____       _____       _____       _____
    / 0,0 \_____/ 0,1 \_____/ 0,2 \_____/ 0,3 \_____
    \_____/ 1,0 \_____/ 1,1 \_____/ 1,2 \_____/ 1,3 \
    / 2,0 \_____/ 2,1 \_____/ 2,2 \_____/ 2,3 \_____/
    \_____/ 3,0 \_____/ 3,1 \_____/ 3,2 \_____/ 3,3 \
    / 4,0 \_____/ 4,1 \_____/ 4,2 \_____/ 4,3 \_____/
    \_____/ 5,0 \_____/ 5,1 \_____/ 5,2 \_____/ 5,3 \
    / 6,0 \_____/ 6,1 \_____/ 6,2 \_____/ 6,3 \_____/
    \_____/     \_____/     \_____/     \_____/
    """

    def __init__(self, rows, cols, holes=[], min_one_fish=0, uniform=False, uniform_num_fish=0):
        """Initialize a game board

        rows:   The number of rows of the game board.
        cols:   The number of columns of the game board.
        holes:  A list of 2D coordinate tuples where holes should appear on the game board, 0 indexed.
        min_one_fish:   The minimum number of tiles that should have one fish on them.
        uniform:    Whether or not to place the same number of fish on every tile and have no holes.
        uniform_num_fish:   The number of fish to place on each tile if the board is uniform.
        """
        if rows < 1:
            raise ValueError("Board rows must be positive.")
        if cols < 1:
            raise ValueError("Board cols must be positive.")

        self.rows = rows
        self.cols = cols

        self.tiles = []
        for r in range(rows):
            self.tiles.append([])
            for c in range(cols):
                if uniform:
                    self.tiles[r].append(Tile(False, uniform_num_fish))
                elif (r, c) in holes:
                    self.tiles[r].append(None)
                elif min_one_fish > 0:
                    self.tiles[r].append(Tile(False, 1))
                    min_one_fish -= 1
                else:
                    self.tiles[r].append(Tile())


    def __ne__(self, other):
        return not self.__eq__(other)


    def __eq__(self, other):
        return (isinstance(other, Board) and
                self.tiles == other.tiles)


    def json_rep(self):
        """Represent the board as Python data structures in format for json.

        returns:    The representation.
        """
        rep = []
        for row in self.tiles:
            rep.append([])
            for tile in row:
                if tile is not None:
                    rep[-1].append(tile.get_num_fish())
                else:
                    rep[-1].append(0)
        return rep


    def get_rows(self):
        """Get the number of rows on this board.

        returns:    The number of rows.
        """
        return self.rows


    def get_cols(self):
        """Get the number of columns on this board.

        returns:    The number of columns.
        """
        return self.cols


    def __valid_coords(self, coords):
        """Check that a set of tile coordinates are within the bounds of the board.

        coords:   A tuple of the tile position (row, column).

        returns:    True if the coordinates are within bounds, False otherwise.
        """
        return 0 <= coords[0] < self.rows and 0 <= coords[1] < self.cols


    def get_reachable(self, coords, penguins):
        """Get the reachable positions from a specific tile on the board.

        This includes all tiles in a straight line from the position in question,
        stopping in each direction if a penguin or hole is encountered.

        coords:   A tuple of the starting position tile (row, column).
        penguins:   A list of penguin coordinates.

        returns:    A List of reachable tile coordinates in tuple form.
        """
        def can_reach(row, col):
            """Small helper to avoid repeating reachability checks.

            row:    tile row
            col:    tile column

            returns:    True the reachable tile candidate is reachable, False otherwise.
            """
            return (self.__valid_coords((row, col)) and
                    self.tiles[row][col] is not None and
                    (row, col) not in penguins)


        reachable = []
        row, col = coords

        if (not self.__valid_coords((row, col)) or
            self.tiles[row][col] is None):
            return reachable

        def trace_line(func):
            """Move in a straight line in one direction,
            appending each tile to reachable if it can be reached.

            func:   A function of signature foo(row, col)->(row, col) that moves the coordinate
                    along one tile in a direction each time it is called.
            """
            row, col = coords
            while True:
                row, col = func(row, col)
                if can_reach(row, col):
                    reachable.append((row, col))
                else:
                    break


        trace_line(lambda row, col: (row-2, col))  # north
        trace_line(lambda row, col: (row+2, col))  # sourth
        trace_line(lambda row, col: (row-1, col+1) if row % 2 == 1 else (row-1, col))  # northeast
        trace_line(lambda row, col: (row+1, col+1) if row % 2 == 1 else (row+1, col))  # southeast
        trace_line(lambda row, col: (row-1, col-1) if row % 2 == 0 else (row-1, col))  # northwest
        trace_line(lambda row, col: (row+1, col-1) if row % 2 == 0 else (row+1, col))  # southwest

        return reachable


    def get_tile(self, coords):
        """Gets a tile from the board.

        coords:   A tuple of the tile position (row, column).

        returns the tile at the given position or None if a tile doesn't exist.
        """
        if self.__valid_coords(coords):
            return self.tiles[coords[0]][coords[1]]
        else:
            return None

    def remove_tile(self, coords):
        """Remove a tile from the board.

        coords:   A tuple of the tile position (row, column).
        """
        if self.__valid_coords(coords):
            self.tiles[coords[0]][coords[1]] = None


    def draw(self, ctx, players):
        """Draw the board.

        ctx:    The drawing context to draw the board in.
        players:    A list of players whose penguins to draw on the board
        """
        ctx.set_source_rgb(1, 1, 1)
        ctx.paint()

        # move the drawing "cursor" to the top left of each tile and draw it
        ctx.move_to(Tile.VISUAL_SIZE, Tile.VISUAL_SIZE)

        for c in range(self.cols):
            for r in range(self.rows):
                if self.tiles[r][c] is not None:
                    player_color = None
                    for p in players:
                        if (r, c) in p.get_penguins():
                            player_color = p.get_color()
                            break
                    point = ctx.get_current_point()
                    self.tiles[r][c].draw(ctx, player_color)
                    ctx.move_to(*point)
                if r % 2 == 0:
                    ctx.rel_move_to(2 * Tile.VISUAL_SIZE, Tile.VISUAL_SIZE)
                else:
                    ctx.rel_move_to(-2 * Tile.VISUAL_SIZE, Tile.VISUAL_SIZE)
            ctx.move_to((c+1) * 4 * Tile.VISUAL_SIZE + Tile.VISUAL_SIZE, Tile.VISUAL_SIZE)


























