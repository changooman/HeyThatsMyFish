from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State
from Fish.Player.strategy import Strategy

from copy import deepcopy
import unittest
import time

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

    def test_looking_ahead(self):

        strat = Strategy()

        # use a depth of 2
        board = Board(4, 4, uniform=True, uniform_num_fish=1)
        board.tiles[1][1] = None
        board.tiles[3][2] = None
        board.tiles[2][2].num_fish = 5
        board.tiles[1][2].num_fish = 2

        red = BoardPlayer("red")
        white = BoardPlayer("white")
        state = State([red, white], deepcopy(board))

        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 3), "white")
        state.place_avatar((2, 0), "red")
        state.place_avatar((1, 3), "white")
        state.place_avatar((3, 0), "red")
        state.place_avatar((2, 3), "white")
        state.place_avatar((3, 1), "red")
        state.place_avatar((3, 3), "white")

        move = strat.make_move(state, 2)
        self.assertEqual(move, ((3, 1), (2, 2)))

        # use a depth of 3
        board = Board(4, 4, uniform=True, uniform_num_fish=1)
        board.tiles[1][1] = None
        board.tiles[3][2] = None
        board.tiles[2][2].num_fish = 5
        board.tiles[1][2].num_fish = 2

        red = BoardPlayer("red")
        white = BoardPlayer("white")
        state = State([red, white], deepcopy(board))

        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 3), "white")
        state.place_avatar((2, 0), "red")
        state.place_avatar((1, 3), "white")
        state.place_avatar((3, 0), "red")
        state.place_avatar((2, 3), "white")
        state.place_avatar((3, 1), "red")
        state.place_avatar((3, 3), "white")

        move = strat.make_move(state, 3)
        self.assertEqual(move, ((3, 1), (1, 2)))

    def test_tiebreaker(self):

        strat = Strategy()
        moves = [
            ((0, 0), (1, 0)),
            ((1, 0), (0, 0))
        ]
        self.assertEqual(moves[0], strat._Strategy__break_tie(moves))

        moves = [
            ((0, 1), (1, 1)),
            ((1, 0), (0, 0))
        ]
        self.assertEqual(moves[0], strat._Strategy__break_tie(moves))

        moves = [
            ((1, 1), (1, 0)),
            ((1, 1), (1, 1))
        ]
        self.assertEqual(moves[0], strat._Strategy__break_tie(moves))

        moves = [
            ((1, 1), (0, 1)),
            ((1, 1), (1, 0))
        ]
        self.assertEqual(moves[0], strat._Strategy__break_tie(moves))

    def test_three_by_five_expensive_make_move(self):

        strat = Strategy()
        
        # 3x5 hard test
        """
         _____       _____       ____      ____      ____
        / 0,0 \_____/ 0,1 \_____/ 0,2\____/ 0,3\____/ 0,4\____
        \__R__/ 1,0 \__W__/ 1,1 \__R_/1,2 \_W__/1,3 \__R_/1,4 \
        / 2,0 \__W__/ 2,1 \__R__/2,2 \_W__/ 2,3\_3__/2,4 \_3__/
        \_3___/     \__3__/     \__3_/    \_3__/    \_3__/
              
        """
        board = Board(3, 5, uniform=True, uniform_num_fish=3)

        red = BoardPlayer("red")
        white = BoardPlayer("white")
        state = State([red, white], deepcopy(board))
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "white")
        state.place_avatar((0, 2), "red")
        state.place_avatar((0, 3), "white")
        state.place_avatar((0, 4), "red")
        state.place_avatar((1, 0), "white")
        state.place_avatar((1, 1), "red")
        state.place_avatar((1, 2), "white")

        move = strat.make_move(state, 20)
        self.assertEqual(move, ((0, 0), (2, 0)))

    

        
    # def test_five_by_five_expensive_make_move(self):

    #     strat = Strategy()
    #     board = Board(5, 5, uniform=True, uniform_num_fish=2)

    #     red = BoardPlayer("red")
    #     white = BoardPlayer("white")
    #     black = BoardPlayer("black")
    #     brown = BoardPlayer("brown")

    #     state = State([red, white, black, brown], board)

    #     state.place_avatar((0, 0), "red")
    #     state.place_avatar((0, 1), "white")
    #     state.place_avatar((0, 2), "black")
    #     state.place_avatar((0, 3), "brown")
    #     state.place_avatar((0, 4), "red")
    #     state.place_avatar((1, 0), "white")
    #     state.place_avatar((1, 1), "black")
    #     state.place_avatar((1, 2), "brown")

    #     move_count = 1
    #     while not state.is_game_over():
    #         start_time = time.time()
    #         move = strat.make_move(state, 2)
    #         if move is None:
    #             state.pass_turn_if_applicable()
    #             continue
    #         end_time = time.time()
    #         print("Elaped time for move {}: {} sec".format(move_count, end_time-start_time))
    #         move_count += 1
    #         state.move_avatar(move[0], move[1])
        

if __name__ == '__main__':
    unittest.main()

