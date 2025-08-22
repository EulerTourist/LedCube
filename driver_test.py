import array, time, rp2
# from driver_patterns import fadeOut, cycleColours
from colorsys import hsv_to_rgb
from driver import ws2812 #local
from machine import Pin
# from snakes import run
import snakes

NUM_LEDS = 256
delay_1 = 20

BLACK = (0, 0, 1)
RED = (25, 0, 0)
YELLOW = (25, 15, 0)
GREEN = (0, 25, 0)
CYAN = (0, 20, 25)
BLUE = (0, 0, 25)
MAG = (18, 0, 25)
COLS = (RED, YELLOW, GREEN, CYAN, BLUE, MAG)


## INIT ##
panels = {  #up, down, front, back, left, right
    0: [0, None], # sm_id: [pin, sm]
    1: [1, None],
    2: [2, None],
    3: [3, None],
    4: [4, None],
    5: [5, None]
}

pixels = array.array("I", [0 for _ in range(NUM_LEDS)])


for i in panels.keys():
    panels[i][1] = rp2.StateMachine(i, ws2812, freq=8_000_000, sideset_base=Pin(panels[i][0])) # pyright: ignore[reportCallIssue]
    panels[i][1].active(1)


## Functions ##
def pixels_fill(col):
    for i in range(NUM_LEDS):
        pixels[i] = col[1]<<16 | col[0]<<8 | col[2]
    

def wheel2(hue=0.5, sat=1.0, val_br=0.2):
    r,g,b = hsv_to_rgb(hue, sat, val_br) # pyright: ignore[reportGeneralTypeIssues]
    return ( int(round(255*r)), int(round(255*g)), int(round(255*b)) )
 
 
def rainbow():
    for i in range(NUM_LEDS):
        h = i*1.0/NUM_LEDS
        col = wheel2(hue = h, val_br=0.1)
        pixels[i] = col[1]<<16 | col[0]<<8 | col[2] 




############ Execution ##############
for i in panels.keys():
    pixels_fill(COLS[i])
    panels[i][1].put(pixels, 8)
    time.sleep_ms(delay_1)
time.sleep_ms(1000)

# rainbow()
# for i in panels.keys():
#     panels[i][1].put(pixels, 8)
#     time.sleep_ms(delay_1)
# time.sleep_ms(1000)

pixels_fill(BLACK)
for i in panels.keys():
    panels[i][1].put(pixels, 8)
    time.sleep_ms(delay_1)

snakes.runCube(panels, 16) # pass info about machines, machine to panel pin, and size of panels
time.sleep_ms(9000)

## Idle ##
print("sleeping")
pixels_fill(BLACK)
for i in panels.keys():
    panels[i][1].put(pixels, 8)
    time.sleep_ms(delay_1)
    panels[i][1].active(0)

