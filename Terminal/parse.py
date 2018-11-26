from math import *
import metodos as mt
import numpy as np  
import matplotlib.pyplot as plt 
import matrix 
from mparse import SimpleParse
import matplotlib 
matplotlib.interactive(False)

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
    error=0.0001
    decimal=4
    def addVariable(self,vname,vval):
        self.variables[vname]=vval
    def setEc(self,ec):        
        self.ecuation=ec
    
    def evaluate(self):    
        if(checkExpression(self.ecuation)):
            self.ecuation=changeSyntax(self.ecuation)
            #print(self.ecuation)
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
        lt["plot2d"]=self.graph
        lt["polyroot"]=mt.polyroot
        

    def addVarFromList(self,lista):
        self.variables=lista


    #### Zona de metodos

    def froot(self,fn,a,b,all,n=0):
        
        if(all==False):
            if n==0:
                resp=mt.biseccion(a,b,fn,self.error)
            elif n==1:
                resp=mt.falsapos(a,b,fn,self.error)
            elif n==2:
                resp=mt.secante(a,fn,self.error)
            else:
                return "desconocido"
        else:
            if n==0:
                resp=mt.tbiseccion(fn,a,b,self.error)
            elif n==1:
                resp=mt.tfalsapos(fn,a,b,self.error)
            elif n==2:
                resp=mt.tsecante(fn,a,b,self.error)
            else:
                return "desconocido"
        
        if(type(resp).__name__=="float"):
            nresp=[resp]
        else:
            nresp=resp
        nlresp=[]
        for i in range(len(nresp)):
            nlresp.append([nresp[i],0])
        self.graphList([fn],nlresp,a,b)
        return resp


    def graph(self,formula,i,f,ncolor):
        prs=SimpleParse()
        x = np.linspace(i,f,100)
        prs.setEc(formula)
        y=getY(formula,x) 
        plt.plot(x, y,color=ncolor)
        plt.axis([i, f, i+1, f])
        #plt.show(block=True)
        plt.show()

    def graphList(self,fList,pList,pi,pf):
        pi=pi-2
        pf=pf+2
        xList = np.linspace(pi,pf,100)
        for i in range(len(fList)):
            yList=getY(fList[i],xList)
            plt.plot(xList, yList)
        for p in pList:
            plt.plot(p[0],p[1],'ro')
        plt.axis([pi, pf, pi, pf])
        plt.show(block=True) 



def getY(formula,x):
    prs=SimpleParse()
    y=[]
    prs.setEc(formula)
    for i in x:
        prs.addVariable("x",i)
        yT=prs.evaluate()
        y.append(yT)
    return y
