import array
import numpy

# a = array.array("I", [0 for _ in range(5)])
a = numpy.zeros(5)
# a.astype(int) 

a[3] = 8
a[2] = 7

a[:] = 0
a.fill(2)

print(type(a[0])) # <class 'numpy.float64'>

# b = a[:]
# b[:] = [0]
# print(b)

# for i in range(len(a)):
    # print(i)