# elemento_view.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import pyqtSignal, QRegExp

#Creamos la clase ElementoView
class ElementoView(QtWidgets.QWidget):
    rx = QRegExp("elem_*")

	#Inicializamos el objeto
    def __init__(self, presenter, parent=None):
        super(ElementoView, self).__init__(parent)

        self.vistaDetalle = uic.loadUi("gui/detalles/elementos_detalle.ui", self)


    #Funcion que trae un elemento y modifica la ifnormacion.
    def getElemento(self):
        rawElemento = self.vistaDetalle.findChildren((QComboBox, QLineEdit, QLabel), self.rx)
        elemento = {}
        for componente in rawElemento:
            if "elem_" not in componente.objectName():
                continue
            if (type(componente) == QtWidgets.QComboBox):
                elemento[componente.objectName()] = componente.currentText()
            else:
                elemento[componente.objectName()] = componente.text()
        return elemento

	#Funcion que carga un elemento en pelemicular dentro de "Detalle del Producto"
    def setElemento(self, elemento):
        print (elemento)
        self.vistaDetalle.elem_id.setText(str(elemento[0]))
        self.vistaDetalle.elem_columna_1.setText(elemento[1])
        self.vistaDetalle.elem_columna_2.setText(elemento[2])
        self.vistaDetalle.elem_columna_3.setText(elemento[3])
        self.vistaDetalle.elem_columna_4.setText(elemento[4])
