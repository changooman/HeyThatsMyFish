from Tkinter import Tk, Canvas
import sys


def drawhexagon(size):
    #test to  make sure size is an integer
    try:
        size = int(size)
    except:
        print('usage: ./xgui Enter a positive-integer')
        return
 
    #test to make sure size is positive
    if size < 1:
        print('usage: ./xgui Enter a positive-integer')
        return

    #defines the window
    window = Tk()
    can = Canvas(window, width=1920, height=1080)

    #if the window is clicked the window will close
    def clicked(*args):
        window.destroy()

    #determines the size of the hexagon based on size variable
    points = [
        560 + (size/2), 533 - size,
        540 - (size/2), 533 - size,
        530 - size, 550,
        540 - (size/2), 567 + size,
        560 + (size/2), 567 + size,
        570 + size, 550

    ]
    hexagon = can.create_polygon(points, fill="red", tags="hexagon")

    can.tag_bind("hexagon", "<Button-1>", clicked)

    can.pack()

    window.mainloop()


def main():
    # defining userinput
    userinput = sys.argv
    userinput.pop(0)
    try:
        drawhexagon(userinput[0])
    except:
        print('usage: ./xgui positive-integer')
        return


main()
