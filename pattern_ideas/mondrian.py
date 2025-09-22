## INCOMPLETE ##
import random, time, array
from collections import deque
# from ucollections import deque
# from micropython import schedule
# from machine import Timer
from colorsys import hsv_to_rgb

PIN = 0; SM = 1; AR = 2 # panel indices
maxrects = 4
rects = deque([], maxrects)
panPxPerEdge = 4; panAcross = 4; panDown = 4

HueCentre = 0.5
HueWidth = 0.5
ValueMax = 0.1
ValueMin = 0
ValueInc = (ValueMax - ValueMin) / 100
HeightMin = 2
HeightMax = panPxPerEdge-2
WidthMin = 2
WidthMax = panPxPerEdge-2
AgeMax = 100

shiftleft = 8 # at sm.put(array, shift)

class Rect:
    pan=0; x=0; y=0
    height=0; width=0
    h=0; s=0; v=0
    age=1

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
                setattr(self, key, value)
    
    def setDims(self, posi):
        self.pan = posi[0]
        self.x = posi[1]
        self.y = posi[2]
        self.height = posi[3]
        self.width = posi[4]

    def getDims(self):
        return (self.pan, self.x, self.y, self.height, self.width)
      
    def setCol(self, col):
        self.h = col[0]
        self.s = col[1]
        self.v = col[2]

    def getCol(self):
        return (self.h, self.s, self.v)


def wheel(hue=0.333, sat=1.0, val_br=0.05):
    r,g,b = hsv_to_rgb(hue, sat, val_br) # pyright: ignore[reportGeneralTypeIssues]
    red = int(round(255*r))
    green = int(round(255*g))
    blue = int(round(255*b))
    return (red, green, blue)


def cycle(t):
    if rects and rects[0].age == AgeMax:
        rects.popleft()
    
    if len(rects) < maxrects:
        makeRect()

    renderRects()
    iterateRects()
    

def makeRect():
    pan = random.randint(0, 5) # TODO make this generic for Wall or Cube
    height = random.randint(HeightMin, HeightMax)
    width = random.randint(WidthMin, WidthMax)
    x = random.randint(0, panPxPerEdge-1-width)
    y = random.randint(0, panPxPerEdge-1-height)
    hue = random.random()
    rect = Rect()
    rect.setDims((pan,x,y, height, width)) 
    rect.setCol((hue,1.0,ValueMax))
    rects.append(rect)


def iterateRects(): #TODO for now this is just per panel, not crossing edges
    for rect in rects:
        rect.age += 1
        if rect.age >= AgeMax: continue

        ran = random.randint(0,7) #
        side = ran//2 # 0-top, 1-bottom, 2-left, 3-right
        grow = ran%2 # 0-shrink, 1-grow
        if side == 0: # Top
            if grow: 
                if rect.y > 0 and rect.height < HeightMax:
                    rect.y -= 1
                    rect.height += 1
            else:
                if rect.height > HeightMin:
                    rect.height -= 1
                    rect.y += 1 #NOTE not checking bounds here
        elif side == 1: # Bottom
            if grow: 
                if rect.height < HeightMax:
                    rect.height += 1
            else: 
                if rect.height > HeightMin:
                    rect.height -= 1
        elif side == 2: # Left
            if grow: 
                if rect.x > 0 and rect.width < WidthMax:
                    rect.x -= 1
                    rect.width += 1
            else:
                if rect.width > WidthMin:
                    rect.width -= 1
                    rect.x += 1 #NOTE not checking bounds here
        else: # Right
            if grow: 
                if rect.width < WidthMax:
                    rect.width += 1
            else: 
                if rect.width > WidthMin:
                    rect.width -= 1


def printRects():
    for rect in rects:
        # print(hex(id(rect)), rect.getDims(), rect.getCol())
        print(hex(id(rect)), 'age:', rect.age, 'dims:', rect.getDims())


def renderRects():
    printRects()
    # #clear array of previous data
    # for pan in panels.values(): #TODO do more efficentnly
    #     for j in range(size):
    #         pan[AR][j] = 0

    # #write snakes to arrays
    # for px in stars:
    #     pan,x,y = px.getPosi() #Px Class
    #     r,g,b = wheel(px.getCol())
    #     panelarray = panels[pan][AR]
    #     panelarray[y*panPxPerEdge + x] = r<<8 | g<<16 | b

    # #write each array to corresponding panel
    # for pan in panels.values(): 
    #     pan[SM].put(pan[AR], shiftleft)
    #     time.sleep_ms(10) # should get an interrupt for this


### execution ###
panPxPerEdge = 8
for i in range(3):
    cycle(0)
    time.sleep(0.1)