import parser
from math import *
import numpy as np  
import matplotlib.pyplot as plt 
import matrix 
from parse import Parse

def trapecio(a,b,fn,n):
    h=(b-a)/n
    prs=Parse()
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

def simpson(a,b,fn,n):
    h=(b-a)/(2*n)
    prs=Parse()
    prs.setEc(fn)
    parSum=0
    imparSum=0
    i=a+h
    xi=np.arange(i,b,h)
    for index in range(len(xi)):
        prs.addVariable("x",xi[index])
        if(index%2==0):
            imparSum+=prs.evaluate()
        else:
            parSum+=prs.evaluate()
    prs.addVariable("x",a)
    fa=prs.evaluate()
    prs.addVariable("x",b)
    fb=prs.evaluate()
    resp=(h/3)*(fa+fb+(2*parSum)+(4*imparSum))
    return resp

def eulerSimple(df,xn,yn,h,xf):
    prs=Parse()
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

