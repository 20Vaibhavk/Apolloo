from tkinter import *

root = Tk()
root.geometry("1138x640")

bgImage = PhotoImage(file = r"images/main_bg.jpg")
Label.place(root, image=bgImage).place(relwidth = 1, relheight = 1)

root.mainloop()