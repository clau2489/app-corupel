# presenter_configuracion.py

import Vistas.VistaConfiguracion as CView
# import Modelos.ModeloElemento as EModel
from PyQt5.QtCore import Qt, QModelIndex
import socket

class ConfiguracionPresenter(object):
    # def __init__(self):
    #     pass

    def myIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(s.getsockname()[0])
        s.close()
