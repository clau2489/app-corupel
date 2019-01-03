# VistaIngreso.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator

class IngresoView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(IngresoView, self).__init__(parent)

        self.vista = uic.loadUi("gui/ingresos/Ingreso.ui", self)

        self.vista.tbl_articulos.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        #Conectamos el evento modificar y guardar con la funcion "operacionCOmpletada"
        # self.vista.btn_guardar.clicked.connect(self.operacionCompletada)

        rxPref = QRegExp("[0-9]{0,10}")
        rxNum = QRegExp("^[0-9]{0,20}$")
        # rxId = QRegExp("^[0-9]{0,16}$")

        # self.vista.prov_id.setValidator(QRegExpValidator(rxId))
        self.vista.rem_prefijo.setValidator(QRegExpValidator(rxPref))
        self.vista.rem_numero.setValidator(QRegExpValidator(rxNum))
        self.vista.fact_prefijo.setValidator(QRegExpValidator(rxPref))
        self.vista.fact_numero.setValidator(QRegExpValidator(rxNum))

    # def setProveedor(self, proveedor):
    #     self.vista.prov_id.setText(str(proveedor[0]))
    #     self.vista.prov_nombre.setText(proveedor[1])
    #
    def getProveedor(self):
    #     return self.vista.prov_id.text()
        return self.vista.prov_proveedor.currentText()
    
    def resetProveedor(self):
        # self.vista.prov_id.setText("")
        # self.vista.prov_nombre.setText("")
        self.vista.prov_proveedor.setCurrentIndex(0)

    def setTotales(self, totalArticulos, totalCosto):
        self.tot_cant.setText(str(totalArticulos))
        self.tot_cost.setText(str(totalCosto))

    def resetTotales(self):
        self.tot_cant.setText(str(""))
        self.tot_cost.setText(str(""))

    def getComprobantes(self):
        rxFact = QRegExp("fact_*")
        rxRem = QRegExp("rem_*")
        remito = self.vista.findChildren(QtWidgets.QWidget, rxRem)
        factura = self.vista.findChildren(QtWidgets.QWidget, rxFact)

        return (remito, factura)

    def resetComprobantes(self):
        self.vista.fact_prefijo.setText("")
        self.vista.rem_prefijo.setText("")
        self.vista.rem_numero.setText("")
        self.vista.fact_numero.setText("")
        self.vista.fact_tipo.setCurrentIndex(0)


    #ejemplo de dialogo
    def operacionCompletada(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Operacion realizada con éxito")
        msg.setWindowTitle("Mensaje de confirmación")
        retval = msg.exec_()
