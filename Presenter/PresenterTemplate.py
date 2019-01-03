# elemento_presenter.py

import Vistas.Elemento.VistaElemento as PView
import Vistas.Elemento.VistaListaElementos as PLView
import Modelos.ModeloElemento as EModel
# import Modelos.ModeloArticulo as AModel
from PyQt5.QtCore import Qt, QModelIndex


class ElementoPresenter(object):
    def __init__(self):
        self.model = PModel.ModeloElemento()
        self.vistaDetalle = PView.ElementoView(self)
        self.vistaLista = PLView.ListaElementosView(self)

        self.vistaLista.tbl_elementoes.setModel(self.model)
        self.vistaLista.tbl_elementoes.doubleClicked.connect(self.verDetalles)

        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearElemento)
        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarElemento)
        # self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarElemento)

        self.vistaLista.ln_buscar.returnPressed.connect(self.verElementos)
        self.vistaLista.btn_buscar.clicked.connect(self.verElementos)
        self.vistaLista.btn_nuevo.clicked.connect(self.verNuevo)
        # self.verElementos(limite = 5)

        self.vistaDetalle.elem_id.returnPressed.connect(self.__refrescar)

        self.vistaLista.show()

        self.activarBotones()

    def verElementos(self, campos = None, condiciones = None, limite = None):
        texto = self.vistaLista.ln_buscar.text()
        texto = "'%{}%'".format(texto)
        condiciones = [('elem_nombre', ' LIKE ', texto)]
        self.model.verListaElementos(campos, condiciones, limite)

    def verNuevo(self):
        self.vistaDetalle.resetElemento()
        self.verDetalles()

    def verDetalles(self, elemento = None):
        if elemento:
            elemento = self.model.verDetallesElemento(elemento)
            self.vistaDetalle.setElemento(elemento)
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', elemento[0])])

        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearElemento(self):
        elemento = self.vistaDetalle.getElemento()
        elemento['elem_id'] = None
        self.model.crearElemento(elemento)

    def modificarElemento(self):
        elemento = self.vistaDetalle.getElemento()
        self.model.modificarElemento(elemento)
        self.verElementos()

    def deshabilitarElemento(self):
        elemento = self.vistaDetalle.getElemento()
        self.model.toggleElementoActivo(elemento)

    def __refrescar(self):
        elemId = self.vistaDetalle.elem_id.text()
        elemento = {}
        if elemId:
            elemento = self.model.verDetallesElemento(elemento = QModelIndex(), condiciones = [('elem_id', ' = ', elemId)])
            # self.artModel.verListaArticulos(condiciones = [('elem_id', ' = ', elemId)])
            if elemento:
                self.vistaDetalle.setElemento(elemento)
        if not elemento:
            self.vistaDetalle.resetElemento()
