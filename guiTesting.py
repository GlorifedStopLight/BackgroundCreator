from tkinter import *

def callback():
    print(master.focus())

master = Tk()
e = Entry(master)
e.pack()
e.focus()
b = Button(master, text="get", width=10, command=callback)
b.pack()

master.mainloop()