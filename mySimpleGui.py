from tkinter import *


width = 1366
height = 768

tk = Tk()
canvas = Canvas(tk, width=width, height=height, bg="white")
tk.attributes('-fullscreen', True)

canvas.pack()


def rgb_to_hex(rgb):
    rgb = int(rgb[0]), int(rgb[1]), int(rgb[2])

    return '#%02x%02x%02x' % rgb


def drawRect(x, y, w, h, c):
    canvas.create_oval(x, y, x+w*2, y+h*2, fill=rgb_to_hex(c), outline='')
    canvas.pack()
