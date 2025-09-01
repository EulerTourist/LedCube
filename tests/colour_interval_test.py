CY = (0,255,255)
MG = (255,0,255)
YL = (255,255,0)
RD = (255,0,0)
GR = (0,255,0)
BL = (0,0,255)
BK = (0,0,0)

radii = { #2-5 items 
    0: (0, BL), #radius, colour
    1: (399, MG),
    2: (430, CY),
    3: (522, GR),
    4: (707, BK)
}

def getColour(radius): #use circles, take radius and give colour
    if radius < 0 or radius > 707: raise ValueError('value out of range')
    # work out which band pixel is in based on radius
    band = 0
    for b in range(len(radii)-2, -1, -1):
        if radius >= radii[b][0]:
            band = b
            break
    if radii[band+1][1] == radii[band][1]: # if two colours are the same short circuit
        # print('colours are the same', radii[band][1], radii[band+1][1])
        return radii[band][1] #just return the common colour
    else: # else work what proportion between colours a and b
        # print('colours are different', radii[band][1], radii[band+1][1])
        interval = radii[band+1][0] - radii[band][0]
        portion = (radius-radii[band][0])/interval #between 0-1
        # print('band', band, 'radius', radius, 'interval', interval, 'portion', portion)
        # find the intermediate colour between those two bases on portion
        def inter(p, a, b):
            a0, a1, a2 = a
            b0, b1, b2 = b
            # c0, c1, c2 = (0,0,0)
            c0 = (1-p)*a0 + p*b0
            c1 = (1-p)*a1 + p*b1
            c2 = (1-p)*a2 + p*b2
            return (round(c0), round(c1), round(c2))
        colNew = inter(portion, radii[band][1], radii[band+1][1])
        print(portion, radii[band][1], radii[band+1][1], colNew)
        return colNew




test = [0, 1, 300, 400, 420, 499, 500, 501, 600, 707]
for t in test:
    getColour(t)
    # print(t, getColour(t))