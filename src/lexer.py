# ------------------------------------------------------------
#  lexer.py
#
#  CoreSML
#
#  Created by Kael on 6/4/15.
#  Copyright (c) 2015 Xinyuan Lu. All rights reserved.
#
# Revisions:
# - rev 0.2 (2015-06-08)
#   Add SYMBOLIC support and literals for single character tokens.
# ------------------------------------------------------------

import unittest
import ply.lex as lex

reserved = {
    'and' : 'AND',
    'andalso' : 'ANDALSO',
    'as' : 'AS',
    'case' : 'CASE',
    'datatype' : 'DATATYPE',
    'do' : 'DO',
    'else' : 'ELSE',
    'end' : 'END',
    'fn' : 'FN',
    'fun' : 'FUN',
    'if' : 'IF',
    'in' : 'IN',
    'infix' : 'INFIX',
    'infixr' : 'INFIXR',
    'let' : 'LET',
    'local' : 'LOCAL',
    'nonfix' : 'NONFIX',
    'of' : 'OF',
    'op' : 'OP',
    'open' : 'OPEN',
    'orelse' : 'ORELSE',
    'rec' : 'REC',
    'then' : 'THEN',
    'type' : 'TYPE',
    'val' : 'VAL',
    'with' : 'WITH',
    'withtype' : 'WITHTYPE',
    'while' : 'WHILE',
    # 'int' : 'INT',
    # 'string' : 'STRING',
    # 'real' : 'REAL',
    'div' : 'DIV_INT',
    'use' : 'USE',
    'op' : 'OP',

    '=>'    : 'LEAD_TO',
    '->'    : 'POINT_TO',
}

tokens = [
    'SUSPENSION',

    'REAL_VAL',
    'INT_VAL',
    'STRING_VAL',
    'CHAR_VAL',
    'COMMENT',
    'SYMBOLIC',
    'ALPHANUMERIC',
    ] + list(reserved.values())

t_SUSPENSION = r'\.{3}'

literals = [ '(', ')', '[', ']', '{', '}', ',', ';', '_', ':', '|', '=', '#', \
             '+', '-', '/', '*', '@', '!', '$', '<', '>', '^', '~', '\'', "'"]

def t_ALPHANUMERIC(t):
    r'([a-zA-Z][\w\'_]*)|(\'[\w\'_]*)'
    t.type = reserved.get(t.value,'ALPHANUMERIC')
    return t


def t_SYMBOLIC(t):
    r'[\!\%\&\$\#\+\-\/\:\<\=\>\?\@\|\~\`\^\\\*]{2,}'
    t.type = reserved.get(t.value, 'SYMBOLIC')
    return t

# real (implemented by float)
def t_REAL_VAL(t):
    r'~?\d+((\.\d+)([eE]~?\d+)|(\.\d+)|([eE]~?\d+))'
    t.value = float(t.value)
    return t

# integer
def t_INT_VAL(t):
    r'~?(\d+)|(0x[0-9a-fA-F]+)'
    t.value = int(t.value)
    return t

# string
def t_STRING_VAL(t):
    r'\"[^"]*\"'
    t.value = t.value[1:-1]
    return t

# char
def t_CHAR_VAL(t):
    r'\#\"[^"]*\"'
    t.value = t.value[2:-1]
    return t

# comment
def t_COMMENT(t):
    # r'\(\*([^*)]|[^*]\)|\*[^)])*\*\)'
    r'\(\*([^*]|[\r\n]|(\*+([^*)]|[\r\n])))*\*+\)'
    # pass
    return t # for debug

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ignore
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

if __name__ == "__main__":
    # Test data
    data = ' val it : int = let val s s: string = "Hello World\n" in print s; 0 end $'
    # Give the lexer input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break

        print(tok)

    # todo: deal with trailing semiconlon
