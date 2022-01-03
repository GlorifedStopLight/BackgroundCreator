import tkinter as tk
from random import *


def testing(event):
    global overlayOn, canvas
    print("pressed Escape")

    if overlayOn:

        canvas.pack_forget()
        canvas2.pack()
        overlayOn = False
        print("forgot")

    else:

        canvas.pack()
        canvas2.pack_forget()
        overlayOn = True

    win.update()


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

# 1366
width = 1366

# 768
height = 768

s = 4

circleMatrix = []
for i in range(width + 1):
    tempList = []
    for j in range(height + 1):
        tempList.append(None)

    circleMatrix.append(tempList.copy())


win = tk.Tk()

# create and show the frame
frame = tk.Frame(win, width=width, height=height)
frame.pack(expand=True, fill=tk.BOTH) #.grid(row=0,column=0)

# create a canvas for the frame
canvas = tk.Canvas(master=frame, bg='#FFFFFF', width=width, height=height, scrollregion=(0, 0, 500, 500))
canvas2 = tk.Canvas(master=frame, bg='#000000')
"""
# create horizontal and vertical scroll bars
hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)

# show these scroll bars
hbar.pack(side=tk.BOTTOM, fill=tk.X)
vbar.pack(side=tk.RIGHT, fill=tk.Y)

# configure the scroll bars to move the canvas left right up and down
hbar.config(command=canvas.xview)
vbar.config(command=canvas.yview)

# do the same to canvas
canvas.config(width=width, height=height)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

# show canvas in frame
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

win.attributes('-fullscreen', True)
"""
win.bind("<Escape>", testing)
canvas2.pack()
canvas.pack()

#lab = Label(canvas, text=str(userPickedSeed))
#lab.pack()

overlayOn = False

