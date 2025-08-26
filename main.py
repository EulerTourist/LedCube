import array, time, rp2
from machine import Pin

from colorsys import hsv_to_rgb # Local
from font import font, flatten # Local
from driver import ws2812 #local
import snakes #local

NUM_LEDS = 256
delay_1 = 20

BLACK = (0, 0, 1)

## INIT ##
panels = {  #up, down, front, back, left, right
    0: [0, None, None], # sm_id: [pin, sm_ref, array]
    1: [1, None, None],
    2: [2, None, None], # TODO make this a tuple
    3: [3, None, None],
    4: [4, None, None],
    5: [5, None, None]
}

pixels = array.array("I", [0 for _ in range(NUM_LEDS)])


for i in panels.keys():
    panels[i][1] = rp2.StateMachine(i, ws2812, freq=8_000_000, sideset_base=Pin(panels[i][0])) # pyright: ignore[reportCallIssue]
    panels[i][1].active(1)


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
## Faces TODO FIX
pixels = array.array("I", flatten(font['U']))
panels[0][1].put(pixels, 8)
time.sleep_ms(delay_1)

pixels = array.array("I", flatten(font['D']))
panels[1][1].put(pixels, 8)
time.sleep_ms(delay_1)

pixels = array.array("I", flatten(font['F']))
panels[2][1].put(pixels, 8)
time.sleep_ms(delay_1)

pixels = array.array("I", flatten(font['B']))
panels[3][1].put(pixels, 8)
time.sleep_ms(delay_1)

pixels = array.array("I", flatten(font['L']))
panels[4][1].put(pixels, 8)
time.sleep_ms(delay_1)

pixels = array.array("I", flatten(font['R']))
panels[5][1].put(pixels, 8)
time.sleep_ms(1000)

# Hearts
pixels = array.array("I", flatten(font['H']))
for pan in panels.values():
    pan[1].put(pixels, 8)
    time.sleep_ms(delay_1)
time.sleep_ms(1000)

# Rainbow
rainbow()
for pan in panels.values():
    pan[1].put(pixels, 8)
    time.sleep_ms(delay_1)
time.sleep_ms(1000)

# Snakes
snakes.runCube(panels, 16, 20) # pass info about machines/panels, size of panels, run duration
time.sleep_ms(1000)

## Idle ##
pixels_fill(BLACK)
for i in panels.keys():
    panels[i][1].put(pixels, 8)
    time.sleep_ms(delay_1)
    panels[i][1].active(0)

print("Done...")