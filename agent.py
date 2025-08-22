# NODE
# bootstrap...
from machine import Pin, I2C
from micropython import schedule
import time
import rp2
# from rp2 import StateMachine
from driver import ws2812
import tests.driver_patterns as driver_patterns

MY_ADDR = 1
WR_OFFSET = 8
# U_COUNT = 1
# U_HIGH = 8
# U_WIDE = 8
# LEDS = U_COUNT * U_HIGH * U_WIDE

px_blocks = [] #mapped for target [[block 0],[block 1],[block 2],[],[],[],[],[]]

class PIN:
    SDA = 0,
    SCL = 1,
    SEL0 = 2, #IN
    SEL1 = 3, #IN
    IRQ0 = 5, #OUT
    IRQ1 = 6, #OUT
    PIO0SIDE = 10

class MEM:
    STAT = 0
    CC = 64
    AG1 = 128
    AG2 = 192 #128+1x768
    AG3 = 256 #128+2x768
    AG4 = 320 #128+3x768

def selectHandler(gpio):
    schedule(addressCheck, gpio)

irq0 = Pin(PIN.IRQ0, Pin.OUT)
irq1 = Pin(PIN.IRQ1, Pin.OUT)
sel0 = Pin(PIN.SEL0, Pin.IN, Pin.PULL_DOWN).irq(selectHandler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True)
sel1 = Pin(PIN.SEL1, Pin.IN, Pin.PULL_DOWN).irq(selectHandler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True)
i2c = I2C(0, sda=Pin(PIN.SDA), scl=Pin(PIN.SCL), freq=400_000)
pio0 = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN.PIO0SIDE))  # type: ignore
pio0.active(1)


def addressCheck(gpio):
    print(gpio)
    time.sleep_ms(1) #to allow time for both pins to toggle
    val = sel1.__call__()<<1 | sel0.__call__() #faster form of pin.value()
    print(val)
    if val == MY_ADDR:
        print('its for me')
        schedule(doJobs, None)


def doJobs(nothing):
    # get status, cc and data
    status = i2c.readfrom_mem(MY_ADDR, MEM.STAT, 8)
    control = i2c.readfrom_mem(MY_ADDR, MEM.CC, 8)
    data = i2c.readfrom_mem(MY_ADDR, MEM.AG1, 8)
    print(status, control, data)
    # process the above and update local variables
    # new status and control sets context
    # new data provides content
    # display it
    patternShow(0,1,2,3) #TODO
    # update my node data i might have
    i2c.writeto_mem(MY_ADDR, MEM.AG1+WR_OFFSET, b'\x1020')
    # update my status
    i2c.writeto_mem(MY_ADDR, MEM.STAT+WR_OFFSET, b'\x1010')
    pulseIRQ()


def pulseIRQ():
    irq1.__call__(MY_ADDR>>1 & 1)
    irq0.__call__(MY_ADDR & 1)
    time.sleep_ms(10)
    irq1.__call__(0)
    irq0.__call__(0)


# this is responsible for playing one pattern with given or stored data
def  patternShow(machines, command, pattern=None, data=None): #machineID, pattern, data, command
    #select the pattern to run from patterns.py according to status & control
    #instantiate: pass in the state machine instances and raw data as needed
    #configure, inititialise a pattern: pass in the state machine instances and raw data as needed
    #control: ready/start/stop/sync_reset the machines. it could be control only e.g start/stop, or prep only
    # pio0.active(1)
    pass


pulseIRQ()