from flask import Flask, request, redirect, render_template, session
from sqlalchemy import create_engine, Column, String, Integer, Date, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import date
import os
from datetime import datetime
from propertyForm import createProperty

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

    def __init__(self, propertyname, propertytype, district, bedroom_no, price, psf, listing_date, date_sold, image_url):
        self.propertyname = propertyname
        self.propertytype = propertytype
        self.district = district
        self.bedroom_no = bedroom_no
        self.price = price
        self.psf = psf
        self.listing_date = listing_date
        self.date_sold = date_sold
        self.image_url = image_url

engine = create_engine("sqlite:///viewnest.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
db_session = Session()

# Sample admin creation
admin = SystemAdmin("admin", "password")
db_session.add(admin)
db_session.commit()
"""
# Sample property creation
listing_date1 = date(2024, 4, 4)
property1 = Property("12 Woodlands Street 12", "Landed", "Woodlands", 5, 1200000.00, 2938, listing_date1, None, "https://images.unsplash.com/photo-1559329145-afaf18e3f349?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&dl=k8-9brIbLCo950-unsplash.jpg")
listing_date2 = date(2024, 2, 13)
date_sold2 = date(2024, 4, 3)
property2 = Property("694A Tampines Street 41", "HDB", "Tampines", 3, 690000.00, 1382, listing_date2, date_sold2, "https://stacked-editorial.sgp1.digitaloceanspaces.com/editorial/wp-content/uploads/2022/06/15120942/Tampines-GreenRidges-127-facade.jpg")
db_session.add(property1)
db_session.add(property2)
db_session.commit()  
"""
@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['loginid']
        password = request.form['password']
        user = db_session.query(SystemAdmin).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.ID
            return redirect('/dashboard')
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = db_session.query(SystemAdmin).filter_by(ID=session['user_id']).first()
        if user:
            return f'Welcome, {user.username}!'
    return redirect('/login')

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
                                image_url=image_path)

        db_session.add(new_property)
        db_session.commit()

        return redirect('/') # need to change to view_properties page
    
    return render_template('create_property.html', form=CreateProperty)



@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/view_properties')
def view_properties():
    properties = db_session.query(Property).all()
    return render_template('view_properties.html', properties=properties)

if __name__ == '__main__':
    app.run(debug=True)
