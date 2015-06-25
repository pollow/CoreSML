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
        print(header, file=self.file)

    def __del__(self):
        print(tail, file=self.file)

    def write(self, s):
        print(s, file=self.file)

    def emitGlobalStr(self, s):
        if not s in self.globalStr:
            self.globalStr.append(s)
            return "@string{}".format(len(self.globalStr))

    def enterMain(self):
        self.indent += 1


    def rtnMain(self, n1):
        self.emitInst("ret i32 {}".format(n1))
        self.write(main.format("\n".join(self.insts)))
        self.insts.clear()
        self.indent = 0

    def emitInst(self, s):
        self.insts.append("  " * self.indent + s)

    def getGlobalStrName(self, s):
        if s in self.globalStr:
            return "@string{}".format(self.globalStr.index(s)+1)
        else:
            return None

    def callFunc(self):
        pass

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

