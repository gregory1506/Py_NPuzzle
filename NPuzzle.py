######################################################################
###### NPuzzle GUI and solver ########################################
###### Gregory Ollivierre  <--> ollivierre.gregory@outlook.com  ######
###### Saturday, 30th May, 2020   ~ 22:00 EST   ######################
######################################################################

import time
from queue import PriorityQueue
from math import inf
from tkinter import *
import random

'''Method to assess if a given board layout is solvable or not'''
def isSolvable(seq):
        # function to count the number of inversions
        seq = list(seq) 
        N = int(len(seq) ** 0.5)
        def countInv(seq):
            numinv = 0
            for i in range(0,N**2,1):
                for j in range(i+1,N**2,1):
                    if seq[i] != N**2 and seq[j] != N**2 and seq[i] > seq[j]:
                        numinv += 1
            return numinv
        #function to find row of the blank tile (counting from bottom)
        def blankRow(seq):
            return N - ((seq.index(N**2)) // N)

        numinv = countInv(seq)
        # If grid is odd, return true if inversion 
        # count is even. 
        if N & 1:
            return bool(not numinv & 1)
        else: # grid is even 
            pos = blankRow(seq)
            if pos & 1:
                return bool(not numinv & 1)
            else:
                return bool(numinv & 1)

####################  DISTANCE HEURISTICS  ################################################
'''Method to implement manhattan distance metric'''
def manhattan(seq):
    result = 0
    dim = int(len(seq)**0.5)
    ref = [[x + i*dim for x in range(1,dim+1)] for i in range(dim)]
    seq2 = to2D(seq)
    for i in range(dim):
        for j in range (dim):
            if (ref[i][j] == dim**2):
                continue
            for l in range(dim):
                for m in range(dim):
                    if (ref[i][j] == seq2[l][m]):
                        result += (abs(m - j) + abs(l - i))
                        break
    return result

'''Methods to implement walking distance metric --- > https://rosettacode.org/wiki/15_puzzle_solver'''
def encode_cfg(cfg, n):
    r = 0
    b = n.bit_length()
    for i in range(len(cfg)):
        r |= cfg[i] << (b*i)
    return r
 
def gen_wd_table(n):
    goal = [[0] * i + [n] + [0] * (n - 1 - i) for i in range(n)]
    goal[-1][-1] = n - 1
    goal = tuple(sum(goal, []))
 
    table = {}
    to_visit = [(goal, 0, n-1)]
    while to_visit:
        cfg, cost, e = to_visit.pop(0)
        enccfg = encode_cfg(cfg, n)
        if enccfg in table: continue
        table[enccfg] = cost
 
        for d in [-1, 1]:
            if 0 <= e + d < n:
                for c in range(n):
                    if cfg[n*(e+d) + c] > 0:
                        ncfg = list(cfg)
                        ncfg[n*(e+d) + c] -= 1
                        ncfg[n*e + c] += 1
                        to_visit.append((tuple(ncfg), cost + 1, e+d))
 
    return table
 
def slide_wd(n, goal):
    wd = gen_wd_table(n)
    goals = {i : goal.index(i) for i in goal}
    b = n.bit_length()
    def replace_with_0(p):
        tmp = list(p)
        idnsq = tmp.index(n*n)
        tmp[idnsq] = 0
        return tuple(tmp)
    def h(p):
        p = replace_with_0(p)
        ht = 0 # Walking distance between rows.
        vt = 0 # Walking distance between columns.
        d = 0
        for i, c in enumerate(p):
            if c == 0: continue
            g = goals[c]
            xi, yi = i % n, i // n
            xg, yg = g % n, g // n
            ht += 1 << (b*(n*yi+yg))
            vt += 1 << (b*(n*xi+xg))
 
            if yg == yi:
                for k in range(i + 1, i - i%n + n): # Until end of row.
                    if p[k] and goals[p[k]] // n == yi and goals[p[k]] < g:
                        d += 2
 
            if xg == xi:
                for k in range(i + n, n * n, n): # Until end of column.
                    if p[k] and goals[p[k]] % n == xi and goals[p[k]] < g:
                        d += 2
 
        d += wd[ht] + wd[vt]
 
        return d
    return h
####################  DISTANCE HEURISTICS  ################################################
'''Method to take long format grid representation (1D array) and convert to matrix representation (2D array)'''
def to2D(seq):
    N = int(len(seq)**0.5)
    tmp = []
    for i in range(N):
        tmp.append(seq[N*i:N*(i+1)])
    return tmp

'''Method that outputs next posible moves (Up, Down, Left, Right) from a given position.''' 
def posibleMoves(seq):
    seq = list(seq)
    Nsq = len(seq)
    N = int(Nsq**0.5)
    empty_loc = seq.index(Nsq)
    row = empty_loc // N
    col = empty_loc % N
    
    def up():
        tmp = seq.copy()
        if row == 0:
            return tmp
        else:
            swap_pos = (row - 1) * N + col
            tmp[swap_pos], tmp[empty_loc] = tmp[empty_loc], tmp[swap_pos]
            return tmp

    def down():
        tmp = seq.copy()
        if row == (N - 1):
            return tmp
        else:
            swap_pos = (row + 1) * N + col
            tmp[swap_pos], tmp[empty_loc] = tmp[empty_loc], tmp[swap_pos]
            return tmp

    def left():
        tmp = seq.copy()
        if col == 0:
            return tmp
        else:
            swap_pos = (row * N) + (col - 1)
            tmp[swap_pos], tmp[empty_loc] = tmp[empty_loc], tmp[swap_pos]
            return tmp
    
    def right():
        tmp = seq.copy()
        if col == (N - 1):
            return tmp
        else:
            swap_pos = (row * N) + (col + 1)
            tmp[swap_pos], tmp[empty_loc] = tmp[empty_loc], tmp[swap_pos]
            return tmp

    moves = set()
    if up() != seq:
        moves.add(tuple(up()))
    if down() != seq:
        moves.add(tuple(down()))
    if left() != seq:
        moves.add(tuple(left()))
    if right() != seq:
        moves.add(tuple(right()))
    return list(moves)

'''Method that take final node object of solution and works backward towards parents to find complete solution path'''
def getPath(node):
    path = []
    path.append(node.board)
    while (node.parent is not None):
        node = node.parent
        path.append(node.board)
    return path[::-1]

'''Method outputs solution path as u,d,l,r which is shorthand for (Up, Down, Left, Right)'''
def path_as_udlr(solution):
    Nsq = len(solution[0])
    n = int(Nsq ** 0.5)
    move_path = ""
    for i in range(len(solution)):
        if i == 0 : continue
        before = solution[i-1].index(Nsq)
        x = before // n
        y = before % n
        after = solution[i].index(Nsq)
        i = after // n
        j = after % n
        if x == i:
            pass
        elif x > i:
            move_path += "u"
            continue
        else:
            move_path += "d"
            continue
        if y == j:
            pass
        elif y > j:
            move_path += "l"
            continue
        else:
            move_path += "r"
            continue
    return move_path

'''Method initializes a game solver given a heuristic and starting board. Returns the start and end node objects plus heuristic function'''
def game_init(heuristic_name,stboard):
    n = int(len(stboard)**0.5)
    goal_board = tuple(i % (n*n) for i in range(1, n*n+1))
    end_board = tuple(x for x in range(1,n*n +1))
    if heuristic_name == "manhattan":
        heuristic = manhattan
    if heuristic_name == "walking_distance":
        heuristic = slide_wd(n,goal_board)   
    g = 0
    h = heuristic(stboard)
    f = g + h
    start = Node(stboard,None,g,h,f)
    goal = Node(end_board,None,0,0,0)
    return start,goal,heuristic

'''Implements A* search algorithm'''
def AStarSearch(heuristic_name,board):
    start,goal,heuristic = game_init(heuristic_name,board)
    openset = PriorityQueue()
    closedset = {}
    openset.put(start)
    positions_seen = 0

    while not openset.empty():
        current = openset.get()
        closedset[current.board] = (current.g, current.h, current.f)
        positions_seen += 1
        if current == goal:
            return getPath(current),positions_seen
        for move in posibleMoves(current.board):
            newg = current.g + 1
            h = heuristic(move)
            f = newg + h
            if move in closedset:
                if newg < closedset[move][0]:
                    node = Node(move,current,newg,h,f)
                    openset.put(node)
                    del closedset[move]
                    continue
                else:
                    continue
            node = Node(move,current,newg,h,f)
            openset.put(node)
            
        if positions_seen % 100000 == 0:
            print("{} positions analyzed...".format(positions_seen))
        if positions_seen > 20000000:
            break
    return [],0

'''Implements Iterative Deepening A* (IDA*) search algorithm'''
def IDAStar(heuristic_name,board):
    
    def search(path, is_in_path, g, threshold, num_positions_evaluated):
        num_positions_evaluated += 1
        current = path[-1]
        if num_positions_evaluated % 100000 == 0:
            print("{} positions analyzed...".format(num_positions_evaluated))
        newf = g + heuristic(current)
        if newf > threshold:
            return newf,num_positions_evaluated
        if current == goal:
            return FOUND,num_positions_evaluated
        minimum = inf
        for move in posibleMoves(current):
            if move in is_in_path:
                continue
            path.append(move)
            is_in_path.add(move)
            t,num_positions_evaluated = search(path, is_in_path, g+1, threshold, num_positions_evaluated)
            if t == FOUND:return FOUND,num_positions_evaluated
            if t < minimum:minimum = t
            path.pop()
            in_path.remove(move)
        return minimum,num_positions_evaluated

    start,goaln,heuristic = game_init(heuristic_name,board)
    goal = goaln.board
    num_positions_evaluated = 0
    threshold = heuristic(board)
    path = [board]
    in_path = set()
    FOUND = object()
    while True:
        t, num_positions_evaluated = search(path, in_path, 0, threshold, num_positions_evaluated)
        if t == FOUND:
            return path,num_positions_evaluated
        elif t is inf:
            return [], num_positions_evaluated
        else:
            threshold = t

'''Wrapper function for finding search solution'''
def Solve(heuristic_name_short,algorithm_name, board):
    if not isSolvable(board):
        print("Bad board. not solvable")
        return -1
    if heuristic_name_short == "WD":
        heuristic_name = "walking_distance"
    else:
        heuristic_name = "manhattan"
    before = time.perf_counter()
    if algorithm_name == "A*":
        soln,numpos = AStarSearch(heuristic_name,board)
    elif algorithm_name == "IDA*":
        soln,numpos = IDAStar(heuristic_name,board)
    else:
        print("No valid solving algorithm")
        return -1
    after = time.perf_counter()
    moves_to_solve = list(path_as_udlr(soln))
    return (board,len(soln)-1,str(round(after - before,3)),numpos,heuristic_name,algorithm_name,moves_to_solve,soln)

'''Class to abstract the connection to board layout and moves'''
class Node:
    def __init__(self,board,parent,g,h,f):
        self.board = tuple(board)
        self.parent = parent
        self.g = g # moves so far
        self.h = h # estimate of distance to goal
        self.f = f # cost of current node ( g + h)

    def __lt__(self,other):
        ''' Defines how a node is less than another '''
        return self.f < other.f

    def __eq__(self,other):
        ''' Defines how two nodes are equal '''
        return self.board == other.board

'''Class to implement Game Window GUI container and variables'''
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

'''Implements first page of the GUI so user can select options'''
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
        self.var3 = StringVar()
        self.var3.set("WD")

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
        lab4opt3 = Label(inner_frame,text="Choose Distance Heuristic Manhattan/WalkingDistance")
        lab4opt3.grid(row=6,column=0,sticky=E)
        option3 = OptionMenu(inner_frame, self.var3, "WD", "MH")
        option3.grid(row=6,column=1,sticky=W)
        lab4opt3 = Label(inner_frame,text="Hit Submit to start a Game with chosen Options")
        lab4opt3.grid(row=7,column=0,sticky=E)
        start_button = Button(inner_frame,text="START",command=self.start)
        start_button.grid(row=7,column=1,sticky=W)
        self.controller.frames["StartPage"] = inner_frame

    def start(self):
        board_size = self.var1.get()
        algo = self.var2.get()
        heuristic = self.var3.get()
        _b = Board(self.parent_frame,self.controller,board_size,algo,heuristic)
        self.controller.show_frame("Board")

'''Abstraction of Board logic and implements main game GUI'''
class Board(Frame):
    def __init__(self, parent, controller, board_size="4x4",solving_algorithm="A*",heuristic_name="WD"):
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
        self.heuristic_name = heuristic_name
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
        self.solution = ""
        self.game_solved = False

    def make_Toplevel(self):
        top = Toplevel()
        top.title("Message")
        msg = Message(top, text="SOLVED!!")
        msg.pack()
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()

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
        if self.game_solved == False and self.board == self.goal:
            self.make_Toplevel()
        else:
            pass

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
        but_quit = Button(frame2, text="Quit", bg="red", justify="center", font=("Arial Bold", 10),command=self.controller.destroy)
        but_quit.pack(padx=1,side=LEFT)

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
        stboard,num_moves,time4soln,positions_look,hname,algo,moves2solve,soln = Solve(self.heuristic_name,self.solving_algo,self.board)
        if len(soln) == 0:
            self.txt_widget.insert(INSERT,"puzzle was not solved\n")
        else:
            txt_to_print = "solved position in {} moves looking at {} positions using {} with {} heuristic.\n\
                Click Solution to see moves\n".format(num_moves,positions_look,algo,hname)
            self.txt_widget.insert(INSERT,txt_to_print)
            self.solution = moves2solve
            self.controller.buttons["Solve"].config(state=DISABLED,bg="Grey")
            self.controller.buttons["Solution"].config(state=NORMAL,bg="red")

if __name__ == "__main__":
    game = Game()
    game.mainloop()

