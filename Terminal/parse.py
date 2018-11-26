from math import *
import metodos as mt
import numpy as np  
import matplotlib.pyplot as plt 
import matrix 
from mparse import SimpleParse
import matplotlib 
from matplotlib.patches import Polygon

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
    nintegral=10
    hedo=0.2
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
        lt["polynomial"]=mt.lagrange
        lt["senl"]=self.senl
        lt["integral"]=self.fintegral
        lt["area"]=self.area
        lt["area2"]=self.area2
        lt["edo"]=self.edo
        lt["intersection"]=self.fintersec
        #lt["grapharea"]=self.graphArea
        

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
        y=getY(fn,nresp)
        for i in range(len(nresp)):
            nlresp.append([nresp[i],y[i]])

        self.graphList([fn],nlresp,a,b)
        return resp


    def graph(self,formula,i,f,ncolor):
        prs=SimpleParse()
        x = np.linspace(i,f,100)
        prs.setEc(formula)
        y=getY(formula,x) 
        plt.plot(x, y,color=ncolor)
        plt.axis([i, f, min(y), max(y)])
        #plt.show(block=True)
        plt.show()


    def graphPoints(self,x,y):
        plt.plot(x, y)
        plt.axis([min(x),max(x), min(y), max(y)])
        #plt.show(block=True)
        plt.show()

    def graphList(self,fList,pList,pi,pf):
        pi=pi-2
        pf=pf+2
        xList = np.linspace(pi,pf,100)
        maxy=0
        miny=0
        for i in range(len(fList)):
            yList=getY(fList[i],xList)
            plt.plot(xList, yList)
            maxy=max(yList)
            miny=min(yList)

        
        for p in pList:
            plt.plot(p[0],p[1],'ro')
        plt.axis([pi, pf, miny, maxy])
        #Process(None, plt.show).start()
        plt.show(block=True) 

    def senl(self,lvar,lfunc,lx):
        return mt.newtonRaphsonG(lvar,lfunc,lx,self.error)

    def fintegral(self,func,a,b,op=0):
        if(op==0):
            resp=mt.trapecio(func,a,b,self.nintegral)
        elif(op==1):
            resp=mt.simpson1_3(func,a,b,self.nintegral)
        elif(op==2):
            resp=mt.simpson3_8(func,a,b)
        else:
            resp="desconocido"
        return resp

    def area(self,func1,func2,a,b):
        #resp=mt.simpson1_3(func1,a,b,self.nintegral)
        pntInter=mt.interseccion(func1,func2,a,b,self.error)
        print(pntInter)
        xprev=a
        areaT=0
        for i in range(len(pntInter)):
            inte1=mt.simpson1_3(func1,xprev,pntInter[i][0],self.nintegral)
            inte2=mt.simpson1_3(func2,xprev,pntInter[i][0],self.nintegral)
            if(inte1<inte2):
                areaT+=abs(inte2-inte1)
            else:
                areaT+=abs(inte1-inte2)
            xprev=pntInter[i][0]

        inte1=mt.simpson1_3(func1,xprev,b,self.nintegral)
        inte2=mt.simpson1_3(func2,xprev,b,self.nintegral)
        if(inte1<inte2):
            areaT+=abs(inte2-inte1)
        else:
            areaT+=abs(inte1-inte2)
        self.graphArea([func1,func2],a,b)
        return areaT
    
    def area2(self,func1,a,b):
        #resp=mt.simpson1_3(func1,a,b,self.nintegral)
        pntInter=mt.tsecante(func1,a,b,self.error)
        xprev=a
        areaT=0
    
        for i in range(len(pntInter)):
            inte1=mt.simpson1_3(func1,xprev,pntInter[i],self.nintegral)
            areaT+=abs(inte1)
            xprev=pntInter[i]

        inte1=mt.simpson1_3(func1,xprev,b,self.nintegral)
        areaT+=abs(inte1)
        self.graphArea([func1],a,b)
        return areaT

    def graphArea(self,formula,i,f):
        x = np.linspace(i-1,f+1,100)
        a=i
        b=f
        fig, ax = plt.subplots()
        for i in range(len(formula)):
            y=getY(formula[i],x) 
            plt.plot(x, y, 'r', linewidth=2)
            plt.ylim(ymin=0)
            plt.axis([i-1, f+1  , min(y), max(y)])

            ix = np.linspace(a, b)
            iy = getY(formula[i],ix)
            verts = [(a, 0), *zip(ix, iy), (b, 0)]
            poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
            ax.add_patch(poly)

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')

        ax.set_xticks((a, b))
        ax.set_xticklabels(('$a$', '$b$'))
        ax.set_yticks([])

        plt.show(block=True)

    def edo(self,df,xo,yo,xn,n=0):
        if(n==0):
            resp=mt.eulerSimple(df,xo,yo,self.hedo,xn)
        elif(n==1):
            resp=mt.eulerHeun(df,xo,yo,self.hedo,xn)
        elif(n==2):
            resp=mt.rungeKutta(df,xo,yo,self.hedo,xn)
        elif(n==3):
            resp=mt.dormandPrince(df,xo,yo,self.hedo,xn)
        else:
            return "desconocido"
        self.graphPoints(resp[0],resp[1])
        return resp

    def fintersec(self,fn1,fn2,pi,pf,color1,color2):
        resp=mt.interseccion(fn1,fn2,pi,pf,self.error)
        self.graphList([fn1,fn2],resp,pi,pf)
        return resp


def getY(formula,x):
    prs=SimpleParse()
    y=[]
    prs.setEc(formula)
    for i in x:
        prs.addVariable("x",i)
        yT=prs.evaluate()
        y.append(yT)
    return y
