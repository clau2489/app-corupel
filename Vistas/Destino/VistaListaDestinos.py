# VistaListaArticulos.py

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import pyqtSignal

class ListaDestinosView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(ListaDestinosView, self).__init__(parent)

        self.vistaLista = uic.loadUi("gui/listas/destinos_lista.ui", self)
