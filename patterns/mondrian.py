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
HeightMax = panPxPerEdge
WidthMin = 2
WidthMax = panPxPerEdge
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
    x = random.randint(0, panPxPerEdge-1)
    y = random.randint(0, panPxPerEdge-1)
    height = random.randint(HeightMin, HeightMax)
    width = random.randint(WidthMin, WidthMax)
    hue = random.random()
    rect = Rect()
    rect.setDims((pan,x,y, height, width)) 
    rect.setCol((hue,1.0,ValueMax))
    rects.append(rect)


def iterateRects():
    for rect in rects:
        rect.age += 1
        if rect.age >= AgeMax: continue

        ran = random.randint(0,7) #
        side = ran//2 # 0-top, 1-bottom, 2-left, 3-right
        grow = ran%2 # 0-shrink, 1-grow
        if side == 0: # Top
            if grow:
                rect.height = min(HeightMax, rect.height+1)
                rect.x = max(0, rect.x-1)
            else:
                rect.height = max(HeightMin, rect.height-1)
                rect.x = min(panPxPerEdge-1-rect.height, rect.x + 1)
        elif side == 1: # Bottom
            if grow: rect.height += 1
            else: rect.height -= 1
        elif side == 2: # Left
            if grow:
                rect.y -= 1
                rect.width += 1
            else:
                rect.y += 1
                rect.width -= 1
        else: # Right
            if grow: rect.width += 1
            else: rect.width -= 1


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