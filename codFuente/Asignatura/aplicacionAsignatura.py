#from distutils.command.config import config

from urllib import request
from flask import Flask, jsonify, request
#importar diccionario configuracion
from configuracion import configuracion
from flask_mysqldb import MySQL
from validacionAsignatura import *

aplicacionAsignatura = Flask(__name__)

conexion = MySQL(aplicacionAsignatura)

@aplicacionAsignatura.route('/asignatura', methods=['GET'])
def lista_Asignatura():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM asignatura"
        cursor.execute(sql)
        datos=cursor.fetchall()
        asignatura=[]
        for fila in datos:
            curso={'pk_asignatura':fila[0], 'asig_nombre':fila[1], 'asig_descripcion':fila[2]}
            asignatura.append(curso)#
        return jsonify({'asignatura':asignatura, 'mensaje':'Consulta de las Asignaturas'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'})

@aplicacionAsignatura.route('/asignatura/<pk_asignatura>', methods=['GET']) 
def consultar_Asignatura(pk_asignatura):
    try:
        cursor=conexion.connection.cursor()
        cursor.execute("SELECT * FROM asignatura WHERE pk_asignatura = %s",(int(pk_asignatura),))
        datos=cursor.fetchone() 
        if datos != None:
            curso={'idCurso':datos[0], 'nombreCurso':datos[1]} 
            return jsonify({'curso':curso, 'mensaje':'Asignatura encontrados'}) 
        else:
            return jsonify({'mensaje':"Asignatura no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':'Error'})

#registrar
@aplicacionAsignatura.route('/asignatura', methods=['POST'])
def insertar_Asignatura():
    if(validar_id(request.json['pk_asignatura'])and validar_nombre(request.json['asig_nombre'])):
        try:
            cursor=conexion.connection.cursor()
            sql = "INSERT INTO asignatura (pk_asignatura, asig_nombre, asig_descripcion) VALUES ('{0}','{1}','{2}')".format(request.json['pk_asignatura'], request.json['asig_nombre'], request.json['asig_descripcion'])
            cursor.execute(sql)
            conexion.connection.commit()#
            return jsonify({'mensaje':'Asignatura registrado'}) 
        except Exception as ex:
            return jsonify({'mensaje':'Error'})
    else:
        return jsonify({'mensaje':'Datos erroneos'})

@aplicacionAsignatura.route('/asignatura/<pk_asignatura>', methods=['DELETE']) 
def eliminar_Asignatura(pk_asignatura):
    try:
        cursor=conexion.connection.cursor()
        cursor.execute("CALL eliminar_asignatura(%s)",(int(pk_asignatura),))
        conexion.connection.commit()
        return jsonify({'mensaje':'Asignatura eliminado'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

@aplicacionAsignatura.route('/asignatura/<pk_asignatura>', methods=['PUT']) 
def actualizar_Asignatura(pk_asignatura): 
    if(validar_id(pk_asignatura)and validar_nombre(request.json['asig_nombre'])):
        try:
            cursor=conexion.connection.cursor()
            cursor.execute("UPDATE asignatura SET asig_nombre = '{0}' WHERE pk_asignatura = '{1}'".format(request.json['asig_nombre'], pk_asignatura))
            conexion.connection.commit()
            return jsonify({'mensaje':'Asignatura actualizado'})
        except Exception as ex:
            return jsonify({'mensaje':'Error'})
    else:
        return jsonify({'mensaje':'Datos erroneos'})

def pagina_No_Existe(error):
    return "<h1>La página no existe</h1>",404

def servidor_No_Soporta_HTTP(error):
    return "<h1>La versión HTTP no es compatible</h1>",505

#ejecución aplicacionAsignatura
if __name__ == '__main__':
    aplicacionAsignatura.config.from_object(configuracion['desarrollo']) 
    #aplicacionAsignatura.run(debug=True) #se reinicia el servidor automtic cuando se hace un cambio
    aplicacionAsignatura.register_error_handler(404, pagina_No_Existe)
    aplicacionAsignatura.run()
