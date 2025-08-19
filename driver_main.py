from driver import ws2812
import array, time
from driver_patterns import fadeOut, cycleColours
import rp2
from machine import Pin

NUM_LEDS = 256

pio0 = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(17)) # pyright: ignore[reportCallIssue]
pio0.active(1)

ar = array.array("I", [0 for _ in range(NUM_LEDS)])

cycleColours(NUM_LEDS, pio0, ar)

fadeOut(NUM_LEDS, pio0, ar)