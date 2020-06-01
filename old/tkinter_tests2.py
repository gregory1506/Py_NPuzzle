from tkinter import *

class UI(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)
        self.create_widgets(parent)

    def create_widgets(self, root):
        #first
        f1 = Frame(root)
        e1 = Entry(f1, width=30, bd=4)
        l1 = Label(f1, text="1")
        e1.grid(row=0, column=0)
        l1.grid(row=0, column=1)
        f1.grid()
        #second
        f2 = Frame(root)
        e2 = Entry(f2, width=30, bd=4)
        l2 = Label(f2, text="2")
        e2.grid(row=0, column=0)
        l2.grid(row=0, column=1)
        f2.grid()
        #third
        self.s1 = IntVar()
        self.s1.set(3)
        f3 = Frame(root)
        e3 = Entry(f3, width=30, bd=4)
        l3 = Label(f3, textvariable=self.s1)
        e3.grid(row=0, column=0)
        l3.grid(row=0, column=1)
        f3.grid()

    def set_score(self, score):
       self.s1.set(score)

def test_ui():
    root = Tk()
    app = UI(root)
    app.set_score(4)
    app.mainloop()

test_ui()