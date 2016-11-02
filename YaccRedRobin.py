# ------------------------------------------------------------
# YaccRedRobin.py
#
# David Delgadillo
# Omar Manjarrez
# ------------------------------------------------------------
import ply.yacc as yacc
import sys
from SemanticsRedRobin import *

# Get the token map from the lexer.  This is required.
from LexRedRobin import tokens

aprobado = True

def p_program(p):
    'program : CLASS REDROBIN smnewprogram L_ABRE cuerpoprogram L_CIERRA'
    
def p_cuerpoprogram(p):
    'cuerpoprogram : codigo REDROBIN P_ABRE P_CIERRA L_ABRE smMainFound cuerpofuncion L_CIERRA'
    
def p_codigo(p):
    '''codigo : clases codigo
              | funciones codigo
              | empty '''

def p_funciones(p):
    'funciones : FUNCTION privilages valor_retorno ID smnewfunction P_ABRE parametros P_CIERRA L_ABRE cuerpofuncion L_CIERRA'
    setScopeFunction('')
    
def p_valor_retorno(p):
    '''valor_retorno : tipovariable
                     | EMPTY'''
    p[0] = p[1]

def p_privilages(p):
    '''privilages : SECRET
                  | PUBLIC'''
    p[0] = p[1]

def p_tipovariable(p):
    '''tipovariable : NUMBER
                    | REAL
                    | STRING
                    | BOOL
                    | ID'''
    p[0] = p[1]
    setCurrentType(p[1])

def p_parametros(p):
    '''parametros : tipovariable posiblesbrackets DOSPUNTOS ID smnewparam mas_ids mas_parametros
                  | empty'''
    
def p_mas_ids(p):
    '''mas_ids : COMA ID smnewparam mas_ids
               | empty'''

def p_mas_parametros(p):
    '''mas_parametros : PUNTOYCOMA parametros
                      | empty'''
    
def p_posiblesbrackets(p):
    '''posiblesbrackets : B_ABRE B_CIERRA
                        | empty'''

def p_clases(p):
    'clases : CLASS ID herencia smnewclass L_ABRE cuerpoclase L_CIERRA'
    setScopeClass("RedRobin")
    
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
                     | io PUNTOYCOMA cuerpofuncion
                     | retorno cuerpofuncion
                     | empty'''

def p_retorno(p):
    'retorno : GIVE expresion PUNTOYCOMA'

def p_invocacion(p):    #TODO --- Print y read NOOOOOOOOO deben ir dentro de la regla de invocacion porque invocacion es llamada por valor, print y read no arrojan valor!
    '''invocacion : ID composicion_atributo smNewInvocacion P_ABRE argumentos P_CIERRA smEndInvocacion
                  | TONUMBER P_ABRE argumentoPosible P_CIERRA
                  | TOREAL P_ABRE argumentoPosible P_CIERRA
                  | TOSTRING P_ABRE argumentoPosible P_CIERRA'''

def p_argumentos(p):
    '''argumentos : valorargumentos mas_argumentos
                  | empty'''

def p_mas_argumentos(p):
    '''mas_argumentos : COMA valorargumentos mas_argumentos
                      | empty'''

def p_valorargumentos(p):
    '''valorargumentos : AMPERSAND ID composicion_atributo
                       | expresion smParamExpresion'''
    #NOTA: no ocupe hacer un smParamID porque al usar un id ya lo estoy metiendo a la pila con validateIdSemantics(p[1]) en la regla p_identificador. Esto NO servira con los ampersand. TODO - considerar ampersands

def p_composicion_atributo(p):
    '''composicion_atributo : PUNTO ID
                            | empty'''
    #TODO -- Aceptar arreglos como atributo de objetos
    if p[1] == '.': # es composicion
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_io(p):
    '''io : PRINT P_ABRE argumentosPrint P_CIERRA
          | READ P_ABRE identificador smReadQuadruple P_CIERRA '''

def p_argumentosPrint(p):
    '''argumentosPrint : argumentoPosible smPrintQuadruple mas_prints
                       | empty'''

def p_mas_prints(p):
    '''mas_prints : COMA argumentoPosible smPrintQuadruple mas_prints
                  | empty'''

def p_argumentoPosible(p):
    '''argumentoPosible : expresion'''

def p_ciclo(p):
    '''ciclo : cicloestatico
             | ciclodinamico'''

def p_cicloestatico(p):
    'cicloestatico : FOR ID smforprepare IN P_ABRE valor smforinitialize GUIONBAJO smforstart valor smforcondition P_CIERRA STEP valor L_ABRE cuerpofuncion L_CIERRA smforend'

def p_ciclodinamico(p):
    'ciclodinamico : WHILE smwhilestart P_ABRE expresion smwhilecondition P_CIERRA L_ABRE cuerpofuncion L_CIERRA smendwhile'

def p_condicional(p):
    'condicional : IF P_ABRE expresion smnewif P_CIERRA L_ABRE cuerpofuncion L_CIERRA condiciones_elif condicion_else smendif'
    
def p_condiciones_elif(p):
    '''condiciones_elif : ELIF smnewelif smnewelse P_ABRE expresion smnewif P_CIERRA L_ABRE cuerpofuncion L_CIERRA condiciones_elif
                        | empty'''

def p_condicion_else(p):
    '''condicion_else : ELSE smnewelse L_ABRE cuerpofuncion L_CIERRA
                      | empty'''

def p_asignacion(p):
    'asignacion : identificador IGUAL expresion smAsignacion PUNTOYCOMA'

def p_declaracion(p):
    'declaracion : tipovariable ID smnewvariable declara_arreglo_o_iniciacion mas_declaraciones PUNTOYCOMA'    

def p_declara_arreglo_o_iniciacion(p):
    '''declara_arreglo_o_iniciacion : B_ABRE valor B_CIERRA
                                    | IGUAL expresion smAsignacion
                                    | empty'''

def p_mas_declaraciones(p):
    '''mas_declaraciones : COMA ID smnewvariable declara_arreglo_o_iniciacion mas_declaraciones
                         | empty'''

def p_expresion(p):
    'expresion : expresionii smcheckpendingors mas_expresion'

def p_mas_expresion(p):
    '''mas_expresion : OR smaddSingleOpe expresion
                   | empty'''

def p_expresionii(p):
    'expresionii : expresioniii smcheckpendingands mas_expresionii'

def p_mas_expresionii(p):
    '''mas_expresionii : AND smaddSingleOpe expresionii
                       | empty'''

def p_expresioniii(p):
    'expresioniii : expresioniv smcheckpendingrelational mas_expresioniii'

def p_mas_expresioniii(p):
    '''mas_expresioniii : operadorrelacional expresioniii
                        | empty'''

def p_expresioniv(p):
    'expresioniv : expresionv smcheckpendingterms mas_expresioniv'

def p_mas_expresioniv(p):
    '''mas_expresioniv : operadortermino expresioniv
                       | empty'''
    
def p_expresionv(p):
    'expresionv : expresionvi smcheckpendingfactors mas_expresionv'

def p_mas_expresionv(p):
    '''mas_expresionv : operadorfactor expresionv
                      | empty'''

def p_expresionvi(p):
    '''expresionvi : valor smCheckPendingNegatives
                   | negacion P_ABRE smaddSingleOpe expresion smRemoveParentesis P_CIERRA smCheckPendingNegatives'''

def p_negacion(p):
    '''negacion : NEGAR
                | OPERADOR_RESTA smNewNegativo
                | empty'''

# TODO - checar jerarquia de estos operadores, tambien tienen al parecer
def p_operadorrelacional(p):
    '''operadorrelacional : MAYOR_IGUAL
                          | MENOR_IGUAL
                          | IGUAL_IGUAL
                          | DIFERENTE'''
    pushToStackOpe(p[1])

def p_operadortermino(p):
    '''operadortermino : OPERADOR_SUMA
                       | OPERADOR_RESTA'''
    pushToStackOpe(p[1])

def p_operadorfactor(p):
    '''operadorfactor : OPERADOR_MULTIPLICACION
                      | OPERADOR_DIVISION'''
    pushToStackOpe(p[1])
    
def p_valor(p):
    '''valor : identificador
             | invocacion
             | CONST_STRING
             | valorbooleano
             | negativo CONST_INTEGER smnewcteint
             | negativo CONST_DOUBLE smnewctedouble'''

def p_valorbooleano(p):
    '''valorbooleano : TRUE
                     | FALSE'''
    newCteBool(p[1]);
    
def p_negativo(p):
    '''negativo : OPERADOR_RESTA smNewNegativo
                | empty'''
             
def p_identificador(p):
    'identificador : ID atributo arreglo'
    validateIdSemantics(p[1])

def p_atributo(p):
    '''atributo : PUNTO ID
                | empty'''
    
def p_arreglo(p):
    '''arreglo : B_ABRE valor B_CIERRA
               | empty'''
                                                
def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    global aprobado
    aprobado = False
    print(p)
    print("Syntax error in input!")
    sys.exit()

# Build the parser
parser = yacc.yacc()

filename = "p4.txt"
# filename = input("Ingresa nombre de archivo con lenguaje Red Robin: ") 
f = open(filename, 'r')
s = f.read()
parser.parse(s)


if aprobado == True:
    print("Aprobado")
    i = 0
    for cuadruplo in cuadruplos:
        print(str(i) + " - " + str(cuadruplo.ope) + " " + str(cuadruplo.op1) + " " + str(cuadruplo.op2) + " " + str(cuadruplo.r))
        i += 1
    print(dirProced)

