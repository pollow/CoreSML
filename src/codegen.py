__author__ = 'Xing, Chang'

from ast import *
from template import *


interface = ['printf']

primitive = ['+', '-', '*', '/', 'div', '#']

tf = "test.ll"


class CodeGenerator:
    'IR Language Generator'
    def __init__(self, file):
        self.file = open(file, "w")
        self.globalStr = []
        self.indent = 0
        self.insts = []
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

    def enterMain(self):
        self.indent += 1

    def rtnMain(self, n1):
        self.emitInst("ret i32 {}".format(n1))
        self.write(main.format("\n".join(self.insts)))
        self.insts.clear()
        self.indent = 0

    def emitInst(self, s):
        self.insts.append("  " * self.indent + s)


    def callFunc(self, fn, param, getName):
        print("callFunc: ", fn, param)
        if fn.type[1] == 'unit':
            self.emitInst("call {} @{} (i32* {})".format(IRTyName[fn.type[1]], fn.id, param))
            print("Call: call {} {} (i32* {})".format(IRTyName[fn.type[1]], fn.id, param))
        else:
            rtn = getName()
            self.emitInst("{} = call {} @{} (i32* {})".format(rtn, IRTyName[fn.type[1]], fn.id, param))
            print("Call: {} = call {} {} (i32* {})".format(rtn, IRTyName[fn.type[1]], fn.id, param))

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
        self.emitInst("{2} = getelementptr inbounds i32* {1}, i32 {0}".format(offset, s, n))

        self.emitInst("; extractVar")
        return n
        # TODO did not save to stack. Dangling pointer if freed.

    def fillScope(self, name, offset, getName):
        # name is a pointer
        n1, n2, n3 = getName(), getName(), getName()
        self.emitInst("{} = load i32* {}, align 4".format(n1, name))
        self.emitInst("{} = load i32** %scope, align 4".format(n2))
        self.emitInst("{} = getelementptr inbounds i32* {}, i32 {}".format(n3, n2, offset))
        self.emitInst("store i32 {}, i32* {}, align 4".format(n1, n3))
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

    def fillRecord(self, name, record, offset, getName):
        # name is a pointer
        n1, n2 = getName(), getName()
        self.emitInst("{} = load i32* {}, align 4".format(n1, name))
        self.emitInst("{} = getelementptr inbounds i32* {}, i32 {}".format(n2, record, offset))
        self.emitInst("store i32 {}, i32* {}, align 4".format(n1, n2))
        self.emitInst("; fillRecord")

    def extractRecord(self, record, offset, getName):
        # return a pointer
        n = getName()
        self.emitInst("{} = getelementptr inbounds i32* {}, i32 {}".format(n, record, int(offset/4)))
        self.emitInst("; extractRecord")
        return n

    def createRecord(self, size, getName):
        n1, n2 = getName(), getName()
        self.emitInst("{} = call noalias i8* @malloc(i32 {}) nounwind".format(n1, size))
        self.emitInst("{} = bitcast i8* {} to i32*".format(n2, n1)) # tmp
        self.emitInst("; createRecord")

        return n2

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


    def allocate(self, name, tyname, size):
        self.emitInst("{} = alloca {}, align {}".format(name, tyname, size))

    @staticmethod
    def tempNameInc(x):
        c = [x]

        def fun():
            c[0] += 1
            # maybe should return str with prefix %
            return "%{}".format(c[0])

        return fun



def codeGen(x, env):
    """
    :param x: Decleration
    :return:
    """
    # print(header, file=tf)

    cg = CodeGenerator(tf)
    x.genCode(env, cg, CodeGenerator.tempNameInc(4), True)

    # print(tail, file=tf)

