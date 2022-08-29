
import os
from pickle import TRUE
from flask import Flask, render_template, request, session
import pymongo

from routes import *
from flask_bcrypt import Bcrypt 


#conexion base datos

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="preescolar"
MONGO_COLECCION="usuarios"
MONGO_COLECCIONPERMISOS="permisos"
MONGO_COLECCIONROLES="rols"
MONGO_COLECCIONMATERIA="materia"
MONGO_COLECCIONPARALELO="paralelo"
MONGO_COLECCIONHORARIO="horario"
MONGO_COLECCIONNOTAS="notas"
MONGO_COLECCIONAULAS="aula"
MONGO_COLECCIONSTORAGE="storage"
MONGO_COLECCIONSPARALELO_ESTUDIANTE="paralelo-estudiante"


cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
#base de datos
baseDatos=cliente[MONGO_BASEDATOS]
#colecciones
coleccionUsuarios=baseDatos[MONGO_COLECCION]
coleccionRoles=baseDatos[MONGO_COLECCIONROLES]
coleccionPermisos=baseDatos[MONGO_COLECCIONPERMISOS]
coleccionHorario=baseDatos[MONGO_COLECCIONHORARIO]
coleccionMateria=baseDatos[MONGO_COLECCIONMATERIA]
coleccionParalelo=baseDatos[MONGO_COLECCIONPARALELO]
coleccionNota=baseDatos[MONGO_COLECCIONNOTAS]
coleccionAula=baseDatos[MONGO_COLECCIONAULAS]
coleccionStorage=baseDatos[MONGO_COLECCIONSTORAGE]
coleccionParaleloEstudiante=baseDatos[MONGO_COLECCIONSPARALELO_ESTUDIANTE]
#Encuentra el primer documento
x=coleccionParaleloEstudiante.find()
for i in x:
    print(i)

#instancia de la aplicación
app = Flask(__name__)
app.register_blueprint(routes)
#clave secreta de la aplicación
app.secret_key = "luisparedez123"
#rutas de la carpeta templates/static
app._static_folder = os.path.abspath("templates/static")

UPLOAD_FOLDER = 'imagenescargadas'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


bcrypt = Bcrypt(app)

#página principal del aplicativo
@app.route("/",methods=['POST', 'GET'])

def login():

    imagen=coleccionUsuarios.find()
    query={"rol":{"$eq":"estudiante"}}
    nombre=coleccionUsuarios.find(query)

    return render_template("layouts/estudiante.html", coleccionUsuarios=imagen, nombres=nombre)

#ruta de la página de enseñanza del aplicativo
@app.route("/index.html", methods=['POST', 'GET'])

def index():

    return render_template("layouts/index.html")

@app.route("/evaluacion.html")

#retorna la página del juego
def evaluacion():

    return render_template("layouts/evaluacion.html")


#Permite acceder a la página inicial del aplicativo
@app.route("/estudiante.html")

def estudiante():
    """Retorna a inicio"""
    imagen=coleccionUsuarios.find()


    return render_template("layouts/estudiante.html", coleccionUsuarios=imagen)

#Permite acceder a la página de login usuario
@app.route("/loginusuario.html")
def usuario():
    """Retorna Login de usuario"""


    return render_template("layouts/loginusuario.html")


#Permiter acceder a la página de login admin
@app.route("/loginadmin.html")

def loginadmin():
    """Retorna Login de admin"""


    return render_template("layouts/loginadmin.html")

#Permite acceder la página para desactivar un usuario
@app.route("/desactivarusuario.html")
def removerUsuario():
    """Retorna pagina de desactivacion de docente"""

    return render_template("layouts/desactivarusuario.html")

@app.route("/reporte.html")

#Permite acceder a la página de reporte
def reporte():
    """Retorna pagina de reporte"""

    return render_template("layouts/reporte.html")

queryLog={ "getLog":"startupWarnings"}
    
log=cliente.admin.command(queryLog)


@app.route("/log.html",methods=['POST', 'GET'])

#Permite acceder a la página de log
def verlog():
    """Retorna pagina de reporte"""

    
    return render_template("layouts/log.html", logging=log)
    

    
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug = True)