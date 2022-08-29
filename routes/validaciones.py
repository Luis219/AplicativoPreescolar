from .import routes
import re

#expresiones regulares
def validarCedula(cedula):
    '''
    Funcion que valida que numero de cedula tenga 10 digitos
    '''
    if re.search("^(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)$", cedula):
        return True
    else:
        return False
def validarTelefono(telefono):
    '''
    Funcion que valida que numero de telefono tenga 10 digitos
    '''
    if re.search("^[0][9](\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)$", telefono):
        return True
    else:
        return False

def validarCaracteres(cadenaValidar):
    '''
    Funcion que valida que la cadena solo contenga letras
    '''
    if re.match("^[a-zA-Z]*$", cadenaValidar):
        return True
    else:
        return False

def validarEmail(emailValidar):
    '''
    Funcion que valida que el correo solo sea (@gmail.com) o (@espe.edu.ec)
    '''
    if re.match("^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$", emailValidar):
        if re.match("^[a-zA-Z0-9.+_-]+@[gmail]+\.[com]+$", emailValidar):
            return True
        else:
            if re.match("^[a-zA-Z0-9.+_-]+@[espe.edu]+\.[ec]+$", emailValidar):
                return True
            else:
                return False
    else:
        return False

def validarEdad(edad):
    '''
    Funcion que valida que la edad debe estar entre 3 y 5 anios
    '''
    if re.search("^[3-5]$", edad):
        return True
    else:
        return False
def validarContrasenia(contrasenia):
    '''
    Funcion que valida que la longitud de la contrasenia sea igual o mayor a 8
    '''
    if re.search(".{8,}", contrasenia):
        return True
    else:
        return False


def validarNota(nota):
    '''
    Funcion que valida que la nota debe estar entre 0 y 5 anios
    '''
    if re.search("^[0-5]$", nota):
        return True
    else:
        return False
