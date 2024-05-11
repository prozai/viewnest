from flask import Blueprint

loginBP = Blueprint('loginroutes', __name__)
propBP = Blueprint('propRoutes',__name__)
adminBP = Blueprint('adminroutes', __name__)


from app.boundary import systemAdminBoundary
from app.boundary import loginBoundary
from app.boundary import propertyBoundary