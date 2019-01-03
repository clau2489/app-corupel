# comprobante.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier
import cerberus
# from lib import Validator


# Cambios para github solamente de prueba.

class ModeloComprobante(QtCore.QAbstractTableModel):

    # db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "comprobantes", prefijo = "comp_")
    __v = cerberus.Validator()


    def __init__(self, propiedades = None, parent = None):
        super(ModeloComprobante, self).__init__()

        self.__scComprobante = {
        'comp_id' : {'type' : 'integer', 'max' : 9999999999999999 },
        'comp_prefijo' : {'type' : 'string', 'maxlength' : 10 },
        'comp_numero' : {'type' : 'integer', 'max' : 99999999999999999999 },
        'comp_fecha' : {'type' : 'date' },
        'ing_id' : {'type' : 'integer', 'max' : 9999999999999999 },
        }


        self.__busqueda
        for componente in self.__scComprobante:

            self.__busqueda.append(componente)

        self.comprobantes = self.__querier.traerComprobantes(self.__busqueda)
        self.comprobante = {}

    def crearComprobante(self, comprobanteNuevo):
        v = self.__v.validate(comprobanteNuevo, self.__scComprobante)
        if v:

            self.__querier.insertarComprobante(comprobanteNuevo)
        else:
            print("ERRORES: ",self.__v.errors)
        return v

    def verDetallesComprobante(self, comprobante, campos = None, condiciones = None):
        comprobante = self.comprobantes[comprobante.row()]
        condiciones = [('comp_id', '=', comprobante[0])]
        resultado = self.__querier.traerComprobantes(campos, condiciones, 1)
        self.comprobante = resultado[0]
        return self.comprobante

    def modificarComprobante(self, comprobante):
        self.__querier.actualizarComprobante(comprobante)

    def toggleComprobanteActivo(self, comprobante):
        if comprobante['comp_activo']:
            comprobante['comp_activo'] = 0
        else:
            comprobante['comp_activo'] = 1
        self.__querier.actualizarComprobante(comprobante)

# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.comprobantes)

    def columnCount(self, parent):
        if self.comprobantes:
            return len(self.comprobantes[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.comprobantes[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.comprobantes[row][column]

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
