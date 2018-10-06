import math
class Taylor:
    error = 0.001
    nMax=50
    def __init__(self):
        print("")
    def exp(self,x):
        resp=0
        respAnt=0
        historial=[]
        for n in range(self.nMax):
            respAnt=resp
            resp=resp+(math.pow(x,n)/math.factorial(n))
            historial.append(resp)
            if(abs(respAnt-resp)<self.error):
                break
        return resp,historial

    def ln(self,x):
        resp=0
        respAnt=0
        historial=[]
        for n in range(self.nMax):
            
            respAnt=resp
            resp+=((1/(2*n +1))* math.pow(( (x-1)/(x+1) ),(2*n +1) )) 
            historial.append(resp)
            if(abs(respAnt-resp)<self.error):
                break
        resp=resp*2
        return resp,historial

    def sin(self,x):
        resp=0
        historial=[]
        for n in range(self.nMax):
            respAnt=resp
            resp+=( (math.pow(-1,n))/(math.factorial(2*n+1)) ) * (math.pow(x,2*n+1))
            historial.append(resp)
            if(abs(respAnt-resp)<self.error):
                break 
        return resp,historial

    def cos(self,x):
        resp=0
        historial=[]
        for n in range(self.nMax):
            respAnt=resp
            resp+=( (math.pow(-1,n))/(math.factorial(2*n)) ) * (math.pow(x,2*n))
            historial.append(resp)
            if(abs(respAnt-resp)<self.error):
                break 
        return resp,historial

    def arcsin(self,x):
        resp=0
        historial=[]
        for n in range(self.nMax):
            respAnt=resp
            resp+=( (math.factorial(2*n))/( math.pow(4,n)*( math.pow(math.factorial(n),2) )*(2*n+1)  ) ) * (math.pow(x,2*n+1)) 
            historial.append(resp)
            if(abs(respAnt-resp)<self.error):
                break
        return resp,historial

    def arctan(self,x):
        resp=0
        historial=[]
        for n in range(self.nMax):
            respAnt=resp
            resp+=( ( math.pow(-1,n) )/( 2*n+1 ) ) * (math.pow(x,2*n+1))
            historial.append(resp)
            if(abs(respAnt-resp)<self.error):
                break 
        return resp,historial
    def selectFunc(self,op,x):
        if(op=="Seno"):
            return self.sin(x)
        elif(op=="Coseno"):
            return self.cos(x)
        elif(op=="Exponencial"):
            return self.exp(x)
        elif(op=="Log Natural"):
            return self.ln(x)
        elif(op=="ArcoSeno"):
            return self.arcsin(x)
        elif(op=="ArcoTangente"):
            return self.arctan(x)
            
