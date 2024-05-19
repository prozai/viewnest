from flask import Blueprint

loginBP = Blueprint('loginroutes', __name__)
propBP = Blueprint('propRoutes',__name__)
adminBP = Blueprint('adminroutes', __name__)
buyerBP = Blueprint('buyer', __name__)
sellerBP = Blueprint('seller', __name__)
reaBP = Blueprint('REA', __name__)

from app.boundary import systemAdminBoundary
from app.boundary import loginBoundary
from app.boundary import propertyBoundary
from app.boundary import buyerBoundary
from app.boundary import sellerBoundary
from app.boundary import reaBoundary
