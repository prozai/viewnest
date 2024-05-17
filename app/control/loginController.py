from flask import session, redirect
from functools import wraps
from app.entity.models import User
from app import session as sqlalchemy_session
from app.control.propertyController import flask_session

class loginController:

    def login(username, password):
        # Clear the session first
        session.pop('user_id', None)
        session.pop('email', None)
        session.pop('profile_id', None)

        # Call the login function from models.py
        user_info, error = User.login(username, password)

        if user_info:
            # Populate the session with user info
            session['user_id'] = user_info['user_id']
            session['email'] = user_info['email']
            session['profile_id'] = user_info['profile_id']
            return {'redirect': '/dashboard'}
    
        # Return the error if login failed
        return {'error': error} if error else {}

    def dashboard():
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.dashboard(user_id)
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