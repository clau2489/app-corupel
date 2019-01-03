from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from lib.db import querier
import cerberus

class ModeloTablaDestino(QtCore.QAbstractTableModel):
    __v = cerberus.Validator()

    def __init__(self, parent = None):
        super(ModeloTablaDestino, self).__init__()
        self.__querier = querier.Querier(tabla = "destinos", prefijo = "des_")

        self.__scDestino = {
        'des_id' : {'type' : 'integer', 'nullable' : True},
        'des_maquina' : {'type' : 'string'},
        'des_descripcion' : {'type' : 'string'}
        }

        self.__header = ["Codigo", "Destino", "Observaciones"]
        self.__destinos = ["", "", ""]
        self.destino = {}
        try:
            resultados = self.__querier.traerElementos(campos = ["des_id", "des_maquina", "des_descripcion"] )
            # print("Resultados: ", resultados)
            for resultado in resultados:
                self.__destinos.append(resultado[0])
            self.layoutChanged.emit()

        except:
            # mensaje el observer que hay un error, guardarlo en el log de errores y cerrar
            print('ERROR - No se pudieron levantar los destinos')
        self.verListaDestinos()

    def verListaDestinos(self, campos = None, condiciones = None, limite = None):
        self.__destinos = self.__querier.traerElementos(campos, condiciones, limite)
        self.layoutChanged.emit()

    def verDetallesDestino(self, destino = QtCore.QModelIndex(), campos = None, condiciones = None):

        if destino.row() >= 0:
            destino = self.__destinos[destino.row()]
            desId = destino[0]
        if not condiciones:
            condiciones = [('des_id', '=', desId)]
        resultado = self.__querier.traerElementos(campos, condiciones, 1)
        if resultado:
            self.destino = resultado[0]
        else:
            return None
        return self.destino

    def modificarDestino(self, destino):
        v = self.__v.validate(destino, self.__scDestino)
        if v:
            self.__querier.actualizarElemento(destino)
        else:
            print("ERRORES: ", self.__v.errors)
        return v

    def crearDestino(self, destinoNuevo):
        v = self.__v.validate(destinoNuevo, self.__scDestino)
        if v:
            self.__querier.insertarElemento(destinoNuevo)
        else:
            print("ERRORES: ",self.__v.errors)
        return v

# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================

    def rowCount(self, parent):
        return len(self.__destinos)

    def columnCount(self, parent):
        if self.__destinos:
            return len(self.__destinos[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            fila = index.row()
            columna = index.column()
            valor = self.__destinos[fila][columna]

            return valor

    def setData(self, index, valor, role = QtCore.Qt.EditRole):

        if role == QtCore.Qt.EditRole:
            fila = index.row()
            columna = index.column()
            valor = self.__destinos[fila][columna]

            return valor

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return self.__header[section]
