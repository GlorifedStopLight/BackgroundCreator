import tkinter as tk
from random import *
from math import *
from threading import Thread
import json
from tkinter.colorchooser import askcolor
from tkinter import ttk
import time
from tkinter import messagebox
import multiprocessing as mp
from tkinter import colorchooser


def normal_round(n):
    if n - floor(n) < 0.5:
        return floor(n)
    return ceil(n)


class DotMaker:

    def __init__(self, splitReflections, isMirrored, colorsToFadeTo, fadeSpeed, followThisDot=None, startLocation=None):

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
        self.followThisDot = followThisDot

        if startLocation is None:
            self.cords = [width//2, height//2]
        else:
            self.cords = startLocation


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

    def getDotCreationInfo(self):
        x = self.cords[0]
        y = self.cords[1]

        self.drawThese = []

        for i in range(self.splitReflections):

            self.drawThese.append((int(x), int(y), s, s, self.currentColor))
            if self.isMirrored:
                self.drawThese.append((int(-x+width), int(y), s, s, self.currentColor))
                self.drawThese.append((int(x), int(-y+height), s, s, self.currentColor))
                self.drawThese.append((int(-x+width), int(-y+height), s, s, self.currentColor))

            x, y = ((x - self.center[0]) * self.cosine - (y - self.center[1]) * self.sine + self.center[0]),\
                   ((x - self.center[0]) * self.sine + (y - self.center[1]) * self.cosine + self.center[1])

    def createDot(self):

        # loop through all the given dots to draw
        for dotInfo in self.drawThese:

            # draw dot
            drawRect(*dotInfo)

    def changeCordsThread(self):
        self.cords[0] = abs(abs(self.cords[0] + choice((-s, s)) - width) - width)
        self.cords[1] = abs(abs(self.cords[1] + choice((-s, s)) - height) - height)

    # doesn't return anything just calculates the next color
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


class ControlAll:
    def __init__(self, colorSelection, colorSpeed, branchNumber, isBranchesMirrored, startLocation=None):
        self.dotFactoryObj = DotMaker(branchNumber, isBranchesMirrored, colorSelection, colorSpeed, startLocation=startLocation)
        toggleOverlay(None)

    def updateAllThings(self):

        getColorThread = Thread(target=self.dotFactoryObj.getNextColor)
        doDotThread = Thread(target=self.dotFactoryObj.getDotCreationInfo)
        cordsThread = Thread(target=self.dotFactoryObj.changeCordsThread)

        getColorThread.start()
        doDotThread.start()
        cordsThread.start()

        #getColorThread = mp.Process(target=self.myColors.getNextColor)
        #getColorThread.start()

        # join all threads
        #getColorThread.join()
        #doDotThread.join()
        #cordsThread.join()

        self.dotFactoryObj.createDot()
        # 0.0041-0.025 (with threading)


class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.itemconfig(i+1, {"bg": x, "selectbackground": x})
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.itemconfig(i - 1, {"bg": x, "selectbackground": x})
            self.curIndex = i


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def saveUserGivenSeed():

    if seedNameInput.get() == "" or entry_seedInput.get() == "":
        return

    with open("mySavedData.json") as outfile:

        # load all of the current presets
        info = json.load(outfile)

        # add another seed
        info["savedSeeds"][seedNameInput.get()] = entry_seedInput.get()

        json_object = json.dumps(info, indent=4)

    # Writing to sample.json
    with open("mySavedData.json", "w") as outfile:

        outfile.write(json_object)


def addColorToColorPallet():
    selectedColor = askcolor(title="Tkinter Color Chooser")
    rgbValue = (floor(selectedColor[0][0]), floor(selectedColor[0][1]), floor(selectedColor[0][2]))
    listbox_colorPallet.insert("end", rgbValue)
    listbox_colorPallet.itemconfig("end", {"bg": selectedColor[1], "selectbackground": selectedColor[1], "fg": selectedColor[1]})


def removeSelectedColorFromColorPallet():
    listbox_colorPallet.delete(listbox_colorPallet.curselection())


def saveColorPreset():
    global drop_colorPresets

    if entry_colorPresetName.get() == "":
        print("no given name for preset")
        return

    with open("mySavedData.json") as outfile:

        # load all of the current presets
        info = json.load(outfile)

        # initialize the list for colors
        presetColors = []

        # loop through each line in listbox
        for i in range(listbox_colorPallet.size()):

            # add the name to the list (the name is a color)
            presetColors.append(hex_to_rgb(listbox_colorPallet.get(i)))

        # create a new color preset
        info["savedColors"][entry_colorPresetName.get()] = presetColors

        # create a json object
        json_object = json.dumps(info, indent=4)

    # Writing to sample.json
    with open("mySavedData.json", "w") as outfile:

        outfile.write(json_object)

    menu = drop_colorPresets["menu"]
    menu.delete(0, "end")
    for string in getColorPresetNames():
        menu.add_command(label=string,
                         command=lambda value=string: dropSelected_colorPalletPresets.set(value))


# returns a list of strings which are the names of saved color presets
def getColorPresetNames():

    # open json file (contains saved information)
    with open("mySavedData.json") as outfile:

        # convert the json file into a python object
        allSavedData = json.load(outfile)

        # get all the names of the color presets
        allColorPresetNames = list(allSavedData["savedColors"].keys())

        return allColorPresetNames


def loadColorPreset(event):

    # open save data
    with open("mySavedData.json") as outfile:

        # convert save data into a python object
        saveData = json.load(outfile)

        # get the currently selected preset name
        colorPresetName = dropSelected_colorPalletPresets.get()

        try:
            # get the array of colors from data using colorPresetName
            loadedColors = saveData["savedColors"][colorPresetName]

        # preset name doesn't exist
        except KeyError:

            # give up
            return

        # go through each line and remove it
        for i in range(listbox_colorPallet.size()):
            listbox_colorPallet.delete(0)

        # add each color to our listbox of colors
        for color in loadedColors:

            listbox_colorPallet.insert("end", color)
            listbox_colorPallet.itemconfig("end", {"bg": rgb_to_hex(color), "selectbackground": rgb_to_hex(color)})


def getPresetColors(presetName):

    # open json file
    with open("mySavedData.json") as outfile:

        # load saved data as python object
        allData = json.load(outfile)

        # return colors
        return allData["savedColors"][presetName]


def getCurrentColorPalletColors():
    currentColors = []

    for i in range(listbox_colorPallet.size()):
        currentColors.append(listbox_colorPallet.get(i))

    return currentColors


def toggleOverlay(event):
    global overlayOn

    if overlayOn:

        overlayFrame.grid_forget()
        frame.grid(row=0, column=0)

        overlayOn = False

    else:
        frame.grid_forget()
        overlayFrame.grid(row=0, column=0)

        overlayOn = True


def rgb_to_hex(rgb):
    rgb = int(rgb[0]), int(rgb[1]), int(rgb[2])

    return '#%02x%02x%02x' % rgb


def drawRect(x, y, w, h, c):

    if 0 <= y <= height and 0 <= x <= width:

        # spot is empty
        if circleMatrix[x][y] is None:

            # add new circle to our matrix
            circleMatrix[x][y] = canvas_mandala.create_oval(x - w, y - h, x + w, y + h, fill=rgb_to_hex(c), outline='')

        # trying to put a circle over an old circle
        else:

            # delete old circle
            canvas_mandala.delete(circleMatrix[x][y])

            # add new circle to our matrix
            circleMatrix[x][y] = canvas_mandala.create_oval(x - w, y - h, x + w, y + h, fill=rgb_to_hex(c), outline='')


def deleteColorPreset():

    presetName = dropSelected_colorPalletPresets.get()
    x = messagebox.askquestion("Warning", "are you sure you would like \n to delete " + presetName + "?")

    if x == "yes":

        with open("mySavedData.json") as outfile:
            savedData = json.load(outfile)

            del savedData["savedColors"][presetName]

        with open("mySavedData.json", "w") as outfile:

            json_object = json.dumps(savedData, indent=4)
            outfile.write(json_object)
    """
    options = list(drop_colorPresets['values'])
    options.remove(presetName)
    drop_colorPresets['values'] = options
    """


#
class myApp:
    def __init__(self):
        seed(entry_seedInput.get())
        self.myControl = ControlAll(getCurrentColorPalletColors(), .5, 3, True)
        #self.myControl2 = ControlAll(getCurrentColors(), .5, 1, True, [0, 0])

        myThreadCool = Thread(target=self.generationLoop)
        myThreadCool.start()

    def generationLoop(self):
        while True:
            self.myControl.updateAllThings()
            #self.myControl2.updateAllThings()

# 1366
width = 1366

# 768
height = 768

s = 5

circleMatrix = []
for i in range(width + 1):
    tempList = []
    for j in range(height + 1):
        tempList.append(None)

    circleMatrix.append(tempList.copy())

# pick a random seed
randomSeed = randint(0, 1000000000)

win = tk.Tk()
overlayFrame = tk.Frame(master=win, bd=30)
overlayFrame.grid(row=0, column=0)

# list of colors
listbox_colorPallet = DragDropListbox(master=win)
listbox_colorPallet.grid(row=7, column=0)
listbox_colorPallet.config(selectborderwidth=5, relief=tk.SUNKEN, exportselection=False, activestyle=tk.UNDERLINE, width=15, height=9)

# gets the desired seed to save
entry_seedInput = tk.Entry(master=overlayFrame, width=30, bg="#d1d1d1", bd=5)
entry_seedInput.grid(row=2, column=0)
entry_seedInput.insert(0, str(randomSeed))

#
#seedInputLabel = tk.Label(master=overlayFrame, text="input your seed below")
#seedInputLabel.grid(row=1, column=0)

# gets the name for the seed
seedNameInput = tk.Entry(master=overlayFrame, width=30, bg="#d1d1d1", bd=5)
seedNameInput.grid(row=4, column=0)
seedNameInput.insert(0, "input your seed name here")

#
#seedNameInputLabel = tk.Label(master=overlayFrame, text="input your seed name below")
#seedNameInputLabel.grid(row=3, column=0)

# save seed
butt_saveSeed = tk.Button(master=overlayFrame, text="Save Seed", command=saveUserGivenSeed)
butt_saveSeed.grid(row=0, column=0)

# add color
butt_chooseColor = tk.Button(master=overlayFrame, text="choose color", command=addColorToColorPallet)
butt_chooseColor.grid(row=5, column=2)

# button to remove color
butt_removeColor = tk.Button(master=overlayFrame, text="Remove Selected Color", command=removeSelectedColorFromColorPallet)
butt_removeColor.grid(row=7, column=2)

# gets the name for the seed
entry_colorPresetName = tk.Entry(master=overlayFrame, width=50)
entry_colorPresetName.grid(row=3, column=3)

# save the colors you've chosen in a json file
butt_saveColorPreset = tk.Button(master=overlayFrame, text="save color preset", command=saveColorPreset)
butt_saveColorPreset.grid(row=5, column=0)

# button to delete the selected color preset
butt_deleteColorPreset = tk.Button(master=overlayFrame, text="delete color preset", command=deleteColorPreset)
butt_deleteColorPreset.grid(row=6, column=0)

# datatype of menu text
dropSelected_colorPalletPresets = tk.StringVar()

# initial menu text
dropSelected_colorPalletPresets.set("--select a preset--")

drop_colorPresets = ttk.OptionMenu(overlayFrame, dropSelected_colorPalletPresets, "--select a preset--", *getColorPresetNames(), command=loadColorPreset)
drop_colorPresets.grid(row=70, column=1)

# generates a mandala
butt_startGeneration = tk.Button(master=overlayFrame, command=myApp, text="start generation")
butt_startGeneration.grid(row=10, column=0)

# create and show the frame
frame = tk.Frame(win, width=width, height=height)

# create a canvas for the frame
canvas_mandala = tk.Canvas(master=frame, bg='#FFFFFF', width=width, height=height, scrollregion=(0, 0, 500, 500))
canvas_mandala.pack()

# create horizontal and vertical scroll bars
hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)

# show these scroll bars
hbar.pack(side=tk.BOTTOM, fill=tk.X)
vbar.pack(side=tk.RIGHT, fill=tk.Y)

# configure the scroll bars to move the canvas left right up and down
hbar.config(command=canvas_mandala.xview)
vbar.config(command=canvas_mandala.yview)

# do the same to canvas
canvas_mandala.config(width=width, height=height)
canvas_mandala.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

# show canvas in frame
canvas_mandala.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

showEvery = 100

overlayOn = True

win.bind("<Escape>", toggleOverlay)
win.attributes('-fullscreen', True)

hi = 255
lo = 0.1
m = .3

compColors = ((22, 255, 236), (255, 193, 22), (255, 22, 146))
handPickedBlues = ((105, 255, 172), (52, 206, 68), (107, 66, 255), (133, 188, 255), (5, 255, 238))

bFlag = ((216, 9, 126), (140, 87, 156), (36, 70, 142), (140, 87, 156))
tFlag = ((91, 206, 250), (245, 169, 184), (255, 255, 255), (245, 169, 184), (91, 206, 250), (245, 169, 184), (255, 255, 255))
pFlag = ((255, 0, 24), (255, 165, 44), (255, 255, 65), (0, 128, 24), (0, 0, 249), (134, 0, 125))
lFlag = ((214, 41, 0), (255, 155, 85), (255, 255, 255), (212, 97, 166), (165, 0, 98))
mothersColor = ((0, 47, 255), (217, 41, 56))
greens = ((32, 178, 170), (0, 255, 127), (85, 107, 47), (60, 179, 113), (107, 142, 35))
sunflower = ((101, 67, 33), (255, 255, 0))
redWhiteAndBlack = ((255, 0, 0), (0, 0, 0), (255, 0, 0), (255, 255, 255))
caleb = ((80, 50, 0), (10, 255, 20), (0, 0, 0))
dog = ((138, 97, 225), (0, 155, 255))
ResshasNumbers = ((3, 198, 252), (247, 221, 17), (81, 10, 247))
helenNumebrs = ((61, 128, 81), (128, 201, 232), (133, 36, 9))

totalDotIterationCount = 0

win.mainloop()
