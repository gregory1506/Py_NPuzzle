# =Iterative Depth A*===
# From https://codegolf.stackexchange.com/questions/6884/solve-the-15-puzzle-the-tile-sliding-puzzle

# Solution titled "PyPy, 195 moves, ~12 seconds computation"

# Modified to run this task's 52 move problem.
# ==
# <lang Python>
import random
import time
class IDAStar:
    def __init__(self, h, neighbours):
        """ Iterative-deepening A* search.

        h(n) is the heuristic that gives the cost between node n and the goal node. It must be admissable, meaning that h(n) MUST NEVER OVERSTIMATE the true cost. Underestimating is fine.

        neighbours(n) is an iterable giving a pair (cost, node, descr) for each node neighbouring n
        IN ASCENDING ORDER OF COST. descr is not used in the computation but can be used to
        efficiently store information about the path edges (e.g. up/left/right/down for grids).
        """

        self.h = h
        self.neighbours = neighbours
        self.FOUND = object()


    def solve(self, root, is_goal, max_cost=None):
        """ Returns the shortest path between the root and a given goal, as well as the total cost.
        If the cost exceeds a given max_cost, the function returns None. If you do not give a
        maximum cost the solver will never return for unsolvable instances."""

        self.is_goal = is_goal
        self.path = [root]
        self.is_in_path = {root}
        self.path_descrs = []
        self.nodes_evaluated = 0

        bound = self.h(root)

        while True:
            t = self._search(0, bound)
            if t is self.FOUND: return self.path, self.path_descrs, bound, self.nodes_evaluated
            if t is None: return None
            bound = t

    def _search(self, g, bound):
        self.nodes_evaluated += 1
        if self.nodes_evaluated % 100000 == 0:
            print("{} positions analyzed...".format(self.nodes_evaluated))
        node = self.path[-1]
        f = g + self.h(node)
        if f > bound: return f
        if self.is_goal(node): return self.FOUND

        m = None # Lower bound on cost.
        for cost, n, descr in self.neighbours(node):
            if n in self.is_in_path: continue

            self.path.append(n)
            self.is_in_path.add(n)
            self.path_descrs.append(descr)
            t = self._search(g + cost, bound)

            if t == self.FOUND: return self.FOUND
            if m is None or (t is not None and t < m): m = t

            self.path.pop()
            self.path_descrs.pop()
            self.is_in_path.remove(n)

        return m


def slide_solved_state(n):
    return tuple(i % (n*n) for i in range(1, n*n+1))

def slide_randomize(p, neighbours):
    for _ in range(len(p) ** 2):
        _, p, _ = random.choice(list(neighbours(p)))
    return p

def slide_neighbours(n):
    movelist = []
    for gap in range(n*n):
        x, y = gap % n, gap // n
        moves = []
        if x > 0: moves.append(-1)    # Move the gap left.
        if x < n-1: moves.append(+1)  # Move the gap right.
        if y > 0: moves.append(-n)    # Move the gap up.
        if y < n-1: moves.append(+n)  # Move the gap down.
        movelist.append(moves)

    def neighbours(p):
        gap = p.index(0)
        l = list(p)

        for m in movelist[gap]:
            l[gap] = l[gap + m]
            l[gap + m] = 0
            yield (1, tuple(l), (l[gap], m))
            l[gap + m] = l[gap]
            l[gap] = 0

    return neighbours

def slide_print(p):
    n = int(round(len(p) ** 0.5))
    l = len(str(n*n))
    for i in range(0, len(p), n):
        print(" ".join("{:>{}}".format(x, l) for x in p[i:i+n]))

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

    def h(p):
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




if __name__ == "__main__":
    solved_state = slide_solved_state(4)
    neighbours = slide_neighbours(4)
    is_goal = lambda p: p == solved_state
    test1 = [9,1,3,4,2,6,7,5,8]
    test2 = [6,5,4,1,7,3,0,8,2]
    test3 = [7,9,13,1,14,0,8,15,3,6,10,5,2,11,12,4] # 58 moves 
    test4 = [15,14,1,6,9,11,4,12,0,10,7,3,13,8,5,2] # 52 moves --> https://rosettacode.org/wiki/15_puzzle_solver#A.2A_with_good_heuristic
    test5 = [4,2,0,8,3,6,7,5,1] # 20 moves --> https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
    test6 = [8,6,7,2,5,4,3,9,1]
    test7 = [7,14,0,9,10,2,11,13,6,15,4,12,5,1,8,3] # 54 moves -- > https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
    test8 = [5,1,2,3,6,0,7,4,9,10,11,8,13,14,15,12] # 8 moves -- > https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
    test9 = [7,8,4,11,12,14,10,15,0,5,3,13,2,1,9,6] # 50 moves -- > https://www.d.umn.edu/~tcolburn/cs2511/slides.new/state_space_search/benchmarks.xhtml
    test10 = [1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,0] # lower bound 40 moves --> https://www.ic-net.or.jp/home/takaken/nt/slide/solve15.html
    # tests = [
    #     # (15, 14, 1, 6, 9, 11, 4, 12, 0, 10, 7, 3, 13, 8, 5, 2),
    #     (7,9,13,1,14,0,8,15,3,6,10,5,2,11,12,4),
    # ]
    before = time.perf_counter()
    slide_solver = IDAStar(slide_wd(4, solved_state), neighbours)
    
    # for p in tests:
    #     path, moves, cost, num_eval = slide_solver.solve(p, is_goal, 80)
    #     slide_print(p)
    #     print(", ".join({-1: "Left", 1: "Right", -4: "Up", 4: "Down"}[move[1]] for move in moves))
    #     print(cost, num_eval)
    p = tuple(test1)
    path, moves, cost, num_eval = slide_solver.solve(p, is_goal, 80)
    slide_print(p)
    print(", ".join({-1: "Left", 1: "Right", -4: "Up", 4: "Down"}[move[1]] for move in moves))
    print(cost, num_eval)
    after = time.perf_counter()
    print("Run time in seconds: "+str(after - before))
# </lang>

# Output - this solution of the problem for this task is the same as the second solution:

# rrruldluuldrurdddluulurrrdlddruldluurddlulurruldrrdd

# Profiling with standard Python 3.7 took 30 seconds.

# <pre>
# 15 14  1  6
#  9 11  4 12
#  0 10  7  3
# 13  8  5  2
# Right, Right, Right, Up, Left, Down, Left, Up, Up, Left, Down, Right, Up, Right, Down, Down, Down, Left, Up, Up, Left, Up, Right, Right, Right, Down, Left, Down, Down, Right, Up, Left, Down, Left, Up, Up, Right, Down, Down, Left, Up, Left, Up, Right, Right, Up, Left, Down, Right, Right, Down, Down
# 52 872794
# </pre>
