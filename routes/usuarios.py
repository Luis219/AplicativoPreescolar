from .import app
import os 
from .import notas
from .import validaciones
from .import routes
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, make_response, render_template, request, flash, url_for, redirect, session
from werkzeug.utils import secure_filename

from flask_bcrypt import Bcrypt 



#Validación de usuario
@routes.route("/loginusuario",  methods=['POST'])

def loginusuario():
        "Validar Login de usuarios"
        
    
        login_usuario = app.coleccionUsuarios.find_one({'correo' : request.form['correo'],'rol':'docente','estado':'activo'})
        contrasenia=request.form['contrasenia']
        if login_usuario:
            
            if  app.bcrypt.check_password_hash(login_usuario['contrasenia'],contrasenia):
                session['correo'] = request.form['correo']
                return notas.accederRegistroNota()
            else:
                flash('Error al ingresar usuario')
                return app.usuario()
        else:
                flash('Error al ingresar usuario')
                return app.usuario()
#Permite acceder a la página de registro de un nuevo usuario
@routes.route("/registrousuario.html", methods=['POST', 'GET'])

def accederRegistroUsuario():
    """Retorna pagina de Registro Usuario"""
    roles=app.coleccionRoles.find()
    permisos=app.coleccionPermisos.find()
    return render_template("layouts/registrousuario.html", coleccionRoles=roles, coleccionPermisos=permisos)

#Permite acceder a la página de registro de estudiante
@routes.route("/registroestudiante.html")
def accederestudiante():
    """Retorna Registro Estudiantes"""
    materia=app.coleccionMateria.find()
    roles=app.coleccionRoles.find()

    return render_template("layouts/registroestudiante.html", coleccionMateria=materia, coleccionRoles=roles)

#acceder a la pagina de usuarios registrados
@routes.route("/usuariosregistrados.html")
def accederUsuariosRegistrados():
    """Retorna pagina de usuarios registrados"""
    
    usuarioNombres=app.coleccionUsuarios.find()
    usuarioApellidos=app.coleccionUsuarios.find()
    usuarioCedulas=app.coleccionUsuarios.find()
    usuarioCorreos=app.coleccionUsuarios.find()
    usuarioRoles=app.coleccionUsuarios.find()
    usuarioEstados=app.coleccionUsuarios.find()
    
    return render_template("layouts/usuariosregistrados.html", nombres=usuarioNombres, apellidos=usuarioApellidos,cedulas=usuarioCedulas,correos=usuarioCorreos,roles=usuarioRoles, estados=usuarioEstados)
#Permite acceder a login estudiante
@routes.route("/inicioestudiante.html", methods=['POST', 'GET'])
def accederInicioEstudiante():
    """Retorna pagina de inicio estudiante"""
    if request.method == 'POST':
        
        query={'paralelo':request.form['menuParalelo']}
        usuario=app.coleccionParaleloEstudiante.find(query)
        print(usuario)
        
        return render_template("layouts/inicioestudiante.html", coleccionUsuarios=usuario)
    return render_template("layouts/inicioestudiante.html")
    
    

#Registra un nuevo usuario
@routes.route('/registroUsuario', methods=['POST', 'GET'])
def registroUsuario():
    if request.method == 'POST':
        
        existe_usuario =  app.coleccionUsuarios.find_one({'correo' : request.form['correo']})

        if existe_usuario is None:
            rol=request.form['menuRoles']
            if  validaciones.validarCaracteres(request.form['nombre']) and validaciones.validarCaracteres(request.form['apellido']) and validaciones.validarTelefono(request.form['telefono']) and validaciones.validarEmail(request.form['correo']) and validaciones.validarContrasenia(request.form['contrasenia']):
                if rol=="docente":
                    queryPermiso={"_id":{"$in":[1,2]}}
                
                    permisosDocente=list(app.coleccionPermisos.find(queryPermiso))
                    contrasenia=request.form['contrasenia']

              
                    hashpass = app.bcrypt.generate_password_hash(contrasenia).decode('utf-8') 
                    app.coleccionUsuarios.insert_one({'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'rol':request.form['menuRoles'],'permiso':permisosDocente,  'correo' : request.form['correo'], 'contrasenia' : hashpass,"estado":"activo"})
                    session['nombre'] = request.form['nombre']
                    session['apellido'] = request.form['apellido']
                    session['telefono'] = request.form['telefono']
                    session['correo'] = request.form['correo']
                    session['rol']=request.form['menuRoles']
                    session['permiso']=permisosDocente
                    flash('Registro con exito')
                    return accederRegistroUsuario()
                        
            
                elif rol=="administrador":
                    numeroUsuarios=app.coleccionUsuarios.count_documents({})
                    if numeroUsuarios==0:
                        queryPermiso={"_id":{"$in":[3,4,5,6,7,8]}}
                    
                        permisosAdministrador=list(app.coleccionPermisos.find(queryPermiso))
                        contrasenia=request.form['contrasenia']

                    
                        hashpass = app.bcrypt.generate_password_hash(contrasenia).decode('utf-8') 

                
                        app.coleccionUsuarios.insert_one({'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'rol':request.form['menuRoles'],'permiso':permisosAdministrador,  'correo' : request.form['correo'], 'contrasenia' : hashpass, "estado":"activo"})
                        session['nombre'] = request.form['nombre']
                        session['apellido'] = request.form['apellido']
                        session['telefono'] = request.form['telefono']
                        session['correo'] = request.form['correo']
                        session['rol']=request.form['menuRoles']
                        session['permiso']=permisosAdministrador
                        flash('Registro con exito')
                        return accederRegistroUsuario()
                    flash('Error')    
                    return accederRegistroUsuario()
                flash('Error')    
                return accederRegistroUsuario()
            else:
                    flash('Error-datos ingresados incorrectamente')
                    return accederRegistroUsuario()
            
        return accederRegistroUsuario()
    return accederRegistroUsuario()

    
@routes.route("/validaLoginAdmin", methods=['POST', 'GET'])
#Valida un usuario con el rol administrador
def validaLoginAdmin():
    """Valida Login de admin"""

    
    login_usuarioAdmin = app.coleccionUsuarios.find_one({'correo' : request.form['correo'],'rol':'administrador','estado':'activo'})
    contrasenia=request.form['contrasenia']



    if login_usuarioAdmin:
            
        if  app.bcrypt.check_password_hash(login_usuarioAdmin['contrasenia'],contrasenia):
            session['correo'] = request.form['correo']
 
            return accederRegistroUsuario()
        else:
            flash('Error al acceder')
            return app.loginadmin()
    else:
        flash('Error al acceder')
        return app.loginadmin()
    
#Registro de estudiante
@routes.route('/registroEstudiante', methods=['POST', 'GET'])
def registroEstudiante():
    if request.method == 'POST':
        existe_usuario =  app.coleccionUsuarios.find_one({'cedula' : request.form['cedula']})
        edad=request.form['edad']
        imagen=request.files['imagen']
        filename = secure_filename(imagen.filename)

        contrasenia=request.form['contrasenia']

                
        hashpass = app.bcrypt.generate_password_hash(contrasenia).decode('utf-8') 
        if validaciones.validarCaracteres(request.form['nombre']) and validaciones.validarCaracteres(request.form['apellido']) and validaciones.validarTelefono(request.form['telefono']) and validaciones.validarEdad(request.form['edad']) and validaciones.validarEmail(request.form['correo']) and validaciones.validarContrasenia(contrasenia):
            if existe_usuario is None:
                imagen.save(os.path.join(app.app.config['UPLOAD_FOLDER'], filename))
                app.coleccionUsuarios.insert_one({'imagen':imagen.filename,'cedula' : request.form['cedula'],'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'edad':request.form['edad'],'materia':request.form['menuMateria'],'rol':request.form['menuRoles'],'correo':request.form['correo'],'contrasenia':hashpass,'estado':"activo"})
                flash('Registrado con exito')
                return accederestudiante()
            else:
                flash('Error al registrar')
            return accederestudiante()
        else:
            flash('Error- Datos incorrectos')
            return accederestudiante()


#Sirve para desactivar un usuario
@routes.route('/desactivarUsuario', methods=['POST', 'GET'])
def desactivarUsuario():
    if request.method == 'POST':
        query={"rol":{"$ne":"administrador"},'correo' : request.form['correo']}
        existe_usuario =  app.coleccionUsuarios.find_one(query)
        print("eee")
        print(existe_usuario)
        if existe_usuario is not None and request.form['activardesactivar']=="desactivar":
            actualizacion={"$set":{"estado":"inactivo"}}
            app.coleccionUsuarios.update_one(existe_usuario, actualizacion)
            
            flash('Usuario Desactivado')
        elif existe_usuario and  request.form['activardesactivar']=="activar":
            actualizacion={"$set":{"estado":"activo"}}
            app.coleccionUsuarios.update_one(existe_usuario, actualizacion)
            
            flash('Usuario Activado')
        else:
            flash('Error al Desactivar/Activar usuario')
        

    return render_template('layouts/desactivarusuario.html')