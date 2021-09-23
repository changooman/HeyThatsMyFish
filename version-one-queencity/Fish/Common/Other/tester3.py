import unittest
import state
import xboard
from game_tree import *


# This test class serves to test the next_state function that either will return a state instance that will follow
# the given state if a certain action is completed, or an error saying that the given action is invalid
class Testing_Next_State(unittest.TestCase):
    #Tests if a penguin can be moved to a valid spot
    def test_next_state(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        game = Game(statetemp.hexboard, player1)
        move = game.get_next_state(statetemp, ('Move', 1, 4))
        self.assertEqual(move.hexboard.hexagons[3].spottaken, True)


    # Tests if a penguin can be moved to spot that is not reachable from it.
    def test_next_state2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        game = Game(statetemp.hexboard, player1)
        with self.assertRaises(IndexError):
            game.get_next_state(statetemp, ('Move', 1, 3))

    # Tests if a penguin can be moved to spot that is a sunken tile.
    def test_next_state3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [[1, 3]])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        game = Game(statetemp.hexboard, player1)
        with self.assertRaises(IndexError):
            game.get_next_state(statetemp, ('Move', 1, 3))

    # Tests if a penguin can be moved to spot that does not exist on the board
    def test_next_state4(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 1, 1, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        game = Game(statetemp.hexboard, player1)
        with self.assertRaises(IndexError):
            game.get_next_state(statetemp, ('Move', 1, 4))


    # Tests if a penguin can be moved to spot that has another penguin
    def test_next_state5(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 1, 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
            if hex.xy == [0, 1]:
                hex.spottaken = True
                player2.penguins.append([0, 1])
        game = Game(statetemp.hexboard, player1)
        with self.assertRaises(IndexError):
            game.get_next_state(statetemp, ('Move', 1, 2))

# This test class serves to test the third bullet point in project milestone four.
class Testing_Map_States(unittest.TestCase):
    # Tests if running isover on a state with no moves left returns true
    def test_map_state(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 1, 2, [])
        statetemp = state.create_state(players, hex_board)
        statetemp.place_penguin(hex_board, player1)
        # state.render_state(hex_board)
        game = Game(statetemp.hexboard, player1)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        thing = game.map_states(statetemp, statetemp.is_over)
        self.assertEqual(thing[0], True)

    # Tests if running isover on a state with moves left returns correct amount of falses
    def test_map_state2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        game = Game(statetemp.hexboard, player1)
        thing = game.map_states(statetemp, statetemp.is_over)
        falsecount = 0
        for isover in thing:
            if not isover:
                falsecount += 1
        self.assertEqual(falsecount, 4)

    # Tests if running isover on a board with only one tile returns an empty list
    def test_map_state3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 1, 1, [])
        for hex in hex_board.hexagons:
            if hex.xy == [1,0]:
                hex.spottaken = True
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player1)
        thing = game.map_states(statetemp, statetemp.is_over)
        self.assertEqual(len(thing), 0)

# This test class serves to test the first bullet point, which asks for a complete game tree.
class Testing_Game_Tree(unittest.TestCase):
    # Tests if making a complete tree of five layers on a four by three board with one penguin returns five states
    def test_game_tree(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [1, 0]:
                hex.spottaken = True
                player1.penguins.append([1, 0])
        # state.render_state(hex_board)
        game = Game(statetemp.hexboard, player1)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        thing = game.game_tree(statetemp, 1)
        self.assertEqual(len(thing), 5)

    # Tests if making a complete tree of three layers on a four by three board with one penguin returns seventy
    # two states
    def test_game_tree2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        game = Game(statetemp.hexboard, player1)
        thing = game.game_tree(statetemp, 3)
        self.assertEqual(len(thing), 72)

    # Tests if making a complete tree of one layer on a four by three board with no penguin returns one state
    def test_game_tree3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player1)
        thing = game.game_tree(statetemp, 1)
        self.assertEqual(len(thing), 1)

    # Tests if making a complete tree of three layers on a one by two board with no penguin returns one state
    def test_game_tree4(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 1, 2, [])
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player1)
        for hex in hex_board.hexagons:
            hex.spottaken = True
            player1.penguins.append(hex.xy)
        thing = game.game_tree(statetemp, 3)
        self.assertEqual(len(thing), 1)


# This test class serves to test the possible moves helper function
class Testing_Possible_Moves(unittest.TestCase):
    # Tests how many moves on a tile with a penguin
    def test_possible_move(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [1, 0]:
                hex.spottaken = True
                player1.penguins.append([1, 0])
        game = Game(statetemp.hexboard, player1)
        posmoves = game.possible_moves([1,0], statetemp, player1)
        self.assertEqual(len(posmoves), 4)

    # Tests how many moves a tile with no penguin has
    def test_possible_move2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [1, 0]:
                hex.spottaken = True
                player1.penguins.append([1, 0])
        game = Game(statetemp.hexboard, player1)
        posmoves = game.possible_moves([0, 0], statetemp, player1)
        self.assertEqual(len(posmoves), 0)

    # Tests how many moves a one tile board with one penguin has
    def test_possible_move3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 1, 1, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [1, 0]:
                hex.spottaken = True
                player1.penguins.append([1, 0])
        game = Game(statetemp.hexboard, player1)
        posmoves = game.possible_moves([1, 0], statetemp, player1)
        self.assertEqual(len(posmoves), 0)

    # Tests how many moves a two tile board with one tile having a penguin and the other being sunk has
    def test_possible_move4(self):
            player1 = state.Player('red', 3)
            player2 = state.Player('black', 4)
            players = [player1, player2]
            hex_board = xboard.HexBoard(30, 1, 2, [])
            statetemp = state.create_state(players, hex_board)
            for hex in hex_board.hexagons:
                if hex.xy == [1, 0]:
                    hex.spottaken = True
                    player1.penguins.append([1, 0])
                if hex.xy == [1, 1]:
                    hex.sunk = True
            game = Game(statetemp.hexboard, player1)
            posmoves = game.possible_moves([1, 0], statetemp, player1)
            self.assertEqual(len(posmoves), 0)

# This test class serves to test the find_player helper function.
class Testing_Find_Player(unittest.TestCase):
    # Tests if it finds the player that exists
    def test_find_player(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player1)
        play = game.tree_findplayer(statetemp)
        self.assertEqual(play.color, 'red')

    # Tests if it cannot find a player that doesn't exist
    def test_find_player2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('green', 9)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player3)
        play = game.tree_findplayer(statetemp)
        self.assertEqual(play, None)


# This test class serves to test the find penguins helper function
class Testing_Find_Penguins(unittest.TestCase):
    # Tests if it finds four penguins for a player with four penguins
    def test_find_penguins(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        count = 4
        for hex in hex_board.hexagons:
            hex.spottaken = True
            player1.penguins.append(hex.xy)
            count += -1
            if count == 0:
                break
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player1)
        penguins = game.tree_findpenguins(statetemp)
        self.assertEqual(len(penguins), 4)

    # Tests if it finds zero penguins for no penguins on the board
    def test_find_penguins2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player1)
        penguins = game.tree_findpenguins(statetemp)
        self.assertEqual(len(penguins), 0)

    # Tests if it finds no penguins for player with no penguins
    def test_find_penguins3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        count = 4
        for hex in hex_board.hexagons:
            hex.spottaken = True
            player2.penguins.append(hex.xy)
            count += -1
            if count == 0:
                break
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player1)
        penguins = game.tree_findpenguins(statetemp)
        self.assertEqual(len(penguins), 0)

# This test class serves to test the the tree states function.
class Testing_Tree_States(unittest.TestCase):
    # Tests if a player with one penguin has four possible states from tree states in a hole free four by three board
    def test_tree_states(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == [1, 0]:
                hex.spottaken = True
                player1.penguins.append([1, 0])
        game = Game(statetemp.hexboard, player1)
        thing = game.tree_states(statetemp)
        self.assertEqual(len(thing), 4)

    # Tests if a player with no penguins has zero possible states
    def test_tree_states2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player1)
        thing = game.tree_states(statetemp)
        self.assertEqual(len(thing), 0)

    # Tests if a player with no penguins has zero possible states in a board with only one tile
    def test_tree_states3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 1, 1, [])
        statetemp = state.create_state(players, hex_board)
        game = Game(statetemp.hexboard, player1)
        thing = game.tree_states(statetemp)
        self.assertEqual(len(thing), 0)

    #Tests if a player with no penguins has zero possible states in a board with all sunken tiles
    def test_tree_states4(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = xboard.HexBoard(30, 4, 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.sunk = True
        game = Game(statetemp.hexboard, player1)
        thing = game.tree_states(statetemp)
        self.assertEqual(len(thing), 0)

    # Tests if a player with one penguin in a board with two holes has two possible states.
    def test_tree_states5(self):
            player1 = state.Player('red', 3)
            player2 = state.Player('black', 4)
            players = [player1, player2]
            hex_board = xboard.HexBoard(30, 2, 2, [[1,1], [1,2]])
            statetemp = state.create_state(players, hex_board)
            for hex in hex_board.hexagons:
                if hex.xy == [1, 0]:
                    hex.spottaken = True
                    player1.penguins.append([1, 0])
            game = Game(statetemp.hexboard, player1)
            thing = game.tree_states(statetemp)
            self.assertEqual(len(thing), 2)



# This runs the test executor above
if __name__ == "__main__":
    unittest.main()
