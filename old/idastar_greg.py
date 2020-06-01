# implement the A* algorithm for 15 puzzle
import random
from time import sleep
from collections import deque
from math import inf

class Node:

    def __init__(self, board=None, parent=None):
        self.board = board
        self.parent = parent

        self.g = 0  #start node distance (basically number of moves made)
        self.h = 0  #distance to end (essentially the manhattan heuristic)
        self.f = 0  #sum of the two
        self.identifier = str(self.board)

    # method to compare 2 nodes
    def __eq__(self, second):
        return self.board == second.board

    # method to help sort the nodes. Only need less than
    def __lt__(self, second):
        return self.f < second.f  # compare f scores

    def __hash__(self):
        return hash(self.id)

def isSolvable(seq):
        # function to count the number of inversions 
        N = int(len(seq) ** 0.5)
        def countInv(seq):
            numinv = 0
            for i in range(0,N**2,1):
                for j in range(i+1,N**2,1):
                    if seq[i] > seq[j]:
                        numinv += 1
            return numinv
        #function to find row of the blank tile (counting from bottom)
        def blankRow(seq):
            return N - ((seq.index(N**2)) // N)

        isNeven = bool((N + 1) % 2)
        isEvenRow = bool((blankRow(seq) + 1) % 2)
        isNinv = bool((countInv(seq) + 1) % 2)
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

def strPuzzle(seq):
    Nsq = len(seq)
    N = int(Nsq**0.5)
    tmp = list(map(str,seq))
    tmp = [x.rjust(2," ") for x in tmp]
    lin = "+" + "++"*N*2 + "+"+"\n"
    for i in range(N):
        lin += "++ " + " ".join(tmp[N*i:N*(i+1)]) + "  ++\n"
    lin += "+" + "++"*N*2 + "+"+"\n"
    lin = lin.replace(str(Nsq)," "*(Nsq//10 + 1))
    return lin

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

def to2D(seq):
    N = int(len(seq)**0.5)
    tmp = []
    for i in range(N):
        tmp.append(seq[N*i:N*(i+1)])
    return tmp

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
    # return list(map(list,moves))
    return list(moves)

def getPath(node):
    path = []
    path.append(node.board)
    while (node.parent is not None):
        node = node.parent
        path.append(node.board)
    return path[::-1]

def IDA_search(start_board):
    #Perfomn DFS up to threshold
    
    def _search(path, is_in_path, g, threshold, num_positions_evaluated):
        num_positions_evaluated += 1
        current = path[-1]
        f = g + manhattan(current)
        if num_positions_evaluated % 100000 == 0:
            print(current, goal, g, manhattan(current),f, threshold,num_positions_evaluated)
            # sleep(0.1)
        if f > threshold:
            return f, num_positions_evaluated, current
        if current == goal:
            return True, num_positions_evaluated, current
        minimum = inf
        for move in posibleMoves(current):
            if move in is_in_path:
                continue
            path.append(move)
            is_in_path.add(move)
            t, num_positions_evaluated , cnode= _search(path, is_in_path, g+1, threshold, num_positions_evaluated)
            if t is True:
                return True, num_positions_evaluated, cnode
            if t < minimum:
                minimum = t
            path.pop()
            is_in_path.remove(move)
        return minimum, num_positions_evaluated, current

    
    
    # start = Node(board=start_board,parent=None)
    # end = Node(board=goal,parent=None)

    # start.g = 0
    # start.h = manhattan(start_board)
    # start.f = start.g + start.h
    num_positions_evaluated = 0
    goal = tuple(x for x in range(1,len(start_board)+1))
    threshold = manhattan(start_board)
    path = [start_board]
    is_in_path = set()
    while True:
        t, num_positions_evaluated, cnode = _search(path, is_in_path, 0, threshold, num_positions_evaluated)
        if t is True:
            return path, num_positions_evaluated
        elif t is inf:
            return [], num_positions_evaluated
        else:
            threshold = t
        # print(t,num_positions_evaluated)
    return "END"
        


test1 = [9,1,3,4,2,6,7,5,8]
test2 = [6,5,4,1,7,3,9,8,2]
test3 = [7,9,13,1,14,16,8,15,3,6,10,5,2,11,12,4]
test4 = [15,14,1,6,9,11,4,12,16,10,7,3,13,8,5,2]
stboard = test3

soln, positions = IDA_search(stboard)
# soln, numiter, status = IDA_search(test2)
# soln = aStar2(test2,heuristic2)
if len(soln) == 0:
    print("was not solved")
else:
    print("solved in {} moves after looking at {} positions ".format(len(soln)-1, positions))
print(soln)