import app
from .import validaciones
from .import notas
from .import routes
from flask import render_template, request, redirect, url_for, flash, Blueprint
import pymongo

#Permite acceder a la página de registro Nota
@routes.route("/registronota.html")
def accederRegistroNota():
    """Retorna pagina de Registro Nota"""
    query={"rol":{"$eq":"estudiante"}}
    usuario=app.coleccionUsuarios.find(query)
    paralelo=app.coleccionParaleloEstudiante.find()
    
    return render_template("layouts/registronota.html", coleccionUsuarios=usuario,coleccionParalelos=paralelo)

    #Registro de Nota
@routes.route('/registroNota', methods=['POST', 'GET'])
def registroNota():
   
    if request.method == 'POST':
        
        if validaciones.validarNota(request.form['calificacion']):
            app.coleccionNota.insert_one({'cedula' : request.form['menuCedula'],'calificacion':request.form['calificacion']})
            flash('Registrado')
            return obtenerDatos()
        else:
            flash('Error al registrar')
            return notas.accederRegistroNota()
    
    return render_template('layouts/registroestudiante.html')

    #Función para generar el reporte de calificaciones
@routes.route('/obtenerDatos', methods=['POST', 'GET'])
def obtenerDatos():
    """Obtención de datos estudiante"""  

    cedula=app.coleccionNota.find()
    calificacion=app.coleccionNota.find()
    
   
    return render_template("layouts/registronota.html", cedulas=cedula,  calificaciones=calificacion)


#Función para obtener puntaje
@routes.route('/obtenerPuntaje', methods=['POST','GET'])
def obtenerPuntaje():
    """Obtención de datos estudiante""" 
    
    if request.method=='POST':

        nuevopuntaje=request.form['data']
        print(nuevopuntaje)
        app.coleccionNota.insert_one({'calificacion':nuevopuntaje})
    

        
        #return ('',204)
        return  url_for('',204)
  
puntajeh=app.coleccionNota.find().limit(1).sort([("_id", pymongo.DESCENDING)])
print(puntajeh)

@routes.route("/puntaje.html")

#retorna la página de calificación de la app
def puntaje():
    
    puntaje=app.coleccionNota.find().limit(1).sort([("_id", pymongo.DESCENDING)])
    return render_template("layouts/puntaje.html",puntajes=puntaje)



