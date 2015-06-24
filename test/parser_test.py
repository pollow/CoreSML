__author__ = 'Deus'

import unittest
from parser import parser
from ast import *
from typecheck import *

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

    elif type(x) in (TyCon, Expression, Declaration, Value, typbind, valbind, datbind, Pattern, RecordItem, Unit, MRule, Match):
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

    def test_hello(self):
        x = parser.parse('val it : int = let val s : string = "Hello World!\n" in print s; 0 end')
        desent(0, x)
        typecheck(x)
        desent(0, x)
        self.assertEqual(True, True)

    def test_call_error(self):
        x = parser.parse('val it : int = let val s : string = "Hello World!\n" in print 1; 0 end')
        with self.assertRaises(SMLSyntaxError):
            typecheck(x)
        x = parser.parse('val it : int = let val a : int = 1.0 val s : string = "Hello World!\n" in print s; 0 end')
        with self.assertRaises(SMLSyntaxError):
            typecheck(x)
        self.assertEqual(True, True)

    def test_record_assign(self):
        x = 'val {x = a : int, y = b : real} = {x = 1, y = 2.0}'
        print("Test: ", x)
        x = parser.parse(x)
        desent(0, x)
        typecheck(x)
        desent(0, x)

        x = 'val x : {x : int, y : real} = {x = 1, y = 2.0}'
        print("Test: ", x)
        x = parser.parse(x)
        desent(0, x)
        typecheck(x)
        desent(0, x)

        x = 'val it : int = let ' \
            'val a : int = 10' \
            'val x : {x : int, y : real} = {x = a, y = 2.0}' \
            'in x; 0 end'

        print("Test: ", x)
        x = parser.parse(x)
        desent(0, x)
        typecheck(x)
        desent(0, x)

        x = 'val it : int = let ' \
            'val a : int = 10' \
            'val x : {x : int, y : {a : int, b : int}} = {x = a, y = {a = 2, b = 3}} ' \
            'in x; 0 end'

        print("Test: ", x)
        x = parser.parse(x)
        desent(0, x)
        typecheck(x)
        desent(0, x)
        self.assertEqual(True, True)

    def test_fn(self):
        x = "val it : int = " \
            "let " \
            "val x : int = 10 " \
            "val double : int -> int = fn x : int => mul { 1 = x, 2 = 2 } " \
            "in double x end"
        print("Test: ", x)
        x = parser.parse(x)
        desent(0, x)
        typecheck(x)
        desent(0, x)

        x = "val it : int = " \
            "let " \
            "val x : int = 10 " \
            "val sum: {1 : int, 2 : int, 3: int} -> int = " \
            "fn {1 = x : int, 2 = y : int, 3 = z : int} : int => " \
            "add { 1 = add { 1 = x, 2 = y} , 2 = z} " \
            "in sum {1=x, 2=x, 3=x} end"
        print("Test: ", x)
        x = parser.parse(x)
        desent(0, x)
        typecheck(x)
        desent(0, x)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

