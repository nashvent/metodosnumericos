import parser

def fun(x):
    return x+10


formula = "sin(x)*10"
code = parser.expr(formula).compile()

from math import sin
x = 10
print (eval(code))