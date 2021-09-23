from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State
from Fish.Player.player import Player

from copy import deepcopy
import unittest

class TestPlayer(unittest.TestCase):
    """Test the Player class."""

    def setUp(self):
        """Create some players for test use."""
        self.red = Player("red")
        self.black = Player("black")


    def test_make_placement(self):
        """Test the make_placement function."""

        board = Board(3, 2, [(1, 1)])
        state = State([BoardPlayer("black"), BoardPlayer("red")], board)

        players = state.get_players()
        black = players[0]
        red = players[1]

        self.assertEqual([], black.get_penguins())
        self.assertEqual([], red.get_penguins())

        self.assertEqual((0, 0), self.black.make_placement(state))
        state.place_avatar((0, 0), "black")

        self.assertEqual((0, 1), self.red.make_placement(state))
        state.place_avatar((0, 1), "red")

        self.assertEqual((1, 0), self.black.make_placement(state))
        state.place_avatar((1, 0), "black")

        # should skip hole
        self.assertEqual((2, 0), self.red.make_placement(state))
        state.place_avatar((2, 0), "red")

        self.assertEqual((2, 1), self.black.make_placement(state))
        state.place_avatar((2, 1), "black")

        # no more avatars can be placed
        try:
            self.red.make_placement(state)
            self.assertTrue(False)
        except ValueError:
            pass


    def test_make_move(self):
        """Test the make_move() function."""

        """
         _____       _____
        / 0,0 \_____/ 0,1 \_____
        \__R__/ 1,0 \__B__/ 1,1 \
        / 2,0 \__0__/ 2,1 \__0__/
        \__0__/ 3,0 \__0__/ 3,1 \
              \__0__/     \__0__/
        """
        board = Board(1, 2, uniform=True, uniform_num_fish=1)

        # test excpetion
        red = BoardPlayer("red")
        black = BoardPlayer("black")
        state = State([red, black], deepcopy(board))
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        try:
            self.red.make_move(state)
            self.assertTrue(False)
        except ValueError:
            pass

        """
         _____       _____
        / 0,0 \_____/ 0,1 \_____
        \__R__/ 1,0 \__B__/ 1,1 \
        / 2,0 \_____/ 2,1 \_____/
        \__5__/ 3,0 \_____/ 3,1 \
              \_____/     \_____/
        """
        board = Board(4, 2, uniform=True, uniform_num_fish=1)
        board.tiles[2][0].num_fish = 5

        # test that the 5 fish tile is always the best move
        red = BoardPlayer("red")
        black = BoardPlayer("black")
        state = State([red, black], deepcopy(board))
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        self.assertEqual(((0, 0), (2, 0)), self.red.make_move(state))

        """
         _____       _____
        / 0,0 \_____/ 0,1 \_____
        \__R__/ 1,0 \__B__/ 1,1 \
        / 2,0 \__B__/ 2,1 \__R__/
        \__5__/ 3,0 \_____/ 3,1 \
              \_____/     \__5__/
        """
        board = Board(4, 2, uniform=True, uniform_num_fish=1)
        board.tiles[2][0].num_fish = 5
        board.tiles[3][1].num_fish = 5

        # test tie-breaking
        red = BoardPlayer("red")
        black = BoardPlayer("black")
        state = State([red, black], deepcopy(board))
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 1), "red")
        state.place_avatar((1, 0), "black")
        self.assertEqual(((0, 0), (2, 0)), self.red.make_move(state))

        """
         _____       _____
        / 0,0 \_____/ 0,1 \_____
        \__R__/ 1,0 \__B__/ 1,1 \
        / 2,0 \__W__/ 2,1 \__R__/
        \__5__/ 3,0 \__W__/ 3,1 \
              \__B__/     \__5__/
        """
        board = Board(4, 2, uniform=True, uniform_num_fish=1)
        board.tiles[2][0].num_fish = 5
        board.tiles[3][1].num_fish = 5

        # test with 3 players
        red = BoardPlayer("red")
        black = BoardPlayer("black")
        white = BoardPlayer("white")
        state = State([red, black, white], deepcopy(board))
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "white")
        state.place_avatar((1, 1), "red")
        state.place_avatar((3, 0), "black")
        state.place_avatar((2, 1), "white")
        self.assertEqual(((0, 0), (2, 0)), self.red.make_move(state))

        """
         _____       _____
        / 0,0 \_____/ 0,1 \_____
        \__R__/ 1,0 \__B__/ 1,1 \
        / 2,0 \__B__/ 2,1 \__R__/
        \__5__/ 3,0 \__5__/ 3,1 \
              \_____/     \__5__/
        """
        board = Board(4, 2, uniform=True, uniform_num_fish=1)
        board.tiles[2][0].num_fish = 5
        board.tiles[2][1].num_fish = 5
        board.tiles[3][1].num_fish = 5

        # test optimal strategy
        red = BoardPlayer("red")
        black = BoardPlayer("black")
        state = State([red, black], deepcopy(board))
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 1), "red")
        state.place_avatar((1, 0), "black")
        self.assertEqual(((1, 1), (2, 1)), self.red.make_move(state))

        """
         _____       _____
        / 0,0 \_____/ 0,1 \_____
        \__R__/ 1,0 \__B__/ 1,1 \
        / 2,0 \__B__/ 2,1 \__R__/
        \__4__/ 3,0 \__5__/ 3,1 \
              \_____/     \__5__/
        """
        board = Board(4, 2, uniform=True, uniform_num_fish=1)
        board.tiles[2][0].num_fish = 4
        board.tiles[2][1].num_fish = 5
        board.tiles[3][1].num_fish = 5

        # test optimal strategy
        red = BoardPlayer("red")
        black = BoardPlayer("black")
        state = State([red, black], deepcopy(board))
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 1), "red")
        state.place_avatar((1, 0), "black")
        self.assertEqual(((1, 1), (2, 1)), self.red.make_move(state))

        """
         _____       _____
        / 0,0 \_____/ 0,1 \_____
        \_____/ 1,0 \__2__/ 1,1 \
        / 2,0 \__R__/ 2,1 \_____/
        \_____/ 3,0 \_____/ 3,1 \
              \_____/     \_____/
        """
        board = Board(4, 2, uniform=True, uniform_num_fish=1)
        board.tiles[0][1].num_fish = 2

        # test optimal strategy
        for i in range(1, 3):
            red = BoardPlayer("red")
            state = State([red], deepcopy(board))
            state.place_avatar((1, 0), "red")
            self.assertEqual(((1, 0), (0, 1)), self.red.make_move(state))


    # def test_outcome_informing(self):
    #     """Test the you_have_won and you_have_lost functions."""
    #     self.red.you_have_won()
    #     self.black.you_have_lost()


if __name__ == '__main__':
    unittest.main()

