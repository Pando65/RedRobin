# ------------------------------------------------------------
# Cubo.py
#
# David Delgadillo
# Omar Manjarrez
# ------------------------------------------------------------
import numpy
from Enums import *

class Cubo:
    semantica = numpy.zeros((35, 35, 35))
    
    # Variables: number, real, string, bool
    # operadores: +, - , *, /, >=, <=, ==, <>, and, or
    
    def __init__(self):
        self.semantica[toCode['number']][toCode['number']][toCode['+']] = toCode['number']
        self.semantica[toCode['number']][toCode['real']]  [toCode['+']] = toCode['real']
        self.semantica[toCode['number']][toCode['string']][toCode['+']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['+']] = toCode['error']
        self.semantica[toCode['number']][toCode['number']][toCode['-']] = toCode['number']
        self.semantica[toCode['number']][toCode['real']]  [toCode['-']] = toCode['real']
        self.semantica[toCode['number']][toCode['string']][toCode['-']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['-']] = toCode['error']
        self.semantica[toCode['number']][toCode['number']][toCode['*']] = toCode['number']
        self.semantica[toCode['number']][toCode['real']]  [toCode['*']] = toCode['real']
        self.semantica[toCode['number']][toCode['string']][toCode['*']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['*']] = toCode['error']
        self.semantica[toCode['number']][toCode['number']][toCode['/']] = toCode['number']
        self.semantica[toCode['number']][toCode['real']]  [toCode['/']] = toCode['real']
        self.semantica[toCode['number']][toCode['string']][toCode['/']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['/']] = toCode['error']
        self.semantica[toCode['number']][toCode['number']][toCode['>=']] = toCode['bool']
        self.semantica[toCode['number']][toCode['real']]  [toCode['>=']] = toCode['bool']
        self.semantica[toCode['number']][toCode['string']][toCode['>=']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['>=']] = toCode['error']
        self.semantica[toCode['number']][toCode['number']][toCode['<=']] = toCode['bool']
        self.semantica[toCode['number']][toCode['real']]  [toCode['<=']] = toCode['bool']
        self.semantica[toCode['number']][toCode['string']][toCode['<=']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['<=']] = toCode['error']
        self.semantica[toCode['number']][toCode['number']][toCode['==']] = toCode['bool']
        self.semantica[toCode['number']][toCode['real']]  [toCode['==']] = toCode['bool']
        self.semantica[toCode['number']][toCode['string']][toCode['==']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['==']] = toCode['error']
        self.semantica[toCode['number']][toCode['number']][toCode['<>']] = toCode['bool']
        self.semantica[toCode['number']][toCode['real']]  [toCode['<>']] = toCode['bool']
        self.semantica[toCode['number']][toCode['string']][toCode['<>']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['<>']] = toCode['error']
        self.semantica[toCode['number']][toCode['number']][toCode['and']] = toCode['error']
        self.semantica[toCode['number']][toCode['real']]  [toCode['and']] = toCode['error']
        self.semantica[toCode['number']][toCode['string']][toCode['and']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['and']] = toCode['error']
        self.semantica[toCode['number']][toCode['number']][toCode['or']] = toCode['error']
        self.semantica[toCode['number']][toCode['real']]  [toCode['or']] = toCode['error']
        self.semantica[toCode['number']][toCode['string']][toCode['or']] = toCode['error']
        self.semantica[toCode['number']][toCode['bool']]  [toCode['or']] = toCode['error']
        
        self.semantica[toCode['real']][toCode['number']][toCode['+']] = toCode['real']
        self.semantica[toCode['real']][toCode['real']]  [toCode['+']] = toCode['real']
        self.semantica[toCode['real']][toCode['string']][toCode['+']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['+']] = toCode['error']
        self.semantica[toCode['real']][toCode['number']][toCode['-']] = toCode['real']
        self.semantica[toCode['real']][toCode['real']]  [toCode['-']] = toCode['real']
        self.semantica[toCode['real']][toCode['string']][toCode['-']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['-']] = toCode['error']
        self.semantica[toCode['real']][toCode['number']][toCode['*']] = toCode['real']
        self.semantica[toCode['real']][toCode['real']]  [toCode['*']] = toCode['real']
        self.semantica[toCode['real']][toCode['string']][toCode['*']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['*']] = toCode['error']
        self.semantica[toCode['real']][toCode['number']][toCode['/']] = toCode['real']
        self.semantica[toCode['real']][toCode['real']]  [toCode['/']] = toCode['real']
        self.semantica[toCode['real']][toCode['string']][toCode['/']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['/']] = toCode['error']
        self.semantica[toCode['real']][toCode['number']][toCode['>=']] = toCode['bool']
        self.semantica[toCode['real']][toCode['real']]  [toCode['>=']] = toCode['bool']
        self.semantica[toCode['real']][toCode['string']][toCode['>=']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['>=']] = toCode['error']
        self.semantica[toCode['real']][toCode['number']][toCode['<=']] = toCode['bool']
        self.semantica[toCode['real']][toCode['real']]  [toCode['<=']] = toCode['bool']
        self.semantica[toCode['real']][toCode['string']][toCode['<=']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['<=']] = toCode['error']
        self.semantica[toCode['real']][toCode['number']][toCode['==']] = toCode['bool']
        self.semantica[toCode['real']][toCode['real']]  [toCode['==']] = toCode['bool']
        self.semantica[toCode['real']][toCode['string']][toCode['==']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['==']] = toCode['error']
        self.semantica[toCode['real']][toCode['number']][toCode['<>']] = toCode['bool']
        self.semantica[toCode['real']][toCode['real']]  [toCode['<>']] = toCode['bool']
        self.semantica[toCode['real']][toCode['string']][toCode['<>']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['<>']] = toCode['error']
        self.semantica[toCode['real']][toCode['number']][toCode['and']] = toCode['error']
        self.semantica[toCode['real']][toCode['real']]  [toCode['and']] = toCode['error']
        self.semantica[toCode['real']][toCode['string']][toCode['and']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['and']] = toCode['error']
        self.semantica[toCode['real']][toCode['number']][toCode['or']] = toCode['error']
        self.semantica[toCode['real']][toCode['real']]  [toCode['or']] = toCode['error']
        self.semantica[toCode['real']][toCode['string']][toCode['or']] = toCode['error']
        self.semantica[toCode['real']][toCode['bool']]  [toCode['or']] = toCode['error']

        self.semantica[toCode['string']][toCode['number']][toCode['+']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['+']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['+']] = toCode['string']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['+']] = toCode['error']
        self.semantica[toCode['string']][toCode['number']][toCode['-']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['-']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['-']] = toCode['string']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['-']] = toCode['error']
        self.semantica[toCode['string']][toCode['number']][toCode['*']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['*']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['*']] = toCode['string']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['*']] = toCode['error']
        self.semantica[toCode['string']][toCode['number']][toCode['/']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['/']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['/']] = toCode['string']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['/']] = toCode['error']
        self.semantica[toCode['string']][toCode['number']][toCode['>=']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['>=']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['>=']] = toCode['bool']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['>=']] = toCode['error']
        self.semantica[toCode['string']][toCode['number']][toCode['<=']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['<=']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['<=']] = toCode['bool']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['<=']] = toCode['error']
        self.semantica[toCode['string']][toCode['number']][toCode['==']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['==']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['==']] = toCode['bool']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['==']] = toCode['error']
        self.semantica[toCode['string']][toCode['number']][toCode['<>']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['<>']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['<>']] = toCode['string']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['<>']] = toCode['error']
        self.semantica[toCode['string']][toCode['number']][toCode['and']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['and']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['and']] = toCode['error']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['and']] = toCode['error']
        self.semantica[toCode['string']][toCode['number']][toCode['or']] = toCode['error']
        self.semantica[toCode['string']][toCode['real']]  [toCode['or']] = toCode['error']
        self.semantica[toCode['string']][toCode['string']][toCode['or']] = toCode['error']
        self.semantica[toCode['string']][toCode['bool']]  [toCode['or']] = toCode['error']
        
        self.semantica[toCode['bool']][toCode['number']][toCode['+']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['+']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['+']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['+']] = toCode['error']
        self.semantica[toCode['bool']][toCode['number']][toCode['-']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['-']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['-']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['-']] = toCode['error']
        self.semantica[toCode['bool']][toCode['number']][toCode['*']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['*']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['*']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['*']] = toCode['error']
        self.semantica[toCode['bool']][toCode['number']][toCode['/']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['/']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['/']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['/']] = toCode['error']
        self.semantica[toCode['bool']][toCode['number']][toCode['>=']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['>=']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['>=']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['>=']] = toCode['bool']
        self.semantica[toCode['bool']][toCode['number']][toCode['<=']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['<=']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['<=']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['<=']] = toCode['bool']
        self.semantica[toCode['bool']][toCode['number']][toCode['==']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['==']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['==']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['==']] = toCode['bool']
        self.semantica[toCode['bool']][toCode['number']][toCode['<>']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['<>']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['<>']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['<>']] = toCode['bool']
        self.semantica[toCode['bool']][toCode['number']][toCode['and']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['and']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['and']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['and']] = toCode['bool']
        self.semantica[toCode['bool']][toCode['number']][toCode['or']] = toCode['error']
        self.semantica[toCode['bool']][toCode['real']]  [toCode['or']] = toCode['error']
        self.semantica[toCode['bool']][toCode['string']][toCode['or']] = toCode['error']
        self.semantica[toCode['bool']][toCode['bool']]  [toCode['or']] = toCode['bool']
        
    def check(self, op1, op2, ope):
        return toSymbol[self.semantica[op1][op2][ope]]


