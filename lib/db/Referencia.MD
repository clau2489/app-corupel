# Referencia de la librería querier.py

La presente es una lista de las funciones y las variables miembro de la clase Querier

## Miembros de la clase Querier:

- tabla = string
- prefijo = string
- conexion = objeto de conexion (ver mysql.connector)

## Funciones de la clase Querier

##### Querier(tabla, prefijo, usuario, password, host, database)

Esta funcion es el constructor del objeto Querier

Parámetros:

| Variable  | Tipo      | Valor por Defecto |
| ----------|---------- | ------------------|
| tabla     | string    | Obligatorio       |
| prefijo   | string    | ""                |
| usuario   | string    | root              |
| password  | string    | admin1234         |
| host      | string    | 127.0.0.1         |
| database  | string    | database          |

##### insertarElemento(elemento)
##### traerElemento(elemento)
##### traerElementos(campos, condiciones, limite, uniones, orden)

| Parámetro   | Tipo                | Valor por Defecto |
| ------------|---------------------|-------------------|
| campos      | [string, ]          | Ninguno           |
| condiciones | [(str, str, str), ] | Obligatorio       |
| limite      | string              | Obligatorio       |
| uniones     | string              | Obligatorio       |
| orden       | (string, string)    | Ninguno           |


##### actualizarElemento(elemento)
##### unirTabla()

### Métodos privados
##### __agregarFiltros(elemento)
##### __encampar(elemento)
##### __conectar(elemento)
##### __consultar(elemento)
##### __conectar(elemento)
