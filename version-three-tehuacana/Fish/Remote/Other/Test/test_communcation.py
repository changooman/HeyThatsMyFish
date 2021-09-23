import Fish.Remote.communication as comm
from Fish.Common.state import State
from Fish.Common.board_player import BoardPlayer
from Fish.Common.board import Board

import unittest
import socket
import json
from threading import Thread
from Queue import Queue

LOCALHOST = "127.0.0.1"
PORT = 8080

class TestCommuncation(unittest.TestCase):
    """Class to test the communication protocol."""

    @classmethod
    def setUpClass(cls):
        cls.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.__server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cls.__server.bind((LOCALHOST, PORT))
        cls.__server.listen(1)

    @classmethod
    def tearDownClass(cls):
        cls.__server.close()

    def accept_void(self):
        self.remote_player.recv(comm.METHOD_CALL_BUFFER_SIZE)

    def setUp(self):
        """Define a server and client to use to test method calls
        over the protocol."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((LOCALHOST, PORT))
        self.client.settimeout(None)
        self.remote_player = self.__server.accept()[0]
        self.remote_player.settimeout(1.0)

    def tearDown(self):
        """Close the client and server"""
        self.remote_player.close()
        self.client.close()

    @staticmethod
    def __client_send_thread(client, data, queue):
        data_recv = client.recv(comm.METHOD_CALL_BUFFER_SIZE)
        data_load = json.loads(data_recv)
        client.sendall(data)
        queue.put(data_load)

    # For all tests, the Queue will contain what the client is expecting to receive, so that we can check that the messages are
    # being properly converted

    def test_start(self):
        """Test the start method call"""
        queue = Queue()
        thread = Thread(
            target=self.__client_send_thread, args=[self.client, json.dumps("void"), queue])
        thread.daemon = True
        thread.start()
        comm.start(self.remote_player, True)
        thread.join()
        data_load = queue.get()
        self.assertEqual(data_load, [comm.START, [True]])

        queue = Queue()
        thread = Thread(
            target=self.__client_send_thread, args=[self.client, json.dumps("void"), queue])
        thread.daemon = True
        thread.start()
        comm.start(self.remote_player, False)
        thread.join()
        data_load = queue.get()
        self.assertEqual(data_load, [comm.START, [False]])

    def test_end(self):
        """Test the end method call"""
        queue = Queue()
        thread = Thread(
            target=self.__client_send_thread, args=[self.client, json.dumps("void"), queue])
        thread.daemon = True
        thread.start()
        comm.end(self.remote_player, True)
        thread.join()
        data_load = queue.get()
        self.assertEqual(data_load, [comm.END, [True]])

        queue = Queue()
        thread = Thread(
            target=self.__client_send_thread, args=[self.client, json.dumps("void"), queue])
        thread.daemon = True
        thread.start()
        comm.end(self.remote_player, False)
        thread.join()
        data_load = queue.get()
        self.assertEqual(data_load, [comm.END, [False]])

    def test_play_as(self):
        """Test the play_as method call"""
        queue = Queue()
        thread = Thread(
            target=self.__client_send_thread, args=[self.client, json.dumps("void"), queue])
        thread.daemon = True
        thread.start()
        comm.play_as(self.remote_player, "red")
        thread.join()
        data_load = queue.get()
        self.assertEqual(data_load, [comm.PLAY_AS, ["red"]])

    def test_play_with(self):
        """Test the play_with method call"""
        queue = Queue()
        thread = Thread(
            target=self.__client_send_thread, args=[self.client, json.dumps("void"), queue])
        thread.daemon = True
        thread.start()
        comm.play_with(self.remote_player, ["red", "white", "black"])
        thread.join()
        data_load = queue.get()
        self.assertEqual(data_load, [comm.PLAY_WITH, [["red", "white", "black"]]])

    def test_setup(self):
        """Test the setup method call"""
        p1 = BoardPlayer("red")
        p1.penguins = [(0, 0), (0, 2)]
        p2 = BoardPlayer("black")
        p2.penguins = [(0, 1), (1, 1)]
        p3 = BoardPlayer("brown")
        p3.penguins = [(2, 0), (2, 1)]
        p4 = BoardPlayer("white")
        p4.penguins = [(1, 2), (2, 2)]
        board = Board(3, 3, uniform=True, uniform_num_fish=1)

        state = State([p1, p2, p3, p4], board)
        state_json = state.json_rep()

        queue = Queue()
        thread = Thread(
            target=self.__client_send_thread, args=[self.client, json.dumps([1, 2]), queue])
        thread.daemon = True
        thread.start()
        placement = comm.setup(self.remote_player, state)
        thread.join()
        data_load = queue.get()
        self.assertEqual(data_load, [comm.SETUP, [state_json]])
        self.assertEqual(placement, (1, 2))

    def test_take_turn(self):
        """Test the setup method call"""
        p1 = BoardPlayer("red")
        p1.penguins = [(0, 0), (0, 2)]
        p2 = BoardPlayer("black")
        p2.penguins = [(0, 1), (1, 1)]
        p3 = BoardPlayer("brown")
        p3.penguins = [(2, 0), (2, 1)]
        p4 = BoardPlayer("white")
        p4.penguins = [(1, 2), (2, 2)]
        board = Board(3, 3, uniform=True, uniform_num_fish=1)

        state = State([p1, p2, p3, p4], board)
        state_json = state.json_rep()

        queue = Queue()
        thread = Thread(
            target=self.__client_send_thread, args=[self.client, json.dumps([[1, 2], [0, 1]]), queue])
        thread.daemon = True
        thread.start()
        move = comm.take_turn(self.remote_player, state, [((1, 1), (0, 1))])
        thread.join()
        data_load = queue.get()
        actions = [[[1, 1], [0, 1]]]
        self.assertEqual(data_load, [comm.TAKE_TURN, [state_json, actions]])
        self.assertEqual(move, ((1, 2), (0, 1)))

if __name__ == "__main__":
    unittest.main()
