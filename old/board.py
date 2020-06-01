import random
from tkinter import *
blank = (3,3)
state=[x for x in range(1,17)]
def move(event):
    global blank
    global state
    blank_row = blank[0]
    blank_col = blank[1]
    sym = event.keysym
    if sym not in ["Up","Down","Left","Right"]:
        pass
    else:
        if sym == "Up" and blank_row > 0:
            swap(master,-1,0)
        if sym == "Down" and blank_row < 3:
            swap(master,1,0)
        if sym == "Left" and blank_col > 0:
            swap(master,0,-1)
        if sym == "Right" and blank_col < 3:
            swap(master,0,1)

def swap(master,drow,dcol):
    global state
    global blank
    N = int(len(state)**0.5)
    blank_row = blank[0]
    blank_col = blank[1]
    new_blank_row = blank_row + drow
    new_blank_col = blank_col + dcol
    but_to_swap = master.grid_slaves(row=new_blank_row,column=new_blank_col)[0]
    but_blank = master.grid_slaves(row=blank_row,column=blank_col)[0]
    but_to_swap['text'], but_blank['text'] = but_blank['text'], but_to_swap['text']
    but_to_swap['bg'], but_blank['bg'] = "red", "grey"
    old_state = state.copy()
    state[new_blank_row * N + new_blank_col], state[blank_row * N + blank_col] = state[blank_row * N + blank_col], state[new_blank_row * N + new_blank_col]
    blank = (new_blank_row,new_blank_col)
    print("old state {} and new state {} after move".format(old_state,state))

def click(event):
    global blank
    txt = event.widget['text']
    row = event.widget.grid_info()['row']
    col = event.widget.grid_info()['column']
    if (abs(row-blank[0]) + abs(col - blank[1])) == 1:
        print("Hello I am button {} in row {} and col {} and I'm a neighbour".format(txt,row,col))
    else:
        print("Hello I am button {} in row {} and col {} not your neighbour".format(txt,row,col))

def create_tiles(master,state):
    N = int(len(state)**0.5)
    for i in range(N):
        for j in range(N):
            idx = i * N + j
            tmp = state[idx]
            if tmp == N**2:
                tmp = "  "
                but = Button(master=master, text="{}".format(tmp), bg="red", justify="center", width=2, font=("Arial Bold", 20))
            else:
                but = Button(master=master, text="{}".format(tmp), bg="grey",justify="center", width=2, font=("Arial Bold", 20))
            but.grid(row=i,column=j)
            but.bind('<Button-1>',click)

if __name__ == "__main__":
    master = Tk()
    create_tiles(master,state)
    master.bind("<Key>", move) 
    master.mainloop()