import numpy as np
from scipy.spatial.distance import cityblock

# start = np.array([1,2,3,4,5,6,7,8,9,10,16,12,13,14,15,11])
start = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,15])
goal = np.array([x for x in range(1,len(start)+1)])
print(start)
moves = {"up":(0,-1),
        "down":(0,1),
        "left":(-1,0),
        "right":(1,0)}

def manhattan(A,B):
    return np.abs(A[:,None] - B).sum(-1)

def makemove(P, move):
    P = P.copy()
    N = len(P)
    dim = np.sqrt(N)
    loc = np.argmax(P)
    todo = moves[move]
    nloc = int((np.floor(loc // dim) + todo[1]) * dim + ((loc % dim) + todo[0]))
    print(loc,nloc)
    P[nloc],P[loc] = P[loc],P[nloc]
    return P

# print("up",makemove(start,"up"))
# print("down",makemove(start,"down"))
# print("left",makemove(start,"left"))
# print("right",makemove(start,"right"))
start1 = start.reshape(4,4)
goal1 = goal.reshape(4,4)   
print(cityblock(start,goal))