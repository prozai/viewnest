from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Float
from sqlalchemy.orm import relationship
from app import Base, session
from datetime import date
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash
from sqlalchemy import desc

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
            #check if role exist
            role_exist = session.query(cls).filter(cls.roles==profile.roles).first() is not None
            if role_exist:
                return False
            
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
    def update_profile(cls, current_role, description):
        try:
            profile = session.query(cls).filter(cls.roles==current_role).first()
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
            if profile is None:
                return False
            
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
    def searchProfile(cls, search_term):
        profiles = session.query(cls) \
                    .filter(cls.suspend_status == False) \
                    .filter((cls.profile_id.contains(search_term)) |  cls.roles.contains(search_term) | cls.description.contains(search_term)) \
                    .all()

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
                return True
        except Exception as e:
            session.rollback()
            print(f"Error creating new account: {e}")
            return False
        finally:
            session.close()

    # Function to check email
    @classmethod
    def check_email(cls, email):
        email_exist = session.query(cls).filter(cls.email==email).first() is not None
        return email_exist
    
     # Function to check phone num
    @classmethod
    def check_phonenum(cls, phonenum):
        phone_num_exist = session.query(cls).filter(cls.phonenum==phonenum).first() is not None
        return phone_num_exist
    
    # Function to check username
    @classmethod
    def check_username(cls, username):
        username_exist = session.query(cls).filter(cls.username==username).first() is not None
        return username_exist


    # Function to read all account records in DB
    @classmethod
    def get_all_accounts(cls):
        users=session.query(cls).filter(cls.suspend_status==False).all()
        return users

    # Function to read one account record 
    @classmethod
    def get_account_by_user_id(cls, user_id):
        user = session.query(cls).filter(cls.user_id==user_id).all()
        return user

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
            if account is not None:
                account.set_suspend_status(True) 
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    # Function to search account
    @classmethod
    def searchAccount(cls, search_term):
        subquery = session.query(UserProfile.profile_id).filter(UserProfile.roles.contains(search_term)).subquery()

        users = session.query(cls) \
                    .filter(cls.suspend_status == False) \
                    .filter(cls.user_id.contains(search_term) |  
                             cls.fname.contains(search_term) | 
                             cls.lname.contains(search_term) | 
                             cls.email.contains(search_term) | 
                             cls.phonenum.contains(search_term) | 
                             cls.username.contains(search_term) | 
                             cls.profile_id.in_(subquery)) \
                    .all()

        return users 
     # Function to retrieve REA ID by email
    @classmethod
    def retrieve_rea_id_by_email(cls, email):
        rea = session.query(cls).filter(cls.email==email).first()
        return rea.user_id
                       
    def __repr__(self):
        return f'User("{self.user_id}","{self.profile_id}""{self.fname}","{self.lname}","{self.email}","{self.username}","{self.phonenum}")'
    
    def login(username, password):
        if username and password:
            user = session.query(User).filter_by(username=username).first()
            if user:
                if user.suspend_status:
                    return None, 'User account is currently suspended.'
                if check_password_hash(user.password_hash, password):
                    user_info = {
                        'user_id': user.user_id,
                        'email': user.email,
                        'profile_id': user.profile_id
                    }
                    return user_info, None
                return None, 'Incorrect username or password. Please try again.'
            return None, 'Incorrect username or password. Please try again.'
        return None, 'Username and password must be provided.'


    def dashboard(user_id):
        user = session.query(User).filter_by(user_id=user_id).first()
        return user
    
# Function to read one account record 
    @classmethod
    def get_account_by_username(cls, username):
        user = session.query(cls).filter(cls.username==username).first()
        return user
    
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

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'propertyname': self.propertyname,
            'propertytype': self.propertytype,
            'district': self.district,
            'bedroom_no': self.bedroom_no,
            'price': self.price,
            'psf': self.psf,
            'selleremail': self.selleremail,
            'listing_date': self.listing_date.isoformat() if self.listing_date else None,
            'date_sold': self.date_sold.isoformat() if self.date_sold else None,
            'image_url': self.image_url,
            'sold': self.sold,
            'view_count': self.view_count,
            'saves': self.saves
        }
    
    def view_properties(offset, limit, filter_type):
        query = session.query(Property)

        # Apply filter if specified
        if filter_type == 'available':
            query = query.filter_by(sold=False)
        elif filter_type == 'sold':
            query = query.filter_by(sold=True)

        # Execute the query with offset and limit
        properties = query.offset(offset).limit(limit).all()

        # Serialize the properties
        serialized_properties = []
        for prop in properties:
            serialized_properties.append({
                'id': prop.ID,
                'propertyname': prop.propertyname,
                'propertytype': prop.propertytype,
                'district': prop.district,
                'bedroom_no': prop.bedroom_no,
                'price': prop.price,
                'psf': prop.psf,
                'selleremail': prop.selleremail,
                'listing_date': prop.listing_date.isoformat() if prop.listing_date else None,
                'date_sold': prop.date_sold.isoformat() if prop.date_sold else None,
                'image_url': prop.image_url,
                'sold': prop.sold,
                'view_count': prop.view_count,
                'saves': prop.saves
            })

        return serialized_properties

    def view_property_detail(property_id):
        try:
            property = session.query(Property).filter_by(ID=property_id).first()
            return property
        except Exception as e:
            print(f"Error fetching property: {e}")
            return None
        finally:
            session.close()

    def get_property_id(self):
        return self.ID
    
    def get_max_id(id):
        max_id = session.query(Property).order_by(desc(id)).first()
        return max_id

    def create_property(new_property):
        try:
            session.add(new_property)
            session.commit()
        except Exception as e:
            print("Error creating property:", str(e))
        finally:
            session.close()
    
    def get_REAproperties(user_id):
        properties = session.query(Property).filter_by(user_id=user_id).all()
        return properties

    def update_property():
        try:
            session.commit()
        except Exception as e:
            print("Error creating property:", str(e))
        finally:
            session.close()

    def delete_property(property):
        try:
            session.delete(property)
            session.commit()
        except Exception as e:
            print("Error creating property:", str(e))
        finally:
            session.close()

    def get_property_by_id(id):
        property = session.query(Property).filter_by(ID=id).first()
        return property
    
    def add_save_new(property):
        try:
            property.saves += 1
            session.commit()
        except Exception as e:
            print("Error creating property:", str(e))
        finally:
            session.close()

    def add_save_sold(property):
        try:
            property.saves += 1
            session.commit()
        except Exception as e:
            print("Error creating property:", str(e))
        finally:
            session.close()

    def minus_save_new(property):
        try:
            property.saves -= 1
            session.commit()
        except Exception as e:
            print("Error creating property:", str(e))
        finally:
            session.close()

    def minus_save_sold(property):
        try:
            property.saves -= 1
            session.commit()
        except Exception as e:
            print("Error creating property:", str(e))
        finally:
            session.close()
        
    def get_sellerproperties(email):
        properties = session.query(Property).filter_by(selleremail=email).all()
        return properties
    
    def search_by_name(search_query):
            # Split the search query into individual keywords
        keywords = search_query.split()

        return session.query(Property).filter(
        *[Property.propertyname.like(f'%{keyword}%') for keyword in keywords]
    ).all()


    def search_by_sold(search_query):
    # Split the search query into individual keywords
         keywords = search_query.split()

         return session.query(Property).filter(
        *[Property.propertyname.like(f'%{keyword}%') for keyword in keywords],
        Property.sold == 1  # Add this condition to filter sold properties
    ).all()
         
    def search_by_avail(search_query):
    # Split the search query into individual keywords
         keywords = search_query.split()

         return session.query(Property).filter(
        *[Property.propertyname.like(f'%{keyword}%') for keyword in keywords],
        Property.sold == 0  # Add this condition to filter sold properties
    ).all()
         
    def search_by_REA_Properties(search_query, userid):
    # Split the search query into individual keywords
         keywords = search_query.split()

         return session.query(Property).filter(
        *[Property.propertyname.like(f'%{keyword}%') for keyword in keywords],
        Property.user_id == userid  
    ).all()



    def load_more_properties(offset, limit, filter_type):
        properties = Property.view_properties(offset, limit, filter_type)
        return properties

    def add_ViewCount(property_id):
        try:
            property = session.query(Property).filter_by(ID=property_id).first()
            if property:
                property.view_count += 1
                session.commit()
                return property
        except Exception as e:
                session.rollback()
                print(f"Error fetching property: {e}")
                return None
        finally:
            session.close()
    
    
 # Save Class   
class Save(Base):
    __tablename__ = "Save"

    ID = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    property_id = Column(Integer)

    def __init__(self, user_id, property_id):
        self.user_id = user_id
        self.property_id = property_id
        
    def get_save(user_id, property_id):
        save = session.query(Save).filter_by(user_id=user_id, property_id=property_id).first()
        return save

    def delete_save_new(saved):
        try:
            session.delete(saved)
        except Exception as e:
            print("Error deleting save:", str(e))

    def delete_save_sold(saved):
        try:
            session.delete(saved)
        except Exception as e:
            print("Error deleting save:", str(e))

    def create_save_new(new_save):
        try:
            session.add(new_save)
        except Exception as e:
            print("Error deleting save:", str(e))

    def create_save_sold(new_save):
        try:
            session.add(new_save)
        except Exception as e:
            print("Error deleting save:", str(e))
        
    def is_saved(user_id, property_id):
        saved = session.query(Save).filter_by(user_id=user_id, property_id=property_id).first()
        if saved:
            is_saved = True
        else:
            is_saved = False

        return is_saved

class Review(Base):
    __tablename__ = "review"
    review_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    review = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users_info.user_id'))
    rea_id = Column(Integer, ForeignKey('users_info.user_id'))
    def __init__(self, review, rating, user_id, rea_id, review_id=None):
        self.review = review
        self.rating = rating
        self.user_id = user_id
        self.rea_id = rea_id
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
    def get_rea_id_by_email(cls, email):
        try:
            rea = session.query(cls).filter(cls.email == email).first()
            if rea:
                return rea.user_id
            else:
                return None
        except Exception as e:
            print(f"Error getting REA ID by email: {e}")
            return None
    
    @classmethod
    def get_all_reviews(cls):
        reviews = session.query(cls).all()
        return reviews
    
    @classmethod
    def get_reviews_by_rea_id(cls, rea_id):
        reviews = session.query(cls).filter(cls.rea_id==rea_id).all()
        return reviews

    @classmethod
    def get_review_by_id(cls, id):
        review = session.query(cls).filter(cls.review_id==id).first()
        return review
    

    def __repr__(self):
        return f'User("{self.user_id}","{self.review}","{self.rating}","{self.review_id}", "{self.rea_id}")'
