#!/usr/bin/python

from Fish.Admin.referee import Referee
from Fish.Player.player import Player
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State

import sys

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

DEPTH = 1
WINDOW_WIDTH = 1150
WINDOW_HEIGHT = 450
BUTTON_SIZE = 50
BUTTON_X = 0
BUTTON_Y = 400
TEXT_VIEW_WIDTH = 1000
TEXT_VIEW_HEIGHT = 50
TEXT_VIEW_X = 120
TEXT_VIEW_Y = 400
DRAWING_AREA_WIDTH = 1150
DRAWING_AREA_HEIGHT = 400
DRAWING_AREA_X = 0
DRAWING_AREA_Y = 0
TITLE = "xgui"
DRAW_EVENT = "draw"
CLICKED_EVENT = "clicked"
DESTROY_EVENT = "destroy"

RUN_NEXT_TURN_MSG = "Run next turn"
RUNNING_TURN_MSG = "Running turn..."
GAME_OVER_MSG = "Game over.\nClick to close"

class GameVisualizerWindow(Gtk.Window):
    """Class to represent a game visualizer. This visualizer allows a user to
    visualize the state of the game at each turn in the game. The visualizer also
    displays the scores at each state. Once the game is finished, the user can view the
    final game state before closing the window.
    
    referee (Referee): the referee used to run the game.
    darea (Gtk.DrawingArea): the drawing area used to display the state of the game in the user
    interface
    scores (Gtk.TextView): the text view used to display the scores of each player. The text in this text
    view is updated every time a turn is taken in the game.
    player_color_order (list): a list of strings representing the order of the players, represented by their color.
    This list is not mutated and is used as a reference for getting scores in the turn order of the players.
    """

    def __init__(self, referee):
        """Initialize an instance of the game visualizer. Store the referee to use to run the game.
        Additionally, the initial order of players is stored.

        referee (Referee): the referee to use to run the game.
        """
        super(GameVisualizerWindow, self).__init__()
        self.referee = referee
        self.darea = None # set in init_ui()
        self.scores = None # set in init_ui()
        self.player_color_order = [player.get_color() for player in referee.get_current_state().get_players()]
        self.init_ui()

    def init_ui(self):
        """Initialize and configure the user interface. This involves setting up the drawing area,
        the button to do turns, and a text view to display scores, as well as setting up callbacks.
        Configurations such as widget sizes and labels are also set here.
        """
        self.set_title(TITLE)
        self.set_default_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_resizable(False)

        fixed = Gtk.Fixed()
        self.add(fixed)

        darea = Gtk.DrawingArea()
        darea.connect(DRAW_EVENT, self.on_draw)
        darea.set_size_request(DRAWING_AREA_WIDTH, DRAWING_AREA_HEIGHT)
        self.darea = darea
        fixed.put(darea, DRAWING_AREA_X, DRAWING_AREA_Y)

        button = Gtk.Button.new_with_label(RUN_NEXT_TURN_MSG)
        button.connect(CLICKED_EVENT, self.on_next_turn_click)
        button.set_size_request(BUTTON_SIZE, BUTTON_SIZE)
        fixed.put(button, BUTTON_X, BUTTON_Y)

        scores = Gtk.TextView()
        scores.get_buffer().set_text(self.get_current_scores_buffer())
        scores.set_size_request(TEXT_VIEW_WIDTH, TEXT_VIEW_HEIGHT)
        self.scores = scores
        fixed.put(scores, TEXT_VIEW_X, TEXT_VIEW_Y)

        self.connect(DESTROY_EVENT, Gtk.main_quit)

    def get_scores_in_order_of_players(self):
        """Return a list of scores representing the scores of the players,
        in the order of player's turns.

        returns: (list) a list of integers representing the scores of the players,
        in turn order.
        """
        
        players = self.referee.get_current_state().get_players()

        player_scores = []
        for player_color in self.player_color_order:
            for player in players:
                if player_color == player.get_color():
                    player_scores.append(player.get_score())
                    break

        return player_scores

    def get_current_scores_buffer(self):
        """Get a string representation of all the players current scores.
        The players are listed in turn order (meaning it does not start at
        the player whose turn it is currently, but starts at the first player
        who placed a penguin.)

        returns: (str) A formatted string listing all the player scores in
        turn order.
        """

        player_scores = self.get_scores_in_order_of_players()
        score_string = "Scores:\n"

        for color, score in zip(self.player_color_order, player_scores):
            player_score = "{}: {}".format(color, score)
            score_string += player_score
            score_string += "\t"

        return score_string
        

    def on_draw(self, da, ctx):
        """Callback to render the game state in this window.

        da: The GTK DrawingArea (unused in this function)
        ctx: The Cairo context to draw to.
        """
        self.referee.get_current_state().draw(ctx)

    def do_next_turn(self, button):
        """Helper function to perform a turn when a button is clicked. This function
        makes the referee run the next turn of the game. This function also updates
        the labels of the button that was pressed to tell the user if a round is
        currently being ran or not. This function also sets the new scores in the
        scores box after the turn is taken.

        button: the GTK button widget that used this callback.
        """
        button.set_label(RUNNING_TURN_MSG)
        self.referee.run_turn()
        self.scores.get_buffer().set_text(self.get_current_scores_buffer())
        button.set_label(RUN_NEXT_TURN_MSG)
        self.darea.queue_draw()

    def on_next_turn_click(self, button):
        """Callback function that runs when a button is clicked. This function will
        run the next turn of the game if the game is not over, or will shut down the
        program if the game is over. This function will also update the button label
        to display the game is over or not.

        button: the GTK button widget that used this callback.
        """
        if self.referee.is_game_over():
            Gtk.main_quit()
        else:
            self.do_next_turn(button)
            # if the game is over after this turn, we will shutdown on the next click,
            # so visually alert the player with the button label
            if self.referee.is_game_over():
                button.set_label(GAME_OVER_MSG)

def get_player_list(num_players):
    """Create a list of players with size num_players. The colors
    of each player are in the order defined in BoardPlayer.POSSIBLE_COLORS.
    Each player has a depth of 1.
    
    num_players (int): the number of players to add to the list
    INVARIANT: num_players should be between 2 and 4, inclusive.
    
    returns: (list): a list of players in turn order.
    """
    
    colors = BoardPlayer.POSSIBLE_COLORS

    player_list = []
    for i in range(num_players):
        player_list.append(Player(colors[i], DEPTH))

    return player_list

def parse_num_players(num_players):
    """Parse a string representing the number of players and convert it to an integer
    representing the number of players to use. The string must be numeric and must be
    between 2 and 4, inclusive, otherwise None is returned

    num_players (str): a string containing a single number representing the
    number of players to use in the game. Must be between 2 and 4, inclusive.

    returns: (int) the number of players, as an integer
    """
    
    try:
	num_players = int(num_players)
    except ValueError:
	return None
    if num_players < 2 or num_players > 4:
        return None

    return num_players

def run_visualizer(num_players):
    """Run the visualizer with the given number of players.

    num_players (str): a string containing a single number representing the
    number of players to use in the game. Must be between 2 and 4, inclusive.
    Otherwise, a ValueError is raised.
    """

    num_players = parse_num_players(num_players)
    if num_players is None:
        raise ValueError("Invalid player count given.")

    players = get_player_list(num_players)
    ref = Referee(players, (5, 5), timeout=600)

    win = GameVisualizerWindow(ref)
    win.show_all()
    Gtk.main()
