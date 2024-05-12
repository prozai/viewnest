from flask import Blueprint

adminBP = Blueprint('adminroutes', __name__)
mainBP = Blueprint('routes', __name__)
buyerBP = Blueprint('buyer', __name__)

from app.control import adminController, mainController
