from ast import *
import pprint

init = {
    '__parent__' : None,
    '__len__' : 0,
    '__children__' : [],
    'print' : Value(tycon=TyCon(name="fn", type=(string_type, unit_type)), id='print'),
    'mul'   : Value(tycon=TyCon(name="fn", type=(
        TyCon(name="record", type={ 1 : int_type, 2 : int_type }), int_type)), id='mul'),
    'add'   : Value(tycon=TyCon(name="fn", type=(
        TyCon(name="record", type={ 1 : int_type, 2 : int_type }), int_type)), id='mul'),
}

def typecheck(p):
    print(p)
    print(type(p))

    if type(p) == Declaration:
        p.checkType(appendNewScope(init))

    print("Type Check finished! ")
    print("The Symbol Table is:")
    pprint.pprint(init)

