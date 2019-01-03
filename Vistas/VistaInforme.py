# VistaInforme.py

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

class InformeView(QtWidgets.QWidget):

    def __init__(self, presenter, parent=None):
        super(InformeView, self).__init__(parent)

        self.vista = uic.loadUi("gui/informes/informes.ui", self)

        # self.vista.filtro_movimiento_sp.currentIndexChanged.connect(self.setFiltrosSp)
        # self.vista.filtro_movimiento_av.currentIndexChanged.connect(self.setFiltrosAv)
        # self.setFiltros()

        # self.vista.tbl_informe.setColumnWidth(1, 600)

    def setFechas(self, desde, hasta):
        self.vista.fecha_desde_sp.setDate(QDate(desde))
        self.vista.fecha_hasta_sp.setDate(QDate(hasta))
        self.vista.fecha_desde_av.setDate(QDate(desde))
        self.vista.fecha_hasta_av.setDate(QDate(hasta))

    def getFiltrosAv(self):
        filtros = {}
        filtros['tipo'] = self.vista.filtro_movimiento_av.currentIndex()
        filtros['operario'] = self.vista.filtro_operario_av.text()
        if self.vista.filtro_proveedor_av.currentIndex():
            filtros['proveedor'] = self.vista.filtro_proveedor_av.currentText()
        if self.vista.filtro_destino_av.currentIndex():
            filtros['destino'] = self.vista.filtro_destino_av.currentIndex()
        if self.vista.filtro_agrupacion_av.currentIndex():
            filtros['agrupacion'] = self.vista.filtro_agrupacion_av.currentText()
        filtros['articulo'] = self.vista.filtro_articulo_av.text()
        filtros['agrupar'] = self.vista.filtro_agrupar_av.isChecked()
        filtros['desde'] = self.vista.fecha_desde_av.date()
        filtros['hasta'] = self.vista.fecha_hasta_av.date()
        return filtros

    def getFiltrosSp(self):
        filtros = {}
        filtros['tipo'] = self.vista.filtro_movimiento_sp.currentIndex()
        filtros['desde'] = self.vista.fecha_desde_sp.date()
        filtros['hasta'] = self.vista.fecha_hasta_sp.date()
        return filtros

    # def setFiltros(self):
    #     proveedor = self.vista.filtro_proveedor_av
    #     operario = self.vista.filtro_operario_av
    #     destino = self.vista.filtro_destino_av
    #     agrupacion = self.vista.filtro_agrupacion_av
    #     articulo = self.vista.filtro_articulo_av
    #
    #     destino.setCurrentIndex(0)
    #     agrupacion.setCurrentIndex(0)
    #     articulo.setText("")
    #     tercero.setText("")
