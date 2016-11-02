toCode = {
    'error': 0,
    'number': 1,
    'real': 2,
    'bool': 3,
    'string': 4,
    '+': 12,
    '-': 13,
    '*': 14,
    '/': 15,
    '=': 16,
    '>=': 17,
    '<=': 18,
    '==': 19,
    '<>': 20,
    'or': 21,
    'and': 22,
    '(': 23,
    ')': 24,
    'goto': 50,
    'gotof': 51,
    'neg': 52,
    'era': 53,
    'gosub': 54,
    'param': 55,
    'print': 56
}

toSymbol = {
    0: 'error',
    1: 'number',
    2: 'real',
    3: 'bool',
    4: 'string'
}

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

memCont = {
    'numberClass': 0,
    'realClass': 1,
    'stringClass': 2,
    'boolClass': 3,
    
    'numberFunc': 4,
    'realFunc': 5,
    'stringFunc': 6,
    'boolFunc': 7,
    
    'numberTemp': 8,
    'realTemp': 9,
    'stringTemp': 10,
    'boolTemp': 11,
    
    'numberCte': 12,
    'realCte': 13,
    'stringCte': 14,
    'boolCte': 15
}