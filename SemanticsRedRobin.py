import sys
from Cubo import *
from Cuadruplo import *

# dirProced: Diccionario que guarda los procedimientos y variables del programa. Estructura:
# [currentScopeClass]:
#   ['func']:
#       [currentScopeFunction]
#           ['vars']
#              [variableName]
#                 ['tipo'] - Tipo de variable
#                 ['size'] - Tamaño de variable
#                 ['mem'] - Direccion de memoria virtual
#           ['params']
#               [contParam]
#                  ['name'] - nombre del parametro
#                  ['type'] - tipo del parametro
#           ['tam'] - diccionario de tamaños requeridos, not defined yet TODO
#           ['giveType'] - Tipo de retorno de la funcion
#           ['privilages'] - Privilegio (public o private)
#           ['mem'] - Direccion de memoria de su variable global asignada
#           ['quad'] - Cuadruplo de inicio
#   ['vars']
#       [variableName]
#           ['tipo'] - Tipo de variable
#           ['size'] - Tamaño de variable (quizas sirva para arrays, unused)
#           ['mem'] - Direccion de memoria virtual
dirProced = {}

# currentType: Guarda el ultimo tipo de dato parseado. Su valor es el ultimo tipo de dato declarado
currentType = ''

# currentScopeClass: Guarda la clase actual que se esta parseando. Su valor se actualiza si se entra a parsear una nueva clase
currentScopeClass = 'RedRobin'

# currentScopeFunction: Guarda la funcion actual que se esta parseando. Su valor se actualiza si se entra a parsear una nueva funcion
currentScopeFunction = ''

########### DIRECCIONES VIRTUALES ###########

# virtualTable: Diccionario donde la llave es la direccion de memoria virtual. AUN NO SE SI ES NECESARIA, NO SE ESTA USANDO
virtualTable = {}

# mapCteToDir: Diccionario que dada una variable constante te regresa su direccion de memoria virtual
mapCteToDir = {}

# memConts: Arreglo de contadores enteros. Cada casilla pertenece a un tipo de dato con determinado scope. El valor de la casilla apunta a una direccion libre.
memConts = numpy.zeros(16)

# Inicializando memConts.
# memCont: diccionario que dado un tipo y scope regresa el indice correspondiente. Se usa para facilidad de lectura en el codigo.
# memStart: diccionario que guarda la primera posicion de memoria de cierto tipo y scope
# memLimit: diccionario que guarda la ultima posicion de memoria de cierto tipo y scope
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

# getTypeCode: dada una direccion de memoria regresa el codigo del tipo de dato correspondiente
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

def p_smMainFound(p):
    'smMainFound :'
    cuadruplos[0].fill(len(cuadruplos))
    
# contador para saber el indice del parametro tanto para invocar como para declarar
contParam = 1

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

### CICLOS for ###

def p_smforprepare(p):
    'smforprepare :'
    validateIdSemantics(p[-1])
    #Validar que sea numero o decimal el operando que se quiere utilizar como iterador del ciclo
    variable = stackDirMem.pop()
    if getTypeCode(variable) != toCode['number'] and getTypeCode(variable) != toCode['real']:
        terminate("TYPE MISMATCH")
    else:
        stackDirMem.append(variable)

def p_smforinitialize(p):
    'smforinitialize :'
    #Validar que sea numero o decimal el operando que va a inicializar el iterador del ciclo
    variable = stackDirMem.pop()
    if getTypeCode(variable) != toCode['number'] and getTypeCode(variable) != toCode['real']:
        terminate("TYPE MISMATCH")
    else:
        #TODO Validar con cubo semantico
        createQuadruple(toCode['='], variable, -1, stackDirMem[-1])

def p_smforstart(p):
    'smforstart :'
    stackJumps.append(len(cuadruplos))

def p_smforcondition(p):
    'smforcondition :'
    #Validar que el valor como final del rango del ciclo for sea numerico
    variable = stackDirMem.pop()
    if getTypeCode(variable) != toCode['number'] and getTypeCode(variable) != toCode['real']:
        terminate("TYPE MISMATCH")
    else:
        opType1 = getTypeCode(stackDirMem[-1])
        opType2 = getTypeCode(variable)
        resultType = cubo.check(opType1, opType2, toCode['<='])
        if resultType != 'error':
            resultType += 'Temp'
            # todo - agregar a tabla de direccion virtual el valor temporal
            createQuadruple(toCode['<='], stackDirMem[-1], variable, memConts[memCont[resultType]])
            stackDirMem.append(memConts[memCont[resultType]])
            memConts[memCont[resultType]] += 1
            condicion = stackDirMem.pop()
            createQuadruple(toCode['gotof'], condicion, -1, -1)
            stackJumps.append(len(cuadruplos) - 1)
        else:
            terminate("TYPE MISMATCH")

def p_smforend(p):
    'smforend :'
    #Pop de la pila de operandos que debe ser el valor arrojado despues del step
    variable = stackDirMem.pop()
    iterador = stackDirMem.pop()
    if getTypeCode(variable) != toCode['number'] and getTypeCode(variable) != toCode['real']:
        terminate("TYPE MISMATCH")
    elif getTypeCode(iterador) != toCode['number'] and getTypeCode(iterador) != toCode['real']:
        terminate("TYPE MISMATCH")
    else:
        opType1 = getTypeCode(iterador)
        opType2 = getTypeCode(variable)
        resultType = cubo.check(opType1, opType2, toCode['+'])
        if resultType != 'error':
            resultType += 'Temp'
            # todo - agregar a tabla de direccion virtual el valor temporal
            stackDirMem.append(memConts[memCont[resultType]])
            createQuadruple(toCode['+'], iterador, variable, memConts[memCont[resultType]])
            memConts[memCont[resultType]] += 1
            nuevoValorIterador = stackDirMem.pop()
            createQuadruple(toCode['='], nuevoValorIterador, -1, iterador)

            saltoEnFalso = stackJumps.pop()
            saltoNuevaIteracion = stackJumps.pop()
            createQuadruple(toCode['goto'], -1, -1, saltoNuevaIteracion)
            cuadruplos[saltoEnFalso].fill(len(cuadruplos))
        else:
            terminate("TYPE MISMATCH")

### termina ciclos for ###

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
    global contParam
    contParam = 1
    newScopeFunction = p[-1]
    giveType = p[-2]
    privlages = p[-3]
    # TODO - checar que no haya una variable global con el mismo nombre
    if newScopeFunction in dirProced[currentScopeClass]['func']:
        terminate("REPEATED FUNCTION NAME")
    else:
        memVar = getMemSpace(giveType, 'Class', newScopeFunction)
        # añado la funcion a mi directorio de procedimientos
        dirProced[currentScopeClass]['func'][newScopeFunction] = {'vars': {}, 'giveType': p[-2], 'params': {}, 'tam': {}, 'privilages': p[-3], 'mem': memVar, 'quad': len(cuadruplos) }
        # creo la variable que guardara el valor de retorno
        dirProced['RedRobin']['vars'][newScopeFunction] = {'tipo': giveType, 'size': 0, 'mem': memVar}
        setScopeFunction(newScopeFunction)

        
# Llamada desde p_parametros
def p_smnewparam(p):
    'smnewparam :'
    global contParam
    newParamName = p[-1]
    # agrego a hash de params
    dirProced[currentScopeClass]['func'][currentScopeFunction]['params'][contParam] = {'name': newParamName, 'type': currentType}
    # agrego a hash de vars
    dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][newParamName] = {'tipo': currentType, 'size': 0, 'mem': getMemSpace(currentType, 'Func', newParamName)}
    contParam += 1

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
    # TODO: checar que no se llame igual que una funcion
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
    createQuadruple(toCode['='], resultDir, -1, varDir)
            
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

    
#### SEMANTICA DE FUNCIONEEES #####
# TODO - manejar los returns

currentFunction = ""

# Llamada desde p_invocacion
def p_smNewInvocacion(p):
    'smNewInvocacion :'
    global contParam
    global currentFunction
    funName = p[-2]
    if funName in dirProced[currentScopeClass]['func']:
        contParam = 1
        currentFunction = funName
        createQuadruple(toCode['era'], -1, -1, dirProced[currentScopeClass]['func'][funName]['mem'])
    else:
        terminate("Function " + funName + " not declared")
        
# Llamada desde p_valorargumentos
def p_smParamExpresion(p):
    'smParamExpresion :'
    global contParam
    if contParam in dirProced[currentScopeClass]['func'][currentFunction]['params']: 
        paramDir = stackDirMem.pop()
        nameVarParam = dirProced[currentScopeClass]['func'][currentFunction]['params'][contParam]['name']
        dirVarParam = dirProced[currentScopeClass]['func'][currentFunction]['vars'][nameVarParam]['mem']
        if cubo.check(getTypeCode(dirVarParam), getTypeCode(paramDir), toCode['=']) != 'error':
            createQuadruple(toCode['param'], paramDir, -1, dirVarParam)
            contParam += 1
        else:
            terminate("Error in params of function " + currentFunction)
    else:
        terminate("Wrong number of arguments")
        
# Llamada dedes p_invocacion
def p_smEndInvocacion(p):
    'smEndInvocacion :'
    global contParam
    if len(dirProced[currentScopeClass]['func'][currentFunction]['params']) == contParam - 1:
        createQuadruple(toCode['gosub'], -1, -1, dirProced[currentScopeClass]['func'][currentFunction]['quad'])
    else:
        terminate("wrong number of arguments")
        
    
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
    # TODO: validar que no se llame igual que una funcion
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
    
    
# creo cuadruplo go to main
createQuadruple(toCode['goto'], -1, -1, -1)    
        