from mySimpleGui import *
from random import *
from math import *
from threading import Thread


hi = 255
lo = 0.1
c = [width//2, height//2]
#co = [lo, lo, hi]
m = .3

switch = True


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
                self.drawThese.append((int(abs(x-width)), int(y), s, s, c))
                self.drawThese.append((int(x), int(abs(y-height)), s, s, c))
                self.drawThese.append((int(abs(x-width)), int(abs(y-height)), s, s, c))

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

dotFactoryObj = DotMaker(3, False)


showEvery = 15

compColors = ((22, 255, 236), (255, 193, 22), (255, 22, 146))
handPickedBlues = ((105, 255, 172), (68, 206, 252), (107, 66, 255), (133, 188, 255), (5, 255, 238))
bFlag = ((216, 9, 126), (140, 87, 156), (36, 70, 142), (140, 87, 156))
tFlag = ((91, 206, 250), (245, 169, 184), (255, 255, 255), (245, 169, 184), (91, 206, 250), (245, 169, 184), (255, 255, 255))
pFlag = ((255, 0, 24), (255, 165, 44), (255, 255, 65), (0, 128, 24), (0, 0, 249), (134, 0, 125))
lFlag = ((214, 41, 0), (255, 155, 85), (255, 255, 255), (212, 97, 166), (165, 0, 98))
mothersColor = ((0, 47, 255), (217, 41, 56))

myColors = CustomColorFade(bFlag, .2)

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
    tk.update()
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
