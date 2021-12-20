from mySimpleGui import *
from random import *
from math import *

hi = 240
lo = 100
c = [width//2, height//2]
co = [hi, lo, lo]
m = .3
f = [400, 400]


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


class DotMaker:

    def __init__(self, splitReflections):
        radianAmount = 2*pi / splitReflections
        self.cosine = cos(radianAmount)
        self.sine = sin(radianAmount)
        self.splitReflections = splitReflections
        self.center = (width//2, height//2)

    def dot(self, cords, c):
        x = cords[0]
        y = cords[1]

        for i in range(self.splitReflections):
            drawRect(int(x), int(y), s, s, c)
            x, y = ((x - self.center[0]) * self.cosine - (y - self.center[1]) * self.sine + self.center[0]),\
                   ((x - self.center[0]) * self.sine + (y - self.center[1]) * self.cosine + self.center[1])



s = 9
col = [lo, lo, hi]

dotFactoryObj = DotMaker(5)

while True:
    tk.update()

    dotFactoryObj.dot(c, co)
    dotFactoryObj.dot(f, col)

    co = rainbow(co)
    #co = changeColorRandom(co)

    col = rainbow(col)
    v = choice((-s, 0, s))
    w = choice((-s, 0, s))
    if not not v:
        c[0] = c[0] + v
    else:
        c[1] = c[1] + choice((-s, s))

    if not not w:
        f[0] = f[0] + v
    else:
        f[1] = f[1] + choice((-s, s))

