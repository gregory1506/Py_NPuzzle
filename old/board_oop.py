import random
from tkinter import *

class Game(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("500x300")
        self.resizable(0,0)
        self.title("The Classic N Puzzle")

        self.create_container()
        self.frames = {}
        for F in (StartPage, Board):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
        self.show_frame("StartPage")

    def create_container(self):
        self.container = Frame(self)
        self.container.pack(side="top",fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def create_board_frame(self, board_size):
        f1 = Board(self.container, self, board_size)
        self.frames[Board.__name__] = f1

    def show_frame(self,page_name):
        self.frames[page_name].tkraise()

    def unshow_frame(self,page_name):
        self.frames[page_name].pack_forget()

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.grid(row=0,column=0,sticky=NSEW)
        self.create_vars()
        self.create_layout()

    def create_vars(self):
        self.var = StringVar()
        self.var.set("3x3") # initial value
        self.var2 = StringVar()
        self.var2.set("A*") # initial value

    def create_layout(self):
        option1 = OptionMenu(self, self.var, "3x3", "4x4")
        option1.place(relx=0.5,rely=0.4,anchor=CENTER)
        option2 = OptionMenu(self, self.var2, "A*", "IDA*")
        option2.place(relx=0.5,rely=0.5,anchor=CENTER)
        start_button = Button(self,text="START",command=self.start)
        start_button.place(relx=0.5,rely=0.6,anchor=CENTER)

    def start(self):
        # board_size = self.var.get()
        # self.controller.create_board_frame(board_size)
        self.controller.show_frame("Board")

class Board(Frame):
    def __init__(self, parent, controller, board_size="3x3"):
        Frame.__init__(self,parent)
        self.N = int(board_size[0])
        self.Nsq = self.N ** 2
        self.board = [x for x in range(1,self.Nsq + 1)]
        self.controller = controller
        self.grid(row=0,column=0,sticky=NSEW)
        self.blank = self.find_blank()
        self.create_tiles()
        self.create_controls()

    def isSolvable(self,seq=None):
        if seq == None:
            seq = list(self.state)
        else:
            pass 
        N = int(len(seq) ** 0.5)
        
        def countInv(seq):
            # function to count the number of inversions
            numinv = 0
            for i in range(0,N**2,1):
                for j in range(i+1,N**2,1):
                    if seq[i] != N**2 and seq[j] != N**2 and seq[i] > seq[j]:
                        numinv += 1
            return numinv
        
        def blankRow(seq):
            #function to find row of the blank tile (counting from bottom)
            return N - ((seq.index(N**2)) // N + 1)
        def isEven(num):
            # returns if number is even
            return num % 2 == 0
        def isOdd(num):
            # returns if number is odd
            return num % 2 == 1

        numinv = countInv(seq)
        # If grid is odd, return true if inversion 
        # count is even. 
        if isOdd(N):
            return isEven(numinv)
        else: # grid is even 
            pos = blankRow(seq)
            if isEven(pos):
                return isEven(numinv)
            else:
                return isOdd(numinv)

    def shuffle(self):
        tmp = self.board.copy()
        # while not self.isSolvable(tmp):
        random.shuffle(tmp)
        print(tmp)
        self.board = tmp.copy()
        self.create_tiles()

    def find_blank(self):
        idx = self.board.index(self.Nsq)
        return (idx // self.N, idx % self.N)

    def move(self,event):
        blank_row = self.blank[0]
        blank_col = self.blank[1]
        sym = event.keysym
        if sym not in ["Up","Down","Left","Right"]:
            pass
        else:
            if sym == "Up" and blank_row > 0:
                self.swap(-1,0)
            if sym == "Down" and blank_row < (self.N - 1):
                self.swap(1,0)
            if sym == "Left" and blank_col > 0:
                self.swap(0,-1)
            if sym == "Right" and blank_col < (self.N - 1):
                self.swap(0,1)

    def swap(self,drow,dcol):
        blank_row = self.blank[0]
        blank_col = self.blank[1]
        new_blank_row = blank_row + drow
        new_blank_col = blank_col + dcol
        but_to_swap = self.grid_slaves(row=new_blank_row,column=new_blank_col)[0]
        but_blank = self.grid_slaves(row=blank_row,column=blank_col)[0]
        but_to_swap['text'], but_blank['text'] = but_blank['text'], but_to_swap['text']
        but_to_swap['bg'], but_blank['bg'] = "red", "grey"
        old_state = self.board.copy()
        new_idx = new_blank_row * self.N + new_blank_col
        old_idx = blank_row * self.N + blank_col
        self.board[new_idx],self.board[old_idx] = self.board[old_idx], self.board[new_idx]
        self.blank = (new_blank_row,new_blank_col)
        print("old state {} and new state {} after move".format(old_state,self.board))

    def click(self,event):
        txt = event.widget['text']
        row = event.widget.grid_info()['row']
        col = event.widget.grid_info()['column']
        if (abs(row-self.blank[0]) + abs(col - self.blank[1])) == 1:
            if row == self.blank[0]:
                if col > self.blank[1]:
                    self.swap(0,1)
                else:
                    self.swap(0,-1)
            elif col == self.blank[1]:
                if row > self.blank[0]:
                    self.swap(1,0)
                else:
                    self.swap(-1,0)
        else:
            print("Click a neighbour")

    def create_controls(self):
        but_shuf = Button(self, text="Shuffle", bg="red", justify="center", font=("Arial Bold", 10),command=self.shuffle)
        but_shuf.grid(row=1,column=self.N + 2,sticky=E)
        # text_info = Text(self)
        # text_info.grid(row = self.N, columnspan=3)

    def create_tiles(self):
        for i in range(self.N):
            for j in range(self.N):
                idx = i * self.N + j
                tmp = self.board[idx]
                if tmp == self.Nsq:
                    tmp = "  "
                    but = Button(self, text="{}".format(tmp), bg="red", justify="center", width=2, font=("Arial Bold", 20))
                else:
                    but = Button(self, text="{}".format(tmp), bg="grey",justify="center", width=2, font=("Arial Bold", 20))
                but.grid(row=i,column=j)
                but.bind('<Button-1>',self.click)

if __name__ == "__main__":
    app = Game()
    app.mainloop()