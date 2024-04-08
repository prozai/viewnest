from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os.path

app = Flask(__name__)

db_name = "viewnest.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_name)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+ db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']= " "

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
#admin = Admin()

app.app_context().push()

# User Profile Class
class UserProfile(db.Model):
    __tablename__="user_profile"

    id=db.Column(db.String, primary_key=True)
    profile_type=db.Column(db.String, unique=True)

# User Class
class User(db.Model):
    __tablename__ = "users_info"

    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id=db.Column(db.String, db.ForeignKey(UserProfile.id))
    fname=db.Column(db.String(255), nullable=False)
    lname=db.Column(db.String(255), nullable=False)
    email=db.Column(db.String(255), nullable=False)
    username=db.Column(db.String(255), nullable=False)
    phonenum=db.Column(db.String(8), nullable=False)
    pw=db.Column(db.String(255), nullable=False)
    userprofile=db.relationship("UserProfile", backref="user")

    def __init__(self, user_id, fname, lname, email, username, phonenum, pw):
        self.user_id=user_id
        #self.profile_id=profile_id
        self.fname=fname
        self.lname=lname
        self.email=email
        self.username=username
        self.phonenum=phonenum
        self.pw=pw

    def __repr__(self):
        return f'User("{self.id}","{self.fname}","{self.lname}","{self.email}","{self.username}","{self.username}","{self.phonenum}")'

# Admin Class
class Admin(db.Model):
    __tablename__ = "admin_info"

    id=db.Column(db.Integer, primary_key=True,  autoincrement=True)
    profile_id=db.Column(db.String, db.ForeignKey(UserProfile.id))
    username=db.Column(db.String(255), nullable=False)
    pw=db.Column(db.String(255), nullable=False)
    userprofile=db.relationship("UserProfile", backref="admin")

    def __repr__(self):
        return f'Admin("{self.username}","{self.id}")'

# Create all tables
db.create_all()

# Main index 
@app.route('/')
def index():
    return render_template('admin-front-index.html', title="")


@app.route('/admin/index')
def adminIndex():
    return render_template('admin/index.html', title="")

@app.route('/admin/all-user', methods=["POST","GET"])
def adminGetAllUsers():
    users=User.query.all() 
    return render_template('admin/all-user.html',title='All User',users=users)

@app.route('/admin/signup')
def adminSignup():
    return render_template('admin/signup.html', title="")

@app.route('/register', methods=['POST', 'GET'])
def userSignUp():
    if request.method == "POST":
        details = request.form
        id = details.get('id')
        fname = details.get('fname')
        lname = details.get('lname')
        email = details.get('email')
        phonenum = details.get('phonenum')
        username=details.get('username')
        pw = details.get('pw')

        if fname =="" or lname=="" or phonenum=="" or email=="" or pw=="" or username=="":
            flash('Please fill all the field','danger')
            return redirect('/admin/signup')
        else:
            # Check if email already exist
            is_email=User.query.filter_by(email=email).first()
            if is_email:
                flash('Email already exist', 'danger')
                return redirect('/admin/signup')
            else:
                hash_pw=bcrypt.generate_password_hash(pw, 10)
                user=User(id, fname, lname, phonenum, email, username, hash_pw)
                db.session.add(user)
                db.session.commit()
                flash('Account Created Successfully', 'success')
                return redirect('/admin/all-user')

    else:
        return render_template('admin/signup.html',title="Create User Account")

if __name__ == '__main__':
    app.run(debug=True)