from flask import Flask, request, flash, redirect, render_template, session
from sqlalchemy import create_engine, Column, String, Integer, Date, Float, Boolean
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import date
import os
from datetime import datetime
from propertyForm import createProperty
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a random secret key

Base = declarative_base()

class SystemAdmin(Base):
    __tablename__ = "SystemAdmin"
    
    ID = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)  # Hash the password

class Property(Base):
    __tablename__ = "Property"

    ID = Column(Integer, primary_key=True)
    propertyname = Column(String)
    propertytype = Column(String)
    district = Column(String)
    bedroom_no = Column(Integer)
    price = Column(Float)
    psf = Column(Integer)
    listing_date = Column(Date)
    date_sold = Column(Date) 
    image_url = Column(String) 
    sold = Column(Boolean, nullable=True, default=False)

    def __init__(self, propertyname, propertytype, district, bedroom_no, price, psf, listing_date, date_sold, image_url, sold):
        self.propertyname = propertyname
        self.propertytype = propertytype
        self.district = district
        self.bedroom_no = bedroom_no
        self.price = price
        self.psf = psf
        self.listing_date = listing_date
        self.date_sold = date_sold
        self.image_url = image_url
        self.sold = sold

engine = create_engine("sqlite:///viewnest.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
db_session = Session()

# Sample admin creation
admin = SystemAdmin("admin", "password")
db_session.add(admin)
db_session.commit()

# Sample property creation
listing_date1 = date(2024, 4, 4)

property1 = Property("12 Woodlands Street 12", "HDB", "Woodlands", 3, 800000.00, 2938, listing_date1, None, "./static/uploads/properties/property1.jpg", False)
listing_date2 = date(2024, 2, 13)
date_sold2 = date(2024, 4, 3)

property2 = Property("29 Tampines Street 41", "Condo", "Tampines", 3, 1200000.00, 1382, listing_date2, date_sold2, "./static/uploads/properties/property2.jpg", True)

# Check if properties already exist before adding them
existing_properties = db_session.query(Property).filter(Property.propertyname.in_(["12 Woodlands Street 12", "694A Tampines Street 41"])).all()

if not existing_properties:
    db_session.add(property1)
    db_session.add(property2)
    db_session.commit()

###########################
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


@app.route('/')
def index():
#    return render_template('admin-front-index.html', title="") #sherna's

    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['loginid']
        password = request.form['password']
        user = db_session.query(SystemAdmin).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.ID
            return redirect('admin-front-index.html')
        else:
            return 'Invalid username or password'
    return render_template('login.html')

#@app.route('/dashboard')
#def dashboard():
    if 'user_id' in session:
        user = db_session.query(SystemAdmin).filter_by(ID=session['user_id']).first()
        if user:
            return f'Welcome, {user.username}!'
    return redirect('/login')



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/view_properties')
def view_properties():
    properties = db_session.query(Property).all()
    return render_template('view_properties.html', properties=properties)
@app.route('/create_property', methods=['GET', 'POST'])
def create_property():
    CreateProperty = createProperty(request.form)
    if request.method == 'POST':
        propertyname = CreateProperty.propertyname.data
        propertytype = CreateProperty.propertytype.data
        district = CreateProperty.district.data
        bedroom_no = CreateProperty.bedroom_no.data
        price = CreateProperty.price.data
        psf = CreateProperty.psf.data
        image_file = request.files.get('image_url')
        
        if image_file:
            filename = secure_filename(image_file.filename)
            app.config['UPLOAD_FOLDER'] = './static/uploads/properties/'
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        else:
            image_path = None
        
        new_property = Property(propertyname=propertyname,
                                propertytype=propertytype,
                                district=district,
                                bedroom_no=bedroom_no,
                                price=price,
                                psf=psf,
                                listing_date=datetime.now().date(),
                                date_sold=None,
                                image_url=image_path,
                                sold=False)

        db_session.add(new_property)
        db_session.commit()

        return redirect('/view_properties') # need to change to view_properties page
    
    return render_template('create_property.html', form=CreateProperty)

#Admin

@app.route('/homepage.html')
def homepage():
    return render_template('homepage.html', title="")



@app.route('/admin-front-index.html')
def adminFrontIndex():
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
