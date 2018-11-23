import parser
from math import *
import numpy as np  
import matplotlib.pyplot as plt 
import matrix 
from mparse import SimpleParse 
plt.style.use('seaborn-whitegrid')
"""
def puntofijo(xn,fn,error):
    maxIt=100
    historial=[]
    xr=xn
    prs=SimpleParse()
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
"""
getSign = lambda a: (a>0) - (a<0)

def bolzano(fn,a,b):
    prs=SimpleParse()
    prs.setEc(fn)
    prs.addVariable("x",a)
    evA=prs.evaluate()
    prs.addVariable("x",b)
    evB=prs.evaluate()
    if((evA*evB)<0):
        return True
    return False

def biseccion(a,b,fn,error):
    maxIt=100
    cont=0
    xn=0
    xprev=0
    x=0.0
    historial=[]
    prs=SimpleParse()
    prs.setEc(fn)    
    while(cont<maxIt):  
        xn=(a+b)/2
        prs.addVariable("x",xn)
        fxn=prs.evaluate()
        prs.addVariable("x",a)
        fa=prs.evaluate()
        nerror=abs(xn-xprev)
        historial.append([a,b,xn,nerror])
        if (fa*fxn)<0:
            b=xn
        else:
            a=xn
        
        xprev=xn
        if (nerror<error):
            break
        cont+=1
    return xn,historial

def falsapos(a,b,fn,error):
    maxIt=100
    cont=0
    xn=0
    xprev=0
    x=0.0
    historial=[]
    prs=SimpleParse()
    prs.setEc(fn)    
    while(cont<maxIt):  
        prs.addVariable("x",a)
        fa=prs.evaluate()
        prs.addVariable("x",b)
        fb=prs.evaluate()
        xn=a-(fa*((b-a)/(fb-fa)))
        prs.addVariable("x",xn)
        fxn=prs.evaluate()
        if (fa*fxn)<0:
            b=xn
        else:
            a=xn
        nerror=abs(xn-xprev)
        historial.append([a,b,xn,nerror])
        xprev=xn
        if (nerror<error):
            break
        cont+=1
    return xn,historial

def secante(xn,fn,error):
    errorTemp=1000000
    maxIt=100
    cont=0
    h=error/10
    xAnt=xn
    prs=SimpleParse()
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

def polyroot(raices):
    rpoly=""
    for idx in range(len(raices)):
        cval=raices[idx]
        if(cval>0):
            csign="-"
        else:
            csign="+"
            cval=cval*(-1)
        
        rpoly=rpoly+"(x"+csign+str(cval)+")"
        if(idx+1<len(raices)):
            rpoly=rpoly+"*"
    return rpoly

def lagrange(xLista,yLista):
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
    return prodStr 

def getY(formula,x):
    prs=SimpleParse()
    y=[]
    prs.setEc(formula)
    for i in x:
        prs.addVariable("x",i)
        yT=prs.evaluate()
        #print(yT)
        y.append(yT)
    return y

def graph(formula,i,f):
    prs=SimpleParse()
    x = np.linspace(i,f,100)
    prs.setEc(formula)
    y=getY(formula,x) 
    plt.plot(x, y)
    plt.axis([i, f, i+1, f])
    plt.show()

def listToDict(Ln,Lv):
    dicc={}
    for i in range(len(Ln)):
        dicc[str(Ln[i])]=Lv[i]
    return dicc

def imagenNR(Lxn,LFn,Lx):
    tparse=SimpleParse()
    LFxn=[]
    tparse.addVarFromList(listToDict(Lxn,Lx))
    for i in range(len(LFn)):
        tparse.setEc(LFn[i])
        LFxn.append(tparse.evaluate())
    return LFxn

def jacobiana(NLx,LFn,Lx,err):
    tparse=SimpleParse()
    Jmatrix=[]
    h=err/10
    for i in range(len(LFn)):
        mTemp=[]
        for j in range(len(Lx)):
            TLx=list(Lx)
            TLx[j]=Lx[j]+h
            tparse.setEc(LFn[i])       
            tparse.addVarFromList(listToDict(NLx,TLx))
            rH=float(tparse.evaluate())
            TLx=list(Lx)
            TLx[j]=Lx[j]-h
            tparse.addVarFromList(listToDict(NLx,TLx))
            r_H=tparse.evaluate()
            DR=(rH-r_H)/(2*(h*100))
            mTemp.append(DR)
        Jmatrix.append(mTemp) 
    return Jmatrix

def errorNR(Lx,TLx):
    err=0
    i=0
    for i in range(len(Lx)):
        tmp=float(float(Lx[i])-float(TLx[i]))
        err+=pow(tmp,2)
    return sqrt(err)

# (['x','y'],['x*y','x**2+y**2'],[2,4])
def newtonRaphsonG(NLx,LFn,Lx,err):
    maxIt=100
    errorAnt=0
    errorTemp=0
    contErr=0
    LxAnt=[]
    for i in range(maxIt):
        TLx=list(Lx)
        jaco=jacobiana(NLx,LFn,Lx,err)
        LFxn=imagenNR(NLx,LFn,Lx)    
        respTemp=matrix.multVectorMatrix(jaco,LFxn)
        LxAnt=Lx
        Lx=matrix.restaArray(Lx,respTemp)
        print("Lx",Lx)
        errorAnt=errorTemp
        errorTemp=errorNR(TLx,Lx)
        if(abs(errorAnt-errorTemp)>1):
            print("Divergente")
            return LxAnt
        if(errorTemp<err):
            break       
    
    return Lx
"""
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
"""
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

    

def trapecio(fn,a,b,n):
    h=(b-a)/n
    prs=SimpleParse()
    prs.setEc(fn)
    i=a+h
    sum=0
    while(i<b):
        prs.addVariable("x",i)
        sum+=prs.evaluate()
        i+=h
    prs.addVariable("x",a)
    fa=prs.evaluate()
    prs.addVariable("x",b)
    fb=prs.evaluate()
    resp=h*( ((fa+fb)/2) + sum)
    return resp

def simpson1_3(fn,a,b,n):
    h=(b-a)/(n)
    prs=SimpleParse()
    prs.setEc(fn)
    parSum=0
    imparSum=0
    i=a+h
    cont=1
    while (i<b):
        print("i",i)
        prs.addVariable("x",i)
        if(cont%2==0):
            parSum+=prs.evaluate()
        else:
            imparSum+=prs.evaluate()
        cont+=1
        i+=h
        i=round(i,15)
    prs.addVariable("x",a)
    fa=prs.evaluate()
    prs.addVariable("x",b)
    fb=prs.evaluate()
    resp=(h/3)*(fa+fb+(2*parSum)+(4*imparSum))
    return resp

def simpson3_8(fn,a,b):
    h=(b-a)/3
    prs=SimpleParse()
    prs.setEc(fn)
    x0=a
    x1=x0+h
    x2=x1+h
    x3=b
    prs.addVariable("x",x0)
    fx0=prs.evaluate()
    prs.addVariable("x",x1)
    fx1=prs.evaluate()
    prs.addVariable("x",x2)
    fx2=prs.evaluate()
    prs.addVariable("x",x3)
    fx3=prs.evaluate()
    resp=(b-a)*(fx0+(3*fx1)+(3*fx2)+fx3)*(1/8)
    resp=round(resp,10)
    return resp

#def simpson3(fn,a,b):
#    return simpson1(fn,a,b,4)

def eulerSimple(df,xn,yn,h,xf):
    prs=SimpleParse()
    prs.setEc(df)
    h=float(h)
    xt=xn
    yt=yn
    while(xt<xf):
        prs.addVariable("x",xt)
        prs.addVariable("y",yt)
        yt=yt+h*(prs.evaluate())
        print(yt)
        xt=round(xt+h,15)    
    return yt