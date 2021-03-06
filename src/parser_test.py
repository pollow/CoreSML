__author__ = 'Deus'

import unittest
from parse import parser
from ast import *
from typecheck import *
from codegen import *


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
                # if type(x) in (list, tuple):
                #     print(x)
                #     for y in x:
                #         desent(level + 1, y)


class ParserTest(unittest.TestCase):
    def test_ast(self):
        x = parser.parse(
            "val it : int = let val x : int = 10 val double : int -> int = fn x : int => x mul 2 in double x end")
        desent(0, x)
        self.assertEqual(True, True)

    def test_hello(self):
        x = parser.parse('val it : int = let val s : string = "Hello World!\n" in print s; 0 end')
        # desent(0, x)
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

    def test_tyinfer(self):
        x = 'val it = 0'
        print("Test: ", x)
        x = parser.parse(x)
        typecheck(x)
        desent(0, x)

        x = 'val it : int = let val {x = a, y = b} = {x = 1, y = 2.0} in 0 end'
        print("Test: ", x)
        x = parser.parse(x)
        typecheck(x)
        desent(0, x)

        x = 'val it = let val x = 1 val y = x in x end'
        print("Test: ", x)
        x = parser.parse(x)
        desent(0, x)

        x = 'val it = let val x : {1:int, 2:real, 3:string} = {1 = 1, 2 = 2.0, 3 = "abc"} in 0 end'
        print("Test: ", x)
        x = parser.parse(x)
        desent(0, x)

        x = 'val it = let val x = {1 = 1, 2 = 2.0, 3 = "abc"} in 0 end'
        print("Test: ", x)
        x = parser.parse(x)
        desent(0, x)

        x = 'val it = let ' \
            'val a = 10 ' \
            'val {x = x, y = {a = b, b = c}}  = {x = a, y = {a = 2, b = 3}} ' \
            'in c end'

        print("Test: ", x)
        x = parser.parse(x)
        typecheck(x)
        desent(0, x)
        self.assertEqual(True, True)

    def test_record_assign(self):
        x = 'val it : int = let val {x = a : int, y = b : real} = {x = 1, y = 2.0} in 0 end'
        print("Test: ", x)
        x = parser.parse(x)
        typecheck(x)
        desent(0, x)

        x = 'val it : int = let val x : {x : int, y : real} = {x = 1, y = 2.0} in 0 end'
        print("Test: ", x)
        x = parser.parse(x)
        # desent(0, x)
        typecheck(x)
        desent(0, x)

        x = 'val it : int = let ' \
            'val a : int = 10 ' \
            'val x : {x : int, y : real} = {x = a, y = 2.0}' \
            'in x; 0 end'

        print("Test: ", x)
        x = parser.parse(x)
        # desent(0, x)
        typecheck(x)
        desent(0, x)

        x = 'val it : int = let ' \
            'val a : int = 10 ' \
            'val x : {x : int, y : {a : int, b : int}} = {x = a, y = {a = 2, b = 3}} ' \
            'in x; 0 end'

        print("Test: ", x)
        x = parser.parse(x)
        # desent(0, x)
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
        # desent(0, x)
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
        # desent(0, x)
        typecheck(x)
        desent(0, x)
        self.assertEqual(True, True)

    def test_gen_hello(self):
        print("--------Code Generator Test----------")

        x = 'val it : int = \
        let val f : {1:int ,2:int} -> int = \
        fn {1=5 , 2=10} => 15 | \
        {1=x:int , 2=10} =>addi{1=x,2=10} | \
        {2=10,...} =>addi{1=5,2=20} | \
        _ => 100 \
        in print (intToStr (f {1=5,2=10}));0 end'

        print("Test: ", x)
        x = parser.parse(x)
        env = typecheck(x)
        print("-------------------*******------------------------*******---------------------")
        print(env)
        desent(0, x)
        # codeGen(x, env)
        self.assertEqual(True, True)
        print("--------Code Generator Test Finished----------")

        # print("--------Code Generator Test----------")
        # x = 'val it : int = let val x : int = 110 val s : string = "Hello World!\n" in x end'
        # print("Test: ", x)
        # x = parser.parse(x)
        # env = typecheck(x)
        # desent(0, x)
        # codeGen(x, env)
        # self.assertEqual(True, True)
        # print("--------Code Generator Test Finished----------")

        # print("--------Code Generator Test----------")
        # x = 'val it : int = let val x : int = 110 in let val q : int = 2 in x end end'
        # print("Test: ", x)
        # x = parser.parse(x)
        # env = typecheck(x)
        # desent(0, x)
        # codeGen(x, env)
        # self.assertEqual(True, True)
        # print("--------Code Generator Test Finished----------")

        # print("--------Code Generator Test----------")
        # x = 'val it : int = let val s : string = "Hello World\n" in ' \
        #     'print s; let val s : string = "Goodbye!\n" in print s end; 0 end'
        # print("Test: ", x)
        # x = parser.parse(x)
        # env = typecheck(x)
        # desent(0, x)
        # codeGen(x, env)
        # self.assertEqual(True, True)
        # print("--------Code Generator Test Finished----------")


        # print("--------Code Generator Test----------")
        # x = 'val it : int = let val {1 = x : int, 2 = y : int, ' \
        #     '3 = {1 = a : int, 2 = b : int} : {1 : int, 2 : int} } : ' \
        #     '{1:int, 2:int, 3: {1:int, 2:int}} = {1 = 3, 2 = 6, 3 = {1 = 10, 2 = 9} } in y end '
        # print("Test: ", x)
        # x = parser.parse(x)
        # env = typecheck(x)
        # desent(0, x)
        # codeGen(x, env)
        # self.assertEqual(True, True)
        # print("--------Code Generator Test Finished----------")

    def test_gen_std(self):
        print("--------Code Generator Test----------")
        x = 'val it : int = let val {x = x: real, y = y: int, z = z: string } = ' \
            '{x = 3.3, y = 10, z = "abcd\n"} in print (realToStr x); print (intToStr y); print z; 0 end'
        print("Test: ", x)
        x = parser.parse(x)
        env = typecheck(x)
        desent(0, x)
        codeGen(x, env)
        self.assertEqual(True, True)
        print("--------Code Generator Test Finished----------")


if __name__ == '__main__':
    unittest.main()
