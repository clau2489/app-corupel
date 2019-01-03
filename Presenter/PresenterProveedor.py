# proveedor_presenter.p

import Vistas.Proveedor.VistaProveedor as PView
import Vistas.Proveedor.VistaListaProveedores as PLView
import Modelos.ModeloProveedor as PModel
import Modelos.ModeloArticulo as AModel
import Presenter.PresenterRelacionador as RPresenter
from PyQt5.QtCore import Qt, QModelIndex


class ProveedorPresenter(object):
    def __init__(self):
        self.artModel = AModel.ModeloArticulo(propiedades = ["Codigo", "Descripcion", "Codigo de Barras"])
        self.model = PModel.ModeloProveedor()
        self.vistaDetalle = PView.ProveedorView(self)
        self.vistaLista = PLView.ListaProveedoresView(self)
        self.relacionador = RPresenter.RelacionadorPresenter("articulos", self)

        self.vistaLista.tbl_proveedores.setModel(self.model)
        self.vistaLista.tbl_proveedores.doubleClicked.connect(self.verDetalles)

        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearProveedor)
        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarProveedor)
        self.vistaDetalle.btn_nuevo_art.clicked.connect(self.__asociar)
        # self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarProveedor)

        # self.vistaDetalle.btn_nuevo.hide()
        # self.vistaDetalle.btn_modificar.hide()
        # self.vistaDetalle.btn_nuevo_art.hide()

        self.vistaLista.ln_buscar.returnPressed.connect(self.verProveedores)
        self.vistaLista.btn_buscar.clicked.connect(self.verProveedores)
        self.vistaLista.btn_nuevo.clicked.connect(self.verNuevo)
        # self.verProveedores(limite = 5)

        self.vistaDetalle.prov_id.returnPressed.connect(self.refrescar)

        self.vistaDetalle.tbl_articulos.setModel(self.artModel)
        self.selMod = self.vistaDetalle.tbl_articulos.selectionModel()
        # self.selMod.selectionChanged.connect(self.activarBotonesArticulos)

        self.vistaLista.show()

        # self.activarBotonesArticulos()

    def verProveedores(self, campos = None, condiciones = None, limite = None):
        busqueda = self.vistaLista.ln_buscar.text()
        condiciones = []
        try:
            busqueda = int(busqueda)
            condiciones = [("prov_id", "=", busqueda)]
        except:
            busqueda = "'%{}%'".format(busqueda)
            condiciones = [('prov_nombre', ' LIKE ', busqueda)]
        self.model.verListaProveedores(campos, condiciones, limite)

    def verNuevo(self):
        self.vistaDetalle.resetProveedor()
        self.verDetalles()

    def verDetalles(self, proveedor = None):
        if proveedor:
            proveedor = self.model.verDetallesProveedor(proveedor)
            self.vistaDetalle.setProveedor(proveedor)
            self.artModel.verListaArticulos(condiciones = [("articulos_de_proveedores.proveedor", " = ", proveedor[0])], campos = ["art_id", "art_descripcion", "art_cod_barras"], uniones = [['articulos_de_proveedores', '`articulos`.`art_id` = `articulos_de_proveedores`.`articulo`']])

        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearProveedor(self):
        proveedor = self.vistaDetalle.getProveedor()
        proveedor['prov_id'] = None
        if self.model.crearProveedor(proveedor):
            self.verProveedores()
            self.vistaDetalle.resetCambios()
            self.vistaDetalle.close()

    def modificarProveedor(self):
        proveedor = self.vistaDetalle.getProveedor()
        if self.model.modificarProveedor(proveedor):
            self.verProveedores()
            self.vistaDetalle.resetCambios()
            self.vistaDetalle.close()

    def deshabilitarProveedor(self):
        proveedor = self.vistaDetalle.getProveedor()
        self.model.toggleProveedorActivo(proveedor)

    def refrescar(self):
        provId = self.vistaDetalle.prov_id.text()
        proveedor = {}
        if provId:
            proveedor = self.model.verDetallesProveedor(proveedor = QModelIndex(), condiciones = [('prov_id', ' = ', provId)])
            self.artModel.verListaArticulos(condiciones = [("articulos_de_proveedores.proveedor", " = ", provId)], campos = ["art_id", "art_descripcion", "art_cod_barras"], uniones = [['articulos_de_proveedores', '`articulos`.`art_id` = `articulos_de_proveedores`.`articulo`']])
            if proveedor:
                self.vistaDetalle.setProveedor(proveedor)
        if not proveedor:
            self.vistaDetalle.resetProveedor()

    # def activarBotonesArticulos(self):
    #     if self.selMod.hasSelection():
    #         self.vistaDetalle.btn_deshabilitar_art.setEnabled(True)
    #     else:
    #         self.vistaDetalle.btn_deshabilitar_art.setEnabled(False)

    def __asociar(self):
        idProveedor = self.model.getId()
        print("idProveedor contiene lo siguiente: ", idProveedor)
        self.relacionador.activar(idProveedor)
