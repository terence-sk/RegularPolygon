# Original program
# http://codegolf.stackexchange.com/a/25945

# Only had these functions
# Set number of polygons
# Statically rotate
# Change radius
# -----------------------------------------
# Extended program
# msvonava@gmail.com

# Added functions such as
# Change width of line
# Change color of line
# Fill the shape
# Change color of fill
# Show lines leading to the center
# Rotate in certain intervals

import Tkinter as gui
import ttk as tgui
from math import pi, radians, sin, cos
import time

BOARD_WIDTH = 800
BOARD_HEIGHT = 400
POLYGON_TAG = 'shape'
DEFAULT_RADIUS = 200
DEFAULT_SIDES = 5
DEFAULT_OFFSET = 0
DEFAULT_WIDTH = 1
SPEED_FAST = 0.01
SPEED_MED = 0.03
SPEED_SLOW = 0.1

do_rotate = 0

"""
Arranges widget to a certain position and gives float value which is needed
by some methods in Tkinter
"""


class ConfigVar:
    def __init__(self, master, name, defaultval=0):
        self.var = gui.StringVar(value=defaultval)
        self.lbl = tgui.Label(master, text=name)
        self.fld = tgui.Entry(window, textvariable=self.var)

    def arrange(self, srow, scol):
        self.lbl.grid(row=srow, column=scol, sticky=gui.W)
        self.fld.grid(row=srow, column=scol+1, sticky=(gui.W, gui.E))

    def get_float_value(self, previous=0.0):
        try:
            return float(self.var.get())
        except ValueError:
            return previous


"""
radius sides offset line width line color fill color fill(true false)
"""


def draw_polygon(canvas, r, s, o, lw, lc, fc, fill):
    radius, sides, offset, lw = (i.get_float_value() for i in (r, s, o, lw))
    cx, cy = canvas.winfo_width()/2, canvas.winfo_height()/2

    step = 2*pi/sides
    offset = radians(offset)

    points = []

    for n in range(int(sides)):
        points.append((radius * cos(step * n + offset) + cx, radius * sin(step * n + offset) + cy))
        points.append((cx, cy))
    for n in range(int(sides)):
        points.append((radius * cos(step * n + offset) + cx, radius * sin(step * n + offset) + cy))

    canvas.delete(POLYGON_TAG)
    canvas.create_polygon(points, fill=(fc if fill else "white"), outline=lc, tags=POLYGON_TAG, width=lw)


def stop_rotate():
    global do_rotate
    do_rotate = 0


def rotate(speed):

    dbl_speed = 1.0

    if speed == "slow":
        dbl_speed = SPEED_SLOW
    elif speed == "medium":
        dbl_speed = SPEED_MED
    elif speed == "fast":
        dbl_speed = SPEED_FAST
    else:
        dbl_speed = 0.5

    global do_rotate
    do_rotate = 1
    # rotates until button is pressed
    while do_rotate == 1:
        for i in range(0, 359):
            if do_rotate == 0:
                return
            txt_offset.var.set(i)
            draw_polygon(board, txt_radius, txt_sides, txt_offset, txt_width,
                         str_line_color.get(), str_fill_color.get(), int_fill.get())
            board.update()
            time.sleep(dbl_speed)


"""
These next lines are just the GUI stuff
"""

root = gui.Tk()
root.title("N-uholnik")
window = tgui.Frame(root)
window.grid()

board = gui.Canvas(window, width=BOARD_WIDTH, height=BOARD_HEIGHT)

colors = ('red', 'blue', 'green', 'black')
speeds = ('slow', 'medium', 'fast')

var_color = colors[0]
var_speed = speeds[0]

str_line_color = gui.StringVar()
str_speed_rotate = gui.StringVar()
str_fill_color = gui.StringVar()
int_fill = gui.IntVar()

sb_line_color = gui.Spinbox(window, values=colors, textvariable=str_line_color, width=10)
sb_fill_color = gui.Spinbox(window, values=colors, textvariable=str_fill_color, width=10)
sb_speed = gui.Spinbox(window, values=speeds, textvariable=str_speed_rotate, width=10)

lbl_line_color = tgui.Label(window, text="Line color")
lbl_fill_color = tgui.Label(window, text="Fill color")

cb_fill = gui.Checkbutton(window, text="Fill", variable=int_fill)

txt_radius = ConfigVar(window, "Radius", DEFAULT_RADIUS)
txt_sides = ConfigVar(window, "Number of Sides", DEFAULT_SIDES)
txt_offset = ConfigVar(window, "Offset", DEFAULT_OFFSET)
txt_width = ConfigVar(window, "Width", DEFAULT_WIDTH)


btn_draw = tgui.Button(window, text="Draw",
                       command=lambda: draw_polygon(board, txt_radius, txt_sides, txt_offset, txt_width,
                                                    str_line_color.get(), str_fill_color.get(), int_fill.get()))

btn_rotate = tgui.Button(window, text="Rotate", command=lambda: rotate(str_speed_rotate.get()))

btn_stop_rotate = tgui.Button(window, text="Stop rotation", command=lambda: stop_rotate())

board.grid(row=1, column=1, columnspan=7, sticky=(gui.N, gui.E, gui.S, gui.W))

txt_radius.arrange(2, 1)
txt_sides.arrange(2, 3)
txt_offset.arrange(2, 5)
txt_width.arrange(3, 1)

btn_draw.grid(row=2, column=7)
btn_rotate.grid(row=3, column=7)
btn_stop_rotate.grid(row=4, column=7)
lbl_line_color.grid(row=3, column=3, sticky=gui.W)
lbl_fill_color.grid(row=3, column=5, sticky=gui.W)
sb_line_color.grid(row=3, column=4, sticky=(gui.W, gui.E))
sb_fill_color.grid(row=3, column=6, sticky=(gui.W, gui.E))
sb_speed.grid(row=4, column=6, sticky=(gui.W, gui.E))
cb_fill.grid(row=0, column=7, sticky=(gui.W, gui.E))

window.rowconfigure(1, weight=1)

for column in (2, 4, 6):
    window.columnconfigure(column, weight=1)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


root.mainloop()
