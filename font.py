from colorsys import hsv_to_rgb

def wheel2(hue=0, sat=1.0, val_br=0.1):
    hue = hue/360
    r,g,b = hsv_to_rgb(hue, sat, val_br) # pyright: ignore[reportGeneralTypeIssues]
    red = int(round(255*r))
    green = int(round(255*g))
    blue = int(round(255*b))
    return red<<16 | green<<8 | blue #flip R/G around


G = wheel2(hue=0)
Y = wheel2(hue=60)
R = wheel2(hue=120)
M = wheel2(hue=180)
B = wheel2(hue=240)
C = wheel2(hue=300)

# print('red:', hex(R))
# print('green:', hex(G))
# print('blue:', hex(B))


font = {
    'U':[ # RD on CY
        [C]*16,
        [C,C,C,R,R,R,C,C,C,C,R,R,R,C,C,C]*11,
        [C,C,C,R,R,R,R,R,R,R,R,R,R,C,C,C]*2,
        [C,C,C,C,R,R,R,R,R,R,R,R,C,C,C,C],
        [C]*16
    ],
    'D':[ # MG on GR
        [G]*16,
        [G,G,G,M,M,M,M,M,M,M,M,G,G,G,G,G],
        [G,G,G,M,M,M,M,M,M,M,M,M,G,G,G,G],
        [G,G,G,M,M,M,M,M,M,M,M,M,M,G,G,G],
        [G,G,G,M,M,M,G,G,G,G,M,M,M,G,G,G]*8,
        [G,G,G,M,M,M,M,M,M,M,M,M,M,G,G,G],
        [G,G,G,M,M,M,M,M,M,M,M,M,G,G,G,G],
        [G,G,G,M,M,M,M,M,M,M,M,G,G,G,G,G],
        [G]*16
    ],
    'F':[ # BL on YL
        [Y]*16,
        [Y,Y,Y,B,B,B,B,B,B,B,B,B,B,Y,Y,Y]*3,
        [Y,Y,Y,B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y]*2,
        [Y,Y,Y,B,B,B,B,B,B,B,B,Y,Y,Y,Y,Y]*3,
        [Y,Y,Y,B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y]*6,
        [Y]*16
    ],
    'B':[ # CY on RD
        [R]*16,
        [R,R,R,C,C,C,C,C,C,C,C,R,R,R,R,R],
        [R,R,R,C,C,C,C,C,C,C,C,C,R,R,R,R],
        [R,R,R,C,C,C,C,C,C,C,C,C,C,R,R,R],
        [R,R,R,C,C,C,R,R,R,R,C,C,C,R,R,R]*2,
        [R,R,R,C,C,C,C,C,C,C,C,C,C,R,R,R],
        [R,R,R,C,C,C,C,C,C,C,C,C,R,R,R,R],
        [R,R,R,C,C,C,C,C,C,C,C,C,C,R,R,R],
        [R,R,R,C,C,C,R,R,R,R,C,C,C,R,R,R]*3,
        [R,R,R,C,C,C,C,C,C,C,C,C,C,R,R,R],
        [R,R,R,C,C,C,C,C,C,C,C,C,R,R,R,R],
        [R,R,R,C,C,C,C,C,C,C,C,R,R,R,R,R],
        [R]*16
    ],
    'L':[ # GR on MG
        [M]*16,
        [M,M,M,G,G,G,M,M,M,M,M,M,M,M,M,M]*11,
        [M,M,M,G,G,G,G,G,G,G,G,G,G,M,M,M]*3,
        [M]*16,
    ],
    'R':[ # YL on BL
        [B]*16,
        [B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,B,B,B,B,B],
        [B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,Y,B,B,B,B],
        [B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,B,B,B],
        [B,B,B,Y,Y,Y,B,B,B,B,Y,Y,Y,B,B,B]*2,
        [B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,Y,Y,B,B,B],
        [B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,Y,B,B,B,B],
        [B,B,B,Y,Y,Y,Y,Y,Y,Y,Y,B,B,B,B,B],
        [B,B,B,Y,Y,Y,B,B,Y,Y,Y,B,B,B,B,B],
        [B,B,B,Y,Y,Y,B,B,B,Y,Y,Y,B,B,B,B]*2,
        [B,B,B,Y,Y,Y,B,B,B,B,Y,Y,Y,B,B,B]*3,
        [B]*16
    ],
    'H':[ #Heart Mg on Gr
        [G]*16,
        [G,G,G,R,R,R,R,G,G,R,R,R,R,G,G,G],
        [G,G,R,R,R,R,R,R,R,R,R,R,R,R,G,G],
        [G,R,R,R,R,R,R,R,R,R,R,R,R,R,R,G]*4,
        [G,G,R,R,R,R,R,R,R,R,R,R,R,R,G,G]*2,
        [G,G,G,R,R,R,R,R,R,R,R,R,R,G,G,G]*2,
        [G,G,G,G,R,R,R,R,R,R,R,R,G,G,G,G],
        [G,G,G,G,G,R,R,R,R,R,R,G,G,G,G,G],
        [G,G,G,G,G,G,R,R,R,R,G,G,G,G,G,G],
        [G,G,G,G,G,G,G,R,R,G,G,G,G,G,G,G],
        [G]*16
    ]
}

def flatten(xss):
    return [x for xs in xss for x in xs]

# for r in font[B]:
#     print(flatten(r))
# print(flatten(font['B']))