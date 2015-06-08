# ------------------------------------------------------------
#  lex.py
#
#  CoreSML
#
#  Created by Kael on 6/4/15.
#  Copyright (c) 2015 Xinyuan Lu. All rights reserved.
#
# ------------------------------------------------------------

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
    'int' : 'INT',
    'string' : 'STRING',
    'real' : 'REAL',
    'div' : 'DIV_INT',
    'use' : 'USE',

    '...'   : 'SUSPENSION',
    '=>'    : 'LEADS_TO',
    '->'    :'POINTS_TO',

    ':'	: 'COLON',
    '_'	: 'UNDERLINE',
    '|'	: 'VERTICAL_BAR',
    '='	: 'EQUAL',
    '#'	: 'POUND_KEY',
}

tokens = [
    'PARENTHESES_L',
    'PARENTHESES_R',
    'BRACKET_L',
    'BRACKET_R',
    'BRACE_R',
    'BRACE_L',
    'COMMA',
    'SEMICOLON',
    'REAL_VAL',
    'INT_VAL',
    'STRING_VAL',
    'COMMENT',
    'SYMBOLIC',
    'ALPHANUMERIC',
    'ADD',
    'SUB',
    'DIV',
    'MUL',
    'AT',
    'EXCLAMATION',
    'DOLLAR',
    'LESS_THAN',
    'LARGER_THAN',
    'CONCATENATION',
    'TILDE',
    'PRIME',
    ] + list(reserved.values())

t_PARENTHESES_L = r'\('
t_PARENTHESES_R = r'\)'
t_BRACKET_L     = r'\['
t_BRACKET_R     = r'\]'
t_BRACE_R       = r'\{'
t_BRACE_L       = r'\}'
t_COMMA         = r','
t_SEMICOLON     = r';'
t_UNDERLINE     = r'\_'
# t_COLON         = r':'
# t_VERTICAL_BAR  = r'\|'
# t_EQUAL         = r'='
# t_POUND_KEY     = r'\#'

# t_SUSPENSION = r'\.\.\.'
# t_LEADS_TO = r'=>'
# t_POINTS_TO = r'->'


def t_ALPHANUMERIC(t):
    r'([a-zA-Z][\w\'_]*)|(\'[\w\'_]*)'
    t.type = reserved.get(t.value,'ALPHANUMERIC')
    return t


def t_SYMBOLIC(t):
    r'[\!\%\&\$\#\+\-\/\:\<\=\>\?\@\|\~\`\^\|\*]+'
    t.type = reserved.get(t.value, 'SYMBOLIC')
    return t


t_ADD=r'\+'
t_SUB=r'-'
t_DIV=r'/'
t_MUL=r'\*'
t_AT=r'\@'
t_EXCLAMATION=r'\!'
t_DOLLAR=r'\$'
t_LESS_THAN=r'\<'
t_LARGER_THAN=r'\>'
t_CONCATENATION=r'\^'
t_TILDE=r'\~'
t_PRIME=r'\''

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

# comment
# todo: conflicts with ignore
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
# todo: conflicts with t_COMMENT!!!!
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test data
data = r'''
1 + 2;
val a__' = "foo";
val b = (*here is a
 * )comm
 ent ) !*) 1.0;
val c = 1.0E5;
val d = 2e3;
c / d;
c div d;
let
    val a : int = 10;
in
    a * 19.0 div 2 / 3;
end

val str = "abc\u0000";

val ## = 1;
val x = fn x => x * 2;
val y = case ## of
  1=> 2
| 2 -> 3
| 3 -> (1,2,3)
end;
'''

# todo: symbolic

# Give the lexer input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break
    
    print(tok)

# todo: deal with trailing semiconlon
