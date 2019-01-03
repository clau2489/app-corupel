# elemento.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier
import cerberus
# from lib import Validator


# Cambios para github solamente de prueba.

class ModeloElemento(QtCore.QAbstractTableModel):

    # db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "elementos", prefijo = "elem_")
    __v = cerberus.Validator()


    def __init__(self, propiedades = None, parent = None):
        super(ModeloElemento, self).__init__()

        self.__scElemento = {
        'elem_id' : {'type' : 'integer' },
        'elem_columna1' : {'type' : 'string' },
        'elem_columna2' : {'type' : 'string' },
        'elem_columna3' : {'type' : 'string' },
        'elem_columna4' : {'type' : 'string' },
        }

        self.__propiedades = [
            'Codigo',
            'Columna 1',
            'Columna 2',
            'Columna 3',
            'Columna 4',
        ]

        if propiedades:
            self.__propiedades = propiedades

        self.relacion = {
            'Codigo' : 'elem_id',
            'Columna1' : 'elem_columna1',
            'Columna2' : 'elem_columna2',
            'Columna3' : 'elem_columna3',
            'Columna4' : 'elem_columna4',
        }

        self.__busqueda = []

        for propiedad in self.__propiedades:
            self.__busqueda.append(self.relacion[propiedad])

        self.elementos = self.__querier.traerElementos(self.__busqueda)
        self.elemento = {}

    def crearElemento(self, elementoNuevo):
        print(self.__v.validate(elementoNuevo, self.__scElemento))
        print("ERRORES: ",self.__v.errors)
        self.__querier.insertarElemento(elementoNuevo)

    def verListaElementos(self, campos = None, condiciones = None, limite = None):
        if not campos:
            campos = self.__busqueda

        self.elementos = self.__querier.traerElementos(campos, condiciones, limite)
        self.layoutChanged.emit()

    def verDetallesElemento(self, elemento, campos = None, condiciones = None):
        elemento = self.elementos[elemento.row()]
        condiciones = [('elem_id', '=', elemento[0])]
        resultado = self.__querier.traerElementos(campos, condiciones, 1)
        self.elemento = resultado[0]
        return self.elemento


    def modificarElemento(self, elemento):
        self.__querier.actualizarElemento(elemento)

    def toggleElementoActivo(self, elemento):
        if elemento['elem_activo']:
            elemento['elem_activo'] = 0
        else:
            elemento['elem_activo'] = 1
        self.__querier.actualizarElemento(elemento)

# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.elementos)

    def columnCount(self, parent):
        if self.elementos:
            return len(self.elementos[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.elementos[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.elementos[row][column]

            return value

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return self.__propiedades[section]

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows()
        self.endInsertRows()

    def insertColumns(self, position, columns, parent = QtCore.QModelIndex()):
        self.beginInsertColumns()
        self.endInsertColumns()

    def removeRows():
        self.beginRemoveRows()
        self.endRemoveRows()

    def removeColumns():

        self.beginRemoveColumns()
        self.endRemoveColumns()
