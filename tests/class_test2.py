import sys 

class Px:
    def __init__(self, posi, colour):
        self.posi = posi
        self.colour = colour

class Py:
    posi = bytearray(3)
    colour = bytearray(3)
    R = 0
    G = 1
    B = 2
    def __init__(self, posi, colour):
        self.posi = posi
        self.colour = colour

class Pz:
    pan=0; x=0; y=0
    r=0; g=0; b=0
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
                setattr(self, key, value)
    
    def setPosi(self, posi): #set with tuple
        self.pan = posi[0]
        self.x = posi[1]
        self.y = posi[2]

    def getPosi(self): #get tuple
        return (self.pan, self.x, self.y)
      
    def setCol(self, col): #set with tuple
        self.r = col[0]
        self.g = col[1]
        self.b = col[2]

    def getCol(self): #get tuple
        return (self.r, self.g, self.b)


# x = Px(0x335577, 0xFF00FE)
# y = Py(b'\x33 \x55 \x77',b'\xFF \x00 \xFE')
z = Pz(pan=0x33, x=0x55, y=0x77, r=0xFF, g=0x00, b=0xFE) #not that order is not guaranteed
# dict  = {'pan':0x33, 'x':0x55, 'y':0x77, 'r':0xFF, 'g':0x00, 'b':0xFE}
# z1 = Pz(dict)

# print(x.posi, x.colour)
# print( hex(y.colour[Py.R]), type(y.colour[Py.R]) ) # can only get and cast into int

# y.colour[1] = y.colour[1] + 1 # XXX can't do integer operations on byte
# y.colour[1] = 1 # XXX can't set
# print(sys.getsizeof(y.posi), sys.getsizeof(y.colour))
# print(sys.getsizeof(z.posi), sys.getsizeof(z.colour))
# print(dir(z))

z.setCol((2,3,4))
z.setPosi((234,235,236))
z.g += 10
# print(z.getPosi())
# print(z.getCol())
# help(z)
# print(dir(z)) #this works in uPython
print(z.__dict__) #this works in uPython
# print(vars(z)) #creates a dictionary, works in Python not uPython
# print(vars(z1))
# print(hex(id(z))) ID = Mem Addr
