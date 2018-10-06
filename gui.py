#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import uic

from PyQt5.QtWidgets import QWidget, QFileDialog,QFileDialog,QMessageBox,QMainWindow, QApplication, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton,QHBoxLayout,QDialog,QTableWidgetItem  
import sys
import taylor
import metodos
import matrix as mtx

def MatrixToTable(matrix,tableView):
    tableView.setRowCount(len(matrix))
    tableView.setColumnCount(len(matrix[0]))
    for i,row in enumerate(matrix):
        for j,val in enumerate(row):
            tableView.setItem(i,j,QTableWidgetItem(str(val)))

def TableToMatrix(tableView):
    matrix=[]
    for i in range(tableView.rowCount()):
        arr=[]
        for j in range(tableView.columnCount()):
            arr.append(float(tableView.item(i,j).text()))
        matrix.append(arr)
    return matrix

class inicio(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui.ui", self)
        self.tlr=taylor.Taylor()
        self.botonTaylor.clicked.connect(self.calcTaylor)
        self.botonMetodCerrados.clicked.connect(self.calcMetodosCerrados)
        self.botonMetodAbiertos.clicked.connect(self.calcMetodosAbiertos)
        self.botonMatriz.clicked.connect(self.calcMatrices)
        self.botonLagrange.clicked.connect(self.calcLagrange)
        self.pushButtonNR.clicked.connect(self.calcNewtonRaphson)
        self.spinBox.valueChanged.connect(self.changeSpin)
        self.spinBox_2.valueChanged.connect(self.changeSpin2)
        self.spinBox_3.valueChanged.connect(self.changeSpin3)
        self.spinBox_4.valueChanged.connect(self.changeSpin4)
        self.spinBoxNR.valueChanged.connect(self.changeSpinNR)
    def calcTaylor(self):
        op=self.comboFunc.currentText() 
        x=float(self.lineAngulo.text())
        resp=0
        historial=[]
        self.tlr.error=float(self.lineError.text())
        resp,historial=self.tlr.selectFunc(op,float(x) )
        historial = [str(i) for i in historial]
        self.iteTaylor.clear()
        self.iteTaylor.addItems(historial)
        self.lineRespTaylor.setText(str(resp))
        

    def calcMetodosCerrados(self):
        op=self.comboBoxMC.currentIndex()
        a=float(self.aLineEdit.text())
        b=float(self.bLineEdit.text())
        fn=self.fnLineEdit.text()
        error=float(self.errorLineEdit.text())
        resp=metodos.selectMetodC(op,a,b,fn,error)
        MatrixToTable(resp[1],self.tableMetodC)
        self.respMetodC.setText(str(resp[0]))

    def calcMetodosAbiertos(self):
        op=self.comboBoxMA.currentIndex()
        xn=float(self.xnLineEdit.text())
        fn=self.fnLineEdit_1.text()
        dfn=self.dFnLineEdit.text()
        error=float(self.errorLineEdit_1.text())
        resp=metodos.selectMetodA(op,xn,fn,dfn,error)
        MatrixToTable(resp[1],self.tableMetodA)
        self.respMetodA.setText(str(resp[0]))



    def calcMatrices(self):
        matrizA=TableToMatrix(self.matrizA)
        matrizB=TableToMatrix(self.matrizB)
        print("MatrizA",matrizA)
        op=self.comboBox_4.currentIndex()
        matrizC=[]
        if(op==0):
            matrizC=mtx.multMatrix(matrizA,matrizB)
            MatrixToTable(matrizC,self.matrizC)
        if(op==1):
            matrizC=mtx.sumaMatrix(matrizA,matrizB)
            MatrixToTable(matrizC,self.matrizC)
        if(op==2):
            matrizC=mtx.restaMatrix(matrizA,matrizB)
            MatrixToTable(matrizC,self.matrizC)
        if(op==3):
            matrizC=mtx.inversa(matrizA)
            MatrixToTable(matrizC,self.matrizC)
        if(op==4):
            matrizC=mtx.transpuesta(matrizA)
            MatrixToTable(matrizC,self.matrizC)
        if(op==5):
            n=int(self.lineEdit_3.text())
            matrizC=mtx.potencia(matrizA,n)
            MatrixToTable(matrizC,self.matrizC)
        if(op==6):
            lineDet=mtx.determinante(matrizA)
            self.lineEdit_5.setText(str(round(lineDet,2)))
            
        print("Calc matrices")
    def calcLagrange(self):
        print("Lagrange")

    def calcNewtonRaphson(self):
        arrFn=[]
        arrLx=[]
        for i in range(self.tableWidgetNR.columnCount()):
            arrFn.append(self.tableWidgetNR.item(0,i).text())
        for i in range(self.tableWidgetNR.columnCount()):
            arrLx.append(float(self.tableWidgetNR.item(1,i).text()))
     
        error=float(self.lineEdit_4.text())
        resp=metodos.newtonRaphsonG(arrFn,arrLx,error)
        for j in range(len(resp)):
            self.tableWidgetNR2.setItem(0,j,QTableWidgetItem(str(resp[j])))

        

    def changeSpin(self):
        self.matrizA.setRowCount(self.spinBox.value())
    def changeSpin2(self):
        self.matrizA.setColumnCount(self.spinBox_2.value())
    def changeSpin3(self):
        self.matrizB.setRowCount(self.spinBox_3.value())
    def changeSpin4(self):
        self.matrizB.setColumnCount(self.spinBox_4.value())

    def changeSpinNR(self):
        self.tableWidgetNR.setColumnCount(self.spinBoxNR.value())
        self.tableWidgetNR2.setColumnCount(self.spinBoxNR.value())    
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)

_ventana = inicio()
_ventana.show()
app.exec_()
#"""