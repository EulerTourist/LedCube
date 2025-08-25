from machine import Timer
import time
tim = Timer(-1)

def callback(x):
    print('poing',x)

tim.init(period=300, mode=Timer.PERIODIC, callback=callback(1))

time.sleep(11)