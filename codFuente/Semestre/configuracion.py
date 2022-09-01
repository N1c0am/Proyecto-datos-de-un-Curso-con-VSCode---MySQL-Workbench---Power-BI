#from distutils.debug import DEBUG
#from distutils.log import debug


class ConfigDesarrollo():
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'mysqlnico'
    MYSQL_DB = 'curso'

configuracion = {
    'desarrollo': ConfigDesarrollo
}