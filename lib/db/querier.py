# querier.py
import mysql.connector
import socket
from mysql.connector import errorcode
# import config

class Querier(object):

    tabla = ""
    prefijo = ""

    conexion = {}

    def __init__(self, tabla, prefijo = "", usuario = None, password = None, host = None, database = None):
        self.prefijo = self.prefijo
        self.tabla = tabla

        self.user = "root"
        self.password = "admin1234"
        # self.host = "192.168.1.190"
        self.host = "127.0.0.1"
        self.database = "corupel"


# Esta funcion recibe un diccionario donde key = columna y value = valor
    def insertarElemento(self, elemento):

        consulta = "INSERT INTO {} (".format(self.tabla)
        valores = "VALUES ("
        for index, columna in enumerate(elemento.keys()):
            consulta += self.prefijo + columna
            valores += "%({})s".format(columna)
            if len(elemento) - 1 != index:
                consulta += ", "
                valores += ", "
        valores += ")"
        consulta += ") " + valores

        print("\nDEBUG - Consulta de insertar elemento:\n", consulta, "\n\n", elemento, "\n")
        self.__consultar(consulta, elemento)

    def actualizarElemento(self, elemento, condiciones = None):
        consulta = "UPDATE {} SET ".format(self.tabla)

        donde = ""

        total = len(elemento)-1

        for index, columna in enumerate(elemento.keys()):
            if (self.prefijo + "id") in columna.lower():
                # print("La columna: " + columna + " fue ignorada")
                donde = self.__agregarFiltros([(columna, " = ", elemento[columna])])
            consulta += "{}{} = %({}{})s".format(self.prefijo, columna, self.prefijo, columna)
            if index < total:
                consulta += ", "

        if condiciones:
            donde = self.__agregarFiltros(condiciones)

        consulta += donde

        print("\nDEBUG - Consulta actualizar elemento a mysql: ", consulta , "\n")
        self.__consultar(consulta, elemento)

    def traerElementos(self, campos = None, condiciones = None, limite = None, uniones = None, orden = None, groupby = None):
        # union debe ser una tupla o lista con dos elementos: union[0] es el nombre de la tabla, union[1] es
        # el conjunto de campos que deben conincidir en la union, ejemplo "`proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`"
        donde = ""
        consulta = "SELECT "

        consulta += self.__encampar(campos)

        consulta += " FROM {} ".format(self.tabla)
        if uniones:
            for union in uniones:
                consulta += self.__unirTabla(union[0], union[1])

        if condiciones:
            donde = self.__agregarFiltros(condiciones)
        consulta += donde

        if orden:
            consulta += " ORDER BY {} {}".format(orden[0], orden[1])

        if groupby:
            consulta += " GROUP BY {}".format(groupby[0])

        if limite:
            consulta += " LIMIT {}".format(limite)

        print("DEBUG - CONSULTA PARA VER ELEMENTOS: ", consulta)

        db = self.__conectar()
        cursor = db.cursor()

        cursor.execute(consulta)
        respuesta = cursor.fetchall()

        # print (respuesta)

        cursor.close()
        db.close()

        return respuesta

    def setConexion(self, user, password, host):
        self.user = user
        self.password = password
        self.host = host

    def agregarUsuario(self, username, password):
        hostname = socket.gethostname()
        grant = "GRANT SELECT, INSERT, UPDATE ON corupel.* TO '{}'@'{}' IDENTIFIED BY '{}'".format(self.user, hostname, self.password)

    def __unirTabla(self, tabla, on):
        union = "JOIN {} ON {} ".format(tabla, on)
        return union

    def __agregarFiltros(self, filtros):
        donde = "\nWHERE "

        totalFiltros = len(filtros)

        for index, filtro in enumerate(filtros):
            campo, condicion, valor = filtro
            donde += "{} {} {}".format(campo, condicion, valor)
            # campo + condicion + valor
            if index < totalFiltros-1:
                donde += "\nAND "
        # donde += campo + condicion + "%({})s".campo

        return donde

    def __encampar(self, campos):
        listaDeCampos = ""
        if campos:
            totalCampos = len(campos)
            for index, campo in enumerate(campos):
                listaDeCampos += "{}".format(campo)

                if index < totalCampos -1:
                    listaDeCampos += ", "
        else:
            listaDeCampos = " * "
        return listaDeCampos

    def __conectar(self):
        con = mysql.connector.connect(
            user = self.user, password = self.password,
            host = self.host, database = self.database)
        return con

    def __consultar(self, consulta, elemento):
        db = self.__conectar()
        cursor = db.cursor()
        try:
            if (type(elemento) != type({})):
                cursor.executeMany(consulta, elemento)
            else:
                cursor.execute(consulta, elemento)
            db.commit()
        except mysql.connector.Error as error:
            print("No se logro insertar el registro: ", error)
            db.rollback()
        cursor.close()
        db.close()
