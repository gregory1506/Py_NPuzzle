import time
from queue import PriorityQueue
from math import inf
from itertools import permutations

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

###############################################################################################################
## walking distance metric seen here --- > https://rosettacode.org/wiki/15_puzzle_solver
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
#########################################################################################################################
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
    return list(moves)

def getPath(node):
    path = []
    path.append(node.board)
    while (node.parent is not None):
        node = node.parent
        path.append(node.board)
    return path[::-1]

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

def Solve(heuristic_name,algorithm_name, board):
    if not isSolvable(board):
        print("Bad board. not solvable")
        return -1
    before = time.perf_counter()
    if algorithm_name == "A*":
        soln,numpos = AStarSearch(heuristic_name,board)
    elif algorithm_name == "IDA*":
        soln,numpos = IDAStar(heuristic_name,board)
    else:
        print("No valid solving algorithm")
        return -1
    after = time.perf_counter()
    moves_to_solve = path_as_udlr(soln)
    return (board,len(soln)-1,str(round(after - before,3)),numpos,heuristic_name,algorithm_name,moves_to_solve)

if __name__ == "__main__":

    # with open("data/3x3_astar_mh.txt","w") as f:
    #     f.write("Board  NumMoves  Time  Positions  Heuristic  Algorithm  Moves\n")
    #     index = 0
    #     for perm in permutations((1,2,3,4,5,6,7,8,9)):
    #         if not isSolvable(perm):
    #             continue
    #         index += 1
    #         answer = Solve("manhattan","A*",perm)
    #         f.write("  ".join(map(str,answer))+"\n")
    #         if index % 1000 == 0:
    #             print(answer, index)
    # index = 0
    # dict4MH = {}
    # for perm in permutations((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)):
    #     if not isSolvable(perm):
    #         continue
    #     index+=1
    #     d_mah = manhattan(perm)
    #     dict4MH[perm] = d_mah
    #     if index % 100000 == 0:
    #         print(perm,d_mah,index)



