from tkinter import *
import random

#we need a Tile that is a Button but knows its location on the NxN board
class Tile(Button):
    def __init__(self, master=None,text=None,position=None,board=None):
        super().__init__(master=master, text=text,justify="center", width=2, font=("Arial Bold", 20))
        self.master = master
        self.position = position
        self.board = board
        self["command"] = lambda : self.swap()

    def setText(self,text=None):
        self["text"] = text
    
    def getText(self):
        return self["text"]

    def setPos(self,position=None):
        self.position = position

    def getPos(self):
        return self.position

    def isNeighbour(self,empty_pos,position):
        if position == None or position >= 16 or position < 0:
            return False
        if empty_pos == position:
            return False
        if (empty_pos - 4) == position:
            return True
        if (empty_pos + 4) == position:
            return True
        if (empty_pos - 1) == position:
            return True
        if (empty_pos + 1) == position:
            return True
        return False

    def swap(self):
        empty_pos = self.board.empty_loc
        position = self.getPos()
        if self.isNeighbour(empty_pos,position):
            self.board.state[empty_pos], self.board.state[position] = self.board.state[position], self.board.state[empty_pos]
            self.board.tiles[empty_pos].setPos(position)
            self.board.tiles[position].setPos(empty_pos)
            self.board.tiles[empty_pos], self.board.tiles[position] = self.board.tiles[position], self.board.tiles[empty_pos]
            self.board.empty_loc = position
            self.board.num_moves += 1
            self.board.drawTiles()
        else:
            print("No swap")




#we need the board to be made up of tiles    
class Board(Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.goal = [x for x in range(1,17)]
        self.state = [x for x in random.sample(range(1,17),16)]
        while not self.isSolvable():
            self.state = [x for x in random.sample(range(1,17),16)]
        self.empty_loc = self.getEmpty()
        self.solvable = True
        self.num_moves = 0
        self.min_moves = 50
        self.tiles = self.createTiles()
        self.drawTiles()
        
    def createTiles(self):
        tmp = []
        for idx,tx in enumerate(self.state):
            if tx == 16:
                tmp.append(Tile(master=self.master, text=" ", position=idx, board=self))
            else:
                tmp.append(Tile(master=self.master, text=str(tx), position=idx, board=self))
        return tmp

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
            return 4 - ((state.index(16)) // 4)

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

    def getEmpty(self):
        return self.state.index(16)

    def drawTiles(self):
        for tile in self.tiles:
            tile.grid(row=tile.position // 4,column=tile.position % 4)


if __name__ == "__main__":
    root = Tk()
    board = Board(root)
    root.mainloop()