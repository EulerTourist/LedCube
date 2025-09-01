import sys 



class Pz:
    posi = (0,0,0)
    col = (0,0,0)
    def __init__(self, posi, col):
        self.posi = posi
        self.col = col
    
    def setPosi(self, posi): #set with tuple
        self.posi = posi

    # def getPosi(self): #get tuple
    #     return (self.pan, self.x, self.y)
      
    def setCol(self, col): #set with tuple
        self.col = col

    # def getCol(self): #get tuple
    #     return (self.r, self.g, self.b)


# x = Px(0x335577, 0xFF00FE)
# y = Py(b'\x33 \x55 \x77',b'\xFF \x00 \xFE')
z = Pz( (0x33,0x55,0x77), (0xFF,0x00,0xFE)) 
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

r,g,b = z.col
# print(z.col)
z.setCol((r,g+10,b))

# print(z.getPosi())
# print(z.getCol())
# help(z)
# print(dir(z)) #this works in uPython
print(z.__dict__) #this works in uPython
# print(vars(z)) #creates a dictionary, works in Python not uPython
# print(vars(z1))
# print(hex(id(z))) ID = Mem Addr
