from flask import Blueprint

loginBP = Blueprint('loginroutes', __name__)

from app.boundary import loginBoundary