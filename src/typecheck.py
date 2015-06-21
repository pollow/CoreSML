from ast import *

init = {
    'print' : Value(tycon=(string_type, unit_type), id='print')
}

def typecheck(p):
    print(p)
    print(type(p))

    if type(p) == Declaration:
        p.checkType(init)
