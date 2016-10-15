# ------------------------------------------------------------
# Cubo.py
#
# David Delgadillo
# Omar Manjarrez
# ------------------------------------------------------------
import numpy
from Enums import *

class Cubo:
    semantica = numpy.zeros((45, 45, 45))
    
    # Variables: number, real, string, bool
    # operadores: +, - , *, /, >=, <=, ==, <>, 
    
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

    def check(self, op1, op2, ope):
        code_op1 = toCode[op1]
        code_op2 = toCode[op2]
        code_ope = toCode[ope]
        return toSymbol[self.semantica[code_op1][code_op2][code_ope]]
    
x = Cubo()

print(x.check('number', 'number', '*') )
        

