import ttkbootstrap as ttk

win = ttk.Window(themename="yeti")
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)

myCanvas = ttk.Canvas(master=win, width=700, height=700)

gif1 = ttk.PhotoImage(file='myImages/dim test 9.png')

# Put gif image on canvas.
# Pic's upper-left corner (NW) on the canvas is at x=50 y=10.
myCanvas.create_image(250, 250, image=gif1)
myCanvas.grid(row=0, column=0)

myCanvas.create_oval(0, 0, 10, 10)

win.mainloop()
