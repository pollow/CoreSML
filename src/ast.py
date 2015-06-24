class SMLSyntaxError(BaseException):
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


IRTyName = {"int" : "i32", "real": "float", "char": "i8", "string": "i8*"}


def appendNewScope(env):
    scope = {"__parent__": env, "__len__": 0, "__children__": []}
    env["__children__"].append(scope)
    return scope


def searchEnv(env, name):
    if env == None:
        raise SMLSyntaxError("Syntax Error: identifier '{}' unbound.".format(name))
        return None
    elif name in env:
        return env[name]
    else:
        return searchEnv(env["__parent__"], name)


class Unit:
    def __init__(self):
        pass

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()


class RecordItem:
    def __init__(self, lab, value):
        type = None
        self.lab = lab
        self.value = value
        self.type = type
        self.dict = locals()
        self.dict.pop('self', None)


    def isWild(self):
        return (self.lab == None) and (self.value == None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

    def calcType(self, env):
        self.type = self.value.calcType(env)
        return self.type


class TyCon:
    def __init__(self, tyvar = [], name = None, len = 0, type = None, size = 0):
        # tycon = ( string, int )
        self.tyvar  = tyvar
        self.name   = name
        self.type   = type # string for primitive type, dict for compound type
        self.len    = len
        self.size   = size
        self.dict   = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

    def checkType(self, env):
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


int_type    = TyCon([], "int", 0, 'int', 4)
real_type   = TyCon([], "real", 0, 'real', 4)
string_type = TyCon([], "string", 0, 'string', 4)
char_type   = TyCon([], "char", 0, 'char', 1)
# record_type = TyCon([], "record", 0, None)
unit_type   = TyCon([], "unit", 0, Unit(), 4)

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

    def genCode(self, getName):
        self.bind.genCode()



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

    def isConstant(self):
        return self.value is not None and \
               self.id is None and \
               self.tycon is not None

    def isConsStr(self):
        return self.isConstant() and self.tycon is string_type

    def update(self):
        for x in self.dict:
            self.dict[x] = getattr(self, x)


    @staticmethod
    def flattenType(env, tycon):
        print("FlattenType: ", tycon)
        name = tycon.checkType(env)
        if isinstance(name, tuple):
            # A function
            rtn = (Value.flattenType(env, name[0]), Value.flattenType(env, name[1]))
            print("FN: ", rtn)
            return rtn
        elif isinstance(name, dict): # records and user defined datatypes are all record
            # just a record type descriptor
            t = {}
            for x in name:
                t[x] = Value.flattenType(env, name[x])

            return t
        elif isinstance(name, str):
            return name
        else:
            # get a way to check if it is a datatype
            # return name now, should return the whole datatype as tuple ('datatype', dict[dict[string, string]]
            raise SMLSyntaxError("Unexpected type check in FlattenType: {}".format(tycon))
            return name


    def calcType(self, env):
        """
        :param env: dict[string, Value]
        :return: string | ( string | dict[string | int, string] ) | dict[string | int, string]
        """
        return Value.flattenType(env, self.tycon)
        # name = self.tycon.checkType(env)
       #  if isinstance(name, tuple):
       #      # A function
       #      rtn = (name[0].checkType(env), name[1].checkType(env))
       #      # rtn = (self.flattenType(env, name[0]), self.flattenType(env, name[1]))
       #      print("FN: ", rtn)
       #      return rtn #(self.tycon[0].checkType(), self.tycon[1].checkType())
       #  elif isinstance(name, dict): # records and user defined datatypes are all record
       #      # just a record type descriptor
       #      t = {}
       #      tys = self.tycon.type
       #      for x in tys:
       #          t[x] = tys[x].type

       #      return t
       #  elif isinstance(name, str):
       #      return name
       #  else:
       #      # get a way to check if it is a datatype
       #      # return name now, should return the whole datatype as tuple ('datatype', dict[dict[string, string]]
       #     return name




class Pattern :
    def __init__(self, value, type=None):
        record = None
        self.type = type
        self.value = value
        self.record = record
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
        if isinstance(self.value, Value):
            self.type = self.value.calcType(env)
        elif isinstance(self.value, list):
            # record decompose binding
            t = {}
            v = {}
            for x in self.value:
                t[x.lab] = x.calcType(env)
                v[x.lab] = x.value # a issue here, nested pattern binding

            self.type = t
            self.record = v


        self.update()
        return self.type


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

    def recordPatBind(self, env, pat):
        v = pat.value
        if isinstance(v, list): # record decompose
            for x in v:
                self.recordPatBind(env, x.value)
        elif isinstance(v, Value): # normal bind
            env[v.id] = v


    def checkType(self, env):
        """
        :param env: dict
        :return: bool
        """
        if self.pat.calcType(env) == self.exp.calcType(env): # primative type
            print("valbind checked: ", self.pat.value)
            if isinstance(self.pat.value, list): # reocord
                self.recordPatBind(env, self.pat)
            else:
                env[self.pat.value.id] = self.pat.value
            return True
        else:
            return False

    def genCode(self, cg, getName):
        pat = self.pat
        name = getName()
        cg.allocate(name, IRTyName[pat.type.name], self.pat.type.size)
        self.exp.genCode(cg, getName, name)
        # cg.assign(name, IRTyName[self.pat.type.name], self.pat.type.size)
        if pat.type in primative_tycon:
            cg.assign(pat.offset, name)


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
        scope = None
        record = None
        self.cls = cls
        self.reg = reg
        self.dict = locals()
        self.dict.pop('self', None)

        self.type = type
        self.scope = scope
        self.record = None

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self.dict.__str__()

    @staticmethod
    def flattenBind(env, pat):
        if isinstance(pat.value, Value):
            env[pat.value.id] = pat.value
        elif isinstance(pat.value, list):
            for x in pat.value:
                Expression.flattenBind(env, x.value)


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
        print("Get into an expression, the scope is: ", env)
        cls = self.cls
        r = self.reg
        """ :type : list[exp] | Value | [RecordItem] """
        self.scope = env
        if cls == "App":
            if isinstance(r, Value):
                print("R: ", r)
                v = searchEnv(env, r.id)
                self.type = v.calcType(env)
            else:
                # don't care about op
                # function should be the first argument
                self.type = self.calcAppList(r, env)
        elif cls == "Let":
            print("LET: ", self)
            scope = appendNewScope(env)
            decs, exp = r
            for x in decs:
                # create a new scope
                x.checkType(scope)
            if isinstance(exp, list):
                for x in exp:
                    x.calcType(scope)
                self.type = exp[-1].type
            else:
                exp.calcType(scope)
                self.type = exp.type
        elif cls == "Constant":
            self.type = r.calcType(env)
        elif cls == "Record":
            t = {}
            v = {}
            for x in r:
                assert isinstance(x, RecordItem)
                x.calcType(env)
                t[x.lab] = x.type
                v[x.lab] = x.value

            self.type = t
            self.record = v
        elif cls == "Fn":
            assert len(self.reg) == 1 # datatype is not supported not
            x = r[0]
            """ :type:(Pattern, Expression)"""
            param = x[0].calcType(env)
            scope = appendNewScope(env)
            # bind to new scope
            # check expression return type
            Expression.flattenBind(scope, x[0])
            exp = x[1].calcType(scope)
            self.type = (param, exp)


        self.update()
        return self.type



