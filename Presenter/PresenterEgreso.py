# egreso_presenter.py

import Vistas.Egreso.VistaEgreso as EView
import Modelos.ModeloArticulo as AModel
import Modelos.ModeloEgreso as EModel
import Modelos.ModeloDestino as DModel
from PyQt5.QtCore import Qt, QModelIndex, QDate
from PyQt5.QtWidgets import QMessageBox
import datetime


class EgresoPresenter(object):
    def __init__(self):
        # self.model = PModel.ModeloEgreso()
        self.vista = EView.EgresoView(self)
        self.model = EModel.ModeloEgreso()
        self.desModel = DModel.ModeloDestino()
        self.artModel = AModel.ModeloArticulo(propiedades = ["Codigo", "Descripcion", "Stock"]) #Agregar Stock
        # self.vistaLista = PLView.ListaEgresosView(self)

        self.vista.tbl_egresos.setModel(self.model)
        self.model.dataChanged.connect(self.__sumador)
        self.vista.move_destino.setModel(self.desModel)
        # self.vistaLista.tbl_egresos.setModel(self.model)
        self.vista.tbl_articulos.setModel(self.artModel)

        self.vista.btn_buscar.clicked.connect(self.__buscarArticulosDisponibles)
        self.vista.btn_guardar.clicked.connect(self.crearEgreso)
        self.vista.buscador.returnPressed.connect(self.__buscarArticulosDisponibles)

        self.vista.ope_legajo.returnPressed.connect(self.__buscarOperario)
        self.headerPrincipal = self.vista.tbl_egresos.horizontalHeader()
        # hoy = datetime.date.today()
        #
        # self.vista.egr_fecha.setDate(QDate(hoy))
        self.__reiniciarFecha()
        self.vista.show()
        # self.activarBotones()
        self.__redimensionarTablaPrincipal()

    def crearEgreso(self):
        operario = self.vista.getOperario()
        detalles = self.vista.getDetalles()

        if not operario[1]:
            self.mensajeDeError("Error: Falta operario")
            return False
        if not detalles[0]:
            self.mensajeDeError("Error: Falta Destino")
            return False

        if self.model.crearEgreso(operario[0], detalles):
            self.restarStockAticulos()
            self.reiniciarMenu()

    def deshabilitarEgreso(self):
        egreso = self.vista.getEgreso()
        # self.model.toggleEgresoActivo(egreso)

    def restarStockAticulos(self):
        articulos = self.model.getArticulos()
        print (articulos)
        for articulo in articulos:
            stock_actual = self.artModel.verDetallesArticulo(campos = ["art_stock_actual"], condiciones = [("art_id", "=", articulo[0])])
            articulo = {
                "art_id" : articulo[0],
                "art_stock_actual" : stock_actual[0] - articulo[1]
            }
            print("/n/nSTOCK PREVIO A LA RESTA DE STOCK ACTUAL: ", stock_actual[0])
            print("/n/nSTOCK ACTUAL ACTUAL: ", articulo["art_stock_actual"])
            index = 0
            articulo = self.artModel.modificarArticulo(articulo, index)
            print("Se ha logrado la modificacion")
            # self.__redimensionarTablaBusqueda()
        # self.__redimensionarTablaBusqueda()

    def __buscarArticulosDisponibles(self):

        destino = self.vista.move_destino.currentIndex()
        busqueda = self.vista.buscador.text()
        try:
            busqueda = int(busqueda)
            condiciones = [("art_stock_actual", ">", 0), ("art_id", "=", busqueda)]
        except:
            condiciones = [("art_stock_actual", ">", 0), ("art_descripcion", "LIKE", "'%{}%'".format(busqueda))]
        # if  destino != 0:
        #     condiciones.append(("art_destino", "=", destino))
        if self.artModel.verListaArticulos(condiciones = condiciones):
            self.__redimensionarTablaBusqueda()

    def __buscarOperario(self):
        operario = self.vista.getOperario()
        opeLeg = operario[0]
        operario = {}

        if opeLeg:
            operario = self.model.buscarOperario(campos = ("ope_legajo", "ope_nombre", "ope_apellido"), condiciones = [("ope_legajo", " = ", opeLeg)])
        if operario:
            self.vista.setOperario(operario)
        else:
            self.vista.resetOperario()
        # self.__redimensionarTablaPrincipal()

    def __sumador(self):
        self.__totalArticulos = 0

        movimientos = self.model.getMovimientos()

        for movimiento in movimientos:
            if type(movimiento[2]) == str:
                continue
            self.__totalArticulos += movimiento[2]
        self.vista.setTotal(self.__totalArticulos)

    def reiniciarMenu(self):
        self.vista.resetEgreso()
        self.artModel.reiniciarTabla()
        self.model.reiniciarTablaEgreso()
        self.__reiniciarFecha()

    def __reiniciarFecha(self):
        hoy = datetime.date.today()

        self.vista.egr_fecha.setDate(QDate(hoy))

    def __redimensionarTablaPrincipal(self):
        self.headerPrincipal.resizeSection(0, 50)
        self.headerPrincipal.resizeSection(2, 100)
        self.headerPrincipal.setSectionResizeMode(1, 1)

    def __redimensionarTablaBusqueda(self):
        self.headerBusqueda = self.vista.tbl_articulos.horizontalHeader()

        self.headerBusqueda.resizeSection(0, 50)
        self.headerBusqueda.resizeSection(2, 50)
        self.headerBusqueda.setSectionResizeMode(1, 1)

    def mensajeDeError(self, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(mensaje)
        msg.setWindowTitle("Error")
        retval = msg.exec_()
