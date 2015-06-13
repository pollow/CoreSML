from lexer import tokens
import ply.yacc as yacc

start = 'pat'

def p_cons(p):
    '''cons : INT_VAL
            | REAL_VAL
            | STRING_VAL
            | CHAR_VAL'''
    p[0] = p[1]


def p_vid(p):
    ''' vid : SYMBOLIC
            | ALPHANUMERIC
    '''
    p[0] = p[1]


def p_tyvar(p):
    ''' tyvar : "'" vid
    '''
    p[0] = "'" + p[2]


def p_lab(p):
    ''' lab : id
            | INT_VAL
    '''
    p[0] = p[1]


# atomic pattern
def p_atpat(p):
    ''' atpat   : '_'
                | cons
                | vid
                | OP vid
                | '{' '}'
                | '{' patrow '}'
                | '(' pat ')'
    '''
    pass


def p_patrow(p):
    ''' patrow  : SUSPENSION
                | patrow_seq
    '''
    pass


def p_patrowseq(p):
    ''' patrowseq   : lab '=' pat
                    | lab '=' pat ',' patrowseq
    '''
    pass


def p_pat(p):
    ''' pat : atpat
            | op vid atpat
            | vid atpat
            | pat vid pat
            | pat : ty
    '''
    pass


def p_ty(p):
    ''' ty  : tyvar
            | '{' '}'
            | '{' tyrow '}'
            | tyseq tycon
            | ty POINT_TO ty
            | '(' ty ')'
    '''
    pass


def p_tyrow(p):
    ''' tyrow   : lab ':' ty
                | lab ':' ty ',' tyrow
    '''
    pass


def p_tyseq(p):
    ''' tyseq   : empty
                | ty
                | '(' tyseq_l ')'
    '''
    pass


def p_tyseq_l(p):
    ''' tyseq_l : ty
                | ty ',' tyseq_l
    '''
    pass


def p_empty(p):
    'empty : '
    pass


parser = yacc.yacc(debug=True)

