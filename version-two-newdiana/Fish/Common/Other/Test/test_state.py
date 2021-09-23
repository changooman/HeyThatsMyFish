from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State
from Fish.Common.tile import Tile

from collections import Counter
import unittest

class TestState(unittest.TestCase):
    """Test the State class."""

    def setUp(self):
        """Define some players for test use."""
        self.red = BoardPlayer("red")
        self.black = BoardPlayer("black")
        self.white = BoardPlayer("white")
        self.brown = BoardPlayer("brown")


    def test_state(self):
        """Test the constructor."""
        b = Board(3, 2)
        state = State([self.red, self.black], b)

        # invalid players
        try:
            state = State([], b)
            self.assertTrue(False)
        except:
            pass


    def test_get_reachable(self):
        """Test the get_reachable function."""
        b = Board(5, 3, [(4, 0)])
        state = State([self.red, self.black, self.white, self.brown], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((0, 2), "white")
        state.place_avatar((1, 2), "brown")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((3, 1), "white")
        state.place_avatar((3, 0), "brown")
        self.assertEqual(
            Counter(state.get_reachable((3, 0))),
            Counter([(2, 0), (2, 1), (4, 1)])
        )

        b = Board(4, 3)
        state = State([BoardPlayer("red"), BoardPlayer("black")], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((3, 1), "black")
        self.assertEqual(
            Counter(state.get_reachable((1, 0))),
            Counter([(2, 0), (0, 1), (2, 1), (3, 0)])
        )

        b = Board(4, 3)
        state = State([BoardPlayer("red"), BoardPlayer("black")], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((1, 0), "black")
        state.place_avatar((2, 0), "red")
        self.assertEqual(
            Counter(state.get_reachable((0, 0))),
            Counter([])
        )


    def test_valid_placement(self):
        """Test the valid_placement function."""
        b = Board(4, 3, [(0, 0)])
        state = State([self.red, self.black], b)

        self.assertFalse(state.valid_placement((0, 0), "red"))  # place on hole
        self.assertFalse(state.valid_placement((-1, 0), "red")) # place out of bounds
        self.assertFalse(state.valid_placement((4, 3), "red"))  # place out of bounds

        self.assertTrue(state.valid_placement((1, 0), "red"))
        state.place_avatar((1, 0), "red")

        self.assertFalse(state.valid_placement((1, 1), "red"))      # place out of turn
        self.assertFalse(state.valid_placement((1, 0), "black"))    # place on other penguin
        self.assertFalse(state.valid_placement((1, 0), "white"))    # place invalid color

        self.assertTrue(state.valid_placement((2, 1), "black"))
        state.place_avatar((2, 1), "black")

        # check turn order again
        self.assertFalse(state.valid_placement((3, 1), "black"))
        self.assertTrue(state.valid_placement((3, 1), "red"))


    def test_whose_turn(self):
        """Test the whose_turn function."""
        b = Board(4, 3)
        state = State([self.red, self.black, self.white, self.brown], b)

        self.assertEqual(state.whose_turn(), self.red)

        # still red's turn after invalid turn attempts
        try:
            state.place_avatar((-1, 0), "red")
            self.assertFalse(True)
        except ValueError:
            pass
        self.assertEqual(state.whose_turn(), self.red)

        try:
            state.place_avatar((0, 0), "black")
            self.assertFalse(True)
        except ValueError:
            pass
        self.assertEqual(state.whose_turn(), self.red)

        # ensure turn order is correct during placement round
        state.place_avatar((0, 0), "red")
        self.assertEqual(state.whose_turn(), self.black)
        state.place_avatar((0, 1), "black")
        self.assertEqual(state.whose_turn(), self.white)
        state.place_avatar((0, 2), "white")
        self.assertEqual(state.whose_turn(), self.brown)
        state.place_avatar((1, 2), "brown")
        self.assertEqual(state.whose_turn(), self.red)
        state.place_avatar((1, 0), "red")
        self.assertEqual(state.whose_turn(), self.black)
        state.place_avatar((1, 1), "black")
        self.assertEqual(state.whose_turn(), self.white)
        state.place_avatar((3, 1), "white")
        self.assertEqual(state.whose_turn(), self.brown)
        state.place_avatar((3, 0), "brown")

        # ensure turn order is correct during movement round
        self.assertEqual(state.whose_turn(), self.red)
        state.move_avatar((0, 0), (2, 0))
        self.assertEqual(state.whose_turn(), self.black)
        state.move_avatar((0, 1), (2, 1))
        self.assertEqual(state.whose_turn(), self.white)
        state.move_avatar((0, 2), (2, 2))
        self.assertEqual(state.whose_turn(), self.brown)
        state.move_avatar((1, 2), (3, 2))
        self.assertEqual(state.whose_turn(), self.red)

        # attempt an invalid move, ensure that whose_turn is still correct
        try:
            state.move_avatar((2, 0), (3, 0))
            self.assertFalse(True)
        except ValueError:
            pass
        self.assertEqual(state.whose_turn(), self.red)


    def test_place_avatar(self):
        """Test the place_avatar function."""
        b = Board(4, 3, [(0, 0)])
        state = State([self.red, self.black], b)

        invalid_args = [
            ((0, 0), "red"),  # place on hole
            ((-1, 0), "red"), # place out of bounds
            ((4, 3), "red"),  # place out of bounds
        ]

        for args in invalid_args:
            try:
                state.place_avatar(*args)
                self.assertFalse(True)
            except ValueError:
                pass

        self.assertTrue((1, 0) not in self.red.get_penguins())
        state.place_avatar((1, 0), "red")
        self.assertTrue((1, 0) in self.red.get_penguins())

        invalid_args = [
            ((1, 1), "red"),    # place out of turn
            ((1, 0), "black"),  # place on other penguin
            ((1, 0), "white"),  # place invalid color
        ]

        for args in invalid_args:
            try:
                state.place_avatar(*args)
                self.assertFalse(True)
            except ValueError:
                pass

        self.assertTrue((2, 1) not in self.black.get_penguins())
        state.place_avatar((2, 1), "black")
        self.assertTrue((2, 1) in self.black.get_penguins())


    def test_valid_move(self):
        """Test the valid_move function."""
        b = Board(5, 3, [(4, 0)])
        state = State([self.red, self.black, self.white, self.brown], b)

        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((0, 2), "white")
        state.place_avatar((1, 2), "brown")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((3, 1), "white")

        # no valid moves before all avatars are placed
        # self.assertFalse(state.valid_move((1, 2), (3, 2)))

        state.place_avatar((3, 0), "brown")

        # check that only the player whose turn it is has valid moves
        self.assertTrue(state.valid_move((0, 0), (2, 0)))
        self.assertFalse(state.valid_move((0, 1), (2, 1)))
        self.assertFalse(state.valid_move((0, 2), (2, 2)))
        self.assertFalse(state.valid_move((1, 2), (3, 2)))

        # can't move into hole
        self.assertFalse(state.valid_move((0, 0), (4, 0)))

        state.move_avatar((0, 0), (2, 0))

        # check that only the player whose turn it is has valid moves
        self.assertFalse(state.valid_move((0, 0), (2, 0)))
        self.assertTrue(state.valid_move((0, 1), (2, 1)))
        self.assertFalse(state.valid_move((0, 2), (2, 2)))
        self.assertFalse(state.valid_move((1, 2), (3, 2)))

        # can't run off board or into other penguins
        self.assertFalse(state.valid_move((0, 1), (1, 0)))
        self.assertFalse(state.valid_move((0, 1), (0, 0)))
        self.assertFalse(state.valid_move((0, 1), (-1, 1)))


    def test_move_avatar(self):
        """Test the move_avatar function."""
        b = Board(5, 3, [(4, 0)], uniform=True, uniform_num_fish=1)
        state = State([self.red, self.black, self.white, self.brown], b)

        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((0, 2), "white")
        state.place_avatar((1, 2), "brown")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        state.place_avatar((3, 1), "white")

        # try:
            # # no valid moves before all avatars are placed
            # state.move_avatar((1, 2), (3, 2))
            # self.assertTrue(False)
        # except ValueError:
            # pass

        state.place_avatar((3, 0), "brown")

        # invalid moves
        invalid_args = [
            ((0, 1), (2, 1)),
            ((0, 2), (2, 2)),
            ((1, 2), (3, 2)),
        ]

        for args in invalid_args:
            try:
                state.move_avatar(*args)
                self.assertTrue(False)
            except ValueError:
                pass

        self.assertIsNotNone(state.board.get_tile((0, 0)))
        self.assertTrue((0, 0) in self.red.get_penguins())
        self.assertTrue((2, 0) not in self.red.get_penguins())
        self.assertEqual(self.red.get_score(), 0)

        state.move_avatar((0, 0), (2, 0))

        self.assertIsNone(state.board.get_tile((0, 0)))
        self.assertTrue((0, 0) not in self.red.get_penguins())
        self.assertTrue((2, 0) in self.red.get_penguins())
        self.assertEqual(self.red.get_score(), 1)

        # invalid moves
        invalid_args = [
            ((0, 0), (2, 0)),
            ((0, 2), (2, 2)),
            ((1, 2), (3, 2)),
            ((0, 1), (1, 0)),
            ((0, 1), (0, 0)),
            ((0, 1), (-1, 1)),
        ]

        for args in invalid_args:
            try:
                state.move_avatar(*args)
                self.assertTrue(False)
            except ValueError:
                pass

        self.assertIsNotNone(state.board.get_tile((1, 1)))
        self.assertTrue((1, 1) in self.black.get_penguins())
        self.assertTrue((2, 2) not in self.black.get_penguins())
        self.assertEqual(self.black.get_score(), 0)

        state.move_avatar((1, 1), (2, 2))

        self.assertIsNone(state.board.get_tile((1, 1)))
        self.assertTrue((1, 1) not in self.black.get_penguins())
        self.assertTrue((2, 2) in self.black.get_penguins())
        self.assertEqual(self.black.get_score(), 1)


    def test_is_game_over(self):
        """Test the is_game_over function."""
        b = Board(5, 3, [(4, 0)])
        self.red, self.black = BoardPlayer("red"), BoardPlayer("black")
        state = State([self.red, self.black, self.white, self.brown], b)
        self.assertTrue(state.is_game_over())

        b = Board(2, 2)
        self.red, self.black = BoardPlayer("red"), BoardPlayer("black")
        state = State([self.red, self.black], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")
        self.assertTrue(state.is_game_over())

        b = Board(2, 2)
        self.red, self.black = BoardPlayer("red"), BoardPlayer("black")
        state = State([self.red, self.black], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        self.assertFalse(state.is_game_over())


    def test_pass_turn_if_applicable(self):
        """Test the pass_turn_if_applicable function."""
        b = Board(5, 3, [(4, 0)])
        self.red, self.black = BoardPlayer("red"), BoardPlayer("black")
        state = State([self.red, self.black], b)

        self.assertTrue("red", state.whose_turn())
        state.place_avatar((0, 0), "red")
        self.assertTrue("black", state.whose_turn())
        state.pass_turn_if_applicable()
        self.assertTrue("red", state.whose_turn())


    def test_remove_player(self):
        """Test the remove player function."""
        b = Board(2, 2)
        self.red, self.black = BoardPlayer("red"), BoardPlayer("black")
        state = State([self.red, self.black], b)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        state.place_avatar((1, 0), "red")
        state.place_avatar((1, 1), "black")

        self.assertEqual(self.red, state.whose_turn())
        state.remove_player("red")
        self.assertEqual(self.black, state.whose_turn())
        self.assertTrue(self.red not in state.get_players())


if __name__ == '__main__':
    unittest.main()
