import tkinter as tk
from random import *
from math import *
from threading import Thread
#from playsound import playsound


def testing(event):
    global overlayOn, canvas
    print("pressed Escape")

    if overlayOn:

        frame.pack_forget()
        overlayFrame.pack()
        #testTextBox.pack()
        overlayOn = False
        print("forgot")

    else:

        frame.pack()
        #testTextBox.pack_forget()
        overlayFrame.pack_forget()

        overlayOn = True




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
frame.pack(expand=True, fill=tk.BOTH)

# create a canvas for the frame
canvas = tk.Canvas(master=frame, bg='#FFFFFF', width=width, height=height, scrollregion=(0, 0, 500, 500))
overlayFrame = tk.Frame(master=win, bg='#000000', width=width, height=height)
overlayFrame.pack()

testTextBox = tk.Text(master=overlayFrame, height=1, width=10, bg="#FF00FF")
testTextBox.pack()

overlayFrame.pack_forget()
canvas.pack()

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


#testTextBox.pack_forget()



#lab = Label(canvas, text=str(userPickedSeed))
#lab.pack()

overlayOn = True



hi = 255
lo = 0.1
c = [width//2, height//2]
#co = [lo, lo, hi]
m = .3


def blackAndWhite(c):
    global switch
    c = list(c)

    if switch:

        if c[0] + m < hi:
            c[0], c[1], c[2] = c[0] + m, c[1] + m, c[2] + m
        elif c[0] - m > lo:
            c[0], c[1], c[2] = c[0] - m, c[1] - m, c[2] - m
            switch = False
    else:

        if c[0] - m > lo:
            c[0], c[1], c[2] = c[0] - m, c[1] - m, c[2] - m
        elif c[0] + m < hi:
            c[0], c[1], c[2] = c[0] + m, c[1] + m, c[2] + m
            switch = True


    return c


def rainbow(c):
    if c[2] <= lo < c[0] and c[1] >= hi:
        c[0] -= m

    elif c[0] <= lo < c[1] and c[2] >= hi:
        c[1] -= m

    elif c[1] <= lo and c[2] >= hi > c[0]:
        c[0] += m

    elif c[2] <= lo and c[0] >= hi > c[1]:
        c[1] += m

    elif c[1] <= lo < c[2] and c[0] >= hi:
        c[2] -= m

    elif c[0] <= lo and c[1] >= hi > c[2]:
        c[2] += m

    return c


def changeColorRandom(c):
    c = list(c)
    if c[0] + 10 < hi:
        c[0] += randint(0, 10)
    if c[0] - 10 > lo:
        c[0] += randint(-10, 0)

    if c[1] + 10 < hi:
        c[1] += randint(0, 10)
    if c[1] - 10 > lo:
        c[1] += randint(-10, 0)

    if c[2] + 10 < hi:
        c[2] += randint(0, 10)
    if c[2] - 10 > lo:
        c[2] += randint(-10, 0)

    return c


def normal_round(n):
    if n - floor(n) < 0.5:
        return floor(n)
    return ceil(n)


def changeCordsThread():

    c[0] = abs(abs(c[0] + choice((-s, s)) - width) - width)
    c[1] = abs(abs(c[1] + choice((-s, s)) - height) - height)


class DotMaker:

    def __init__(self, splitReflections, isMirrored):

        if isMirrored:
            radianAmount = 2*pi / splitReflections / 2
        else:
            radianAmount = 2 * pi / splitReflections

        self.cosine = cos(radianAmount)
        self.sine = sin(radianAmount)
        self.splitReflections = splitReflections
        self.center = (width//2, height//2)
        self.isMirrored = isMirrored
        self.drawThese = []

    def getDotCreationInfo(self, cords, c):
        x = cords[0]
        y = cords[1]

        self.drawThese = []

        for i in range(self.splitReflections):

            self.drawThese.append((int(x), int(y), s, s, c))
            if self.isMirrored:
                self.drawThese.append((int(-x+width), int(y), s, s, c))
                self.drawThese.append((int(x), int(-y+height), s, s, c))
                self.drawThese.append((int(-x+width), int(-y+height), s, s, c))

            x, y = ((x - self.center[0]) * self.cosine - (y - self.center[1]) * self.sine + self.center[0]),\
                   ((x - self.center[0]) * self.sine + (y - self.center[1]) * self.cosine + self.center[1])

    def createDot(self):

        # loop through all the given dots to draw
        for dotInfo in self.drawThese:

            # draw dot
            drawRect(*dotInfo)


# a class t
class CustomColorFade:
    def __init__(self, colorsToFadeTo, fadeSpeed):

        # a list of colors that the user wants to fade to (in order)
        self.colorsToFadeTo = colorsToFadeTo

        # the current color starts at the first color in the list
        self.currentColor = list(colorsToFadeTo[0])

        # the last specific color that we faded from (given by user)
        self.previousColor = colorsToFadeTo[0]

        # the index of the color from our list that we are going to
        self.fadeToColorIndex = 1

        # the color that we are fading to
        self.nextColor = colorsToFadeTo[1]

        # how fast we fade from one color to the next
        self.fadeSpeed = fadeSpeed

        i = fadeSpeed
        while i < 1:
            i += fadeSpeed

        self.newColorGracePeriod = i

        self.currentGrace = 0

        self.feedGrace = True

    # returns the next color to fade properly
    def getNextColor(self):

        # add to current grace
        if self.feedGrace:
            self.currentGrace += self.fadeSpeed
            if self.newColorGracePeriod <= self.currentGrace:
                self.feedGrace = False

        # have arrived at the desired color
        if [normal_round(self.currentColor[0]), normal_round(self.currentColor[1]), normal_round(self.currentColor[2])] == list(self.nextColor) and\
                self.newColorGracePeriod <= self.currentGrace:

            self.currentGrace = 0
            self.feedGrace = True

            # last color in the list start from the beginning
            if self.fadeToColorIndex + 1 == len(self.colorsToFadeTo):
                self.fadeToColorIndex = 0

            else:
                self.fadeToColorIndex += 1

            self.currentColor = list(self.nextColor)
            self.previousColor = self.nextColor
            self.nextColor = self.colorsToFadeTo[self.fadeToColorIndex]

        # change red green and blue
        for i in range(3):

            # subtract
            if self.previousColor[i] > self.nextColor[i]:

                # not done subtracting
                if self.currentColor[i] - self.fadeSpeed >= self.nextColor[i]:
                    self.currentColor[i] -= self.fadeSpeed

            # add
            else:

                # not done adding
                if self.currentColor[i] + self.fadeSpeed <= self.nextColor[i]:
                    self.currentColor[i] += self.fadeSpeed

        # return the updated current color
        return self.currentColor


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


col = [lo, lo, hi]

dotFactoryObj = DotMaker(4, True)


showEvery = 100

compColors = ((22, 255, 236), (255, 193, 22), (255, 22, 146))
handPickedBlues = ((105, 255, 172), (52, 206, 68), (107, 66, 255), (133, 188, 255), (5, 255, 238))

bFlag = ((216, 9, 126), (140, 87, 156), (36, 70, 142), (140, 87, 156))
tFlag = ((91, 206, 250), (245, 169, 184), (255, 255, 255), (245, 169, 184), (91, 206, 250), (245, 169, 184), (255, 255, 255))
pFlag = ((255, 0, 24), (255, 165, 44), (255, 255, 65), (0, 128, 24), (0, 0, 249), (134, 0, 125))
lFlag = ((214, 41, 0), (255, 155, 85), (255, 255, 255), (212, 97, 166), (165, 0, 98))
mothersColor = ((0, 47, 255), (217, 41, 56))
greens = ((32,178,170), (0,255,127), (85,107,47), (60,179,113), (107,142,35))
sunflower = ((101, 67, 33), (255,255,0))
redWhiteAndBlack = ((255, 0, 0), (0, 0, 0), (255, 0, 0), (255, 255, 255))
caleb = ((80, 50, 0), (10, 255, 20), (0, 0, 0))
dog = ((138, 97, 225), (0, 155, 255))
ResshasNumbers = ((3, 198, 252), (247, 221, 17), (81, 10, 247))


myColors = CustomColorFade(ResshasNumbers, .09)

getColorThread = ThreadWithReturnValue(target=myColors.getNextColor)
getColorThread.start()
co = getColorThread.join()

doDotThread = ThreadWithReturnValue(target=dotFactoryObj.getDotCreationInfo, args=(c, co))
doDotThread.start()
doDotThread.join()

cordsThread = ThreadWithReturnValue(target=changeCordsThread)
cordsThread.start()
cordsThread.join()

while True:
    win.update()
    if overlayOn:

        for i in range(showEvery):

            getColorThread = ThreadWithReturnValue(target=myColors.getNextColor)

            getColorThread.start()

            doDotThread = ThreadWithReturnValue(target=dotFactoryObj.getDotCreationInfo, args=(c, co))
            doDotThread.start()

            cordsThread = ThreadWithReturnValue(target=changeCordsThread)
            cordsThread.start()

            dotFactoryObj.createDot()

            # join all threads
            doDotThread.join()
            co = getColorThread.join()
            cordsThread.join()
