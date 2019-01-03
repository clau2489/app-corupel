# articulo_presenter.py

import Vistas.Articulo.VistaArticulo as AView
import Vistas.Articulo.VistaListaArticulos as ALView
import Modelos.ModeloArticulo as AModel
import Modelos.ModeloProveedor as PModel
import Modelos.ModeloDestino as DModel
import Presenter.PresenterRelacionador as RPresenter
from PyQt5.QtCore import Qt, QModelIndex


class ArticuloPresenter(object):
    def __init__(self):
        self.provModel = PModel.ModeloProveedor(propiedades = ["Codigo", "Nombre", "Teléfono"])
        self.model = AModel.ModeloArticulo(propiedades = ["Codigo", "Descripcion", "Marca", "Destino", "Stock"])
        self.desModel = DModel.ModeloDestino()

        self.vistaDetalle = AView.ArticuloView(self)
        self.vistaLista = ALView.ListaArticuloView(self)

        self.relacionador = RPresenter.RelacionadorPresenter("proveedores", self)

        self.vistaLista.tbl_articulos.setModel(self.model)


        self.vistaLista.tbl_articulos.doubleClicked.connect(self.verDetalles)

        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearArticulo)
        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarArticulo)
        self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarArticulo)
        self.vistaDetalle.btn_habilitar.clicked.connect(self.habilitarArticulo)
        self.vistaDetalle.art_id.returnPressed.connect(self.refrescar)
        self.vistaDetalle.tbl_proveedores.setModel(self.provModel)
        self.vistaDetalle.opcion_costo.currentIndexChanged.connect(self.__actualizarCostos)
        self.vistaDetalle.art_destino.setModel(self.desModel)
        self.vistaDetalle.art_stock_actual.returnPressed.connect(self.agregarStockExcp)

        # self.vistaDetalle.btn_nuevo.hide()
        # self.vistaDetalle.btn_modificar.hide()
        # self.vistaDetalle.btn_deshabilitar.hide()
        # self.vistaDetalle.btn_nuevo_prov.hide()

        self.vistaDetalle.btn_nuevo_prov.clicked.connect(self.__asociar)

        self.vistaLista.btn_nuevo.clicked.connect(self.nuevoArticulo)
        self.vistaLista.ln_buscar.returnPressed.connect(self.verArticulos)
        self.vistaLista.btn_buscar.clicked.connect(self.verArticulos)

        self.header = self.vistaLista.tbl_articulos.horizontalHeader()
        self.verArticulos()
        self.__redimensionarTabla()
        self.vistaLista.show()

    def verArticulos(self, campos = None, condiciones = None, limite = None):
        busqueda = self.vistaLista.ln_buscar.text()
        condiciones = []
        try:
            busqueda = int(busqueda)
            condiciones = [('art_id', "=", busqueda)]
        except:
            busqueda = "'%{}%'".format(busqueda)
            condiciones = [('art_descripcion', ' LIKE ', busqueda)]
        campos = ["art_id", "art_descripcion", "art_marca", "des_maquina", "art_stock_actual"]
        uniones = [("destinos", "articulos.art_destino = destinos.des_id")]
        self.model.verListaArticulos(campos, condiciones, limite, uniones)

        self.__redimensionarTabla()

    def verDetalles(self, articulo):
        if articulo:
            articulo = self.model.verDetallesArticulo(articulo)
            # costos = self.model.verCostosArticulo(condiciones = [('movimientos_ingreso.art_id', ' = ', articulo[0]), ('movimientos_ingreso.movi_restante', ' > ', 0)])
            totales = []
            # if costos:
            #     totales = self.__calcularTotales(costos)

            self.vistaDetalle.setArticulo(articulo)
            self.vistaDetalle.setTotales(totales)
            self.__actualizarCostos()
            self.provModel.verListaProveedores(condiciones = [("articulos_de_proveedores.articulo", " = ", articulo[0])], campos = ["prov_id", "prov_nombre", "prov_telefono"], uniones = [['articulos_de_proveedores', '`proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`']])

        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()
        self.__redimensionarTabla()

    def crearArticulo(self):
        # print("DEBUG - Tipo de objeto de artículo_ ", type(articulo))
        print("ESTO ANDA")
        articulo = self.vistaDetalle.getArticulo()
        print("DEBUG - Artículo: ", articulo)
        articulo['art_id'] = None
        # error =
        if self.model.crearArticulo(articulo):
            self.verArticulos()
            #Crear la funcion resetCambios que pone el estado de cambios en False
            self.vistaDetalle.resetCambios()
            #Cierra la Ventana
            self.vistaDetalle.close()
        self.__redimensionarTabla()

    def modificarArticulo(self):
        articulo = self.vistaDetalle.getArticulo()
        if self.model.modificarArticulo(articulo, 7):
            self.verArticulos()
            self.vistaDetalle.resetCambios()
            self.vistaDetalle.close()
        self.__redimensionarTabla()

    def deshabilitarArticulo(self):
        articulo = { 'art_id' : int(self.vistaDetalle.art_id.text())}
        print(articulo)
        self.model.deshabilitarArticulo(articulo)
        self.vistaDetalle.close()

    def habilitarArticulo(self):
        articulo = { 'art_id' : int(self.vistaDetalle.art_id.text())}
        print(articulo)
        self.model.habilitarArticulo(articulo)
        self.vistaDetalle.close()

    def nuevoArticulo(self):
        self.vistaDetalle.resetArticulo()
        self.vistaDetalle.show()

    def refrescar(self):
        artId = self.vistaDetalle.art_id.text()
        articulo = {}
        if artId:
            print("DEBUG - ART_ID = ", artId)
            articulo = self.model.verDetallesArticulo(condiciones = [('art_id', ' = ', artId)])
            costos = self.model.verCostosArticulo(condiciones = [('movimientos_ingreso.art_id', ' = ', artId)])
            totales = {}
            if costos:
                totales = self.__calcularTotales(costos)

            self.provModel.verListaProveedores(condiciones = [("articulos_de_proveedores.articulo", " = ", artId)],
                campos = ["prov_id", "prov_nombre", "prov_telefono"],
                uniones = [['articulos_de_proveedores', '`proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`']])
            if articulo:
                self.vistaDetalle.setArticulo(articulo)
                if totales:
                    self.vistaDetalle.setTotales(totales)
        if not articulo:
            self.vistaDetalle.resetArticulo()
        self.__redimensionarTabla()

    def agregarStockExcp(self):
        try:
            stock = int(self.vistaDetalle.art_stock_actual.text())
        except:
            stock = 0
        # stockModel = self.model.stockActual(7)
        # print("STOCKS: ", stock, stockModel)
        # if stock < stockModel:
        #     self.vistaDetalle.art_stock_actual.setText(str(stockModel))

    def __calcularTotales(self, costos):
        promedioCosto = 0
        ultimo = len(costos) - 1

        for cantidad in costos:
            promedioCosto += cantidad[1]

        promedioCosto /= len(costos)
        primerCosto = costos[0][1]
        ultimoCosto = costos[ultimo][1]

        return [primerCosto, promedioCosto, ultimoCosto]

    def __actualizarCostos(self):
        index = self.vistaDetalle.opcion_costo.currentIndex()
        if index == 0:
            self.vistaDetalle.comp_costo.setText(self.model.primerCosto())
        elif index == 1:
            self.vistaDetalle.comp_costo.setText(self.model.ultimoCosto())
        # elif index == 2:
        #     self.vistaDetalle.comp_costo.setText(self.model.CostoPromedio())

    def __asociar(self):
        idArticulo = self.model.getId()
        print("idArticulo contiene lo siguiente: ", idArticulo)
        self.relacionador.activar(idArticulo)

    def __redimensionarTabla(self):
        self.header.resizeSection(0, 50)
        self.header.resizeSection(2, 150)
        self.header.resizeSection(3, 150)
        self.header.resizeSection(4, 50)
        self.header.setSectionResizeMode(1, 1)
