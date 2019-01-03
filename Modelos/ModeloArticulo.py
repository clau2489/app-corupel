
from PyQt5 import QtCore
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime
from lib.db import querier
import cerberus
# from lib import Validator


# Cambios para github solamente de prueba.

class ModeloArticulo(QtCore.QAbstractTableModel):

    # db = mysql.connector.connect(user = 'admin', password = 'admin1234', host = '127.0.0.1', database = 'corupel')
    __querier = querier.Querier( tabla = "articulos", prefijo = "art_")
    __querierMovi = querier.Querier( tabla = "movimientos_ingreso", prefijo = "movi_")

    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloArticulo, self).__init__()

        self.__scArticulo = {
        'art_id' : {'type' : 'integer', 'nullable' : True },
        # 'prov_id' : {'type' : 'integer' },
        'art_cod_barras' : {'type' : 'string' },
        'art_descripcion' : {'type' : 'string' },
        'art_marca' : {'type' : 'string' },
        'art_agrupacion' : {'type' : 'string' },
        'art_stock_minimo' : {'type' : 'integer'},
        'art_destino' : {'type' : 'integer'},
        'art_stock_actual' : {'type' : 'integer'}
        # 'art_activo' : {'type' : 'integer' }
        }

        self.__propiedades = [
            'Codigo',
            # 'Proveedor',
            'Codigo de Barras',
            'Descripcion',
            'Marca',
            'Agrupacion',
            'Destino'
            'Stock mínimo'
            'Stock'
        ]

        if propiedades:
            self.__propiedades = propiedades

        self.relacion = {
            'Codigo' : 'art_id',
            # 'Proveedor' : 'prov_nombre',
            'Codigo de Barras' : 'art_cod_barras',
            'Descripcion' : 'art_descripcion',
            'Marca' : 'art_marca',
            'Agrupacion' : 'art_agrupacion',
            # 'art_stock_min', 'art_stock_actual',
            'Destino' : 'art_destino',
            'Stock' : 'art_stock_actual',
            'Stock mínimo' : 'art_stock_minimo',
            # 'Estado' : 'art_activo',
        }

        self.__costos = { 'primer_costo' : '0',
            'ultimo_costo' : '1',
            'costo_promedio' : '2'}

        self.__busqueda = []

        for propiedad in self.__propiedades:
            self.__busqueda.append(self.relacion[propiedad])

        # self.articulos = self.__querier.traerElementos(self.__busqueda)
        self.articulos = []
        self.articulo = {}

    def crearArticulo(self, articuloNuevo):
        print(articuloNuevo)
        v = self.__v.validate(articuloNuevo, self.__scArticulo)
        if v:
            self.__querier.insertarElemento(articuloNuevo)
        else:
            print("ERRORES: ",self.__v.errors)
        return v

        # Implementar ERRORCODE de MySQL y devolver errores

    def verListaArticulos(self, campos = None, condiciones = None, limite = None, uniones = None):
        if not campos:
            campos = self.__busqueda

        self.articulos = self.__querier.traerElementos(campos, condiciones, limite, uniones)
        if self.articulos:
            self.layoutChanged.emit()
            return True
        return False

    def verDetallesArticulo(self, articulo = QtCore.QModelIndex(), campos = None, condiciones = None):

        print (articulo)
        print (articulo.row())

        if articulo.row() >= 0:
            articulo = self.articulos[articulo.row()]
            artId = articulo[0]
        if not condiciones:
            print("DEBUG MSG: El contenido de articulo[0] es: ", artId)
            condiciones = [('art_id', '=', artId)]
        resultado = self.__querier.traerElementos(campos, condiciones, 1)
        if resultado:
            self.articulo = resultado[0]
        else:
            return None
        # print(self.articulo)
        return self.articulo


    def modificarArticulo(self, articulo, stockIx = None):
        v = self.__v.validate(articulo, self.__scArticulo)
        print("ARTICULOOO ", self.articulo)
        # if stockIx:
        #     print("ESTO ANDA?", self.stockActual(stockIx))
        #     if articulo['art_stock_actual'] < self.stockActual(stockIx):
        #         return False
        if v:
            self.__querier.actualizarElemento(articulo)
        else:
            print("ERRORES: ", self.__v.errors)
        return v

    def asociarProveedor(self, proveedor = { 'prov_nombre' : 'Indeterminado' }):
        # El ID de proveedor por defecto no debe ser 0000, sino el que sea creado para el proveedor con nombre "Indeterminado"

        prov_id = proveedor.fetchID()
        art_id = self.fetchID()

        if prov_id:
            QUERY = "UPDATE articulos SET prov_ID = " + prov_id
            + " WHERE articulos.art_ID = " + art_id
        else:
            print("El proveedor no existe")

    def deshabilitarArticulo(self, articulo):

        articulo['art_activo'] = 0
        self.__querier.actualizarElemento(articulo)

    def habilitarArticulo(self, articulo):
        articulo['art_activo'] = 1
        self.__querier.actualizarElemento(articulo)

    def verCostosArticulo(self, condiciones = None):
        costos = self.__querierMovi.traerElementos(campos = ["movi_costo "],
            condiciones = condiciones, orden=("movi_id","ASC"))
        if costos:

            self.__costos['primer_costo'] = str(costos[0][0])
            self.__costos['ultimo_costo'] = str(costos[len(costos)-1][1])
            costoTotal = 0
            for costo in costos:
                costoTotal += costo[0]
            self.__costos['costo_promedio'] = str(costoTotal/len(costos))
        # self.articulo.append(costos)
        return costos

    def getId(self):
        return self.articulo[0]

    def reiniciarTabla(self):
        self.articulos = []
        self.layoutChanged.emit()

    def stockActual(self, stockIx):
        return self.articulo[stockIx]

# ===============================================================
# Funciones para Modelo de tabla para PyQt
# ===============================================================
    def rowCount(self, parent):
        return len(self.articulos)

    def columnCount(self, parent):
        if self.articulos:
            return len(self.articulos[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.articulos[row][column]

            return value

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.articulos[row][column]

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

    def primerCosto(self):
        return self.__costos['primer_costo']

    def ultimoCosto(self):
        return self.__costos['ultimo_costo']

    def CostoPromedio(self):
        return self.__costos['costo_promedio']
