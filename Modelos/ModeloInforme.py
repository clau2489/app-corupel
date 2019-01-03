# informe.py

from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier
import cerberus

class ModeloInforme(QtCore.QAbstractTableModel):

    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloInforme, self).__init__()

        self.__busqueda = []

        self.__header = ["","","","",""]

        self.informe = [["", "", "", "", ""]]

    def traerInforme(self, filtros):
        # querier = {}

        tablas = ''
        campos = []
        condiciones = []
        unionones = []
        group = []

        print (filtros)

        if filtros['tipo'] == 1:
            campos = [
                "prov_nombre",
                "ing_fecha",
                "articulos.art_id",
                "art_descripcion",
                "art_agrupacion",
                "des_maquina",
                "movi_cantidad",
                "movi_costo",
                "movi_cantidad * movi_costo as total"
                ]

            # "ingresos.ing_fecha", "articulos.art_descripcion", "movimientos_ingreso.movi_cantidad", "movimientos_ingreso.movi_costo"]
            tablas = 'movimientos_ingreso'
            uniones =[
                ['ingresos',
                    "ingresos.ing_id = movimientos_ingreso.ing_id"],
                ['proveedores',
                    "proveedores.prov_id = ingresos.prov_id"],
                ['articulos',
                    "articulos.art_id = movimientos_ingreso.art_id"],
                ['destinos',
                    "destinos.des_id = articulos.art_destino"]
            ]
            condiciones = [
                ("ingresos.ing_fecha", "BETWEEN", "'{}' AND '{}'".format(filtros['desde'], filtros['hasta']))
                ]

            try:
                if filtros['agrupar']:
                    campos[6] = "SUM(movi_cantidad)"
                    group.append("articulos.art_id")
            except:
                pass
        elif filtros['tipo'] == 2:
            campos = [
                "articulos.art_id",
                "art_descripcion",
                "egr_fecha",
                "move_sector",
                "destinos.des_maquina",
                "move_cantidad",
                "egr_vale",
                "(select movi_costo from movimientos_ingreso where movimientos_ingreso.art_id = articulos.art_id limit 1) as costo"
                ]
            tablas = 'movimientos_egreso'
            uniones =[
                ['egresos',
                    "egresos.egr_id = movimientos_egreso.egr_id"],
                ['articulos',
                    "articulos.art_id = movimientos_egreso.art_id"],
                ['operarios',
                    "operarios.ope_legajo = egresos.ope_legajo"],
                ['destinos',
                    "destinos.des_id = movimientos_egreso.move_destino"]
            ]
            condiciones = [
                # ("articulos.art_id", "=", "movimientos_egreso.art_id"),
                ("egr_fecha", "BETWEEN", "'{}' AND '{}'".format(filtros['desde'], filtros['hasta']))

            ]

            try:
                if filtros['agrupar']:
                    campos[5] = "SUM(move_cantidad)"
                    group.append("articulos.art_id")
            except:
                pass
            # if filtros['agrupacion']:
            #     condiciones.append(("articulos.art_agrupacion", "LIKE", "'{}'".format(filtros['agrupacion'])))
            # if filtros['destino']:
            #     condiciones.append(("movimientos_egreso.move_destino", "=", filtros['destino']))
            # if filtros['tercero']:
            #     uniones.append(['operarios',
            #         "operarios.ope_legajo = egresos.ope_legajo"])
            #     condiciones.append(("operarios.ope_legajo", "=", filtros['tercero']))

        else:
            return False




        try:
            if filtros['articulo']:
                condiciones.append(("articulos.art_descripcion", "LIKE", "'%{}%'".format(filtros['articulo'])))
        except:
            pass
        try:
            if filtros['agrupacion']:
                condiciones.append(("articulos.art_agrupacion", "LIKE", "'{}'".format(filtros['agrupacion'])))
        except:
            pass
        try:
            if filtros['destino']:
                condiciones.append(("articulos.art_destino", "=", "'{}'".format(filtros['destino'])))
        except:
            pass
        try:
            if filtros['proveedor']:
                condiciones.append(("proveedores.prov_nombre", "=", "'{}'".format(filtros['proveedor'])))
        except:
            pass

        try:
            qr = querier.Querier(tabla = tablas)
            self.informe = qr.traerElementos(campos = campos,
                condiciones = condiciones,
                uniones = uniones,
                groupby = group
                )
            print("\n\n\nDEBUG - INFORME: ", self.informe)
            self.__acomodarInforme(tipo = filtros['tipo'])
        except:
            # print("ERROR - ", qr.errorcode())
            return False
        self.layoutChanged.emit()

    def __acomodarInforme(self, tipo):
        reinforme = []
        if tipo == 1:

            for item in self.informe:
                item = list(item)
                item[1] = str(item[1])
                item[7] = str(item[7])
                item[6] = str(item[6])
                item[8] = str(item[8])
                reinforme.append(item)
            self.__header = [
            "Proveedor",
            "Fecha",
            "Codigo de Articulo",
            "Descripcion de Articulo",
            "Agrupacion",
            "Destino",
            "Cantidad",
            "Costo",
            "Costo total"]
        elif tipo == 2:
            for item in self.informe:
                item = list(item)
                item[2] = str(item[2])
                item[5] = str(item[5])
                item[7] = str(item[7])
                reinforme.append(item)

            self.__header = [
            "Codigo de Articulo",
            "Descripcion de Articulo",
            "Fecha",
            "Agrupacion",
            "Destino",
            "Cantidad",
            "Numero de Vale",
            "Total"
            ]

        print(self.__header)
        self.informe = reinforme

    def getHeader(self):
        return self.__header

# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.informe)

    def columnCount(self, parent):
        if self.informe:
            return len(self.informe[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.informe[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.informe[row][column]

            return value

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return self.__header[section]

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows()
        self.endInsertRows()

    def removeRows():
        self.beginRemoveRows()
        self.endRemoveRows()
