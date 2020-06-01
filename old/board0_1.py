from tkinter import *
import random
from A_new import *
from IDA_new import *
import time

class Game(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("800x500")
        self.resizable(0,0)
        self.title("The N Puzzle game")
        self.var = IntVar()
        self.var.set(0)
        self.container = Frame(self)
        self.container.pack(side="top",fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.buttons = {}
        # board_frame = Board(self.container,self)
        _s = StartPage(self.container,self)
        self.show_frame("StartPage")

    def show_frame(self,frame_name):
        if frame_name == "Board":
            self.frames["StartPage"].grid_forget()
            self.frames["Board"].grid()
        elif frame_name == "StartPage":
            if "Board" in self.frames:
                self.frames["Board"].grid_forget()
            self.frames[frame_name].grid()
        else:
            pass

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent_frame = parent
        self.controller = controller
        self.create_vars()
        self.create_layout()
        # self.grid(row=0,column=0)

    def create_vars(self):
        self.var1 = StringVar()
        self.var1.set("3x3") # initial value
        self.var2 = StringVar()
        self.var2.set("A*") # initial value

    def create_layout(self):
        inner_frame = Frame(self.parent_frame)
        # inner_frame.grid()
        inner_frame.grid_columnconfigure(0,weight=1)
        inner_frame.grid_columnconfigure(1,weight=1)
        for row in range(9):
            inner_frame.grid_rowconfigure(row,weight=1)    
        lab4opt1 = Label(inner_frame,text="Choose your Board layout")
        lab4opt1.grid(row=4,column=0,sticky=E)
        option1 = OptionMenu(inner_frame, self.var1, "3x3", "4x4")
        option1.grid(row=4,column=1,sticky=W)
        lab4opt2 = Label(inner_frame,text="Choose your Solving Algorithm")
        lab4opt2.grid(row=5,column=0,sticky=E)
        option2 = OptionMenu(inner_frame, self.var2, "A*", "IDA*")
        option2.grid(row=5,column=1,sticky=W)
        lab4opt3 = Label(inner_frame,text="Hit Submit to start a Game with chosen Options")
        lab4opt3.grid(row=6,column=0,sticky=E)
        start_button = Button(inner_frame,text="START",command=self.start)
        start_button.grid(row=6,column=1,sticky=W)
        self.controller.frames["StartPage"] = inner_frame

    def start(self):
        board_size = self.var1.get()
        algo = self.var2.get()
        _b = Board(self.parent_frame,self.controller,board_size,algo)
        self.controller.show_frame("Board")

class Board(Frame):
    def __init__(self, parent, controller, board_size="4x4",solving_algorithm="A*"):
        Frame.__init__(self,parent)
        self.parent_frame = parent
        self.N = int(board_size[0])
        self.Nsq = self.N ** 2
        self.board = [x for x in range(1,self.Nsq + 1)]
        self.goal = [x for x in range(1,self.Nsq + 1)]
        self.controller = controller
        self.game_solved = True
        self.solution = ""
        self.solving_algo = solving_algorithm
        # self.grid(row=0,column=0,sticky=NSEW)
        self.blank = self.find_blank()
        self.create_content()
        self.controller.bind("<Key>",self.move)

    def isSolvable(self,seq=None):
        if seq == None:
            seq = list(self.board)
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
        random.shuffle(tmp)
        while not self.isSolvable(tmp):
            random.shuffle(tmp)
        self.board = tmp.copy()
        self.blank = self.find_blank()
        self.create_tiles()
        self.controller.var.set(0)

    def find_blank(self):
        idx = self.board.index(self.Nsq)
        return (idx // self.N, idx % self.N)

    def move(self,event):
        blank_row = self.blank[0]
        blank_col = self.blank[1]
        sym = event.keysym
        if sym not in ["Up","Down","Left","Right"]:
            self.txt_widget.insert(INSERT,"Please press one of the arrow Keys\n")
        else:
            if sym == "Up" and blank_row > 0:
                self.swap("Up",-1,0)
            if sym == "Down" and blank_row < (self.N - 1):
                self.swap("Down",1,0)
            if sym == "Left" and blank_col > 0:
                self.swap("Left",0,-1)
            if sym == "Right" and blank_col < (self.N - 1):
                self.swap("Right",0,1)

    def move_solution(self):
        def callback():
            if len(self.solution) == 0:
                self.controller.buttons["Solve"].config(state=NORMAL,bg="red")
                self.controller.buttons["Solution"].config(state=DISABLED,bg="Grey")
                self.controller.buttons["shuffle"].config(state=NORMAL,bg="red")
                return
            uldr = self.solution.pop(0)
            if uldr == "u":
                self.swap("Up",-1,0)
            if uldr == "d":
                self.swap("Down",1,0)
            if uldr == "l":
                self.swap("Left",0,-1)
            if uldr == "r":
                self.swap("Right",0,1)
            self.frame1.after(500,callback)
        self.frame1.after(500, callback)
        
    def swap(self,move_name,drow,dcol):
        blank_row = self.blank[0]
        blank_col = self.blank[1]
        new_blank_row = blank_row + drow
        new_blank_col = blank_col + dcol
        but_to_swap = self.frame1.grid_slaves(row=new_blank_row,column=new_blank_col)[0]
        but_blank = self.frame1.grid_slaves(row=blank_row,column=blank_col)[0]
        but_to_swap['text'], but_blank['text'] = but_blank['text'], but_to_swap['text']
        but_to_swap['bg'], but_blank['bg'] = "red", "grey"
        old_state = self.board.copy()
        new_idx = new_blank_row * self.N + new_blank_col
        old_idx = blank_row * self.N + blank_col
        self.board[new_idx],self.board[old_idx] = self.board[old_idx], self.board[new_idx]
        self.blank = (new_blank_row,new_blank_col)
        #update moves made
        intvartmp = self.controller.var.get() + 1
        self.controller.var.set(intvartmp)
        txt2write = "move {} made was {}\n".format(self.controller.var.get(),move_name)
        self.txt_widget.insert(INSERT,txt2write)
        self.txt_widget.see(END)
        # print("old state {} and new state {} after move".format(old_state,self.board))

    def click(self,event):
        txt = event.widget['text']
        row = event.widget.grid_info()['row']
        col = event.widget.grid_info()['column']
        if (abs(row-self.blank[0]) + abs(col - self.blank[1])) == 1:
            if row == self.blank[0]:
                if col > self.blank[1]:
                    self.swap("Right",0,1)
                else:
                    self.swap("Left",0,-1)
            elif col == self.blank[1]:
                if row > self.blank[0]:
                    self.swap("Down",1,0)
                else:
                    self.swap("Up",-1,0)
        else:
            self.txt_widget.insert(INSERT,"Click a neighbour\n")

    def create_tiles(self):
        for i in range(self.N):
            for j in range(self.N):
                idx = i * self.N + j
                tmp = self.board[idx]
                if tmp == self.Nsq:
                    tmp = "  "
                    but = Button(self.frame1, text="{}".format(tmp), bg="red", justify="center", width=2, font=("Arial Bold", 20))
                else:
                    but = Button(self.frame1, text="{}".format(tmp), bg="grey",justify="center", width=2, font=("Arial Bold", 20))
                but.grid(row=i,column=j)
                but.bind('<Button-1>',self.click)
    
    def create_content(self):
        inner_frame = Frame(self.parent_frame)
        frame0 = Frame(inner_frame)
        self.frame1 = Frame(inner_frame)
        frame2 = Frame(inner_frame)
        frame3 = Frame(inner_frame)
        # make the game status bar
        solve_status = Label(frame0, text="Is Puzzle solvable?")
        solve_status.pack(side=LEFT)
        solve_color = Label(frame0)
        if self.isSolvable():
            solve_color["text"] = "Yes"
            solve_color["bg"] = "green"
        else:
            solve_color["text"] = "No"
            solve_color["bg"] = "red"
        solve_color.pack(side=LEFT)
        moves_msg = Label(frame0,text="Moves made so far")
        moves_msg.pack(side=LEFT)
        moves_made = Label(frame0,textvariable=self.controller.var)
        moves_made.pack(side=LEFT)
        
        
        # make the NxN board
        self.create_tiles()
        
        # make game play buttons
        but_shuf = Button(frame2, text="Shuffle", bg="red", justify="center", font=("Arial Bold", 10),command=self.shuffle)
        but_shuf.pack(padx=1,side=LEFT)
        self.controller.buttons["shuffle"] = but_shuf
        but_solve = Button(frame2, text="Solve", bg="red", justify="center", font=("Arial Bold", 10),command=self.Solver)
        but_solve.pack(padx=1,side=LEFT)
        self.controller.buttons["Solve"] = but_solve
        but_play = Button(frame2, text="Solution", bg="Grey", justify="center", font=("Arial Bold", 10),state=DISABLED,command=self.move_solution)
        but_play.pack(padx=1,side=LEFT)
        self.controller.buttons["Solution"] = but_play
        but_back = Button(frame2, text="Back", bg="red", justify="center", font=("Arial Bold", 10),command=self.goToStart)
        but_back.pack(padx=1,side=LEFT)

        # make text info box
        text_info = Text(frame3,height=10)
        text_info.pack(side=BOTTOM)
        self.txt_widget = text_info
        self.txt_widget.configure(font="Helvetica 12 bold italic")
        txt2start = "Welcome to the N Puzzle game.\nPlease hit Shuffle to create a new Board to solve.\n"+\
            "You can use the arrow keys to move the blank tile around.\n"+\
            "The objective is to arrange the tiles in sequence. Good Luck\n\n\n"
        self.txt_widget.insert(INSERT,txt2start)
        # pack or grid frames
        frame0.grid(row=0,column=0,pady=10)
        self.frame1.grid(row=1,column=0,pady=10)
        frame2.grid(row=2,column=0,pady=10)
        frame3.grid(row=3,column=0)
        self.controller.frames["Board"] = inner_frame

    def goToStart(self):
        self.controller.show_frame("StartPage")

    def Solver(self):
        self.controller.buttons["shuffle"].config(state=DISABLED,bg="Grey")
        stboard = self.board
        heuristic_metric = "walking_distance"
        before = time.perf_counter()
        if self.solving_algo == "A*":
            soln,numpos = AStarSearch(heuristic_metric,stboard)
        else:
            soln,numpos = IDAStar(heuristic_metric,stboard)
        after = time.perf_counter()
        if len(soln) == 0:
            self.txt_widget.insert(INSERT,"puzzle was not solved\n")
        else:
            txt_to_print = "solved position in {} moves looking at {} positions using {} with {} heuristic.\n\
                Click Solution to see moves\n".format(len(soln)-1,numpos,self.solving_algo,heuristic_metric)
            self.txt_widget.insert(INSERT,txt_to_print)
            self.solution = list(path_as_udlr(soln))
            self.controller.buttons["Solve"].config(state=DISABLED,bg="Grey")
            self.controller.buttons["Solution"].config(state=NORMAL,bg="red")

if __name__ == "__main__":
    game = Game()
    game.mainloop()
