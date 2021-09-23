import Tkinter as tk
from Tkinter import *
from state import *
from board import *
from game_tree import *

# Purpose: Represents a basis for allowing the referee to host communication through its variety of functions/method calls.
class PlayerInterface:
    # Purpose: Constructs a PlayerInterface object
    # @param state A GameState object which hosts the critical data for helping direct function calls for certain players
    # @param player The player associated with the PlayerInterface who will have the functions called on
    # @param player_protocol A PlayerProtocol object which helps facilitate the communication
    # @param render A Render Object which helps visualize the state of the game
    def __init__(state, player, player_protocol, render):
        current_state = state
        current_player = player
        player_protocol = player_protocol
        game_rendering = render


    # Purpose: Returns the state of the PlayerInterface
    def get_state(self):
        return self.current_state


    # Purpose: Returns the associated Player of the PlayerInterface
    def get_player(self):
        return self.current_player


    # Purpose: Returns the PlayerProtocl
    def get_playerprotocol(self):
        return self.player_protocol


    # Purpose: Sets the state of the PlayerInterface, allowing
    # functions for different possible states if needed
    def set_state(self, state):
        self.current_state = state


    # Purpose: sets up the current player that will be giving actions
    # @param player, the instance of the current player
    def set_player(self, player):
        self.player = player


    # Purpose: sets up the player protocol that will be used by this
    # interface
    # @param protocol, the protocol player’s actions must go through
    def set_playerprotocol(self, protocol):
        self.player_protocol = protocol


    # Purpose: Checks if the GameState’s game is over
    # @param state The GameState object where it will be determined if the game is over
    def check_game(self, state):
        return state.isOver(state)


    # Purpose: checks the game tree for future states
    # @param game_tree, the class that defines a tree of future game states
    # @return tree_states, the final list of all possible states one layer down stemming from the given state
    def check_future(game_tree):
        return game_tree.tree_states(game_tree)


    # Purpose: initializes the move interface and handles entries
    # into it
    # @return entry, the player’s entry for a desired move
    def make_move_interface(self):
        master = Tk()
        tk.label(master, text='Please enter Move').grid(row=0)
        entry = tk.entry(master)
        entry.grid(row=0, column=1)
        mainloop()
        return entry


    # Purpose: runs the given move through the protocol to check if
    # valid move in given state and runs the move through the
    # protocol if valid
    # @param protocol, the protocol player’s actions must go through
    # @param state, the current state of the game
    # @param entry, the player’s entry into the interface that must be
    # checked to see if it’s a valid move or not
    def run_given_move(self, protocol, state, entry)
        if protocol.check_player_move(state, entry)
            protocol.move(state, entry)
        else:
            raise IndexError("Given move is invalid, try again!")
