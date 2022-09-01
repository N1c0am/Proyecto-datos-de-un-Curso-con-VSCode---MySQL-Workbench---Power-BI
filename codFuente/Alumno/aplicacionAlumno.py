#from distutils.command.config import config

from urllib import request
from flask import Flask, jsonify, request
#importar diccionario configuracion
from configuracion import configuracion
from flask_mysqldb import MySQL
from validacionAlumno import *


aplicacionAlumno = Flask(__name__)


conexion = MySQL(aplicacionAlumno)

@aplicacionAlumno.route('/alumno', methods=['GET']) 
def lista_alumno():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM alumno"
        cursor.execute(sql) 
        datos=cursor.fetchall() 
        alumno=[]
        for fila in datos:
            curso={'pk_alumno':fila[0], 'pk_semestre':fila[1], 'pk_asignatura':fila[2], 'alu_nombre_alumno':fila[3], 'alu_apellido_alumno':fila[4], 'alu_direccion':fila[5]} 
            alumno.append(curso) 
        return jsonify({'alumno':alumno, 'mensaje':'Consulta de las alumnos'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'})

@aplicacionAlumno.route('/alumno/<pk_alumno>', methods=['GET']) 
def consultar_alumno(pk_alumno):
    try:
        cursor=conexion.connection.cursor()
        cursor.execute("SELECT * FROM alumno WHERE pk_alumno = %s") #En esta ocasión la conulta está protegida en contra de las inyecciones SQL (se utilizan diferentes métodos en cada función CRUD de la aplicación)
        datos=cursor.fetchone() 
        if datos != None:
            curso={'pk_alumno':datos[0], 'pk_semestre':datos[1], 'pk_asignatura':datos[2], 'alu_nombre_alumno':datos[3], 'alu_apellido_alumno':datos[4], 'alu_direccion':datos[5]} 
            return jsonify({'curso':curso, 'mensaje':'alumno encontrados'}) 
        else:
            return jsonify({'mensaje':"alumno no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

@aplicacionAlumno.route('/alumno', methods=['POST'])
def insertar_alumno():
    if(validar_id(request.json['pk_alumno'])and validar_nombre(request.json['alu_nombre_alumno']) and validar_apellido(request.json['alu_apellido_alumno']) and validar_direccion(request.json['alu_direccion'])):
        try:
            cursor=conexion.connection.cursor()
            sql = "INSERT INTO alumno (pk_alumno, pk_semestre, pk_asignatura, alu_nombre_alumno, alu_apellido_alumno, alu_direccion) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(request.json['pk_alumno'], request.json['pk_semestre'], request.json['pk_asignatura'], request.json['alu_nombre_alumno'], request.json['alu_apellido_alumno'], request.json['alu_direccion']) 
            cursor.execute(sql)
            conexion.connection.commit() 
            return jsonify({'mensaje':'alumno registrado'}) 
        except Exception as ex:
            return jsonify({'mensaje':'Error'}) 
    else:
        return jsonify({'mensaje':'Datos erroneos'})

@aplicacionAlumno.route('/alumno/<pk_alumno>', methods=['DELETE']) 
def eliminar_alumno(pk_alumno):
    try:
        cursor=conexion.connection.cursor()
        cursor.execute("CALL eliminar_alumno(%s)",(int(pk_alumno),)) #Se utiliza procedimientos almacenados
        conexion.connection.commit() 
        return jsonify({'mensaje':'alumno eliminado'})
    except Exception as ex:
        return jsonify({'mensaje':'Error'})

@aplicacionAlumno.route('/alumno/<pk_alumno>', methods=['PUT']) 
def actualizar_alumno(pk_alumno): 
    if(validar_id(request.json['pk_alumno'])and validar_nombre(request.json['alu_nombre_alumno']) and validar_apellido(request.json['alu_apellido_alumno']) and validar_direccion(request.json['alu_direccion'])):
        try:
            cursor=conexion.connection.cursor()
            cursor.execute("UPDATE alumno SET pk_semestre = '{0}', pk_asignatura = '{1}', alu_nombre_alumno = '{2}', alu_apellido_alumno = '{3}', alu_direccion = '{4}' WHERE pk_alumno = '{5}'".format(request.json['pk_semestre'], request.json['pk_asignatura'], request.json['alu_nombre_alumno'], request.json['alu_apellido_alumno'], request.json['alu_direccion'], pk_alumno))
            conexion.connection.commit()
            return jsonify({'mensaje':'alumno actualizado'}) 
        except Exception as ex:
            return jsonify({'mensaje':'Error'}) 
    else:
        return jsonify({'mensaje':'Datos erroneos'})

def pagina_No_Existe(error):
    return "<h1>La página no existe</h1>",404

def servidor_No_Soporta_HTTP(error):
    return "<h1>La versión HTTP no es compatible</h1>",505

#ejecución aplicacionAlumno
if __name__ == '__main__':
    aplicacionAlumno.config.from_object(configuracion['desarrollo']) 
    aplicacionAlumno.register_error_handler(404, pagina_No_Existe)
    aplicacionAlumno.run()
