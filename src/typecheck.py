from ast import *


def typecheck(p):
    print(p)
    print(type(p))

    if type(p) == Declaration:
        p.checkType({})
