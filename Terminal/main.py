#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import uic

from PyQt5.QtWidgets import QWidget, QFileDialog,QFileDialog,QMessageBox,QMainWindow, QApplication, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton,QHBoxLayout,QDialog,QTableWidgetItem  
import sys
from parse import Parse

class inicio(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui.ui", self)
        #self.lineEdit.setText("cmd> ")
        self.lineEdit.returnPressed.connect(self.pressedEnter)
        #self.lineEdit.keyPressEvent=self.keyPressEvent
        self.variablesLocales={}
        self.prs=Parse()
        self.historial=[]
        self.posicionHistorial=0

    def pressedEnter(self):
        comando=self.lineEdit.text()
        self.plainTextEdit.appendPlainText(comando)
        tipo=self.checkComando(comando)
        self.registroHistorial(comando)
        res=""
        self.prs.addVarFromList(self.variablesLocales)
        
        if(tipo==0):
            if(comando=="clear"):
                self.plainTextEdit.clear()
                return
            
            self.prs.setEc(comando)
            try:
                res=self.prs.evaluate()
            except NameError:
                res="Variable no definida"
            except:
                res="Error desconocido"
        elif(tipo==1):
            indxIgual=comando.find('=')
            nombreVar=comando[:indxIgual].replace(" ","")
            valVar=comando[indxIgual+1:]
            self.variablesLocales[nombreVar]=float(valVar)
            res=str(self.variablesLocales)
        
        self.plainTextEdit.appendPlainText("=>"+str(res)+"\n")
        #self.lineEdit.setText("cmd> ")
        self.lineEdit.setText("")
        self.updateVar()
        
    def checkComando(self,comando):
        if comando.find("=") == -1:
            return 0 #Llamando funcion
        else:
            return 1 #assignacion
    def updateVar(self):
        self.tableVar.setRowCount(len(self.variablesLocales))
        it=0
        for key,val in self.variablesLocales.items():
            self.tableVar.setItem(it,0, QTableWidgetItem(str(key)))
            self.tableVar.setItem(it,1, QTableWidgetItem(str(val)))
            it+=1 
    def registroHistorial(self,comando):
        self.historial.append(comando)
        self.posicionHistorial=len(self.historial)
        self.tableHistorial.setRowCount(len(self.historial))
        it=0
        for comd in reversed(self.historial):
            self.tableHistorial.setItem(it,0, QTableWidgetItem(str(comd)))
            it+=1
        
"""    def keyPressEvent(self, event):
        key = event.key()
        print("press",self.posicionHistorial)
                    
        if(len(self.historial)>0):
            if(key==16777235):
                if(self.posicionHistorial>0):
                    self.posicionHistorial=self.posicionHistorial-1
                    print("arriba",self.posicionHistorial)
                    self.lineEdit.setText(self.historial[self.posicionHistorial])        
                    
                
            if(key==16777237):
                if(self.posicionHistorial+1<len(self.historial)):
                    self.posicionHistorial=self.posicionHistorial+1
                    print("abajo",self.posicionHistorial)
                    self.lineEdit.setText(self.historial[self.posicionHistorial])
                    
                else:

                    self.lineEdit.setText("")
"""
                
        
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)

_ventana = inicio()
_ventana.show()
app.exec_()
#"""