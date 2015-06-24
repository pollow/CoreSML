from lexer import tokens
import ply.yacc as yacc
from ast import *

start = 'dec'

debug = 1


def p_program(p):
    '''program  : program ';' exp 
                | program ';' dec
                | exp
                | dec
    '''
    if debug==1:
        print('     PROGRAM')

    if len(p) == 2:
        p[0] = [ p[1] ]
    else:
        p[0] = p[1] + [ p[3] ]


def p_cons_int(p):
    'cons : INT_VAL'
    print("int : ", p[1])
    p[0] = Value(value=p[1], tycon=int_type)


def p_cons_real(p):
    'cons : REAL_VAL'
    print("real : ", p[1])
    p[0] = Value(value=p[1], tycon=real_type)


def p_cons_str(p):
    'cons : STRING_VAL'
    print("string : ", p[1])
    p[0] = Value(value=p[1], tycon=string_type)


def p_cons_char(p):
    'cons : CHAR_VAL'
    print("char : ", p[1])
    p[0] = Value(value=p[1], tycon=char_type)


def p_vid(p):
    ''' vid : symbol
            | ALPHANUMERIC
    '''
    print(" VID : ", p[1])
    p[0] = p[1]


def p_tycon(p):
    ''' tycon : vid
    '''
    print(" TYCON : ", p[1])
    p[0] = p[1]


def p_tyvar(p):
    ''' tyvar : "'" vid
    '''
    p[0] = "'" + p[2]
    print(" TYVAR : ", p[0])


def p_lab(p):
    ''' lab : vid
            | INT_VAL
    '''
    try:
        p[0] = int(p[1])
    except ValueError:
        p[0] = p[1]

    print(" LAB : ", p[0])


# (*---------------------------------------------------------------*)
# (*                             Pattern                           *)
# (*---------------------------------------------------------------*)


# atomic pattern
def p_atpat_wc(p):
    """atpat    : '_'
                | cons """
    if p[1] == '_':
        p[0] = Pattern(Value(wildcard=True))
    else:
        p[0] = Pattern(p[1])


def p_atpat_id(p):
    """atpat    : vid
                | OP vid"""
    if len(p) == 2:
        p[0] = Pattern(Value(id=p[1]))
    else:
        p[0] = Pattern(Value(id=p[2], op=True))


def p_atpat_r(p):
    """atpat    : '{' '}'
                | '{' patrow '}' """
    if len(p) == 3:
        p[0] = Pattern(Unit())
    else:
        p[0] = Pattern( p[2] )


def p_atpat(p):
    " atpat   : '(' pat ')' "
    p[0] = p[2]


def p_patrow_seq(p):
    ''' patrow_seq  : lab '=' pat
                    | lab '=' pat ',' patrow
    '''
    if len(p) == 4:
        p[0] = [ RecordItem(lab=p[1], value=p[3]) ]
    else:
        p[0] = [ RecordItem(lab=p[1], value=p[3]) ] + p[5]


def p_patrow(p):
    ''' patrow  : SUSPENSION
                | patrow_seq
    '''
    if p[1] == "...":
        p[0] = [RecordItem(None, None)]
    else:
        p[0] = p[1]


def p_pat(p):
    ''' pat : atpat
            | OP vid atpat
            | vid atpat
            | pat vid pat
            | pat ':' ty
    '''
    print(" PAT ")
    if len(p) == 2: # atpat
        p[0] = p[1]
    elif p[1] == "op": # op vid atpat
        p[0] = Pattern(Value(vcon=p[2], value=p[3].value, op=True))
    elif len(p) == 3: # vid atpat
        p[0] = Pattern(Value(vcon=p[1], value=p[2].value)) # or p[2].value with vcon = p[1]?
    elif p[2] == ':': # pat : ty
        p[1].value.tycon = p[3]
        p[1].value.update()
        p[0] = Pattern(p[1].value)
    else: # pat vid pat TODO
        p[0] = Pattern( Value(
                value=Value(
                    value=[RecordItem(1, p[1].value), RecordItem(2, p[3].value)],
                    tycon=TyCon(name="record")),
                vcon=p[2]))


# (*---------------------------------------------------------------*)
# (*                           type                                *)
# (*---------------------------------------------------------------*)


def p_ty(p):
    ''' ty  : aty
            | ty POINT_TO ty
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = TyCon([], None, 0, (p[1], p[3]))

def p_aty_con(p):
    ''' aty : tycon
            | aty tycon
            | '(' tyseq_l ')' tycon
    '''
    if len(p) == 2:
        if p[1] in primative_tycon:
            p[0] = primative_tycon[p[1]]
        else:
            p[0] = TyCon(tyvar = [], name = p[1])
    elif len(p) == 3:
        p[0] = TyCon([p[1]], p[2], 1)
    else:
        p[0] = TyCon(p[3], p[3], len(p[2]))


def p_aty(p):
    ''' aty : tyvar
            | '(' ty ')'
            | '{' '}'
            | '{' tyrow '}'
    '''
    print(" TY ")
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]
    elif p[1] == '{':
        if len(p) == 3:
            p[0] = unit_type
        else:
            p[0] = p[2]


def p_tyrow(p):
    ''' tyrow   : lab ':' ty
                | lab ':' ty ',' tyrow
    '''
    print(" TYROW : ", len(p))
    if len(p) == 4:
        p[0] = TyCon(type={p[1] : p[3]}, name='record')
    else:
        p[0] = p[5]
        p[0].type[p[1]] = p[3]


def p_tyseq_l(p):
    ''' tyseq_l : ty ',' ty
                | ty ',' tyseq_l
    '''
    print(" TYSEQ_LIST ")
    p[0] = [ p[1] ] + (p[3] if type(p[3]) == list else [ p[3] ])


# (*---------------------------------------------------------------*)
# (*                        expression                             *)
# (*---------------------------------------------------------------*)


def p_atexp_c(p):
    ' atexp   : cons '
    p[0] = Expression( "Constant", p[1] )


def p_atexp_r(p):
    ''' atexp   : '{' '}'
                | '{' exprow '}' '''

    if len(p) == 3:
        p[0] = Expression( "Record", [RecordItem(None, None)] )
    else:
        p[0] = Expression( "Record", p[2] )


def p_atexp(p):
    ''' atexp   : vid
                | OP vid
                | LET decs IN exp END
                | LET decs IN exps END
                | '(' exp ')'
    '''
    if len(p) == 2:
        p[0] = Expression( "App", Value(id=p[1]) )
    elif len(p) == 3:
        p[0] = Expression( "App", Value(id=p[2], op=True) )
    elif len(p) == 6:
        p[0] = Expression( "Let", ( p[2], p[4] ) )
    else:
        p[0] = p[2]


def p_exprow(p):
    ''' exprow  : lab '=' exp
                | lab '=' exp ',' exprow
    '''
    print(" EXPROW ")
    if len(p) == 4:
        p[0] = [ RecordItem(p[1], p[3]) ]
    else:
        p[0] = [ RecordItem(p[1], p[3]) ] + p[5]


def p_exps(p):
    ''' exps    : exp ';' exp
    '''
    p[0] = [p[1], p[3]]


def p_exps_(p):
    ''' exps    : exp ';' exps
    '''
    p[0] = [p[1]] + p[3]


def p_exp(p):
    ''' exp : app_exp
            | exp ':' ty
            | exp ANDALSO exp
            | exp ORELSE exp
            | CASE exp OF match
            | IF exp THEN exp ELSE exp
            | FN match
    '''
    print(" EXP ")
    if len(p) == 2:
        if len(p[1]) == 1:
            p[0] = p[1][0]
        else:
            p[0] = Expression( "App", p[1] )
    elif len(p) == 3:
        p[0] = Expression( "Fn", p[2] )
    elif p[2] == ':':
        p[0] = Expression( "Constraint", ( p[1], p[3] ) )
    elif p[2] == "andalso":
        p[0] = Expression( "Andalso", (p[1], p[3]) )
    elif p[2] == "orelse":
        p[0] = Expression( "Orelse", (p[1], p[3]) )
    elif len(p) == 5:
        p[0] = Expression( "Case",  (p[2], p[4]) )
    elif len(p) == 5:
        p[0] = Expression( "If",  (p[2], p[4], p[6]) )


def p_app_exp(p):
    ''' app_exp : atexp app_exp1
    '''
    # | vid app_exp1
    p[0] = [ p[1] ] + p[2]


def p_app_exp1(p):
    ''' app_exp1    : empty
                    | app_exp
    '''
    p[0] = p[1]


# (*---------------------------------------------------------------*)
# (*                        declaration                            *)
# (*---------------------------------------------------------------*)


def p_match(p):
    ''' match   : mrule
                | mrule '|' match
    '''
    print(" MATCH ")
    if len(p) == 2:
        p[0] = [ p[1] ]
    else:
        p[0] = [ p[1] ] + p[3]


def p_mrule(p):
    ''' mrule : pat LEAD_TO exp
    '''
    print(" MRULE ")
    p[0] = (p[1], p[3])


def p_decs(p):
    ''' decs    : empty
                | dec decs
                | dec ';' decs
    '''
    print(" DECS ")
    if len(p) == 2:
        p[0] = []
    elif len(p) == 3:
        p[0] = [ p[1] ] + p[2]
    else:
        p[0] = [ p[1] ] + p[3]


def p_dec(p):
    ''' dec : VAL valbind
            | TYPE typbind
            | DATATYPE datbind
    '''
    print(" DEC ", p[1])
    if  p[1] == "val":
            p[0] = Declaration(p[1], p[2])
    elif p[1] == "type":
        p[0] = Declaration(p[1], p[2])
    else:
        p[0] = Declaration(p[1], p[2])


def p_valbind(p):
    ''' valbind : pat '=' exp
                | REC fvalbind
    '''
    print(" VALBIND ")
    if len(p) == 3:
        p[0] = p[2]
        p[0].rec = True
    elif len(p) == 4:
        p[0] = valbind(p[1], p[3])


def p_fvalbind(p):
    ''' fvalbind    : pat '=' FN match
    '''
    p[0] = (p[1], p[3])


def p_typbind(p):
    ''' typbind : tyvarseq tycon '=' ty
                | tycon '=' ty
    '''
    print(" TYPBIND ")
    if len(p) == 4:
        p[0] = typbind([], p[1], p[3])
    elif len(p) == 5:
        p[0] = typbind(p[1], p[2], p[4])


def p_datbind(p):
    ''' datbind : tyvarseq tycon '=' conbind
                | tycon '=' conbind
    '''
    print(" DATBIND ")
    if len(p) == 4:
        p[0] = [ datbind([], p[1], p[3]) ]
    elif len(p) == 5:
        p[0] = [ datbind(p[1], p[2], p[4]) ]


def p_conbind(p):
    ''' conbind : vid connext
                | vid OF ty connext
    '''
    print(" CONBIND ")
    if len(p) == 3:
        p[0] = [ (Value(id = p[1], op=False), unit_type) ] + p[2]
    else:
        p[0] = [ (Value(id = p[1], op=False), p[3]) ] + p[4]


def p_conbind_op(p):
    ''' conbind : OP vid connext
                | OP vid OF ty connext
    '''
    print(" CONBIND ")
    if len(p) == 4:
        p[0] = [ (Value(id = p[1], op=True), unit_type) ] + p[2]
    else:
        p[0] = [ (Value(id = p[1], op=True), p[3]) ] + p[4]


def p_connext(p):
    ''' connext : empty
                | '|' conbind
    '''
    print(" CONNEXT ")
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# (*---------------------------------------------------------------*)
# (*                           type                                *)
# (*---------------------------------------------------------------*)


def p_tyvarseq(p):
    ''' tyvarseq    : tyvar
                    | '(' tyvarseq_l ')'
    '''
    print(" TYVARSEQ ", len(p))
    if len(p) == 2:
        p[0] = [ p[1] ]
    else:
        p[0] =  p[2]


def p_tyvarseq_l(p):
    ''' tyvarseq_l  : tyvar
                    | tyvar ',' tyvarseq_l
    '''
    print(" TYVARSEQ_L ")
    if len(p) == 2:
        p[0] = [ p[1] ]
    else:
        p[0] = [ p[1] ] + p[3]


def p_empty(p):
    'empty : '
    print(" EMPTY ")
    p[0] = []


def p_symbol(p):
    '''symbol :  SYMBOLIC
            | '+'
            | '-'
            | '*'
            | '/'
            | '^'
            | '#'
    '''
    print(' symbol ')


parser = yacc.yacc(debug=True)

