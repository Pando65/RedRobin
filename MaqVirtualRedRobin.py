# ------------------------------------------------------------
# MaqVirtualRedRobin.py
#
# David Delgadillo
# Omar Manjarrez
# ------------------------------------------------------------
import sys
from Cuadruplo import *

#Diccionario de valores globales donde la llave es la direccion y el valor es el 'valor' almacenado en la direccion
memEjecucion = {}

#Pila de diccionarios con memoria local a las funciones
pilaMemoriaLocal = [{}]

#Lista de cuadruplos
liCuadruplos = []

#Pila de apuntadores de cuadruplos
pilaApunCuadruplo = []

#Apunta al cuadruplo al que se esta ejecutando
apunCuadruplo = 0

#Nivel alcance local
nivelAlcance = 0

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
    #Se verifica si es una direccion indirecta
    if numDireccion < -1:
        #Se obtiene la verdadera direccion invocando a findValueInMemory que identifica en que estructura esta segun el absoluto de la direccion
        numDireccion = findValueInMemory(abs(numDireccion), nivelAlcance)

    if numDireccion >= memStart['numberClass'] and numDireccion <= memLimit['numberClass']:
        return True
    if numDireccion >= memStart['numberFunc'] and numDireccion <= memLimit['numberFunc']:
        return True
    if numDireccion >= memStart['numberTemp'] and numDireccion <= memLimit['numberTemp']:
        return True
    if numDireccion >= memStart['numberCte'] and numDireccion <= memLimit['numberCte']:
        return True
    
    return False

#Recibe una direccion y nivel de alcance para retornar el valor de la estructura pertinente segun la misma direccion: memoria global o local
def findValueInMemory(numDireccion, alcanceFuncion):
    #Se verifica si es una direccion indirecta
    if numDireccion < -1:
        #Se obtiene la verdadera direccion invocandose a si mismo
        numDireccion = findValueInMemory(abs(numDireccion), alcanceFuncion)

    if numDireccion < memStart['numberFunc'] or numDireccion > memLimit['boolTemp']:
        #Se trata de una direccion global
        return memEjecucion[numDireccion]
    else:
        #Se trata de una direccion local o temporal
        return pilaMemoriaLocal[alcanceFuncion][numDireccion]

#Recibe una direccion y determina si es de tipo global o local
def isGlobal(numDireccion):
    #Se verifica si es una direccion indirecta
    if numDireccion < -1:
        #Se obtiene la verdadera direccion invocando a findValueInMemory que identifica en que estructura esta segun el absoluto de la direccion
        numDireccion = findValueInMemory(abs(numDireccion), nivelAlcance)

    if numDireccion < memStart['numberFunc'] or numDireccion > memLimit['boolTemp']:
        #Se trata de una direccion global
        return True
    else:
        #Se trata de una direccion local o temporal
        return False

#Retorna la direccion correcta al que se le debe almacenar un valor
def findAbsoluteAddress(numDireccion, alcanceFuncion):
    #Se verifica si es una direccion indirecta
    if numDireccion < -1:
        #Se obtiene el valor de la verdadera direccion que almacena esta indirecta
        return findValueInMemory(abs(numDireccion), alcanceFuncion)
    else:
        return numDireccion

def terminate(message):
    print(message)
    sys.exit()

def suma():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 + valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 + valor2

def resta():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 - valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 - valor2

def multiplica():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 * valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 * valor2

def divide():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se valida que la division sea valida
    if valor2 == 0:
        terminate("Zero division error\n")

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 / valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 / valor2

def asigna():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    valor1 = findValueInMemory(operando1, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
        if isNumber(direccionAlmacenar):
            memEjecucion[direccionAlmacenar] = int(valor1)
        else:
            memEjecucion[direccionAlmacenar] = valor1
    else:
        #Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
        if isNumber(direccionAlmacenar):
            pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = int(valor1)
        else:
            pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1

def mayoroigual():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 >= valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 >= valor2

def menoroigual():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 <= valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 <= valor2

def esigual():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 == valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 == valor2

def esdiferente():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 != valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 != valor2

def condicionalor():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 or valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 or valor2

def condicionaland():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    operando2 = liCuadruplos[apunCuadruplo].op2

    valor1 = findValueInMemory(operando1, nivelAlcance)
    valor2 = findValueInMemory(operando2, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se almacena valor global dentro de la estructura que maneja almacenamiento global
        memEjecucion[direccionAlmacenar] = valor1 and valor2
    else:
        #Se almacena valor local dentro de la estructura que maneja almacenamiento local
        pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1 and valor2

def goTo():
    global apunCuadruplo
    destino = liCuadruplos[apunCuadruplo].r
    apunCuadruplo = destino
    fromCode[ liCuadruplos[apunCuadruplo].ope ]()

def goTof():
    global apunCuadruplo
    
    operando1 = liCuadruplos[apunCuadruplo].op1

    valor1 = findValueInMemory(operando1, nivelAlcance)

    if not valor1:
        destino = liCuadruplos[apunCuadruplo].r
        apunCuadruplo = destino
        fromCode[ liCuadruplos[apunCuadruplo].ope ]()

def era():
    global pilaMemoriaLocal

    # Se le agrega una nuevo entorno de variables locales para la funcion a ser invocada
    pilaMemoriaLocal.append({})

def irASubrutina():
    global apunCuadruplo
    global pilaApunCuadruplo
    global nivelAlcance

    # Se mete el a la pila de apuntadores a cuadruplos el numero del siguiente cuadruplo que se dormira
    pilaApunCuadruplo.append(apunCuadruplo + 1)
    # Se obtiene el numero de cuadruplo destino y se actualiza el mismo
    destino = liCuadruplos[apunCuadruplo].r
    apunCuadruplo = destino

    # Se incrementa el nuevo nivel de entorno de valores locales a uno mayor
    nivelAlcance = nivelAlcance + 1

    fromCode[ liCuadruplos[apunCuadruplo].ope ]()

def parametro():
    global apunCuadruplo

    operando1 = liCuadruplos[apunCuadruplo].op1
    valor1 = findValueInMemory(operando1, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    # Se inicializa valor de la variable local en la funcion a ejecutarse
    pilaMemoriaLocal[nivelAlcance + 1][direccionAlmacenar] = valor1

def imprimir():
    global apunCuadruplo

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)
    valor = findValueInMemory(direccionAlmacenar, nivelAlcance)

    #Si el valor es un string se imprime con este formato
    if isinstance(valor, str):
        print(valor[1:-1])
    else:
        # Se verifica si se trata de una variable entera segun la direccion
        if isNumber(direccionAlmacenar):
            print(int(valor))
        else:
            #No es una variable entera
            print(valor)

def give():
    operando1 = liCuadruplos[apunCuadruplo].op1
    valor1 = findValueInMemory(operando1, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    #Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
    if isNumber(direccionAlmacenar):
        memEjecucion[direccionAlmacenar] = int(valor1)
    else:
        memEjecucion[direccionAlmacenar] = valor1

def terminaProcedimiento():
    global apunCuadruplo
    global pilaApunCuadruplo
    global pilaMemoriaLocal
    global nivelAlcance

    #Se obtiene el apuntador a cuadruplo que se dejo dormido donde se invoco la rutina que acaba de terminar
    apunCuadruplo = pilaApunCuadruplo.pop()
    #Se decrementa el nivel de entorno de los valores locales pero sin destruir el de la funcion recien terminada
    nivelAlcance = nivelAlcance - 1

    # Si el cuadruplo al que se regresa no tiene operaciones de referencia
    if liCuadruplos[apunCuadruplo].ope != 65:
        #Se 'destruye' toda la memoria de entorno local de la funcion que recien acaba de terminar pues ya no se requiere
        pilaMemoriaLocal.pop()
    
    fromCode[ liCuadruplos[apunCuadruplo].ope ]()

def terminaPrograma():
    #Nothing to do
    terminate("")

def referencia():
    global pilaMemoriaLocal

    operando1 = liCuadruplos[apunCuadruplo].op1
    #Se busca valor en el entorno de memoria local que se acaba de dejar de la funcion que se termino de invocar
    valor1 = findValueInMemory(operando1, nivelAlcance + 1)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta en el entorno local actual
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
        if isNumber(direccionAlmacenar):
            memEjecucion[direccionAlmacenar] = int(valor1)
        else:
            memEjecucion[direccionAlmacenar] = valor1
    else:
        #Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
        if isNumber(direccionAlmacenar):
            pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = int(valor1)
        else:
            pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1

    #Se verifica si el siguiente NO es un cuadruplo de referencia
    if liCuadruplos[apunCuadruplo + 1].ope != 65:
        #Se 'destruye' toda la memoria de entorno local de la funcion que recien acaba de terminar pues ya no se requiere
        pilaMemoriaLocal.pop()

def asignaRetorno():
    operando1 = liCuadruplos[apunCuadruplo].op1
    valor1 = findValueInMemory(operando1, nivelAlcance)

    #Se obtiene la direccion absoluta en caso de que sea una direccion indirecta
    direccionAlmacenar = findAbsoluteAddress(liCuadruplos[apunCuadruplo].r, nivelAlcance)

    if isGlobal(direccionAlmacenar):
        #Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
        if isNumber(direccionAlmacenar):
            memEjecucion[direccionAlmacenar] = int(valor1)
        else:
            memEjecucion[direccionAlmacenar] = valor1
    else:
        #Se checa si la direccion a asignar valor es entera para almacenar solo la parte entera
        if isNumber(direccionAlmacenar):
            pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = int(valor1)
        else:
            pilaMemoriaLocal[nivelAlcance][direccionAlmacenar] = valor1

#Enumeracion de funciones
fromCode = {
    12 : suma, #+
    13 : resta, #-
    14 : multiplica, #*
    15 : divide, #/
    16 : asigna, #=
    17 : mayoroigual, #>=
    18 : menoroigual, #<=
    19 : esigual, #==
    20 : esdiferente, #<>
    21 : condicionalor, #or
    22 : condicionaland, #and
#    '(': 23,
#    ')': 24,
    50 : goTo, #goto
    51 : goTof, #gotof
#    52 : negativo, #neg
    53 : era, #era
    54 : irASubrutina, #gosub
    55 : parametro, #param
    56 : imprimir, #print
#    'read' : 57,
#    'toNumber' : 58,
#    'toReal' : 59,
#    'toString': 60,
#    'null' : 61,
    62 : give, #'give': 62,
    63 : terminaProcedimiento, #endproc
    64 : terminaPrograma, #endprogram
    65 : referencia, #ref
#    66 : verificarLimites, #ver
    67 : asignaRetorno #retu
}

# Se pregunta por archivo ejecutable
filename = "p1_bin.txt"
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
        #Es constante boolean
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