# VistaEgreso.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal

class EgresoView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(EgresoView, self).__init__(parent)

        self.vista = uic.loadUi("gui/egresos/Egreso.ui", self)
        #Conectamos el evento modificar y guardar con la funcion "operacionCOmpletada"
        self.vista.btn_guardar.clicked.connect(self.operacionCompletada)

        self.__haCambiado = False

    def setOperario(self, operario):
        self.vista.ope_legajo.setText(str(operario[0]))
        self.vista.ope_nombre.setText(operario[1] + " " + operario[2])

    def getOperario(self):
        legajo = self.vista.ope_legajo.text()
        nombre = self.vista.ope_nombre.text()
        return (legajo, nombre)

    def resetOperario(self):
        self.vista.ope_legajo.setText("")
        self.vista.ope_nombre.setText("")

    def setTotal(self, totalArticulos):
        self.egr_total_cant.setText(str(totalArticulos))

    def getDetalles(self):
        destino = self.vista.move_destino.currentIndex()
        agrupacion = self.vista.move_sector.currentText()
        vale = self.vista.egr_numero.text()
        return (destino, agrupacion, vale)

    def resetEgreso(self):
        self.resetOperario()
        self.resetDetalles()

    def resetDetalles(self):
        self.vista.egr_numero.setText("")
        self.vista.move_destino.setCurrentIndex(0)

    def __egresoHaCambiado(self):
        self.__haCambiado = True

    def resetCambios(self):
        self.__haCambiado = False

    def closeEvent(self, event):
        if not self.__haCambiado:
            event.accept()
            return
        resultado = QMessageBox.question(self, "Atencion", "No se guardarán los cambios. ¿Desea salir?", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()

    def operacionCompletada(self):
        if self.__haCambiado:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Operacion realizada con éxito")
            msg.setWindowTitle("Mensaje de confirmación")
            retval = msg.exec_()
