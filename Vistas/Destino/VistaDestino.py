# destino_view.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import pyqtSignal, QRegExp, Qt



#Creamos la clase DestinoView
class DestinoView(QtWidgets.QWidget):

    rxDes = QRegExp("des_*")


	#Inicializamos el objeto
    def __init__(self, presenter, parent=None):
        super(DestinoView, self).__init__(parent)

        #Traemos el archivo .UI "Destinos_detalle"
        self.vistaDetalle = uic.loadUi("gui/detalles/destino_detalle.ui", self)

        rxId = QRegExp("[0-9]{0,16}")
        rxDesc = QRegExp(".{0,20}")

        #ocultamos los botones que no vamos a usar por el momento.
        self.vistaDetalle.btn_deshabilitar.hide()
        self.vistaDetalle.btn_imprimir.hide()

        #Conectamos el evento modificar y guardar con la funcion "operacionCOmpletada"
        self.vistaDetalle.btn_modificar.clicked.connect(self.operacionCompletada)
        self.vistaDetalle.btn_nuevo.clicked.connect(self.operacionCompletada)

        self.vistaDetalle.des_id.setValidator(QRegExpValidator(rxId))
        self.vistaDetalle.des_descripcion.setValidator(QRegExpValidator(rxDesc))

        self.vistaDetalle.des_id.textChanged.connect(self.activarBotones)

        self.activarBotones("")

        self.__haCambiado = False

        # Las siguientes líneas son para conectar los eventos en los
        # que los campos son modificados, en caso de modificarse alguno
        # levanto una bandera que me indica que se modificó un campo

        self.vistaDetalle.des_id.textChanged.connect(self.__destinoHaCambiado)
        self.vistaDetalle.des_maquina.textChanged.connect(self.__destinoHaCambiado)
        self.vistaDetalle.des_descripcion.textChanged.connect(self.__destinoHaCambiado)

    def getDestino(self):
        rawDestino = self.vistaDetalle.findChildren(QLineEdit, self.rxDes)
        destino = {}
        for componente in rawDestino:
                destino[componente.objectName()] = componente.text()
                # print(componente.objectName(), componente.text())
        if (destino['des_id']):
            destino['des_id'] = int(destino['des_id'])

        return destino

	#Funcion que carga un destino en pdesicular dentro de "Detalle del Producto"
    def setDestino(self, destino):
        self.vistaDetalle.des_id.setText(str(destino[0]))
        self.vistaDetalle.des_maquina.setText(destino[1])
        self.vistaDetalle.des_descripcion.setText(destino[2])

        # Cuando seteo un desículo, la bandera debe ponerse en FALSO
        self.__haCambiado = False

    def resetDestino(self):
        self.vistaDetalle.des_id.setText("")
        self.vistaDetalle.des_maquina.setText("")
        self.vistaDetalle.des_descripcion.setText("")

        # Cuando pongo todos los campos en blanco (no es una modificacion
        #de usuario), debo poner la bandera en FALSO
        self.__haCambiado = False

    def errorDeCampo(self, descripcion):
        label = QLabel(descripcion)
        layout = self.vistaDetalle.box_destino.findChild(QGridLayout)
        layout.addWidget(label)

    def activarBotones(self, snl):
        if snl:
            self.vistaDetalle.btn_nuevo.setEnabled(False)
            self.vistaDetalle.btn_modificar.setEnabled(True)
        else:
            self.vistaDetalle.btn_nuevo.setEnabled(True)
            self.vistaDetalle.btn_modificar.setEnabled(False)

    def __destinoHaCambiado(self):
        self.__haCambiado = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    #Esta es la funcion resetCambios que interactua con el archivo PresenterDestino
    def resetCambios(self):
        self.__haCambiado = False

    # El evento de cerrar ventana se dispara y verifica
    # que no haya sido modificado ningún campo
    def closeEvent(self, event):
        if not self.__haCambiado:
           event.accept()
           return
        resultado = QMessageBox.question(self, "Atencion", "No se guardarán los cambios. ¿Desea salir?", QMessageBox.Yes | QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()

    #ejemplo de dialogo
    def operacionCompletada(self):
        if self.__haCambiado:
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Information)
           msg.setText("Operacion realizada con éxito")
           msg.setWindowTitle("...")
           retval = msg.exec_()
