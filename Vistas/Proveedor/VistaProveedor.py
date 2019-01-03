    # proveedor_view.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel, QCheckBox, QTextEdit, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import pyqtSignal, QRegExp, Qt

#Creamos la clase ProveedorView
class ProveedorView(QtWidgets.QWidget):

    rxProv = QRegExp("prov_*")

	#Inicializamos el objeto
    def __init__(self, presenter, parent=None):
        super(ProveedorView, self).__init__(parent)
        # Todos los Widgets de PyQT deben ser privados,
        # esto se logra NO COLOCANDO 'self.' sino la variable localmente.

        #Traemos el archivo .UI "Proveedores_detalle"
        self.vistaDetalle = uic.loadUi("gui/detalles/proveedor_detalle.ui", self)
        self.vistaDetalle.btn_deshabilitar.hide()
        self.vistaDetalle.btn_imprimir.hide()

        self.vistaDetalle.btn_modificar.clicked.connect(self.operacionCompletada)
        self.vistaDetalle.btn_nuevo.clicked.connect(self.operacionCompletada)

        rxId = QRegExp("[0-9]{0,16}")
        rxNumeros = QRegExp("[0-9]{0,20}")

        self.vistaDetalle.prov_id.setValidator(QRegExpValidator(rxId))
        self.vistaDetalle.prov_cuit.setValidator(QRegExpValidator(rxNumeros))
        # self.vistaDetalle.prov_telefono.setValidator(QRegExpValidator(rxNumeros))
        # self.vistaDetalle.prov_telefono_dos.setValidator(QRegExpValidator(rxNumeros))
        self.vistaDetalle.prov_id.textChanged.connect(self.__activarBotones)

        self.vistaDetalle.prov_id.textChanged.connect(self.__proveedorHaCmabiado)
        self.vistaDetalle.prov_nombre.textChanged.connect(self.__proveedorHaCmabiado)
        self.vistaDetalle.prov_razon_social.textChanged.connect(self.__proveedorHaCmabiado)
        self.vistaDetalle.prov_cuit.textChanged.connect(self.__proveedorHaCmabiado)
        self.vistaDetalle.prov_direccion.textChanged.connect(self.__proveedorHaCmabiado)
        self.vistaDetalle.prov_nombre_contacto.textChanged.connect(self.__proveedorHaCmabiado)
        self.vistaDetalle.prov_telefono.textChanged.connect(self.__proveedorHaCmabiado)
        self.vistaDetalle.prov_telefono_dos.textChanged.connect(self.__proveedorHaCmabiado)
        self.vistaDetalle.prov_email.textChanged.connect(self.__proveedorHaCmabiado)
        self.vistaDetalle.prov_notas.textChanged.connect(self.__proveedorHaCmabiado)

        self.__activarBotones("")
        self.__haCambiado = False


    #Funcion que trae un proveedor y modifica la informacion.
    def getProveedor(self):
        rawProveedor = self.vistaDetalle.findChildren((QTextEdit, QLineEdit, QCheckBox), self.rxProv)
        proveedor = {}
        for componente in rawProveedor:
                if type(componente) == QLineEdit:
                    proveedor[componente.objectName()] = componente.text()
                if type(componente) == QTextEdit:
                    proveedor[componente.objectName()] = componente.toPlainText()
                if type(componente) == QCheckBox:
                    proveedor[componente.objectName()] = componente.isChecked()
                # print(componente.objectName(), componente.text())
        if (proveedor['prov_id']):
            proveedor['prov_id'] = int(proveedor['prov_id'])

        # if proveedor['prov_activo']:
        #     proveedor['prov_activo'] = 1
        # else:
        #     proveedor['prov_activo'] = 0

        return proveedor

	#Funcion que carga un proveedor en particular dentro de "Detalle del Producto"
    def setProveedor(self, proveedor):
        print (proveedor)
        self.vistaDetalle.prov_id.setText(str(proveedor[0]))
        self.vistaDetalle.prov_nombre.setText(proveedor[1])
        self.vistaDetalle.prov_razon_social.setText(proveedor[2])
        self.vistaDetalle.prov_cuit.setText(proveedor[3])
        self.vistaDetalle.prov_direccion.setText(proveedor[4])
        self.vistaDetalle.prov_nombre_contacto.setText(proveedor[5])
        self.vistaDetalle.prov_telefono.setText(proveedor[6])
        self.vistaDetalle.prov_telefono_dos.setText(proveedor[7])
        self.vistaDetalle.prov_email.setText(proveedor[8])
        self.vistaDetalle.prov_notas.setText(proveedor[9])
        # if proveedor[8]:
        #     self.vistaDetalle.prov_activo.setChecked(True)
        # else:
        #     self.vistaDetalle.prov_activo.setChecked(False)
        self.__haCambiado = False


    def resetProveedor(self):
        camposAResetear = self.vistaDetalle.findChildren(QLineEdit, self.rxProv)
        for campo in camposAResetear:
            campo.setText("")
        self.__haCambiado = False

    def resetCambios(self):
        self.__haCambiado = False

    def __activarBotones(self, snl):
        if snl:
            self.vistaDetalle.btn_nuevo.setEnabled(False)
            self.vistaDetalle.btn_modificar.setEnabled(True)
        else:
            self.vistaDetalle.btn_nuevo.setEnabled(True)
            self.vistaDetalle.btn_modificar.setEnabled(False)

    def __proveedorHaCmabiado(self):
        self.__haCambiado = True

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


    def operacionCompletada(self):
        if self.__haCambiado:
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Information)
           msg.setText("Operacion realizada con éxito")
           msg.setWindowTitle("Mensaje de confirmación")
           retval = msg.exec_()
