# proveedor_view.py
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFormLayout, QSizePolicy
from PyQt5.QtCore import pyqtSignal

class ListaProveedoresView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(ListaProveedoresView, self).__init__(parent)
        # Todos los Widgets de PyQT deben ser privados,
        # esto se logra NO COLOCANDO 'self.' sino la variable localmente.

        mainWindow = uic.loadUi("gui/listas/proveedores_lista.ui", self)
        mainWindow.tbl_proveedores.horizontalHeader().setStretchLastSection(True)

        # pol = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        # mainWindow.setSizePolicy(pol)
