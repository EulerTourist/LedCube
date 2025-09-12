from array import array
from math import sqrt

px_per_edge = 4
num_pix = px_per_edge * px_per_edge
pix = [[(0,0,0) for c in range(num_pix)] for r in range(num_pix)] #2D List
panels = {}
radii = {}
radius_corner = 707 #centre to absolute corner
radius_side = 500 #centre to absolute edge
inter = 2*radius_side/num_pix

def checkCircleInput(circles):
    if not circles: return False
    if circles[0][0] != 0: return False
    if 2 > len(circles) > 5: return False
    for i in range(1,len(circles)):
        if circles[i-1][0] > circles[i][0]: return False
    return True


def getRadius(col, row): #origin top-left
    x = (inter/2 + inter*col) - radius_side
    y = radius_side - (inter/2 + inter*row)
    r = sqrt(x**2 + y**2)
    return r


def getColour(radius): #use circles, take radius and give colour for that pixel
    if radius < 0 or radius > 707: raise ValueError('value out of range')
    # work out which band pixel is in, based on radius
    band = 0
    for b in range(len(radii)-2, -1, -1):
        if radius >= radii[b][0]:
            band = b
            break
    if radii[band+1][1] == radii[band][1]: # if two colours are the same, short circuit
        return radii[band][1] #just return the common colour
    else: # else work what proportion between colours a and b
        interval = radii[band+1][0] - radii[band][0]
        portion = (radius - radii[band][0])/interval #between 0-1
        # print('band', band, 'radius', radius, 'interval', interval, 'portion', portion)
        # find the intermediate colour between those two colours on portion
        def inter(p, a, b):
            a0, a1, a2 = a
            b0, b1, b2 = b
            c0 = (1-p)*a0 + p*b0
            c1 = (1-p)*a1 + p*b1
            c2 = (1-p)*a2 + p*b2
            return (round(c0), round(c1), round(c2))
        colNew = inter(portion, radii[band][1], radii[band+1][1])
        # print(portion, radii[band][1], radii[band+1][1], colNew)
        return colNew


def doDiag():  #north-west 
    for d in range(int(px_per_edge/2)):
        rad = getRadius(d,d)
        col = getColour(rad)
        # print(d, rad, col) #0-0, 1-1, 2-2, 3-3, 4-4, 5-5
        # copy radially 4 x times
        pix[d][d] = col #pix[y][x]
        pix[d][px_per_edge-d] = col
        pix[px_per_edge-d][d] = col
        pix[px_per_edge-d][px_per_edge-d] = col
        

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
            pix[y][px_per_edge-x] = col
            pix[x][px_per_edge-y] = col
            pix[px_per_edge-y][x] = col
            pix[px_per_edge-x][y] = col
            pix[px_per_edge-y][px_per_edge-x] = col
            pix[px_per_edge-x][px_per_edge-y] = col

    
def doCycle():
    # iterate each colour in radii, nudge H,S or V of each
    pass


def doRender():
    #pix -> panels
    # copy each 2D list 'pix' into its corresponding array
    pass


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
    
    # everything seems okay, let's go
    doDiag()
    doSector()
    doRender()

