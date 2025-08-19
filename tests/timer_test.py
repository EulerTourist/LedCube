from machine import Timer, Pin

led0 = Pin(24, mode=Pin.OUT) # using WeAct V10 board
led1 = Pin(25, mode=Pin.OUT)
led1.on()

def callback(x):
    print("cb", x)
    led0.toggle()
    led1.toggle()

tim = Timer(-1, period=500, mode=Timer.PERIODIC, callback=callback)

while True:
    pass