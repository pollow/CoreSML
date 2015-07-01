from ast import *
import pprint
import colors

init = {
    '__parent__' : None,
    '__len__' : 0,
    '__children__' : [],
    'print' : (Value(tycon=TyCon(name="fn", type=(string_type, unit_type)), id='print'), 4),

    'muli'   : (Value(tycon=TyCon(name="fn", type=(
        TyCon(name="record", type={ 1 : int_type, 2 : int_type }), int_type)), id='muli'), 8),

    'addi'   : (Value(tycon=TyCon(name="fn", type=(
        TyCon(name="record", type={ 1 : int_type, 2 : int_type }), int_type)), id='addi'), 12),
    'intToStr': (Value(tycon=TyCon(name="fn", type=(int_type, string_type)), id='intToStr'), 16),
    'realToStr': (Value(tycon=TyCon(name="fn", type=(real_type, string_type)), id='realToStr'), 20),
}

def typecheck(p):

    if type(p) == Declaration:
        init["__children__"] = []
        init["__len__"] = 0
        if "it" in init:
            del init["it"]
        p.checkType(init)

    print(colors.success("Type Check finished! The Symbol Table is:"))
    pprint.pprint(init)

    return init

