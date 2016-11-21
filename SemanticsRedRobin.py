import sys
import copy
from Cubo import *
from Cuadruplo import *
from MemoriasVirtuales import *

# dirProced: Diccionario que guarda los procedimientos y variables del programa. Estructura:
# [currentScopeClass]:
#   ['parent'] - Padre de la clase en caso de existir
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
#           ['class'] - clase en donde esta su definicion
#   ['vars']
#       [variableName]
#           ['tipo'] - Tipo de variable
#           ['size'] - Tamaño de variable (quizas sirva para arrays, unused)
#           ['mem'] - Direccion de memoria virtual
#   ['obj']
#       [objectName]
#           ['class'] - clase a la que pertenece este objeto
#           ['attr']
#               [attrName]
#                   ['tipo'] - Tipo de variable
#                   ['size'] - Tamaño de variable (quizas sirva para arrays, unused)
#                   ['mem'] - Direccion de memoria virtual
dirProced = {}

# currentType: Guarda el ultimo tipo de dato parseado. Su valor es el ultimo tipo de dato declarado
currentType = ''

# currentScopeClass: Guarda la clase actual que se esta parseando. Su valor se actualiza si se entra a parsear una nueva clase
currentScopeClass = 'RedRobin'

# currentScopeFunction: Guarda la funcion actual que se esta parseando. Su valor se actualiza si se entra a parsear una nueva funcion
currentScopeFunction = ''
    
########### GENERACION DE CUADRUPLOS ###########

# stackOpe: Pila que guarda los operadores pendientes por resolver
stackOpe = []

# stackDirMem: pila que guardar las direcciones de los operandos pendientes por resolver
stackDirMem = []

# stackJumps: pila de saltos que garda cuadruplos pendientes por llenar
stackJumps = []

# Cuadruplos: lista que almacena todos los cuadruplos generados
cuadruplos = []

# Instanciamos el cubo semantico
cubo = Cubo()

# contador para saber el indice del parametro actual tanto para invocar como para declarar
contParam = 1

########### REGLAS DE SEMANTICA ###########

# smMainFound: Se encarga de crear el cuadruplo inicial que llevara el flujo a la primera instruccion del main (RedRobin)
# Llamada desde p_cuerpoprogram
def p_smMainFound(p):
    'smMainFound :'
    cuadruplos[0].fill(len(cuadruplos))

### CICLOS IF ###

# Contador para saber cuantos cuadruplos de elif se dejaron pendientes por llenar
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
    validateIdSemantics(p[-1], None, None)
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
    dirProced['RedRobin'] = {'func': {}, 'vars': {}, 'obj': {}}
    # Declaracion predefinida de la constante -1 para la generacion de caudruplos que maneje la transformacion de negativos
    mapCteToDir[-1] = memConts[memCont['numberCte']]
    memConts[memCont['numberCte']] += 1
    
# Llamada desde p_funciones
def p_smnewfunction(p):
    'smnewfunction : '
    global contParam
    contParam = 1
    newScopeFunction = p[-1]
    giveType = p[-2]
    if not isAtomic(giveType) and giveType != 'empty':
        terminate("ONLY PRIMITIVE TYPES CAN BE RETURNED")
    privlages = p[-3]
    # TODO - checar que no haya una variable global con el mismo nombre
    if existsFunc(newScopeFunction):
        terminate("NAME ALREADY IN USE")
    else:
        memVar = -1
        if giveType != 'empty':
            memVar = getMemSpace(giveType, 'Class', newScopeFunction)
            # creo la variable que guardara el valor de retorno
            dirProced['RedRobin']['vars'][newScopeFunction] = {'tipo': giveType, 'size': 0, 'mem': memVar}
        dirProced[currentScopeClass]['func'][newScopeFunction] = {'vars': {}, 'giveType': p[-2], 'params': {}, 'tam': {}, 'privilages': p[-3], 'mem': memVar, 'quad': len(cuadruplos), 'class': currentScopeClass }
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
    # Nuevo scope de clase, estoy definiendo una nueva calse
    global currentScopeClass
    newScopeClass = p[-2]
    # Si ya existe, es error
    if newScopeClass in dirProced:
        terminate("REPEATED CLASS NAME")
    else:
        parent = ''
        parentObjects = {}
        parentVariables = {}   
        parentFunctions = {}
        # Pregunto si tengo un padre
        # TODO - invalidar mas 1 nivel en herencia
        if p[-1] != None:
            parent = p[-1]
            # Si tengo un padre debo copiar todas su variables y sus objetos. Estos objetos no pueden tener mas objetos
            
            # Jalo las variables de mi padre
            parentVariables = copy.deepcopy(dirProced[parent]['vars'])
            
            # Jalo las funciones de mi padre
            parentFunctions = copy.deepcopy(dirProced[parent]['func'])
            
            # Obtengo los objetos de mi padre, tampoco pueden tener mas objetos para evitar composicion de mas de 1 nivel
            parentObjects = copy.deepcopy(dirProced[parent]['obj'])
            
            # Valido lo anterior
            # mi padre SI puede tener objetos, pero esos objetos NO pueden tener mas objetos
            # por cada objeto reviso si en su definicion de clase tiene objetos
            for objName in parentObjects:
                objectClass = parentObjects[objName]['class']
                if len(dirProced[objectClass]['obj']) > 0:
                    terminate("MORE THAN 1 LEVEL IN COMPOSITION2")
                    
            # Cada atributo de objeto debe tener direccion de memoria unica para mantener la unicidad de memorias dentro del scope
            for objName in parentObjects:
                dicAttr = parentObjects[objName]['attr']
                for nameVar in dicAttr: 
                    parentObjects[objName]['attr'][nameVar]['mem'] = getMemSpace(dicAttr[nameVar]['tipo'], 'Class', nameVar)
                    
            # Hago lo mismo de arriba con las variables
            for varName in parentVariables:
                parentVariables[varName]['mem'] = getMemSpace(parentVariables[varName]['tipo'], 'Class', varName)
                
        dirProced[newScopeClass] = {'func': parentFunctions, 'vars': parentVariables, 'obj': parentObjects, 'parent': parent}
        setScopeClass(newScopeClass)
        
def existsVar(newVarName):
    # Si estamos dentro de una funcion
    if currentScopeFunction != '':
        # Si es una variable dentro de la funcion
        if newVarName in dirProced[currentScopeClass]['func'][currentScopeFunction]['vars']:
            return True
    # si es una variable de clase
    if newVarName in dirProced[currentScopeClass]['vars']:
        return True
    # si ya hay una funcion que se llama asi (var global)
    if newVarName in dirProced[currentScopeClass]['func']:
        return True
    return False
    
def existsObj(newObjName):
    # Si estamos dentro de una funcion
    if currentScopeFunction != '':
        # si es un objeto dentro de la funcion TODO
        if newObjName in dirProced[currentScopeClass]['func'][currentScopeFunction]['vars']:
            return True
    # si es un objeto de clase
    if newObjName in dirProced[currentScopeClass]['obj']:
        return True
    return False
    
def existsFunc(newFunName):
    # Si ya hay una funcion que se llama asi
    if newFunName in dirProced[currentScopeClass]['func']:
        return True

def isAtomic(mType):
    if mType == 'number' or mType == 'real' or mType == 'bool' or mType == 'string':
        return True
    return False
    
# Llamada desde p_declaracion y p_masdeclaraciones
def p_smnewvariable(p):
    'smnewvariable : '
    newVarName = p[-1]
    # Si el nobre ya existe, está repetido
    if existsVar(newVarName) or existsObj(newVarName) or existsFunc(newVarName):
        terminate("REPETAED VARIABLE NAME: " + newVarName)
    
    # Si estamos dentro de una funcion
    if currentScopeFunction != '': 
        # TODO- objetos dentro de funciones
        # Instancio el primitivo de funcion
        dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][newVarName] = {'tipo': currentType, 'size': 0, 'mem': getMemSpace(currentType, 'Func', newVarName)}
    else:
        # else-  Si estamos fuera de una funcion
        if isAtomic(currentType):
            # instancio el primitivo de clase
            dirProced[currentScopeClass]['vars'][newVarName] = {'tipo': currentType, 'size': 0, 'mem': getMemSpace(currentType, 'Class', newVarName)}
        else:
            # Es un objeto
            # Valido que la clase del objeto exista
            if currentType not in dirProced or currentType == 'RedRobin':
                terminate("WRONG OBJECT TYPE")
            # Depende si estoy en la clase main red robin o en alguna otra clase el comportamiento cambia
            if currentScopeClass == 'RedRobin':
                # Hay que crear una instancia de la clase
                dicAttr = copy.deepcopy(dirProced[currentType]['vars']);
                for varName in dicAttr:
                    dicAttr[varName]['mem'] = getMemSpace(dicAttr[varName]['tipo'], 'Class', varName)
                    arraySize = dicAttr[varName]['size']
                    # Pido todas las memorias que ocupo en caso de q sea un arreglo
                    if int(arraySize) > 0:
                        memConts[memCont[dicAttr[varName]['tipo'] + 'Class']] += (int(arraySize) - 1)
                    
                dicObj = copy.deepcopy(dirProced[currentType]['obj']);
                for objName in dicObj:
                    dicAttrObj = dicObj[objName]['attr']
                    for attrName in dicAttrObj:
                        dicObj[objName]['attr'][attrName]['mem'] = getMemSpace(dicObj[objName]['attr'][attrName]['tipo'], 'Class', attrName)
                        arraySize = dicObj[objName]['attr'][attrName]['size']
                        if int(arraySize) > 0:
                            memConts[memCont[dicObj[objName]['attr'][attrName]['tipo']+ 'Class']] += (int(arraySize) - 1)
                
                dirProced['RedRobin']['obj'][newVarName] = {'class': currentType, 'attr': dicAttr, 'obj': dicObj}
            else:
                # Si tiene mas objetos mi composicion, seria error
                if len(dirProced[currentType]['obj']) > 0:
                    terminate("MORE THAN 1 LEVEL IN COMPOSITION1")
                
                # Arrastro las variables de la clase que estoy "instanciando" en esta clase
                variables = copy.deepcopy(dirProced[currentType]['vars'])
                
                # Asigno direcciones nuevas para mantener unicidad 
                for varName in variables:
                    variables[varName]['mem'] = getMemSpace(variables[varName]['tipo'], 'Class', varName)
                    arraySize = variables[varName]['size']
                    if int(arraySize) > 0:
                        memConts[memCont[variables[varName]['tipo'] + 'Class']] += (int(arraySize) - 1)                    
                
                # Actualizo el directorio de variables de la clase "papa"
                dirProced[currentScopeClass]['obj'][newVarName] = {'class': currentType, 'attr': variables}

# Llamada desde p_expresion

def p_smNewArray(p):
    'smNewArray :'
    # Descartamos la direccion, ocupamos el numero en si
    stackDirMem.pop()
    # Obtenemos el numero del lexico
    arraySize = p[-3]
    if int(arraySize) <= 0:
        terminate("array size must be greater than 0");
    # Obtenemos el nombre del arreglo, ya fue declarado, solo hay que aumentar el size
    varName = p[-6]
    # Obtenemos el tipo del arreglo para saber q tipo de memorias darle
    typeArray = currentType
    if currentScopeFunction != "":
        dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][varName]['size'] = arraySize
        memConts[memCont[typeArray + 'Func']] += (int(arraySize) - 1)
    else:
        dirProced[currentScopeClass]['vars'][varName]['size'] = arraySize
        memConts[memCont[typeArray + 'Class']] += (int(arraySize) - 1)
    
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
        resultType = cubo.check(abs(opTypeCode1), abs(opTypeCode2), opeCode) 
        if resultType != 'error':
            # ocupo crear la temporal que manejara el resultado
            resultType += "Temp"
            stackDirMem.append(memConts[memCont[resultType]])
            createQuadruple(opeCode, opDir1, opDir2, memConts[memCont[resultType]])
            memConts[memCont[resultType]] += 1
        else:
            terminate("TYPE MISSMATCH")
            
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
            stackDirMem.append(memConts[memCont[resultType]])
            createQuadruple(opeCode, opDir1, opDir2, memConts[memCont[resultType]])
            memConts[memCont[resultType]] += 1
        else:
            terminate("TYPE MISSMATCH")            
            
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
            stackDirMem.append(memConts[memCont[resultType]])
            createQuadruple(toCode['*'], opDir1, opDir2, memConts[memCont[resultType]])
            memConts[memCont[resultType]] += 1
        else:
            terminate("TYPE MISSMATCH")

def p_smaddSingleOpe(p):
    'smaddSingleOpe :'
    pushToStackOpe(p[-1])
    
def p_smaddParentesis(p):
    'smaddParentesis :'
    pushToStackOpe('(')
    
def p_smRemoveParentesis(p):
    'smRemoveParentesis :'
    opeCode = stackOpe.pop()
    if opeCode != toCode['(']:
        print(toSymbol[opeCode])
        print(len(cuadruplos))
        terminate("ERROR EXPRESION")
        
def p_smAsignacion(p):
    'smAsignacion :'
    resultDir = stackDirMem.pop()
    varDir = stackDirMem.pop()
    if cubo.check(getTypeCode(resultDir), getTypeCode(varDir), toCode['=']) != 'error':
        createQuadruple(toCode['='], resultDir, -1, varDir)
    else:
        terminate("TYPE MISSMATCH")
            
# Llamada desde p_valor
def p_smnewcteint(p):
    'smnewcteint :'
    # nueva constate entera, crear la direccion de mem si no existe
    if not p[-1] in mapCteToDir:
        mapCteToDir[p[-1]] = memConts[memCont['numberCte']]
        memConts[memCont['numberCte']] += 1
    stackDirMem.append(mapCteToDir[p[-1]])
    
# Llamada desde p_valor
def p_smnewctedouble(p):
    'smnewctedouble :'
    # nueva constate double, crear la direccion de mem si no existe
    if not p[-1] in mapCteToDir:
        mapCteToDir[p[-1]] = memConts[memCont['realCte']]
        memConts[memCont['realCte']] += 1
    stackDirMem.append(mapCteToDir[p[-1]])    

# Llamada desde p_valor
def p_smNewCteString(p):
    'smNewCteString :'
    # nueva constate string, crear la direccion de mem si no existe
    if not p[-1] in mapCteToDir:
        mapCteToDir[p[-1]] = memConts[memCont['stringCte']]
        memConts[memCont['stringCte']] += 1
    stackDirMem.append(mapCteToDir[p[-1]])

# Llama desde p_negacion o p_negativo
def p_smNewNegativo(p):
    'smNewNegativo :'
    # Genera cuadruplo de resta a 0 para convertir una constante numerica u expresion a su negativo
    stackOpe.append(toCode['neg'])

    
#### SEMANTICA DE FUNCIONEEES #####

currentFunction = ""
currentClass = ""
# key: real, value: temp o fantasma
hashRef = {}
hashRefTam = {}

def generalInvocationRutine(funName, currClass, objPath):
    global currentFunction
    global contParam
    global currentClass
    # Inicializo variables auxiliares que serviran durante la rutina
    contParam = 1
    hashRef.clear()
    hashRefTam.clear()
    currentFunction = funName
    # Current class es en DONDE esta definida la funcion
    # puede ser en el currentClassScope o en la class del objeto que invoco la funcion
    currentClass = currClass
    createQuadruple(toCode['era'], -1, -1, dirProced[currentClass]['func'][funName]['quad'])
    if objPath != None:
        # mando como referencia todos los atributos de MI instancia (por eso uso currentScopeClass)
        # currentScopeClass es en donde SE INVOCO la funcion
        for attrName in dirProced[currentScopeClass]['obj'][objPath]['attr']:
            dirReal = dirProced[currentScopeClass]['obj'][objPath]['attr'][attrName]['mem']
            # currClass es en DONDE se definio la funcion, por eso de ahi saco la fake mem
            hashRef[dirReal] = dirProced[currClass]['vars'][attrName]['mem']
            hashRefTam[dirReal] = dirProced[currClass]['vars'][attrName]['size']
    

def newInvocacionFuncDeObjNoReturn(objPath, funName):
    if currentScopeClass == 'RedRobin':
        print("desde redrobin invamos")
    else:
        global contParam
        global currentFunction
        global currentClass
        # Valido que el objeto exista
        if objPath in dirProced[currentScopeClass]['obj']:
            currentClass = dirProced[currentScopeClass]['obj'][objPath]['class']
            if funName in dirProced[currentClass]['func']:
                if dirProced[currentClass]['func'][funName]['giveType'] == 'empty':
                    generalInvocationRutine(funName, currentClass, objPath)
                else:
                    terminate("No variable to catch returned value")
            else:
                terminate("Funcition " + funName + " doesn't exists in object " + objPath)
        else:
            terminate("Object " + objPath + " doesn't exists")    

# Llamada desde p_invocacion
def p_smNewFuncNoReturn(p):
    'smNewFuncNoReturn :'
    global contParam
    global currentFunction
    global currentClass
    global giveValue
    funName = p[-2]
    objPath = p[-1]
    if objPath != None:
        newInvocacionFuncDeObjNoReturn(funName, objPath)
    else:
        if funName in dirProced[currentScopeClass]['func']:
            # Funcion invocada debe ser 'void'
            if dirProced[currentScopeClass]['func'][funName]['giveType'] == 'empty':
                generalInvocationRutine(funName, currentScopeClass, None)
                # si la funcion es heredada, de una vez pido por referencia todos los atributos de la clase donde originalmente esta la funcion
                if dirProced[currentScopeClass]['func'][funName]['class'] != currentScopeClass:
                    for varName in dirProced[ dirProced[currentScopeClass]['func'][funName]['class'] ]['vars']:
                        dirReal = dirProced[currentScopeClass]['vars'][varName]['mem']
                        parentClass = dirProced[currentScopeClass]['func'][funName]['class']
                        hashRef[dirReal] = dirProced[parentClass]['vars'][varName]['mem']
                        hashRefTam[dirReal] = dirProced[currentScopeClass]['vars'][varName]['size']

                    for objName in dirProced[ dirProced[currentScopeClass]['func'][funName]['class'] ]['obj']:
                        # recorro todas las variables atomicas del objeto actual
                        objClass = dirProced[ dirProced[currentScopeClass]['func'][funName]['class'] ]['obj'][objName]['class']
                        for attrName in dirProced[objClass]['vars']:
                            dirReal = dirProced[currentScopeClass]['obj'][objName]['attr'][attrName]['mem']
                            hashRef[dirReal] = dirProced[objClass]['vars'][attrName]['mem']
                            hashRefTam[dirReal] = dirProced[currentScopeClass]['obj'][objName]['attr'][attrName]['size']
            else:
                terminate("No variable to catch returned value")
        else:
            terminate("Function " + funName + " not declared")

# Llamada desde p_valor

def newInvocacionFuncDeObj(objPath, funName):
    if currentScopeClass == 'RedRobin':
        print("desde redrobin invamos")
    else:
        global contParam
        global currentFunction
        global currentClass
        # Valido que el objeto exista
        if objPath in dirProced[currentScopeClass]['obj']:
            currentClass = dirProced[currentScopeClass]['obj'][objPath]['class']
            if funName in dirProced[currentClass]['func']:
                generalInvocationRutine(funName, currentClass, objPath)
            else:
                terminate("Funcition " + funName + " doesn't exists in object " + objPath)
        else:
            terminate("Object " + objPath + " doesn't exists")
        
def p_smNewInvocacion(p):
    'smNewInvocacion :'
    global contParam
    global currentFunction
    global currentClass
    funName = p[-2]
    objPath = p[-1]
    if objPath != None:
        newInvocacionFuncDeObj(funName, objPath)
    else:
        if funName in dirProced[currentScopeClass]['func']:
            generalInvocationRutine(funName, currentScopeClass, None)
            # si la funcion es heredada, de una vez pido por referencia todos los atributos de la clase donde originalmente esta la funcion
            if dirProced[currentScopeClass]['func'][funName]['class'] != currentScopeClass:
                for varName in dirProced[ dirProced[currentScopeClass]['func'][funName]['class'] ]['vars']:
                    dirReal = dirProced[currentScopeClass]['vars'][varName]['mem']
                    parentClass = dirProced[currentScopeClass]['func'][funName]['class']
                    hashRef[dirReal] = dirProced[parentClass]['vars'][varName]['mem']
                    hashRefTam[dirReal] = dirProced[currentScopeClass]['vars'][varName]['size']

                for objName in dirProced[ dirProced[currentScopeClass]['func'][funName]['class'] ]['obj']:
                    # recorro todas las variables atomicas del objeto actual
                    objClass = dirProced[ dirProced[currentScopeClass]['func'][funName]['class'] ]['obj'][objName]['class']
                    for attrName in dirProced[objClass]['vars']:
                        dirReal = dirProced[currentScopeClass]['obj'][objName]['attr'][attrName]['mem']
                        hashRef[dirReal] = dirProced[objClass]['vars'][attrName]['mem']
                        hashRefTam[dirReal] = dirProced[currentScopeClass]['obj'][objName]['attr'][attrName]['size']
        else:
            terminate("Function " + funName + " not declared")
        
# Llamada desde p_valorargumentos
def p_smArgumentoRef(p):
    'smArgumentoRef :'
    global contParam
    global currentClass
    if contParam in dirProced[currentClass]['func'][currentFunction]['params']:
        # Obtenemos la direccion del argumento
        argDir = stackDirMem.pop()
        # Obtenemos el nombre declarado del parametro, segun su posicion
        nameVarParam = dirProced[currentClass]['func'][currentFunction]['params'][contParam]['name']
        # Obtenemos la direccion asignada a ese parametro para la generacion de cuadruplos
        # TODO - ver si esto de jalar la direccion de vars se va a quedar así, dado que en teoria se va a eliminar el hash de vars del dir de procedimientos despues de q acabe la funcion
        dirVarParam = dirProced[currentClass]['func'][currentFunction]['vars'][nameVarParam]['mem']
        # Verificamos que el argumento sea del mismo tipo que el parametro
        if cubo.check(getTypeCode(dirVarParam), getTypeCode(argDir), toCode['=']) != 'error':
            createQuadruple(toCode['param'], argDir, -1, dirVarParam)
            hashRef[argDir] = dirVarParam
            hashRefTam[argDir] = dirProced[currentClass]['func'][currentFunction]['vars'][nameVarParam]['size']
            contParam += 1
        else:
            terminate("Error in params of function " + currentFunction)
    else:
        terminate("Wrong number of arguments")
        
# Llamada desde p_valorargumentos
def p_smArgumentoExpresion(p):
    'smArgumentoExpresion :'
    global contParam
    # Verificamos que el numero de argumentos siga dentro del rango
    if contParam in dirProced[currentClass]['func'][currentFunction]['params']:
        # Obtenemos la direccion del argumento
        argDir = stackDirMem.pop()
        # Obtenemos el nombre declarado del parametro, segun su posicion
        nameVarParam = dirProced[currentClass]['func'][currentFunction]['params'][contParam]['name']
        # Obtenemos la direccion asignada a ese parametro para la generacion de cuadruplos
        # TODO - ver si esto de jalar la direccion de vars se va a quedar así, dado que en teoria se va a eliminar el hash de vars del dir de procedimientos despues de q acabe la funcion
        dirVarParam = dirProced[currentClass]['func'][currentFunction]['vars'][nameVarParam]['mem']
        # Verificamos que el argumento sea del mismo tipo que el parametro
        if cubo.check(getTypeCode(dirVarParam), getTypeCode(argDir), toCode['=']) != 'error':
            createQuadruple(toCode['param'], argDir, -1, dirVarParam)
            contParam += 1
        else:
            terminate("Error in params of function " + currentFunction)
    else:
        terminate("Wrong number of arguments")
        
        
# Llamada de p_retorno
def p_smNewGive(p):
    'smNewGive :'
    if currentScopeFunction == "":
        terminate("Give not in a function")
    
    # obtenemos la direccion del valor de retorno
    memReturn = stackDirMem.pop()

    # el tipo de expresion debe coincidir con el tipo de retorno
    funcType = dirProced[currentScopeClass]['func'][currentScopeFunction]['giveType']
    
    if funcType == "empty":
        terminate("unexpeted give in non give function")
    # direccion de la funcion global que almacena el retorno
    dirReturnGlobal = dirProced[currentScopeClass]['func'][currentScopeFunction]['mem']
        
    if toCode[funcType] == getTypeCode(memReturn):
        # creamos el cuadruplo de retorno
        createQuadruple(toCode["give"], memReturn, -1, dirReturnGlobal)
        createQuadruple(toCode["endproc"], -1, -1, -1)
    else:
        terminate("wrong give type")

# Llamada dedes p_valor
def p_smEndInvocacion(p):
    'smEndInvocacion :'
    global contParam
    if len(dirProced[currentClass]['func'][currentFunction]['params']) == contParam - 1:
        createQuadruple(toCode['gosub'], -1, -1, dirProced[currentClass]['func'][currentFunction]['quad'])
        dirRetorno = dirProced[currentClass]['func'][currentFunction]['mem']
        # Actualizamos los valores por referncia
        for real in hashRef:
            createQuadruple(toCode["ref"], hashRef[real], hashRefTam[real], real)
        # creamos el cuadruplo que guarda el valor de retorno
        if dirRetorno != -1:
            returnType = toSymbol[getTypeCode(dirRetorno)]
            newtemp = memConts[memCont[returnType + 'Temp']]
            createQuadruple(toCode['retu'], dirRetorno, -1, newtemp)
            stackDirMem.append(newtemp)
            memConts[memCont[returnType + 'Temp']] += 1
        
    else:
        terminate("wrong number of arguments")
        
# Llamada desde p_argumentosPrint o p_mas_prints
def p_smPrintQuadruple(p):
    'smPrintQuadruple :'
    operandToPrint = stackDirMem.pop()
    createQuadruple(toCode['print'], -1, -1, operandToPrint)

# Llamada desde p_io
def p_smReadQuadruple(p):
    'smReadQuadruple :'
    operandRead = stackDirMem.pop()
    createQuadruple(toCode['read'], -1, -1, operandRead)

# Llamada desde p_invocacion
def p_smQuadToNumber(p):
    'smQuadToNumber :'
    operand = stackDirMem.pop()
    resultType = cubo.check(getTypeCode(operand), toCode['null'], toCode['toNumber'])
    if resultType != 'error':
        resultType += 'Temp'
        stackDirMem.append(memConts[memCont[resultType]])
        createQuadruple(toCode['toNumber'], operand, -1, memConts[memCont[resultType]])
        memConts[memCont[resultType]] += 1
    else:
        terminate("invalid argument")

# Llamada desde p_invocacion
def p_smQuadToReal(p):
    'smQuadToReal :'
    operand = stackDirMem.pop()
    resultType = cubo.check(getTypeCode(operand), toCode['null'], toCode['toReal'])
    if resultType != 'error':
        resultType += 'Temp'
        stackDirMem.append(memConts[memCont[resultType]])
        createQuadruple(toCode['toReal'], operand, -1, memConts[memCont[resultType]])
        memConts[memCont[resultType]] += 1
    else:
        terminate("invalid argument")

# Llamada desde p_invocacion
def p_smQuadToString(p):
    'smQuadToString :'
    operand = stackDirMem.pop()
    resultType = cubo.check(getTypeCode(operand), toCode['null'], toCode['toString'])
    if resultType != 'error':
        resultType += 'Temp'
        stackDirMem.append(memConts[memCont[resultType]])
        createQuadruple(toCode['toString'], operand, -1, memConts[memCont[resultType]])
        memConts[memCont[resultType]] += 1
    else:
        terminate("invalid argument")

# Llamada desde p_declara_arreglo_o_iniciacion
def p_smDeclaredToStack(p):
    'smDeclaredToStack :'
    validateIdSemantics(p[-3], None, None)

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
    memConts[memCont[memType]] += 1
    return memConts[memCont[memType]] - 1
    
# Llamada de p_identificador
def validateIdSemantics(currentIdName, currentObjPath, currentArray):
    # TODO: validar que el tipo de variable concuerde con su declaracion
    # TODO: que exista el nombre, no queire decir que sea una variable
            # puedo tener objeto perro y usar un numero perro, deberia ser error
            # tal vez con arreglar el primer to do sea suficiente
    # answer todo: creo q esto ya esta, falta testear bien
    # Voy a delegar orientado a objetos a otra funcion
    if currentObjPath != None:
        validateObjSemantics(currentIdName, currentObjPath, currentArray)
    else:
        if not existsVar(currentIdName):
            terminate("Variable " + currentIdName + " not declared")
        if existsFunc(currentIdName):
            terminate("Name variable " + currentIdName + " already used by a function")
        # si es arreglo hacer validaciones
        if currentArray == '[':
            arrayRutine(currentIdName, None)
        else:
            # variable valida, insertar a pila
            if currentIdName in dirProced[currentScopeClass]['vars']:
                stackDirMem.append(dirProced[currentScopeClass]['vars'][currentIdName]['mem'])
            elif currentScopeFunction == '' or currentIdName in dirProced[currentScopeClass]['func'][currentScopeFunction]['vars']:
                stackDirMem.append(dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][currentIdName]['mem'])
        
def validateObjSemantics(currentAttrPath, currentIdName, currentArray):
    # TODO: considerar composicion en red robin
    if '.' in currentIdName:
        print("ok")
        terminate("okkk")
    else:
        # Se que currentObjPath tendra solo un objeto "padre"
        # Valido que exista el objeto
        if currentAttrPath in dirProced[currentScopeClass]['obj']:
            # Valido que exista el nombre dentro del objeto
            if currentIdName in dirProced[currentScopeClass]['obj'][currentAttrPath]['attr']:
                if currentArray == '[':
                    arrayRutine(currentIdName, currentAttrPath)
                else:
                    # existe, lo meto a la pila
                    stackDirMem.append(dirProced[currentScopeClass]['obj'][currentAttrPath]['attr'][currentIdName]['mem'])
            else:
                terminate("Attribute " + currentIdName + " not found")
        else:
            terminate("Object " + currentAttrPath + " not found")
            
def newCteBool(newBool):
    if newBool == 'true':
        stackDirMem.append(memConts[memCont['boolCte']] + 1)
    else:
        stackDirMem.append(memConts[memCont['boolCte']])
        
def arrayRutine(currentIdName, currentObjPath):
    # Obtengo la expresion de indexamiento
    indexMem = stackDirMem.pop()
    # Si no es numero, termino
    if getTypeCode(indexMem) != toCode['number']:
        terminate("bad index for array")
    # Declaro variables auxiliares
    limitArray = 0
    typeVarCode = 0
    newTemp = 0
    dirBase = 0
    # busco donde esta declarado el arreglo para obtener datos
    if currentObjPath != None:
        limitArray = dirProced[currentScopeClass]['obj'][currentObjPath]['attr'][currentIdName]['size']
        dirBase = dirProced[currentScopeClass]['obj'][currentObjPath]['attr'][currentIdName]['mem']
    elif currentScopeFunction != "" and currentIdName in dirProced[currentScopeClass]['func'][currentScopeFunction]['vars']:
        limitArray = dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][currentIdName]['size']
        dirBase = dirProced[currentScopeClass]['func'][currentScopeFunction]['vars'][currentIdName]['mem']
    else:
        limitArray = dirProced[currentScopeClass]['vars'][currentIdName]['size']
        dirBase = dirProced[currentScopeClass]['vars'][currentIdName]['mem']

    # genero cuadruplos del arreglo
    typeVarCode = getTypeCode(dirBase)
    newTemp = getMemSpace(toSymbol[typeVarCode], 'Temp', "-")                
    createQuadruple(toCode['ver'], indexMem, 0, int(limitArray) - 1)
    dirBase = int(dirBase)
    if not dirBase in mapCteToDir:
        mapCteToDir[dirBase] = memConts[memCont['numberCte']]
        memConts[memCont['numberCte']] += 1
    createQuadruple(toCode['+'], mapCteToDir[dirBase], indexMem, newTemp)
    stackDirMem.append(newTemp * -1)    
    
    
# creo cuadruplo go to main
createQuadruple(toCode['goto'], -1, -1, -1)    
        