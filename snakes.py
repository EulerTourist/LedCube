# Names of cube_tfmcube faces:
#           ^
#           D
#           |
#           B                   0,0 1,0 -> W,0
#           v                   0,1 ---->   |
#           ^                    | ---->    |
#  L> ----- U ----- <R           | --->     |
#           |                   0,H ->     W,H
#           ^
#           F
# 
# Snake: 
# red head=1, body of alternate greens
# new snake starts on random pixel and random direction (U,D,L,R), start one straight away then every rand()*10sec 
# each snake moves by one pixel each step, L=-1, R=+1, U=-W, D=+W in the current direction, update all pixels
# however, preceding the step, snake may change direction turning left or right with a probablity of P=1/(4*(H+W)) 
# if the snake reaches the edge of the panel, go adjacent panel
# snake starts with body=0 and extends by one each time it crosses an edge, that is, not deleting last
# snake fades out when length attempts to increment to max length N=2*(H+W), that is, at edge
# Specs:
# px = (0pxy, 0rgb)
# snake = { dir: <U/D/L/R/Fade>, bright:<byte>, px: deque}
# NB: calculate as RGB but GRB on the pixel

import random, time
from ucollections import deque
from micropython import schedule
from machine import Timer

# queue = deque()
maxsnakes = 1
snakes = deque([], maxsnakes)
panPxPerEdge = 4; panAcross = 4; panDown = 4
turniness = 10 # higher means lower probablity of turning this iteration
fertility = 100 # higher means lower probablity of creating a snake this iteration
maxsnakelen = 3*panPxPerEdge
growth_rate = 10 # cycles till next lengthening
age_of_death = 999
pio = []

turns_idx = ['12', '3', '6', '9']
turns = { # key off current direction to get possible turns
    '12': ['3', '9'], #up the panel
    '3': ['12', '6'], #to right of panel
    '6': ['9', '3'], #down the panel
    '9': ['6', '12'] # to left of panel
}

# this is currently specific to Cube, along with edgeTransform
cube_idx = [ b'U', b'D', b'F', b'B', b'L', b'R']
cube_tfm = { # key off current panel to get (target panel, transform)
    0: [(3,3), (5,4), (2,5), (4,6)], # 0/90/180/270
    1: [(2,11), (4,12), (3,13), (5,14)],
    2: [(0,7), (5,1), (1,15), (4,2)],
    3: [(0,8), (4,1), (1,16), (5,2)],
    4: [(0,9), (2,1), (1,17), (3,2)],
    5: [(0,10), (3,1), (1,18), (2,2)]
}

panels = { 
        0: [0] * (panPxPerEdge*panPxPerEdge),
        1: [0] * (panPxPerEdge*panPxPerEdge),
        2: [0] * (panPxPerEdge*panPxPerEdge),
        3: [0] * (panPxPerEdge*panPxPerEdge),
        4: [0] * (panPxPerEdge*panPxPerEdge),
        5: [0] * (panPxPerEdge*panPxPerEdge)
    }


class Px:
    def __init__(self, posi, colour):
        self.posi = posi #int of PXY
        self.colour = colour #int of RGB

class Snake:
    def __init__(self, dir, age, pixels):
        self.dir = dir #integer
        self.age = age #integer
        self.pixels = pixels #deque

### this is Class below here ###

def timerHandler(t): #one second timer, we might split this to 100ms update and 1-10sec new snake
    schedule(iteration, 1)


def iteration(t):
    if snakes[-1].age >= age_of_death:
        snakes.popleft() #delete the last snake, will it ever be anything other than the last?
    # randomly create new snake if snakes queue not maxed out
    if len(snakes) < maxsnakes:
        r = random.randint(1, fertility) #~1 per 5 iterations
        if r == 1: makeSnake()
    for snake in snakes:
        stepSnake(snake)
        colourSnake(snake)
        printSnake(snake)
    renderSnakes()


def makeSnake():
    #Random Pixel
    pan = random.randint(0, 5) # TODO change this for Wall as opposed Cube
    x = random.randint(0, panPxPerEdge-1)
    y = random.randint(0, panPxPerEdge-1)
    p = pan<<16 
    posi = p<<16 | x<<8 | y
    colour = 0xFF0000 #Full Red Head TODO define colours
    #Pixel List
    segments = deque([Px( posi, colour)], maxsnakelen) #new Px list for this snake, maxlen
    #random direction
    direction = turns_idx[random.randint(0, 3)]
    #make a snake and add it to snakes list
    snake = Snake( direction, 1, segments ) #dir, age, pixels
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
    colour = 0xFF<<16 #Full Red Head 
    head = Px( posi, colour)
    s.pixels.appendleft(head)
    # decide whether to extend the tail
    s.age+=1
    if s.age > 2 and s.age%growth_rate: #extend length every Nth, otherwise delete the last pixel, effectively moving it along
        tail = s.pixels.pop()
    

# this is currently specific to Cube, along with cube_tfm lookup NOTE
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


def colourSnake(s):
    if len(s.pixels) > 1:
        s.pixels[1].colour = 0xFF00 # TODO define colours


def renderSnakes():
    # the last snake should be be displayed last
    # the last pixel in a snake should be be displayed last
    # pan is panel
    # position = y x panPxPerEdge + x
    for s in snakes:
        for p in s.pixels:
            pan = p.posi>>16 & 0xFF
            x = p.posi>>8 & 0xFF
            y = p.posi & 0xFF
            panels[pan][y*panPxPerEdge + x] = p.colour
    shiftleft = 8
    pio[0].put(panels[0], shiftleft)
    pio[1].put(panels[1], shiftleft)
    pio[2].put(panels[2], shiftleft)
    pio[3].put(panels[3], shiftleft)
    pio[4].put(panels[4], shiftleft)
    pio[5].put(panels[5], shiftleft)


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

def __init__(self, pio):
    self.pio = pio


################### TEST ####################
panPxPerEdge = 8
# timer1 = Timer(-1).init(period=2000, mode=Timer.PERIODIC, callback=timerHandler) #one second timer
makeSnake() # make the first snake
for i in range(16):
    iteration(1)
    # printSnake(snakes[0])
    # stepSnake(snakes[0])
    time.sleep(0.1)
# while True:
#     pass

