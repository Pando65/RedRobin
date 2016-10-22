# ------------------------------------------------------------
# LexRedRobin.py
#
# David Delgadillo
# Omar Manjarrez
# ------------------------------------------------------------
import ply.lex as lex

tokens = [
    'L_ABRE',
    'L_CIERRA',
    'P_ABRE',
    'P_CIERRA',
    'ID',
    'DOSPUNTOS',
    'COMA',
    'PUNTOYCOMA',
    'AMPERSAND',
    'PUNTO',
    'GUIONBAJO',
    'IGUAL',
    'B_ABRE',
    'B_CIERRA',
    'MAYOR_IGUAL',
    'MENOR_IGUAL',
    'IGUAL_IGUAL',
    'DIFERENTE',
    'OPERADOR_SUMA',
    'OPERADOR_RESTA',
    'OPERADOR_MULTIPLICACION',
    'OPERADOR_DIVISION',
    'CONST_STRING',
    'CONST_INTEGER',
    'CONST_DOUBLE',
    'NEGAR'
]

reserved = {
    'class' : 'CLASS',
    'RedRobin' : 'REDROBIN',
    'public' : 'PUBLIC',
    'empty' : 'EMPTY',
    'secret' : 'SECRET',
    'number' : 'NUMBER',
    'real' : 'REAL',
    'string' : 'STRING',
    'bool' : 'BOOL',
    'inherit' : 'INHERIT',
    'give' : 'GIVE',
    'for' : 'FOR',
    'in' : 'IN',
    'step' : 'STEP',
    'while' : 'WHILE',
    'if' : 'IF',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'and' : 'AND',
    'or' : 'OR',
    'func' : 'FUNCTION',
    'true' : 'TRUE',
    'false' : 'FALSE'
}

t_L_ABRE = r'\{'
t_L_CIERRA = r'\}'
t_P_ABRE = r'\('
t_P_CIERRA = r'\)'
t_DOSPUNTOS = r'\:'
t_COMA = r'\,'
t_PUNTOYCOMA = r'\;'
t_AMPERSAND = r'\&'
t_PUNTO = r'\.'
t_GUIONBAJO = r'\_'
t_IGUAL = r'\='
t_B_ABRE = r'\['
t_B_CIERRA = r'\]'
t_MAYOR_IGUAL = r'\>\='
t_MENOR_IGUAL = r'\<\='
t_IGUAL_IGUAL = r'\=\='
t_DIFERENTE = r'\<\>'
t_OPERADOR_SUMA = r'\+'
t_OPERADOR_RESTA = r'\-'
t_OPERADOR_MULTIPLICACION = r'\*'
t_OPERADOR_DIVISION = r'\/'
t_CONST_STRING = r'\"[^ \"]*\"'
t_CONST_INTEGER = r'[0-9]+'
t_CONST_DOUBLE = r'[0-9]+\.[0-9]+'
t_NEGAR = r'\!'

def t_ID(t):
    r'[A-Z|a-z][A-Z|a-z|0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
  
tokens = tokens + list(reserved.values())

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer from my environment and return it    
lexer = lex.lex()