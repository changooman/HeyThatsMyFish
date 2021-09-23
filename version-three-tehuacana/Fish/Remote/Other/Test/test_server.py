import unittest
import socket
import random
import time
import os
import json

from Queue import Queue
from threading import Thread

import Fish.Remote.server as server
from Fish.Remote.client_player import ClientPlayer

LOCALHOST = "127.0.0.1"
PORT = 8080

class DoNotRespondPlayer(ClientPlayer):
    """Client that Errors when responding to the end message"""

    def __init__(self, server_ip, port, name, depth=2, timeout=1.0):
        super(DoNotRespondPlayer, self).__init__(server_ip, port, name, depth, timeout)

    def _handle_end_msg(self, win):
        raise ValueError("{} couldn't respond, he is now a losing player!".format(self.name))

class IllegalMovePlayer(ClientPlayer):
    """A client that raises an exception when making a move"""

    def __init__(self, server_ip, port, name, depth=2, timeout=1.0):
        super(IllegalMovePlayer, self).__init__(server_ip, port, name, depth, timeout)

    def _handle_take_turn_msg(self, _state, _actions):
        raise ValueError("{} failed to take a turn!".format(self.name))
        

class SlowPlayer(ClientPlayer):
    """A client that never finishes making a move"""

    def __init__(self, server_ip, port, name, depth=2, timeout=1.0):
        super(SlowPlayer, self).__init__(server_ip, port, name, depth, timeout)

    def _handle_take_turn_msg(self, _state, _actions):
        time.sleep(10000)

class InvalidJSONPlayer(ClientPlayer):
    """A client that sends invalid json as a move"""

    def __init__(self, server_ip, port, name, depth=2, timeout=1.0):
        super(InvalidJSONPlayer, self).__init__(server_ip, port, name, depth, timeout)

    def __send_data(self, data):
        bytes_left = self.sock.sendall(data)
        time.sleep(0.1)

    def _handle_take_turn_msg(self, _state, _actions):
        self.__send_data(json.dumps("i am a bad move"))
        

class TestServer(unittest.TestCase):
    """Class to test the server"""

    def run_client_func(self, client):
        """Function to run in a thread, used for running a client concurrently"""
        try:
            client.start()
        except socket.error as e:
            print(e)
        except socket.timeout as e:
            print(e)
        except ValueError as e:
            print(e)
        except KeyboardInterrupt:
            exit()

    def run_server_func(self, board, queue):
        """Function to run the server"""
        res = server.run_tournament(LOCALHOST, PORT, board=board, waiting_period=3.0, timeout=3.0)

        if res is None:
            queue.put(res)
        else:
            queue.put(res[0])
            queue.put(res[1])
            queue.put(res[2])

    def test_run_tournament(self):
        """Run a 5-player tournament on a randomized board."""
        random.seed("test_seed")
        
        queue = Queue()
        server_thread = Thread(target=self.run_server_func, args=[None, queue])
        server_thread.daemon = True

        server_thread.start()
        time.sleep(1)

        players = [
            ClientPlayer(LOCALHOST, PORT, "andre", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "matt", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "jason", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "matthias", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "deepak", depth=1, timeout=None),
        ]

        client_threads = [Thread(target=self.run_client_func, args=[players[i]]) for i in range(5)]

        for i in range(5):
            client_threads[i].daemon = True
            client_threads[i].start()

        for i in range(4, -1, -1):
            client_threads[i].join(20)

        server_thread.join(20)
        
        winners = queue.get()
        losers = queue.get()
        violators = queue.get()
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0], "matthias")
        self.assertEqual(len(losers), 4)
        self.assertEqual(len(violators), 0)

    def test_run_tournament_not_enough(self):
        """Try to run a tournament with only 4 players. This test results in a message being printed 4 times
        describing how the peer was closed"""
        random.seed("test_seed")
        
        queue = Queue()
        server_thread = Thread(target=self.run_server_func, args=[None, queue])
        server_thread.daemon = True

        server_thread.start()
        time.sleep(1)

        players = [
            ClientPlayer(LOCALHOST, PORT, "a", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "b", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "c", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "d", depth=1, timeout=None),
        ]

        client_threads = [Thread(target=self.run_client_func, args=[players[i]]) for i in range(4)]

        for i in range(4):
            client_threads[i].daemon = True
            client_threads[i].start()

        for i in range(3, -1, -1):
            client_threads[i].join(8)

        server_thread.join(100)
        
        self.assertIsNone(queue.get())

    def test_run_tournament_max_10(self):
        """Try to run an 11-player tournament server and only allow 10 players. This test will print that the
        peer has closed, as the last player will close without being able to connect."""
        random.seed("test_seed")
        
        queue = Queue()
        server_thread = Thread(target=self.run_server_func, args=[None, queue])
        server_thread.daemon = True

        server_thread.start()
        time.sleep(1)

        players = [
            ClientPlayer(LOCALHOST, PORT, "a", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "b", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "c", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "d", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "e", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "f", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "g", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "h", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "i", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "j", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "k", depth=1, timeout=None),
        ]

        client_threads = [Thread(target=self.run_client_func, args=[players[i]]) for i in range(11)]

        for i in range(11):
            client_threads[i].daemon = True
            client_threads[i].start()

        for i in range(10, -1, -1):
            if i == 10:
                client_threads[i].join(10)
            else:
                client_threads[i].join(100)

        server_thread.join(100)
        
        winners = queue.get()
        losers = queue.get()
        violators = queue.get()
        self.assertEqual(len(winners) + len(losers) + len(violators), 10)


    def test_run_tournament_winner_does_not_respond(self):
        """Convert that a player who does not respond to the end message gets converted to
        a losing player. matthias should the player who does not respond."""
        random.seed("test_seed")
        
        queue = Queue()
        server_thread = Thread(target=self.run_server_func, args=[None, queue])
        server_thread.daemon = True

        server_thread.start()
        time.sleep(1)

        players = [
            ClientPlayer(LOCALHOST, PORT, "andre", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "matt", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "jason", depth=1, timeout=None),
            DoNotRespondPlayer(LOCALHOST, PORT, "matthias", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "deepak", depth=1, timeout=None),
        ]

        client_threads = [Thread(target=self.run_client_func, args=[players[i]]) for i in range(5)]

        for i in range(5):
            client_threads[i].daemon = True
            client_threads[i].start()

        for i in range(4, -1, -1):
            client_threads[i].join(20)

        server_thread.join(20)
        
        winners = queue.get()
        losers = queue.get()
        violators = queue.get()
        self.assertEqual(len(winners), 0)
        self.assertEqual(len(losers), 5)
        self.assertEqual(len(violators), 0)

    def test_run_tournament_bad_move(self):
        """Test that a player who makes a bad move gets converted to a cheater."""
        random.seed("test_seed")
        
        queue = Queue()
        server_thread = Thread(target=self.run_server_func, args=[None, queue])
        server_thread.daemon = True

        server_thread.start()
        time.sleep(1)

        players = [
            ClientPlayer(LOCALHOST, PORT, "andre", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "matt", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "jason", depth=1, timeout=None),
            IllegalMovePlayer(LOCALHOST, PORT, "matthias", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "deepak", depth=1, timeout=None),
        ]

        client_threads = [Thread(target=self.run_client_func, args=[players[i]]) for i in range(5)]

        for i in range(5):
            client_threads[i].daemon = True
            client_threads[i].start()

        for i in range(4, -1, -1):
            client_threads[i].join(10)

        server_thread.join(10)
        
        _winners = queue.get()
        _losers = queue.get()
        violators = queue.get()
        self.assertEqual(len(violators), 1)
        self.assertEqual(violators[0], "matthias")

    def test_run_tournament_slow_move(self):
        """Test that a player who times out making a move gets converted to a cheater."""
        random.seed("test_seed")
        
        queue = Queue()
        server_thread = Thread(target=self.run_server_func, args=[None, queue])
        server_thread.daemon = True

        server_thread.start()
        time.sleep(1)

        players = [
            ClientPlayer(LOCALHOST, PORT, "andre", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "matt", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "jason", depth=1, timeout=None),
            SlowPlayer(LOCALHOST, PORT, "matthias", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "deepak", depth=1, timeout=None),
        ]

        client_threads = [Thread(target=self.run_client_func, args=[players[i]]) for i in range(5)]

        for i in range(5):
            client_threads[i].daemon = True
            client_threads[i].start()

        for i in range(4, -1, -1):
            if i == 3:
                # kill this thread earlier so the test doesn't take 60 seconds
                client_threads[i].join(10)
            else:
                client_threads[i].join(15)

        server_thread.join(15)
        
        _winners = queue.get()
        _losers = queue.get()
        violators = queue.get()
        self.assertEqual(len(violators), 1)
        self.assertEqual(violators[0], "matthias")

    def test_run_tournament_invalid_json_move(self):
        """Test that a player who times out making a move gets converted to a cheater."""
        random.seed("test_seed")
        
        queue = Queue()
        server_thread = Thread(target=self.run_server_func, args=[None, queue])
        server_thread.daemon = True

        server_thread.start()
        time.sleep(1)

        players = [
            ClientPlayer(LOCALHOST, PORT, "andre", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "matt", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "jason", depth=1, timeout=None),
            InvalidJSONPlayer(LOCALHOST, PORT, "matthias", depth=1, timeout=None),
            ClientPlayer(LOCALHOST, PORT, "deepak", depth=1, timeout=None),
        ]

        client_threads = [Thread(target=self.run_client_func, args=[players[i]]) for i in range(5)]

        for i in range(5):
            client_threads[i].daemon = True
            client_threads[i].start()

        for i in range(4, -1, -1):
            if i == 3:
                # kill this thread earlier so the test doesn't take 60 seconds
                client_threads[i].join(10)
            else:
                client_threads[i].join(20)

        server_thread.join(20)
        
        _winners = queue.get()
        _losers = queue.get()
        violators = queue.get()
        self.assertEqual(len(violators), 1)
        self.assertEqual(violators[0], "matthias")
    

if __name__ == "__main__":
    unittest.main()
    os._exit(0)
