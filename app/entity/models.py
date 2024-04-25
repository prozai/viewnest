from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app import Base, session

#Base = declarative_base()

# User Profile Class
class UserProfile(Base):
    __tablename__ = "user_profile"
    
    profile_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    roles = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)
    user = relationship("User", back_populates="userprofile")

    # Constructor
    def __init__(self, roles, description=None):
        #self.profile_id = profile_id
        self.roles = roles
        self.description = description

    # Get methods
    def get_profile_id(self):
        return self.profile_id
    
    def get_role(self):
        return self.roles
    
    def get_description(self):
        return self.description
    
    # Set methods
    def set_profile_id(self, id):
        self.profile_id = id

    def set_role(self, role):
        self.roles = role

    def set_description(self, description):
        self.description = description

    # Function to create new profile record in DB
    def create_new_profile(self):
        try:
            #with session.begin():
                session.add(self)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error creating new profile: {e}")
        finally:
            session.close()
        
    # Function to retrieve all profile records
    @staticmethod
    def get_all_profiles():
        profiles = session.query(UserProfile).all()
        return profiles

    # Function to retrieve one profile record using profile name
    @staticmethod
    def get_profile_by_name(name):
        profile = session.query(UserProfile).filter(UserProfile.roles==name).one()
        return profile

# User Class
class User(Base):
    __tablename__ = "users_info"

    user_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    profile_id = Column(Integer, ForeignKey('user_profile.profile_id'))
    fname = Column(String(255), nullable=False)
    lname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phonenum = Column(String(8), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    userprofile = relationship("UserProfile", back_populates="user")

    # Constructor
    def __init__(self, profile_id, fname, lname, email, phonenum, username, password_hash):
        self.profile_id = profile_id
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phonenum = phonenum
        self.username = username
        self.password_hash = password_hash

    # Get methods
    def get_user_id(self):
        return self.user_id
    
    def get_profile_id(self):
        return self.profile_id 
    
    def get_fname(self):
        return self.fname
    
    def get_lname(self):
        return self.lname
    
    def get_email(self):
        return self.email
    
    def get_phone_num(self):
        return self.phonenum
    
    def get_username(self):
        return self.username
    
    def get_password_hash(self):
        return self.password_hash

    # Set methods
    def set_profile_id(self, id):
        self.profile_id = id

    def set_fname(self, name):
        self.fname = name

    def set_lname(self, name):
        self.lname = name

    def set_email(self, email):
        self.email = email

    def set_phone_num(self, phonenum):
        self.phonenum = phonenum

    def set_username(self, username):
        self.username = username

    def set_password_hash(self, pw_hash):
        self.password_hash = pw_hash

    # Function to create new account record in DB
    def create_new_account(self):
        try:
            #with session.begin():
                session.add(self)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error creating new account: {e}")
        finally:
            session.close()

    # Function to read all account records in DB
    @staticmethod
    def get_all_accounts():
        users=session.query(User).all()
        return users
    
    # Function to read one account record in DB

    # Function to update account record in DB

    # Function to delete account record in DB

    def __repr__(self):
        return f'User("{self.user_id}","{self.profile_id}""{self.fname}","{self.lname}","{self.email}","{self.username}","{self.phonenum}")'

# Property Class
class Property(Base):
    __tablename__ = "Property"

    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer)
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

    def __init__(self, user_id, propertyname, propertytype, district, bedroom_no, price, psf, listing_date, date_sold, image_url, sold):
        self.user_id = user_id
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