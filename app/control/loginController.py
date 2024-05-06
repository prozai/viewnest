from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import sqlalchemy as sa
from flask import render_template, redirect
from app.entity.models import User
from app.control import bp
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from app.entity.models import User
from flask_login import login_user, logout_user, login_required
from flask import Flask as flask
from app import session


@bp.route('/loginIndex', methods=['GET', 'POST'])
def loginIndex():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(user)
        user = session.query(User).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect('/loginIndex')
        if user.is_authenticated:
            if user.is_active:
                if user.is_anonymous:
                    return redirect('/loginIndex')
                return redirect('/dashboard')
        return redirect('/dashboard')
    return render_template('/login/loginIndex.html', title='Sign In', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/loginIndex')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')