from collections import deque

d = deque("steven")
for l in d:
    if l == 'v': del l
    else: print(l)

# del d[5]
# print(d)