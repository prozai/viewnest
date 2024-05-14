from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Float
from sqlalchemy.orm import relationship
from app import Base, session
from datetime import date
from sqlalchemy.ext.declarative import declarative_base



# User Profile Class
class UserProfile(Base):
    __tablename__ = "user_profile"
    
    profile_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    roles = Column(String(255), unique=True)
    description = Column(String(255), nullable=True)
    suspend_status = Column(Boolean, nullable=False)
    user = relationship("User", back_populates="userprofile")

    # Constructor
    def __init__(self, roles, description=None):
        #self.profile_id = profile_id
        self.roles = roles
        self.description = description
        self.suspend_status = False

    # Get methods
    def get_profile_id(self):
        return self.profile_id
    
    def get_role(self):
        return self.roles
    
    def get_description(self):
        return self.description
    
    def get_suspend_status(self):
        return self.suspend_status
    
    # Set methods
    def set_profile_id(self, id):
        self.profile_id = id

    def set_role(self, role):
        self.roles = role

    def set_description(self, description):
        self.description = description

    def set_suspend_status(self, status):
        self.suspend_status = status

    # Function to create new profile record in DB
    @classmethod
    def create_new_profile(cls, profile):
        try:
            #with session.begin():
                session.add(profile)
                session.commit()
                session.close()
                return True
        except Exception as e:
            session.rollback()
            print(f"Error creating new profile: {e}")
            session.close()
            return False
                    
    # Function to retrieve all profile records
    @classmethod
    def get_all_profiles(cls):
        profiles = session.query(cls).filter(cls.suspend_status==False).all()
        return profiles

    # Function to retrieve one profile record using profile name
    @classmethod
    def get_profile_by_name(cls, name):
        profile = session.query(cls).filter(cls.roles==name).first()
        return profile

    # Function to update profile information
    @classmethod
    def update_profile(cls, current_role, name, description):
        try:
            profile = session.query(cls).filter(cls.roles==current_role).first()
            profile.set_role(name)
            profile.set_description(description)
            session.commit()
            session.close()
            return True
        
        except Exception as e:
            session.rollback()
            print(f"Error updating profile: {e}")
            session.close()
            return False

    # Function to suspend profile
    @classmethod
    def suspend_profile(cls, role):
        try:
            profile = session.query(cls).filter(cls.roles==role).first()
            profile.set_suspend_status(True) 
            session.commit()
            session.close()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error suspending profile: {e}")
            session.close()
            return False

    # Function to search profile
    @classmethod
    def searchProfile(cls, search_term, attribute):
        if attribute == 'profile_id':
            profiles = session.query(cls).filter(cls.profile_id==search_term).all()
        elif attribute == 'roles':
            profiles = session.query(cls).filter(cls.roles==search_term).all()
        elif attribute == 'description':
            profiles = session.query(cls).filter(cls.description.contains(search_term)).all()
        
        return profiles
            

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
    suspend_status = Column(Boolean, nullable=False)
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
        self.suspend_status = False

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
    
    def get_suspend_status(self):
        return self.suspend_status

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

    def set_suspend_status(self, status):
        self.suspend_status = status

    # Function to create new account record in DB
    @classmethod
    def create_new_account(cls, account):
        try:
            #with session.begin():
                session.add(account)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error creating new account: {e}")
        finally:
            session.close()

    # Function to read all account records in DB
    @classmethod
    def get_all_accounts(cls):
        users=session.query(cls).filter(cls.suspend_status==False).all()
        return users
    
    # Function to search account record in DB

    # Function to update account record in DB
    @classmethod
    def update_account(cls, username, new_fname, new_lname, new_email, new_phone_num, new_password_hash):
        try:
            account = session.query(cls).filter(cls.username==username).first()
            if new_fname != "":
                account.set_fname(new_fname)
            if new_lname != "":
                account.set_lname(new_lname)
            if new_email != "":
                account.set_email(new_email)
            if new_phone_num != "":
                account.set_phone_num(new_phone_num)
            if new_password_hash != "":
                account.set_password_hash(new_password_hash)
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # Function to suspend account record 
    @classmethod
    def suspend_account(cls, username):
        try:
            account = session.query(cls).filter(cls.username==username).first()
            account.set_suspend_status(True) 
            session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def __repr__(self):
        return f'User("{self.user_id}","{self.profile_id}""{self.fname}","{self.lname}","{self.email}","{self.username}","{self.phonenum}")'

#added during integration
    def is_system_admin(self):
        # Assuming roles is a string containing comma-separated roles
        roles = self.userprofile.roles.split(', ')
        return 'system admin' in roles
    
    
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
    selleremail = Column(String)
    listing_date = Column(Date)
    date_sold = Column(Date)
    image_url = Column(String) 
    sold = Column(Boolean)
    view_count = Column(Integer, default=0)
    saves = Column(Integer, default=0)

    def __init__(self, user_id, propertyname, propertytype, district, bedroom_no, price, psf, selleremail, listing_date, date_sold, image_url, sold):
        self.user_id = user_id
        self.propertyname = propertyname
        self.propertytype = propertytype
        self.district = district
        self.bedroom_no = bedroom_no
        self.price = price
        self.psf = psf
        self.selleremail = selleremail
        self.listing_date = listing_date
        self.date_sold = date_sold
        self.image_url = image_url
        self.sold = sold

    def get_property_id(self):
        return self.ID
    
 # Save Class   
class Save(Base):
    __tablename__ = "Save"

    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    property_id = Column(Integer)

    def __init__(self, user_id, property_id):
        self.user_id = user_id
        self.property_id = property_id

class Review(Base):
    __tablename__ = "review"
    review_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    review = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users_info.user_id'))

    def __init__(self, review, rating, user_id, review_id=None):
        self.review = review
        self.rating = rating
        self.user_id = user_id
        self.review_id = review_id

    def get_review_id(self):
        return self.review_id
    
    def get_review(self):
        return self.review
    
    def get_rating(self):
        return self.rating
    
    def get_user_id(self):
        return self.user_id
    
    def set_review_id(self, id):
        self.review_id = id

    def set_review(self, review):
        self.review = review

    def set_rating(self, rating):
        self.rating = rating

    def set_user_id(self, id):
        self.user_id = id

    @classmethod
    def create_new_review(cls, review):
        try:
            session.add(review)
            session.commit()
            return 200
        except Exception as e:
            session.rollback()
            print(f"Error creating new review: {e}")
            return 500
        finally:
            session.close()
    
    @classmethod
    def get_all_reviews(cls):
        reviews = session.query(cls).all()
        return reviews
    
    @classmethod
    def get_review_by_id(cls, id):
        review = session.query(cls).filter(cls.review_id==id).first()
        return review
    

    def __repr__(self):
        return f'User("{self.user_id}","{self.review}","{self.rating}","{self.review_id}")'