from tkinter import *
import random

# class Tile(Button):
#     def __init__(self, master=None, text=None):
#         super().__init__(master=master, text=text)
#         self.master = master

#     def changePos(self,row=None,column=None):
#         self.row = row
#         self.column = column

class Board(Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.state = [str(x) for x in range(1,17)]
        random.shuffle(self.state)
        self.blank_loc = self.state.index("16")
        self.num_moves = 0

        for i in range(4):
            for j in range(4):
                idx = (i - 1) * 4 + j
                tmp = self.state[idx]
                if tmp == "16":
                    tmp = "  "
                    but = Button(master=master, text="{}".format(tmp), justify="center", width=2, font=("Arial Bold", 20))
                else:
                    but = Button(master=master, text="{}".format(tmp), justify="center", width=2, font=("Arial Bold", 20))
                but.grid(row=i,column=j)
    
    def isSolvable(self):
        # function to count the number of inversions 
        def countInv(state):
            numinv = 0
            tmp = state.copy()
            for i in range(0,16,1):
                for j in range(i+1,16,1):
                    if tmp[i] > tmp[j]:
                        numinv += 1
            return numinv
        #function to find row of the blank tile (counting from bottom)
        def blankRow(state):
            return 4 - ((state.index("16")) // 4)

        isNeven = bool((int(len(self.state) ** 0.5) + 1) % 2)
        isEvenRow = bool((blankRow(self.state) + 1) % 2)
        isNinv = bool((countInv(self.state) + 1) % 2)
        if not isNeven:
            if isNinv:
                return True
            else:
                return False
        else:
            if isEvenRow:
                if not isNinv:
                    return True
                else:
                    return False
            else:
                if isNinv:
                    return True
                else:
                    return False
    
    def swap(self,loc1,loc2):
        pass

root = Tk()
root.title("15 PUZZLE")
# root.geometry("600x400")
left_top_frame = Frame(root,relief=RIDGE,bg="white",highlightbackground="black",highlightthickness=1)
right_top_frame = Frame(root,relief=RAISED,highlightbackground="black",highlightthickness=1)
left_bot_frame = Frame(root,relief=RIDGE,bg="blue",highlightbackground="black",highlightthickness=1)
right_bot_frame = Frame(root,relief=RIDGE,bg="white",highlightbackground="black",highlightthickness=1)
# top left stuff
newboard = Board(left_top_frame)
# bottom left stuff
lb_but = Button(left_bot_frame,text="Solve")
lb_but.pack(side=LEFT)
lb_but1 = Button(left_bot_frame,text="New Puzzle")
lb_but1.pack(side=RIGHT)
# top right stuff 
rt_lab1 = Label(right_top_frame,text="Is this puzzle solvable?")
rt_lab1.pack()
rt_lab2 = Label(right_top_frame)
if newboard.isSolvable():
    rt_lab2["text"] = "Yes"
    rt_lab2["bg"] = "green"
else:
    rt_lab2["text"] = "No"
    rt_lab2["bg"] = "red"
rt_lab2.pack()
rt_lab3 = Label(right_top_frame,text="Minimum number of moves")
rt_lab3.pack()
rt_lab4 = Label(right_top_frame,text=str(50))
rt_lab4.pack()

# bottom right stuff

# set the frames in place
left_top_frame.grid(row=0,column=0,padx=1,pady=1)
right_top_frame.grid(row=0,column=1,padx=1,pady=1)
left_bot_frame.grid(row=1,column=0,padx=1,pady=1)
right_bot_frame.grid(row=1,column=1,padx=1,pady=1)
root.mainloop()



