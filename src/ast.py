

class TypeExpression :
    def __init__(self):
        pass


class Unit:
    def __init__(self):
        pass

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()


class RecordItem:
    def __init__(self, lab, value):
        self.lab = lab
        self.value = value
        self.dict = locals()
        self.dict.pop('self', None)

    def isWild(self):
        return (self.lab == None) and (self.value == None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()


class TyCon:
    def __init__(self, tyvar = [], name = None, len = 0, type = None):
        # tycon = ( string, int )
        self.tyvar  = tyvar
        self.name   = name
        self.type   = type # string for primitive type, dict for compound type
        self.len    = len
        self.dict   = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

int_type    = TyCon([], "int", 0, 'int')
real_type   = TyCon([], "real", 0, 'real')
string_type = TyCon([], "string", 0, 'string')
char_type   = TyCon([], "char", 0, 'char')
record_type = TyCon([], "record", 0, None)
unit_type   = TyCon([], "unit", 0, Unit())

primative_tycon = {
    'int'       : int_type,
    'real'      : real_type,
    'string'    : string_type,
    'char'      : char_type
}


class VCon:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.dict = locals()
        self.dict.pop('self', None)

    def __str__(self):
        return self.dict.__str__()

    def __repr__(self):
        return self.__class__.__name__


class Declaration :
    def __init__(self, cls, binds):
        self.cls = cls
        self.bind = binds
        self.dict = locals()
        self.dict.pop('self', None)

    def __str__(self):
        return self.dict.__str__()

    def __repr__(self):
        return self.__class__.__name__

    def checkType(self, env):
        return self.bind.checkType(env)


class Value :
    def __init__(self, id = None, value = None, tycon = None, vcon = None, wildcard = False, OP = False):
        self.id = id
        self.value = value
        self.tycon = tycon # A TyCon instance
        self.vcon = vcon
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

    def update(self):
        for x in self.dict:
            self.dict[x] = getattr(self, x)

    def calcType(self, env):
        name = self.tycon.name
        if name in primative_tycon:
            return name
        elif name == 'unit':
            return Unit()
        else: # records and user defined datatypes are all records
            l = self.value
            """:type : list[RecordItem]"""
            if type(l) == list:
                t = {}
                for x in l:
                    assert(type(x) == RecordItem)
                    t[x.lab] = x.value

                return t
            else:
                # get a way to check if it is a datatype
                # return name now, should return the whole datatype as tuple ('datatype', dict[dict[string, string]]
                return name


class Pattern :
    def __init__(self, value):
        type = None
        self.type = type
        self.value = value
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

    def update(self):
        for x in self.dict:
            self.dict[x] = getattr(self, x)

    def calcType(self, env):
        self.type = self.value.calcType(env)


class Constant :
    def __init__(self, value, ctype):
        self.value = value
        self.ctype = ctype
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()


class MRule:
    def __init__(self, pat, exp):
        self.pat = pat
        self.exp = exp
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

class Match:
    def __init__(self, value, rules):
        self.value = value
        self.rules = rules
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()


class typbind:
    def __init__(self, param, tycon, type):
        self.param = param
        self.tycon = tycon
        self.type = type
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()


class valbind:
    def __init__(self, pat, exp):
        """
        :param pat: Pattern
        :param exp: Expression
        """
        self.pat = pat
        self.exp = exp
        self.rec = False
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

    def checkType(self, env):
        """
        :param env: dict
        :return: bool
        """
        self.pat.calcType(env)
        self.exp.checkType(env)
        return self.pat.type == self.exp.type


class datbind:
    def __init__(self, tyvars, tycon, vcon):
        # vcon = [ VCon ]
        self.type = tycon
        self.vcon = vcon
        self.tyvars = tyvars
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()


class Expression:
    def __init__(self, cls, reg):
        """
        :param cls: string
        :param reg: tuple
        """
        self.cls = cls
        self.reg = reg
        self.dict = locals()
        self.dict.pop('self', None)

        self.type = None

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

    def calcAppList(self, applist, env):
        """
        :param applist: list[Expression]
        :param env: dict
        """
        for x in applist:
            x.checkType(env)
            print(x)

        return True

    def update(self):
        for x in self.dict:
            self.dict[x] = getattr(self, x)

    def checkType(self, env):
        cls = self.cls
        if cls == "App":
            r = self.reg
            """ :type : list[exp] | Value """
            if type(r) == Value:
                print(r)
                self.type = r.calcType(env)
                self.update()
            else:
                # don't care about op
                # function should be the first argument
                self.type = self.calcAppList(r, env)
                self.update()
                return True
        elif cls == "Let":
            decs, exp = self.reg
            for x in decs:
                x.checkType(env)
            exp.checkType(env)



