from flask import Blueprint

bp = Blueprint('route', __name__)

from app.control import routes