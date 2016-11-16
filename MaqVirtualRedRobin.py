# ------------------------------------------------------------
# MaqVirtualRedRobin.py
#
# David Delgadillo
# Omar Manjarrez
# ------------------------------------------------------------
import sys
from Cuadruplo import *

#Diccionario de valores donde la llave es la direccion y el valor es el 'valor' almacenado en la direccion
memEjecucion = {}

#Lista de cuadruplos
liCuadruplos = []

#Apunta al cuadruplo al que se esta ejecutando
apunCuadruplo = 0

# Diccionarios de rangos de direcciones para cada tipo de variable
memStart = {
    'numberClass': 100,
    'realClass': 1100,
    'stringClass': 2100,
    'boolClass': 3100,
    
    'numberFunc': 4100,
    'realFunc': 5100,
    'stringFunc': 6100,
    'boolFunc': 7100,
    
    'numberTemp': 8100,
    'realTemp': 9100,
    'stringTemp': 10100,
    'boolTemp': 11100,
    
    'numberCte': 12100,
    'realCte': 13100,
    'stringCte': 14100,
    'boolCte': 15100
}

memLimit = {
    'numberClass': 1099,
    'realClass': 2099,
    'stringClass': 3099,
    'boolClass': 4099,
    
    'numberFunc': 5099,
    'realFunc': 6099,
    'stringFunc': 7099,
    'boolFunc': 8099,
    
    'numberTemp': 9099,
    'realTemp': 10099,
    'stringTemp': 11099,
    'boolTemp': 12099,
    
    'numberCte': 13099,
    'realCte': 14099,
    'stringCte': 15099,
    'boolCte': 16099 
}

#Indica si una direccion almacena valor numerico entero
def isNumber(numDireccion):
    if numDireccion >= memStart['numberClass'] and numDireccion <= memLimit['numberClass']:
        return True
    if numDireccion >= memStart['numberFunc'] and numDireccion <= memLimit['numberFunc']:
        return True
    if numDireccion >= memStart['numberTemp'] and numDireccion <= memLimit['numberTemp']:
        return True
    if numDireccion >= memStart['numberCte'] and numDireccion <= memLimit['numberCte']:
        return True
    
    return False

def terminate(message):
    print(message)
    sys.exit()

def suma():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = memEjecucion[operando1]
    valor2 = memEjecucion[operando2]

    memEjecucion[liCuadruplos[apunCuadruplo].r] = valor1 + valor2

def resta():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = memEjecucion[operando1]
    valor2 = memEjecucion[operando2]

    memEjecucion[liCuadruplos[apunCuadruplo].r] = valor1 - valor2

def multiplica():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = memEjecucion[operando1]
    valor2 = memEjecucion[operando2]

    memEjecucion[liCuadruplos[apunCuadruplo].r] = valor1 * valor2

def divide():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = memEjecucion[operando1]
    valor2 = memEjecucion[operando2]

    #Se valida que la division sea valida
    if valor2 == 0:
        terminate("Zero division error\n")

    memEjecucion[liCuadruplos[apunCuadruplo].r] = valor1 / valor2

def asigna():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    valor1 = memEjecucion[operando1]

    #Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
    if isNumber(liCuadruplos[apunCuadruplo].r):
        memEjecucion[liCuadruplos[apunCuadruplo].r] = int(valor1)
    else:
        memEjecucion[liCuadruplos[apunCuadruplo].r] = valor1

def goTo():
    global apunCuadruplo
    destino = liCuadruplos[apunCuadruplo].r
    apunCuadruplo = destino
    fromCode[ liCuadruplos[apunCuadruplo].ope ]()

def imprimir():
    global apunCuadruplo
    if isinstance(memEjecucion[liCuadruplos[apunCuadruplo].r], str):
        print(memEjecucion[liCuadruplos[apunCuadruplo].r][1:-1])
    else:
        # Se verifica si se trata de una variable entera segun la direccion
        if isNumber(liCuadruplos[apunCuadruplo].r):
            print(int(memEjecucion[liCuadruplos[apunCuadruplo].r]))
        else:
            print(memEjecucion[liCuadruplos[apunCuadruplo].r])

#Enumeracion de funciones
fromCode = {
    12 : suma, #+
    13 : resta, #-
    14 : multiplica, #*
    15 : divide, #/
    16 : asigna, #=
#    '>=': 17,
#    '<=': 18,
#    '==': 19,
#    '<>': 20,
#    'or': 21,
#    'and': 22,
#    '(': 23,
#    ')': 24,
    50 : goTo, #goto
#    'gotof': 51,
#    'neg': 52,
#    'era': 53,
#    'gosub': 54,
#    'param': 55,
    56 : imprimir #print
#    'read' : 57,
#    'toNumber' : 58,
#    'toReal' : 59,
#    'toString': 60,
#    'null' : 61
}

# Se pregunta por archivo ejecutable
filename = "probarMaquina_bin.txt"
# filename = input("Ingresa nombre de archivo con condigo objeto de Red Robin: ") 
f = open(filename, 'r')
listaRenglones = f.readlines()

# Se verifica la cantidad de valores constantes a almacenar inicialmente
cantConstantes = int(listaRenglones[0])
for ite in range(1, 1 + cantConstantes):
    separacionConstantes = listaRenglones[ite].split('~')
    #Determinar de que tipo es la constante segun la direccion
    direccion = int(float(separacionConstantes[1][:-1]))
    if direccion <= 13099:
        #Es constante numerica
        valor = int(separacionConstantes[0])
    elif direccion <= 14099:
        #Es cosntante real
        valor = float(separacionConstantes[0])
    elif direccion <= 15099:
        #Es constante string
        valor = separacionConstantes[0]
    elif direccion <= 16099:
        #Es constante string
        if separacionConstantes[0] == 'true':
            valor = True
        else:
            valor = False

    memEjecucion[direccion] = valor

# Se obtiene la cantidad de cuadruplos
cantCuadruplos = int(listaRenglones[cantConstantes + 1])
for ite in range(cantConstantes + 2, cantConstantes + 2 + cantCuadruplos):
    #Se itera para cada cuadruplo
    separaQuadruplos = listaRenglones[ite].split('~')
    liCuadruplos.append(Cuadruplo())
    liCuadruplos[-1].ope = int(separaQuadruplos[1])
    liCuadruplos[-1].op1 = int(float(separaQuadruplos[2]))
    liCuadruplos[-1].op2 = int(float(separaQuadruplos[3]))
    liCuadruplos[-1].r = int(float(separaQuadruplos[4][:-1]))


while apunCuadruplo < cantCuadruplos:
    fromCode[ liCuadruplos[apunCuadruplo].ope ]()
    apunCuadruplo = apunCuadruplo + 1