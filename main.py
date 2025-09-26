import array, time, rp2
from machine import Pin

from colorsys import hsv_to_rgb # Local
from driver import ws2812 #local

NUM_LEDS = 256
delay_1 = 20

BLACK = (0, 0, 1)
PIN = 0; SM = 1; AR = 2

RD = (0,1.0,0.1)
YL = (0.1666,1.0,0.1)
GR = (0.3333,1.0,0.1)
CY = (0.5,1.0,0.1)
BL = (0.6666,1.0,0.1)
MG = (0.8333,1.0,0.1)
BK = (0,0,0)
WH = (0,0,0.1)

## INIT ##
panels = {  #up, down, front, back, left, right
    0: [0, None, []], # sm_id: [pin, sm_ref, array]
    1: [1, None, []],
    2: [2, None, []], # TODO make this a tuple
    3: [3, None, []],
    4: [4, None, []],
    5: [5, None, []]
}


# instantiate all machines in dictionary
for i in panels.keys():
    panels[i][SM] = rp2.StateMachine(i, ws2812, freq=8_000_000, sideset_base=Pin(panels[i][0])) # pyright: ignore[reportCallIssue]
    panels[i][SM].active(1)

#this is used by rainbow, idle, stars
pixels = array.array("I", [0 for _ in range(NUM_LEDS)])
## Functions ##
def pixels_fill(col):
    for i in range(NUM_LEDS): #
        pixels[i] = col[1]<<16 | col[0]<<8 | col[2]
    

def wheel1(hue=0.5, sat=1.0, val_br=0.1):
    r,g,b = hsv_to_rgb(hue, sat, val_br) # pyright: ignore[reportGeneralTypeIssues]
    return ( int(round(255*r)), int(round(255*g)), int(round(255*b)) )
 
 
def rainbow():
    for i in range(NUM_LEDS):
        h = i*1.0/NUM_LEDS
        col = wheel1(hue = h, val_br=0.1)
        pixels[i] = col[1]<<16 | col[0]<<8 | col[2] 




############ Execution ##############
from patterns.font import font, flatten, font_idx # Local
from patterns.snakes import runSnakes
from patterns.radial import runRadial
from patterns.stars import runStars
from patterns.drips import runDrips


if(True): # Face Indicators 6
    for i in panels.keys():
        # print(i, font_idx[i])
        colours = flatten(font[font_idx[i]])
        pixels = array.array("I", colours)
        panels[i][SM].put(pixels, 8)
        time.sleep_ms(delay_1)
    time.sleep_ms(1000)

if(True): # Hearts 6
    pixels = array.array("I", flatten(font['H']))
    for pan in panels.values():
        pan[1].put(pixels, 8)
        time.sleep_ms(delay_1)
    time.sleep_ms(1000)

if(True): # Rainbow 6
    rainbow()
    for pan in panels.values():
        pan[1].put(pixels, 8)
        time.sleep_ms(delay_1)
    time.sleep_ms(1000)

if(True): # Snakes 6
    runSnakes(panels, 16, 20) # pass info about machines/panels, size of panels, run duration
    time.sleep_ms(1000)

if(True): # Radial HSV 1
    radius_corner = 700 #centre to absolute corner
    radius_side = 500 #centre to absolute edge
    rings = { 
        0: (0, RD), #radius, colour
        1: (200, YL),
        2: (300, GR),
        3: (400, BL),
        4: (500, BK),
        5: (700, BK)
    }

    panels[0][AR] = pixels
    runRadial(panels=panels, px_per_edge=16, radii=rings) 
    time.sleep_ms(1000)

if(True): # Stars 1
    panels[0][AR] = pixels
    runStars(panels, 16, 64, 100) # panels, edge, stars. iterations
    time.sleep_ms(1000)

if(True): # Drips 1
    # HueCentre = 0.125, HueWidth = 0.10, 
    panels[0][AR] = pixels
    runDrips( panels=panels, px_per_edge=16, iterations = 20, maxdrips = 8, max_drip_length = 6, HueCentre = 0.333, HueWidth = 0.05 )
    time.sleep_ms(1000)

if(True): ## END ##
    pixels_fill(BLACK)
    for i in panels.keys():
        panels[i][1].put(pixels, 8)
        time.sleep_ms(delay_1)
        panels[i][1].active(0)



print("Done...")