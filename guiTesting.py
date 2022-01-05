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


def saveUserInput():

    if seedNameInput == "" or seedCodeInput == "":
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
    #listbox.get(listbox.curselection())
    listbox.delete(listbox.curselection())


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
wantColor.grid(row=1, column=2)

# 'list' of chosen colors
chosenColorTab = tk.Canvas(master=overlayFrame)
chosenColorTab.grid(row=0, column=30)

# button to remove color
removeColorButton = tk.Button(master=overlayFrame, text="Remove Selected Color", command=removeSelectedColor)
removeColorButton.grid(row=1, column=3)

win.mainloop()
