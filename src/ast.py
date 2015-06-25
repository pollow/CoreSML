class SMLSyntaxError(BaseException):
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


IRTyName = {"int" : "i32", "real": "float", "char": "i8", "string": "i8*", "unit": "void"}

def calcLevels(env, name):
    if env == None:
        raise SMLSyntaxError("Syntax Error: identifier '{}' unbound.".format(name))
        return None
    elif name in env:
        print("Search Env: ", env[name])
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
    if name in env:
        raise SMLSyntaxError("Identifier '{}' rebound.".format(name))
    env[name] = (value, env["__len__"])
    env["__len__"] += TyCon.calcSize(value.type)


def searchTyCon(tyc,name):
    if not isinstance(tyc.type,list):
        return False
    for ele in tyc.type: 
        if isinstance(name,Value): #datatype without param
            if ele[0].id==name.id and ele[1]==unit_type:
                return True
        if isinstance(name,tuple): #datatype with param
            if ele[0].id==name[0]:
                if len(name[1].value)==1 and isinstance(ele[1].type,str):
                    return ele[1].type==(name[1].value)[0].value.calcType()
                else:
                    for index in range(len(name[1].value)):
                        if (ele[1].type)[index]==(name[1].value)[index].value.calcType():
                            pass
                        else:
                            return False
                    return True
    return False

def searchEnvO(env, name, typ=None):
    if typ!=None:
        if env==None:
            return None
        for ele in env.keys():
            if isinstance(env[ele],TyCon) and searchTyCon(env[ele],name):
                return ele
        return searchEnvO(env["__parent__"], name , 1)
    if env == None:
        raise SMLSyntaxError("Syntax Error: identifier '{}' unbound.".format(name))
        return None
    elif name in env:
        print("Search Env: ", env[name])
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

    def calcType(self, env):
        # TODO tyvars support
        if self.name in primative_tycon: # primative type
            return self.name
        elif self.name == 'unit': # unit
            return self.name
        elif self.name in ['record', 'fn'] : # record or fn
            return self.type
        else: # datatype or alias
            return self.type

    @staticmethod
    def calcSize(type):
        if type is None:
            raise SMLSyntaxError("Type not determined when calculate size.")
        elif isinstance(type, str):
            if type == "char":
                return 1
            else:
                return 4
        elif isinstance(type, tuple): #function call
            return 8 # function pointer and env
        else:
            return 4



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

    def genCode(self, env, cg, getName, entry = False):
        self.bind.genCode(env, cg, getName, entry)



class Value :
    def __init__(self, id = None, value = None, tycon = None, vcon = None, wildcard = False, op = False):
        type = None
        self.id = id
        self.value = value
        self.tycon = tycon # A TyCon instance
        self.vcon = vcon
        self.op = op
        self.type = type
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
        name = tycon.calcType(env)
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
        self.type = Value.flattenType(env, self.tycon)
        self.update()
        return self.type


class Pattern :
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
        return self.dict.__str__()

    def update(self):
        for x in self.dict:
            self.dict[x] = getattr(self, x)

    def calcType(self, env):
        if isinstance(self.value, Value):
            self.type = self.value.calcType(env)
            self.size = TyCon.calcSize(self.type)
        elif isinstance(self.value, list):
            # record decompose binding
            t = {}
            v = {}
            for x in self.value:
                t[x.lab] = x.calcType(env)
                v[x.lab] = x.value # a issue here, nested pattern binding

            # index = 0
            # for x in v:
            #     v[x] = (v[x], index)
            #     index += v[x][0].calcSize()

            self.type = t
            self.record = v
            print("Record Pattern: ", self.record)
        elif isinstance(self.value,tuple):
            tmp=searchEnvO(env,self.value,1)
            if tmp==False:
                raise SMLSyntaxError("Parameters doesn't match!")
            else:
                self.type=tmp

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

    def checkType(self, env):
        self.typBind(env)
        return True

    def typBind(self,env):
        env[self.tycon]=Tycon(name=self.tycon,type=self.type,size=0,len=0,tyvar=self.param)


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
            insertScope(env, v.id, v) # env[v.id] = v


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
                insertScope(env, self.pat.value.id, self.pat.value)
                # env[self.pat.value.id] = self.pat.value
            return True
        else:
            return False

    def genCode(self, env, cg, getName, entry = False):
        if entry:
            cg.enterMain()
        pat = self.pat
        # only 1 assginment
        rtnName = self.exp.genCode(env, cg, getName)

        if entry:
            n1 = getName()
            cg.emitInst("{} = load {}* {}, align {}".format(n1, IRTyName[pat.type], rtnName, self.pat.size))
            cg.rtnMain(n1)
        else:
            cg.fillScope(rtnName, int(getOffset(env, self.pat.value.id)/4), getName)
            cg.emitInst("; Valbind")

        # cg.assign(name, IRTyName[self.pat.type.name], self.pat.type.size)
        # if pat.type in primative_tycon:
        #     cg.assign(pat.offset, n1)


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

    def checkType(self,env):
        self.datBind(env)
        return True
    
    def datBind(self,env):
        env[self.type]=TyCon(name=self.type,len=0,size=0,type=self.vcon,tyvar=self.tyvars)



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
        return self.dict.__str__()

    @staticmethod
    def flattenBind(env, pat):
        if isinstance(pat.value, Value):
            insertScope(env, pat.value.id, pat.value)
            # env[pat.value.id] = pat.value
        elif isinstance(pat.value, list):
            for x in pat.value:
                Expression.flattenBind(env, x.value)
        elif isinstance(pat.value,tuple):
            for x in (pat.value)[1].value:
                Expression.flattenBind(env,x.value)



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

    def calcFun(self,env,typ=1):
        #assert len(self.reg) == 1 # datatype is not supported not
        #x = r[0]
        patType=None
        expType=None
        for x in r: 
            """ :type:(Pattern, Expression)"""
            if isinstance(x[0].value,Value):# 1.single value 2.constant 3.wildcard 4.datatype without param
                if x[0].value.wildcard==True: # wildcard
                    pass #do nothing
                else :
                    param = x[0].calcType(env)
                    if isinstance(param,str): # constant ; single value with ty mentioned
                        if patType != None and patType !=param:
                            raise SMLSyntaxError("Parameters doesn't match!")
                        else:
                            patType=param
                    elif param==None: # datatype without param
                        tmp=searchEnvO(env,x[0].value,1)
                        if tmp==False: # cannot find datatype in env
                            raise SMLSyntaxError("Parameters doesn't match!")
                        if patType != None and patType != tmp:
                            raise SMLSyntaxError("Parameters doesn't match!")
                        else:
                            patType=tmp;

            elif isinstance(x[0].value,tuple): #datatype with param
                tmp=searchEnvO(env,x[0].value,1)
                if tmp==False:
                    raise SMLSyntaxError("Parameters doesn't match!")
                elif patType!= None and patType != tmp:
                    raise SMLSyntaxError("Parameters doesn't match!")
                else:
                    patType=tmp

            elif isinstance(x[0].value,list): #[RecordItem,...]
                t={"__wildCard__":False}
                for element in x[0].value:
                    if element.value==None and element.lab==None:
                        t['__wildCard__']=True
                    else:
                        tmp=element.value.calcType()
                        t[element.lab]=tmp
                if patType == None:
                    patType=t
                elif not isinstance(patType,dict):
                    raise SMLSyntaxError("Parameters doesn't match!")
                else:
                    if patType['__wildCard__']==False:
                        if not ((patType.keys() | t.keys())==patType.keys()):
                            raise SMLSyntaxError("Parameters doesn't match!")

                    if t['__wildCard__']==False:
                        if not ((patType.keys() | t.keys())==t.keys()):
                            raise SMLSyntaxError("Parameters doesn't match!")
                        
                    for ele in patType.keys() & t.keys():
                        if ele != "__wildCard__" and t[ele]==patType[ele]:
                            pass
                        elif ele != "__wildCard__" and t[ele]!=patType[ele]:
                            raise SMLSyntaxError("Parameters doesn't match!")

                    if t['__wildCard__']==False:
                        patType=t

                    elif patType['__wildCard__']==True:
                        patType=dict(patType,**t)


            scope = appendNewScope(env)
            # bind to new scope
            # check expression return type
            Expression.flattenBind(scope, x[0])
            exp = x[1].calcType(scope)
            if expType != None and expType != exp:
                raise SMLSyntaxError("Parameters doesn't match!")
            else:
                expType=exp

        return (patType,expType)

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
            self.letScope = scope
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

            # index = 0
            # for x in v:
            #     v[x] = (v[x], index)
            #     index += v[x][0].calcSize()

            self.type = t
            self.record = v
            print("Record Expression: ", self.record)
        elif cls == "Fn":
            self.type=calcFun(env)

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
                print("R: ", r)
                n = cg.extractVar(int(getOffset(env, r.id)/4), calcLevels(env, r.id), getName)
                cg.emitInst("; Expression -- App ")
                return n

            else:
                # don't care about op
                # function should be the first argument
                caller = r[0]
                fnEnv = caller.genCode(env, cg, getName)
                assert isinstance(caller.reg, Value)
                assert len(r) == 2
                for i in range(1, len(r)):
                    p = r[i]
                    param = p.genCode(env, cg, getName)
                    callEnv = cg.createParam(getName, fnEnv, param)
                    rtn = cg.callFunc(searchEnv(env, caller.reg.id), callEnv, getName)

                return rtn
                r.reverse()
        elif cls == "Let":
            print("Let: ", self)
            scope = self.letScope
            cg.pushNewScope(getName, scope["__len__"])
            decs, exp = r
            for x in decs:
                # create a new scope
                x.genCode(scope, cg, getName)

            if isinstance(exp, list):
                for x in exp:
                    rtnName = x.genCode(scope, cg, getName)
            else:
                rtnName = exp.genCode(scope, cg, getName)

            cg.popScope(getName)

            cg.emitInst("; Expression -- Let ")

            return rtnName
        elif cls == "Constant":
            print("Constant: ", self)
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

            if r.isConsStr():
                n2 = getName()
                cg.emitInst("{} = bitcast i8** {} to i32*".format(n2, n1))
                n1 = n2

            cg.emitInst("; Expression -- Constant ")
            return n1
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
            print("Record Expression: ", self.record)
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

