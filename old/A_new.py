import time
from queue import PriorityQueue

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

test1 = [9,1,3,4,2,6,7,5,8] # 4 moves
test2 = [6,5,4,1,7,3,9,8,2] # 26 moves
test3 = [7,9,13,1,14,16,8,15,3,6,10,5,2,11,12,4] # 58 moves 
test4 = [15,14,1,6,9,11,4,12,16,10,7,3,13,8,5,2] # 52 moves --> https://rosettacode.org/wiki/15_puzzle_solver#A.2A_with_good_heuristic
test5 = [2,8,3,1,6,4,7,9,5] # 18 moves --> https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
test6 = [8,6,7,2,5,4,3,9,1] # 31 moves
test6b = [6,4,7,8,5,9,3,2,1] # 31 moves --> http://kevingong.com/Math/SixteenPuzzle.html
test7 = [7,14,16,9,10,2,11,13,6,15,4,12,5,1,8,3] # 54 moves -- > https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
test8 = [5,1,2,3,6,16,7,4,9,10,11,8,13,14,15,12] # 8 moves -- > https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
test9 = [7,8,4,11,12,14,10,15,16,5,3,13,2,1,9,6] # 50 moves -- > https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
test10 = [1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16] # lower bound 40 moves --> https://www.ic-net.or.jp/home/takaken/nt/slide/solve15.html
test11 = [15,14,8,12,10,11,9,13,2,6,5,1,3,7,4,16] # 80 moves --> https://puzzling.stackexchange.com/questions/24265/what-is-the-superflip-on-15-puzzle
test_1 = [3,6,9,8,10,1,16,11,5,2,7,13,12,15,4,14] # 53 moves




if __name__ == "__main__":
    stboard = test_1
    if not isSolvable(stboard):
        print("Bad board. not solvable")
        raise SystemExit
    before = time.perf_counter()
    # heuristic_metric = "manhattan"
    heuristic_metric = "walking_distance"
    soln,numpos = AStarSearch(heuristic_metric,stboard)
    after = time.perf_counter()
    if len(soln) == 0:
        print("was not solved")
        raise SystemExit
    else:
        print("solved {} position in {} moves over {} seconds looking at {} positions with {} heuristic".format(stboard,len(soln)-1,str(round(after - before,3)),numpos,heuristic_metric))
    print(path_as_udlr(soln))
