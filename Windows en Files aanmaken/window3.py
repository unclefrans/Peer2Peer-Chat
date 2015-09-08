import Tkinter
root = Tkinter.Tk()
var = Tkinter.StringVar()
entry = Tkinter.Entry(root, textvariable=var)
entry.focus_set()
entry.pack()
var.set(root.title())

def changeTitle(): root.title(var.get())

Tkinter.Button(root, text="Change Title", command=changeTitle).pack()
Tkinter.mainloop()