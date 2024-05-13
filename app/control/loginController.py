from flask import session
from werkzeug.security import check_password_hash
from app.entity.models import User
from app import session as sqlalchemy_session

class loginController:

    def login(username, password):
        session.pop('user_id', None)
        session.pop('email', None)
        if username and password:
            user = sqlalchemy_session.query(User).filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.user_id
                session['email'] = user.email
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

    def logout():
        session.pop('user_id', None)
        session.pop('email', None)
        return {'redirect': 'login'}
    
