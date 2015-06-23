__author__ = 'Xing, Chang'

from ast import *
from template import *


interface = ['printf']

primitive = ['+', '-', '*', '/', 'div', '#']

tf = "test.ll"


class CodeGenerator:
    'IR Language Generator'
    def __init__(self, file):
        self.file = open(file)
        self.globalStr = []
        self.indent = 0
        print(header, file=self.file)

    def __del__(self):
        print(tail, file=self.file)

    def write(self, s):
        print("    " * self.indent, s, file=self.file)

    def emitGloablStr(self, s):
        if not s in self.globalStr:
            self.globalStr.append(s)

    def getGlobalStrName(self, s):
        if s in self.globalStr:
            return "str{}".format(self.globalStr.index(s))
        else:
            return None

    def allocate(self, name, tyname, size):
        self.write("{} = alloca {}, align".format(name, tyname, size))

    def tempNameInc(x):
        c = [x]

        def fun():
            c[0] += 1
            # maybe should return str with prefix %
            return c[0]

        return fun



def codeGen(x):
    """
    :param x: Decleration
    :return:
    """
    print(header, file=tf)

    cg = CodeGenerator(tf)
    x.genCode(cg.tempNameInc(0), cg)

    print(tail, file=tf)

