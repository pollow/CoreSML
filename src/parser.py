from lexer import tokens
import ply.yacc as yacc

start = 'exp'

def p_cons(p):
    '''cons : INT_VAL
            | REAL_VAL
            | STRING_VAL
            | CHAR_VAL'''
    p[0] = p[1]
    print(type(p[1]), p[1], sep=" ")
    print(" CONS ")


def p_vid(p):
    ''' vid : SYMBOLIC
            | ALPHANUMERIC
    '''
    print(type(p[1]), p[1], sep=" ")
    print(" VID({0}) ".format(p[1]))
    p[0] = p[1]

#
# Types and Patterns
#

def p_tycon(p):
    ''' tycon : vid
    '''
    print(" TYCON ")
    p[0] = p[1]


def p_tyvar(p):
    ''' tyvar : "'" vid
    '''
    print(" TYVAR ")
    p[0] = "'" + p[2]


def p_lab(p):
    ''' lab : vid
            | INT_VAL
    '''
    try:
        p[0] = int(p[1])
    except ValueError:
        p[0] = p[1]

    print(" LAB ")


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
    print(" ATPAT ")



def p_patrow_seq(p):
    ''' patrow_seq   : lab '=' pat
                    | lab '=' pat ',' patrow_seq
    '''
    pass


def p_patrow(p):
    ''' patrow  : SUSPENSION
                | patrow_seq
    '''
    print(" PATROW ")
    pass

def p_pat(p):
    ''' pat : atpat
            | OP vid atpat
            | vid atpat
            | pat vid pat
            | pat ':' ty
    '''
    print(" PAT ")
    pass


def p_ty(p):
    ''' ty  : tyvar
            | '{' '}'
            | '{' tyrow '}'
            | tyseq tycon
            | ty POINT_TO ty
    '''
    print(" TY ")
    pass
# | '(' ty ')'


def p_tyrow(p):
    ''' tyrow   : lab ':' ty
                | lab ':' ty ',' tyrow
    '''
    print(" TYROW ")
    pass


def p_tyseq(p):
    ''' tyseq   : empty
                | ty
                | '(' tyseq_l ')'
    '''
    print(" TYSEQ ", len(p))
    pass


def p_tyseq_l(p):
    ''' tyseq_l : ty
                | ty ',' tyseq_l
    '''
    print(" TYSEQ_LIST ")
    pass


#
# Expressions and Declaration
#


def p_atexp(p):
    ''' atexp   : cons
                | OP vid
                | vid
                | '{' '}'
                | '{' exprow '}'
                | LET dec IN exp END
                | '(' exp ')'
    '''
    print(" ATEXP ")


def p_exprow(p):
    ''' exprow  : lab '=' exp
                | lab '=' exp ',' exprow
    '''
    print(" EXPROW ")


def p_exp(p):
    ''' exp : atexp
            | exp atexp
            | exp vid exp
            | exp ':' ty
            | FN match
    '''
    print(" EXP ")


def p_match(p):
    ''' match   : mrule
                | mrule '|' match
    '''
    print(" MATCH ")


def p_mrule(p):
    ''' mrule : pat LEAD_TO exp
    '''
    print(" MRULE ")
    pass


def p_dec(p):
    ''' dec : VAL tyvarseq valbind
            | TYPE typbind
            | DATATYPE datbind
            | dec ';' dec
            | dec dec
    '''
    print(" DEC ", p[1])


def p_valbind(p):
    ''' valbind : pat '=' exp
                | pat '=' exp AND valbind
                | REC valbind
    '''
    print(" VALBIND ")


def p_typbind(p):
    ''' typbind : tyvarseq tycon '=' ty
                | tyvarseq tycon '=' ty AND typbind
    '''
    print(" TYPBIND ")


def p_datbind(p):
    ''' datbind : tyvarseq tycon '=' conbind
                | tyvarseq tycon '=' conbind AND datbind
    '''
    print(" DATBIND ")


def p_conbind(p):
    ''' conbind : OP vid connext
                | OP vid OF ty connext
    '''
    print(" CONBIND ")


def p_connext(p):
    ''' connext : empty
                | '|' conbind
    '''
    print(" CONNEXT ")


def p_tyvarseq(p):
    ''' tyvarseq    : empty
                    | tyvarseq
                    | '(' tyvarseq_l ')'
    '''
    print(" TYVARSEQ ", len(p))


def p_tyvarseq_l(p):
    ''' tyvarseq_l  : tyvar
                    | tyvar ',' tyvarseq_l
    '''
    print(" TYVARSEQ_L ")


def p_empty(p):
    'empty : '
    print(" EMPTY ")
    pass


parser = yacc.yacc(debug=True)


