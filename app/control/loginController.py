from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
from app.entity.models import User
from app import session as sqlalchemy_session

loginBP = Blueprint('loginroutes', __name__)

@loginBP.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user_id', None)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = sqlalchemy_session.query(User).filter_by(username=username).first()
            if user:
                if check_password_hash(user.password_hash, password):
                    session['user_id'] = user.user_id
                    return redirect('/dashboard')
            error = 'Incorrect username or password. Please try again.'
            return render_template('/login/login.html', error=error)

    return render_template('/login/login.html', error=None)


@loginBP.route('/dashboard')
def dashboard():

    if 'user_id' in session:
        user_id = session['user_id']
        user = sqlalchemy_session.query(User).filter_by(user_id=user_id).first()
        if user:
            return render_template('/login/dashboard.html', user=user)
        else:
            return redirect('/login/login.html')
    else:
        return redirect('/login')

@loginBP.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect('/login')