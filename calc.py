import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS'
]

#regular expressions
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_ignore = r' \t'


#token functions
def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

def t_error(t):
    print('Illegal characters!')
    t.lexer.skip(1)

#Building the lexer
lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'), #low precedence
    ('left', 'MULTIPLY', 'DIVIDE'), #high precedence
)
# Parsing Rules
def p_calc(p):
    '''
    calc : expression
         | var_assign
         | empty
    '''
    print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''
    p[0]= ('=',p[1],p[3])
    
def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2],p[1],p[3]) #("+",10,("*",5,4))

def p_expression_int_float(p):
    '''
    expression : INT 
               | FLOAT
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var',p[1])

def p_error(p):
    print("Syntax error found!")

def p_empty(p):
    '''
    empty :
    '''
    p[0]= None

parser = yacc.yacc()
env = {}

def run(p): #proccesses AST
    global env
    if type(p)==tuple:
        if p[0]=='+':
            return run(p[1])+run(p[2])
        elif p[0]=='-':
            return run(p[1])-run(p[2])
        elif p[0]=='*':
            return run(p[1])*run(p[2])
        elif p[0]=='/':
            return run(p[1]) / run(p[2]) if run(p[2]) != 0 else "Error: Division by zero"
        elif p[0]=='=':
            env[p[1]]=run(p[2])
        elif p[0]=="var":
            if p[1] not in env:
                raise ValueError("Undeclared variable found!")
            else:
                return env[p[1]]
    else:
        return p

while True:
    try:
        s=input('calc> ')
    except EOFError: #CTRLD on keyboard
        break
    try:
        parser.parse(s)
    except ValueError as e:
        print(e)