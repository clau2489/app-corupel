#__main__.py

import sys, os
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from Presenter import PresenterArticulo, PresenterProveedor, PresenterPrincipalOperario, PresenterPrincipal

root = os.path.dirname(os.path.abspath(__file__))

def main():
	#Instancia para iniciar una aplicación
    app = QtWidgets.QApplication(sys.argv)

    config = {
        'user' : 'root',
        'password' : 'admin1234',
        'host' : '127.0.0.1',
        'database' : 'corupel'
    }

    mainPresenter = PresenterPrincipal.PrincipalPresenter()
    # mainPresenter = PresenterPrincipalOperario.PrincipalPresenter()


	#Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
