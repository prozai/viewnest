from flask_wtf import FlaskForm
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import session
from app.entity.models import User, UserProfile

class RegisterProfile(FlaskForm):
    role = StringField('Role', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Register Profile')

    # Check if role exists
    def validateRole(self, role):
        user_profile = sa.select(UserProfile).where(UserProfile.roles==role)
        user_profile = session.execute(user_profile).scalar_one()
        if user_profile is not None:
            raise ValidationError('Please enter a different profile name.')

class RegisterAccount(FlaskForm):
    profile_list = [('buyer', 'buyer'), ('seller', 'seller'), ('real estate agent', 'real estate agent'), ('admin', 'admin')]
    profile_role = SelectField('Roles', choices=profile_list, validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phonenum = StringField('Phone Number', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Account')

    # Check if username exists
    def validateUsername(self, username):
        user = sa.select(User).where(User.username==username)
        user = session.execute(user).scalar_one()
        if user is not None:
            raise ValidationError('Please enter a different username.')

        # Check if email exists
    def validateEmail(self, email):
        user = sa.select(User).where(User.email==email)
        user = session.execute(user).scalar_one()
        if user is not None:
            raise ValidationError('Please enter a different email.')

# Function to show all existing user records
def showAllAccounts():
    return User.get_all_accounts()

# Function to show all existing user profiles
def showAllProfiles():
    return UserProfile.get_all_profiles()

# Function to update user account info from form

# Function to update user profile info from form

# Function to suspend user account info from form

# Function to suspend user profile info from form

