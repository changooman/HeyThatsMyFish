import sys
sys.path.insert(1, '../../')

from Fish.Common.board_player import BoardPlayer

import unittest

class TestBoardPlayer(unittest.TestCase):
    """Test the BoardPlayer class."""

    def test_constructor(self):
        """Test the BoardPlayer constructor."""

        p = BoardPlayer("black")
        p = BoardPlayer("White")
        p = BoardPlayer("rEd")
        p = BoardPlayer("brown")

        try:
            p = BoardPlayer("blue")
            self.assertTrue(False)
        except:
            pass


if __name__ == '__main__':
    unittest.main()
