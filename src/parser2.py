from lexer import tokens
import ply.yacc as yacc

debug = 1
tree = 1

def p_program(p):
    '''program : program ';' exp 
                | program ';' dec
                | empty
                | exp
                | dec
    '''
    if debug==1:
        print('     PROGRAM')
    if tree == 1: 
        p[0]=['program']
        for i in range(1,len(p)):
            p[0].append(p[i])

# (*---------------------------------------------------------------*)
# (*                        expression                             *)
# (*---------------------------------------------------------------*)

def p_exp(p):
    ''' exp : atexp
            | exp SYMBOL exp
            | exp ANDALSO exp
            | exp ORELSE exp
            | exp atexp
            | exp ':' ty
            | FN match
            | CASE exp OF match
            | IF exp THEN exp ELSE exp
    '''
    if debug==1:
        print("exp")
    if tree == 1:
        p[0]=['exp']
        for i in range(1,len(p)):
            p[0].append(p[i])



def p_atexp(p):
    '''atexp : cons
            | vid
            | OP vid
            | '{' '}'
            | '{' exprow '}'
            | LET dec IN exp END
            | '(' expseq ')'
            | '[' expseq ']'
            | '[' ']'
    '''
    if debug==1:
        print('atexp')
    if tree == 1:
        p[0]=['atexp']
        for i in range(1,len(p)):
            p[0].append(p[i])

def p_expseq(p):
    '''expseq : exp
             | expseq ',' exp
    '''
    if debug==1:
        print('atexp')
    p[0]=['atexp']
    for i in range(1,len(p)):
        p[0].append(p[i])

def p_exprow(p):
    ''' exprow  : lab '=' exp
                | lab '=' exp ',' exprow
    '''
    if debug==1:
        print(" EXPROW ")
    p[0]=['exprow']
    for i in range(1,len(p)):
        p[0].append(p[i])


# (*---------------------------------------------------------------*)
# (*                        declaration                            *)
# (*---------------------------------------------------------------*)

def p_dec(p):
    ''' dec : VAL tyvarseq valbind
            | VAL valbind
            | FUN tyvarseq funbind
            | FUN funbind
            | TYPE typbind
            | DATATYPE datbind
    '''
    # p[0]=('dec',p[1],p[2])
    if debug==1:
        print("dec")
    p[0]=["dec"]
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_valbind(p):
    ''' valbind : pat '=' exp
                | pat '=' exp AND valbind
                | REC valbind
    '''
    if debug==1:
        print("valbind")
    p[0]=['valbind']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_datbind(p):
    '''datbind : tyvarseq tycon '=' conbind
                | tyvarseq tycon '=' conbind AND datbind
                | tycon '=' conbind 
                | tycon '=' conbind AND datbind
    '''
    if debug==1:
        print("datbind")
    p[0]=['datbind']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_conbind(p):
    ''' conbind : OP vid OF ty
                | vid OF ty
                | OP vid 
                | vid
                | OP vid OF ty '|' conbind
                | vid OF ty '|' conbind
                | OP vid '|' conbind
                | vid '|' conbind
    ''' 
    if debug==1:
        print("conbind")
    p[0]=['conbind']
    for i in range(1,len(p)):
        p[0].append(p[i])



def p_typbind(p):
    ''' typbind : tyvarseq tycon '=' ty
                | tyvarseq tycon '=' ty AND typbind
                | tycon '=' ty
                | tycon '=' ty AND typbind
    '''
    if debug==1:
        print("typbind")
    p[0]=['typbind']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_funbind(p):
    '''funbind : funmatch AND funbind
                | funmatch   
    '''
    if debug==1:
        print("funbind")
    p[0]=['funbind']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_funmatch(p):
    ''' funmatch : clause
                | clause '|' funmatch
    '''
    if debug==1:
        print("funmatch")
    p[0]=['funmatch']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_clause(p):
    '''clause : atpats '=' exp
            | atpats ':' ty '=' exp
    '''
    if debug==1:
        print("clause")
    p[0]=['clause']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_match(p):
    ''' match : pat LEAD_TO exp
              | pat LEAD_TO exp '|' match
    '''
    if debug==1:
        print("match")
    p[0]=['match']
    for i in range(1,len(p)):
        p[0].append(p[i])


# (*---------------------------------------------------------------*)
# (*                           type                                *)
# (*---------------------------------------------------------------*)

def p_ty(p):
    ''' ty  : ty POINT_TO ty
            | aty
            | ty '*' ty
    '''
    if debug==1:
        print("ty")
    p[0]=['ty']
    for i in range(1,len(p)):
        p[0].append(p[i])

def p_aty(p):
    '''aty : tyvar
            | '{' '}'
            | '{' tyrow '}'
            | aty tycon
            | '(' tyseq_l ')' tycon
            | tycon
            | '(' ty ')'
    '''
    if debug==1:
        print("aty")
    p[0]=['aty']
    for i in range(1,len(p)):
        p[0].append(p[i])


# def p_tyseq(p):
#     '''tyseq : aty
#             | '(' tyseq_l ')'
#     '''
#     if debug==1:
#         print("tyseq")
#     p[0]=['tyseq']
#     for i in range(1,len(p)):
#         p[0].append(p[i])


def p_tyseq_l(p):
    '''tyseq_l : ty ',' ty
            | tyseq_l ',' ty
    '''
    if debug==1:
        print("tyseq_l")
    p[0]=['tyseq_l']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_tyrow(p):
    ''' tyrow   : lab ':' ty
                | lab ':' ty ',' tyrow
    '''
    if debug==1:
        print(" tyrow ")
    p[0]=['tyrow']
    for i in range(1,len(p)):
        p[0].append(p[i])

def p_tycon(p):
    ''' tycon : vid
    '''
    if debug==1:
        print(" tycon ")
    p[0]=['tycon']
    for i in range(1,len(p)):
        p[0].append(p[i])

# def p_tytup(p):
#     '''tytup : ty
#              | tytup '*' ty
#     '''
#     print('tytup')

# (*---------------------------------------------------------------*)
# (*                             pattern                           *)
# (*---------------------------------------------------------------*)

def p_pat(p):
    ''' pat : atpat
            | OP vid atpat
            | pat SYMBOLIC pat
            | vid atpat
            | pat ':' ty
    '''
    if debug==1:
        print("pat")
    p[0]=['pat']
    for i in range(1,len(p)):
        p[0].append(p[i])

def p_atpats(p):
    '''atpats : atpat 
                | atpats atpat
    '''
    if debug==1:
        print("atpats")
    p[0]=['atpats']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_atpat(p):
    ''' atpat   : '_'
                | cons
                | vid
                | OP vid
                | '(' patseq ')'
                | '{' '}'
                | '{' patrow '}'
                | '[' ']'
                | '[' patseq ']'
    '''
    if debug==1:
        print("atpat")
    p[0]=['atpat']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_patseq(p):
    '''patseq : pat
            | patseq ',' pat
    '''
    if debug==1:
        print("patseq")
    p[0]=['patseq']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_patrow(p):
    ''' patrow  : SUSPENSION
                | lab '=' pat 
                | lab '=' pat ',' patrow
    '''
    if debug==1:
        print("patrow")
    p[0]=['patrow']
    for i in range(1,len(p)):
        p[0].append(p[i])



# (*---------------------------------------------------------------*)
# (*                           other                               *)
# (*---------------------------------------------------------------*)

def p_cons(p):
    '''cons : INT_VAL
            | REAL_VAL
            | STRING_VAL
            | CHAR_VAL'''
    # p[0]="CONS"
    if debug==1:
        print('cons')
    p[0]=['cons']
    for i in range(1,len(p)):
        p[0].append(p[i])


# def p_id(p):
#     '''id : ALPHANUMERIC
#          | SYMBOLIC
#     '''
#     p[0]=['id']
#     for i in range(1,len(p)):
#         p[0].append(p[i])


def p_vid(p):
    '''vid : ALPHANUMERIC
    '''
    if debug==1:
        print('vid')
    p[0]=['vid']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_lab(p):
    '''lab : ALPHANUMERIC
            | INT_VAL
    '''
    if debug==1:
        print('lab')
    p[0]=['lab']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_tyvar(p):
    ''' tyvar : "'" ALPHANUMERIC
    '''
    if debug==1:
        print("tyvar")
    p[0]=['tyvar']
    for i in range(1,len(p)):
        p[0].append(p[i])



def p_tyvarseq(p):
    ''' tyvarseq  :  tyvar
                | '(' tyvarseq_l ')'
    '''
    if debug==1:
        print("tyvarseq")
    p[0]=['tyvarseq']
    for i in range(1,len(p)):
        p[0].append(p[i])



def p_tyvarseq_l(p):
    ''' tyvarseq_l  : tyvar
                    | tyvar ',' tyvarseq_l
    '''
    if debug==1:
        print(" tyvarseq_l ")
    p[0]=['tyvarseq_l']
    for i in range(1,len(p)):
        p[0].append(p[i])



def p_SYMBOL(p):
    '''SYMBOL : '!' 
                | '%' 
                | '&' 
                | '$' 
                | '#' 
                | '+' 
                | '-' 
                | '/' 
                | '='
                | ':' 
                | '<' 
                | '>' 
                | '?' 
                | '@' 
                | '|' 
                | '~' 
                | '`' 
                | '^' 
                | '\' 
                | '*'
                | SYMBOLIC
    '''
    if debug==1:
        print(" symbol ")
    p[0]=['symbol']
    for i in range(1,len(p)):
        p[0].append(p[i])


def p_empty(p):
    'empty : '
    if debug==1:
        print(" EMPTY ")
    p[0]=['EMPTY']
    for i in range(1,len(p)):
        p[0].append(p[i])



# (*---------------------------------------------------------------*)
# (*                              end                              *)
# (*---------------------------------------------------------------*)


s= '''
fun f(xs:int)= 
    case xs of 
    1 => 1
    |2 => 2 
'''


def printTree(l,level=0):
    print('   '*level,l[0])
    for i in range(1,len(l)):
        if type(l[i])==type([]):
            printTree(l[i],level+1)
        else:
            print('   '*(level+1),l[i])

if __name__=='__main__':
    parser=yacc.yacc(debug=True)
    printTree(parser.parse(s))