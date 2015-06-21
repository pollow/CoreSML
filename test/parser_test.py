__author__ = 'Deus'

import unittest
from parser import parser
from ast import *
from typecheck import *

def desent(level, x):
    if type(x) == tuple:
        print("  " * level, end="")
        print(x)
        for y in x:
            if y:
                desent(level + 1, y)

    elif type(x) == list:
        for y in x:
            if y:
                desent(level + 1, y)

    elif type(x) in (TyCon, TypeExpression, Expression, Declaration, Value, typbind, valbind, datbind, Pattern, Constant, RecordItem, Unit, MRule, Match):
        print("  " * level, end="")
        # x.show()
        print(x)
        for y in x.dict.values():
            if y:
                desent(level + 1, y)
                # if type(x) in (list, tuple):
                #     print(x)
                #     for y in x:
                #         desent(level + 1, y)


if __name__ == "__main__":
    x = parser.parse(input())


class ParserTest(unittest.TestCase):
    def test_ast(self):
        x = parser.parse("val it : int = let val x : int = 10 val double : int -> int = fn x : int => x mul 2 in double x end")
        desent(0, x)
        self.assertEqual(True, True)

    def test_something(self):
        self.assertEqual(True, True)

    def test_typecheck(self):
        x = parser.parse("val it : int = let val x : int = 10 val double : int -> int = fn x : int => x mul 2 in double x end")
        typecheck(x)
        self.assertEqual(True, True)



if __name__ == '__main__':
    unittest.main()
