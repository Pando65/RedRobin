# ------------------------------------------------------------
# YaccRedRobin.py
#
# David Delgadillo
# Omar Manjarrez
# ------------------------------------------------------------
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from LexRedRobin import tokens

aprobado = True

def p_program(p):
    'program : CLASS REDROBIN L_ABRE cuerpoprogram L_CIERRA'
    
def p_cuerpoprogram(p):
    'cuerpoprogram : codigo REDROBIN P_ABRE P_CIERRA L_ABRE cuerpofuncion L_CIERRA'
    
def p_codigo(p):
    '''codigo : clases codigo
              | funciones codigo
              | empty '''

#funciones deberia generar mas funciones
def p_funciones(p):
    'funciones : privilages valor_retorno ID P_ABRE parametros P_CIERRA L_ABRE cuerpofuncion L_CIERRA'

def p_valor_retorno(p):
    '''valor_retorno : tipovariable
                     | EMPTY'''

def p_privilages(p):
    '''privilages : SECRET
                  | PUBLIC'''
    print("olivermelapela")

def p_tipovariable(p):
    '''tipovariable : NUMBER
                    | REAL
                    | STRING
                    | BOOL
                    | ID'''

def p_parametros(p):
    '''parametros : tipovariable DOSPUNTOS ID mas_ids mas_parametros
                  | empty'''

def p_mas_ids(p):
    '''mas_ids : COMA ID mas_ids
               | empty'''

def p_mas_parametros(p):
    '''mas_parametros : PUNTOYCOMA tipovariable DOSPUNTOS ID mas_ids mas_parametros
                      | empty'''
    

def p_clases(p):
    'clases : CLASS ID herencia L_ABRE cuerpoclase L_CIERRA'
    
def p_herencia(p):
    '''herencia : INHERIT ID
                | empty'''

def p_cuerpoclase(p):
    '''cuerpoclase : privilages declaracion mas_cuerpoclase
                   | funciones mas_cuerpoclase'''

def p_mas_cuerpoclase(p):
    '''mas_cuerpoclase : cuerpoclase
                       | empty'''
                       

def p_cuerpofuncion(p):
    '''cuerpofuncion : declaracion cuerpofuncion
                     | asignacion cuerpofuncion
                     | condicional cuerpofuncion
                     | ciclo cuerpofuncion
                     | invocacion PUNTOYCOMA cuerpofuncion
                     | retorno cuerpofuncion
                     | empty'''

def p_retorno(p):
    'retorno : GIVE comparacion PUNTOYCOMA'

def p_invocacion(p):
    'invocacion : ID composicion_atributo P_ABRE argumentos P_CIERRA'

def p_argumentos(p):
    '''argumentos : valorargumentos mas_argumentos
                  | empty'''

def p_mas_argumentos(p):
    '''mas_argumentos : COMA valorargumentos mas_argumentos
                      | empty'''

def p_valorargumentos(p):
    '''valorargumentos : AMPERSAND ID composicion_atributo 
                       | comparacion'''

def p_composicion_atributo(p):
    '''composicion_atributo : PUNTO ID
                            | empty'''

def p_ciclo(p):
    '''ciclo : cicloestatico
             | ciclodinamico'''

def p_cicloestatico(p):
    'cicloestatico : FOR ID IN P_ABRE valor DOSPUNTOS valor P_CIERRA STEP valor L_ABRE cuerpofuncion L_CIERRA'

def p_ciclodinamico(p):
    'ciclodinamico : UNTIL P_ABRE comparacion P_CIERRA DO L_ABRE cuerpofuncion L_CIERRA'

def p_condicional(p):
    'condicional : IF P_ABRE comparacion P_CIERRA L_ABRE cuerpofuncion L_CIERRA condiciones_elif condicion_else'

def p_condiciones_elif(p):
    '''condiciones_elif : ELIF P_ABRE comparacion P_CIERRA L_ABRE cuerpofuncion L_CIERRA condiciones_elif
                        | empty'''

def p_condicion_else(p):
    '''condicion_else : ELSE L_ABRE cuerpofuncion L_CIERRA
                      | empty'''

def p_asignacion(p):
    'asignacion : ID composicion_atributo IGUAL comparacion PUNTOYCOMA'

def p_declaracion(p):
    'declaracion : tipovariable ID declara_arreglo iniciacion mas_declaraciones PUNTOYCOMA'

def p_declara_arreglo(p):
    '''declara_arreglo : B_ABRE valor B_CIERRA
                       | empty'''

def p_iniciacion(p):
    '''iniciacion : IGUAL comparacion
                  | empty'''

def p_mas_declaraciones(p):
    '''mas_declaraciones : COMA ID declara_arreglo iniciacion mas_declaraciones
                         | empty'''
    

#def p_expresion(p):
#    '''expresion : comparacion'''
                 

def p_comparacion(p):
    'comparacion : operando_comparacion mas_operadores'

def p_operando_comparacion(p):
    '''operando_comparacion : expresionaritmetica
                            | comparacion operadorrelacional comparacion
                            | negacion P_ABRE comparacion P_CIERRA'''

def p_negacion(p):
    '''negacion : NEGAR
                | empty'''
                
def p_mas_operadores(p):
    '''mas_operadores : AND comparacion
                      | OR comparacion
                      | empty'''

def p_operadorrelacional(p):
    '''operadorrelacional : MAYOR_IGUAL
                          | MENOR_IGUAL
                          | IGUAL_IGUAL
                          | DIFERENTE'''
                          

def p_expresionaritmetica(p):
    '''expresionaritmetica : valor mas_expresionesaritmeticas
                           | P_ABRE expresionaritmetica P_CIERRA mas_expresionesaritmeticas'''

def p_mas_expresionesaritmeticas(p):
    '''mas_expresionesaritmeticas : operadoresaritmeticos expresionaritmetica mas_expresionesaritmeticas
                                  | empty'''

def p_operadoresaritmeticos(p):
    '''operadoresaritmeticos : OPERADOR_SUMA
                             | OPERAODR_RESTA
                             | OPERADOR_MULTIPLICACION
                             | OPERADOR_DIVISION'''
    
def p_valor(p):
    '''valor : identificador
             | invocacion
             | CONST_STRING
             | CONST_BOOL
             | CONST_INTEGER
             | CONST_DOUBLE'''
             
def p_identificador(p):
    'identificador : ID atributo_o_arreglo'
    
def p_atributo_o_arreglo(p):
    '''atributo_o_arreglo : PUNTO ID
                          | B_ABRE valor B_CIERRA
                          | empty'''
                                                
def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    global aprobado
    aprobado = False
    print(p);
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

filename = "p2.txt"
file = open(filename, 'r')
s = ""
for line in file:
    s += line
parser.parse(s)

if aprobado == True:
    print("Aprobado")

