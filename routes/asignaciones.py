import app
from .import routes
from flask import render_template, request, redirect, url_for, flash, Blueprint
import re


#Permite acceder a la página de asignación de parámetros a docente
@routes.route("/asignacion.html", methods=['POST', 'GET'])

def accederAsignacion():
    """Retorna pagina de asignacion"""
    materia=app.coleccionMateria.find()
    paralelo=app.coleccionParalelo.find()
    horarioInicio=app.coleccionHorario.find()
    horarioFin=app.coleccionHorario.find()
    aula=app.coleccionAula.find()
    query={"rol":{"$eq":"docente"}}
    docente=app.coleccionUsuarios.find(query)

    return render_template("layouts/asignacion.html", coleccionMateria=materia, coleccionAula=aula, coleccionParalelo=paralelo, coleccionHorarioInicio=horarioInicio, coleccionHorarioFin=horarioFin,coleccionUsuarios=docente)

    
#Permite acceder a asignacionestudiante
@routes.route("/asignacionestudiante.html")
def accederAsignacionEstudiante():
    """Retorna pagina de asignacione estudiante"""
    query={"rol":{"$eq":"estudiante"}}
    usuario=app.coleccionUsuarios.find(query)
    paralelo=app.coleccionParalelo.find()
    
    return render_template("layouts/asignacionestudiante.html", coleccionUsuarios=usuario,  coleccionCedulas=usuario, coleccionParalelos=paralelo)


#Registro de asignacion de materia, aula y horario a un docente
@routes.route('/registroAsignacion', methods=['POST', 'GET'])
def registroAsignacion():
    if request.method == 'POST':
        existe_usuario =  app.coleccionUsuarios.find_one({'nombre' : request.form['menuDocentes']})
        print(existe_usuario)
        if existe_usuario:

            actualizacion={ "$set":{'materia': request.form['menuMaterias'],'aula': request.form['menuParalelos'],'hora inicio': request.form['menuHorarioInicio'], 'hora fin': request.form['menuHorarioFin']}}
            app.coleccionUsuarios.update_one(existe_usuario,actualizacion)
            flash('Registrado')
        else:
            flash('Error')
            return accederAsignacion()
        return render_template("layouts/asignacion.html")

        #Registro de asignacion de paralelo un docente
@routes.route('/registroAsignacionestudiante', methods=['POST', 'GET'])
def registroAsignacionEstudiante():
    if request.method == 'POST':
        existe_usuario =  app.coleccionUsuarios.find_one({'cedula' : request.form['menuEstudiantes']})
        print(existe_usuario)
        if existe_usuario:

            app.coleccionParaleloEstudiante.insert_one({'paralelo':request.form['menuParalelos'],'cedula' : request.form['menuEstudiantes']})
            print(app.coleccionParaleloEstudiante)
            flash('Registrado')
        else:
            flash('Error')
            return accederAsignacion()
        return render_template("layouts/asignacionestudiante.html")

        