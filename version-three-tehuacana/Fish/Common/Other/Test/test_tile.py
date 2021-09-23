from Fish.Common.tile import Tile

import unittest

class TestTile(unittest.TestCase):
    """Test the Tile class."""

    def test_tile(self):
        t = Tile(False, 1)
        self.assertEqual(t.get_num_fish(), 1)

        t = Tile(False, int(Tile.MAX_FISH / 2))
        self.assertEqual(t.get_num_fish(), int(Tile.MAX_FISH / 2))

        t = Tile(False, Tile.MAX_FISH)
        self.assertEqual(t.get_num_fish(), Tile.MAX_FISH)

        try:
            t = Tile(False, 0)
            self.assertTrue(False)
        except ValueError:
            pass

        try:
            t = Tile(False, -1)
            self.assertTrue(False)
        except ValueError:
            pass

        try:
            t = Tile(False, Tile.MAX_FISH + 1)
            self.assertTrue(False)
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main()
