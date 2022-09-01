#from distutils.debug import DEBUG
#from distutils.log import debug

class ConfigDesarrollo():
    DEBUG=True #se reinicia el servidor automatic cuando se hace un cambio
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'mysqlnico'
    MYSQL_DB = 'curso'

#Creacion diccionario
configuracion = {
    'desarrollo': ConfigDesarrollo
}