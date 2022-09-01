#from distutils.command.config import config

from urllib import request
from flask import Flask, jsonify, request
#importar diccionario configuracion
from configuracion import configuracion
from flask_mysqldb import MySQL
from validacionNota import *

aplicacionAlumno = Flask(__name__)

conexion = MySQL(aplicacionAlumno)

@aplicacionAlumno.route('/nota', methods=['GET'])
def lista_nota():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM nota"
        cursor.execute(sql) 
        datos=cursor.fetchall() 
        nota=[]
        for fila in datos:
            curso={'pk_nota':fila[0], 'pk_alumno':fila[1], 'pk_semestre':fila[2], 'nota':fila[3], 'pk_alumno':fila[4], 'num_nota':fila[5]} 
            nota.append(curso) 
        return jsonify({'nota':nota, 'mensaje':'Consulta de las notas'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

@aplicacionAlumno.route('/nota/<pk_nota>', methods=['GET']) 
def consultar_nota(pk_nota):
    try:
        cursor=conexion.connection.cursor()
        cursor.execute("SELECT * FROM nota WHERE pk_nota = %s",(int(pk_nota),))
        datos=cursor.fetchone()
        if datos != None:
            curso={'pk_nota':datos[0], 'pk_alumno':datos[1], 'pk_semestre':datos[2], 'nota':datos[3], 'pk_alumno':datos[4], 'num_nota':datos[5]} 
            return jsonify({'curso':curso, 'mensaje':'nota encontrados'}) 
        else:
            return jsonify({'mensaje':"nota no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

@aplicacionAlumno.route('/nota', methods=['POST'])
def insertar_nota():
    if(validar_id(request.json['pk_nota'])and validar_nota(request.json['nota'])and validar_num_nota(request.json['num_nota'])):
        try:
            cursor=conexion.connection.cursor()
            sql = "INSERT INTO nota (pk_nota, pk_alumno, pk_semestre, pk_asignatura, nota, num_nota) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(request.json['pk_nota'], request.json['pk_alumno'], request.json['pk_semestre'], request.json['pk_asignatura'], request.json['nota'], request.json['num_nota']) 
            cursor.execute(sql)
            conexion.connection.commit() 
            return jsonify({'mensaje':'nota registrado'}) 
        except Exception as ex:
            return jsonify({'mensaje':'Error'}) 
    else:
        return jsonify({'mensaje':'Datos erroneos'})

@aplicacionAlumno.route('/nota/<pk_nota>', methods=['DELETE']) 
def eliminar_nota(pk_nota):
    try:
        cursor=conexion.connection.cursor()
        cursor.execute("CALL eliminar_nota(%s)",(int(pk_nota),))
        conexion.connection.commit() 
        return jsonify({'mensaje':'nota eliminado'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

@aplicacionAlumno.route('/nota/<pk_nota>', methods=['PUT']) 
def actualizar_nota(pk_nota): 
    if(validar_id(request.json['pk_nota'])and validar_nota(request.json['nota'])and validar_num_nota(request.json['num_nota'])):
        try:
            cursor=conexion.connection.cursor()
            cursor.execute("UPDATE nota SET pk_alumno = '{0}', pk_semestre = '{1}', pk_asignatura = '{2}', nota = '{3}', num_nota = '{4}' WHERE pk_nota = '{5}'".format(request.json['pk_alumno'], request.json['pk_semestre'], request.json['pk_asignatura'], request.json['nota'], request.json['num_nota'], pk_nota))
            conexion.connection.commit() 
            return jsonify({'mensaje':'nota actualizado'}) 
        except Exception as ex:
            return jsonify({'mensaje':'Error'}) 
    else:
        return jsonify({'mensaje':'Datos erroneos'})

def pagina_No_Existe(error):
    return "<h1>La página no existe</h1>",404

def servidor_No_Soporta_HTTP(error):
    return "<h1>La versión HTTP no es compatible</h1>",505

#ejecución aplicacionAlumnonota
if __name__ == '__main__':
    aplicacionAlumno.config.from_object(configuracion['desarrollo']) 
    aplicacionAlumno.register_error_handler(404, pagina_No_Existe)
    aplicacionAlumno.run()
