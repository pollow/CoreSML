__author__ = 'Xing, Chang'

from ast import *
from template import *


interface = ['printf']

primitive = ['+', '-', '*', '/', 'div', '#']

def funType(tycon):
    assert isinstance(tycon, tuple)
    return "{} (i32*)*".format(IRTyName[tycon[1].name])

class CodeGenerator:
    'IR Language Generator'
    def __init__(self, file):
        self.file = open(file, "w")
        self.globalStr = []
        self.indent = 0
        self.insts = []
        self.insts_stack = []
        self.write(header)

    def __del__(self):

        def char(c):
            t = hex(ord(c))[2:]
            if len(t) == 1:
                t = '0' + t
            return '\\' + t.upper()

        # print all global str
        for x in zip(range(1, len(self.globalStr)+1), self.globalStr):
            self.write('@string{} = private unnamed_addr constant [{} x i8] c"{}", align 1'
                       .format(x[0], len(x[1]), "".join([ char(c) for c in x[1]])))
        self.write(tail)

    def write(self, s):
        print(s, file=self.file)

    def getGlobalStrName(self, s):
        if s in self.globalStr:
            return "@string{}".format(self.globalStr.index(s)+1)
        else:
            return None

    def emitGlobalStr(self, s):
        if not s in self.globalStr:
            self.globalStr.append(s)
            return "@string{}".format(len(self.globalStr))
        else:
            return self.getGlobalStrName(s)

    def enterMain(self, env, getName):
        # TODO init build in function
        zero = getName()
        self.indent += 2
        self.emitInst("{} = add i32 0, 0". format(zero))
        for x in env:
            if not x[:2] == "__" and env[x][0].tycon is not None and isinstance(env[x][0].tycon.type, tuple):
                r = self.createRecord(8, getName)
                self.fillRecord(zero, r[1], 0, getName, ptr=False)
                n1 = getName()
                self.emitInst("{} = ptrtoint {} {} to i32".format(n1, funType(env[x][0].tycon.type), "@"+x))
                self.fillRecord(n1, r[1], 4, getName, ptr=False)
                self.fillScope(r[0], env[x][1], getName)

        self.indent -= 1

    def rtnMain(self, n1):
        self.emitInst("ret i32 {}".format(n1))
        self.write(main.format("\n".join(self.insts)))
        self.insts.clear()
        self.indent = 0

    def emitInst(self, s):
        self.insts.append("    " * self.indent + s)


    def callFunc(self, fn, param, getName):
        # print("callFunc: ", fn, param)
        self.emitInst("; callFunc - Enter")
        if fn.type[1] == 'unit':
            self.emitInst("call {} @{} (i32* {})".format(IRTyName[fn.type[1]], fn.id, param))
            self.emitInst("; callFunc - Exit")
        else:
            rtn, n1 = getName(), getName()
            # TODO bitcast
            self.emitInst("{} = call {} @{} (i32* {})".format(rtn, IRTyName[fn.type[1]], fn.id, param))

            self.allocate(n1, "i32", 4)
            if fn.type[1] in ["record", "fn", "string"]:
                # TODO datatype
                n2 = self.ptrToInt(rtn, IRTyName[fn.type[1]], getName)
            else:
                n2 = getName()
                self.emitInst("{} = bitcast {} {} to i32".format(n2, IRTyName[fn.type[1]], rtn)) # tmp
            self.emitInst("store i32 {}, i32* {}, align 4".format(n2, n1))
            self.emitInst("; callFunc - Exit")
            return n1


    def extractVar(self, offset, levels, getName):
        # return a pointer
        s = getName()
        self.emitInst("{} = load i32** %scope, align 4".format(s))
        while levels:
            s1, s2 = getName(), getName()
            self.emitInst("{} = load i32* {}, align 4".format(s1, s))
            self.emitInst("{} = inttoptr i32 {} to i32*".format(s2, s1))
            s = s2
            levels -= 1
        n = getName()
        self.emitInst("{2} = getelementptr inbounds i32* {1}, i32 {0}".format(int(offset/4), s, n))

        self.emitInst("; extractVar")
        return n
        # TODO did not save to stack. Dangling pointer if freed.

    def fillScope(self, name, offset, getName,func=None):
        # name is a pointer
        n1, n2, n3 = getName(), getName(), getName()
        self.emitInst("{} = load i32** %scope, align 4".format(n1))
        self.emitInst("{} = getelementptr inbounds i32* {}, i32 {}".format(n2, n1, int(offset/4)))
        if func == None:
            self.emitInst("{} = load i32* {}, align 4".format(n3, name))
        else:
            self.emitInst("{} = ptrtoint i32* {} to i32".format(n3, n1))
        self.emitInst("store i32 {}, i32* {}, align 4".format(n3, n2))
        self.emitInst("; fillScope")


    def createParam(self, getName, fnEnv, param):
        n1, n2, n3, n4, n5, n6 = getName(), getName(), getName(), getName(), getName(), getName()
        self.emitInst("{} = call noalias i8* @malloc(i32 {}) nounwind".format(n1, 2 * 4))
        self.emitInst("{} = bitcast i8* {} to i32*".format(n2, n1)) # tmp
        self.emitInst("{} = getelementptr inbounds i32* {}, i32 {}".format(n3, n2, 0))
        self.emitInst("{} = load i32* {}, align 4".format(n4, fnEnv))
        self.emitInst("store i32 {}, i32* {}, align 4".format(n4, n3))
        self.emitInst("{} = getelementptr inbounds i32* {}, i32 {}".format(n5, n2, 1))
        self.emitInst("{} = load i32* {}, align 4".format(n6, param))
        self.emitInst("store i32 {}, i32* {}, align 4".format(n6, n5))

        self.emitInst("; createParam")
        return n2

    def fillRecord(self, name, record, offset, getName, ptr = True):
        # name is a pointer
        if ptr:
            n1 = getName()
            self.emitInst("{} = load i32* {}, align 4".format(n1, name))
        else:
            n1 = name

        n2 = getName()
        self.emitInst("{} = getelementptr inbounds i32* {}, i32 {}".format(n2, record, int(offset/4)))
        self.emitInst("store i32 {}, i32* {}, align 4".format(n1, n2))
        self.emitInst("; fillRecord")

    def extractRecord(self, record, offset, getName):
        # return a pointer
        n = getName()
        self.emitInst("{} = getelementptr inbounds i32* {}, i32 {}".format(n, record, int(offset/4)))
        self.emitInst("; extractRecord")
        return n

    def createRecord(self, size, getName):
        tmp = getName()
        self.allocate(tmp, "i32", 4)
        n1, n2, n3 = getName(), getName(), getName()
        self.emitInst("{} = call noalias i8* @malloc(i32 {}) nounwind".format(n1, size))
        self.emitInst("{} = bitcast i8* {} to i32*".format(n2, n1)) # tmp
        self.emitInst("{} = ptrtoint i32* {} to i32".format(n3, n2)) # tmp
        self.emitInst("store i32 {}, i32* {}, align 4".format(n3, tmp)) # scope = tmp
        self.emitInst("; createRecord")

        return (tmp, n2)

    def pushNewScope(self, getName, size):
        n1, n2, n3, n4 = getName(), getName(), getName(), getName()
        self.emitInst("{} = call noalias i8* @malloc(i32 {}) nounwind".format(n1, size * 4))
        self.emitInst("{} = bitcast i8* {} to i32*".format(n2, n1)) # tmp
        self.emitInst("{} = load i32** %scope, align 4".format(n3)) # scope
        self.emitInst("{} = ptrtoint i32* {} to i32".format(n4, n3)) # convert scope to value
        self.emitInst("store i32 {}, i32* {}, align 4".format(n4, n2)) # tmp[0] = scope
        self.emitInst("store i32* {}, i32** %scope, align 4".format(n2)) # scope = tmp

        self.emitInst("; pushNewScope")


    def popScope(self, getName):
        temp = "{0} = load i32** %scope, align 4\n" \
               "{1} = getelementptr inbounds i32* {0}, i32 0\n" \
               "{2} = load i32* {1}, align 4\n" \
               "{3} = inttoptr i32 {2} to i32*\n" \
               "store i32* {3}, i32** %scope, align 4".format(*[getName() for i in range(4)])

        for x in temp.split('\n'):
            self.emitInst(x)

        self.emitInst("; popScope")

    def intToPtr(self, name, getName):
        n = getName()
        self.emitInst("{} = inttoptr i32 {} to i32*".format(n, name))
        return n

    def ptrToInt(self, name, ty, getName):
        n = getName()
        self.emitInst("{} = ptrtoint {} {} to i32".format(n, ty,  name))
        return n

    def loadValue(self, name, getName):
        n = getName()
        self.emitInst("{} = load i32* {}, align 4".format(n, name))
        return n

    def allocate(self, name, tyname, size):
        self.emitInst("{} = alloca {}, align {}".format(name, tyname, size))

    def decFuncHead1(self):
        self.insts_stack.append((self.insts, self.indent))
        self.insts = []
        self.indent = 0
        getName=CodeGenerator.tempNameInc(0)
        self.emitInst("define i32 @f(i32* %p) {")
        self.emitInst("%scope = alloca i32*, align 4")
        self.emitInst("store i32* %p, i32** %scope, align 4")
        self.indent += 1
        return getName

    def decFuncHead2(self):
        getLabel=CodeGenerator.tempLabelInc(0)
        return getLabel

    def decFuncTail(self):
        # self.emitInst("call void %rtError(i8* getelementptr inbounds ([19 x i8]* @.str10, i32 0, i32 0))")
        self.emitInst("ret i32 0")
        self.indent -= 1
        self.emitInst("}")
        self.write("\n".join(self.insts)+"\n")
        self.insts, self.indent = self.insts_stack.pop()

    def MRuleRet(self,n,getName):
        n1=getName()
        self.emitInst("{}=load i32* {} ,align 4".format(n1,n))
        self.emitInst("ret i32 {}".format(n1))

    def getParamValue1(self,getName):
        n1,n2=getName(),getName()
        self.emitInst("{}= getelementptr inbounds i32** %scope, i32 {}".format(n1,1))
        self.emitInst("{}= bitcast i32** {} to i32*".format(n2,n1))
        return n2


    def getParamValue2(self,getName):
        n1,n2,n3=getName(),getName(),getName()
        self.emitInst("{}= getelementptr inbounds i32** %scope, i32 {}".format(n1,1))
        self.emitInst("{}=load i32** {}, align 4".format(n2,n1))
        self.emitInst("{}=ptrtoint i32* {} to i32".format(n3,n2))
        return n3


    def MRuleCompare(self,pat,param,getName,getLabel,FLabel=None,compound=None):
        if compound==None:
            n1=getName()
            self.emitInst("{}=icmp eq i32 {}, {}".format(n1,pat,param))
            return n1
        else: # compound is a dict
            r=0
            dic={}
            for i in range(len(pat)):
                if pat[i].lab!=None and pat[i].value!=None: #wildcard
                    dic[pat[i].lab]=i
            for element in compound:
                if element in dic:
                    n1,n2,n3=getName(),getName(),getName()
                    self.emitInst("{} = inttoptr i32 {} to i32*".format(n1,param))
                    self.emitInst("{} = getelementptr inbounds i32* {}, i32 {}".format(n2,n1,element))
                    self.emitInst("{} = load i32* {}, align 4".format(n3,n2))
                    x=pat[dic[element]].value.value
                    if isinstance(x,Value):#simple type:const,x,wildcard
                        if x.wildcard==True: #wildcard
                            pass
                        elif x.value!=None: #const
                            comp=self.MRuleCompare(x.value,n3,getName,getLabel)
                            l1=getLabel()
                            self.emitInst("br i1 {}, label %{}, label %{}".format(comp,l1,FLabel))
                            self.emitInst("{}:".format(l1))
                        else: #x
                            pass
                    else: #compound type
                        self.MRuleCompare(x,n3,getName,FLabel,compound[element])


    def MRuleBr1(self,comp,l1,l2):
        self.emitInst("br i1 {}, label %{}, label %{}".format(comp,l1,l2))
        self.emitInst("{}:".format(l1))

    def MRuleBr2(self,l2):
        self.emitInst("{}:".format(l2))

    @staticmethod
    def tempNameInc(x):
        c = [x]

        def fun():
            c[0] += 1
            # maybe should return str with prefix %
            return "%{}".format(c[0])

        return fun

    @staticmethod
    def tempLabelInc(x):
        c=[x]
        def fun():
            c[0]+=1
            return "L{}".format(c[0])
        return fun



def codeGen(x, env, tf = "test.ll"):

    """
    :param x: Decleration
    :return: 
    """

    cg = CodeGenerator(tf)
    x.genCode(env, cg, CodeGenerator.tempNameInc(4), True)

