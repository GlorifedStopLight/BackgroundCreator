import ttkbootstrap as ttk

win = ttk.Window(themename="yeti")
#overlayFrame = ttk.Frame(master=win)
#overlayFrame.grid(row=0, column=0, padx=30, pady=30)

#image1 = ttk.PhotoImage(file="myImages/dim test 9.png")
myButt = ttk.Button(master=win, text="sup") #  image=image1,
myButt.grid(row=0, column=0)
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)
#myButt.image = image1

win.mainloop()
