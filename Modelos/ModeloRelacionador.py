# ModeloRelacionador.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from lib.db import querier
import cerberus

class ModeloRelacionador(QtCore.QAbstractTableModel):

    __v = cerberus.Validator()


    def __init__(self, parent = None):
        super(ModeloRelacionador, self).__init__()

        # self.elementos = self.__querier.traerElementos(self.__busqueda)
        self.elementos = []
        self.elemento = {}
        self.tipo = ""
        self.busqueda = ""
        self.campos = []
        self.condiciones = [()]
        self.idElemento = {}

    def guardarRelacion(self, fila):

        articuloDeProv = {}
        if self.tipo == "articulos":
            articuloDeProv['proveedor'] = self.idElemento
            articuloDeProv['articulo'] = self.elementos[fila][0]
        elif self.tipo == "proveedores":
            articuloDeProv['articulo'] = self.idElemento
            articuloDeProv['proveedor'] = self.elementos[fila][0]
        print(articuloDeProv)
        q = querier.Querier( tabla = "articulos_de_proveedores", prefijo = "")
        q.insertarElemento(articuloDeProv)

    def verLista(self, busqueda):
        self.busqueda = busqueda
        if self.tipo == "articulos":
            self.condiciones = [("art_descripcion", "LIKE", "'%{}%'".format(busqueda))]
            # self.__setCondiciones("art_descripcion", "LIKE", "'%{}%'".format(busqueda))
        elif self.tipo == "proveedores":
# ESTE ES EL CODIGO MÁGICO QUE ME AYUDA A BUSCAR EN LA BASE DE DATOS POR CODIGO O POR NOMBRE, USAR PARA REPLICAR EN OTRAS BÚSQUEDAS
            try:
                self.busqueda = int(busqueda)
                self.condiciones = [("prov_id", "=", self.busqueda)]
                # self.__setCondiciones("prov_id", "=", self.busqueda)
            except:
                self.condiciones = [("prov_nombre", "LIKE", "'%{}%'".format(self.busqueda))]
                # self.__setCondiciones("prov_nombre", "LIKE", "'%{}%'".format(self.busqueda))
        try:
            self.elementos = self.__querier.traerElementos(self.campos, self.condiciones)
        except:
            print("ERROR")
        self.layoutChanged.emit()

    def setTipo(self, tipo):
        prefijo = ""
        self.tipo = tipo
        if tipo == "articulos":

            prefijo = "art_"
            self.campos = ["art_id", "art_descripcion"]
            self.__headers = ["Codigo", "Descripcion"]

        elif tipo == "proveedores":

            prefijo == "prov_"
            self.campos = ["prov_id", "prov_nombre"]
            self.__headers = ["Codigo", "Nombre"]

        self.__querier = querier.Querier( tabla = tipo, prefijo = prefijo)

    def setId(self, idElemento):
        self.idElemento = idElemento
        print("IDELEMENTO CONTIENE LO SIGUIENTE", self.idElemento)

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
                return self.__headers[section]
