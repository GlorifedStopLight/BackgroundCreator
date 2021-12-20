from tkinter import *

width = 1366
height = 768

tk = Tk()
canvas = Canvas(tk, width=width, height=height, bg="white")

canvas.pack()


def rgb_to_hex(rgb):
    rgb = int(rgb[0]), int(rgb[1]), int(rgb[2])

    return '#%02x%02x%02x' % rgb

extraSpace = 3

def drawRect(x, y, w, h, c):
    canvas.create_oval(x, y, x+w+extraSpace, y+h+extraSpace, fill=rgb_to_hex(c), outline='')
    canvas.pack()
