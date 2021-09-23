
from Fish.Admin.game_visualizer import parse_num_players
from Fish.Admin.game_visualizer import get_player_list
from Fish.Admin.game_visualizer import GameVisualizerWindow
from Fish.Admin.referee import Referee
from Fish.Common.board_player import BoardPlayer

import unittest


class TestGameVisualizer(unittest.TestCase):
    """Class to test the game visualizer"""

    def test_parse_num_players(self):
        """Test the parse_num_players function"""

        self.assertIsNone(parse_num_players("a"))
        self.assertIsNone(parse_num_players("1"))
        self.assertIsNone(parse_num_players("5"))
        self.assertEqual(parse_num_players("2"), 2)
        self.assertEqual(parse_num_players("3"), 3)
        self.assertEqual(parse_num_players("4"), 4)

    def test_get_player_list(self):
        """Test the get_player_list function"""

        two_player_list = get_player_list(2)
        three_player_list = get_player_list(3)
        four_player_list = get_player_list(4)

        self.assertEqual(len(two_player_list), 2)
        self.assertEqual(len(three_player_list), 3)
        self.assertEqual(len(four_player_list), 4)

        colors = BoardPlayer.POSSIBLE_COLORS
        
        for i in range(4):
            self.assertEqual(four_player_list[i].get_color(), colors[i])
            if i < 3:
                self.assertEqual(three_player_list[i].get_color(), colors[i])
            if i < 2:
                self.assertEqual(two_player_list[i].get_color(), colors[i])

   # def test_get_scores_in_order_of_players(self):
   #     """Test the get_scores_in_order_of_players function"""

   #     players = get_player_list(4)
   #     ref = Referee(players, (5, 5), timeout=600)

   #     win = GameVisualizerWindow(ref)

   #     # order of players by color
   #     colors = win.player_color_order
   #     self.assertEqual(colors, BoardPlayer.POSSIBLE_COLORS)

   #     player_scores_init = win.get_scores_in_order_of_players()

   #     self.assertEqual(player_scores_init, [0, 0, 0, 0])

   #     # run the referee 10 times, 8 for penguin placements and then we move
   #     # players 1 and 2
   #     for _ in range(10):
   #         win.referee.run_turn()

   #     player_scores_new = win.get_scores_in_order_of_players()
   #     self.assertNotEqual(player_scores_new[0], 0)
   #     self.assertNotEqual(player_scores_new[1], 0)

   # def test_get_current_scores_buffer(self):
   #     """Test the get_current_scores_buffer function"""

   #     players = get_player_list(4)
   #     ref = Referee(players, (5, 5), timeout=600)

   #     win = GameVisualizerWindow(ref)

   #     expected_init_string = "Scores:\nred: 0\tblack: 0\twhite: 0\tbrown: 0\t"
   #     self.assertEqual(expected_init_string, win.get_current_scores_buffer())

   #     # run the referee 10 times, 8 for penguin placements and then we move
   #     # players 1 and 2
   #     for _ in range(10):
   #         win.referee.run_turn()

   #     player_scores_new = win.get_scores_in_order_of_players()
   #     expected_new_string = "Scores:\nred: {}\tblack: {}\twhite: 0\tbrown: 0\t".format(player_scores_new[0], player_scores_new[1])

   #     self.assertEqual(expected_new_string, win.get_current_scores_buffer())
    

if __name__ == '__main__':
    unittest.main()
