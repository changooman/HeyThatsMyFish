import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from Fish.Common.board import Board
from Fish.Common.board_player import BoardPlayer
from Fish.Common.state import State

class FishWindow(Gtk.Window):
    def __init__(self, width, height):
        super(FishWindow, self).__init__()
        self.width, self.height = width, height

        self.set_resizable(False)
        self.init_ui()

        self.board = Board(4, 3, [(1, 0), (2, 2)])
        self.state = State([BoardPlayer("red"), BoardPlayer("brown"), BoardPlayer("black"), BoardPlayer("white")], self.board)
        self.state.place_avatar((0, 0), "red")
        self.state.place_avatar((2, 1), "brown")
        self.state.place_avatar((1, 2), "black")
        self.state.place_avatar((3, 2), "white")


    def init_ui(self):
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)

        self.set_title("Fish")
        self.set_default_size(self.width, self.height)

        self.connect("destroy", Gtk.main_quit)


    def on_draw(self, da, ctx):
        self.state.draw(ctx)


win = FishWindow(750, 350)
win.show_all()
Gtk.main()
