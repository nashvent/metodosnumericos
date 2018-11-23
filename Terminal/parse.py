from math import *
import metodos as mt


def checkExpression(expr):
    if(expr.isspace() or expr==''):
        return False
    return True

def changeSyntax(expr):
    expr=expr.replace("^","**")
    return expr 


class ParseConsola:
    variables={}
    ecuation=""
    error="0.00001"
    decimal="7"
    def addVariable(self,vname,vval):
        self.variables[vname]=vval
    def setEc(self,ec):        
        self.ecuation=ec
    
    def evaluate(self):    
        if(checkExpression(self.ecuation)):
            self.ecuation=changeSyntax(self.ecuation)
            print(self.ecuation)
            var=self.variables.copy()
            self.addStaticVar(var)         
            try:
                return eval(self.ecuation,var)
            except SyntaxError:
                return "Error"
            
    def addStaticVar(self,lt):
        lt["error"]=self.error
        lt["decimal"]=self.decimal
        lt["root"]=self.froot

    def addVarFromList(self,lista):
        self.variables=lista


    #### Zona de metodos

    def froot(self,fn,a,b,all,n=0):
        if(all==False):
            if n==0:
                return mt.biseccion(a,b,fn,self.error)
            elif n==1:
                return "Falsapos"
            elif n==2:
                return "sec"
            else:
                return "desconocido"
        else:
            if n==0:
                return "bissec"
            elif n==1:
                return "Falsapos"
            elif n==2:
                return "sec"
            else:
                return "desconocido"




