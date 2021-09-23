from collections import Counter

from Fish.Common.board import Board

import unittest

class TestBoard(unittest.TestCase):
    """Test the Board class."""

    def test_valid_coords(self):
        b = Board(3, 2)
        # name mangling required to run private methods
        self.assertTrue(b._Board__valid_coords((0, 0)))
        self.assertTrue(b._Board__valid_coords((2, 1)))
        self.assertFalse(b._Board__valid_coords((-1, 1)))
        self.assertFalse(b._Board__valid_coords((3, 1)))
        self.assertFalse(b._Board__valid_coords((2, 2)))


    def test_remove_tile(self):
        b = Board(4, 3)
        # pre removal
        self.assertEqual(
            Counter(b.get_reachable((2, 1), [])),
            Counter([(1, 0), (0, 0), (0, 1), (1, 1), (0, 2), (3, 1), (3, 0)])
        )

        b.remove_tile((1, 1))

        # post removal
        self.assertEqual(
            Counter(b.get_reachable((2, 1), [])),
            Counter([(1, 0), (0, 0), (0, 1), (3, 1), (3, 0)])
        )

        # make sure double removal is safe
        b.remove_tile((1, 1))

        # try removing invalid tile
        b.remove_tile((-1, 1))


    def test_get_tile(self):
        b = Board(4, 3, holes=[(2, 2)])

        self.assertIsNone(b.get_tile((2, 2)))

        self.assertIsNotNone(b.get_tile((1, 1)))

        self.assertIsNotNone(b.get_tile((3, 2)))

        self.assertIsNone(b.get_tile((3, 3)))

        self.assertIsNone(b.get_tile((4, 3)))

        self.assertIsNone(b.get_tile((2, -2)))

        self.assertIsNone(b.get_tile((-1, 0)))

    def test_get_holes_in_board(self):
        # test the number of holes in each board
        self.assertEqual(Board(4, 3).get_holes_in_board(), 0)
        self.assertEqual(Board(4, 3, holes=[(0, 0)]).get_holes_in_board(), 1)

    def test_get_reachable(self):
        # test with no holes
        b = Board(4, 3)
        self.assertEqual(
            Counter(b.get_reachable((1, 0), [])),
            Counter([(0, 0), (2, 0), (0, 1), (2, 1), (3, 1), (3, 0)])
        )
        self.assertEqual(
            Counter(b.get_reachable((2, 1), [])),
            Counter([(1, 0), (0, 0), (0, 1), (1, 1), (0, 2), (3, 1), (3, 0)])
        )

        # test with holes
        b = Board(4, 3, [(0, 0), (1, 1)])
        # test getting reachable of a hole spot
        self.assertEqual(
            Counter(b.get_reachable((1, 1), [])),
            Counter([])
        )
        self.assertEqual(
            Counter(b.get_reachable((1, 0), [])),
            Counter([(2, 0), (0, 1), (2, 1), (3, 1), (3, 0)])
        )
        self.assertEqual(
            Counter(b.get_reachable((2, 1), [])),
            Counter([(1, 0), (0, 1), (3, 1), (3, 0)])
        )

        # test with penguins
        b = Board(4, 3)
        self.assertEqual(
            Counter(b.get_reachable((1, 0), [(0, 0), (3, 1)])),
            Counter([(2, 0), (0, 1), (2, 1), (3, 0)])
        )


    def test_constructor(self):
        # row col values
        try:
            b = Board(0, 3)
            self.assertTrue(False)
        except ValueError:
            pass

        try:
            b = Board(3, 0)
            self.assertTrue(False)
        except ValueError:
            pass

        # board size
        b = Board(2, 3)
        self.assertEqual(len(b.tiles), 2)
        self.assertEqual(len(b.tiles[0]), 3)

        # holes
        holes = [(0, 0), (3, 3), (2, 1), (1, 2), (-1, -5), (-3, 4)]
        b = Board(4, 4, holes)
        for r in range(4):
            for c in range(4):
                if (r, c) in holes:
                    self.assertIsNone(b.tiles[r][c])
                else:
                    self.assertIsNotNone(b.tiles[r][c])

        # minimum number of one-fish tiles
        b = Board(3, 5, min_one_fish=3*5)
        for r in range(3):
            for c in range(5):
                self.assertEqual(b.tiles[r][c].get_num_fish(), 1)

        # uniform
        b = Board(4, 4, holes, uniform=True, uniform_num_fish=3)
        for r in range(4):
            for c in range(4):
                self.assertEqual(b.tiles[r][c].get_num_fish(), 3)

        # argument stability
        b = Board(3, 4, min_one_fish=-1)

        # invalid uniform number of fish
        try:
            b = Board(4, 4, uniform=True, uniform_num_fish=-1)
            self.assertTrue(False)
        except ValueError:
            pass

if __name__ == '__main__':
    unittest.main()
