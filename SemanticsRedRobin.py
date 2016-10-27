import sys
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
stackJumps = []
cubo = Cubo()
cuadruplos = []

########### REGLAS DE SEMANTICA ###########

### CICLOS IF ###
elifCount = 0

# Llamada desde p_condicional
def p_smnewif(p):
    'smnewif :'
    condition = stackDirMem.pop()
    if getTypeCode(condition) != toCode['bool']:
        terminate("TYPE MISMATCH")
    else:
        createQuadruple(toCode['gotof'], condition, -1, -1)
        stackJumps.append(len(cuadruplos) - 1)
        
def p_smendif(p):
    'smendif :'
    global elifCount
    # lleno todos los goto pendientes hacia al zona ya no condicionada
    # es +1 porque tengo que hacer el ciclo aunque sea 1 vez para cerrar el primer if
    while elifCount + 1 > 0:
        exitIf = stackJumps.pop()
        cuadruplos[exitIf].fill(len(cuadruplos))
        elifCount -= 1
    elifCount = 0
    
def p_smnewelse(p):
    'smnewelse :'
    falseIf = stackJumps.pop()
    createQuadruple(toCode['goto'], -1, -1, -1)
    stackJumps.append(len(cuadruplos) - 1)
    cuadruplos[falseIf].fill(len(cuadruplos))
    
def p_smnewelif(p):
    'smnewelif :'
    global elifCount
    elifCount += 1

### termina ciclos if ###

### CICLOS WHILE ###

def p_smwhilestart(p):
    'smwhilestart :'
    stackJumps.append(len(cuadruplos))
    
def p_smwhilecondition(p):
    'smwhilecondition :'
    condition = stackDirMem.pop()
    if getTypeCode(condition) != toCode['bool']:
        terminate("TYPE MISSMATCH1")
    else:
        createQuadruple(toCode['gotof'], condition, -1, -1)
        stackJumps.append(len(cuadruplos) - 1)
        
def p_smendwhile(p):
    'smendwhile :'
    false = stackJumps.pop()
    retrn = stackJumps.pop()
    createQuadruple(toCode['goto'], -1, -1, retrn)
    cuadruplos[false].fill(len(cuadruplos))

### termina ciclos while ###

# Llamada desde p_program
def p_smnewprogram(p):
    'smnewprogram : '
    global dirProced
    dirProced['RedRobin'] = {'func': {}, 'vars': {}}
    # Declaracion predefinida de la constante 1 para la generacion de caudruplos que maneje la transformacion de negativos
    mapCteToDir[-1] = memConts[memCont['numberCte']]
    virtualTable[memConts[memCont['numberCte']]] = -1
    memConts[memCont['numberCte']] += 1
    
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
    dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][newParamName] = {'tipo': currentType, 'size': 0, 'mem': getMemSpace(currentType, 'Func', newParamName)}         

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
    newVarName = p[-1]
    # TODO: ver que rollo con los arreglos y valores de la variable
    if currentScopeFunction != '': # si estamos dentro de una funcion
        if newVarName in dirProced[currentScopeClass]['func'][currentScopeFunction]:
            terminate("REPEATED VARIABLE NAME")
        else:
            dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][newVarName] = {'tipo': currentType, 'size': 0, 'mem': getMemSpace(currentType, 'Func', newVarName)}
    else:
        # si es una variable de clase
        if newVarName in dirProced[currentScopeClass]['vars']:
            terminate("REPEATED VARIABLE NAME")
        else:
            dirProced[currentScopeClass]['vars'][newVarName] = {'tipo': currentType, 'size': 0, 'mem': getMemSpace(currentType, 'Class', newVarName)}

# Llamada desde p_expresion
def p_smcheckpendingors(p):
    'smcheckpendingors :'
    if len(stackOpe) > 0 and stackOpe[-1] == toCode['or']:
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
            
            
# Llamada desde p_expreionii
def p_smcheckpendingsingleope(p):
    'smcheckpendingands :'
    if len(stackOpe) > 0 and stackOpe[-1] == toCode['and']:
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
            
            
# Llamada desde p_expresioniii
def p_smcheckpendingrelational(p):
    'smcheckpendingrelational :'
    if len(stackOpe) > 0 and (stackOpe[-1] == toCode['>='] or stackOpe[-1] == toCode['<='] or stackOpe[-1] == toCode['=='] or stackOpe[-1] == toCode['<>']):
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
            
def p_smCheckPendingNegatives(p):
    'smCheckPendingNegatives :'
    if len(stackOpe) > 0 and stackOpe[-1] == toCode['neg']:
        opDir2 = stackDirMem.pop()
        opDir1 = mapCteToDir[-1]
        opTypeCode2 = getTypeCode(opDir2)
        opTypeCode1 = getTypeCode(opDir1)
        stackOpe.pop()
        resultType = cubo.check(opTypeCode1, opTypeCode2, toCode['*'])
        if resultType != 'error':
            resultType += 'Temp'
             # todo - agregar a tabla de direccion virtual el valor temporal  # Answer to todo: Esto es copiado de la de arriba tonses no se si aplica
            stackDirMem.append(memConts[memCont[resultType]])
            createQuadruple(toCode['*'], opDir1, opDir2, memConts[memCont[resultType]])
            memConts[memCont[resultType]] += 1

def p_smaddSingleOpe(p):
    'smaddSingleOpe :'
    pushToStackOpe(p[-1])
    
def p_smRemoveParentesis(p):
    'smRemoveParentesis :'
    opeCode = stackOpe.pop()
    if opeCode != toCode['(']:
        terminate("ERROR EXPRESION")
        
def p_smAsignacion(p):
    'smAsignacion :'
    resultDir = stackDirMem.pop()
    varDir = stackDirMem.pop()
    createQuadruple(toCode['='], resultDir, '-1', varDir)
            
# Llamada desde p_valor
def p_smnewcteint(p):
    'smnewcteint :'
    # nueva constate entera, crear la direccion de mem si no existe
    if not p[-1] in mapCteToDir:
        mapCteToDir[p[-1]] = memConts[memCont['numberCte']]
        virtualTable[memConts[memCont['numberCte']]] = p[-1]
        memConts[memCont['numberCte']] += 1
    stackDirMem.append(mapCteToDir[p[-1]])
    
# Llamada desde p_valor
def p_smnewctedouble(p):
    'smnewctedouble :'
    # nueva constate double, crear la direccion de mem si no existe
    if not p[-1] in mapCteToDir:
        mapCteToDir[p[-1]] = memConts[memCont['realCte']]
        virtualTable[memConts[memCont['realCte']]] = p[-1]
        memConts[memCont['realCte']] += 1
    stackDirMem.append(mapCteToDir[p[-1]])    

# Llama desde p_negacion o p_negativo
def p_smNewNegativo(p):
    'smNewNegativo :'
    # Genera cuadruplo de resta a 0 para convertir una constante numerica u expresion a su negativo
    stackOpe.append(toCode['neg'])

    
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
    
def getMemSpace(varType, scope, varName):
    memType = varType + scope
    #todo - ver que guardo, val depende del tipo
    virtualTable[memConts[memCont[memType]]] = {'name': varName, 'val': -1}
    memConts[memCont[memType]] += 1
    return memConts[memCont[memType]] - 1
    
# Llamada de p_identificador
def validateIdSemantics(currentIdName):
    # TODO: validar que el tipo de variable concuerde con su declaracion
    # Checo si existe la variable como:
        # Variable Global de la clase actual
        # Funcion dentro de la clase actual        
        # Variable local dentro funcion
    if not currentIdName in dirProced[currentScopeClass]['vars'] and not currentIdName in dirProced[currentScopeClass]['func'] and (currentScopeFunction == '' or not currentIdName in dirProced[currentScopeClass]['func'][currentScopeFunction]['vars']):
        terminate("Variable " + currentIdName + " not declared")
    else:
        # variable valida, insertar a pila
#        print("class scope " + currentScopeClass)
#        print("func scope " + currentScopeFunction)
#        print("var name " +  currentIdName)
        if currentIdName in dirProced[currentScopeClass]['vars']:
            stackDirMem.append(dirProced[currentScopeClass]['vars'][currentIdName]['mem'])
        elif currentScopeFunction == '' or currentIdName in dirProced[currentScopeClass]['func'][currentScopeFunction]['vars']:
            stackDirMem.append(dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][currentIdName]['mem'])
            
def newCteBool(newBool):
    virtualTable[memConts[memCont['boolCte']]] = 'false'
    virtualTable[memConts[memCont['boolCte']] + 1] = 'true'
    if newBool == 'true':
        stackDirMem.append(memConts[memCont['boolCte']] + 1)
    else:
        stackDirMem.append(memConts[memCont['boolCte']])
    
        