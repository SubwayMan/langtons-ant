
from fltk import *
from collections import deque
import time
import math 
import re

class Langton(Fl_Double_Window):

    """Main class that controls all aspects of the program."""

    def __init__(self, label = "Langton's Ant"):

        """Initializes object. DO NOT CALL DIRECTLY."""

        Fl_Double_Window.__init__(self, 600, 670, label)
        #starting location, empty tile grid
        self.loc = (150, 150)
        self.tiles = []
        #ant orientation and default sequence
        self.orient = deque(["LEFT", "UP", "RIGHT", "DOWN"])
        self.seq = "RL"
        #convenience functions that alter new loc based on orientation
        self.cmp = {"UP": lambda a: (a[0]-1, a[1]), 
                    "DOWN": lambda a: (a[0]+1, a[1]), 
                    "LEFT": lambda a: (a[0], a[1]-1), 
                    "RIGHT": lambda a: (a[0], a[1]+1)}

        #define 12 colors that the simulation uses
        self.colors = [FL_BLACK, FL_WHITE, FL_RED, FL_CYAN, FL_DARK_MAGENTA, FL_BLUE, FL_DARK_GREEN, FL_YELLOW, FL_DARK_RED, 
                       fl_rgb_color(252, 119, 3), fl_rgb_color(87, 23, 235), fl_rgb_color(0, 255, 4)]
        #maps specific color to certain character of seq
        self.cmap = {}
        #default sim speed
        self.waittime = 1
        #create cmap       
        self.setcmap()
        #start drawing
        self.begin()

        #menu
        self.menu = Fl_Menu_Bar(0, 0, 600, 20)
        self.menu.add("New/Sequence", 0, self.setseq)
        #tiles
        for i in range(300):
            row = []
            for j in range(300):
                t = Fl_Box(i*2, (j*2)+20, 2, 2)
                #sets box to visible and sets color
                t.box(FL_FLAT_BOX)
                t.color(FL_BLACK)
                row.append(t)
            
            #creates reference grid
            self.tiles.append(row)

        #control buttons
        #play
        self.startbut = Fl_Button(0, 620, 50, 50)
        self.startbut.label("@>")
        self.startbut.callback(self.b_cb)
        #stop/reset button
        self.stopbut = Fl_Button(550, 620, 50, 50)
        self.stopbut.label("@refresh")
        self.stopbut.callback(self.s_cb)

        #sim speed slider
        self.sl = Fl_Slider(50, 620, 500, 50)
        self.sl.type(FL_HOR_NICE_SLIDER)
        #slider bounds
        self.sl.range(0, 3)
        #slider increment
        self.sl.step(0.1)
        self.sl.callback(self.slide_cb)

        #finish initializing
        self.end()
        self.show()

    def setcmap(self):
        """Creates cmap, which maps a color(int) to a movement rule (L or R)."""

        for pos, c in enumerate(self.seq):
            self.cmap[self.colors[pos]] = c

    def setseq(self, w):
        """Prompts user for a new sequence and manages result."""

        #preemptively stop simulation
        self.s_cb(self)

        #dialog
        newseq = fl_input("Enter Sequence", "")
        #exit in case of null return
        if newseq == None:
            return None

        #validity of given string
        if re.search("^[LR]{2,12}$", newseq):
            self.reset_cb(self)
            self.seq = newseq            
            self.setcmap()
            
        else:
            fl_alert("Invalid sequence!")

        self.b_cb(self)
        
    def step(self, w=None):
        """Advances simulation to its next iteration."""
        #verbose coordinates
        r, c = self.loc
        #exits if ant is outside grid. Note that it is called before timeout can be set.
        if not 0<=r<300 or not 0<=c<300:
            return None

        #get color
        col = self.tiles[r][c].color()
        #cycle to get next color
        ncol = (self.colors.index(col)+1)%len(self.seq)
        if ncol < 0: ncol += len(self.colors)

        #rotate orientation depending on rule
        if self.cmap[col] == "R":
            self.orient.rotate(-1)

        elif self.cmap[col] == "L":
            self.orient.rotate(1)

        #set new color and location
        self.tiles[r][c].color(self.colors[ncol])
        self.loc = self.cmp[self.orient[0]](self.loc)
        #redraw tile
        self.tiles[r][c].redraw()
        #schedule next step() call
        Fl.repeat_timeout(1/self.waittime, self.step)

    def b_cb(self, w):
        
        """Starts the simulation."""
        #prevent multiple steps from happening asynchronously
        self.startbut.deactivate()
        #schedule step()
        Fl.add_timeout(1/self.waittime, self.step) 
        #set button_r to PAUSE mode instead of RESET mode
        self.stopbut.label("@#||")
        self.stopbut.callback(self.s_cb)

    def s_cb(self, w):
        """Stops the simulation."""
        #Remove scheduled call
        Fl.remove_timeout(self.step)
        #Reenable start button
        self.startbut.activate()
        #set button_r to RESET mode
        self.stopbut.label("@refresh")
        self.stopbut.callback(self.reset_cb)

    def slide_cb(self, w):
        """Handles simulation speed slider events."""
        #set the new time between step() calls
        self.waittime = math.pow(10, self.sl.value())

    def reset_cb(self, w):       
        """Resets ant back to origin position."""

        self.loc = (150, 150)
        for r in self.tiles:
            for e in r:
                #Default color is BLACK - if tampered with, order of self.colors() must be fixed
                e.color(FL_BLACK)

        #reset to original orientation
        self.orient.rotate(-1*(self.orient.index("LEFT")))
        self.redraw()

    

#create instance of program class
if __name__ == "__main__":
    a = Langton()
    Fl.run()
