import ttkbootstrap as ttk

root = ttk.Window(themename="yeti")
frame_photos = ttk.Frame(master=root)
frame_photos.grid(row=0, column=0)

img = ttk.PhotoImage(file="myIcons/tiny.png")
button1 = ttk.Button(master=frame_photos, image=img)
button1.grid(row=0, column=0)

frame_photos.mainloop()