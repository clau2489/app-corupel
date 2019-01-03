# VistaConfiguracion.py

from PyQt5 import QtWidgets, uic
# from PyQt5.QtWidgets import QFormLayout, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import QRegExp

#Creamos la clase ElementoView
class ConfiguracionView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(ConfiguracionView, self).__init__(parent)

        self.vista = uic.loadUi("gui/configuracion.ui", self)

    def getConfig(self):
        config = {
            'host': self.vista.host.text(),
            'database': self.vista.database.text(),
            'user': self.vista.user.text(),
            'password': self.vista.password.text()
        }

        return config

    def setConfig(self, config):
        if config:
            self.vista.host.setText(config['host'])
            self.vista.database.setText(config['database'])
            self.vista.user.setText(config['user'])
            self.vista.password.setText(config['password'])
