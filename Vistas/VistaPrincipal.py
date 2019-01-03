from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QStringListModel

class VistaPrincipal(QtWidgets.QMainWindow):

    def __init__(self, presenter, parent = None):
        super(VistaPrincipal, self).__init__()

        data = ["Proveedores", "Articulos", "Ingreso de Factura", "Salida de articulos",  "Informes", "Operarios", "Configuracion"]
        model = QStringListModel(data)

        main = uic.loadUi("gui/main.ui", self)
        # main.menu_navegacion.setModel(model)
        #
        # contenido = QtWidgets.QStackedWidget()
        # # contenido.addWidget(vistaArticulo)
        #
        # print(main.menu_navegacion.currentIndex())
        # main.contenido = contenido
        # main.contenido.setCurrentIndex(2)
