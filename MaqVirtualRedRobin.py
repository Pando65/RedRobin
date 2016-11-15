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

    memEjecucion[liCuadruplos[apunCuadruplo].r] = valor1

def goTo():
    global apunCuadruplo
    destino = liCuadruplos[apunCuadruplo].r
    apunCuadruplo = destino
    fromCode[ liCuadruplos[apunCuadruplo].ope ]()

def imprimir():
    global apunCuadruplo
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