from flask import session, redirect
from functools import wraps
from werkzeug.security import check_password_hash
from app.entity.models import User
from app import session as sqlalchemy_session
from app.control.propertyController import flask_session

class loginController:

    def login(username, password):
        session.pop('user_id', None)
        session.pop('email', None)
        if username and password:
            user = sqlalchemy_session.query(User).filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.user_id
                session['email'] = user.email
                session['profile_id'] = user.profile_id
                return {'redirect': '/dashboard'}
            error = 'Incorrect username or password. Please try again.'
            return {'error': error}
        return {}

    def dashboard():
        if 'user_id' in session:
            user_id = session['user_id']
            
            user = sqlalchemy_session.query(User).filter_by(user_id=user_id).first()
            if user:
                return {'template': '/login/dashboard.html', 'user': user}
        return {'redirect': '/login'}
    
    def login_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect('/login')
            return func(*args, **kwargs)
        return decorated_function

    def rea_authentication(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or session.get('profile_id') != 3:
                return redirect('/login/access-denied')
            return func(*args, **kwargs)
        return decorated_function

    def sysadmin_authentication(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or session.get('profile_id') != 4:
                return redirect('/login/access-denied')
            return func(*args, **kwargs)
        return decorated_function