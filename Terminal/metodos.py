from math import *
import numpy as np  
import matplotlib.pyplot as plt 
import matrix 
from mparse import SimpleParse 
from decimal import *

plt.style.use('seaborn-whitegrid')

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
    if(bolzano(fn,a,b)==False):
        return "no bolzano"
    maxIt=100
    cont=0
    xn=0
    xprev=10000
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
        #print(a,b,xn,nerror)
        historial.append([a,b,xn,nerror])
        if(fa==0):
            xn=fa
            break
        if(fxn==0):
            break

        if (fa*fxn)<0:
            b=xn
        else:
            a=xn        
        xprev=xn
        if (nerror<error):
            break
        cont+=1
    return xn #,historial

def falsapos(a,b,fn,error):
    maxIt=100
    cont=0
    xn=0
    xprev=0
    historial=[]
    prs=SimpleParse()
    prs.setEc(fn)    
    error=Decimal(error)
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
    return xn #,historial

def secante(xn,fn,error):
    errorTemp=10000
    maxIt=100
    cont=0
    h=0.001
    xnv=xn
    prs=SimpleParse()
    prs.setEc(fn)
    historial=[]
    historial.append([xn,0.0])
    xprev=0
    while(errorTemp>error and maxIt>cont):
        prs.addVariable("x",xnv)
        resfn=prs.evaluate()
        prs.addVariable("x",xnv+h)
        resfxh=prs.evaluate()
        prs.addVariable("x",xnv-h)
        resfx_h=prs.evaluate()
        if((resfxh-resfx_h)==0):
            return "Error /0"
            break
        xprev=xnv
        xnv=xprev-((2*h*resfn)/(resfxh-resfx_h))
        errorTemp=abs(xprev-xnv)
        historial.append([xnv,errorTemp])
        if(errorTemp<error):
            break  
        cont+=1
    return xnv#,historial

def tsecante(fn1,pi,pf,error):
    partes=30
    tamRango=abs(pf-pi)
    sizePart=tamRango/30
    tempPi=pi
    xInter=[]
    #print(fnT)
    for i in range(partes-1):
        nTempPi=tempPi+sizePart
        if(bolzano(fn1,tempPi,nTempPi)):
            result=secante(tempPi,fn1,error)
            xInter.append(result)       
        tempPi=nTempPi
        
    yInter=getY(fn1,xInter)
    puntosInter=[]
    for cnt in range(len(xInter)):
        puntosInter.append([xInter[cnt],yInter[cnt]])
    fList=[fn1]
    graphList(fList,puntosInter,pi,pf)
    return puntosInter

def tbiseccion(fn1,pi,pf,error):
    partes=30
    tamRango=abs(pf-pi)
    sizePart=tamRango/30
    tempPi=pi
    xInter=[]
    for i in range(partes-1):
        nTempPi=tempPi+sizePart
        if(bolzano(fn1,tempPi,nTempPi)):
            result=biseccion(tempPi,nTempPi,fn1,error)
            xInter.append(result)       
        tempPi=nTempPi
        
    yInter=getY(fn1,xInter)
    puntosInter=[]
    for cnt in range(len(xInter)):
        puntosInter.append([xInter[cnt],yInter[cnt]])
    fList=[fn1]
    graphList(fList,puntosInter,pi,pf)
    return puntosInter

def tfalsapos(fn1,pi,pf,error):
    partes=30
    tamRango=abs(pf-pi)
    sizePart=tamRango/30
    tempPi=pi
    xInter=[]
    #print(fnT)
    for i in range(partes-1):
        nTempPi=tempPi+sizePart
        if(bolzano(fn1,tempPi,nTempPi)):
            result=falsapos(tempPi,nTempPi,fn1,error)
            xInter.append(result)       
        """else:
            print("No cumple bolzano")
        """
        tempPi=nTempPi
        
    yInter=getY(fn1,xInter)
    puntosInter=[]
    for cnt in range(len(xInter)):
        puntosInter.append([xInter[cnt],yInter[cnt]])
    fList=[fn1]
    graphList(fList,puntosInter,pi,pf)
    return puntosInter



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
    xlist=[]
    ylist=[]
    while(xt<xf):
        prs.addVariable("x",xt)
        prs.addVariable("y",yt)
        xlist.append(xt)
        ylist.append(yt)
        yt=yt+h*(prs.evaluate())
        xt=round(xt+h,15)
    xlist.append(xt)
    ylist.append(yt)
    return xlist,ylist

def eulerHeun(df,xn,yn,h,xf):
    prs=SimpleParse()
    prs.setEc(df)
    xt=xn
    yt=yn
    xlist=[]
    ylist=[]
    while(xt<xf):
        prs.addVariable("x",xt)
        prs.addVariable("y",yt)
        xlist.append(xt)
        ylist.append(yt)
        f1=prs.evaluate()
        yt1=yt+h*f1
        xt1=round(xt+h,15)
        prs.addVariable("x",xt1)
        prs.addVariable("y",yt1)
        f2=prs.evaluate()
        yt=yt+(h/2)*(f1+f2)
        xt=xt1
    xlist.append(xt)
    ylist.append(yt)
    return xlist,ylist

def rungeKutta(df,xn,yn,h,xf):
    prs=SimpleParse()
    prs.setEc(df)
    xt=xn
    yt=yn
    xlist=[]
    ylist=[]
    while(xt<xf):
        xlist.append(xt)
        ylist.append(yt)

        prs.addVariable("x",xt)
        prs.addVariable("y",yt)
        k1=prs.evaluate()
        
        prs.addVariable("x",xt+(0.5*h))
        prs.addVariable("y",yt+(0.5*k1*h))
        k2=prs.evaluate()

        prs.addVariable("x",xt+(0.5*h))
        prs.addVariable("y",yt+(0.5*k2*h))
        k3=prs.evaluate()

        prs.addVariable("x",xt+h)
        prs.addVariable("y",yt+(k3*h))
        k4=prs.evaluate()

        yt=yt+(1/6)*(k1+(2*k2)+(2*k3)+k4)*h
        xt=round(xt+h,15)

    xlist.append(xt)
    ylist.append(yt)
    return xlist,ylist

def dormandPrince(df,xn,yn,h,xf):
    prs=SimpleParse()
    prs.setEc(df)
    xt=xn
    yt=yn
    xlist=[]
    ylist=[]
    while(xt<xf):
        xlist.append(xt)
        ylist.append(yt)

        prs.addVariable("x",xt)
        prs.addVariable("y",yt)
        k1=h*prs.evaluate()
        
        prs.addVariable("x",xt+((1/5)*h))
        prs.addVariable("y",yt+((1/5)*k1))
        k2=h*prs.evaluate()

        prs.addVariable("x",xt+((3/10)*h))
        prs.addVariable("y",yt+((3/40)*k1)+((9/40)*k2))
        k3=h*prs.evaluate()

        prs.addVariable("x",xt+((4/5)*h))
        prs.addVariable("y",yt+((44/45)*k1)-((56/15)*k2)+((32/9)*k3))
        k4=h*prs.evaluate()

        prs.addVariable("x",xt+((8/9)*h))
        prs.addVariable("y",yt+((19372/6561)*k1)-((25360/2187)*k2)+((64448/6561)*k3)-((212/729)*k4))
        k5=h*prs.evaluate()

        prs.addVariable("x",xt+h)
        prs.addVariable("y",yt+((9017/3168)*k1)-((355/33)*k2)-((46732/5247)*k3)+((49/176)*k4)-((5103/18656)*k5))
        k6=h*prs.evaluate()

        yt=yt+((35/384)*k1)+((500/1113)*k3)+((125/192)*k4)-((2187/6784)*k5)+((11/84)*k6)  
        xt=round(xt+h,15)

    xlist.append(xt)
    ylist.append(yt)
    return xlist,ylist