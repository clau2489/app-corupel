# PresenterRelacionador.py

import Vistas.VistaRelacionador as RView
import Modelos.ModeloRelacionador as RModel

class RelacionadorPresenter(object):
    def __init__(self, tipo, parent = None):
        self.model = RModel.ModeloRelacionador()
        self.vista = RView.RelacionadorView(self)
        self.vista.tabla_objetos.setModel(self.model)

        self.vista.buscador.returnPressed.connect(self.buscar)

        self.model.setTipo(tipo)
        self.vista.setTitulo(tipo)

        self.vista.btn_guardar.clicked.connect(self.guardar)

        self.vista.btn_guardar.clicked.connect(parent.refrescar)

    def buscar(self):
        busqueda = self.vista.getBusqueda()
        self.model.verLista(busqueda)

    def activar(self, idElemento):
        self.model.setId(idElemento)
        self.buscar()
        self.vista.show()

    def guardar(self):
        selmod = self.vista.tabla_objetos.selectionModel()
        fila = selmod.currentIndex().row()
        self.model.guardarRelacion(fila)
        self.vista.close()
