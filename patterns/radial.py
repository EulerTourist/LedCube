from array import array
from time import sleep_ms
from math import sqrt
from colorsys import hsv_to_rgb

PIN = 0; SM = 1; AR = 2
RAD = 0; COL = 1 

px_per_edge = 4
num_pix = 0
pix = [] #2D List
panels = {}
radii = {}
radius_corner = 707 #centre to absolute corner
radius_side = 500 #centre to absolute edge
px_width = 0
shiftleft = 8


def checkCircleInput(circles):
    if not circles: return False
    if circles[0][0] != 0: return False
    if 2 > len(circles) > 5: return False
    for i in range(1,len(circles)):
        if circles[i-1][0] > circles[i][0]: return False
        # if the colour is not type tuple TODO
    return True


def getRadius(col, row): #origin top-left; x,y,r wrt to centre
    x = (px_width/2 + px_width*col) - radius_side
    y = radius_side - (px_width/2 + px_width*row)
    r = sqrt(x**2 + y**2)
    # print('col, row, x,y,r=', col, row, x, y, r)
    return r


def getColour(radius): #use circles, take radius and give colour for that pixel
    
    if radius < 0 or radius > 707: raise ValueError(f"Radius not between 0 and 707, radius= {radius}")
    # work out which band pixel is in, based on radius
    band = 0
    for b in range(len(radii)-2, -1, -1):
        if radius >= radii[b][RAD]:
            band = b
            break
    # print('radii:', radii, 'band:', band)
    # print('radii[band][COL]:', radii[band][COL])
    # print('radii[band+1][COL]:', radii[band+1][COL])
    if radii[band+1][COL] == radii[band][COL]: # if two colours are the same, short circuit
        return radii[band][COL] #just return the common colour
    else: # else work what proportion between colours a and b
        interval = radii[band+1][RAD] - radii[band][RAD]
        portion = (radius - radii[band][RAD])/interval #between 0-1
        # print('band', band, 'radius', radius, 'interval', interval, 'portion', portion)
        # find the intermediate colour between those two colours on portion
        def inter(p, a, b):
            a0, a1, a2 = a
            b0, b1, b2 = b
            c0 = (1-p)*a0 + p*b0
            c1 = (1-p)*a1 + p*b1
            c2 = (1-p)*a2 + p*b2
            return (c0, c1, c2)
        colNew = inter(portion, radii[band][COL], radii[band+1][COL])
        # print(portion, radii[band][1], radii[band+1][1], colNew)
        return colNew


def doDiag():  #north-west 
    for d in range(int(px_per_edge/2)):
        rad = getRadius(d,d)
        col = getColour(rad)
        # print('px_per_edge:', px_per_edge)
        # print('d/rad/col:', d, rad, col) #0-0, 1-1, 2-2, 3-3, 4-4, 5-5
        # copy radially 4 x times
        pix[d][d] = col #pix[y][x]
        pix[d][px_per_edge-1-d] = col
        pix[px_per_edge-1-d][d] = col
        pix[px_per_edge-1-d][px_per_edge-1-d] = col
        

def doSector(): #north-west upper half 0-45deg sector
    for y in range(int(px_per_edge/2-1)): #y = 0,1,2,3,4
        for x in range(y+1, int(px_per_edge/2)):
            #     1-0, 2-0, 3-0, 4-0, 5-0 ...X-Y
            #          2-1, 3-1, 4-1, 5-1
            #               3-2, 4-2, 5-2
            #                    4-3, 5-3
            #                         5-4
            rad = getRadius(x, y)
            col = getColour(rad)
            # print(x, y, rad, col)
            # copy radially 4 x times
            # mirror across the diag and copy that radially 4 x times
            pix[y][x] = col #pix[y][x]
            pix[x][y] = col
            pix[y][px_per_edge-1-x] = col
            pix[x][px_per_edge-1-y] = col
            pix[px_per_edge-1-y][x] = col
            pix[px_per_edge-1-x][y] = col
            pix[px_per_edge-1-y][px_per_edge-1-x] = col
            pix[px_per_edge-1-x][px_per_edge-1-y] = col

    
def doCycle():
    # iterate each colour in radii, nudge H,S or V of each
    pass


def wheel(hue=0.333, sat=1.0, val_br=0.05):
    r,g,b = hsv_to_rgb(hue, sat, val_br) # pyright: ignore[reportGeneralTypeIssues]
    red = int(round(255*r))
    green = int(round(255*g))
    blue = int(round(255*b))
    return (red, green, blue)


def doRender():
    # #write px to arrays
    panelarray = panels[0][AR]
    for row in range(px_per_edge):
        for col in range(px_per_edge):
            h,s,v = pix[row][col]
            r,g,b = wheel(h,s,v)
            panelarray[row * px_per_edge + col] = r<<8 | g<<16 | b

    # #write each array to corresponding panel
    panels[0][SM].put(panels[0][AR], shiftleft)
    sleep_ms(10) # should get an interrupt for this


def printRadial():
    for row in range(px_per_edge):
        for col in range(px_per_edge):
            print(pix[row][col])
        print('\n')


### RUN ###
def runRadial(**kwargs):
    for k,v in kwargs.items():
        globals()[k] = v

    if px_per_edge < 2 or px_per_edge%2: 
        print('pixel count along edge should be even and 2 or more')
        return

    if not radii and checkCircleInput(radii): 
        print('the raddii object is not complaint')
        return

    if not panels: # may need to add structure check here as above
        print('i don\'t have any panels to talk to, check structure')
        return
    
    global px_width
    global num_pix
    global pix

    px_width = 2*radius_side/px_per_edge #px width in terms of radius units
    num_pix = px_per_edge * px_per_edge
    pix = [[(0,0,0) for col in range(px_per_edge)] for row in range(px_per_edge)] #2D List

    # everything seems okay, let's go
    doDiag()
    doSector()
    doRender()

