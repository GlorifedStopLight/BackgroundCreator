import ttkbootstrap as ttk

win = ttk.Window(themename="cosmo")

lab1 = ttk.Label(master=win, text="0,0")
lab1.grid(row=0, column=0)

lab2 = ttk.Label(master=win, text="0,1")
lab2.grid(row=0, column=1)

lab3 = ttk.Label(master=win, text="0,2")
lab3.grid(row=0, column=2)

lab4 = ttk.Label(master=win, text="1,0")
lab4.grid(row=1, column=0)

lab5 = ttk.Label(master=win, text="2,0")
lab5.grid(row=2, column=0)

win.mainloop()
