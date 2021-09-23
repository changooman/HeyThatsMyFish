# -*- coding: utf-8 -*-
import unittest
import socket
import json
import random
import time

from threading import Thread
from Queue import Queue

import Fish.Remote.server_player as server_player
from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State
from Fish.Player.strategy import Strategy
from Fish.Admin.manager import Manager
from Fish.Remote.client_player import ClientPlayer
from Fish.Remote.server_player import ServerPlayer

LOCALHOST = "127.0.0.1"
PORT = 8080

class DoNotRespondPlayer(ClientPlayer):

    def __init__(self, server_ip, port, name, depth=2, timeout=1.0):
        super(DoNotRespondPlayer, self).__init__(server_ip, port, name, depth, timeout)

    def _handle_end_msg(self, win):
        time.sleep(100)

class TestClientPlayer(unittest.TestCase):
    """Class to test the server player."""

    @classmethod
    def setUpClass(cls):
        cls.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cls.__server.bind((LOCALHOST, PORT))
        cls.__server.listen(1)

    @classmethod
    def tearDownClass(cls):
        cls.__server.close()

    def setUp(self):
        """Define a server and client to use to test method calls
        over the protocol."""
        self.player_red = ClientPlayer(LOCALHOST, PORT, "andre", depth=1, timeout=10)
        self.remote_player_red = self.__server.accept()[0]
        self.player_black = ClientPlayer(LOCALHOST, PORT, "matt", depth=1, timeout=10)
        self.remote_player_black = self.__server.accept()[0]
        self.player_bad = DoNotRespondPlayer(LOCALHOST, PORT, "bad", depth=1, timeout=10)
        self.remote_player_bad = self.__server.accept()[0]
        self.server_player_red = ServerPlayer(self.remote_player_red)
        self.server_player_black = ServerPlayer(self.remote_player_black)
        self.server_player_bad = ServerPlayer(self.remote_player_bad)


    def tearDown(self):
        """Close the client and server"""
        self.player_red.sock.close()
        self.player_black.sock.close()
        self.remote_player_red.close()
        self.remote_player_black.close()

    def test_name_sent(self):
        """Test that the name is sent to the server"""
        self.assertEqual(self.server_player_red.name, "andre")
        self.assertEqual(self.server_player_black.name, "matt")

    def test_is_name_valid(self):
        """Test the is_name_valid function"""
        unicode_str = "♥αβγ!"
        self.assertFalse(self.player_red.is_name_valid(""))
        self.assertFalse(self.player_red.is_name_valid(unicode_str))
        self.assertFalse(self.player_red.is_name_valid("crash bandicoot"))
        self.assertTrue(self.player_red.is_name_valid("andre"))

    def run_client_func(self, client):
        """Function to run in a thread, used for running a client concurrently"""
        client.start()

    def test_start(self):
        """Test the start function of the client_player"""
        random.seed("test_seed")
        players = [self.server_player_red, self.server_player_black]
        thread_red = Thread(target=self.run_client_func, args=[self.player_red])
        thread_red.daemon = True
        thread_black = Thread(target=self.run_client_func, args=[self.player_black])
        thread_black.daemon = True
        manager = Manager(players)
        thread_red.start()
        thread_black.start()
        winners = manager.run()
        thread_black.join(180)
        thread_red.join(180)
        self.assertEqual(winners, [self.server_player_black])


    def test_start_not_responding_player(self):
        """Test the run function."""
        random.seed("test_seed")

        players = [self.server_player_red, self.server_player_bad]
        thread_red = Thread(target=self.run_client_func, args=[self.player_red])
        thread_red.daemon = True
        thread_bad = Thread(target=self.run_client_func, args=[self.player_bad])
        thread_bad.daemon = True
        manager = Manager(players)
        thread_red.start()
        thread_bad.start()
        winners = manager.run()
        thread_bad.join(10)
        thread_red.join(10)
        self.assertEqual(winners, [])


if __name__ == "__main__":
    unittest.main()
