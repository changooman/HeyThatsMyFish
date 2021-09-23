import unittest
from state import *
from board import *
from strategy import *
from game_tree import *
from referee import *
from player import *


# This test class serves to test the referee function that will return a list of player instances
class TestReferee(unittest.TestCase):
    # tests a board with 3 players and 4 tiles and one penguin each
    def test_referee(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 1
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        self.assertEqual(ref.referee("ZigZag", 1), [player1, player2, player3])

    # tests a game with 2 players, 12 tiles, and 6 penguins each, there should be no moves available and thus a tie
    def test_referee1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 3
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        self.assertEqual(ref.referee("Zigzag", 6), [player1, player2])

    # tests a game with one player
    def test_referee2(self):
        player1 = state.Player('red', 3)
        players = [player1]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 1
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        self.assertEqual(ref.referee("ZigZag", 1), [player1])

    # runs a test with 2 players
    def test_referee3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 1
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        self.assertEqual(ref.referee("ZigZag", 1), [player1, player2])

# This test class serves to test the get_winners function that will return a list of player instances
class TestGetWinners(unittest.TestCase):
    # tests a game with 2 players, 12 tiles, and 6 penguins each, there should be no moves available and thus a tie
    def test_get_winners(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        interface.place_ordered_penguins(statetemp, player1, 6)
        interface.place_ordered_penguins(statetemp, player2, 6)
        # state.render_state(hex_board)
        layers = 3
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        self.assertEqual(ref.get_winners(), [player1, player2])

    # tests a case where player1 is the winner
    def test_get_winners1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 5
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # state.render_state(hex_board)
        layers = 3
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        playr.initial_moves("Zigzag", 3, player1)
        playr.take_turn(player1, 2)
        self.assertEqual(ref.get_winners(), [player1])

    # tests a 4x3 board with one player that has 2 penguins
    def test_get_winners2(self):
        player1 = state.Player('red', 3)
        players = [player1]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        interface.place_ordered_penguins(statetemp, player1, 2)
        # state.render_state(hex_board)
        layers = 3
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        self.assertEqual(ref.get_winners(), [player1])

    # tests a case where player2 is the winner
    def test_get_winners3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        interface.place_ordered_penguins(statetemp, player1, 2)
        # state.render_state(hex_board)
        layers = 3
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        playr.initial_moves("Zigzag", 3, player2)
        playr.take_turn(player2, 2)
        self.assertEqual(ref.get_winners(), [player2])

# This test class serves to test the inital_moves function that will return a list of player instances
class TestInitialMoves(unittest.TestCase):
    # tests a board with 3 players and 4 tiles and one penguin each, tests the random style
    def test_inital_moves(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        playr.initial_moves("Random", 1, player1)
        self.assertEqual(len(player1.penguins), 1)

    # tests the same as before but using the zigzag pattern
    def test_inital_moves1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        playr.initial_moves("Zigzag", 2, player1)
        self.assertEqual(len(player1.penguins), 2)

    # tests that it only places penguins for given player
    def test_inital_moves2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        playr.initial_moves("Zigzag", 2, player2)
        self.assertEqual(len(player1.penguins), 0)

    # tests that it can fill a board with one player's penguin
    def test_inital_moves3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        playr.initial_moves("Zigzag", 12, player1)
        self.assertEqual(len(player1.penguins), 12)

# This test class serves to test the take_turn function that will return a list of player instances
class TestTakeTurn(unittest.TestCase):
    # tests a board with 3 players and 4 tiles and one penguin each, tests one move on a board of all 1 fish tiles
    def test_take_turn(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 1
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        playr.initial_moves("Zigzag", 1, player1)
        playr.take_turn(player1, layers)
        self.assertEqual(player1.score, 1)

    # tests a board with 3 players and 4 tiles and one penguin each, tests one move on a board of all 3 fish tiles
    def test_take_turn1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 3
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        playr.initial_moves("Zigzag", 1, player1)
        playr.take_turn(player1, layers)
        self.assertEqual(player1.score, 3)

    # tests making 3 moves with one player
    def test_take_turn3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 1
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        playr.initial_moves("Zigzag", 1, player1)
        playr.take_turn(player1, layers)
        playr.take_turn(player1, layers)
        playr.take_turn(player1, layers)
        self.assertEqual(player1.score, 3)

    # tests moving two players twice each
    def test_take_turn4(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 4, 4 * 4, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 3
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        playr.initial_moves("Zigzag", 1, player1)
        playr.initial_moves("Zigzag", 1, player2)
        playr.initial_moves("Zigzag", 1, player1)
        playr.initial_moves("Zigzag", 1, player2)
        playr.take_turn(player1, layers)
        playr.take_turn(player2, layers)
        self.assertEqual(player1.score, 3)

# This test class serves to test the remove_player function that will return a list of player instances
class TestRemovePlayer(unittest.TestCase):
    # tests a board with 3 players and revomes the third player
    def test_remove_player(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 1
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        ref.remove_player(player3)
        self.assertEqual(len(statetemp.players), 2)

    # tests removing players that have moved
    def test_remove_player1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 1
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        playr.initial_moves("Random", 1, player1)
        playr.take_turn(player1, layers)
        playr.take_turn(player1, layers)
        ref.remove_player(player1)
        self.assertEqual(len(statetemp.players), 2)

    # tests a board with 3 players and removes all players
    def test_remove_player2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        player3 = state.Player('white', 4)
        players = [player1, player2, player3]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 1
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        ref.remove_player(player3)
        ref.remove_player(player2)
        ref.remove_player(player1)
        self.assertEqual(len(statetemp.players), 0)

    # tests removing the only player in a game
    def test_remove_player3(self):
        player1 = state.Player('red', 3)
        players = [player1]
        hex_board = board.HexBoard(30, 2, 2, 2 * 2, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            hex.fish = 1
        # statetemp.place_penguin(hex_board, player1, 1)
        # statetemp.place_penguin(hex_board, player2, 1)
        interface = PlayerInterface(statetemp, player1, players)
        # statetemp.place_penguin(hex_board, player2)
        # state.render_state(hex_board)
        layers = 2
        game = Game(statetemp.hexboard, players, 0, layers)
        # thing = game.get_next_state(statetemp, ('Move', 1, 2))
        # thing = game.map_states(statetemp, statetemp.is_over)
        game_tree = game.game_tree(statetemp)
        # interface.best_move(game_tree, player1)
        # interface.place_ordered_penguins(statetemp, player1, 1)
        # thing = player1.penguins
        playr = PlayerComp(statetemp, player1, interface)
        ref = Referee(statetemp, playr)
        ref.remove_player(player1)
        self.assertEqual(len(statetemp.players), 0)
# This runs the test executor above
if __name__ == "__main__":
    unittest.main()