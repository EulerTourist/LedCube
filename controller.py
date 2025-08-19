# CONTROLLER
# bootrap
from machine import Pin, I2C, Timer
from micropython import schedule
from collections import deque
import time

MY_ADDR = 0
AGENT_ADDR = [1,2,3,4]

class PIN:
    SDA = 0,
    SCL = 1,
    SEL0 = 2, #OUT
    SEL1 = 3, #OUT
    IRQ0 = 5, #IN
    IRQ1 = 6, #IN

#build it here, translate and save to MEM
px_playlist = [] #mapped for target [[pattern 0],[pattern 1],[pattern 2],[],[],[],[],[]]
px_patterns = [] #mapped for target [[pattern 0],[pattern 1],[pattern 2],[],[],[],[],[]]


# Any Node can pulse any IRQ lines at any time: enqueue interrupt handler
def irqHandler(gpio):
    schedule(enqueue, gpio)


sel0 = Pin(PIN.SEL0, Pin.OUT, value=0)
sel1 = Pin(PIN.SEL1, Pin.OUT, value=0)
irq0 = Pin(PIN.IRQ0, Pin.IN, Pin.PULL_DOWN).irq(irqHandler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True)
irq1 = Pin(PIN.IRQ1, Pin.IN, Pin.PULL_DOWN).irq(irqHandler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True)
i2c = I2C(0, sda=Pin(PIN.SDA), scl=Pin(PIN.SCL), freq=400_000)
timer1 = Timer(0) #TODO hard=True
queue = deque()


# If IRQ in == SELECT out, Controller clears SELECT and clears 1s timer
# IRQ number is queued if IRQ in != SELECT out
def enqueue(gpio):
    print(gpio)
    time.sleep_ms(1) #to allow time for both pins to toggle
    val = irq1.__call__()<<1 | irq0.__call__() #faster form of pin.value()
    print(val)
    if val == (sel1.__call__()<<1 | sel0.__call__()):
        #stop one second timer if it's running
        timer1.deinit()
        setSelect(0)
    elif queue[-1] != val: #prevent double triggering
        queue.append(val)
        schedule(queueProcessor, None)


def timerHandler(x):
    setSelect(0)


def queueProcessor(gpio):
    while queue[0]:
        addr = queue.popleft
        setSelect(addr) # Controller SELECTs next Node in Queue: out 
        timer1.init(period=1000, mode=Timer.ONE_SHOT, callback=timerHandler) # Start 1 second safety timer
        # Node can now control the Bus and exchange data: see list of tasks in drawing
        # Node pulses IRQ when done: out


def setSelect(val):
    #check value bounds
    if 0 > val > 3: return
    #set pins according to select value
    sel1.__call__(val>>1 & 1)
    sel0.__call__(val & 1)


# API handlers:
    # create empty playlist with name, delete playlist by name (sequence of patterns), list steps in named playlist
    # activate named playlist, start, stop, then=stop/repeat/link, link (activate other PL and start it)
    # edit patterns: add new pattern data for a selected pattern.py function and name it, delete the named pattern (but not the function)
    # edit step: add named pattern [to optionally given step] to named playlist (add to end if not given, fail if given step already occupied)(empty steps run some default pattern), delete pattern from step
    # edit step: set duration for given step in named playlist
    # edit playlist: move or copy steps A [to C] to start at step X (create any step numbers that don't exist)(fail if any target steps already occupied)
    # usage how-to information INFO


def  playlistShow(idx):
    # build the data and write to MEM
    # build status and control
    # trigger the agents via SELECTions when SELECT is idle next
    # Controller can talk to Mem while SELECT == 0
    pass