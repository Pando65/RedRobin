# ------------------------------------------------------------
# YaccRedRobin.py
#
# David Delgadillo
# Omar Manjarrez
# ------------------------------------------------------------
import ply.yacc as yacc
import sys
from Cubo import *
from Cuadruplo import *

# Get the token map from the lexer.  This is required.
from LexRedRobin import tokens

# Procedures directory
dirProced = {}
currentType = ''
currentScopeClass = 'RedRobin'
currentScopeFunction = ''

# direccion virtuales
virtualTable = {}
mapCteToDir = {}
memConts = numpy.zeros(16)
memConts[memCont['numberClass']] = memStart['numberClass']
memConts[memCont['realClass']] =   memStart['realClass']
memConts[memCont['stringClass']] = memStart['stringClass']
memConts[memCont['boolClass']] =   memStart['boolClass']

memConts[memCont['numberFunc']] = memStart['numberFunc']
memConts[memCont['realFunc']] =   memStart['realFunc']
memConts[memCont['stringFunc']] = memStart['stringFunc']
memConts[memCont['boolFunc']] =   memStart['boolFunc']

memConts[memCont['numberTemp']] = memStart['numberTemp']
memConts[memCont['realTemp']] =   memStart['realTemp']
memConts[memCont['stringTemp']] = memStart['stringTemp']
memConts[memCont['boolTemp']] =   memStart['boolTemp']

memConts[memCont['numberCte']] = memStart['numberCte']
memConts[memCont['realCte']] =   memStart['realCte']
memConts[memCont['stringCte']] = memStart['stringCte']
memConts[memCont['boolCte']] =   memStart['boolCte']

def getType(memAddress):
    if memAddress <= memLimit['numberClass']:
        return 'number'
    if memAddress <= memLimit['realClass']:
        return 'real'
    if memAddress <= memLimit['stringClass']:
        return 'string'
    if memAddress <= memLimit['boolClass']:
        return 'bool'
    
    if memAddress <= memLimit['numberFunc']:
        return 'number'
    if memAddress <= memLimit['realFunc']:
        return 'real'
    if memAddress <= memLimit['stringFunc']:
        return 'string'
    if memAddress <= memLimit['boolFunc']:
        return 'bool'
    
    if memAddress <= memLimit['numberTemp']:
        return 'number'
    if memAddress <= memLimit['realTemp']:
        return 'real'
    if memAddress <= memLimit['stringTemp']:
        return 'string'
    if memAddress <= memLimit['boolTemp']:
        return 'bool'
    
    if memAddress <= memLimit['numberCte']:
        return 'number'
    if memAddress <= memLimit['realCte']:
        return 'real'
    if memAddress <= memLimit['stringCte']:
        return 'string'
    if memAddress <= memLimit['boolCte']:
        return 'bool'

# generacion de cuadruplos
stackOpe = []
stackDirMem = []
cubo = Cubo()
cuadruplos = []

aprobado = True

def p_program(p):
    'program : CLASS REDROBIN newprogram L_ABRE cuerpoprogram L_CIERRA'
    
def p_newprogram(p):
    'newprogram : '
    global dirProced
    dirProced['RedRobin'] = {'func': {}, 'vars': {}}
    
    
def p_cuerpoprogram(p):
    'cuerpoprogram : codigo REDROBIN P_ABRE P_CIERRA L_ABRE cuerpofuncion L_CIERRA'
    
def p_codigo(p):
    '''codigo : clases codigo
              | funciones codigo
              | empty '''

def p_funciones(p):
    'funciones : FUNCTION privilages valor_retorno ID newfunction P_ABRE parametros P_CIERRA L_ABRE cuerpofuncion L_CIERRA'
    global currentScopeFunction
    currentScopeFunction = ''
    
def p_newfunction(p):
    'newfunction : '
    # nueva funcion encontrada
    global dirProced
    global currentScopeClass
    global currentScopeFunction
    newScopeFunction = p[-1]
    # TODO - encontrar el tipo de la funcion, hardcodeado con empty
    if newScopeFunction in dirProced[currentScopeClass]['func']:
        print("FUNCION YA DECLARADA")
        global aprobado
        aprobado = False
    else:
        dirProced[currentScopeClass]['func'][newScopeFunction] = {'vars': {}, 'giveType': 'empty', 'params': {}}
        currentScopeFunction = newScopeFunction

def p_valor_retorno(p):
    '''valor_retorno : tipovariable
                     | EMPTY'''

def p_privilages(p):
    '''privilages : SECRET
                  | PUBLIC'''

def p_tipovariable(p):
    '''tipovariable : NUMBER
                    | REAL
                    | STRING
                    | BOOL
                    | ID'''
    global currentType
    currentType = p[1]

# nuevo parametro, solo el primero MARCA
def p_parametros(p):
    '''parametros : tipovariable posiblesbrackets DOSPUNTOS ID paramFound mas_ids mas_parametros
                  | empty'''
    
def p_paramFound(p):
    'paramFound :'
    newParamName = p[-1]
    # agrego a hash de params
    dirProced[currentScopeClass]['func'][currentScopeFunction]['params'][newParamName] = {'pos': 1, 'type': currentType}
    # agrego a hash de vars
    dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][newParamName] = {'tipo': currentType, 'size': 0} 
    
def p_mas_ids(p):
    '''mas_ids : COMA ID paramFound mas_ids
               | empty'''

def p_mas_parametros(p):
    '''mas_parametros : PUNTOYCOMA parametros
                      | empty'''
    
def p_posiblesbrackets(p):
    '''posiblesbrackets : B_ABRE B_CIERRA
                        | empty'''

def p_clases(p):
    'clases : CLASS ID herencia newclass L_ABRE cuerpoclase L_CIERRA'
    global currentScopeClass
    currentScopeClass = 'RedRobin'
    
def p_newclass(p):
    'newclass :'
    # Nuevo scope de clase
    global dirProced
    global currentScopeClass
    newScopeClass = p[-2]
    if newScopeClass in dirProced:
        print("CLASE YA DECLARADA")
        sys.exit()
    else:
        dirProced[newScopeClass] = {'func': {}, 'vars': {}}
        currentScopeClass = newScopeClass
    
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
    'retorno : GIVE expresion PUNTOYCOMA'

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
                       | expresion'''

def p_composicion_atributo(p):
    '''composicion_atributo : PUNTO ID
                            | empty'''

def p_ciclo(p):
    '''ciclo : cicloestatico
             | ciclodinamico'''

def p_cicloestatico(p):
    'cicloestatico : FOR ID IN P_ABRE valor GUIONBAJO valor P_CIERRA STEP valor L_ABRE cuerpofuncion L_CIERRA'

def p_ciclodinamico(p):
    'ciclodinamico : UNTIL P_ABRE expresion P_CIERRA DO L_ABRE cuerpofuncion L_CIERRA'

def p_condicional(p):
    'condicional : IF P_ABRE expresion P_CIERRA L_ABRE cuerpofuncion L_CIERRA condiciones_elif condicion_else'
    
def p_condiciones_elif(p):
    '''condiciones_elif : ELIF P_ABRE expresion P_CIERRA L_ABRE cuerpofuncion L_CIERRA condiciones_elif
                        | empty'''

def p_condicion_else(p):
    '''condicion_else : ELSE L_ABRE cuerpofuncion L_CIERRA
                      | empty'''

def p_asignacion(p):
    'asignacion : identificador IGUAL expresion PUNTOYCOMA'

def p_declaracion(p):
    'declaracion : tipovariable ID newvariable declara_arreglo_o_iniciacion mas_declaraciones PUNTOYCOMA'

def p_newvariable(p):
    'newvariable : '
    global dirProced
    global currentScopeClass
    global currentScopeFunction
    global currentType
    newVariableName = p[-1]
    # nueva variable encontrada
    # si es una variable de funcion
    # TODO: ver que rollo con los arreglos y valores de la variable y su tipo
    if currentScopeFunction != '':
        if newVariableName in dirProced[currentScopeClass]['func'][currentScopeFunction]:
            print("VARIABLE YA DECLARADA")
            sys.exit()
        else:
            dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][newVariableName] = {'tipo': 'number', 'size': 0}
    else:
        # si es una variable de clase
        if newVariableName in dirProced[currentScopeClass]['vars']:
            print("VARIABLE YA DECLARADA")
            sys.exit()
        else:
            dirProced[currentScopeClass]['vars'][newVariableName] = {'tipo': 'number', 'size': 0}    
    

def p_declara_arreglo_o_iniciacion(p):
    '''declara_arreglo_o_iniciacion : B_ABRE valor B_CIERRA
                                    | IGUAL expresion
                                    | empty'''

def p_mas_declaraciones(p):
    '''mas_declaraciones : COMA ID newvariable declara_arreglo_o_iniciacion mas_declaraciones
                         | empty'''

def p_expresion(p):
    'expresion : expresionii pendingors mas_expresion'

def p_mas_expresion(p):
    '''mas_expresion : OR newor expresion
                   | empty'''

def p_newor(p):
    'newor :'
    # nuevo or se agrega a la pila
    stackOpe.append(toCode['OR'])
    
def p_pendingors(p):
    'pendingors :'
    # pregunto si tengo ors pendientes por resolver
#    if stackOpe[-1] == toCode["OR"]:
#        ope2 = getType(stackOpe.pop())
#        ope1 = getType(stackOpe.pop())
#        if cubo.check(ope1, ope2, 'OR') != 'error':
#            print(ope1 + " " + ope2 + " OR")

def p_expresionii(p):
    'expresionii : expresioniii mas_expresionii'

def p_mas_expresionii(p):
    '''mas_expresionii : AND expresionii
                       | empty'''

def p_expresioniii(p):
    'expresioniii : expresioniv mas_expresioniii'

def p_mas_expresioniii(p):
    '''mas_expresioniii : operadorrelacional expresioniii
                        | empty'''

def p_expresioniv(p):
    'expresioniv : expresionv checkpendingterminos mas_expresioniv'

def p_mas_expresioniv(p):
    '''mas_expresioniv : operadortermino expresioniv
                       | empty'''
    
def p_checkpendingterminos(p):
    'checkpendingterminos :'
    # pregunto si tengo sumas o restas pendientes por resolver
    if len(stackOpe) > 0 and (stackOpe[-1] == toCode['+'] or stackOpe[-1] == toCode['-']):
        oope2 = stackDirMem.pop()
        oope1 = stackDirMem.pop()
        ope2 = getType(oope2)
        ope1 = getType(oope1)
        op = stackOpe[-1]
        resultType = cubo.check(ope1, ope2, op) 
        if resultType != 'error':
            # ocupo crear la temporal que manejara el resultado
            resultType += "Temp"
            # virtualTable[memConts[memCont[resultType]]] = {''} no se que cosa guardar de la temporal
            stackDirMem.append(memConts[memCont[resultType]])
            # genero el cuadruplo
            cuadruplos.append(Cuadruplo())
            cuadruplos[-1].v[0] = op
            cuadruplos[-1].v[1] = oope1
            cuadruplos[-1].v[2] = oope2
            cuadruplos[-1].v[3] = memConts[memCont[resultType]]
            memConts[memCont[resultType]] += 1
            

def p_expresionv(p):
    'expresionv : expresionvi mas_expresionv'

def p_mas_expresionv(p):
    '''mas_expresionv : operadorfactor expresionv
                      | empty'''

def p_expresionvi(p):
    '''expresionvi : valor
                   | negacion P_ABRE expresion P_CIERRA'''

def p_negacion(p):
    '''negacion : NEGAR
                | empty'''

def p_operadorrelacional(p):
    '''operadorrelacional : MAYOR_IGUAL
                          | MENOR_IGUAL
                          | IGUAL_IGUAL
                          | DIFERENTE'''

def p_operadortermino(p):
    '''operadortermino : OPERADOR_SUMA
                       | OPERADOR_RESTA'''
    stackOpe.append(toCode[p[1]])

def p_operadorfactor(p):
    '''operadorfactor : OPERADOR_MULTIPLICACION
                      | OPERADOR_DIVISION'''
    
def p_valor(p):
    '''valor : identificador
             | invocacion
             | CONST_STRING newCteString
             | valorbooleano newCteBool
             | negativo CONST_INTEGER newCteInt
             | negativo CONST_DOUBLE'''

def p_valorbooleano(p):
    '''valorbooleano : TRUE
                     | FALSE'''
def p_negativo(p):
    '''negativo : OPERADOR_RESTA
                | empty'''

def p_newCteString(p):
    'newCteString :'
    
def p_newCteBool(p):
    'newCteBool :'
    #print("new bool" + p[-1])
    
def p_newCteInt(p):
    'newCteInt :'
    # nueva constate entera, crear la direccion de mem si no existe
    if not p[-1] in mapCteToDir:
        mapCteToDir[p[-1]] = memConts[memCont['numberCte']]
        virtualTable[memCont['numberCte']] = p[-1]
        memConts[memCont['numberCte']] += 1
    stackDirMem.append(mapCteToDir[p[-1]])
             
def p_identificador(p):
    'identificador : ID atributo arreglo'
    # TODO: validar que el tipo de variable concuerde con su declaracion
    # Checar si existe la variable como:
        # Variable Global de la clase actual
        # Funcion dentro de la clase actual        
        # Variable local dentro funcion
    if not p[1] in dirProced[currentScopeClass]['vars'] and not p[1] in dirProced[currentScopeClass]['func'] and not p[1] in dirProced[currentScopeClass]['func'][currentScopeFunction]['vars']:
        print("Variable " + p[1] + " no declarada")
        sys.exit()
    
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

filename = "p1.txt"
# filename = input("Ingresa nombre de archivo con lenguaje Red Robin: ") 
f = open(filename, 'r')
s = f.read()
parser.parse(s)


if aprobado == True:
    print("Aprobado")
    for cuadruplo in cuadruplos:
        print(str(cuadruplo.v[0]) + " " + str(cuadruplo.v[1]) + " " + str(cuadruplo.v[2]) + " " + str(cuadruplo.v[3]))

