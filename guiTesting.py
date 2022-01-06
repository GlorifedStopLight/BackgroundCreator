import tkinter as tk
import json
from tkinter.colorchooser import askcolor
from threading import Thread


myExampleObject = {
    "fullPresets": {
        "that fun spiral one": {
            "all dot Info": [
                {
                    "color change speed": 0.5,
                    "color scheme": ((0, 0, 0), (255, 255, 255), (0, 255, 0)),
                    "number of branches": 2,
                    "isMirrored": True
                },
                {
                    "color change speed": 45,
                    "color scheme": ((255, 255, 255), (0, 255, 0)),
                    "number of branches": 9,
                    "isMirrored": False
                }
            ],
            "number of dots made at time of save": 8239,
            "show screen every": 50,
            "seed": 913042

        },

        "I really like tits": {
            "all dot Info": [
                {
                    "color change speed": 0.5,
                    "color scheme": ((0, 0, 0), (255, 255, 255), (0, 255, 0)),
                    "number of branches": 2,
                    "isMirrored": True
                },
                {
                    "color change speed": 45,
                    "color scheme": ((255, 255, 255), (0, 255, 0)),
                    "number of branches": 9,
                    "isMirrored": False
                }
            ],
            "number of dots made at time of save": 8239,
            "show screen every": 50,
            "seed": 12
        }
    },
    "savedColors": {
        "blues and purples": ((0, 0, 255), (0, 0, 0), (23, 203, 234)),
        "lesbian Flag": ((214, 41, 0), (255, 155, 85), (255, 255, 255), (212, 97, 166), (165, 0, 98))
    },
    "savedSeeds": {
        "little man person": 12,
        "idk I haven't tried this one": 3982384928
    }
}


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


def rgb_to_hex(rgb):
    rgb = rgb[0], rgb[1], rgb[2]

    return '#%02x%02x%02x' % rgb


def saveUserInput():

    if seedNameInput.get() == "" or seedCodeInput.get() == "":
        return

    with open("mySavedData.json") as outfile:

        # load all of the current presets
        info = json.load(outfile)

        # add another seed
        info["savedSeeds"][seedNameInput.get()] = seedCodeInput.get()

        json_object = json.dumps(info, indent=4)

    # Writing to sample.json
    with open("mySavedData.json", "w") as outfile:

        outfile.write(json_object)


def addColor():
    myColors.append(askcolor(title="Tkinter Color Chooser")[1])
    listbox.insert("end", myColors[-1])
    listbox.itemconfig("end", {"bg": myColors[-1], "selectbackground": myColors[-1]})


def removeSelectedColor():
    listbox.delete(listbox.curselection())


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
        for i in range(listbox.size()):

            # add the name to the list (the name is a color)
            presetColors.append(hex_to_rgb(listbox.get(i)))

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
                         command=lambda value=string: clicked.set(value))


# returns a list of strings which are the names of saved color presets
def getColorPresetNames():

    # open json file (contains saved information)
    with open("mySavedData.json") as outfile:

        # convert the json file into a python object
        allSavedData = json.load(outfile)

        # get all the names of the color presets
        allColorPresetNames = list(allSavedData["savedColors"].keys())

        return allColorPresetNames


def loadColorPreset():

    # open save data
    with open("mySavedData.json") as outfile:

        # convert save data into a python object
        saveData = json.load(outfile)

        # get the currently selected preset name
        colorPresetName = clicked.get()

        try:
            # get the array of colors from data using colorPresetName
            loadedColors = saveData["savedColors"][colorPresetName]

        # preset name doesn't exist
        except KeyError:

            # give up
            return

        # go through each line and remove it
        for i in range(listbox.size()):
            listbox.delete(0)

        # add each color to our listbox of colors
        for color in loadedColors:

            listbox.insert("end", color)
            listbox.itemconfig("end", {"bg": rgb_to_hex(color), "selectbackground": rgb_to_hex(color)})


def getPresetColors(presetName):

    # open json file
    with open("mySavedData.json") as outfile:

        # load saved data as python object
        allData = json.load(outfile)

        # return colors
        return allData["savedColors"][presetName]


myColorButtons = []
myColors = []

win = tk.Tk()
overlayFrame = tk.Frame(master=win).grid(row=0, column=0)

# list of colors
listbox = DragDropListbox(master=win)
listbox.grid(row=0, column=3)
listbox.config(selectborderwidth=5, relief=tk.SUNKEN, exportselection=False, activestyle=tk.UNDERLINE)

# gets the desired seed to save
seedCodeInput = tk.Entry(master=overlayFrame, width=50)
seedCodeInput.grid(row=2, column=0)

#
seedInputLabel = tk.Label(mast=overlayFrame, text="input your seed below")
seedInputLabel.grid(row=1, column=0)

# gets the name for the seed
seedNameInput = tk.Entry(master=overlayFrame, width=50)
seedNameInput.grid(row=4, column=0)

#
seedNameInputLabel = tk.Label(mast=overlayFrame, text="input your seed name below")
seedNameInputLabel.grid(row=3, column=0)

saveSeedButton = tk.Button(master=overlayFrame, text="Save Seed", command=saveUserInput)
saveSeedButton.grid(row=0, column=0)

# add color
wantColor = tk.Button(master=overlayFrame, text="choose color", command=addColor)
wantColor.grid(row=2, column=2)

# button to remove color
removeColorButton = tk.Button(master=overlayFrame, text="Remove Selected Color", command=removeSelectedColor)
removeColorButton.grid(row=2, column=3)

# gets the name for the seed
entry_colorPresetName = tk.Entry(master=overlayFrame, width=50)
entry_colorPresetName.grid(row=3, column=3)

# save the colors you've chosen in a json file
butt_saveColorPreset = tk.Button(master=overlayFrame, text="save color preset", command=saveColorPreset)
butt_saveColorPreset.grid(row=3, column=4)

# datatype of menu text
clicked = tk.StringVar()

# initial menu text
clicked.set("--select a preset--")

drop_colorPresets = tk.OptionMenu(win, clicked, *getColorPresetNames())
drop_colorPresets.grid(row=1, column=5)

butt_loadInColorPreset = tk.Button(master=win, command=loadColorPreset, text="load Preset")
butt_loadInColorPreset.grid(row=0, column=5)

win.mainloop()
