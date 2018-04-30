import sys
sys.path.append('../problem')

# import

from PTO import random

#decorator

def dec(f):
    return f

@dec
def pippo():
    return 0

# list comprehension

[ord(c) for line in file for c in line]

# foor loops

def pippo():
    x, i = 0, 1
    for i in range(3):
        y = 2
        for j in range(i):
            print(i, j)
    print(i + 1)

def pappa():
    print(i)

# while loops

def pippo():
    x, i = 0, 1
    while True:
        y = 2
        for j in range(i):
            print(i, j)
    print(i + 1)
    while False:
        pass
