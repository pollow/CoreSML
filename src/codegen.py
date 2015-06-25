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

    def reserve(self, name, type):
        self.emitInst("{} = {} {} 0, 0")


    def rtnMain(self, n1):
        self.emitInst("ret i32 {}".format(n1))
        self.write(main.format("\n".join(self.insts)))
        self.insts.clear()
        self.indent = 0

    def emitInst(self, s):
        self.insts.append("    " * self.indent + s)

    def getGlobalStrName(self, s):
        if s in self.globalStr:
            return "@string{}".format(self.globalStr.index(s)+1)
        else:
            return None

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
    x.genCode(env, cg, CodeGenerator.tempNameInc(0), True)

    # print(tail, file=tf)

