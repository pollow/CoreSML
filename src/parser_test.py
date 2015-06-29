__author__ = 'Deus'

import unittest
from parse import parser
from ast import *
from typecheck import *
from codegen import *

import sys


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


#if __name__ == "__main__":
 #   x = parser.parse(input())


class ParserTest(unittest.TestCase):
    '''
    def test_ast(self):
        # x = parser.parse('val f : int->int = fn 0 => 0 | x : int => mul {1=x,2=mul{1=x, 2=2}}')
        # x = parser.parse('val it : int->int  = fn x : int => mul {1=x , 2 = mul{1=x, 2=2}}')
        # x = parser.parse('val add1 : {x:int , y:int}->int = fn {x=x:int, y=y:int} => add{1=x,2=y}')
        desent(0, x)
        self.assertEqual(True, True)

    def test_hello(self):
        x = parser.parse('val it : int = let val s : string = "Hello World!\n" in print s; 0 end')
        # desent(0, x)
        typecheck(x)
        desent(0, x)
        self.assertEqual(True, True)
'''
    def test_call_error(self):
        x = parser.parse('val it : int = let val s : string = "Hello World!\n" in print s; 0 end')
        # with self.assertRaises(SMLSyntaxError):
            # typecheck(x)
        # x=parser.parse('val it : int = let val {x = a : int, y = b : real} = {x = 1, y = 2.0} in 0 end')
        # x = parser.parse('val f : {x:real , y:string} -> int = fn {x = 7.0 , y = "hello"} => 17')
        # x = parser.parse('val add1 : {x:int , y:int}->int = fn {x=x:int, y=y:int} => add{1=x,2=y}')
        env=typecheck(x)
        print('**----------------------------------------------**')
        print(env)
        print('**----------------------------------------------**')

        desent(0, x)
        codeGen(x,env)
        # with self.assertRaises(SMLSyntaxError):
            # typecheck(x)
        self.assertEqual(True, True)
'''
    def test_record_assign(self):
        x = 'val it : int = let val {x = a : int, y = b : real} = {x = 1, y = 2.0} in 0 end'
        print("Test: ", x)
        x = parser.parse(x)
        # desent(0, x)
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
'''

if __name__ == '__main__':
    unittest.main()

