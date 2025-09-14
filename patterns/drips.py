import random, time, array
# from collections import deque
from ucollections import deque
# from micropython import schedule
# from machine import Timer
from colorsys import hsv_to_rgb

PIN = 0; SM = 1; AR = 2

# drips = {}
panels = {}
maxdrips = 4
max_drip_length = 4
px_per_edge = 2; pansAcross = 2; pansDown = 2
HueCentre = 0.5; HueWidth = 0.5
ValueMin = 0; ValueMax = 0.1 #Brightness
shiftleft = 8 # at sm.put(array, shift)
iterations=100

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


class Drip:
    age = 1
    def __init__(self, pixels, dir = 2, body_col = (0,0,0)): #int, tuple, array of Px
        self.dir = dir #integer
        self.body_col = body_col
        self.pixels = deque(pixels, max_drip_length) #deque


def wheel(hue=0.333, sat=1.0, val_br=0.05):
    r,g,b = hsv_to_rgb(hue, sat, val_br) # pyright: ignore[reportGeneralTypeIssues]
    red = int(round(255*r))
    green = int(round(255*g))
    blue = int(round(255*b))
    return (red, green, blue)


def iterate(t):
    if drips and not drips[0].age: # TODO what determines removed from 'drips' deque
        drips.popleft()

    if len(drips) < maxdrips:
        makeDrip()
    
    renderDrips()

    for drip in drips:
       moveDrip(drip)
    

def makeDrip():
    pan = 0
    x = random.randint(0, px_per_edge-1)
    y = 0
    # sat = random.random()
    sat = 1
    low = max(0, HueCentre-HueWidth)
    high = min(HueCentre+HueWidth, 1)
    hue = random.uniform(low, high)
    colour = (hue,sat,ValueMax)

    px = Px() #Px Class
    px.setPosi((pan,x,y)) #Px Class
    px.setCol(colour) #Px Class
    
    drip = Drip([px], body_col=colour)
    drips.append(drip)


def moveDrip(drip):
    # print( hex(id(drip)) )
    pan,x,y = drip.pixels[0].getPosi()
    
    if y >= px_per_edge-1: 
        drip.pixels.pop()
        if not len(drip.pixels): # make age = 0 if tail goes off the panel
            drip.age = 0
    else: 
        y += 1
        # make new pixel in the direction we're going
        newhead = Px()  #Px Class
        newhead.setPosi((pan,x,y)) #Px Class
        newhead.setCol(drip.body_col) #Px Class
        drip.pixels.appendleft(newhead)


def renderDrips():
    # #clear array of previous data
    for pan in panels.values(): #TODO do more efficentnly
        for j in range(px_per_edge*px_per_edge):
            pan[AR][j] = 0

    panelarray = panels[0][AR] #NOTE temp
    for drip in drips:
        for px in drip.pixels:
            pan,x,y = px.getPosi() #Px Class
            h,s,v = px.getCol()
            r,g,b = wheel(h,s,v)
            # panelarray = panels[pan][AR]
            panelarray[y*px_per_edge + x] = r<<8 | g<<16 | b

    # #write each array to corresponding panel
    panels[0][SM].put(panels[0][AR], shiftleft)
    time.sleep_ms(10) # should get an interrupt for this


def runDrips(**kwargs):
    for k,v in kwargs.items():
        globals()[k] = v

    if px_per_edge < 2 or px_per_edge%2: 
        print('pixel count along edge should be even and 2 or more')
        return

    if not panels: # may need to add structure check here as above
        print('i don\'t have any panels to talk to, check structure')
        return
    
    global drips # Potential Bug
    drips = deque([], maxdrips)
    
    for i in range(iterations):
        iterate(0)
        time.sleep(0.2)



### execution ###
# panPxPerEdge = 6
# for i in range(100):
#     iterate(0)
#     time.sleep(0.1)