import sys
import uselect
import time

poll = uselect.poll()
poll.register(sys.stdin, uselect.POLLIN) # Register stdin for polling

while True:
    if poll.poll(0): # Check for input with a 0ms timeout (non-blocking)
        cmd = sys.stdin.read(1) # Read a single character
        # cmd = sys.stdin.readline() #fails
        if cmd == 'q':
            print("Exiting...")
            break
        else:
            print("Received:", cmd)
    # Perform other tasks here
    time.sleep_ms(100) # Example: do other work