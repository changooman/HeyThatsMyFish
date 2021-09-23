import unittest
from fish import *


# This test class serves to test the neighbors function which returns the neighbors of a tile
# It checks to see if the function will return the correct amount of neighbors for a hexagon tile
class Testing_Neighbors(unittest.TestCase):
    def test_neighbor(self):
        hex_board = HexBoard(30, 4, 3,  [])
        self.assertEqual(len(hex_board.find_neighbors(hex_board.hexagons[0])), 3)
        hex_board.dooneevent()
        hex_board.destroy()

    def test_neighbor2(self):
        hex_board = HexBoard(30, 4, 3,  [])
        self.assertEqual(len(hex_board.find_neighbors(hex_board.hexagons[3])), 2)
        hex_board.dooneevent()
        hex_board.destroy()

    def test_neighbor3(self):
        hex_board = HexBoard(30, 4, 3,  [])
        self.assertEqual(len(hex_board.find_neighbors(hex_board.hexagons[9])), 5)
        hex_board.dooneevent()
        hex_board.destroy()

    def test_neighbor4(self):
        hex_board = HexBoard(30, 4, 3,  [])
        self.assertEqual(len(hex_board.find_neighbors(hex_board.hexagons[10])), 3)
        hex_board.dooneevent()
        hex_board.destroy()


# This test class serves to test the adjust_hexagonindex function which adjusts the index of a clicked item
# It checks to see if the function will subtract the index of the canvas item by the length of the hexagon list
# and return the correct number
class Test_AdjustHexagonIndex(unittest.TestCase):
    def test_adjustindex(self):
        hex_board = HexBoard(30, 4, 3, [])
        self.assertEqual(hex_board.adjust_hexagon_index(13), 1)
        hex_board.dooneevent()
        hex_board.destroy()

    def test_adjustindex2(self):
        hex_board = HexBoard(30, 4, 3, [])
        self.assertEqual(hex_board.adjust_hexagon_index(24), 12)
        hex_board.dooneevent()
        hex_board.destroy()

    def test_adjustindex3(self):
        hex_board = HexBoard(30, 4, 3, [])
        self.assertEqual(hex_board.adjust_hexagon_index(15), 3)
        hex_board.dooneevent()
        hex_board.destroy()

    def test_adjustindex4(self):
        hex_board = HexBoard(30, 4, 3,  [])
        self.assertEqual(hex_board.adjust_hexagon_index(17), 5)
        hex_board.dooneevent()
        hex_board.destroy()

# This test class serves to test the reset_tiles function which will reset the startingtile to the origin hexagon.
# This checks if the returned tile has the same tags as the actual tile in the hexagon list
class Test_ResetTiles(unittest.TestCase):
    def test_resetiles(self):
        hex_board = HexBoard(30, 4, 3, [])
        clicked = 1
        self.assertEqual(hex_board.reset_tiles(clicked).tags, hex_board.hexagons[int(clicked) - 1].tags)
        hex_board.dooneevent()
        hex_board.destroy()

    def test_resetiles2(self):
        hex_board = HexBoard(30, 4, 3,  [])
        clicked = 10
        self.assertEqual(hex_board.reset_tiles(clicked).tags, hex_board.hexagons[int(clicked) - 1].tags)
        hex_board.dooneevent()
        hex_board.destroy()

# This test class serves to test the setFishes function which initializes each tile's fish amount.
# It tests both modes of setting all tile(s) to the same amount of fish and the minimum tiles with
# one fish mode.
class Test_SetFishes(unittest.TestCase):
    def test_setfishes(self):
        hex_board = HexBoard(30, 4, 3,  [])
        count = 0
        mintilegoal = 1
        hex_board.set_fishes(hex_board.hexagons, hex_board.size, mintilegoal, None)
        acheivedmintiles = False
        for hex in hex_board.hexagons:
            if hex.fish == 1:
                count += 1
        if count >= 1:
            acheivedmintiles = True
        self.assertEqual(acheivedmintiles, True)
        hex_board.dooneevent()
        hex_board.destroy()

    def test_setfishes2(self):
        hex_board = HexBoard(30, 4, 3,  [])
        count = 0
        setallto = 5
        hex_board.set_fishes(hex_board.hexagons, hex_board.size, None, setallto)
        acheivedmintiles = False
        for hex in hex_board.hexagons:
            if hex.fish == setallto:
                count += 1
        self.assertEqual(count, 12)
        hex_board.dooneevent()
        hex_board.destroy()


# This test class serves to test the initialization process of the hexagon board
# This checks if each initialized attribute was properly st from the row, cols to the size of the board, etc.
class Test_HexagonBoard(unittest.TestCase):
    def test_hexagonboard(self):
        hex_board = HexBoard(30, 4, 3,  [])
        self.assertEqual(hex_board.rows, (3))
        self.assertEqual(hex_board.cols, (4))
        hex_board.dooneevent()
        hex_board.destroy()

    def test_hexagonboard2(self):
        hex_board = HexBoard(30, 4, 3,  [])
        self.assertEqual(hex_board.size, (30))
        hex_board.dooneevent()
        hex_board.destroy()

    def test_hexagonboard3(self):
        hex_board = HexBoard(30, 4, 3,  [])
        self.assertEqual(hex_board.can_color, "grey")
        self.assertEqual(hex_board.tile_color, "orange")
        hex_board.dooneevent()
        hex_board.destroy()




# This runs the test executor above
if __name__ == "__main__":
    unittest.main()
