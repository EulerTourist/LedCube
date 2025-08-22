import array, time

def fadeOut(NUM, sm, arr):
    for i in range(24):
        for j in range(NUM):
            arr[j] >>= 1
        sm.put(arr, 8)
        time.sleep_ms(50)

def cycleColours(NUM, sm, arr):
    for i in range(4 * NUM):
        for j in range(NUM):
            r = j * 100 // (NUM - 1)
            b = 100 - j * 100 // (NUM - 1)
            if j != i % NUM:
                r >>= 3
                b >>= 3
            arr[j] = r << 16 | b
        sm.put(arr, 8)
        time.sleep_ms(50)



