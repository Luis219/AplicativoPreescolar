from flask import Blueprint
routes = Blueprint('routes', __name__)

from .notas import *
from .asignaciones import *
from .validaciones import *
from .usuarios import *