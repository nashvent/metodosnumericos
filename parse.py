from math import *
import parser
class Parse:
    variables={}
    ecuation=""
    def addVariable(self,vname,vval):
        self.variables[vname]=vval
    def setEc(self,ec):        
        self.ecuation=ec
    
    def evaluate(self):
        var=self.variables
        tempec=self.cleanStringEc()
        code = parser.expr(tempec).compile()
        return (eval(code)) 

    def addVarFromList(self,lista):
        varNames=["x","y","z","w"]
        for i in range(len(lista)):
            self.addVariable(varNames[i],lista[i])
    def cleanStringEc(self):
        tempEc=list(self.ecuation)
        for key,value in self.variables.items():
            for i in range(len(tempEc)):
                if(tempEc[i]==key):
                    if((i==0 or tempEc[i-1].isalpha()==False ) and ( i+1>=len(tempEc) or tempEc[i+1].isalpha()==False)  ):
                        tempEc[i]="var['"+key+"']"
                    #tempec=tempec.replace(key,"var['"+key+"']")
    
        return "".join(tempEc)