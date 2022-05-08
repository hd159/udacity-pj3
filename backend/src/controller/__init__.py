from flask import Blueprint
routes = Blueprint('routes', __name__)

from .drink import *
from .auth import *
from .errors_handling import *