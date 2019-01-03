# elemento_presenter.py

import Vistas.VistaAlerta as AlView
import Modelos.ModeloArticulo as AModel
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QHeaderView

class AlertaPresenter(object):
    def __init__(self):
        self.model = AModel.ModeloArticulo(propiedades = ["Codigo", "Descripcion", "Stock", "Stock mínimo"])
        self.vista = AlView.AlertaView(self)

        self.vista.tbl_articulos.setModel(self.model)

        self.vista.tbl_articulos.setColumnWidth(0, 50)
        self.vista.tbl_articulos.setColumnWidth(1, 350)
        # self.vista.tbl_articulos.horizontalHeader().setResizeMode(0, 1)
        self.header = self.vista.tbl_articulos.horizontalHeader()

        self.vista.btn_aceptar.clicked.connect(self.vista.close)

        self.verElementos()

    def verElementos(self, campos = None, condiciones = None, limite = None):
        campos = ["art_id", "art_descripcion", "art_stock_actual", "art_stock_minimo"]
        condiciones = [("art_stock_actual", "<" ,"art_stock_minimo"), ("art_activo","=","1")]
        self.model.verListaArticulos(campos, condiciones)
        self.header.resizeSection(0, 50)
        self.header.resizeSection(2, 50)
        self.header.resizeSection(3, 50)
        self.header.setSectionResizeMode(1, 1)
