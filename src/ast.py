
class TypeExpression :
    def __init__(self):
        pass


class RecordItem:
    def __init__(self, lab, value):
        self.lab = lab
        self.value = value


    def isWild(self):
        return (self.lab == None) and (self.value == None)


class TyCon:
    def __init__(self, tyvar = [], name = None, len = 0, type = None):
        # tycon = ( string, int )
        self.tyvar = tyvar
        self.tycon = name
        self.type  = type
        self.len   = len


class VCon:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Declaration :
    def __init__(self, bindType, ):
        pass


class Value :
    def __init__(self, id = None, value = None, tycon = None, vcon = None, wildcard = False, OP = False):
        self.id = id
        self.value = value
        self.tycon = tycon # A TyCon instance
        self.vcon = vcon


class Pattern :
    def __init__(self, value):
        self.value = value


class Constant :
    def __init__(self, value, ctype):
        self.value = value
        self.ctype = ctype


class Unit:
    def __init__(self):
        pass


class MRule:
    def __init__(self, pat, exp):
        self.pat = pat
        self.exp = exp


class Match:
    def __init__(self, value, rules):
        self.value = value
        self.rules = rules


class typbind:
    def __init__(self, param, tycon, type):
        self.param = param
        self.tycon = tycon
        self.type = type

class valbind:
    def __init__(self, tyvars, pat, exp):
        self.tyvars = tyvars
        self.pat = pat
        self.exp = exp


class datbind:
    def __init__(self, tyvars, tycon, vcon):
        # vcon = [ VCon ]
        self.type = tycon
        self.vcon = vcon
        self.tyvars = tyvars


class Expression:
    def __init__(self, cls, reg):
        self.cls = cls
        self.reg = reg

