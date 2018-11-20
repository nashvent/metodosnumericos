import parser
from math import *
import numpy as np  
import matplotlib.pyplot as plt 
import matrix 
from parse import Parse
plt.style.use('seaborn-whitegrid')
def ln(x):
    return log(x)
def sen(x):
    return sin(x)

def bolzano(fn,a,b):

    prs=Parse()
    prs.setEc(fn)
    prs.addVariable("x",a)
    evA=prs.evaluate()
    prs.addVariable("x",b)
    evB=prs.evaluate()
    print("bolzano val",evA,evB)
    if((evA*evB)<0):
        return True
    return False

def biseccion(a,b,fn,error):
    errorTemp=0
    maxIt=100
    cont=0
    code = parser.expr(fn).compile()    
    xAnt=0
    x=0.0
    historial=[]    
    while(cont<maxIt):  
        x=a
        ra=eval(code)
        x=(a+b)/2 
        rx=eval(code)
        if(cont>=1):
            errorTemp=abs(x-xAnt)
            if(errorTemp<error):
                break        
        historial.append([a,b,x,errorTemp])
        if((rx*ra)<0):
            b=x
        else:
            a=x
        xAnt=x
        cont+=1
    return xAnt,historial

def falsapos(a,b,fn,error):
    errorTemp=1000000
    maxIt=100
    cont=0
    code = parser.expr(fn).compile()    
    xAnt=0
    x=0
    historial=[]
    while(cont<maxIt):
        x=a
        ra=eval(code)
        x=b
        rb=eval(code)
        xn=a-(ra*(b-a)/(rb-ra)) 
        x=xn
        rx=eval(code)
        if(cont>=1):
            errorTemp=abs(x-xAnt)
            if(errorTemp<error):
                break        
        historial.append([a,b,x,errorTemp])


        if((rx*ra)<0):
            b=x
        else:
            a=x
        xAnt=x
        cont+=1
    return x,historial

def puntofijo(xn,fn,error):
    maxIt=100
    historial=[]
    xr=xn
    prs=Parse()
    fn=fn+"+x"
    prs.setEc(fn)
    historial.append([xn,0])
    for i in range(maxIt):
        xAnt=xr
        prs.addVariable("x",xr)
        xr=prs.evaluate()
        print("xr",xr)
        errorTemp=abs(xAnt-xr)
        historial.append([xr,errorTemp])
        if(errorTemp<error):
            break
    return xr,historial

def newton(xn,fn,dfn,error):
    errorTemp=0.0
    maxIt=100
    cont=0
    Fnx = parser.expr(fn).compile()
    DFnx = parser.expr(dfn).compile()    
    xAnt=xn
    x=xn
    historial=[]
    historial.append([x,0.0])
    while( maxIt>cont):
        xAnt=x
        resfn=eval(Fnx)
        resdnf=eval(DFnx)
        x=x-(resfn/resdnf)
        errorTemp=abs(xAnt-x)    
        historial.append([x,errorTemp])
        if(errorTemp<error):
            break      
        cont+=1
    return x,historial


def secante(xn,fn,error):
    errorTemp=1000000
    maxIt=100
    cont=0
    h=error/10
    xAnt=xn
    prs=Parse()
    prs.setEc(fn)
    historial=[]
    historial.append([xn,0.0])
    while(errorTemp>error and maxIt>cont):
        prs.addVariable("x",xAnt)
        resfn=prs.evaluate()
        prs.addVariable("x",xAnt+h)
        resfxh=prs.evaluate()
        prs.addVariable("x",xAnt-h)
        resfx_h=prs.evaluate()
        if((resfxh-resfx_h)==0):
            print("division entre zero")
            break
        x=xAnt-((2*h*resfn)/(resfxh-resfx_h))
        errorTemp=abs(xAnt-x)
        historial.append([xAnt,errorTemp])
        xAnt=x
        if(errorTemp<error):
            break  
        cont+=1
    return x,historial



def lagrange(xLista,yLista,punto):
    prodStr=""
    for i in range (len(yLista)):
        prodStr=prodStr+str(yLista[i])+"*"
        cont=0
        for j in range (len(xLista)): 
            if(i!=j):
               prodStr=prodStr+"((x-"+str(xLista[j])+")"
               tempDiv=xLista[i]-xLista[j]
               prodStr=prodStr+"/("+str(tempDiv)+"))"
               cont=cont+1
               if(cont+1<len(xLista)):
                   prodStr=prodStr+"*"
        if(i+1<len(yLista)):
            prodStr+="+"
    x=punto
    code = parser.expr(prodStr).compile()
    res= (eval(code))
    return prodStr,res 

def getY(formula,x):
    prs=Parse()
    y=[]
    prs.setEc(formula)
    for i in x:
        prs.addVariable("x",i)
        yT=prs.evaluate()
        #print(yT)
        y.append(yT)
    return y

#graph(resp[0],range(0,10))
def graph(formula,i,f):
    prs=Parse()
    x = np.linspace(i,f,100)
    prs.setEc(formula)
    y=getY(formula,x) 
    plt.plot(x, y)
    plt.axis([i, f, i+1, f])
    plt.show()

def imagenNR(LFn,Lx):
    tparse=Parse()
    LFxn=[]
    for i in range(len(LFn)):
        tparse.setEc(LFn[i])
        tparse.addVarFromList(Lx)
        LFxn.append(tparse.evaluate())
    return LFxn

def jacobiana(LFn,Lx,err):
    tparse=Parse()
    Jmatrix=[]
    h=err/10
    TLx=[]
    for i in range(len(LFn)):
        mTemp=[]
        for j in range(len(Lx)):
            TLx=list(Lx)
            TLx[j]=Lx[j]+h
            tparse.setEc(LFn[i])
            tparse.addVarFromList(TLx)
            rH=tparse.evaluate()
            TLx=list(Lx)
            TLx[j]=Lx[j]-h
            tparse.addVarFromList(TLx)
            r_H=tparse.evaluate()
            DR=(rH-r_H)/(2*(h*100))
            mTemp.append(DR)       
        Jmatrix.append(mTemp) 
    
    result=Jmatrix
    return result
def errorNR(Lx,TLx):
    err=0
    i=0
    for i in range(len(Lx)):
        tmp=float(float(Lx[i])-float(TLx[i]))
        err+=pow(tmp,2)
    return sqrt(err)

def newtonRaphsonG(LFn,Lx,error):
    print("NewtonRG")
    maxIt=10
    tparse=Parse()
    TLx=[]
    errorAnt=0
    errorTemp=0
    contErr=0
    LxAnt=[]
    for i in range(maxIt):
        TLx=Lx
        jaco=jacobiana(LFn,Lx,error)
        LFxn=imagenNR(LFn,Lx)    
        respTemp=matrix.multVectorMatrix(jaco,LFxn)
        LxAnt=Lx
        Lx=matrix.restaArray(Lx,respTemp)
        print("Lx",Lx)
        errorAnt=errorTemp
        errorTemp=errorNR(TLx,Lx)
        print("error",errorTemp)
        if(abs(errorAnt-errorTemp)>1):
            print("Divergente")
            return LxAnt
        if(errorTemp<error):
            break       
    
    #graphList(LFn,[],-2,2)

    return Lx

def selectMetodC(op,a,b,fn,error):
    if(op==0):
        return biseccion(a,b,fn,error)
    elif(op==1):
        return falsapos(a,b,fn,error)

def selectMetodA(op,xn,fn,dfn,error):
    if(op==0):
        return newton(xn,fn,dfn,error)
    elif(op==1):
        return secante(xn,fn,error)
    elif(op==2):
        return puntofijo(xn,fn,error)

def graphList(fList,pList,pi,pf):
    pi=pi-2
    pf=pf+2
    xList = np.linspace(pi,pf,100)
    for i in range(len(fList)):
        yList=getY(fList[i],xList)
        plt.plot(xList, yList)
    for p in pList:
        plt.plot(p[0],p[1],'ro')
    plt.axis([pi, pf, pi, pf])
    plt.show() 
    
def interseccion(fn1,fn2,pi,pf,error):
    partes=10
    tamRango=abs(pf-pi)
    sizePart=tamRango/10
    tempPi=pi
    fnT=fn1+"-("+fn2+")"
    xInter=[]
    #print(fnT)
    for i in range(partes-1):
        nTempPi=tempPi+sizePart
        if(bolzano(fnT,tempPi,nTempPi)):
            result=secante(tempPi,fnT,error)
            xInter.append(result[0])       
        else:
            print("No cumple bolzano")
        tempPi=nTempPi
        
    yInter=getY(fn1,xInter)
    puntosInter=[]
    for cnt in range(len(xInter)):
        puntosInter.append([xInter[cnt],yInter[cnt]])
    fList=[fn1,fn2]
    graphList(fList,puntosInter,pi,pf)
    return puntosInter

"""def propagacion(LFn,Lerr,ec):
    prs=Parse()
"""
    