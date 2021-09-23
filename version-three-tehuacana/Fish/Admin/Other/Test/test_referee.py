from Fish.Admin.referee import Referee
from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State
from Fish.Player.player import Player

import unittest
from time import sleep

class SlowPlayer(Player):
    """A very slow Fish player."""

    def make_placement(self, state):
        sleep(10)
        return super(SlowPlayer, self).make_placement(state)


    def make_move(self, state):
        sleep(10)
        return super(SlowPlayer, self).make_move(state)


class StupidPlayer(Player):
    """A stupid Fish player."""

    def make_placement(self, state):
        return (-1, -1)


    def make_move(self, state):
        return ((-1, -1), (-1, -1))


class UnstablePlayer(Player):
    """A Fish player that throws exceptions."""

    def make_placement(self, state):
        raise Exception


    def make_move(self, state):
        raise Exception


class CountingPlayer(Player):
    """A Fish player that counts his turns."""

    def __init__(self, color):
        super(CountingPlayer, self).__init__(color)
        self.placements = 0
        self.moves = 0


    def make_placement(self, state):
        self.placements += 1
        return super(CountingPlayer, self).make_placement(state)


    def make_move(self, state):
        self.moves += 1
        return super(CountingPlayer, self).make_move(state)



class TestReferee(unittest.TestCase):
    """Test the Referee class."""

    def setUp(self):
        """Define some players for test use."""
        self.red = Player("red")
        self.black = Player("black")
        self.white = Player("white")
        self.brown = Player("brown")


    def test_constructor(self):
        """Test the Referee constructor."""
        bad_args = [
            ([], (3, 3)),  # no players
            ([self.red], (3, 3)),  # just one player
            ([self.red, self.black], (2, 2)),  # undersized board
            ([self.red, self.black, self.white, self.brown, self.red], (9, 9))  # too many players
        ]
        for args in bad_args:
            try:
                r = Referee(*args)
                self.assertTrue(False)
            except ValueError:
                pass

        good_args = [
            ([self.red, self.black],  (2, 4)),
            ([self.red, self.black, self.white, self.brown], (9, 9))
        ]
        for args in good_args:
            r = Referee(*args)


    def test_is_game_over(self):
        """Test the is_game_over function."""
        ref = Referee([self.red, self.black], (2, 4))
        self.assertFalse(ref.is_game_over())

        b = Board(4, 2)
        red, black = BoardPlayer("red"), BoardPlayer("black")
        state = State([red, black], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((2, 0), "red")
        state.place_avatar((2, 1), "black")
        state.place_avatar((3, 0), "red")
        state.place_avatar((3, 1), "black")
        ref.state = state
        self.assertTrue(ref.is_game_over())


    def test_get_scores(self):
        """Test the get_scores function."""
        ref = Referee([self.red, self.black], (2, 4))
        b = Board(5, 2)
        b.tiles[3][0].num_fish = 5
        b.tiles[3][1].num_fish = 3
        red, black = BoardPlayer("red"), BoardPlayer("black")
        state = State([red, black], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((2, 0), "red")
        state.place_avatar((2, 1), "black")
        state.place_avatar((3, 0), "red")
        state.place_avatar((3, 1), "black")
        state.move_avatar((3, 0), (4, 0))
        state.move_avatar((3, 1), (4, 1))
        ref.state = state
        self.assertEqual([(self.red, 5), (self.black, 3)], ref.get_scores())


    def test_get_victors(self):
        """Test the get_victors function."""
        ref = Referee([self.red, self.black], (2, 4))
        b = Board(5, 2)
        b.tiles[3][0].num_fish = 5
        b.tiles[3][1].num_fish = 3
        red, black = BoardPlayer("red"), BoardPlayer("black")
        state = State([red, black], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((2, 0), "red")
        state.place_avatar((2, 1), "black")
        state.place_avatar((3, 0), "red")
        state.place_avatar((3, 1), "black")
        state.move_avatar((3, 0), (4, 0))
        state.move_avatar((3, 1), (4, 1))
        ref.state = state
        self.assertEqual([self.red], ref.get_victors())

        ref = Referee([self.red, self.black], (2, 4))
        b = Board(5, 2)
        b.tiles[3][0].num_fish = 5
        b.tiles[3][1].num_fish = 5
        red, black = BoardPlayer("red"), BoardPlayer("black")
        state = State([red, black], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((2, 0), "red")
        state.place_avatar((2, 1), "black")
        state.place_avatar((3, 0), "red")
        state.place_avatar((3, 1), "black")
        state.move_avatar((3, 0), (4, 0))
        state.move_avatar((3, 1), (4, 1))
        ref.state = state
        self.assertEqual([self.red, self.black], ref.get_victors())

        ref = Referee([SlowPlayer(), UnstablePlayer()], (2, 4))
        ref.run()
        self.assertEqual([], ref.get_victors())

        unstable = UnstablePlayer()
        unstable.set_color("black")
        ref = Referee([self.red, unstable], (2, 4))
        ref.run()
        self.assertEqual([self.red], ref.get_victors())



    def test_player_order(self):
        red = CountingPlayer("red")
        black = CountingPlayer("black")
        ref = Referee([red, black], (2, 4))

        b = Board(5, 2, [(4, 1)])
        b.tiles[3][0].num_fish = 5
        b.tiles[3][1].num_fish = 3
        red_bp, black_bp = BoardPlayer("red"), BoardPlayer("black")
        state = State([red_bp, black_bp], b)
        ref.state = state
        ref.run()
        self.assertEqual(1, red.moves)
        self.assertEqual(0, black.moves)
        self.assertEqual((0, 0), red_bp.get_penguins()[0])
        self.assertEqual((0, 1), black_bp.get_penguins()[0])
        self.assertEqual((1, 0), red_bp.get_penguins()[1])
        self.assertEqual((1, 1), black_bp.get_penguins()[1])


    def test_run(self):
        """Test the run function with no violations."""
        red, black = CountingPlayer("red"), CountingPlayer("black")
        ref = Referee([red, black], (2, 4))
        ref.state = State([BoardPlayer("red"), BoardPlayer("black")],
                          Board(4, 4, uniform=True, uniform_num_fish=1))
        self.assertFalse(ref.is_game_over())
        ref.run()
        self.assertEqual((4, 4, 4, 4), (red.placements, red.moves, black.placements, black.moves))
        self.assertEqual([(red, 4), (black, 4)], ref.get_scores())
        self.assertTrue(ref.is_game_over())
        self.assertEqual([], ref.get_violators())

    def test_run_custom_board(self):
        """Test the run function with no violations."""
        red, black = CountingPlayer("red"), CountingPlayer("black")
        ref = Referee([red, black], (2, 4), board=Board(4, 4, uniform=True, uniform_num_fish=1))
        self.assertFalse(ref.is_game_over())
        ref.run()
        self.assertEqual((4, 4, 4, 4), (red.placements, red.moves, black.placements, black.moves))
        self.assertEqual([(red, 4), (black, 4)], ref.get_scores())
        self.assertTrue(ref.is_game_over())
        self.assertEqual([], ref.get_violators())

    def test_board_too_small(self):
        "Test if the board raises an exception of board size isnt big enough for players"
        red, black, white = CountingPlayer("red"), CountingPlayer("black"), CountingPlayer("white")
        # if these do not throw a value error, fail the test
        try:
            Referee([red, black], (1, 1), board=Board(1, 1, uniform=True, uniform_num_fish=1))
            self.assertTrue(False)
        except ValueError:
            pass

        try:
            Referee([red, black, white], (1, 1), board=Board(2, 4, uniform=True, uniform_num_fish=1))
            self.assertTrue(False)
        except ValueError:
            pass

    def test_board_too_many_holes(self):
        "Test if the board raises an exception of board size isnt big enough for players"
        red, black = CountingPlayer("red"), CountingPlayer("black")

        try:
            Referee([red, black], (1, 1), board=Board(2, 4, holes=[(0,0)]))
            self.assertTrue(False)
        except ValueError:
            pass

    def test_run_turn(self):
        """Test that running individual turns works when there are no violations."""

        red, black = CountingPlayer("red"), CountingPlayer("black")
        ref = Referee([red, black], (2, 4))
        ref.state = State([BoardPlayer("red"), BoardPlayer("black")],
                          Board(4, 4, uniform=True, uniform_num_fish=1))
        self.assertFalse(ref.is_game_over())
        while True:
            if ref.is_game_over():
                break
            ref.run_turn()
        self.assertEqual((4, 4, 4, 4), (red.placements, red.moves, black.placements, black.moves))
        self.assertEqual([(red, 4), (black, 4)], ref.get_scores())
        self.assertTrue(ref.is_game_over())
        self.assertEqual([], ref.get_violators())


    def test_timeout(self):
        """Test when a Player times out."""
        red, black =  SlowPlayer("red"), SlowPlayer("black")
        ref = Referee([red, black], (2, 4), timeout=0.5)
        ref.run()
        self.assertEqual([], ref.get_scores())
        self.assertEqual([red, black], ref.get_violators())

        ref = Referee([self.red, black], (2, 4), timeout=0.5)
        b = Board(5, 2)
        b.tiles[3][0].num_fish = 5
        b.tiles[4][0].num_fish = 5
        red_bp, black_bp = BoardPlayer("red"), BoardPlayer("black")
        state = State([red_bp, black_bp], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((2, 0), "red")
        state.place_avatar((2, 1), "black")
        state.place_avatar((3, 0), "red")
        state.place_avatar((3, 1), "black")
        state.move_avatar((3, 0), (4, 0))
        ref.state = state
        ref.run()
        self.assertEqual([black], ref.get_violators())


    def test_exceptions(self):
        """Test when a Player throws exceptions."""
        red, black =  UnstablePlayer("red"), UnstablePlayer("black")
        ref = Referee([red, black], (2, 4))
        ref.run()
        self.assertEqual([], ref.get_scores())
        self.assertEqual([red, black], ref.get_violators())

        ref = Referee([self.red, black], (2, 4))
        b = Board(5, 2)
        b.tiles[3][0].num_fish = 5
        b.tiles[4][0].num_fish = 5
        red_bp, black_bp = BoardPlayer("red"), BoardPlayer("black")
        state = State([red_bp, black_bp], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((2, 0), "red")
        state.place_avatar((2, 1), "black")
        state.place_avatar((3, 0), "red")
        state.place_avatar((3, 1), "black")
        state.move_avatar((3, 0), (4, 0))
        ref.state = state
        ref.run()
        self.assertEqual([black], ref.get_violators())


    def test_invalid_moves(self):
        """Test when a Player tries to make invalid moves or placements."""
        red, black =  StupidPlayer("red"), StupidPlayer("black")
        ref = Referee([red, black], (2, 4))
        ref.run()
        self.assertEqual([], ref.get_scores())
        self.assertEqual([red, black], ref.get_violators())

        ref = Referee([self.red, black], (2, 4))
        b = Board(5, 2)
        b.tiles[3][0].num_fish = 5
        b.tiles[4][0].num_fish = 5
        red_bp, black_bp = BoardPlayer("red"), BoardPlayer("black")
        state = State([red_bp, black_bp], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((2, 0), "red")
        state.place_avatar((2, 1), "black")
        state.place_avatar((3, 0), "red")
        state.place_avatar((3, 1), "black")
        state.move_avatar((3, 0), (4, 0))
        ref.state = state
        ref.run()
        self.assertEqual([black], ref.get_violators())


    def test_color_assignment(self):
        """Test that the referee is able to assign colors to Players and run a game."""
        ref = Referee([Player(depth=1), Player(depth=1),
                       Player(depth=1), Player(depth=1)],
                      (5, 5))
        ref.run()


if __name__ == '__main__':
    unittest.main()
