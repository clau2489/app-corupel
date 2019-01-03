# operario_presenter.py

import Vistas.Operario.VistaOperario as PView
import Vistas.Operario.VistaListaOperarios as PLView
import Modelos.ModeloOperario as OModel
from PyQt5.QtCore import Qt, QModelIndex


class OperarioPresenter(object):
    def __init__(self):
        self.model = OModel.ModeloOperario()
        self.vistaDetalle = PView.OperarioView(self)
        self.vistaLista = PLView.ListaOperariosView(self)

        self.vistaLista.tbl_operarios.setModel(self.model)
        self.vistaLista.tbl_operarios.doubleClicked.connect(self.verDetalles)

        self.vistaDetalle.btn_nuevo.clicked.connect(self.crearOperario)
        self.vistaDetalle.btn_modificar.clicked.connect(self.modificarOperario)
        # self.vistaDetalle.btn_deshabilitar.clicked.connect(self.deshabilitarOperario)

        # self.vistaDetalle.btn_nuevo.hide()
        # self.vistaDetalle.btn_modificar.hide()

        self.vistaLista.ln_buscar.returnPressed.connect(self.verOperarios)
        self.vistaLista.btn_buscar.clicked.connect(self.verOperarios)
        self.vistaLista.btn_nuevo.clicked.connect(self.verNuevo)
        # self.verOperarios(limite = 5)

        self.vistaDetalle.ope_legajo.returnPressed.connect(self.__refrescar)

        self.vistaLista.show()

        # self.activarBotones()

    def verOperarios(self, campos = None, condiciones = None, limite = None):
        busqueda = self.vistaLista.ln_buscar.text()
        condiciones = []
        try:
            busqueda = int(busqueda)
            condiciones = [("ope_legajo", "=", busqueda)]
        except:
            #HACKEADISIMO
            busqueda = "'%{}%' or ope_apellido LIKE '%{}%'".format(busqueda, busqueda)
            condiciones = [('ope_nombre', ' LIKE ', busqueda)]
        self.model.verListaOperarios(campos, condiciones, limite)

    def verNuevo(self):
        self.vistaDetalle.resetOperario()
        self.verDetalles()

    def verDetalles(self, operario = None):
        if operario:
            operario = self.model.verDetallesOperario(operario)
            self.vistaDetalle.setOperario(operario)

        self.vistaDetalle.show()
        self.vistaDetalle.activateWindow()

    def crearOperario(self):
        operario = self.vistaDetalle.getOperario()
        if self.model.crearOperario(operario):
            self.verOperarios()
            self.vistaDetalle.resetCambios()
            self.vistaDetalle.close()

    def modificarOperario(self):
        operario = self.vistaDetalle.getOperario()
        if self.model.modificarOperario(operario):
            self.verOperarios()
            self.vistaDetalle.resetCambios()
            self.vistaDetalle.close()

    def deshabilitarOperario(self):
        operario = self.vistaDetalle.getOperario()
        self.model.toggleOperarioActivo(operario)

    def __refrescar(self):
        opeLeg = self.vistaDetalle.ope_legajo.text()
        operario = {}
        if opeLeg:
            operario = self.model.verDetallesOperario(operario = QModelIndex(), condiciones = [('ope_legajo', ' = ', opeLeg)])
            # self.artModel.verListaArticulos(condiciones = [('ope_id', ' = ', opeLeg)])
            if operario:
                self.vistaDetalle.setOperario(operario)
        if not operario:
            self.vistaDetalle.resetOperario()
