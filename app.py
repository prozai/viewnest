from flask import Flask, request, redirect, render_template, session
from sqlalchemy import create_engine, Column, String, Integer, Date, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

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
    sold = Column(Boolean)

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

@app.route('/')
def index():
    return render_template('index.html')

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
