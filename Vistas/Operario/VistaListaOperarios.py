# VistaListaOperarios.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal

class ListaOperariosView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(ListaOperariosView, self).__init__(parent)

        self.vistaLista = uic.loadUi("gui/listas/operarios_lista.ui", self)
