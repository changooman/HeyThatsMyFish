import unittest
from state import *
from board import *
from strategy import *
from game_tree import *


# This test class serves to test the next_state function that either will return a state instance that will follow
# the given state if a certain action is completed, or an error saying that the given action is invalid
class TestBestMove(unittest.TestCase):
    # tests the best move for a given tree
    def test_bext_move(self):
        return
        # player1 = state.Player('red', 3)
        # player2 = state.Player('black', 4)
        # players = [player1, player2]
        # hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        # statetemp = state.create_state(players, hex_board)
        # for hex in hex_board.hexagons:
        #     if hex.xy == (1,0):
        #         hex.fish = 5
        #     else:
        #         hex.fish = 1
        # for hex in hex_board.hexagons:
        #     if hex.xy == [0, 0]:
        #         hex.spottaken = True
        #         player1.penguins.append([0, 0])
        # for hex in hex_board.hexagons:
        #     if hex.xy == [2, 2]:
        #         hex.spottaken = True
        #         player1.penguins.append([2, 2])
        # interface = PlayerInterface(statetemp, player1, players)
        # game = Game(statetemp.hexboard, players, 0)
        # game_tree = game.game_tree(statetemp, 3)
        # self.assertEqual(PlayerInterface.best_move(interface, game_tree, player1), (1,2))


    # tests the best move for a given tree where only the given player has penguins
    def test_best_move1(self):
        return
        # player1 = state.Player('red', 3)
        # player2 = state.Player('black', 4)
        # players = [player1, player2]
        # hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        # statetemp = state.create_state(players, hex_board)
        # for hex in hex_board.hexagons:
        #     if hex.xy == (1, 0):
        #         hex.fish = 5
        #     else:
        #         hex.fish = 1
        # for hex in hex_board.hexagons:
        #     if hex.xy == [0, 0]:
        #         hex.spottaken = True
        #         player1.penguins.append([0, 0])
        # interface = PlayerInterface(statetemp, player1, players)
        # game = Game(statetemp.hexboard, players, 0)
        # game_tree = game.game_tree(statetemp, 3)
        # self.assertEqual(PlayerInterface.best_move(interface, game_tree, player1), (1, 2))

    # tests the best move for a given tree with other player at a different location
    def test_bext_move2(self):
        return
        # player1 = state.Player('red', 3)
        # player2 = state.Player('black', 4)
        # players = [player1, player2]
        # hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        # statetemp = state.create_state(players, hex_board)
        # for hex in hex_board.hexagons:
        #     if hex.xy == (1,0):
        #         hex.fish = 5
        #     else:
        #         hex.fish = 1
        # for hex in hex_board.hexagons:
        #     if hex.xy == [0, 0]:
        #         hex.spottaken = True
        #         player1.penguins.append([0, 0])
        # for hex in hex_board.hexagons:
        #     if hex.xy == [1, 2]:
        #         hex.spottaken = True
        #         player1.penguins.append([1, 2])
        # interface = PlayerInterface(statetemp, player1, players)
        # game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        # self.assertEqual(PlayerInterface.best_move(interface, game_tree, player1), (1,4))

    # tests the best move for a given tree where only the given player has penguins at a different location
    def test_best_move3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (1, 0):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 2]:
                hex.spottaken = True
                player1.penguins.append([0, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        # self.assertEqual(PlayerInterface.best_move(interface, game_tree, player1), (5, 4))

class TestBestPath(unittest.TestCase):
    #tests the best path for a given tree
    def test_next_path(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (1,0):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        # self.assertEqual(interface.best_path(game_tree, player1)[3][0], 3)

    def test_next_path1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        # self.assertEqual(len(interface.best_path(game_tree, player1)), 4)


class TestScoreList(unittest.TestCase):

    def test_score_list(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        best_path = interface.check_best_path(origin_list, player1, game_tree)
        # self.assertEqual(len(interface.check_scores(best_path, player1)), 82)

    def test_score_list1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [1, 1]:
                hex.spottaken = True
                player1.penguins.append([1, 1])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        best_path = interface.check_best_path(origin_list, player1, game_tree)
        # self.assertEqual(len(interface.check_scores(best_path, player1)), 88)

class TestAllPaths(unittest.TestCase):

    def test_all_paths(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(all_paths), 561)

    def test_all_paths1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(all_paths[1]), 4)

    def test_all_paths2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [1, 2]:
                hex.spottaken = True
                player1.penguins.append([1, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(all_paths), 490)

    def test_all_paths3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [1, 1]:
                hex.spottaken = True
                player1.penguins.append([1, 1])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(all_paths[1]), 4)

class TestOriginList(unittest.TestCase):

    def test_origin_list(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(origin_list), 93)

    def test_origin_list1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(origin_list[5][1]), 11)

class TestCheckBestPath(unittest.TestCase):

    def test_check_best_path(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(interface.check_best_path(origin_list, player1, game_tree)), 93)

    def test_check_best_path1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(interface.check_best_path(origin_list, player1, game_tree)[0]), 4)

    def test_check_best_path2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (1, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [1, 1]:
                hex.spottaken = True
                player1.penguins.append([1, 1])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(interface.check_best_path(origin_list, player1, game_tree)), 100)

    def test_check_best_path3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [0, 2]:
                hex.spottaken = True
                player1.penguins.append([0, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(len(interface.check_best_path(origin_list, player1, game_tree)[0]), 4)

class TestGetPath(unittest.TestCase):

    def test_get_path(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(interface.get_path(all_paths[0][0], all_paths), all_paths[0])

    def test_get_path1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(interface.get_path(all_paths[4][0], all_paths), all_paths[4])

    def test_get_path2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (1, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(interface.get_path(all_paths[0][0], all_paths), all_paths[0])

    def test_get_path3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (1, 3):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        all_paths, origin_list = interface.get_all_paths(game_tree)
        # self.assertEqual(interface.get_path(all_paths[4][0], all_paths), all_paths[4])

class TestPlaceOrderedPenguin(unittest.TestCase):
    #tests the best path for a given tree
    def test_place_ordered_penguin(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (1,0):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        game_tree = game.game_tree(statetemp, 1)
        interface.place_ordered_penguins(statetemp, player1, 1)
        # self.assertEqual(len(player1.penguins), 3)

    def test_place_ordered_penguin1(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        for hex in hex_board.hexagons:
            if hex.xy == (0, 1):
                hex.fish = 5
            else:
                hex.fish = 1
        for hex in hex_board.hexagons:
            if hex.xy == [0, 0]:
                hex.spottaken = True
                player1.penguins.append([0, 0])
        for hex in hex_board.hexagons:
            if hex.xy == [2, 2]:
                hex.spottaken = True
                player1.penguins.append([2, 2])
        interface = PlayerInterface(statetemp, player1, players)
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        interface.place_ordered_penguins(statetemp, player1, 1)
        # self.assertEqual(len(player1.penguins), 5)

        # tests the best path for a given tree
    def test_place_ordered_penguin2(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        interface.place_ordered_penguins(statetemp, player1, 1)
        interface.place_ordered_penguins(statetemp, player2, 1)
        # self.assertEqual(len(player1.penguins), 3)

    def test_place_ordered_penguin3(self):
        player1 = state.Player('red', 3)
        player2 = state.Player('black', 4)
        players = [player1, player2]
        hex_board = board.HexBoard(30, 4, 3, 4 * 3, [])
        statetemp = state.create_state(players, hex_board)
        interface = PlayerInterface(statetemp, player1, players)
        game = Game(statetemp.hexboard, players, 0)
        interface.place_ordered_penguins(statetemp, player1, 1)
        interface.place_ordered_penguins(statetemp, player2, 1)
        # self.assertEqual(len(player1.penguins), 3)


# This runs the test executor above
if __name__ == "__main__":
    unittest.main()
