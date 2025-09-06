import random

# opts = turns[s.dir]
# opts = {
#     'x': ['a', 'b', 'c'],
#     'y': ['d', 'e', 'f'],
#     'z': ['h', 'i', 'j']
# } 

# panels = { # key off current panel
#     'U': ['B', 'R', 'F', 'L'], # 0/90/180/270
#     'D': ['F', 'L', 'B', 'R'],
#     'F': ['U', 'R', 'D', 'L'],
#     'B': ['U', 'L', 'D', 'R'],
#     'L': ['U', 'F', 'D', 'B'],
#     'R': ['U', 'B', 'D', 'F']
# }

# k = list(['x', 'y', 'z'])
# print(k)

# i = list(opts).index('y')
# print(i)
# data = [b'U', b'L', b'R', b'D', b'B', b'F']
# pan = random.choice(data)
# print(pan)

# for d in data:
#     print( panels[d.decode('ascii')] )


# keys = panels.keys()
# for k in keys:
#     asc = k.encode('ascii')
#     for b in asc:
#         print(hex(b))
sides = ['Top', 'Bottom', 'Left', 'Right']
dirs = ['Shrink', 'Grow']
for i in range(20):
        ran = random.randint(0,7) #
        # ran = i
        side = ran//2
        dir = ran%2
        print(ran, sides[side], dirs[dir])