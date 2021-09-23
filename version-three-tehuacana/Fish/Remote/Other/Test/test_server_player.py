import unittest
import socket
import json

from threading import Thread
from Queue import Queue

import Fish.Remote.server_player as server_player
import Fish.Remote.communication as comm
from Fish.Remote.server_player import ServerPlayer
from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State
from Fish.Player.strategy import Strategy
from Fish.Remote.client_player import ClientPlayer

LOCALHOST = "127.0.0.1"
PORT = 8080

class TestServerPlayer(unittest.TestCase):
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
        over the protocol.

        remote_player (socket): the socket that the ServerPlayer uses
        player (ServerPlayer): the server player to test.
        client (socket): the socket that represents the client player receiving
            and sending messages from and to the ServerPlayer"""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((LOCALHOST, PORT))
        self.client.send(json.dumps("matt"))
        self.remote_player = self.__server.accept()[0]
        self.remote_player.settimeout(1)
        self.client.settimeout(1)
        self.player = ServerPlayer(self.remote_player)

    def tearDown(self):
        """Close the client and server"""
        self.client.close()
        self.remote_player.close()

    def test_correct_name(self):
        """"Test that the name was read correctly from the client"""
        self.assertEqual(self.player.name, "matt")

    @staticmethod
    def json_void():
        return json.dumps("void")

    @staticmethod
    def start_client_thread(func, args):
        """Function to use to mock a client sending data.

        func (function): the function to run in the thread
        args (list): a list of arguments to run
        
        return (Thread, Queue): the thread that was started and a queue
        """

        thread = Thread(target=func, args=args)
        thread.start()
        return thread

    def test_make_placement(self):
        """Test the make_placement function. The client will return a placement
        with the row value increased by one."""

        def client_func(client_sock):
            data = client_sock.recv(comm.METHOD_CALL_BUFFER_SIZE)
            data = json.loads(data)
            state = State.json_to_state(data[1][0])
            strat = Strategy()
            placement = strat.make_placement(state)
            placement = [placement[0] + 1, placement[1]]
            send_data = json.dumps(placement)
            client_sock.sendall(send_data)

        board = Board(3, 2, [(1, 1)])
        state = State([BoardPlayer("black"), BoardPlayer("red")], board)
        thread = self.start_client_thread(client_func, [self.client])
        placement = self.player.make_placement(state)
        thread.join(1)
        self.assertEqual(placement, (1, 0))

    def test_make_move(self):
        """Test the make_move function. The client will return a move
        with the row value of the 'from' coordinate increased by one
        and the col value of the 'to' coordinate increased by one"""

        def client_func(client_sock):
            data = client_sock.recv(comm.METHOD_CALL_BUFFER_SIZE)
            data = json.loads(data)
            state = State.json_to_state(data[1][0])
            strat = Strategy()
            move = strat.make_move(state, 2)
            move = [[move[0][0] + 1, move[0][1]], [move[1][0], move[1][1]+1]]
            send_data = json.dumps(move)
            client_sock.sendall(send_data)

        board = Board(4, 2, uniform=True, uniform_num_fish=1)
        board.tiles[2][0].num_fish = 5
        state = State([BoardPlayer("red"), BoardPlayer("black")], board)
        state.place_avatar((0, 0), "red")
        state.place_avatar((0, 1), "black")
        thread = self.start_client_thread(client_func, [self.client])
        move = self.player.make_move(state)
        thread.join(1)
        self.assertEqual(move, ((1, 0), (2, 1)))

    def test_inform_start(self):
        """Test the inform_start function. Record the response in a queue
        and check that the client gets it."""

        def client_func(client_sock, queue):
            data = client_sock.recv(comm.METHOD_CALL_BUFFER_SIZE)
            data = json.loads(data)
            queue.put(data)
            client_sock.sendall(self.json_void())

        queue = Queue()
        thread = self.start_client_thread(client_func, [self.client, queue])
        self.player.inform_start()
        thread.join(1)
        msg = queue.get()
        self.assertEqual(msg[0], comm.START)
        self.assertEqual(msg[1][0], True)

    def test_inform_end(self):
        """Test the inform_end function. Record the response in a queue
        and check that the client gets it."""

        def client_func(client_sock, queue):
            data = client_sock.recv(comm.METHOD_CALL_BUFFER_SIZE)
            data = json.loads(data)
            queue.put(data)
            client_sock.sendall(self.json_void())

        queue = Queue()
        thread = self.start_client_thread(client_func, [self.client, queue])
        self.player.inform_end(False)
        thread.join(1)
        msg = queue.get()
        self.assertEqual(msg[0], comm.END)
        self.assertEqual(msg[1][0], False)

        thread = self.start_client_thread(client_func, [self.client, queue])
        self.player.inform_end(True)
        thread.join(1)
        msg = queue.get()
        self.assertEqual(msg[0], comm.END)
        self.assertEqual(msg[1][0], True)

    
    def test_set_and_get_color(self):
        """Test the get_color function. Record the response in a queue
        and check that the client gets it."""

        def client_func(client_sock, queue):
            data_1 = client_sock.recv(comm.METHOD_CALL_BUFFER_SIZE)
            client_sock.sendall(self.json_void())
            data_2 = client_sock.recv(comm.METHOD_CALL_BUFFER_SIZE)
            client_sock.sendall(self.json_void())
            data_1 = json.loads(data_1)
            data_2 = json.loads(data_2)
            queue.put(data_1)
            queue.put(data_2)

        queue = Queue()
        thread = self.start_client_thread(client_func, [self.client, queue])
        self.assertIsNone(self.player.get_color())
        self.player.set_color("red")
        thread.join(1)
        msg_1 = queue.get()
        msg_2 = queue.get()
        self.assertEqual(msg_1[0], comm.PLAY_AS)
        self.assertEqual(msg_2[0], comm.PLAY_WITH)
        self.assertEqual(msg_1[1][0], "red")
        self.assertEqual(set(msg_2[1][0]), {"white", "black", "brown"})
        self.assertEqual(self.player.get_color(), "red")
    

if __name__ == "__main__":
    unittest.main()
