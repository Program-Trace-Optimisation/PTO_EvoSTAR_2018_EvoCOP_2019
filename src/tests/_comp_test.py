import sys
sys.path.append('../problem')
from _PTO import random, random_function


@random_function
def dec(f):
    return f


@random_function
@dec
def pippo():
    return 0


[ord(_c) for _line in file for _c in _line]


@random_function
def pippo():
    x, _i = 0, 1
    for _i in range(3):
        y = 2
        for _j in range(_i):
            print(_i, _j)
    print(_i + 1)


@random_function
def pappa():
    print(i)


@random_function
def pippo():
    x, i = 0, 1
    _i = 0
    while True:
        _i += 1
        y = 2
        for _j in range(i):
            print(i, _j)
    print(i + 1)
    _i = 0
    while False:
        _i += 1
        pass
