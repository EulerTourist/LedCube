from array import array
from math import sqrt

CY = (0,255,255)
MG = (255,0,255)
YL = (255,255,0)
RD = (255,0,0)
GR = (0,255,0)
BL = (0,0,255)
BK = (0,0,0)

px_per_edge = 4
num_pix = px_per_edge * px_per_edge
pix = [[(0,0,0) for c in range(num_pix)] for r in range(num_pix)]
# pixels = array("I", [0 for _ in range(num_pix)])
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


def makeRadial(pan, px_edge, config):
    if px_edge < 2 or px_edge%2: raise ValueError('only does even-sided squares') # check that edge is even... 
    else: px_per_edge = px_edge
    if not checkCircleInput(config): raise ValueError('values in circles out of range') # check that for all r, r > r-1, r[0] == 0
    else: radii = config
    doDiag()
    doSector()
    #write pix -> panel


###### Execution #######
pan = {0: [0, None, None]} # sm_id: [pin, sm_ref, array]


config = { #2-5 items 
    0: (0, MG), #radius, colour
    1: (400, MG),
    2: (450, CY),
    3: (radius_side, BK),
    4: (radius_corner, BK),
}

makeRadial(pan, 8, config)

# for row in range(num_pix):
#     for col in range(num_pix):
#         x,y,r = getRadius(col, row)
#         # print( 'col:', col, 'x:', x, '\trow:', row, 'y:', y, 'radius:', r) 
#         print( 'col:', col, '\trow:', row, '\tradius:', r) 