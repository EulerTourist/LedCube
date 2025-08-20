import array, time, rp2
# from driver_patterns import fadeOut, cycleColours

from driver import ws2812 #local
from machine import Pin

NUM_LEDS = 256
delay_1 = 20

BLACK = (0, 0, 1)
RED = (25, 0, 0)
YELLOW = (25, 15, 0)
GREEN = (0, 25, 0)
CYAN = (0, 20, 25)
BLUE = (0, 0, 25)
MAG = (18, 0, 25)
COLORS = (RED, YELLOW, GREEN, CYAN, BLUE, MAG)


## INIT ##
panels = {  #up, down, front, back, left, right
    0: [0, None], # sm_id: [pin, sm]
    2: [2, None],
    3: [3, None],
    4: [4, None],
    5: [5, None]
}

pixels = array.array("I", [0 for _ in range(NUM_LEDS)])


for i in panels.keys():
    panels[i][1] = rp2.StateMachine(i, ws2812, freq=8_000_000, sideset_base=Pin(panels[i][0]))
    panels[i][1].active(1)


## Functions ##
def pixels_fill(color):
    for i in range(NUM_LEDS):
        pixels[i] = (color[1]<<16) + (color[0]<<8) + color[2]

def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)
 
 
def rainbow():
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            pixels[i] = wheel(rc_index & 255)



############ Execution ##############
for i in panels.keys():
    pixels_fill(COLORS[i])
    panels[i][1].put(pixels, 8)
    time.sleep_ms(delay_1) #wait for full load

time.sleep(5)

for i in panels.keys():
    rainbow()
    panels[i][1].put(pixels, 8)
    time.sleep_ms(delay_1) #wait for full load


## Idle ##
time.sleep(5)

pixels_fill(BLACK)

for i in panels.keys():
    panels[i][1].put(pixels, 8)
    time.sleep_ms(delay_1) #wait for full load
    panels[i][1].active(0)

