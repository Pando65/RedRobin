import numpy
from Enums import *

########### DIRECCIONES VIRTUALES ###########

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