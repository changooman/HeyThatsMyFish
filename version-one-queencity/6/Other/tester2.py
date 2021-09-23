import unittest
from state import *
from fish import *



# This test class serves to test the creating a state for a certain number of players.
class Testing_CreatingState(unittest.TestCase):
    # Tests if two players used in a GameState creates a GameState with two players.
    def test_creatingstate(self):
        player1 = Player('brown', 3)
        player2 = Player('black', 4)
        players = [player1, player2]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        start = GameState(queue)
        self.assertEqual(start.game_over, False)
        self.assertEqual(len(start.players), 2)

    # Tests if one players used in a GameState creates a GameState with one player.
    def test_creatingstate2(self):
        player2 = Player('black', 4)
        players = [player2]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        start = GameState(queue)
        self.assertEqual(start.game_over, False)
        self.assertEqual(len(start.players), 1)

# This test class serves to test the sub function for modify_index.
class Testing_ModifyIndex(unittest.TestCase):
    def test_modifyindex(self):
        player1 = Player('brown', 3)
        player2 = Player('black', 4)
        players = [player1, player2]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        hex_board = fish.HexBoard(30, 9, 2, [])
        game = create_state(players)
        self.assertEqual(game.modify_index(13, hex_board), 13)
        hex_board.dooneevent()
        hex_board.destroy()


    def test_modifyindex2(self):
        player1 = Player('brown', 3)
        players = [player1]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        hex_board = fish.HexBoard(30, 3, 3, [])
        game = create_state(players)
        self.assertEqual(game.modify_index(13, hex_board), 4)
        hex_board.dooneevent()
        hex_board.destroy()

# This test class serves to test the sub function for modify_index.
class Testing_RenderState(unittest.TestCase):
    def test_renderstate(self):
        player1 = Player('brown', 3)
        player2 = Player('black', 4)
        players = [player1, player2]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        hex_board = fish.HexBoard(30, 9, 2, [])
        game = create_state(players)
        # render_state(hex_board)
        self.assertEqual(len(game.photocache), 0)
        hex_board.dooneevent()
        hex_board.destroy()


# This test class serves to test the placing of an avatar on behalf of a player.
class Testing_PlaceAvatar(unittest.TestCase):
    # Tests if a player's six avatar's are placed.
    def test_placeavatar(self):
        player1 = Player('brown', 3)
        players = [player1]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        start = GameState(queue)
        hex_board = HexBoard(30, 4, 3, [])
        start.place_penguin(hex_board, player1)
        count = 0
        for hex in hex_board.hexagons:
            if hex.spottaken:
                if hex.penguincolor == player1.color:
                    count += 1
        self.assertEqual(count, 1)
        hex_board.dooneevent()
        hex_board.destroy()


# This test class serves to test the placing of an avatar on behalf of a player.
class Testing_MoveAvatar(unittest.TestCase):
    # Tests if function throws an exception if trying to move a piece that doesn't exist.
    def test_moveavatar(self):
        player2 = Player('black', 4)
        players = [player2]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        hex_board = HexBoard(30, 4, 3,  [])
        hexagon = hex_board.hexagons[0]
        hexagon.spottaken = True
        hexagon.penguincolor = "black"
        start = GameState(queue)
        with self.assertRaises(IndexError):
            start.move_penguin(2, 3, hex_board, queue[0])
        hex_board.dooneevent()
        hex_board.destroy()

    # Tests if function successfully moves an avatar.
    def test_moveavatar2(self):
        player2 = Player('black', 4)
        players = [player2]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        hex_board = HexBoard(30, 4, 3,  [])
        hexagon = hex_board.hexagons[0]
        hexagon.spottaken = True
        hexagon.penguincolor = "black"
        start = GameState(queue)
        start.move_penguin(1, 2, hex_board, queue[0])
        hex_board.dooneevent()
        hex_board.destroy()

    # Tests if function throws an exception when trying to move an avatar that doesn't belong to the player.
    def test_moveavatar3(self):
        player2 = Player('black', 4)
        players = [player2]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        hex_board = HexBoard(30, 4, 3,  [])
        hexagon = hex_board.hexagons[0]
        hexagon.spottaken = True
        hexagon.penguincolor = "brown"
        start = GameState(queue)
        with self.assertRaises(IndexError):
            start.move_penguin(1, 2, hex_board, queue[0])
        hex_board.dooneevent()
        hex_board.destroy()


# This test class serves to test whether any player can move an avatar.
class Testing_GameOver(unittest.TestCase):
    # Tests if function correctly returns False about it being game over if the game still has moves left.
    def test_gameover(self):
        player2 = Player('black', 4)
        players = [player2]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        hex_board = HexBoard(30, 4, 3,  [])
        hexagon = hex_board.hexagons[0]
        hexagon.spottaken = True
        hexagon.penguincolor = "black"
        start = GameState(queue)
        self.assertEqual(start.is_over(hex_board), False)
        hex_board.dooneevent()
        hex_board.destroy()

    # Tests if function correctly returns True about it being game over if there's no moves left to make.
    def test_gameover2(self):
        player1 = Player('brown', 3)
        player2 = Player('black', 4)
        players = [player1, player2]
        queue = sorted(players, key=lambda x: x.age, reverse=False)
        start = GameState(queue)
        hex_board = HexBoard(30, 4, 3, [])
        start = GameState(queue)
        self.assertEqual(start.is_over(hex_board), True)
        hex_board.dooneevent()
        hex_board.destroy()


# This runs the test executor above
if __name__ == "__main__":
    unittest.main()
