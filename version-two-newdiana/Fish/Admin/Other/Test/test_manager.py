from Fish.Admin.manager import Manager
from Fish.Player.player import Player

import random
import unittest

class SlowPlayer(Player):
    """A very slow Fish player."""

    def you_have_won(self, state):
        sleep(10)
        return super(SlowPlayer, self).you_have_won(state)


    def you_have_lost(self, state):
        sleep(10)
        return super(SlowPlayer, self).you_have_lost(state)


class UnstablePlayer(Player):
    """A Fish player that throws exceptions."""

    def make_placement(self, state):
        raise Exception


    def make_move(self, state):
        raise Exception


    def you_have_won(self, state):
        raise Exception


    def you_have_lost(self, state):
        raise Exception


class SemiUnstablePlayer(Player):
    """A Fish player that throws exceptions only when being informed of tournament outcomes."""

    def you_have_won(self, state):
        raise Exception


    def you_have_lost(self, state):
        raise Exception


class TestManager(unittest.TestCase):
    """Test the Manager class."""

    def setUp(self):
        """Create some objects for testing convenience."""
        self.harrison = Player(depth=1)
        self.andre = Player(depth=1)
        self.matthias = Player(depth=1)
        self.jason = Player(depth=1)
        self.ben = Player(depth=1)
        self.deepak = Player(depth=1)
        self.julia = Player(depth=1)
        self.suzanne = Player(depth=1)

        self.one_player = [
            self.harrison
        ]

        self.two_players = [
            self.harrison,
            self.andre
        ]

        self.three_players = [
            self.harrison,
            self.andre,
            self.matthias
        ]

        self.four_players = [
            self.harrison,
            self.andre,
            self.matthias,
            self.jason
        ]

        self.five_players = [
            self.harrison,
            self.andre,
            self.matthias,
            self.jason,
            self.ben
        ]

        self.six_players = [
            self.harrison,
            self.andre,
            self.matthias,
            self.jason,
            self.ben,
            self.deepak
        ]

        self.seven_players = [
            self.harrison,
            self.andre,
            self.matthias,
            self.jason,
            self.ben,
            self.deepak,
            self.julia
        ]

        self.eight_players = [
            self.harrison,
            self.andre,
            self.matthias,
            self.jason,
            self.ben,
            self.deepak,
            self.julia,
            self.suzanne
        ]

        self.man = Manager(self.eight_players)


    def test_constructor(self):
        """Test the Manager constructor."""
        man = Manager(self.one_player, 1, 3)
        man = Manager(self.three_players, 3, 7)

        try:
            man = Manager(self.three_players, -1, 0)
            self.assertTrue(False)
        except ValueError:
            pass

        try:
            man = Manager(self.three_players, 0, -1)
            self.assertTrue(False)
        except ValueError:
            pass

        try:
            man = Manager(self.three_players, 3, 2)
            self.assertTrue(False)
        except ValueError:
            pass

        try:
            man = Manager(self.three_players, 4, 8)
            self.assertTrue(False)
        except ValueError:
            pass


    def test_group_players(self):
        """Test the __group_players function."""
        self.assertEqual([[self.harrison, self.andre]],
                         self.man._Manager__group_players(self.two_players))
        self.assertEqual([[self.harrison, self.andre, self.matthias]],
                         self.man._Manager__group_players(self.three_players))
        self.assertEqual([[self.harrison, self.andre, self.matthias, self.jason]],
                         self.man._Manager__group_players(self.four_players))
        self.assertEqual([[self.harrison, self.andre, self.matthias],
                          [self.jason, self.ben]],
                         self.man._Manager__group_players(self.five_players))
        self.assertEqual([[self.harrison, self.andre, self.matthias, self.jason],
                          [self.ben, self.deepak]],
                         self.man._Manager__group_players(self.six_players))
        self.assertEqual([[self.harrison, self.andre, self.matthias, self.jason],
                          [self.ben, self.deepak, self.julia]],
                         self.man._Manager__group_players(self.seven_players))
        self.assertEqual([[self.harrison, self.andre, self.matthias, self.jason],
                          [self.ben, self.deepak, self.julia, self.suzanne]],
                         self.man._Manager__group_players(self.eight_players))


    def test_board_size(self):
        """Test the __board_size function."""
        for i in range(1,5):
            size = self.man._Manager__board_size(i)
            self.assertTrue(size[0] * size[1] > (6-i) * i)


    def test_remove_violators(self):
        """Test the __remove_violators function."""
        man = Manager(self.eight_players)
        man._Manager__remove_violators([])
        self.assertEqual(self.eight_players, man.players)
        man._Manager__remove_violators([self.harrison, self.andre, self.jason])
        self.assertEqual([self.matthias, self.ben, self.deepak, self.julia, self.suzanne], man.players)
        man._Manager__remove_violators([self.julia, self.deepak])
        self.assertEqual([self.matthias, self.ben, self.suzanne], man.players)


    def test_sort_players(self):
        """Test the __sort_players function."""
        self.assertEqual([],
                         self.man._Manager__sort_players([]))
        self.assertEqual([self.andre],
                         self.man._Manager__sort_players([self.andre]))
        self.assertEqual([self.harrison, self.andre],
                         self.man._Manager__sort_players([self.andre, self.harrison]))
        self.assertEqual([self.harrison, self.andre, self.matthias, self.suzanne],
                         self.man._Manager__sort_players([self.matthias, self.suzanne, self.andre, self.harrison]))


    def test_tournament_over(self):
        """Test the __tournament_over function."""
        self.assertTrue(self.man._Manager__tournament_over(
            [],
            []))
        self.assertTrue(self.man._Manager__tournament_over(
            [self.harrison, self.andre],
            [self.harrison, self.andre]))
        self.assertTrue(self.man._Manager__tournament_over(
            [self.harrison, self.andre],
            [self.harrison]))
        self.assertTrue(self.man._Manager__tournament_over(
            [self.harrison, self.andre, self.matthias],
            [self.harrison, self.andre]))
        self.assertTrue(self.man._Manager__tournament_over(
            [self.harrison, self.andre, self.matthias, self.jason],
            [self.harrison, self.andre]))
        self.assertTrue(self.man._Manager__tournament_over(
            [self.harrison, self.andre, self.matthias, self.jason, self.deepak],
            [self.harrison, self.andre, self.matthias, self.jason, self.deepak]))
        self.assertTrue(self.man._Manager__tournament_over(
            [self.harrison, self.andre, self.matthias, self.jason, self.deepak],
            [self.deepak]))
        self.assertTrue(self.man._Manager__tournament_over(
            [self.harrison, self.andre, self.matthias, self.jason, self.deepak],
            []))
        self.assertFalse(self.man._Manager__tournament_over(
            [self.harrison, self.andre, self.matthias, self.jason, self.deepak, self.julia],
            [self.harrison, self.andre, self.matthias, self.jason, self.julia]))
        self.assertFalse(self.man._Manager__tournament_over(
            [self.harrison, self.andre, self.matthias, self.jason, self.deepak],
            [self.harrison, self.andre, self.matthias, self.jason]))
        self.assertFalse(self.man._Manager__tournament_over(
            [self.harrison, self.andre, self.matthias, self.jason, self.deepak],
            [self.harrison, self.andre, self.matthias]))
        self.assertFalse(self.man._Manager__tournament_over(
            [self.harrison, self.andre, self.matthias, self.jason, self.deepak],
            [self.harrison, self.andre]))


    def test_inform_players(self):
        """Test the __inform_players function."""
        self.assertEqual(self.one_player,
                         self.man._Manager__inform_players(self.one_player))
        self.assertEqual(self.three_players,
                         self.man._Manager__inform_players(self.three_players))
        self.assertEqual(self.eight_players,
                         self.man._Manager__inform_players(self.eight_players))

        slow = SlowPlayer()
        unstable = UnstablePlayer()

        self.man = Manager(self.two_players + [slow, unstable])
        self.assertEqual(self.two_players,
                         self.man._Manager__inform_players(self.two_players + [slow]))

        self.man = Manager(self.two_players + [slow, unstable])
        self.assertEqual(self.two_players,
                         self.man._Manager__inform_players([unstable] + self.two_players))

        self.man = Manager(self.two_players + [slow, unstable])
        self.assertEqual([],
                         self.man._Manager__inform_players([slow, unstable]))


    def test_run_round(self):
        """Test the __run_round function."""
        try:
            self.man._Manager__run_round([])
            self.assertTrue(False)
        except:
            pass

        try:
            self.man._Manager__run_round(self.one_player)
            self.assertTrue(False)
        except:
            pass

        self.assertEqual([], self.man._Manager__run_round([UnstablePlayer(), UnstablePlayer()]))
        self.assertEqual(self.one_player, self.man._Manager__run_round(self.one_player + [UnstablePlayer()]))

        random.seed("test_seed")
        self.assertEqual([self.andre], Manager(self.two_players)._Manager__run_round(self.two_players))

        for players in (self.three_players, self.four_players, self.five_players,
                        self.six_players, self.seven_players, self.eight_players):
            victors = self.man._Manager__run_round(players)
            self.assertTrue(len(victors) > 0)


    def test_run(self):
        """Test the run function."""
        self.assertEqual(self.one_player, Manager(self.one_player + [UnstablePlayer()]).run())
        self.assertEqual(self.one_player, Manager(self.one_player + [SemiUnstablePlayer()]).run())
        self.assertEqual([], Manager([UnstablePlayer(), SemiUnstablePlayer()]).run())

        random.seed("test_seed")
        self.assertEqual([self.andre], Manager(self.two_players).run())

        for players in (self.three_players, self.four_players, self.five_players,
                        self.six_players, self.seven_players, self.eight_players):
            victors = Manager(players).run()
            self.assertTrue(len(victors) > 0)


if __name__ == '__main__':
    unittest.main()
