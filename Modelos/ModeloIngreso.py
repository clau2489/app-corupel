# ingreso.py

from PyQt5 import QtCore
from mysql.connector import errorcode
from datetime import date
from lib.db import querier

import cerberus, decimal, mysql.connector
# from lib import Validator

class ModeloIngreso(QtCore.QAbstractTableModel):

    # db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "ingresos", prefijo = "ing_")
    __querierMovi = querier.Querier( tabla = "movimientos_ingreso", prefijo = "movi_")
    __querierArt = querier.Querier( tabla = "articulos", prefijo = "art_")
    __querierProv = querier.Querier( tabla = "proveedores", prefijo = "prov_")
    __querierComp = querier.Querier( tabla = "comprobantes", prefijo = "comp_")

    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloIngreso, self).__init__()

        self.__scIngreso = {
        'ing_id' : {'type' : 'integer', 'max' : 9999999999999999 },
        'ing_fecha' : {'type' : 'date' },
        'prov_id' : {'type' : 'integer', 'max' : 9999999999999999 }
        }

        self.__scMovIngreso = {
        'movi_id' : { 'type' : 'integer', 'max' : 9999999999999999 },
        'ing_id' : { 'type' : 'integer', 'max' : 9999999999999999 },
        'art_id' : { 'type' : 'integer', 'max' : 9999999999999999 },
        'movi_canitdad' : { 'type' : 'integer' },
        'movi_restante' : { 'type' : 'integer' },
        'movi_costo' : { 'type' : 'decimal' }
        }

        self.__scComprobante = {
        'comp_id' : { 'type' : 'integer', 'max' : 9999999999999999 },
        'ing_id' : { 'type' : 'integer', 'max' : 9999999999999999 },
        'comp_tipo' : { 'type' : 'string', 'allowed' : ['A', 'B', 'C', 'R'] },
        'comp_prefijo' : { 'type' : 'integer', 'max' : 9999999999999999 },
        'comp_fecha' : { 'type' : 'integer' },
        'comp_numero' : { 'type' : 'integer' }
        }

        self.__headers = ["Codigo", "Descripcion", "Cantidad", "Costo"]

        self.__movimientos = [["", "", "", ""]]
        self.ingreso = {}
        self.__proveedor = {}

    def crearIngreso(self, proveedor, comprobantes):
        # print(self.__v.validate(ingresoNuevo, self.__scIngreso))
        # print("ERRORES: ",self.__v.errors)
        if len(self.__movimientos) == 1:
            return False

        hoy = date.today()

        ingreso = { 'ing_fecha' : hoy, 'prov_id' : proveedor }

        for comprobante in comprobantes:
            print("ESTO ES EL COMPROBANTE: ", comprobante)
            compValidator = self.__querierComp.traerElementos(
                condiciones = [("comprobantes.comp_prefijo", " = ", "'{}'".format(comprobante['comp_prefijo'])),
                    ("comprobantes.comp_numero", " = ", "'{}'".format(comprobante['comp_numero']))])
            print(compValidator)
            if compValidator:
                return (False)

        self.__querier.insertarElemento(ingreso)
        ingId = self.__querier.traerElementos(campos = ["ing_id"], orden = ("ing_id", "DESC"), limite = 1)

        ingId = ingId[0][0]
        for comprobante in comprobantes:
            comprobante['ing_id'] = ingId
            self.__querierComp.insertarElemento(comprobante)
        for movimiento in self.__movimientos:
            if movimiento[2] == 0:
                continue
            movimiento = { 'art_id': movimiento[0],
            'ing_id' : ingId,
            'movi_cantidad' : movimiento[2],
            'movi_restante' : movimiento[2],
            'movi_costo' : movimiento[3]
            }

            if not movimiento['art_id']:
                continue
            self.__querierMovi.insertarElemento(movimiento)
        return True


    def verListaIngresos(self, campos = None, condiciones = None, limite = None):
        if not campos:
            campos = self.__busqueda

        self.__movimientos = self.__querier.traerElementos(campos, condiciones, limite)
        self.layoutChanged.emit()

    def verDetallesIngreso(self, ingreso, campos = None, condiciones = None):
        ingreso = self.__movimientos[ingreso.row()]
        condiciones = [('ing_id', '=', ingreso[0])]
        resultado = self.__querier.traerElementos(campos, condiciones, 1)
        self.ingreso = resultado[0]
        return self.ingreso

    def modificarIngreso(self, ingreso):
        self.__querier.actualizarIngreso(ingreso)

    def toggleIngresoActivo(self, ingreso):
        if ingreso['ing_activo']:
            ingreso['ing_activo'] = 0
        else:
            ingreso['ing_activo'] = 1
        self.__querier.actualizarIngreso(ingreso)

    def buscarProveedor(self, campos = None, condiciones = None):
        self.__proveedor = {}
        resultado = self.__querierProv.traerElementos(campos, condiciones)
        print("BUSCOOOO")
        if resultado:
            self.reiniciarTablaIngreso()
            self.__proveedor = resultado[0]
            print("PROVEEEEEEE ", self.__proveedor)
        return self.__proveedor

    def getMovimientos(self):
        return self.__movimientos

    def hayMovimientos(self):
        if len(self.__movimientos) == 1:
            return False
        for movimiento in self.__movimientos:
            print("LA CANTIDAD DE UNIDADES DEL ARTICULO ES: ", movimiento[2])
            if not (movimiento[2] == '0' or movimiento[2] == ''):
                return True
        return False

    def reiniciarTablaIngreso(self):
        self.removeRows()

    def getArticulos(self):
        articulos = []
        for movimiento in self.__movimientos:
            if movimiento[0] == '': continue
            articulos.append((movimiento[0], movimiento[2]))
        return articulos

# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.__movimientos)

    def columnCount(self, parent):
        if self.__movimientos:
            return len(self.__movimientos[0])
        else:
            return 0

    def flags(self, index):
        columna = index.column()
        fila = index.row()

        if (columna == 2 or columna == 3) and self.__movimientos[fila][0]:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        if columna == 0:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__movimientos[row][column]
            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()



            self.__articulo = {}
            if self.__proveedor:
                provId = self.__proveedor[0]
            if column == 0:
                for articulo in self.__movimientos:
                    if value == str(articulo[0]):
                        return (False)
                try:
                    value = int(value)
                    resultado = self.__querierArt.traerElementos(campos = ("art_id", "art_descripcion"),
                        condiciones = [("art_id", " = ", value), ("articulos_de_proveedores.proveedor", " = ", provId)],
                        uniones = [['articulos_de_proveedores', '`articulos`.`art_id` = `articulos_de_proveedores`.`articulo`']])
                    self.__articulo = list(resultado[0])
                    self.__articulo.append(0)
                    self.__articulo.append(0)
                except:
                    return False
                if not self.__movimientos[row][0]:
                    self.insertRows(self.rowCount(self), 1)
                else:
                    self.__movimientos[row] = self.__articulo
                self.dataChanged.emit(index, index)
                return True
            elif column == 3:
                try:
                    decvalue = decimal.Decimal(value)
                    if decvalue <= 0:
                        return False
                except:
                    return False
            else:
                try:
                    value = int(value)
                    if value < 0:
                        return False
                except:
                    return False
            self.__movimientos[row][column] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]

    def insertRows(self, row, count, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.__movimientos.insert(row, self.__articulo)
        self.endInsertRows()

    def removeRows(self, row = 1, parent = QtCore.QModelIndex()):
        last = self.rowCount(parent) - 1
        self.beginRemoveRows(parent, row, last)
        self.__movimientos = [["", "", "", ""]]
        # self.dataChanged.emit()
        self.endRemoveRows()
