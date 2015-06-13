__author__ = 'Deus'

import unittest
from parser import parser


class ParserTest(unittest.TestCase):
    def test_cons(self):
        self.assertEqual(parser.parse("1"), 1)
        self.assertEqual(parser.parse("1.1"), 1.1)
        self.assertEqual(parser.parse('"asdf"'), "asdf")
        self.assertEqual(parser.parse('#"a"'), 'a')


    def test_something(self):
        self.assertEqual(True, True)



if __name__ == '__main__':
    unittest.main()
