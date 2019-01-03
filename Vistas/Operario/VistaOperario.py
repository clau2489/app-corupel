# operario_view.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal, QRegExp, Qt

#Creamos la clase OperarioView
class OperarioView(QtWidgets.QWidget):
    rxOpe = QRegExp("ope_*")

	#Inicializamos el objeto
    def __init__(self, presenter, parent=None):
        super(OperarioView, self).__init__(parent)

        self.vistaDetalle = uic.loadUi("gui/detalles/operario_detalle.ui", self)
        self.vistaDetalle.btn_deshabilitar.hide()
        self.vistaDetalle.btn_imprimir.hide()

        #Conectamos el evento modificar y guardar con la funcion "operacionCOmpletada"
        self.vistaDetalle.btn_modificar.clicked.connect(self.operacionCompletada)
        self.vistaDetalle.btn_nuevo.clicked.connect(self.operacionCompletada)

        self.vistaDetalle.ope_legajo.textChanged.connect(self.__operarioHaCambiado)
        self.vistaDetalle.ope_nombre.textChanged.connect(self.__operarioHaCambiado)
        self.vistaDetalle.ope_apellido.textChanged.connect(self.__operarioHaCambiado)
        self.vistaDetalle.ope_puesto.textChanged.connect(self.__operarioHaCambiado)

        self.__haCambiado = False

    #Funcion que trae un operario y modifica la ifnormacion.
    def getOperario(self):
        rawOperario = self.vistaDetalle.findChildren((QComboBox, QLineEdit, QLabel), self.rxOpe)
        operario = {}
        for componente in rawOperario:
            if "ope_" not in componente.objectName():
                continue
            if (type(componente) == QtWidgets.QComboBox):
                operario[componente.objectName()] = componente.currentText()
            else:
                operario[componente.objectName()] = componente.text()
        try:
            operario['ope_legajo'] = int(operario['ope_legajo'])
        except:
            print("ERROR - El legajo del operario no es un numero")
        return operario

	#Funcion que carga un operario en particular dentro de "Detalle del Producto"
    def setOperario(self, operario):
        print (operario)
        self.vistaDetalle.ope_legajo.setText(str(operario[0]))
        self.vistaDetalle.ope_nombre.setText(operario[1])
        self.vistaDetalle.ope_apellido.setText(operario[2])
        self.vistaDetalle.ope_puesto.setText(operario[3])

        self.__haCambiado = False

    def resetOperario(self):
        camposAResetear = self.vistaDetalle.findChildren(QLineEdit, self.rxOpe)
        for campo in camposAResetear:
            campo.setText("")
        self.__haCambiado = False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        if not self.__haCambiado:
           event.accept()
           return
        resultado = QMessageBox.question(self, "Atencion", "No se guardarán los cambios. ¿Desea salir?", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()

    def resetCambios(self):
        self.__haCambiado = False

    def __operarioHaCambiado(self):
        self.__haCambiado = True

    #ejemplo de dialogo
    def operacionCompletada(self):
        if self.__haCambiado:
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Information)
           msg.setText("Operacion realizada con éxito")
           msg.setWindowTitle("Mensaje de confirmación")
           retval = msg.exec_()
