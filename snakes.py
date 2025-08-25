import random, time, array
from ucollections import deque
from micropython import schedule
from machine import Timer
from colorsys import hsv_to_rgb

class Px:
    def __init__(self, posi, colour):
        self.posi = posi #int of PXY TODO use a byte array here bytes[3]
        self.colour = colour #int of RGB TODO use a byte array here bytes[3]

class Snake:
    age = 1
    # body = (0,0,0)
    def __init__(self, dir, body, pixels):
        self.dir = dir #integer
        self.body = body
        self.pixels = pixels #deque

PIN = 0; SM = 1; AR = 2
maxsnakes = 4
maxage = 32
maxsnakelen = 10
snakes = deque([], maxsnakes)
panPxPerEdge = 4; panAcross = 4; panDown = 4
turniness = 10 # higher means lower probablity of turning this iteration
fertility = 25 # higher means lower probablity of creating a snake this iteration
growth_rate = 10 # cycles till next lengthening

shiftleft = 8 # at sm.put(array, shift)

turns_idx = ['12', '3', '6', '9']
turns = { # key off current direction to get possible turns
    '12': ['3', '9'], #up the panel
    '3': ['12', '6'], #to right of panel
    '6': ['9', '3'], #down the panel
    '9': ['6', '12'] # to left of panel
}

cube_idx = [ b'U', b'D', b'F', b'B', b'L', b'R']
cube_tfm = { # key off current panel to get (target panel, transform)
    0: [(3,3), (5,4), (2,5), (4,6)], # 0/90/180/270
    1: [(2,11), (5,12), (3,13), (4,14)],
    2: [(0,7), (5,1), (1,15), (4,2)],
    3: [(0,8), (4,1), (1,16), (5,2)],
    4: [(0,9), (2,1), (1,17), (3,2)],
    5: [(0,10), (3,1), (1,18), (2,2)]
}

tim = Timer(-1)


def timerHandler(t): 
    schedule(iteration, t)


def iteration(t):
    if len(snakes) < maxsnakes or snakes[0].age >= maxage:
        r = random.randint(1, fertility) 
        if r == 1: makeSnake()

    for snake in snakes:
        stepSnake(snake)
        colourSnake(snake)
        # printSnake(snake)

    renderSnakes()


def makeSnake():
    #Random Pixel
    pan = random.randint(0, 5) # TODO change this for Wall as opposed Cube
    x = random.randint(0, panPxPerEdge-1)
    y = random.randint(0, panPxPerEdge-1)
    posi = pan<<16 | x<<8 | y
    head = RED #red
    #Pixel List
    pixs = deque([Px( posi, head)], maxsnakelen) #new Px list for this snake, maxlen

    #make a snake and add it to snakes list
    #random direction
    dir = turns_idx[random.randint(0, 3)]
    col = random.random()
    body_col = wheel2(hue = col)
    snake = Snake( dir, body_col, pixs ) #dir, age, body, pixel list with first pixel
    # print(hex(id(snake)))
    snakes.append(snake)


def stepSnake(s): #add pixel to head of given snake
    pan = s.pixels[0].posi >> 16 & 0xFF
    x = s.pixels[0].posi >> 8 & 0xFF
    y = s.pixels[0].posi & 0xFF

    # turn left or right?              #TODO do this better
    rnd = random.randint(1, turniness) #TODO do this better
    if rnd == 1:                       #TODO do this better
        s.dir = random.choice(turns[s.dir]) # type: ignore tested okay. In WALL mode check that we are not at edge TODO 

    #work out next pixel location
    if s.dir == '12':
        if y > 0: y -=1
        else: pan, x, y, s.dir = edgeTransformCube(pan, x, y, 0)
    elif s.dir == '3':
        if x < panPxPerEdge-1: x+=1
        else: pan, x, y, s.dir = edgeTransformCube(pan, x, y, 1)
    elif s.dir == '6':
        if y < panPxPerEdge-1: y+=1
        else: pan, x, y, s.dir = edgeTransformCube(pan, x, y, 2)
    elif s.dir == '9': 
        if x > 0: x-=1
        else: pan, x, y, s.dir = edgeTransformCube(pan, x, y, 3)

    #create a new pixel and add it to front of snakes Px queue
    posi = pan<<16 | x<<8 | y
    colour = RED #Full Red Head 
    head = Px( posi, colour)
    s.pixels.appendleft(head)
    # decide whether to extend the tail
    s.age+=1
    if len(s.pixels) > maxsnakelen: #and s.age%growth_rate: #extend length every Nth, otherwise delete the last pixel, effectively moving it along
        s.pixels.pop()


def edgeTransformCube(pan, x, y, dir):
    # print('edgeTransform:', pan, x, y, dir)
    pan1, transform = cube_tfm[pan][dir] #lookup
    # print('pan1:', pan1, 'transform:' , transform)
    if transform == 0: #nothing
        x1 = x; y1 = y; dir1 = dir
    elif transform == 1: # FBLR cube_tfm ->3 
        x1 = 0; y1 = y; dir1 = '3'
    elif transform == 2: # FBLR cube_tfm ->9
        x1 = panPxPerEdge-1; y1 = y; dir1 = '9'

    elif transform == 3: # U -> B
        x1 = panPxPerEdge-1-x; y1 = 0; dir1 = '6'
    elif transform == 4: # U -> R
        x1 = panPxPerEdge-1-y; y1 = 0; dir1 = '6'
    elif transform == 5: # U -> F
        x1 = x; y1 = 0; dir1 = '6'
    elif transform == 6: # U -> L
        x1 = y; y1 = 0; dir1 = '6'

    elif transform == 7: # F -> U
        x1 = x; y1 = panPxPerEdge-1; dir1 = '12'
    elif transform == 8: # B -> U   =3
        x1 = panPxPerEdge-1-x; y1 = 0; dir1 = '6'
    elif transform == 9: # L -> U
        x1 = 0; y1 = x; dir1 = '3'
    elif transform == 10: # R -> U
        x1 = panPxPerEdge-1; y1 = panPxPerEdge-1-x; dir1 = '9'

    elif transform == 11: # D -> F   =7
        x1 = x; y1 = panPxPerEdge-1; dir1 = '12'
    elif transform == 12: # D -> L
        x1 = panPxPerEdge-1-y; y1 = panPxPerEdge-1; dir1 = '12'
    elif transform == 13: # D -> B
        x1 = panPxPerEdge-1-x; y1 = panPxPerEdge-1; dir1 = '12'
    elif transform == 14: # D -> R
        x1 = y; y1 = panPxPerEdge-1; dir1 = '12'

    elif transform == 15: # F -> D   =5
        x1 = x; y1 = 0; dir1 = '6'
    elif transform == 16: # B -> D   =13
        x1 = panPxPerEdge-1-x; y1 = panPxPerEdge-1; dir1 = '12'
    elif transform == 17: # L -> D
        x1 = 0; y1 = panPxPerEdge-1-x; dir1 = '3'
    elif transform == 18: # R -> D
        x1 = panPxPerEdge-1; y1 = x; dir1 = '9'

    return (pan1, x1, y1, dir1)


def edgeTransformWall(pan, x, y, dir):
    # if we got here, we are at the edge of a panel travelling towards that edge (we could also be travelling along an edge) 
    # if there's an adjacent panel in this direction, keep going in that direction and just update pan and either x or y, and return
    # else there's no adjacent panel in this direction, work out x,y limits, is it a wall edge or wall corner
    #   We can either (through/bounce/both_randomly) tunnel through or turn
    #      tunnel? just go to the opposite panel, update pan and, x or y
    #      bounce?
    #       if its an edge, randomly turn either way in the usual way
    #       if its a corner, turn within the constraint
    #       update dir, pan, x OR y
    
    h_idx = pan%panAcross
    v_idx = pan//panAcross

    if dir == '12':
        if v_idx == 0: # border = True
            v_idx = panDown-1 #if going through
            # if turning: TL corner dir = '3', TR corner dir = '9', TOP dir = 3 or 9 according to turns:{}, update dir, x
        else: # not at border, just go to adjacent panel
            v_idx -= 1; y = panPxPerEdge-1
    elif dir == '6':
        if v_idx == panDown-1: # border = True
            v_idx = 0 #if going through
            # if turning: BL corner dir = '3', BR corner dir = '9', BOTTOM go 3 or 9 according to turns:{}, update dir, x
        else:
            v_idx += 1; y = 0
    elif dir == '3':
        if h_idx == panAcross-1: # border = True
            h_idx = 0 #if going through
            # if turning: TR corner dir = '6', BR corner dir = '12', RIGHT go 6 or 12 according to turns:{}, update dir, y
        else:
            h_idx += 1; x = 0
    elif dir == '9':
        if h_idx == 0:# border = True
            h_idx = panAcross-1 #if going through
            # if turning: TL corner dir = 6, BL corner dir = 12, LEFT go 6 or 12 according to turns:{}, update dir, y
        else:
            h_idx -= 1; x = panPxPerEdge-1

    pan1 = panAcross * v_idx + h_idx
    return (pan1, x, y, dir)


def wheel2(hue=0.333, sat=1.0, val_br=0.05):
    r,g,b = hsv_to_rgb(hue, sat, val_br) # pyright: ignore[reportGeneralTypeIssues]
    red = int(round(255*r))
    green = int(round(255*g))
    blue = int(round(255*b))
    return red<<8 | green<<16 | blue #flip the colours around

RED = wheel2(hue=0.0)
# GREEN = wheel2(val_br=0.05)


def colourSnake(s):
    if len(s.pixels) > 1:
        s.pixels[1].colour = s.body


def renderSnakes():
    for pan in panels.values(): #TODO do more efficentnly
        for j in range(size):
            pan[AR][j] = 0

    for snake in snakes:
        for px in snake.pixels:
            pan = px.posi>>16 & 0xFF #TODO use byte array instead
            x = px.posi>>8 & 0xFF
            y = px.posi & 0xFF
            panelarray = panels[pan][AR]
            panelarray[y*panPxPerEdge + x] = px.colour

    for pan in panels.values(): 
        pan[SM].put(pan[AR], shiftleft)
        time.sleep_ms(20)


def runCube(pans, px_per_edge, seconds):
    global panels
    panels = pans
    global panPxPerEdge 
    panPxPerEdge = px_per_edge
    global size
    size = panPxPerEdge*panPxPerEdge

    for pan in panels.values():
        pan[2] = array.array("I", [0 for _ in range(size)])

    makeSnake() # make the first snake

    # tim.init(period=100, mode=Timer.PERIODIC, callback=iteration)
    # time.sleep(seconds)

    for i in range(seconds*10): # controlled TEST
        timerHandler(1)
        time.sleep(0.1)
   


def runWall(pans, px_per_edge, seconds):
    global panels
    panels = pans
    global panPxPerEdge 
    panPxPerEdge = px_per_edge
    global size
    size = panPxPerEdge*panPxPerEdge

    for pan in panels.values():
        pan[2] = array.array("I", [0 for _ in range(size)])

    makeSnake() # make the first snake

    # tim.init(period=100, mode=Timer.PERIODIC, callback=timerHandler(1))
    # time.sleep(seconds)
    # tim.deinit()

    for i in range(int(seconds*10)):
        timerHandler(2)
        # iteration(2)
        time.sleep(0.1)


def printSnake(s):
    pan = s.pixels[0].posi >> 16 & 0xFF
    x = s.pixels[0].posi >> 8 & 0xFF
    y = s.pixels[0].posi & 0xFF
    cols = list(map(lambda p: hex(p.colour), s.pixels))
    print(
        'id:', hex(id(s)), 
        'dir:', s.dir,
        'length:', len(s.pixels),
        #   'pixels:', cols,
        'panel:', cube_idx[pan], #cube_idx[pan],
        'x:', x,
        'y:', y,
        'age:', s.age
    )