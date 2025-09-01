from array import array
from math import sqrt

num_pix = 16
radius_corner = 707 #centre to absolute corner
radius_side = 500 #centre to absolute edge
inter = 2*radius_side/num_pix

pix = [[0 for c in range(num_pix)] for r in range(num_pix)]

def getRadius(col, row): #origin top-left
    x = (inter/2 + inter*col) - radius_side
    y = radius_side - (inter/2 + inter*row)
    r = sqrt(x**2 + y**2)
    return (x,y,r)

def getColour(radius):
    pass


# pix[1][1] = 9
# print(pix)
# for row in range(num_pix):
#     for col in range(num_pix):
#         x,y,r = getRadius(col, row)
#         # print( 'col:', col, 'x:', x, '\trow:', row, 'y:', y, 'radius:', r) 
#         print( 'col:', col, '\trow:', row, '\tradius:', r) 

# tst = [1,2,3]
# out = array('I', tst)
# print(out)

# D O O O O O
# O D O O O O
# O O D O O O
# O O O D O O
# O O O O D O
# O O O O O D
# ..... six more row and six more columns

for d in range(int(num_pix/2)): print(d,d) #0-0, 1-1, 2-2, 3-3, 4-4, 5-5
for y in range(int(num_pix/2-1)): #y = 0,1,2,3,4
    for x in range(y+1, int(num_pix/2)):
        print(x,y)
#     1-0, 2-0, 3-0, 4-0, 5-0
#          2-1, 3-1, 4-1, 5-1
#               3-2, 4-2, 5-2
#                    4-3, 5-3
#                         5-4