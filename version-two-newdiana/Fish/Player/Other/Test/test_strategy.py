from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State
from Fish.Player.strategy import Strategy

from copy import deepcopy
import unittest

class TestStrategy(unittest.TestCase):
    """Test the Strategy class."""

    def test_make_placement(self):
        """Test the make_placement function."""

        board = Board(3, 2, [(1, 1)])
        state = State([BoardPlayer("black"), BoardPlayer("red")], board)

        strat = Strategy()

        players = state.get_players()
        black = players[0]
        red = players[1]

        self.assertEqual([], black.get_penguins())
        self.assertEqual([], red.get_penguins())

        self.assertEqual((0, 0), strat.make_placement(state))
        state.place_avatar((0, 0), "black")

        self.assertEqual((0, 1), strat.make_placement(state))
        state.place_avatar((0, 1), "red")

        self.assertEqual((1, 0), strat.make_placement(state))
        state.place_avatar((1, 0), "black")

        # should skip hole
        self.assertEqual((2, 0), strat.make_placement(state))
        state.place_avatar((2, 0), "red")

        self.assertEqual((2, 1), strat.make_placement(state))
        state.place_avatar((2, 1), "black")

        # no more avatars can be placed
        self.assertEqual(None, strat.make_placement(state))


    def test_make_move(self):
        """Test the make_move() function."""

        strat = Strategy()

        """
         _____       _____
        / 0,0 \_____/ 0,1 \_____
        \__R__/ 1,0 \__B__/ 1,1 \
        / 2,0 \__0__/ 2,1 \__0__/
        \__0__/ 3,0 \__0__/ 3,1 \
              \__0__/     \__0__/
        """
        board = Board(1, 2, uniform=True, uniform_num_fish=1)

        # test that nothing happens when no move can be made
        for i in range(1, 10):
            red = BoardPlayer("red")
            black = BoardPlayer("black")
            state = State([red, black], deepcopy(board))
            state.place_avatar((0, 0), "red")
            state.place_avatar((0, 1), "black")
            self.assertEqual(None, strat.make_move(state, i))

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
        for i in range(1, 10):
            red = BoardPlayer("red")
            black = BoardPlayer("black")
            state = State([red, black], deepcopy(board))
            state.place_avatar((0, 0), "red")
            state.place_avatar((0, 1), "black")
            if i == 1:
                self.assertEqual(((0, 0), (1, 0)), strat.make_move(state, i))
            else:
                self.assertEqual(((0, 0), (2, 0)), strat.make_move(state, i))


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
        for i in range(1, 10):
            red = BoardPlayer("red")
            black = BoardPlayer("black")
            state = State([red, black], deepcopy(board))
            state.place_avatar((0, 0), "red")
            state.place_avatar((0, 1), "black")
            state.place_avatar((1, 1), "red")
            state.place_avatar((1, 0), "black")
            self.assertEqual(((0, 0), (2, 0)), strat.make_move(state, i))

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
        for i in range(1, 10):
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
            self.assertEqual(((0, 0), (2, 0)), strat.make_move(state, i))

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
        for i in range(1, 10):
            red = BoardPlayer("red")
            black = BoardPlayer("black")
            state = State([red, black], deepcopy(board))
            state.place_avatar((0, 0), "red")
            state.place_avatar((0, 1), "black")
            state.place_avatar((1, 1), "red")
            state.place_avatar((1, 0), "black")
            if i == 1:
                self.assertEqual(((0, 0), (2, 0)), strat.make_move(state, i))
            elif i == 2:
                self.assertEqual(((1, 1), (2, 1)), strat.make_move(state, i))
            else:
                self.assertEqual(((0, 0), (2, 0)), strat.make_move(state, i))

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
        for i in range(1, 10):
            red = BoardPlayer("red")
            black = BoardPlayer("black")
            state = State([red, black], deepcopy(board))
            state.place_avatar((0, 0), "red")
            state.place_avatar((0, 1), "black")
            state.place_avatar((1, 1), "red")
            state.place_avatar((1, 0), "black")
            if i == 1:
                self.assertEqual(((0, 0), (2, 0)), strat.make_move(state, i))
            else:
                self.assertEqual(((1, 1), (2, 1)), strat.make_move(state, i))

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
            if i == 1:
                self.assertEqual(((1, 0), (0, 0)), strat.make_move(state, i))
            else:
                self.assertEqual(((1, 0), (0, 1)), strat.make_move(state, i))

        # test exception
        board = Board(4, 2, uniform=True, uniform_num_fish=1)
        board.tiles[0][1].num_fish = 2
        red = BoardPlayer("red")
        state = State([red], deepcopy(board))
        state.place_avatar((1, 0), "red")
        try:
            strat.make_move(state, 0)
            self.assertTrue(False)
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main()

