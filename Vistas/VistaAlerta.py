from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QStringListModel, Qt

class AlertaView(QtWidgets.QWidget):

    def __init__(self, presenter, parent = None):
        super(AlertaView, self).__init__(parent)

        # data = ["Proveedores", "Articulos", "Ingreso de Factura", "Salida de articulos",  "Informes", "Operarios", "Configuracion"]
        # model = QStringListModel(data)

        self.vista = uic.loadUi("gui/dialogos/alerta_reposicion.ui", self)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
