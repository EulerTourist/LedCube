import random, time, array
# from collections import deque
from ucollections import deque
# from micropython import schedule
# from machine import Timer
from colorsys import hsv_to_rgb

PIN = 0; SM = 1; AR = 2
maxstars = 16
stars = deque([], maxstars)
panPxPerEdge = 2; panAcross = 2; panDown = 2
HueCentre = 0.5
HueWidth = 0.5
ValueMax = 0.1
ValueMin = 0
ValueInc = (ValueMax - ValueMin) / 20
shiftleft = 8 # at sm.put(array, shift)

class Px:
    pan=0; x=0; y=0
    h=0; s=0; v=0

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
                setattr(self, key, value)
    
    def setPosi(self, posi):
        self.pan = posi[0]
        self.x = posi[1]
        self.y = posi[2]

    def getPosi(self):
        return (self.pan, self.x, self.y)
      
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


def iterate(t):
    if stars and stars[0].v == ValueMin:
        stars.popleft()

    if len(stars) < maxstars:
        makeStar()

    for star in stars:
       star.v = max(ValueMin, star.v - ValueInc)

    renderStars()
    


def makeStar():
    # Random Pixel
    # pan = random.randint(0, 5) # TODO make this generic for Wall or Cube
    pan = 0
    x = random.randint(0, panPxPerEdge-1)
    y = random.randint(0, panPxPerEdge-1)
    hue = random.random()
    star = Px() #Px Class
    star.setPosi((pan,x,y)) #Px Class
    star.setCol((hue,1.0,ValueMax)) #Px Class
    # print(hex(id(star)), star.getPosi(), star.getCol())
    stars.append(star)


def printStars():
    for star in stars:
        print(hex(id(star)), star.getPosi(), star.getCol())


def renderStars():
    # printStars()
    # #clear array of previous data
    # for pan in panels.values(): #TODO do more efficentnly
    #     for j in range(size):
    #         pan[AR][j] = 0

    # #write snakes to arrays
    for px in stars:
        # pan,x,y = px.getPosi() #Px Class
        # h,s,v = px.getCol()
        r,g,b = wheel(px.h,px.s,px.v)
        panelarray = panel[AR]
        panelarray[px.y*panPxPerEdge + px.x] = r<<8 | g<<16 | b

    # #write each array to corresponding panel
    panel[SM].put(panel[AR], shiftleft)
    time.sleep_ms(10) # should get an interrupt for this


def runStars(pans, px_per_edge, starcount, iterations):
    global panel
    panel = pans[0]
    global panPxPerEdge
    panPxPerEdge = px_per_edge
    global maxstars
    maxstars = starcount

    for i in range(iterations):
        iterate(0)
        time.sleep(0.2)



### execution ###
# panPxPerEdge = 6
# for i in range(100):
#     iterate(0)
#     time.sleep(0.1)