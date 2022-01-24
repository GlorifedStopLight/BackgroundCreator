import tkinter as tk
from random import *
from math import *
from threading import Thread
import json
from tkinter.colorchooser import askcolor
from tkinter import messagebox
import ttkbootstrap as ttk
from tkinter import simpledialog
import os
from os.path import exists
from PIL import Image, ImageDraw, ImageFont, Image
from datetime import datetime

mockJsonFile = {
    "imageName": {
        "constants": {
            "width": 500,
            "height": 500,
            "seed": 12,
            "screenshotTakenAfterXDots": 92039
        },
        "dot generators": [
            {
                "branchCount": 3,
                "isMirrored": True,
                "colorPallet": ((255, 255, 255), (0, 0, 255), (0, 0, 0)),
                "colorSpeed": 0.3,
                "dotSize": 5
            },
            {
                "branchCount": 2,
                "isMirrored": True,
                "colorPallet": ((255, 0, 255), (255, 0, 255), (0, 255, 0)),
                "colorSpeed": 0.5,
                "dotSize": 5
            }
        ]
    }
}


def normal_round(n):
    if n - floor(n) < 0.5:
        return floor(n)
    return ceil(n)


class DotMaker:

    def __init__(self, splitReflections, isMirrored, colorsToFadeTo, fadeSpeed, followThisDot=None, startLocation=None,
                 moveType="random", angleOfTurn=90):

        if isMirrored:
            radianAmount = 2 * pi / splitReflections / 2
        else:
            radianAmount = 2 * pi / splitReflections

        self.angleOfTurn = angleOfTurn
        self.radianOfTurn = 2 * pi / angleOfTurn

        self.moveType = moveType
        self.movesBeforeDirectionChangeRange = (1, 10)
        self.changeDirectionIn = randint(self.movesBeforeDirectionChangeRange[0],
                                         self.movesBeforeDirectionChangeRange[1])
        self.slope = [s, s]

        self.cosine = cos(radianAmount)
        self.sine = sin(radianAmount)
        self.splitReflections = splitReflections
        self.center = (width // 2, height // 2)
        self.isMirrored = isMirrored
        self.drawThese = []
        self.followThisDot = followThisDot

        if startLocation is None:
            self.cords = [width // 2, height // 2]
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

        if len(colorsToFadeTo) == 1:
            self.getNextColor = self.onlyOneColor
            self.nextColor = self.currentColor
        else:
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

        if self.moveType == "random":
            self.changeCordsThread = self.randomGen

        elif self.moveType == "bouncing line":
            self.changeCordsThread = self.bouncingLineGen

        elif self.moveType == "point by point":
            self.changeCordsThread = self.pointByPoint
            self.moveHere = [0, 0]
            self.xDirection = self.cords[0] < self.moveHere[0]
            self.yDirection = self.cords[1] < self.moveHere[1]

            if self.xDirection:
                self.addX = s
            else:
                self.addX = -s

            if self.yDirection:
                self.addY = s
            else:
                self.addY = -s

        elif self.moveType == "direct point by point":
            self.changeCordsThread = self.directPointByPoint

            self.moveHere = [0, 0]
            self.xDirection = self.cords[0] < self.moveHere[0]
            self.yDirection = self.cords[1] < self.moveHere[1]

            self.m = (self.cords[0] - self.moveHere[0]), (self.cords[1] - self.moveHere[1])

            if self.xDirection:
                self.addX = -s * self.m[0] / self.m[1]
            else:
                self.addX = -s * self.m[0] / self.m[1]

            if self.yDirection:
                self.addY = s * self.m[1] / self.m[0]
            else:
                self.addY = s * self.m[1] / self.m[0]

        elif self.moveType == "random point by point":
            self.changeCordsThread = self.randomPointByPoint

            self.moveHere = [0, 0]
            self.xDirection = self.cords[0] < self.moveHere[0]
            self.yDirection = self.cords[1] < self.moveHere[1]

            if self.xDirection:
                self.addX = s
            else:
                self.addX = -s

            if self.yDirection:
                self.addY = s
            else:
                self.addY = -s

    def getDotCreationInfo(self):
        x = self.cords[0]
        y = self.cords[1]
        self.drawThese = []

        for i in range(self.splitReflections):

            self.drawThese.append((int(x), int(y), s, s, self.currentColor))
            if self.isMirrored:
                self.drawThese.append((int(-x + width), int(y), s, s, self.currentColor))
                self.drawThese.append((int(x), int(-y + height), s, s, self.currentColor))
                self.drawThese.append((int(-x + width), int(-y + height), s, s, self.currentColor))

            x, y = ((x - self.center[0]) * self.cosine - (y - self.center[1]) * self.sine + self.center[0]), \
                   ((x - self.center[0]) * self.sine + (y - self.center[1]) * self.cosine + self.center[1])

    def createDot(self):

        # loop through all the given dots to draw
        for dotInfo in self.drawThese:
            # draw dot
            drawRect(*dotInfo)

    def randomGen(self):

        self.cords[0] = abs(abs(self.cords[0] + choice((-s, s)) - width) - width)
        self.cords[1] = abs(abs(self.cords[1] + choice((-s, s)) - height) - height)

    def pointByPoint(self):
        conditions = [True, True]

        if self.xDirection and self.cords[0] + self.addX < self.moveHere[0] or \
                not self.xDirection and self.cords[0] + self.addX > self.moveHere[0]:
            self.cords[0] += self.addX
            conditions[0] = False

        if self.yDirection and self.cords[1] + self.addY < self.moveHere[1] or \
                not self.yDirection and self.cords[1] + self.addY > self.moveHere[1]:
            self.cords[1] += self.addY
            conditions[1] = False

        if all(conditions):

            self.moveHere = [randint(0, width), randint(0, height)]
            self.xDirection = self.cords[0] < self.moveHere[0]
            self.yDirection = self.cords[1] < self.moveHere[1]

            if self.xDirection:
                self.addX = s
            else:
                self.addX = -s

            if self.yDirection:
                self.addY = s
            else:
                self.addY = -s

    def randomPointByPoint(self):

        directions = []

        # adding to x won't be bad
        if self.xDirection and self.cords[0] + self.addX < self.moveHere[0] or \
                not self.xDirection and self.cords[0] + self.addX > self.moveHere[0]:

            directions.append(0)

        # adding to y won't be bad
        elif self.yDirection and self.cords[1] + self.addY < self.moveHere[1] or \
                not self.yDirection and self.cords[1] + self.addY > self.moveHere[1]:

            directions.append(1)

        if directions != []:

            myDirection = choice(directions)
            if myDirection == 0:
                self.cords[0] += self.addX

            elif myDirection == 1:
                self.cords[1] += self.addY

        else:

            self.moveHere = [randint(0, width), randint(0, height)]
            self.xDirection = self.cords[0] < self.moveHere[0]
            self.yDirection = self.cords[1] < self.moveHere[1]

            if self.xDirection:
                self.addX = s
            else:
                self.addX = -s

            if self.yDirection:
                self.addY = s
            else:
                self.addY = -s

    def directPointByPoint(self):
        conditions = [True, True]

        if self.xDirection and self.cords[0] + self.addX < self.moveHere[0] or \
                not self.xDirection and self.cords[0] + self.addX > self.moveHere[0]:
            self.cords[0] += self.addX
            self.cords[1] = self.moveHere[1] + ((self.m[1] / self.m[0]) * (self.cords[0] - self.moveHere[0]))
            conditions[0] = False
        """
        if self.yDirection and self.cords[1] + self.addY < self.moveHere[1] or \
                not self.yDirection and self.cords[1] + self.addY > self.moveHere[1]:
            self.cords[1] += self.addY
            conditions[1] = False
        """
        if all(conditions):

            self.moveHere = [randint(0, width), randint(0, height)]
            self.xDirection = self.cords[0] < self.moveHere[0]
            self.yDirection = self.cords[1] < self.moveHere[1]

            self.m = (self.cords[0] - self.moveHere[0]), (self.cords[1] - self.moveHere[1])

            if self.xDirection:
                self.addX = s * self.m[0] / self.m[1]
            else:
                self.addX = s * self.m[0] / self.m[1]

            if self.yDirection:
                self.addY = -s * self.m[1] / self.m[0]
            else:
                self.addY = -s * self.m[1] / self.m[0]

    def bouncingLineGen(self):

        # going off the right side
        if not 0 < self.cords[0] + self.slope[0] < width:
            self.slope[0] = self.slope[0] * -1

        if not 0 < self.cords[1] + self.slope[1] < height:
            self.slope[1] = self.slope[1] * -1

        if self.changeDirectionIn == 0:
            newDirect = choice((-1, 1))

            if newDirect == 1:
                self.slope[1] *= -1
            else:
                self.slope[0] *= -1

            self.changeDirectionIn = randint(self.movesBeforeDirectionChangeRange[0],
                                             self.movesBeforeDirectionChangeRange[1])

        else:
            self.changeDirectionIn -= 1

        self.cords[0] = abs(abs(self.cords[0] + self.slope[0] - width) - width)
        self.cords[1] = abs(abs(self.cords[1] + self.slope[1] - height) - height)

    # doesn't return anything just calculates the next color
    def getNextColor(self):

        # add to current grace
        if self.feedGrace:
            self.currentGrace += self.fadeSpeed
            if self.newColorGracePeriod <= self.currentGrace:
                self.feedGrace = False

        # have arrived at the desired color
        if [normal_round(self.currentColor[0]), normal_round(self.currentColor[1]),
            normal_round(self.currentColor[2])] == list(self.nextColor) and \
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

    # lol
    def onlyOneColor(self):
        pass


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
        if [normal_round(self.currentColor[0]), normal_round(self.currentColor[1]),
            normal_round(self.currentColor[2])] == list(self.nextColor) and \
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
    def __init__(self, colorSelection, colorSpeed, branchNumber, isBranchesMirrored, moveType, startLocation=None):
        self.dotFactoryObj = DotMaker(branchNumber, isBranchesMirrored, colorSelection, colorSpeed,
                                      startLocation=startLocation, moveType=moveType)

    def updateAllThings(self):
        getColorThread = Thread(target=self.dotFactoryObj.getNextColor)
        doDotThread = Thread(target=self.dotFactoryObj.getDotCreationInfo)
        cordsThread = Thread(target=self.dotFactoryObj.changeCordsThread)

        getColorThread.start()
        doDotThread.start()
        cordsThread.start()

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
            self.insert(i + 1, x)
            self.itemconfig(i + 1, {"bg": rgb_to_hex(x), "selectbackground": rgb_to_hex(x), "fg": rgb_to_hex(x),
                                    "selectforeground": rgb_to_hex(invertRGBValues(x))})
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.itemconfig(i - 1, {"bg": rgb_to_hex(x), "selectbackground": rgb_to_hex(x), "fg": rgb_to_hex(x),
                                    "selectforeground": rgb_to_hex(invertRGBValues(x))})
            self.curIndex = i


class DotGUITab:

    def __init__(self, frame_dotSettings, frame_colors, tabName):

        self.frame_dotSettings = frame_dotSettings
        self.frame_dotSettings.grid(row=0, column=0)

        self.tabName = tabName

        # add a tab
        notebook_dots.add(child=self.frame_dotSettings, text=self.tabName)

        self.listbox_colorPallet = DragDropListbox(master=frame_colors)
        self.listbox_colorPallet.grid(row=1, column=0)

        self.label_colorSpeed = ttk.Label(master=self.frame_dotSettings, text="color speed")
        self.label_colorSpeed.grid(row=1, column=0)

        self.entry_colorSpeed = ttk.Entry(master=self.frame_dotSettings, width=5)
        self.entry_colorSpeed.grid(row=1, column=1)
        self.entry_colorSpeed.insert(0, "0.3")

        self.label_branchCount = ttk.Label(master=self.frame_dotSettings, text="branch Count")
        self.label_branchCount.grid(row=2, column=0)

        self.entry_branchCount = ttk.Entry(master=self.frame_dotSettings, width=5)
        self.entry_branchCount.grid(row=2, column=1)
        self.entry_branchCount.insert(0, "4")

        self.checkBoxSelected_isMirrored = ttk.IntVar()
        self.checkBox_isMirrored = ttk.Checkbutton(master=self.frame_dotSettings,
                                                   text="mirrored",
                                                   variable=self.checkBoxSelected_isMirrored)
        self.checkBox_isMirrored.grid(row=3, column=0)

        self.dropSelected_generationOptions = ttk.StringVar()
        self.drop_generationOptions = ttk.OptionMenu(self.frame_dotSettings, self.dropSelected_generationOptions,
                                                     movementTypes[0],
                                                     *movementTypes, style="secondary")
        self.drop_generationOptions.grid(row=0, column=0)

        # add color
        self.butt_chooseColor = ttk.Button(master=frame_colors, text="+", command=self.addColorToColorPallet)
        self.butt_chooseColor.grid(row=2, column=0, sticky="W", pady=5)

        # button to remove color
        self.butt_removeColor = ttk.Button(master=frame_colors, text="-",
                                           command=self.removeSelectedColorFromColorPallet)
        self.butt_removeColor.grid(row=2, column=0, sticky="E", pady=5)

        self.butt_randomColor = ttk.Button(master=frame_colors, text="rand", command=self.addRandomColor)
        self.butt_randomColor.grid(row=2, column=0)

        # save the colors you've chosen in a json file
        self.butt_saveColorPreset = ttk.Button(master=frame_colors, text="save color preset",
                                               command=self.saveColorPreset,
                                               style="success")
        self.butt_saveColorPreset.grid(row=3, column=0, pady=5)

        # button to delete the selected color preset
        self.butt_deleteColorPreset = ttk.Button(master=frame_colors, text="delete color preset",
                                                 command=self.deleteColorPreset,
                                                 style="danger")
        self.butt_deleteColorPreset.grid(row=4, column=0, pady=5)

        # datatype of menu text
        self.dropSelected_colorPalletPresets = ttk.StringVar()

        self.drop_colorPresets = ttk.OptionMenu(frame_colors,
                                                self.dropSelected_colorPalletPresets,
                                                "--select a preset--",
                                                *self.getColorPresetNames(),
                                                command=self.loadColorPreset)
        self.drop_colorPresets.grid(row=0, column=0, pady=5)

    def addRandomColor(self):
        rgbValue = []
        color = [randint(0, 255), 255, 0]

        for i in range(2, -1, -1):
            rgbValue.append(color.pop(randint(0, i)))

        rgbValue = [randint(0, 255), randint(0, 255), randint(0, 255)]
        selectedColor = rgb_to_hex(rgbValue)

        self.listbox_colorPallet.insert("end", rgbValue)
        self.listbox_colorPallet.itemconfig("end", {"bg": selectedColor, "selectbackground": selectedColor,
                                                    "fg": selectedColor,
                                                    "selectforeground": rgb_to_hex(invertRGBValues(rgbValue))})

    def removeSelectedColorFromColorPallet(self):
        self.listbox_colorPallet.delete(self.listbox_colorPallet.curselection())

    def addColorToColorPallet(self):
        selectedColor = askcolor(title="Tkinter Color Chooser")
        rgbValue = (floor(selectedColor[0][0]), floor(selectedColor[0][1]), floor(selectedColor[0][2]))
        self.listbox_colorPallet.insert("end", rgbValue)
        self.listbox_colorPallet.itemconfig("end", {"bg": selectedColor[1], "selectbackground": selectedColor[1],
                                                    "fg": selectedColor[1],
                                                    "selectforeground": rgb_to_hex(invertRGBValues(rgbValue))})

    def saveColorPreset(self):

        colorPresetName = simpledialog.askstring(title="Save Color Preset",
                                                 prompt="Enter the name of your new color preset:")

        if colorPresetName == "":
            print("no given name for preset")
            return

        with open("mySavedData.json") as outfile:

            # load all of the current presets
            info = json.load(outfile)

            # initialize the list for colors
            presetColors = []

            # loop through each line in listbox
            for i in range(self.listbox_colorPallet.size()):
                # add the name to the list (the name is a color)
                presetColors.append(self.listbox_colorPallet.get(i))

            # create a new color preset
            info["savedColors"][colorPresetName] = presetColors

            # create a json object
            json_object = json.dumps(info, indent=4)

        # Writing to sample.json
        with open("mySavedData.json", "w") as outfile:

            outfile.write(json_object)

        """
        menu = drop_colorPresets["menu"]
        menu.delete(0, "end")
        for string in getColorPresetNames():
            menu.add_command(label=string,
                             command=lambda value=string: dropSelected_colorPalletPresets.set(value))
        """

    # returns a list of strings which are the names of saved color presets
    def getColorPresetNames(self):
        # open json file (contains saved information)
        with open("mySavedData.json") as outfile:
            # convert the json file into a python object
            allSavedData = json.load(outfile)

            # get all the names of the color presets
            allColorPresetNames = list(allSavedData["savedColors"].keys())

            return allColorPresetNames

    def loadColorPreset(self, event):
        # open save data
        with open("mySavedData.json") as outfile:

            # convert save data into a python object
            saveData = json.load(outfile)

            # get the currently selected preset name
            colorPresetName = self.dropSelected_colorPalletPresets.get()

            try:
                # get the array of colors from data using colorPresetName
                loadedColors = saveData["savedColors"][colorPresetName]

            # preset name doesn't exist
            except KeyError:

                print("preset name does not exist")

                # give up
                return

            # go through each line and remove it
            for i in range(self.listbox_colorPallet.size()):
                self.listbox_colorPallet.delete(0)

            # add each color to our listbox of colors
            for color in loadedColors:
                self.listbox_colorPallet.insert("end", color)
                self.listbox_colorPallet.itemconfig("end",
                                                    {"bg": rgb_to_hex(color), "selectbackground": rgb_to_hex(color),
                                                     "fg": rgb_to_hex(color),
                                                     "selectforeground": rgb_to_hex(invertRGBValues(color))})

    def getCurrentColorPalletColors(self):
        currentColors = []

        for i in range(self.listbox_colorPallet.size()):
            currentColors.append(self.listbox_colorPallet.get(i))

        return currentColors

    def deleteColorPreset(self):
        presetName = self.dropSelected_colorPalletPresets.get()
        x = messagebox.askquestion("Warning", "are you sure you would like \n to delete " + presetName + "?")

        if x == "yes":
            with open("mySavedData.json") as outfile:
                savedData = json.load(outfile)

                del savedData["savedColors"][presetName]

            with open("mySavedData.json", "w") as outfile:
                json_object = json.dumps(savedData, indent=4)
                outfile.write(json_object)

        # at least one color preset still exists
        # if getColorPresetNames():

        # set the selected item in the drop down menu to the first item in the menu
        # dropSelected_colorPalletPresets.set(getColorPresetNames()[0])


# window of previous images
class ImageViewWindow:
    def __init__(self):

        path = "myIcons"
        dir_list = os.listdir(path)

        onlyPNGFiles = []
        for fileName in dir_list:
            if fileName.endswith(".png"):
                onlyPNGFiles.append(fileName)

        itemsInEachRow = 7

        self.icons = []
        for pngFileIndex in range(len(onlyPNGFiles)):

            image = ttk.PhotoImage(file="myIcons/" + onlyPNGFiles[pngFileIndex])
            columnIndex = pngFileIndex % itemsInEachRow
            rowIndex = pngFileIndex // itemsInEachRow

            editor = ImageEditor("myImages/" + onlyPNGFiles[pngFileIndex])

            self.icons.append(ttk.Button(master=frame_photos, image=image, command=editor.showPhotoEditor))
            self.icons[pngFileIndex].grid(row=rowIndex, column=columnIndex)
            self.icons[pngFileIndex].image = image


class ImageEditor:
    def __init__(self, fileName):
        self.fileName = fileName
        self.frame_pictureEdit = ttk.Frame(master=win, width=screenWidth, height=screenHeight)

        image = ttk.PhotoImage(file=self.fileName)
        self.label_image = ttk.Label(master=self.frame_pictureEdit, image=image)
        self.label_image.grid(row=0, column=0)
        self.label_image.image = image

        # blur value
        self.blurValue = ttk.Entry(master=self.frame_pictureEdit)
        self.blurValue.grid(row=0, column=1)

        # button reloads image
        self.button_reloadImage = ttk.Button(master=self.frame_pictureEdit)
        self.button_reloadImage.grid(row=1, column=0)

        # get the preset information using the fileName and the json file

    def showPhotoEditor(self):
        frame_photos.grid_forget()
        self.frame_pictureEdit.grid(row=0, column=0)

    def reloadImage(self):
        # Open existing image
        OriImage = Image.open('images/boy.jpg')
        OriImage.show()

        # Applying GaussianBlur filter
        gaussImage = OriImage.filter(ImageFilter.GaussianBlur(5))
        gaussImage.show()

        # Save Gaussian Blur Image
        gaussImage.save('images/gaussian_blur.jpg')


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def saveSeed():
    seedName = simpledialog.askstring(title="Saving Seed", prompt="Enter name for this seed: ")

    if seedName == "" or entry_seedInput.get() == "":
        return

    with open("mySavedData.json") as outfile:
        # load all of the current presets
        info = json.load(outfile)

        # add another seed
        info["savedSeeds"][seedName] = entry_seedInput.get()

        json_object = json.dumps(info, indent=4)

    # Writing to sample.json
    with open("mySavedData.json", "w") as outfile:
        outfile.write(json_object)


def invertRGBValues(rgb):
    return 255 - rgb[0], 255 - rgb[1], 255 - rgb[2]


def getPresetColors(presetName):
    # open json file
    with open("mySavedData.json") as outfile:
        # load saved data as python object
        allData = json.load(outfile)

        # return colors
        return allData["savedColors"][presetName]


def activateOverlayView(event):
    if "entry" in str(win.focus_get()):
        return

    for childFrame in win.winfo_children():
        childFrame.grid_forget()
    overlayFrame.grid(row=0, column=0)


def activateMandalaView(event):
    if "entry" in str(win.focus_get()):
        return
    for childFrame in win.winfo_children():
        childFrame.grid_forget()
    frame_mandala.grid(row=0, column=0)


def activatePhotoView(event):
    if "entry" in str(win.focus_get()):
        return
    for childFrame in win.winfo_children():
        childFrame.grid_forget()
    frame_photos.grid(row=0, column=0)


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


def returnNumberFromString(givenString):
    letters = "0123456789abcdefghijklmnopqrstuvwxyz,./<>?;':[]{}\| _+-=)(*&^%$#@!~`"
    numberString = ""
    for char in givenString:
        numberString += str(letters.index(char))

    return int(numberString)


#
class myApp:
    def __init__(self):
        chosenSeed = returnNumberFromString(entry_seedInput.get())

        for preset in dotsDict:

            if not dotsDict[preset].getCurrentColorPalletColors():
                messagebox.showerror(title="Color Error", message="must have at least one color in the color pallet")
                return

            elif len(dotsDict[preset].getCurrentColorPalletColors()) == 1:
                if not messagebox.askyesno(title="U GOOF", message="you're only using one color so you're a goof \n "
                                                                   "you may only continue if you agree that you're dumb"):
                    return

        # set seed
        seed(chosenSeed)

        # show mandala frame
        activateMandalaView(None)
        myThreads = []
        for preset in dotsDict:
            self.myControls = ControlAll(colorSelection=dotsDict[preset].getCurrentColorPalletColors(),
                                    colorSpeed=float(dotsDict[preset].entry_colorSpeed.get()),
                                    branchNumber=int(dotsDict[preset].entry_branchCount.get()),
                                    isBranchesMirrored=dotsDict[preset].checkBoxSelected_isMirrored.get(),
                                    moveType=dotsDict[preset].dropSelected_generationOptions.get())

            myThreads.append(Thread(target=self.generationLoop))
        for thread in myThreads:
            thread.start()


    def generationLoop(self):
        while True:
            self.myControls.updateAllThings()


def shot(event):
    # ask user what the image name should be
    imageName = simpledialog.askstring(title="Screenshot", prompt="Enter a name for this image: ")

    # check if name is already being used for a previous screenshot
    if exists('myImages/' + imageName + '.png'):

        # ask user whether or not to override old screenshot
        overrideScreenshot = messagebox.askokcancel(title="Error: Name In Use",
                                                    message=imageName + ".png already exists. Would you like to override this file?")

        # user wanted to override the old screenshot
        if not overrideScreenshot:
            now = datetime.now()

            imageName = "screenshot at " + now.strftime("%d-%m-%Y %H:%M:%S")

    canvas_mandala.postscript(file="myImages/screenshot.ps", colormode='color')
    psimage = Image.open('myImages/screenshot.ps')
    psimage.save('myImages/' + imageName + '.png')

    psimage = Image.open('myImages/' + imageName + '.png')
    psimage = psimage.crop((1, 1, width + 1, height + 1))
    psimage.save('myImages/' + imageName + '.png')

    psimage.save('myImages/' + 'MOSTRECENTSCREENSHOT' + '.png')

    # this code will add an icon of the new screenshot to the icons folder
    iconSize = [(100, 100)]
    filename = "myImages/" + imageName + ".png"
    img = Image.open(filename)

    # save as an icon, with low resolution
    img.save("myIcons/" + imageName + '.ico', sizes=iconSize)

    # open low resolution .ico image
    filename = "myIcons/" + imageName + ".ico"
    img = Image.open(filename)

    # save image as png
    img.save("myIcons/" + imageName + '.png')

    if checkBoxSelected_addWaterMarkToScreenShots.get():

        # Opening Image
        img = Image.open(r'myImages/screenshot.png')

        # Creating draw object
        draw = ImageDraw.Draw(img)

        # Creating text and font object
        text = "github.com/mhanna3141"
        font = ImageFont.load_default()

        # Positioning Text
        textwidth, textheight = draw.textsize(text, font)

        x = width / 2 - textwidth / 2
        y = height - textheight - 300

        # Applying text on image via draw object
        draw.text((x, y), text, font=font)

        # Saving the new image
        img.save(r'myImages/screenshot.png')


def printImage(event):
    printMe = simpledialog.askstring(title="Printer", prompt="Enter the name of your picture, \n leave blank to print most recently saved: ")

    if printMe == "":
        printMe = 'MOSTRECENTSCREENSHOT'

    os.system(
        "lpr -P HP_Color_LaserJet_MFP_M281fdw__DDA757_ myImages/" + printMe + ".png")


def addDotConfigureTab():
    # holds widgets that control the colors
    frame_dotSettings = ttk.Frame(master=overlayFrame)

    frame_colors = ttk.Frame(master=frame_dotSettings)
    frame_colors.grid(row=0, column=3, padx=20)

    name = "Dot Gen " + str(len(dotsDict) + 1)

    dotsDict[name] = DotGUITab(frame_dotSettings, frame_colors, name)


def deselect(event):
    win.focus()


# 1366
# iphone 500
width = 1366
screenWidth = 1366

# 768
# iphone 900
height = 768
screenHeight = 768
s = 5

circleMatrix = []
for i in range(width + s):
    tempList = []
    for j in range(height + s):
        tempList.append(None)

    circleMatrix.append(tempList.copy())


# pick a random seed
randomSeed = randint(0, 1000000000)

movementTypes = ["random", "bouncing line", "point by point", "direct point by point", "random point by point"]

dotsDict = {}

win = ttk.Window(themename="yeti")
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)

overlayFrame = ttk.Frame(master=win)
overlayFrame.grid(row=0, column=0, padx=30, pady=30)

frame_globalSettings = ttk.Frame(master=overlayFrame)
frame_globalSettings.grid(row=0, column=1)

frame_mandala = ttk.Frame(win, width=screenWidth, height=screenHeight)

# show each photo
frame_photos = ttk.Frame(master=win, width=screenWidth, height=screenHeight)

notebook_dots = ttk.Notebook(master=overlayFrame)
notebook_dots.grid(row=0, column=10)

# gets the desired seed to save
entry_seedInput = ttk.Entry(master=overlayFrame, width=30)
entry_seedInput.grid(row=0, column=0)
entry_seedInput.insert(0, str(randomSeed))

# save seed
butt_saveSeed = ttk.Button(master=overlayFrame, text="Save Seed", command=saveSeed, style="success")
butt_saveSeed.grid(row=1, column=0)

# generates a mandala
butt_startGeneration = ttk.Button(master=overlayFrame, command=myApp, text="start generation")
butt_startGeneration.grid(row=10, column=6)

# create a canvas for the frame
canvas_mandala = ttk.Canvas(master=frame_mandala, width=width, height=height)  #, scrollregion=(0, 0, 500, 500))
canvas_mandala.grid(row=0, column=0)

checkBoxSelected_addWaterMarkToScreenShots = ttk.IntVar()
checkBox_addWaterMarkToScreenShots = ttk.Checkbutton(master=frame_globalSettings, text="add water mark to screenshots",
                                                     variable=checkBoxSelected_addWaterMarkToScreenShots)
checkBox_addWaterMarkToScreenShots.grid(row=4, column=0)

butt_addTab = ttk.Button(master=frame_globalSettings, text="add dot generator", command=addDotConfigureTab)
butt_addTab.grid(row=1, column=0)

win.bind("<F2>", shot)
win.bind("<p>", printImage)
win.bind("1", activateOverlayView)
win.bind("2", activateMandalaView)
win.bind("3", activatePhotoView)
win.bind("<Return>", deselect)

win.attributes('-fullscreen', True)

ImageViewWindow()

# add dot generator
addDotConfigureTab()
win.mainloop()

# TODO: add a delete dot generator button, cure cancer, get multiple dot generators working, save generator presets,
# TODO: save current set up, save preset when taking a screenshot
# TODO: add help buttons, add tutorial, able to pick which printer to print to, open screenshot folder in finder button
# TODO: make default settings configurable

# TODO: after a variable number of dot iterations save the canvas as a screenshot, delete the canvas show the screenshot
# TODO: and continue drawing.