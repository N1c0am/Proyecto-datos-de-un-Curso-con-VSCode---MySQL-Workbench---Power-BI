#from distutils.command.config import config

from urllib import request
from flask import Flask, jsonify, request
#importar diccionario configuracion
from configuracion import configuracion
from flask_mysqldb import MySQL
from validacionAlumno import *

aplicacionAlumnoNota = Flask(__name__)

conexion = MySQL(aplicacionAlumnoNota)

@aplicacionAlumnoNota.route('/alumnoNotaAsignatura', methods=['GET']) 
def lista_nota_alumno_asignatura():
    try:
        cursor=conexion.connection.cursor()
        sql="CALL listadoNotasAlumnoAsignatura"
        cursor.execute(sql) 
        datos=cursor.fetchall() 
        alumno=[]
        for fila in datos:
            curso={'alu_nombre_alumno':fila[0], 'alu_apellido_alumno':fila[1], 'nota':fila[2], 'asig_nombre':fila[3]} 
            alumno.append(curso) 
        return jsonify({'alumno':alumno, 'mensaje':'Consulta de las alumnos'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

@aplicacionAlumnoNota.route('/alumnoNota', methods=['GET']) 
def lista_nota_alumno():
    try:
        cursor=conexion.connection.cursor()
        sql="CALL listadoNotasAlumno"
        cursor.execute(sql) 
        datos=cursor.fetchall() 
        alumno=[]
        for fila in datos:
            curso={'alu_nombre_alumno':fila[0], 'alu_apellido_alumno':fila[1], 'nota':fila[2]} 
            alumno.append(curso) 
        return jsonify({'alumno':alumno, 'mensaje':'Consulta de las alumnos'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

@aplicacionAlumnoNota.route('/promAlumnoNota', methods=['GET']) 
def promedio_nota_alumno():
    try:
        cursor=conexion.connection.cursor()
        sql="CALL promedioNotasAlumno"
        cursor.execute(sql) 
        datos=cursor.fetchall() 
        alumno=[]
        for fila in datos:
            curso={'alu_nombre_alumno':fila[0], 'alu_apellido_alumno':fila[1], 'prom_calif':fila[2]} 
            alumno.append(curso) 
        return jsonify({'alumno':alumno, 'mensaje':'Consulta de las alumnos'}) 
    except Exception as ex:
        return jsonify({'mensaje':'Error'}) 

def pagina_No_Existe(error):
    return "<h1>La página no existe</h1>",404

def servidor_No_Soporta_HTTP(error):
    return "<h1>La versión HTTP no es compatible</h1>",505

#ejecución aplicacionAlumnoNota
if __name__ == '__main__':
    aplicacionAlumnoNota.config.from_object(configuracion['desarrollo']) 
    aplicacionAlumnoNota.register_error_handler(404, pagina_No_Existe)
    aplicacionAlumnoNota.run()
