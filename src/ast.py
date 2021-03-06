class Unit:
    def __init__(self):
        pass

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s


class RecordItem:
    def __init__(self, lab, value):
        type = None
        self.lab = lab
        self.value = value
        self.type = type
        self.dict = locals()
        self.dict.pop('self', None)

    def isWild(self):
        return (self.lab is None) and (self.value is None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

    def calcType(self, env):
        self.type = self.value.calcType(env)
        return self.type


class TyCon:
    def __init__(self, tyvar=None, name=None, len=0, type=None, size=0):
        # tycon = ( string, int )
        self.tyvar = tyvar
        self.name = name
        self.type = type  # string for primitive type, dict for compound type
        self.len = len
        self.size = size
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

    def calcType(self, env):
        # TODO tyvars support
        if self.name in primative_tycon:  # primative type
            return self.name
        elif self.name in ['record', 'fn']:  # record or fn
            return self.type
        else:  # datatype or alias
            return self.type

    @staticmethod
    def calcSize(type):
        return 4


int_type = TyCon([], "int", 0, 'int', 4)
real_type = TyCon([], "real", 0, 'real', 4)
string_type = TyCon([], "string", 0, 'string', 4)
char_type = TyCon([], "char", 0, 'char', 1)
# record_type = TyCon([], "record", 0, None)
unit_type = TyCon([], "unit", 0, Unit(), 4)

primative_tycon = {
    'int': int_type,
    'real': real_type,
    'string': string_type,
    'char': char_type,
    'unit': unit_type,
}


def desent(level, x):
    if isinstance(x, tuple):
        print("  " * level, end="")
        print(x)
        for y in x:
            if y:
                desent(level + 1, y)

    elif isinstance(x, list):
        for y in x:
            if y:
                desent(level + 1, y)

    elif type(x) in (
            TyCon, Expression, Declaration, Value, typbind, valbind, datbind, Pattern, RecordItem, Unit, MRule, Match):
        print("  " * level, end="")
        # x.show()
        print(x)
        for y in x.dict.values():
            if y:
                desent(level + 1, y)


class SMLSyntaxError(BaseException):
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


IRTyName = {"int": "i32", "real": "float", "char": "i8",
            "string": "i8*", "unit": "void", "record": "i32*", "fn": "i32*"}


def calcLevels(env, name):
    if env is None:
        raise SMLSyntaxError("Syntax Error: identifier '{}' unbound.".format(name))
    elif name in env:
        # print("Search Env: ", env[name])
        return 0
    else:
        return 1 + calcLevels(env["__parent__"], name)


def appendNewScope(env):
    scope = {"__parent__": env, "__len__": 4, "__children__": []}
    env["__children__"].append(scope)
    return scope


def insertScope(env, name, value):
    """
    :param value: Value
    :return:
    """
    if name is None:
        return
    if name in env:
        raise SMLSyntaxError("Identifier '{}' rebound.".format(name))
    env[name] = (value, env["__len__"])
    env["__len__"] += TyCon.calcSize(value.type)


def searchTyCon(tyc, name, env):
    if not isinstance(tyc.type, list):
        return False
    for ele in tyc.type:
        if isinstance(name, Value):  # datatype without param
            if ele[0].id == name.id and ele[1] == unit_type:
                return True
        if isinstance(name, tuple):  # datatype with param
            if ele[0].id == name[0]:
                if len(name[1].value) == 1 and isinstance(ele[1].type, str):
                    return ele[1].type == name[1].value[0].value.calcType(env)
                else:
                    for index in range(len(name[1].value)):
                        if ele[1].type[index] == name[1].value[index].value.calcType(env):
                            pass
                        else:
                            return False
                    return True
    return False


def searchEnvO(env, name, typ=None):
    if typ is not None:
        if env is None:
            return None
        for ele in env.keys():
            if isinstance(env[ele], TyCon) and searchTyCon(env[ele], name, env):
                return ele
        return searchEnvO(env["__parent__"], name, 1)
    if env is None:
        raise SMLSyntaxError("Syntax Error: identifier '{}' unbound.".format(name))
    elif name in env:
        # print("Search Env: ", env[name])
        return env[name]
    else:
        return searchEnvO(env["__parent__"], name)


def getOffset(env, name):
    return searchEnvO(env, name)[1]


def searchEnv(env, name):
    t = searchEnvO(env, name)
    if isinstance(t, Value):
        pass
    return t[0]


class VCon:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.dict = locals()
        self.dict.pop('self', None)

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

    def __repr__(self):
        return self.__class__.__name__


class Declaration:
    def __init__(self, cls, bind):
        self.cls = cls
        self.bind = bind
        self.dict = locals()
        self.dict.pop('self', None)

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

    def __repr__(self):
        return self.__class__.__name__

    def checkType(self, env):
        if not self.bind.checkType(env):
            raise SMLSyntaxError("Valbind with different type.")
        else:
            return True

    def genCode(self, env, cg, getName, entry=False):
        self.bind.genCode(env, cg, getName, entry)


class Value:
    def __init__(self, id=None, value=None, tycon=None, vcon=None, wildcard=False, op=False):
        type = None
        self.id = id
        self.value = value
        self.tycon = tycon  # A TyCon instance
        self.vcon = vcon
        self.op = op
        self.type = type
        self.wildcard = wildcard
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

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
        # print("FlattenType: ", tycon)
        if tycon is None:
            return None
        name = tycon.calcType(env)
        if isinstance(name, tuple):
            # A function
            rtn = (Value.flattenType(env, name[0]), Value.flattenType(env, name[1]))
            # print("FN: ", rtn)
            return rtn
        elif isinstance(name, dict):  # records and user defined datatypes are all record
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

    def calcType(self, env):
        """
        :param env: dict[string, Value]
        :return: string | ( string | dict[string | int, string] ) | dict[string | int, string]
        """

        if self.type:
            return self.type
        self.type = Value.flattenType(env, self.tycon)
        # print("after",self)
        self.update()
        return self.type


class Pattern:
    def __init__(self, value, type=None):
        record = None
        size = None
        self.type = type
        self.size = size
        self.value = value
        self.record = record
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

    def update(self):
        for x in self.dict:
            self.dict[x] = getattr(self, x)

    def calcType(self, env):
        if isinstance(self.value, Value):
            self.type = self.value.calcType(env)
            self.size = TyCon.calcSize(self.type)
        elif isinstance(self.value, list):
            # record decompose binding
            t = {'__wildCard__': False}
            v = {"__len__": 0}
            for x in self.value:
                if x.lab is None and x.value is None:  # wildcard
                    t['__wildCard__'] = True
                else:
                    t[x.lab] = x.calcType(env)

            tmp = sorted(t.keys())
            tmp.remove('__wildCard__')
            for x in tmp:
                v[x] = v["__len__"]
                v["__len__"] += 4
                # v[x] = x.value # a issue here, nested pattern binding

            self.type = t
            self.record = v
            # print("Record Pattern: ", self.record)
        elif isinstance(self.value, tuple):
            tmp = searchEnvO(env, self.value, 1)
            if not tmp:
                raise SMLSyntaxError("Parameters doesn't match!")
            else:
                self.type = tmp

        self.update()
        return self.type

    def genCode(self, env, cg, src, getName, recordOffset=None, func=None):
        # src is i32* pointer to real value
        if isinstance(self.value, Value):
            if self.value.id is not None:
                cg.fillScope(src, getOffset(env, self.value.id), getName, func)
                cg.emitInst("; Pattern - Value")
        elif isinstance(self.value, list):
            # real value is a i32*, load as i32 and convert to i32*
            cg.emitInst("; Pattern - Record Enter")
            cg.indent += 1
            src = cg.intToPtr(cg.loadValue(src, getName), getName)
            for i in range(len(self.value)):
                x = self.value[i]
                if x.value is not None and x.lab is not None:
                    if recordOffset is not None:
                        tmp = cg.extractRecord(src, recordOffset[x.lab], getName)
                        x.value.genCode(env, cg, tmp, getName, recordOffset)
                    else:
                        tmp = cg.extractRecord(src, i * 4, getName)
                        # tmp = cg.loadValue(tmp,getName)
                        x.value.genCode(env, cg, tmp, getName, None, 1)

            cg.indent -= 1
            cg.emitInst("; Pattern - Record Exit")


class MRule:
    def __init__(self, pat, exp):
        self.pat = pat
        self.exp = exp
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s


class Match:
    def __init__(self, value, rules):
        self.value = value
        self.rules = rules
        self.dict = locals()
        self.dict.pop('self', None)

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s


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
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

    def checkType(self, env):
        self.typBind(env)
        return True

    def typBind(self, env):
        env[self.tycon] = TyCon(name=self.tycon, type=self.type, size=0, len=0, tyvar=self.param)


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
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

    def recordPatBind(self, env, pat, ty):
        v = pat.value
        if isinstance(v, list):  # record decompose
            if not isinstance(ty, dict):
                return False
            for x in v:
                if not self.recordPatBind(env, x.value, ty[x.lab]):
                    return False
        elif isinstance(v, Value):  # normal bind
            if v.type is None:
                v.type = ty
                v.update()
            elif v.type != ty:
                return False
            insertScope(env, v.id, v)  # env[v.id] = v
        return True

    @staticmethod
    def checkTypeExpPat(expType, patType):
        if type(expType) != type(patType):
            return False
        if isinstance(expType, str):
            return expType == patType
        elif isinstance(expType, tuple):
            return valbind.checkTypeExpPat(expType[1], patType[1]) and valbind.checkTypeExpPat(expType[0], patType[0])
        elif isinstance(expType, dict):
            key1 = expType.keys()
            key2 = patType.keys()
            if key1 & key2 == key1 | key2 or key1 <= key2 and key2 - key1 == {
                '__wildCard__'} or key1 >= key2 and key1 - key2 == {'__wildCard__'}:
                for key in key1 & key2:
                    if not valbind.checkTypeExpPat(expType[key], patType[key]):
                        return False
                return True
            elif not '__wildCard__' in key1 | key2:
                return False
            elif not '__wildCard__' in key1 & key2 and (
                                '__wildCard__' in key1 and expType[
                            '__wildCard__'] == False or '__wildCard__' in key2 and
                            expType['__wildCard__'] == False):
                return False
            elif not '__wildCard__' in key1 & key2 and '__wildCard__' in key1 and expType[ '__wildCard__'] and key2 > (key1 - '__wildCard__'):
                for key in key1 - '__wildCard__':
                    if not valbind.checkTypeExpPat(expType[key], patType[key]):
                        return False
                return True
            elif '__wildCard__' in key1 & key2 and expType['__wildCard__'] and patType['__wildCard__']:
                for key in (key1 & key2) - '__wildCard__':
                    if not valbind.checkTypeExpPat(expType[key], patType[key]):
                        return False
                return True
            # TODO
            return False

    def checkType(self, env):
        """
        :param env: dict
        :return: bool
        """
        self.pat.calcType(env)
        if self.rec:
            # simple bind, function
            assert isinstance(self.pat.value, Value)
            insertScope(env, self.pat.value.id, self.pat.value)
        self.exp.calcType(env)

        if self.rec or self.recordPatBind(env, self.pat, self.exp.type):
            self.pat.update()
            self.pat.calcType(env)
            return True
        else:
            return False

    def genCode(self, env, cg, getName, entry=False):
        if entry:
            cg.enterMain(env, getName)
        else:
            cg.emitInst("; valbind enter")
            cg.indent += 1
        pat = self.pat
        rtnName = self.exp.genCode(env, cg, getName)

        if entry:
            n1 = getName()
            cg.emitInst("{} = load {}* {}, align {}".format(n1, IRTyName[pat.type], rtnName, self.pat.size))
            cg.rtnMain(n1)
        else:
            if self.exp.cls == "Fn":
                pat.genCode(env, cg, rtnName, getName, self.exp.record, 1)
            else:
                pat.genCode(env, cg, rtnName, getName, self.exp.record)
            cg.indent -= 1
            cg.emitInst("; valbind exit")


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
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

    def checkType(self, env):
        self.datBind(env)
        return True

    def datBind(self, env):
        env[self.type] = TyCon(name=self.type, len=0, size=0, type=self.vcon, tyvar=self.tyvars)


class Expression:
    def __init__(self, cls, reg):
        """
        :param cls: string
        :param reg: tuple
        """
        type = None
        scope = None
        record = None
        letScope = None
        self.cls = cls
        self.reg = reg
        self.dict = locals()
        self.dict.pop('self', None)

        self.type = type
        self.scope = scope
        self.record = record
        self.letScope = letScope

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        tmp = self.dict.pop('scope', None)
        s = self.dict.__str__()
        if tmp:
            self.dict['scope'] = tmp
        return s

    @staticmethod
    def flattenBind(env, pat):
        if isinstance(pat.value, Value):
            insertScope(env, pat.value.id, pat.value)
            # env[pat.value.id] = pat.value
        elif isinstance(pat.value, list):
            for x in pat.value:
                if x.value is not None:
                    Expression.flattenBind(env, x.value)
        elif isinstance(pat.value, tuple):
            for x in pat.value[1].value:
                Expression.flattenBind(env, x.value)

    @staticmethod
    def calcAppList(applist, env):
        """
        :param applist: list[Expression]
        :param env: dict
        """
        # print("calcApplist")
        applist[0].calcType(env)
        rtn = applist[0].type  # function type

        for i in range(1, len(applist)):
            x = applist[i]
            """ :type : Expression """
            x.calcType(env)
            if rtn[0] != x.type:
                raise SMLSyntaxError("Parameters doesn't match!")
            else:
                rtn = rtn[1]

        return rtn

    def update(self):
        for x in self.dict:
            self.dict[x] = getattr(self, x)

    def calcFun(self, env):
        # assert len(self.reg) == 1 # datatype is not supported not
        # x = r[0]
        patType = None
        expType = None
        for x in self.reg:
            """ :type:(Pattern, Expression)"""
            if isinstance(x[0].value, Value):  # 1.single value 2.constant 3.wildcard 4.datatype without param
                # print("calcFun::value") ######
                if x[0].value.wildcard:  # wildcard
                    if patType is not None:
                        x[0].type = patType
                        x[0].update()
                else:
                    param = x[0].calcType(env)
                    if isinstance(param, str):  # constant ; single value with ty mentioned
                        if patType is not None and patType != param:
                            raise SMLSyntaxError("Parameters doesn't match!")
                        else:
                            patType = param
                    elif param is None:  # datatype without param; single value without ty mentioned
                        tmp = searchEnvO(env, x[0].value, 1)
                        if not tmp:  # cannot find datatype in env
                            raise SMLSyntaxError("Parameters doesn't match!")
                        if patType is not None and patType != tmp:
                            raise SMLSyntaxError("Parameters doesn't match!")
                        else:
                            patType = tmp

            elif isinstance(x[0].value, tuple):  # datatype with param
                # print("calcFun:: tuple")   #####
                tmp = searchEnvO(env, x[0].value, 1)
                if not tmp:
                    raise SMLSyntaxError("Parameters doesn't match!")
                elif patType is not None and patType != tmp:
                    raise SMLSyntaxError("Parameters doesn't match!")
                else:
                    patType = tmp

            elif isinstance(x[0].value, list):  # [RecordItem,...]
                x[0].calcType(env)
                t = x[0].type
                if patType is None:
                    patType = t
                elif not isinstance(patType, dict):
                    raise SMLSyntaxError("Parameters doesn't match!")
                else:
                    if not patType['__wildCard__']:
                        if not ((patType.keys() | t.keys()) == patType.keys()):
                            raise SMLSyntaxError("Parameters doesn't match!")

                    if not t['__wildCard__']:
                        if not ((patType.keys() | t.keys()) == t.keys()):
                            raise SMLSyntaxError("Parameters doesn't match!")

                    for ele in patType.keys() & t.keys():
                        if ele != "__wildCard__" and t[ele] == patType[ele]:
                            pass
                        elif ele != "__wildCard__" and t[ele] != patType[ele]:
                            raise SMLSyntaxError("Parameters doesn't match!")

                    if not t['__wildCard__']:
                        patType = t

                    elif patType['__wildCard__']:
                        patType = dict(patType, **t)

            scope = appendNewScope(env)
            # bind to new scope
            # check expression return type
            # print("before exp.flattern")
            Expression.flattenBind(scope, x[0])
            exp = x[1].calcType(scope)
            if expType is not None and expType != exp:
                raise SMLSyntaxError("Parameters doesn't match!")
            else:
                expType = exp
        if '__wildCard__' in patType:
            del (patType['__wildCard__'])
        return patType, expType

    def calcType(self, env):
        cls = self.cls
        r = self.reg
        """ :type : list[exp] | Value | [RecordItem] """
        self.scope = env
        if cls == "App":
            if isinstance(r, Value):
                # print("R: ", r)
                v = searchEnv(env, r.id)
                self.type = v.calcType(env)
            else:
                # don't care about op
                # function should be the first argument
                self.type = Expression.calcAppList(r, env)
        elif cls == "Let":
            scope = appendNewScope(env)
            self.letScope = scope
            decs, exp = r
            for x in decs:
                # create a new scope
                x.checkType(scope)
            exp.calcType(scope)
            self.type = exp.type
        elif cls == "EXPS":
            for x in r:
                x.calcType(env)
            self.type = r[-1].type
        elif cls == "Constant":
            self.type = r.calcType(env)
        elif cls == "Record":
            t = {}
            v = {"__len__": 0}
            for x in r:
                assert isinstance(x, RecordItem)
                x.calcType(env)
                t[x.lab] = x.type

            for x in sorted(t.keys()):
                v[x] = v["__len__"]
                v["__len__"] += 4

            self.type = t
            self.record = v
        elif cls == "Fn":
            self.type = self.calcFun(env)

        self.update()
        return self.type

    def genCode(self, env, cg, getName):
        """
        :param cg: CodeGenerator
        :param resultName: String
        :return:
        """
        cls = self.cls
        r = self.reg
        """ :type : list[exp] | Value | [RecordItem] """
        self.scope = env
        if cls == "App":
            if isinstance(r, Value):
                # print("R: ", r)
                n = cg.extractVar(getOffset(env, r.id), calcLevels(env, r.id), getName)
                cg.emitInst("; Expression -- App {}".format(r.id))
                return n

            else:
                # don't care about op
                # function should be the first argument
                caller = r[0]

                print("Debug: ", caller)
                assert len(r) == 2

                fun = cg.intToPtr(cg.loadValue(caller.genCode(env, cg, getName), getName), getName)
                callEnv = cg.extractRecord(fun, 0, getName)
                fp = cg.extractRecord(fun, 4, getName)
                rtn = None
                for i in range(1, len(r)):
                    p = r[i]
                    param = p.genCode(env, cg, getName)
                    arg = cg.createParam(getName, callEnv, param)
                    type = None
                    if isinstance(caller.reg, Value):
                        type = searchEnv(env, caller.reg.id).type
                    elif caller.cls == "App":
                        type = caller.type
                    rtn = cg.callFunc(type, cg.loadValue(fp, getName), arg, getName)

                return rtn
        elif cls == "Let":
            cg.emitInst("; Expression -- Let Start")
            scope = self.letScope
            cg.pushNewScope(getName, scope["__len__"])
            decs, exp = r
            for x in decs:
                # create a new scope
                x.genCode(scope, cg, getName)

            rtnName = None
            if isinstance(exp, list):
                for x in exp:
                    rtnName = x.genCode(scope, cg, getName)
            else:
                rtnName = exp.genCode(scope, cg, getName)

            cg.popScope(getName)
            cg.emitInst("; Expression -- Let End")

            return rtnName
        elif cls == "EXPS":
            rtnName = None
            for x in r:
                rtnName = x.genCode(env, cg, getName)
            return rtnName
        elif cls == "Constant":
            x = None
            if r.isConsStr():
                x = cg.emitGlobalStr(r.value + '\x00')
                x = "i8* getelementptr inbounds ([{} x i8]* {}, i32 0, i32 0)".format(len(r.value) + 1, x)
            else:
                x = str(r.value)
                # TODO char
                x = "{} {}".format(IRTyName[r.type], r.value)

            align, n1 = TyCon.calcSize(self.type), getName()
            cg.allocate(n1, IRTyName[self.type], align)
            cg.emitInst("store {}, {}* {}, align {}".format(x, IRTyName[r.type], n1, align))
            if r.type != 'int':
                n2 = getName()
                cg.emitInst("{} = bitcast {}* {} to i32*".format(n2, IRTyName[r.type], n1))
                n1 = n2

            cg.emitInst("; Expression -- Constant ")
            return n1
        elif cls == "Record":
            cg.emitInst("; Expression -- Record Enter")
            cg.indent += 1
            rtn, n1 = cg.createRecord(self.record["__len__"], getName)
            for x in r:
                rst = x.value.genCode(env, cg, getName)
                cg.fillRecord(rst, n1, self.record[x.lab], getName)

            cg.indent -= 1
            cg.emitInst("; Expression -- Record Exit")
            return rtn
        elif cls == "Fn":
            cg.emitInst("; Expression -- FN")

            getName_fun, getLabel, funName = cg.decFuncHead(self.type)  # print function head
            self.genCodeFuncBody(cg, env, getName_fun, getLabel, self.type)
            rtnName = cg.decFuncTail(getName, funName, self.type)

            return rtnName

    def genCodeFuncBody(self, cg, env, getName, getLabel, typ):
        for i in range(len(self.reg)):  # self.reg : [(pattern,exp),...]
            x = self.reg[i]
            if isinstance(x[0].value, Value) and isinstance(x[0].type, str):  # constant wildcard x
                scope = x[1].scope
                if x[0].value.wildcard:  # wildcard
                    cg.pushNewScope(getName, scope["__len__"])
                    n = x[1].genCode(env, cg, getName)
                    cg.MRuleRet(n, getName)
                    if i != len(self.reg):
                        l1 = getLabel()
                        cg.emitInst("{}:".format(l1))
                elif x[0].value.value is not None:  # constant
                    comp = cg.MRuleCompare(x[0].value.value, "%param", getName, getLabel)
                    l1, l2 = getLabel(), getLabel()
                    cg.MRuleBr1(comp, l1, l2)
                    cg.pushNewScope(getName, scope["__len__"])
                    n = x[1].genCode(env, cg, getName)
                    cg.MRuleRet(n, typ[1], getName)
                    cg.MRuleBr2(l2)
                else:  # x
                    cg.emitInst("; value binding")
                    cg.pushNewScope(getName, scope["__len__"])
                    x[0].genCode(scope, cg, "%param", getName)
                    n = x[1].genCode(scope, cg, getName)
                    cg.MRuleRet(n, typ[1], getName)

            elif isinstance(x[0].value, list):  # compound type
                FLabel = getLabel()
                scope = x[1].scope
                cg.emitInst("; compound binding")
                cg.MRuleCompare(x[0].value, "%param", getName, getLabel, FLabel, typ[0], x[0].record)  # compare pattern
                cg.pushNewScope(getName, scope["__len__"])
                x[0].genCode(x[1].scope, cg, "%param", getName, None, 1)  # fill scope
                n = x[1].genCode(x[1].scope, cg, getName)  # calc exp
                cg.MRuleRet(n, typ[1], getName)
                cg.emitInst("{}:".format(FLabel))
