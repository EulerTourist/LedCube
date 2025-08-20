from colorsys import hsv_to_rgb

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
    

def wheel1():
    T = 12 * 128 #total period
    Vmax = 6 * 128
    # r_lvl = 128; r_dir = 0
    # g_lvl = 128; g_dir = 0
    # b_lvl = 128; b_dir = 0

    def triangle(time):
        def func(t):
            if t <= T/4:
                return 
            elif T/4 < t < T/4*3:
                return 
            elif t > T/4*3:
                return ()
            else: return 


def wheel2(hue=0.5, sat=1.0, v_bright=1.0):
    r,g,b = hsv_to_rgb(hue, sat, v_bright)
    return ( int(round(255*r)), int(round(255*g)), int(round(255*b)) )


########## exec ###########
for i in range(100):
    h = i*1.0/100
    print(wheel2(hue=h))