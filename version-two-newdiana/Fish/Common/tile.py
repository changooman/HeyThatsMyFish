import cairo
import os
import random

dir_path = os.path.dirname(os.path.abspath(__file__))
PENGUIN_IMAGES = { "red":      "/red_penguin.png",
                   "white":    "/white_penguin.png",
                   "brown":    "/brown_penguin.png",
                   "black":    "/black_penguin.png" }

for color in PENGUIN_IMAGES.keys():
    path = dir_path + PENGUIN_IMAGES[color]
    PENGUIN_IMAGES[color] = cairo.ImageSurface.create_from_png(path)

class Tile():
    """Represents a single tile in the game of fish.

    self.num_fish:  The number of fish on the Tile.
    """

    MAX_FISH = 5
    VISUAL_SIZE = 50

    def __init__(self, random_num_fish=True, num_fish=0):
        """Initialize the tile.

        random_num_fish:    Whether or not to randomize how many fish are on the tile.
        num_fish:   The number of fish on the tile; must be between 1 and Tile.MAX_FISH inclusive.
        """
        if random_num_fish:
            self.num_fish = random.randint(1, Tile.MAX_FISH)
        elif not 1 <= num_fish <= Tile.MAX_FISH:
            raise ValueError("Number of fish on a Tile must be positive and cannot exceed " + str(Tile.MAX_FISH))
        else:
            self.num_fish = num_fish
        self.penguin = None


    def __ne__(self, other):
        return not self.__eq__(other)


    def __eq__(self, other):
        return (isinstance(other, Tile) and
                self.num_fish == other.num_fish)


    def get_num_fish(self):
        """Returns the number of fish on the tile."""
        return self.num_fish


    def draw(self, ctx, player_color):
        """Draw the tile with its fish.

        ctx:    The drawing context to draw the tile in.
        player_color:   The color to draw the penguin on the tile,
                        or None if no penguin is present.
        """
        # draw the tile
        side = self.VISUAL_SIZE
        ctx.rel_move_to(side, 0)
        ctx.rel_line_to(side, 0)
        ctx.rel_line_to(side, side)
        ctx.rel_line_to(-side, side)
        ctx.rel_line_to(-side, 0)
        ctx.rel_line_to(-side, -side)
        ctx.rel_line_to(side, -side)

        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(5)
        ctx.stroke_preserve()

        ctx.set_source_rgb(1, 1, 1)
        point = ctx.get_current_point()
        ctx.fill()
        ctx.move_to(*point)

        # draw the fish
        fish_size = side / 2.5
        def draw_fish():
            """Draw a fish on the tile.

            ctx:    The drawing context to draw the fish in.
            """
            ctx.rel_line_to(2 * fish_size, fish_size)
            ctx.rel_line_to(0.5 * fish_size, -fish_size / 2)
            ctx.rel_line_to(-0.5 * fish_size, -fish_size / 2)
            ctx.rel_line_to(-2 * fish_size, fish_size)
            ctx.rel_line_to(0, -fish_size)
            ctx.set_source_rgb(0, 0, 1)
            point = ctx.get_current_point()
            ctx.fill()
            ctx.move_to(*point)

        for _ in range(self.num_fish):
            draw_fish()
            ctx.rel_move_to(0, fish_size)
        ctx.rel_move_to(0, -fish_size * self.num_fish)

        if player_color is not None:
            ctx.rel_move_to(-20, 5)
            x, y = ctx.get_current_point()
            ctx.set_source_surface(PENGUIN_IMAGES[player_color], x, y)
            ctx.paint()
