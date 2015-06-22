class SMLSyntaxError(BaseException):
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


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

    def checkType(self):
        # TODO tyvars support
        if self.name in primative_tycon: # primative type
            return self.name
        elif self.name == 'unit': # unit
            return self.name
        elif self.name in ['record', 'fn'] : # record or fn
            return self.type
        else: # datatype or alias
            # TODO not sure now
            return self.name


int_type    = TyCon([], "int", 0, 'int')
real_type   = TyCon([], "real", 0, 'real')
string_type = TyCon([], "string", 0, 'string')
char_type   = TyCon([], "char", 0, 'char')
# record_type = TyCon([], "record", 0, None)
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
        if not self.bind.checkType(env):
            raise SMLSyntaxError("Valbind with different type.")
        else:
            return True


class Value :
    def __init__(self, id = None, value = None, tycon = None, vcon = None, wildcard = False, op = False):
        self.id = id
        self.value = value
        self.tycon = tycon # A TyCon instance
        self.vcon = vcon
        self.op = op
        self.wildcard = wildcard
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
        """
        :param env: dict[string, Value]
        :return: string | ( string | dict[string | int, string] ) | dict[string | int, string]
        """
        if type(self.tycon) == tuple:
            # A function call
            rtn = (self.tycon[0].checkType(), self.tycon[1].checkType())
            print("FN: ", rtn)
            return rtn #(self.tycon[0].checkType(), self.tycon[1].checkType())
        else:
            name = self.tycon.name
            if name in primative_tycon:
                return name
            elif name == 'unit':
                return name
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
        self.pat.update()
        self.exp.calcType(env)
        print("Valbind: ", self.pat.value)
        if self.pat.type == self.exp.type:
            print("valbind checked: ", self.pat.value.id)
            env[self.pat.value.id] = self.pat.value
            return True
        else:
            return False


class datbind:
    def __init__(self, tyvars, tycon, vcon):
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
        type = None
        self.cls = cls
        self.reg = reg
        self.dict = locals()
        self.dict.pop('self', None)

        self.type = type

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

    def calcAppList(self, applist, env):
        """
        :param applist: list[Expression]
        :param env: dict
        """

        applist[0].calcType(env)
        rtn = applist[0].type # function type

        for i in range(1, len(applist)):
            x = applist[i]
            """ :type : Expression """
            x.calcType(env)
            print('Function call ', i, ' : ', rtn)
            if rtn[0] != x.type:
                raise SMLSyntaxError("Parameters doesn't match!")
            else:
                rtn = rtn[1]

        return rtn

    def update(self):
        for x in self.dict:
            self.dict[x] = getattr(self, x)

    def calcType(self, env):
        # print(self)
        cls = self.cls
        if cls == "App":
            r = self.reg
            """ :type : list[exp] | Value"""
            if type(r) == Value:
                print("R: ", r)
                self.type = env[r.id].calcType(env)
            else:
                # don't care about op
                # function should be the first argument
                self.type = self.calcAppList(r, env)
        elif cls == "Let":
            print("LET: ", self)
            decs, exp = self.reg
            for x in decs:
                x.checkType(env)
            if type(exp) == list:
                for x in exp:
                    x.calcType(env)
                self.type = exp[-1].type
            else:
                exp.calcType(env)
                self.type = exp.type
        elif cls == "Constant":
            r = self.reg
            """ :type : Value """
            self.type = r.calcType(env)

        self.update()



