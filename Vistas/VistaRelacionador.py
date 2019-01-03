# VistaRelacionador.py

from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import QRegExp, Qt

class RelacionadorView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(RelacionadorView, self).__init__(parent)

        self.vista = uic.loadUi("gui/dialogos/dialogo_relacionador.ui", self)

        self.vista.btn_cancelar.clicked.connect(self.close)

    def setTitulo(self, titulo):
        self.vista.grupo.setTitle(titulo.capitalize() + " disponibles")
        self.vista.setWindowTitle("Relacionador de articulo y proveedor")

    def getBusqueda(self):
        return self.vista.buscador.text()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
