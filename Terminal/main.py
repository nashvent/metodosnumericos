#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import uic

from PyQt5.QtWidgets import QWidget, QFileDialog,QFileDialog,QMessageBox,QMainWindow, QApplication, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton,QHBoxLayout,QDialog,QTableWidgetItem  
import sys
import re
import ast
from parse import ParseConsola

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False



def isarray(value):
    if(value[0]=="["):
        return True
    return False
    


class inicio(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui.ui", self)
        self.lineEdit.returnPressed.connect(self.pressedEnter)
        self.variablesLocales={}
        self.tipoVariablesLocales={}
        self.prs=ParseConsola()
        self.historial=[]
        self.posicionHistorial=0

    def pressedEnter(self):
        comando=self.lineEdit.text()
        self.plainTextEdit.appendPlainText(comando)
        data=self.checkComando(comando)    
        self.addVariableLocal(data)
        self.registroHistorial(comando)
        res=data[1]
        self.plainTextEdit.appendPlainText("=> "+str(res)+"\n")
        self.lineEdit.setText("")
        self.updateVar()
        
    def checkComando(self,comando):
        nVar=""
        vVar=""
        tVar=""
        if comando.find("=") == -1:
            print("Ejectuar")
            vVar=self.runFunc(comando)
        else:
            indxIgual=comando.find('=')
            nVar=comando[:indxIgual]
            vVar=comando[indxIgual+1:]
            if(vVar[0]=="'"):
                tVar="string"
                #print("es un string")
            elif(isarray(vVar)):
                vVar=self.runFunc(vVar)
                tVar=type(vVar).__name__
                #print ("Es un array pero aun no se cual")
                
            elif(isfloat(vVar)):
                tVar="float"
                #print("Es flotante")
            
            else:
                vVar=self.runFunc(vVar)
                tVar=type(vVar).__name__
                #print("Es funcion")
        return nVar,vVar,tVar

    def runFunc(self,funcion):
        self.prs.setEc(funcion)
        self.prs.addVarFromList(self.variablesLocales)
        return self.prs.evaluate()

    def addVariableLocal(self,data):
        if(data[0]!=''):
            self.tipoVariablesLocales[data[0]]=data[2]
            if(data[2]=="float"):
                self.variablesLocales[data[0]]=float(data[1])
            elif(data[2]=="string"):
                self.variablesLocales[data[0]]=data[1]
            elif(data[2]=="int"):
                self.variablesLocales[data[0]]=int(data[1])  
            else:
                self.variablesLocales[data[0]]=data[1]   

    def updateVar(self):
        self.tableVar.setRowCount(len(self.variablesLocales))
        it=0
        for key,val in self.variablesLocales.items():
            self.tableVar.setItem(it,0, QTableWidgetItem(str(key)))
            self.tableVar.setItem(it,1, QTableWidgetItem(str(val)))
            self.tableVar.setItem(it,2, QTableWidgetItem(self.tipoVariablesLocales[key]))
            it+=1 
    def registroHistorial(self,comando):
        self.historial.append(comando)
        self.posicionHistorial=len(self.historial)

    def keyPressEvent(self, event):
        key = event.key()
        if(len(self.historial)>0):
            if(key==16777235):
                if(self.posicionHistorial>0):
                    self.posicionHistorial=self.posicionHistorial-1
                    self.lineEdit.setText(self.historial[self.posicionHistorial])        
  
            if(key==16777237):
                self.posicionHistorial=self.posicionHistorial+1
                if(self.posicionHistorial<len(self.historial)):
                    self.lineEdit.setText(self.historial[self.posicionHistorial])
                    
                else:
                    self.posicionHistorial=len(self.historial)
                    self.lineEdit.setText("")
                
        
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)

_ventana = inicio()
_ventana.show()
app.exec_()
#"""