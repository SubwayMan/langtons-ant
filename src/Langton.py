
from fltk import *
from collections import deque
import time
import math 
import re

class Langton(Fl_Double_Window):

    def __init__(self, label = "Langton's Ant"):

        Fl_Double_Window.__init__(self, 600, 670, label)
        self.loc = (150, 150)
        self.tiles = []
        self.orient = deque(["LEFT", "UP", "RIGHT", "DOWN"])
        self.seq = "RL"
        self.cmp = {"UP": lambda a: (a[0]-1, a[1]), 
                    "DOWN": lambda a: (a[0]+1, a[1]), 
                    "LEFT": lambda a: (a[0], a[1]-1), 
                    "RIGHT": lambda a: (a[0], a[1]+1)}

        self.colors = [FL_BLACK, FL_WHITE, FL_RED, FL_CYAN, FL_DARK_MAGENTA, FL_BLUE, FL_DARK_GREEN, FL_YELLOW, FL_DARK_RED, 
                       fl_rgb_color(252, 119, 3), fl_rgb_color(87, 23, 235), fl_rgb_color(0, 255, 4)]
        self.cmap = {}
        self.waittime = 1

        self.setcmap()
      
        self.begin()

        #menu
        self.menu = Fl_Menu_Bar(0, 0, 600, 20)
        self.menu.add("New/Sequence", 0, self.setseq)
        for i in range(300):
            row = []
            for j in range(300):
                t = Fl_Box(i*2, (j*2)+20, 2, 2)
                t.box(FL_FLAT_BOX)
                t.color(FL_BLACK)
                row.append(t)
            
            self.tiles.append(row)

        self.startbut = Fl_Button(0, 620, 50, 50)
        self.startbut.label("@>")
        self.startbut.callback(self.b_cb)
        self.stopbut = Fl_Button(550, 620, 50, 50)
        self.stopbut.label("@refresh")
        self.stopbut.callback(self.s_cb)

        #slider
        self.sl = Fl_Slider(50, 620, 500, 50)
        self.sl.type(FL_HOR_NICE_SLIDER)
        self.sl.range(0, 3)
        self.sl.step(0.1)
        self.sl.callback(self.slide_cb)

        self.end()
        self.show()

    def setcmap(self):

        for pos, c in enumerate(self.seq):
    
            self.cmap[self.colors[pos]] = c

    def setseq(self, w):

        self.s_cb(self)

        newseq = fl_input("Enter Sequence", "")

        if newseq == None:
            return None

        if re.search("^[LR]{2,12}$", newseq):
            self.reset_cb(self)
            self.seq = newseq            
            self.setcmap()
            self.b_cb(self)

    def step(self, w=None):
        
        r, c = self.loc

        if not 0<=r<300 or not 0<=c<300:
            return None

        col = self.tiles[r][c].color()
        ncol = (self.colors.index(col)+1)%len(self.seq)
        if ncol < 0: ncol += len(self.colors)

        if self.cmap[col] == "R":
            self.orient.rotate(-1)

        elif self.cmap[col] == "L":
            self.orient.rotate(1)

        self.tiles[r][c].color(self.colors[ncol])
        self.loc = self.cmp[self.orient[0]](self.loc)
        self.tiles[r][c].redraw()
        Fl.repeat_timeout(1/self.waittime, self.step)

    def b_cb(self, w):
        
        self.startbut.deactivate()
        Fl.add_timeout(1/self.waittime, self.step) 
        self.stopbut.label("@#||")
        self.stopbut.callback(self.s_cb)

    def s_cb(self, w):
    	
        Fl.remove_timeout(self.step)
        self.startbut.activate()
        self.stopbut.label("@refresh")
        self.stopbut.callback(self.reset_cb)

    def slide_cb(self, w):

        self.waittime = math.pow(10, self.sl.value())

    def reset_cb(self, w):       
        
        self.loc = (150, 150)
        for r in self.tiles:
            for e in r:
                e.color(FL_BLACK)

        self.orient.rotate(-1*(self.orient.index("LEFT")))
        self.redraw()

    



if __name__ == "__main__":
    a = Langton()
    Fl.run()
