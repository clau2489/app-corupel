# operario.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier
import cerberus
# from lib import Validator


# Cambios para github solamente de prueba.

class ModeloOperario(QtCore.QAbstractTableModel):

    # db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "operarios", prefijo = "ope_")
    __v = cerberus.Validator()


    def __init__(self, propiedades = None, parent = None):
        super(ModeloOperario, self).__init__()

        self.__scOperario = {
        'ope_legajo' : {'type' : 'integer' },
        'ope_nombre' : {'type' : 'string' },
        'ope_apellido' : {'type' : 'string' },
        'ope_puesto' : {'type' : 'string' },
        }

        self.__propiedades = [
            'Legajo',
            'Nombre',
            'Apellido',
            'Puesto'
        ]

        if propiedades:
            self.__propiedades = propiedades

        self.relacion = {
            'Legajo' : 'ope_legajo',
            'Nombre' : 'ope_nombre',
            'Apellido' : 'ope_apellido',
            'Puesto' : 'ope_puesto'
        }

        self.__busqueda = []

        for propiedad in self.__propiedades:
            self.__busqueda.append(self.relacion[propiedad])

        self.operarios = self.__querier.traerElementos(self.__busqueda)
        self.operario = {}

    def crearOperario(self, operarioNuevo):
        v = self.__v.validate(operarioNuevo, self.__scOperario)
        if v:
            self.__querier.insertarElemento(operarioNuevo)
        else:
            print("ERRORES: ", self.__v.errors)
        return v

    def verListaOperarios(self, campos = None, condiciones = None, limite = None):
        if not campos:
            campos = self.__busqueda

        self.operarios = self.__querier.traerElementos(campos, condiciones, limite)
        self.layoutChanged.emit()

    def verDetallesOperario(self, operario, campos = None, condiciones = None):
        operario = self.operarios[operario.row()]
        condiciones = [('ope_legajo', '=', operario[0])]
        resultado = self.__querier.traerElementos(campos, condiciones, 1)
        self.operario = resultado[0]
        return self.operario

    def modificarOperario(self, operario):
        v = self.__v.validate(operario, self.__scOperario)
        if v:
            self.__querier.actualizarElemento(operario, condiciones = [("ope_legajo", "=", operario['ope_legajo'])])
        else:
            print("ERRORES: ", self.__v.errors)
        return v

    def toggleOperarioActivo(self, operario):
        if operario['ope_activo']:
            operario['ope_activo'] = 0
        else:
            operario['ope_activo'] = 1
        self.__querier.actualizarElemento(operario)

# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.operarios)

    def columnCount(self, parent):
        if self.operarios:
            return len(self.operarios[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.operarios[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.operarios[row][column]

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
