from collections import Counter
from copy import deepcopy

from Fish.Common.board import Board
from Fish.Common.game_tree import GameTreeNode
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State

import unittest

class TestGameTree(unittest.TestCase):
    """Test the GameTreeNode class."""

    def setUp(self):
        """Create a game for test use.
         _____       _____
        / 0,0 \_____/ 0,1 \_____
        \__A__/ 1,0 \__A__/ 1,1 \
        / 2,0 \__A__/ 2,1 \_____/
        \__A__/ 3,0 \_____/ 3,1 \
              \__A__/     \_____/
        """
        board = Board(4, 2)
        self.state = State([BoardPlayer("red")], board)
        self.state.place_avatar((0, 0), "red")
        self.state.place_avatar((1, 0), "red")
        self.state.place_avatar((2, 0), "red")
        self.state.place_avatar((3, 0), "red")
        self.state.place_avatar((0, 1), "red")
        self.root = GameTreeNode(self.state)

        board2 = Board(4, 2, [(2, 1), (1, 1), (3, 1)])
        self.state2 = State([BoardPlayer("red")], board2)
        self.state2.place_avatar((0, 0), "red")
        self.state2.place_avatar((1, 0), "red")
        self.state2.place_avatar((2, 0), "red")
        self.state2.place_avatar((3, 0), "red")
        self.state2.place_avatar((0, 1), "red")
        self.root2 = GameTreeNode(self.state2)

        board3 = Board(5, 2)
        self.state3 = State([BoardPlayer("black"), BoardPlayer("red")], board3)
        self.state3.place_avatar((0, 1), "black")
        self.state3.place_avatar((0, 0), "red")
        self.state3.place_avatar((1, 1), "black")
        self.state3.place_avatar((1, 0), "red")
        self.state3.place_avatar((2, 1), "black")
        self.state3.place_avatar((2, 0), "red")
        self.state3.place_avatar((3, 1), "black")
        self.state3.place_avatar((3, 0), "red")
        self.root3 = GameTreeNode(self.state3)


    # def test_constructor(self):
        # board = Board(5, 2)
        # state = State([BoardPlayer("black"), BoardPlayer("red")], board)

        # try:
            # n = GameTreeNode(state)
            # self.assertTrue(False)
        # except ValueError:
            # pass


    def test_children(self):
        """Test that the node generates the correct child states."""
        moves = [
            ((0, 1), (1, 1)),
            ((0, 1), (2, 1)),
            ((1, 0), (2, 1)),
            ((1, 0), (3, 1)),
            ((3, 0), (2, 1)),
            ((3, 0), (1, 1))
        ]

        children = [child.state for child in self.root.get_children()]
        self.assertEqual(len(moves), len(children))
        for move in moves:
            new_state = deepcopy(self.state)
            new_state.move_avatar(*move)
            self.assertIn(new_state, children)

        # ended game
        self.assertEqual(0, len(self.root2.get_children()))

        moves = [
            ((2, 1), (4, 1)),
            ((3, 1), (4, 1))
        ]

        children = [child.state for child in self.root3.get_children()]
        self.assertEqual(len(moves), len(children))
        for move in moves:
            new_state = deepcopy(self.state3)
            new_state.move_avatar(*move)
            self.assertIn(new_state, children)


    def exFunc(self, state):
        """Add up the sums of all penguin coordinates."""
        ret = 0
        for player in state.get_players():
            for penguin in player.get_penguins():
                ret += sum(penguin)
        return ret


    def test_query_function(self):
        """Test the query_function function."""
        self.assertEqual(Counter([8, 9, 9, 10, 7, 6]), Counter(self.root.query_function(self.exFunc)))

        # ended game
        self.assertEqual([], self.root2.query_function(self.exFunc))

        self.assertEqual(Counter([18, 17]), Counter(self.root3.query_function(self.exFunc)))


    def test_query_action(self):
        """Test the query_action function."""
        action = ((0, 1), (1, 1))
        new_state = deepcopy(self.state)
        new_state.move_avatar(*action)
        self.assertEqual(new_state, self.root.query_action(action))

        # invalid move
        action = ((0, 1), (1, 0))
        self.assertEqual(None, self.root.query_action(action))

        # ended game
        action = ((0, 1), (1, 0))
        self.assertEqual(None, self.root2.query_action(action))

        # wrong turn
        action = ((3, 0), (4, 0))
        self.assertEqual(None, self.root3.query_action(action))

        # correct turn
        action = ((3, 1), (4, 1))
        new_state = deepcopy(self.state3)
        new_state.move_avatar(*action)
        self.assertEqual(new_state, self.root3.query_action(action))


if __name__ == '__main__':
    unittest.main()
