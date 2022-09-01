#from distutils.command.config import config

from urllib import request
from flask import Flask, jsonify, request
#importar diccionario configuracion
from configuracion import configuracion
from flask_mysqldb import MySQL
from validacionSemestre import *
from datetime import *
from csv import *

aplicacionSemestre = Flask(__name__)

conexion = MySQL(aplicacionSemestre)

@aplicacionSemestre.route('/semestre', methods=['GET']) 
def lista_semestre():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM semestre s, tipo_semestre ts WHERE s.pk_tipo_semestre = ts.pk_tipo_semestre;"
        cursor.execute(sql) 
        datos=cursor.fetchall() 
        semestre=[]
        for fila in datos:
            curso={'s.pk_semestre':fila[0], 's.pk_asignatura':fila[1], 's.pk_tipo_semestre':fila[2], 'fecha':fila[3], 'pk_tipo_semestre':fila[4], 'descrpcion':fila[5]} 
            semestre.append(curso) 
        return jsonify({'semestre':semestre, 'mensaje':'Consulta de las semestres'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'})

@aplicacionSemestre.route('/semestre/<pk_semestre>', methods=['GET']) 
def consultar_semestre(pk_semestre):
    try:
        cursor=conexion.connection.cursor()
        cursor.execute("SELECT * FROM semestre s, tipo_semestre ts WHERE s.pk_tipo_semestre = ts.pk_tipo_semestre AND s.pk_semestre = %s",(int(pk_semestre),))
        datos=cursor.fetchone() 
        if datos != None:
            curso={'pk_semestre':datos[0], 'pk_asignatura':datos[1], 'pk_tipo_semestre':datos[2], 'fecha':datos[3], 'pk_tipo_semestre':datos[4], 'descrpcion':datos[5]}
            return jsonify({'curso':curso, 'mensaje':'semestre encontrados'}) 
        else:
            return jsonify({'mensaje':"semestre no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

@aplicacionSemestre.route('/semestre', methods=['POST'])
def insertar_semestre():
    if(validar_id(request.json['pk_semestre'])):
        try:
            cursor=conexion.connection.cursor()
            sql = "INSERT INTO semestre (pk_semestre, pk_asignatura, pk_tipo_semestre, fecha) VALUES ('%s','%s','%s','%s')"
            datos=cursor.fetchone()
            if datos != None:
                date = datetime.datetime.strptime(datos[3], "%B %d, %Y")
                datos[3] = date.date()
                cursor.execute(sql)
            conexion.connection.commit() 
            return jsonify({'mensaje':'semestre registrado'}) 
        except Exception as ex:
            return jsonify({'mensaje':'Error'}) 
    else:
        return jsonify({'mensaje':'Datos erroneos'})

@aplicacionSemestre.route('/semestre/<pk_semestre>', methods=['DELETE']) 
def eliminar_semestre(pk_semestre):
    try:
        cursor=conexion.connection.cursor()
        cursor.execute("CALL eliminar_semestre(%s)",(int(pk_semestre),))
        conexion.connection.commit() 
        return jsonify({'mensaje':'semestre eliminado'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

@aplicacionSemestre.route('/semestre/<pk_semestre>', methods=['PUT']) 
def actualizar_semestre(pk_semestre): 
    if(validar_id(pk_semestre)):
        try:
            cursor=conexion.connection.cursor()
            cursor.execute("UPDATE semestre SET pk_asignatura = '{0}', pk_tipo_semestre = '{1}',fecha = '{2}'  WHERE pk_semestre = '{3}'".format(request.json['pk_asignatura'], request.json['pk_tipo_semestre'], request.json['fecha'], pk_semestre))
            conexion.connection.commit() 
            return jsonify({'mensaje':'semestre actualizado'}) 
        except Exception as ex:
            return jsonify({'mensaje':'Error'}) 
    else:
        return jsonify({'mensaje':'Datos erroneos'})

def pagina_No_Existe(error):
    return "<h1>La página no existe</h1>",404

def servidor_No_Soporta_HTTP(error):
    return "<h1>La versión HTTP no es compatible</h1>",505

#ejecución aplicacionSemestresemestre
if __name__ == '__main__':
    aplicacionSemestre.config.from_object(configuracion['desarrollo']) 
    aplicacionSemestre.register_error_handler(404, pagina_No_Existe)
    aplicacionSemestre.run()
