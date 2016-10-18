from Cubo import *
from Cuadruplo import *

########### PROCEDURES DIRECTORY ###########
dirProced = {}
currentType = ''
currentScopeClass = 'RedRobin'
currentScopeFunction = ''

########### VIRTUAL ADDRESSES ###########
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

def getTypeCode(memAddress):
    if memAddress <= memLimit['numberClass']:
        return toCode['number']
    if memAddress <= memLimit['realClass']:
        return toCode['real']
    if memAddress <= memLimit['stringClass']:
        return toCode['string']
    if memAddress <= memLimit['boolClass']:
        return toCode['bool']
    
    if memAddress <= memLimit['numberFunc']:
        return toCode['number']
    if memAddress <= memLimit['realFunc']:
        return toCode['real']
    if memAddress <= memLimit['stringFunc']:
        return toCode['string']
    if memAddress <= memLimit['boolFunc']:
        return toCode['bool']
    
    if memAddress <= memLimit['numberTemp']:
        return toCode['number']
    if memAddress <= memLimit['realTemp']:
        return toCode['real']
    if memAddress <= memLimit['stringTemp']:
        return toCode['string']
    if memAddress <= memLimit['boolTemp']:
        return toCode['bool']
    
    if memAddress <= memLimit['numberCte']:
        return toCode['number']
    if memAddress <= memLimit['realCte']:
        return toCode['real']
    if memAddress <= memLimit['stringCte']:
        return toCode['string']
    if memAddress <= memLimit['boolCte']:
        return toCode['bool']
    
########### GENERACION DE CUADRUPLOS ###########
stackOpe = []
stackDirMem = []
cubo = Cubo()
cuadruplos = []

########### REGLAS DE SEMANTICA ###########

# Llamada desde p_program
def p_smnewprogram(p):
    'smnewprogram : '
    global dirProced
    dirProced['RedRobin'] = {'func': {}, 'vars': {}}
    
# Llamada desde p_funciones
def p_smnewfunction(p):
    'smnewfunction : '
    global dirProced
    global currentScopeClass
    global currentScopeFunction
    newScopeFunction = p[-1]
    # TODO - encontrar el tipo de la funcion, hardcodeado con empty
    if newScopeFunction in dirProced[currentScopeClass]['func']:
        terminate("REPEATED FUNCTION NAME")
    else:
        dirProced[currentScopeClass]['func'][newScopeFunction] = {'vars': {}, 'giveType': 'empty', 'params': {}}
        setScopeFunction(newScopeFunction)
        
# Llamada desde p_parametros
def p_smnewparam(p):
    'smnewparam :'
    newParamName = p[-1]
    # agrego a hash de params TODO - actualizar al posicion del parametro, dar dir de memoria a variable
    dirProced[currentScopeClass]['func'][currentScopeFunction]['params'][newParamName] = {'pos': 1, 'type': currentType}
    # agrego a hash de vars
    dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][newParamName] = {'tipo': currentType, 'size': 0}         

# Llamada desde p_clases
def p_smnewclass(p):
    'smnewclass :'
    # Nuevo scope de clase
    global dirProced
    global currentScopeClass
    newScopeClass = p[-2]
    if newScopeClass in dirProced:
        terminate("REPEATED CLASS NAME")
    else:
        dirProced[newScopeClass] = {'func': {}, 'vars': {}}
        setScopeClass(newScopeClass)
        
# Llamada desde p_declaracion y p_masdeclaraciones
def p_smnewvariable(p):
    'smnewvariable : '
    global dirProced
    global currentScopeClass
    global currentScopeFunction
    global currentType
    newVarName = p[-1]
    # nueva variable encontrada
    # si es una variable de funcion
    # TODO: ver que rollo con los arreglos y valores de la variable y su tipo
    if currentScopeFunction != '': # si estamos dentro de una funcion
        if newVarName in dirProced[currentScopeClass]['func'][currentScopeFunction]:
            terminate("REPEATED VARIABLE NAME")
        else:
            dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][newVarName] = {'tipo': 'number', 'size': 0}
    else:
        # si es una variable de clase
        if newVarName in dirProced[currentScopeClass]['vars']:
            terminate("REPEATED VARIABLE NAME")
        else:
            dirProced[currentScopeClass]['vars'][newVarName] = {'tipo': 'number', 'size': 0}

# Llamada desde p_expresioniv
def p_smcheckpendingterms(p):
    'smcheckpendingterms :'
    # pregunto si tengo sumas o restas pendientes por resolver
    if len(stackOpe) > 0 and (stackOpe[-1] == toCode['+'] or stackOpe[-1] == toCode['-']):
        # obtengo direcciones de memoria de los valores a sumar/restar
        opDir2 = stackDirMem.pop()
        opDir1 = stackDirMem.pop()
        opTypeCode2 = getTypeCode(opDir2)
        opTypeCode1 = getTypeCode(opDir1)
        opeCode = stackOpe.pop()
        resultType = cubo.check(opTypeCode1, opTypeCode2, opeCode) 
        if resultType != 'error':
            # ocupo crear la temporal que manejara el resultado
            resultType += "Temp"
            # virtualTable[memConts[memCont[resultType]]] = {''} Guardar algo en la temporal (?)
            stackDirMem.append(memConts[memCont[resultType]])
            createQuadruple(opeCode, opDir1, opDir2, memConts[memCont[resultType]])
            memConts[memCont[resultType]] += 1
        else:
            terminate("TYPE MISMATCH")
            
def p_smcheckpendingfactors(p):
    'smcheckpendingfactors :'
    if len(stackOpe) > 0 and (stackOpe[-1] == toCode['*'] or stackOpe[-1] == toCode['/']):
        opDir2 = stackDirMem.pop()
        opDir1 = stackDirMem.pop()
        opTypeCode2 = getTypeCode(opDir2)
        opTypeCode1 = getTypeCode(opDir1)
        opeCode = stackOpe.pop()
        resultType = cubo.check(opTypeCode1, opTypeCode2, opeCode)
        if resultType != 'error':
            resultType += 'Temp'
            # todo - agregar a tabla de direccion virtual el valor temporal
            stackDirMem.append(memConts[memCont[resultType]])
            createQuadruple(opeCode, opDir1, opDir2, memConts[memCont[resultType]])
            memConts[memCont[resultType]] += 1
            
# Llamada desde p_valor
def p_smnewcteint(p):
    'smnewcteint :'
    # nueva constate entera, crear la direccion de mem si no existe
    global stackDirMem
    if not p[-1] in mapCteToDir:
        mapCteToDir[p[-1]] = memConts[memCont['numberCte']]
        virtualTable[memConts[memCont['numberCte']]] = p[-1]
        memConts[memCont['numberCte']] += 1
    stackDirMem.append(mapCteToDir[p[-1]])

########### FUNCIONES DE SEMANTICA ###########

def setScopeFunction(newScopeFunc):
    global currentScopeFunction
    currentScopeFunction = newScopeFunc
    
def setCurrentType(newType):
    global currentType
    currentType = newType    
    
def setScopeClass(newScopeClass):
    global currentScopeClass
    currentScopeClass = newScopeClass
    
def pushToStackOpe(opeSymbol):
    global stackOpe
    stackOpe.append(toCode[opeSymbol])    
    
def terminate(message):
    print(message)
    sys.exit()
    
def createQuadruple(ope, op1, op2, r):
    global cuadruplos
    cuadruplos.append(Cuadruplo())
    cuadruplos[-1].ope = ope
    cuadruplos[-1].op1 = op1
    cuadruplos[-1].op2 = op2
    cuadruplos[-1].r = r
    
# Llamada de p_identificador
def validateVarSemantics(currentVarName):
    # TODO: validar que el tipo de variable concuerde con su declaracion
    # Checo si existe la variable como:
        # Variable Global de la clase actual
        # Funcion dentro de la clase actual        
        # Variable local dentro funcion
    if not currentVarName in dirProced[currentScopeClass]['vars'] and not currentVarName in dirProced[currentScopeClass]['func'] and not currentVarName in dirProced[currentScopeClass]['func'][currentScopeFunction]['vars']:
        terminate("Variable " + " not declared")
    
        