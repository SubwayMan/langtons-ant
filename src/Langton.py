
from fltk import *
from collections import deque
import time
import math 

class Langton(Fl_Double_Window):

    def __init__(self, label = "Langton's Ant"):

        Fl_Double_Window.__init__(self, 600, 650, label)
        self.loc = (150, 150)
        self.tiles = []
        self.orient = deque(["LEFT", "UP", "RIGHT", "DOWN"])
        self.cmp = {"UP": lambda a: (a[0]-1, a[1]), 
                    "DOWN": lambda a: (a[0]+1, a[1]), 
                    "LEFT": lambda a: (a[0], a[1]-1), 
                    "RIGHT": lambda a: (a[0], a[1]+1)}

        self.colors = [FL_BLACK, FL_WHITE, FL_GRAY0, FL_RED, FL_DARK_MAGENTA, FL_CYAN, FL_BLUE, FL_DARK_GREEN]
        self.waittime = 1
        self.begin()

        for i in range(300):
            row = []
            for j in range(300):
                t = Fl_Box(i*2, j*2, 2, 2)
                t.box(FL_FLAT_BOX)
                t.color(FL_WHITE)
                row.append(t)
            
            self.tiles.append(row)

        self.startbut = Fl_Button(0, 600, 50, 50)
        self.startbut.label("START")
        self.startbut.callback(self.b_cb)
        self.stopbut = Fl_Button(550, 600, 50, 50)
        self.stopbut.label("STOP")
        self.stopbut.callback(self.s_cb)

        #slider
        self.sl = Fl_Slider(50, 600, 500, 50)
        self.sl.type(FL_HOR_NICE_SLIDER)
        self.sl.range(0, 3)
        self.sl.step(0.1)
        self.sl.callback(self.slide_cb)

        self.end()
        self.show()

    def step(self, w=None):
        
        r, c = self.loc

        if not 0<=r<300 or not 0<=c<300:
            return None

        if self.tiles[r][c].color() == FL_WHITE:
            self.tiles[r][c].color(FL_BLACK)
            self.orient.rotate(-1)

        elif self.tiles[r][c].color() == FL_BLACK:
            self.tiles[r][c].color(FL_WHITE)
            self.orient.rotate(1)

        self.loc = self.cmp[self.orient[0]](self.loc)
        self.tiles[r][c].redraw()
        Fl.repeat_timeout(1/self.waittime, self.step)

    def b_cb(self, w):
        
        self.startbut.deactivate()
        Fl.add_timeout(1/self.waittime, self.step) 

    def s_cb(self, w):
        Fl.remove_timeout(self.step)
        self.startbut.activate()

    def slide_cb(self, w):

        print(w.value())
        self.waittime = math.pow(10, self.sl.value())
       
if __name__ == "__main__":
    a = Langton()
    Fl.run()
