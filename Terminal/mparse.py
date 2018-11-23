from math import *
def ln(x):
    return log(x)
def sen(x):
    return sin(x)

class SimpleParse:
    variables={}
    ecuation=""
    def addVariable(self,vname,vval):
        self.variables[vname]=vval
    def setEc(self,ec):        
        self.ecuation=ec
    
    def evaluate(self):    
        var=self.variables.copy()
        try:
            return eval(self.ecuation,var)
        except SyntaxError:
            return "Error"

    def __init__(self):
        self.variables["e"]=e
        self.variables["ln"]=ln
        self.variables["pi"]=pi
        self.variables["exp"]=exp
        
    def addVarFromList(self,lista):
        self.variables=lista
