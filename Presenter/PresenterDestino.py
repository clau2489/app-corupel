# destino_presenter.py

import Vistas.Destino.VistaDestino as DView
import Vistas.Destino.VistaListaDestinos as DLView
import Modelos.ModeloTablaDestino as DModel
# import Modelos.ModeloArticulo as AModel
from PyQt5.QtCore import Qt, QModelIndex


class DestinoPresenter(object):
    def __init__(self):
        self.model = DModel.ModeloTablaDestino()
        self.vistaDetalle = DView.DestinoView(self)
        self.vistaLista = DLView.ListaDestinosView(self)

        self.vistaLista.tbl_destinos.setModel(self.model)
        self.vistaLista.tbl_destinos.doubleClicked.connect(self.verDetalles)

        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearDestino)
        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarDestino)
        # self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarDestino)

        self.vistaLista.ln_buscar.returnPressed.connect(self.verDestinos)
        self.vistaLista.btn_buscar.clicked.connect(self.verDestinos)
        self.vistaLista.btn_nuevo.clicked.connect(self.verNuevo)
        # self.verDestinos(limite = 5)

        self.vistaDetalle.des_id.returnPressed.connect(self.__refrescar)

        self.vistaLista.show()

        # self.vistaDetalle.activarBotones()

    def verDestinos(self, campos = None, condiciones = None, limite = None):
        texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('des_maquina', ' LIKE ', texto)]
        self.model.verListaDestinos(campos, condiciones, limite)

    def verNuevo(self):
        self.vistaDetalle.resetDestino()
        self.verDetalles()

    def verDetalles(self, destino = None):
        if destino:
            destino = self.model.verDetallesDestino(destino)
            self.vistaDetalle.setDestino(destino)
            # self.artModel.verListaArticulos(condiciones = [('des_id', ' = ', destino[0])])

        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearDestino(self):
        destino = self.vistaDetalle.getDestino()
        destino['des_id'] = None
        if self.model.crearDestino(destino):
            self.verDestinos()
            self.vistaDetalle.resetCambios()
            self.vistaDetalle.close()

    def modificarDestino(self):
        destino = self.vistaDetalle.getDestino()
        if self.model.modificarDestino(destino):
            self.verDestinos()
            self.vistaDetalle.resetCambios()
            self.vistaDetalle.close()

    def deshabilitarDestino(self):
        destino = self.vistaDetalle.getDestino()
        self.model.toggleDestinoActivo(destino)

    def __refrescar(self):
        desId = self.vistaDetalle.des_id.text()
        destino = {}
        if desId:
            destino = self.model.verDetallesDestino(destino = QModelIndex(), condiciones = [('des_id', ' = ', desId)])
            # self.artModel.verListaArticulos(condiciones = [('des_id', ' = ', desId)])
            if destino:
                self.vistaDetalle.setDestino(destino)
        if not destino:
            self.vistaDetalle.resetDestino()
