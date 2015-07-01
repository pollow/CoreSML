#!/usr/local/bin/python3
__author__ = 'Xing, Chang'

import sys
from parse import parser
from ast import *
from typecheck import *
from codegen import *

if __name__ == "__main__":
    f = open(sys.argv[1])
    src = f.read()
    x = parser.parse(src)
    env = typecheck(x)
    desent(0, x)
    codeGen(x, env, sys.argv[1].split(".")[0] + ".ll")

