
from fltk import *
from collections import deque

class Langton(Fl_Double_Window):

    def __init__(self, label = "Langton's Ant"):

        Fl_Double_Window.__init__(self, 600, 800, label)
        self.loc = (150, 150)
        self.tiles = []
        self.orient = deque(["LEFT", "UP", "RIGHT", "DOWN"])
        self.cmp = {"UP": lambda a: (a[0]-1, a[1]), 
                    "DOWN": lambda a: (a[0]+1, a[1]), 
                    "LEFT": lambda a: (a[0], a[1]-1), 
                    "RIGHT": lambda a: (a[0], a[1]+1)}

        self.begin()
        for i in range(300):
            row = []
            for j in range(300):
                t = Fl_Box(i*2, j*2, 2, 2)
                t.box(FL_FLAT_BOX)
                t.color(FL_WHITE)
                row.append(t)
            
            self.tiles.append(row)

        self.but = Fl_Button(0, 600, 600, 200)
        self.but.label("NEXT")
        self.but.callback(self.step)
        self.end()
        self.show()

    def step(self, w):
        
        r, c = self.loc

        if not 0<=r<=300 or not 0<=c<=300:
            return None

        if self.tiles[r][c].color() == FL_WHITE:
            self.tiles[r][c].color(FL_BLACK)
            self.orient.rotate(-1)

        elif self.tiles[r][c].color() == FL_BLACK:
            self.tiles[r][c].color(FL_WHITE)
            self.orient.rotate(1)

        self.loc = self.cmp[self.orient[0]](self.loc)
        self.redraw()
        print(self.orient[0])
if __name__ == "__main__":
    a = Langton()
    Fl.run()