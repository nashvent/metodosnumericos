import numpy
def sumaMatrix(ma,mb):
    lenM=len(ma)
    lenN=len(ma[0])
    mr=[]
    for i in range(lenM):
        mrT=[]
        for j in range(lenN):
           mrT.append(ma[i][j]+mb[i][j])
        mr.append(mrT) 
    return mr

def restaMatrix(ma,mb):
    lenM=len(ma)
    lenN=len(ma[0])
    mr=[]
    for i in range(lenM):
        mrT=[]
        for j in range(lenN):
           mrT.append(ma[i][j]-mb[i][j])
        mr.append(mrT) 
    return mr

def multEscalarMatrix(ma,escal):
    lenM=len(ma)
    lenN=len(ma[0])
    mr=[]
    for i in range(lenM):
        mrT=[]
        for j in range(lenN):
           mrT.append(ma[i][j]*escal)
        mr.append(mrT) 
    return mr

def divEscalarMatrix(ma,escal):
    lenM=len(ma)
    lenN=len(ma[0])
    mr=[]
    for i in range(lenM):
        mrT=[]
        for j in range(lenN):
           mrT.append(ma[i][j]/escal)
        mr.append(mrT) 
    return mr

def multMatrix(ma,mb):
    lenM=len(ma)
    lenN=len(ma[0])
    mr=[]
    for i in range(lenN):
        mrT=[]
        for j in range(lenN):
            res=0
            for k in range(lenN):
               res=res+(ma[i][k]*mb[k][j]) 
            mrT.append(res)
        mr.append(mrT) 
    return mr

def determinante(ma):
    return numpy.linalg.det(ma)

def inversa(ma):
    return numpy.linalg.inv(ma)
def transpuesta(ma):
    matrix = [[0 for i in range(len(ma[0]))] for i in range(len(ma))]
    for i in range(len(ma)):
        for j in range(len(ma[i])):
            matrix[j][i]=ma[i][j]
    return matrix

def potencia(ma,n):
    mr=ma
    for i in range(n-1):
        mr=multMatrix(mr,ma)
    return mr

def selectFuncMatrix(op,ma,mb,n):
    if(op==0):
        return multMatrix(ma,mb)
    elif(op==1):
        return sumaMatrix(ma,mb)
    elif(op==2):
        return restaMatrix(ma,mb)
'''class Matrix:
    mtx = []
    def __init__(self, mtx):
         self.mtx=mtx
    def suma(self):
        print("This is a message inside the class.")
'''

def restaArray(arrA,arrB):
    arrC=[]
    for i in range(len(arrA)):
        arrC.append(arrA[i]-arrB[i])
    return arrC

def multVectorMatrix(matx,vectr):
    return numpy.matmul(matx,vectr)