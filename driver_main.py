import array, time, rp2
# from driver_patterns import fadeOut, cycleColours

from driver import ws2812 #local
from machine import Pin

NUM_LEDS = 256

pins = {  #up, down, front, back, left, right
    0: [0, None],
    2: [2, None],
    3: [3, None],
    4: [4, None],
    5: [5, None]
}

# pixels = [0] * NUM_LEDS
# pixels = array.array("I", [0 for _ in range(NUM_LEDS)])


sm0 = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(0))
sm2 = rp2.StateMachine(2, ws2812, freq=8_000_000, sideset_base=Pin(2))
sm3 = rp2.StateMachine(3, ws2812, freq=8_000_000, sideset_base=Pin(3))
sm4 = rp2.StateMachine(4, ws2812, freq=8_000_000, sideset_base=Pin(4))
sm5 = rp2.StateMachine(5, ws2812, freq=8_000_000, sideset_base=Pin(5))

sm5.active(1)
sm4.active(1)
sm3.active(1)
sm0.active(1)
sm2.active(1)



def pixels_fill(color):
    for i in range(NUM_LEDS):
        pixels[i] = (color[1]<<16) + (color[0]<<8) + color[2]


# RED = (255, 0, 0)
# YELLOW = (255, 150, 0)
# GREEN = (0, 255, 0)
# CYAN = (0, 200, 255)
# BLUE = (0, 0, 255)
# PURPLE = (180, 0, 255)

BLACK = (0, 0, 1)
RED = (25, 0, 0)
YELLOW = (25, 15, 0)
GREEN = (0, 25, 0)
CYAN = (0, 20, 25)
BLUE = (0, 0, 25)
PURPLE = (18, 0, 25)
COLORS = (RED, YELLOW, GREEN, CYAN, BLUE, PURPLE)

delay_1 = 20
delay_2 = 10

pixels = array.array("I", [0 for _ in range(NUM_LEDS)])

pixels_fill(RED)
sm5.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load

pixels_fill(YELLOW)
sm4.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load

pixels_fill(GREEN)
sm3.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load

pixels_fill(CYAN)
sm0.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load

pixels_fill(BLUE)
sm2.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load


for i in range(1000):
    time.sleep_ms(delay_2)

pixels_fill(BLACK)
sm5.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load

sm4.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load

sm3.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load

sm0.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load

sm2.put(pixels, 8)
time.sleep_ms(delay_1) #wait for full load

sm5.active(0)
sm4.active(0)
sm3.active(0)
sm0.active(0)
sm2.active(0)








# def wheel(pos):
#     # Input a value 0 to 255 to get a color value.
#     # The colours are a transition r - g - b - back to r.
#     if pos < 0 or pos > 255:
#         return (0, 0, 0)
#     if pos < 85:
#         return (255 - pos * 3, pos * 3, 0)
#     if pos < 170:
#         pos -= 85
#         return (0, 255 - pos * 3, pos * 3)
#     pos -= 170
#     return (pos * 3, 0, 255 - pos * 3)
 
 
# def rainbow_cycle(wait):
#     for j in range(255):
#         for i in range(NUM_LEDS):
#             rc_index = (i * 256 // NUM_LEDS) + j
#             pixels_set(i, wheel(rc_index & 255))
#         pixels_show()
#         time.sleep(wait)