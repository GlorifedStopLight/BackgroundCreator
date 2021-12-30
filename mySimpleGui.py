from tkinter import *
from random import *


def testing(event):
    print("pressed Escape")

    # overlay is on
    if overlayItems[0].pack:

        # turn all the items in the overlay off
        for item in overlayItems:
            item.pack_forget()

    # overlay is off
    else:

        # turn all the items in the overlay on
        for item in overlayItems:
            item.pack()


def rgb_to_hex(rgb):
    rgb = int(rgb[0]), int(rgb[1]), int(rgb[2])

    return '#%02x%02x%02x' % rgb


def drawRect(x, y, w, h, c):

    if 0 <= x <= width and 0 <= y <= height:

        # spot is empty
        if circleMatrix[x][y] is None:

            # add new circle to our matrix
            circleMatrix[x][y] = canvas.create_oval(x-w, y-h, x+w, y+h, fill=rgb_to_hex(c), outline='')

            canvas.pack()

        # trying to put a circle over an old circle
        else:

            # delete old circle
            canvas.delete(circleMatrix[x][y])

            # add new circle to our matrix
            circleMatrix[x][y] = canvas.create_oval(x - w, y - h, x + w, y + h, fill=rgb_to_hex(c), outline='')
            canvas.pack()


userPickedSeed = input("input a seed leave blank for random seed: ")

if userPickedSeed == "":
    userPickedSeed = randint(0, 99999999)
    print(userPickedSeed)
else:
    userPickedSeed = int(userPickedSeed)

seed(userPickedSeed)

width = 1366
height = 768

s = 5

circleMatrix = []
for i in range(width + 1):
    tempList = []
    for j in range(height + 1):
        tempList.append(None)

    circleMatrix.append(tempList.copy())


tk = Tk()
canvas = Canvas(tk, width=width, height=height, bg="white")
tk.attributes('-fullscreen', True)

tk.bind("<Escape>", testing)

overlayItems = []

overlayItems.append(Label(tk, text=str(userPickedSeed)))
canvas.pack()


